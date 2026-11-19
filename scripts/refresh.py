#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auto-refresh data feeds for Home.Direct (run by GitHub Actions every 6 hours).

- data/rates.json   Freddie Mac PMMS 30/15-yr averages via FRED CSV (no API key)
- data/news.json    Housing & home-improvement headlines via Google News RSS (title + link + source only)
- data/videos.json  Latest uploads from home channels via YouTube RSS (no API key)

Standard library only. Every feed fails soft: if a source is down, the previous file is kept.
"""
import datetime as dt
import email.utils
import html
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SOURCES = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))
UA = "Mozilla/5.0 (compatible; HomeDotDirectBot/1.0; +https://home.direct)"
NOW = dt.datetime.now(dt.timezone.utc)


def get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def save(name, obj):
    (DATA / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  wrote data/{name}")


def label(d):
    return d.strftime("%b %-d, %Y")


# ---------------------------------------------------------------- rates
def fred(series):
    txt = get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}")
    rows = []
    for line in txt.strip().splitlines()[1:]:
        parts = line.split(",")
        if len(parts) == 2 and parts[1] not in (".", ""):
            rows.append([parts[0], float(parts[1])])
    return rows


def refresh_rates():
    print("rates…")
    try:
        s30, s15 = fred("MORTGAGE30US"), fred("MORTGAGE15US")
        if len(s30) < 3 or len(s15) < 3:
            raise ValueError("short series")
        last = s30[-1][0]
        d = dt.date.fromisoformat(last)
        ago = d - dt.timedelta(days=365)

        def year_ago(s):
            c = [v for k, v in s if dt.date.fromisoformat(k) <= ago]
            return c[-1] if c else None
        save("rates.json", {
            "updated": NOW.isoformat(timespec="seconds"), "source": "Freddie Mac Primary Mortgage Market Survey (PMMS) via FRED",
            "as_of": last, "as_of_label": "week of " + label(d),
            "r30": s30[-1][1], "r15": s15[-1][1], "r30_prev": s30[-2][1], "r15_prev": s15[-2][1],
            "r30_year_ago": year_ago(s30), "r15_year_ago": year_ago(s15),
            "series30": s30[-53:], "series15": s15[-53:]})
    except Exception as e:  # keep previous file
        print("  rates skipped:", e)


# ---------------------------------------------------------------- news
def refresh_news():
    print("news…")
    items, seen, per_cat = [], set(), {}
    for q in SOURCES["news_queries"]:
        url = "https://news.google.com/rss/search?" + urllib.parse.urlencode({"q": q["q"] + " when:3d", "hl": q.get("hl", "en-US"), "gl": q.get("gl", "US"), "ceid": q.get("ceid", "US:en")})
        try:
            root = ET.fromstring(get(url))
        except Exception as e:
            print("  feed failed:", q["q"], e)
            continue
        for it in root.iter("item"):
            title = html.unescape(it.findtext("title") or "").strip()
            link = (it.findtext("link") or "").strip()
            src_el = it.find("source")
            source = (src_el.text or "").strip() if src_el is not None else ""
            if source and title.endswith(" - " + source):
                title = title[: -len(" - " + source)]
            key = re.sub(r"\W+", "", title.lower())[:80]
            if not title or not link or key in seen:
                continue
            low = title.lower()
            if "|" in title or len(title.split()) < SOURCES.get("news_min_words", 6):
                continue  # SEO landing pages and fragments, not news
            if any(b.lower() in low for b in SOURCES.get("news_block_words", [])):
                continue
            if any(b.lower() in source.lower() for b in SOURCES.get("news_block_sources", [])):
                continue
            if per_cat.get(q["cat"], 0) >= SOURCES.get("news_cap_per_cat", 14):
                continue
            try:
                pub = email.utils.parsedate_to_datetime(it.findtext("pubDate"))
            except Exception:
                pub = NOW
            seen.add(key)
            per_cat[q["cat"]] = per_cat.get(q["cat"], 0) + 1
            items.append({"title": title, "link": link, "source": source, "cat": q["cat"], "date": pub.isoformat(), "date_label": label(pub)})
    if len(items) >= 6:
        items.sort(key=lambda x: x["date"], reverse=True)
        save("news.json", {"updated": NOW.isoformat(timespec="seconds"), "updated_label": NOW.strftime("%b %-d, %Y %H:%M UTC"), "items": items[:80]})
    else:
        print("  news skipped: too few items")


# ---------------------------------------------------------------- videos
def channel_id(ch):
    if ch.get("id"):
        return ch["id"]
    page = get("https://www.youtube.com/" + ch["handle"])
    m = re.search(r'"(?:channelId|externalId)":"(UC[\w-]{22})"', page) or re.search(r"youtube\.com/channel/(UC[\w-]{22})", page)
    return m.group(1) if m else None


def refresh_videos():
    print("videos…")
    ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015", "media": "http://search.yahoo.com/mrss/"}
    items = []
    for ch in SOURCES["youtube_channels"]:
        try:
            cid = channel_id(ch)
            if not cid:
                raise ValueError("no channel id")
            root = ET.fromstring(get("https://www.youtube.com/feeds/videos.xml?channel_id=" + cid))
        except Exception as e:
            print("  channel failed:", ch.get("name"), e)
            continue
        n = 0
        for en in root.findall("a:entry", ns):
            vid = en.findtext("yt:videoId", namespaces=ns)
            title = (en.findtext("a:title", namespaces=ns) or "").strip()
            pub = en.findtext("a:published", namespaces=ns) or NOW.isoformat()
            if not vid or not title:
                continue
            if any(w.lower() in title.lower() for w in SOURCES.get("video_skip_words", [])):
                continue
            try:
                pdt = dt.datetime.fromisoformat(pub.replace("Z", "+00:00"))
            except Exception:
                pdt = NOW
            items.append({"id": vid, "title": html.unescape(title), "channel": ch["name"], "date": pdt.isoformat(), "date_label": label(pdt)})
            n += 1
            if n >= ch.get("max", 6):
                break
    if len(items) >= 6:
        items.sort(key=lambda x: x["date"], reverse=True)
        save("videos.json", {"updated": NOW.isoformat(timespec="seconds"), "updated_label": NOW.strftime("%b %-d, %Y %H:%M UTC"), "items": items[:36]})
    else:
        print("  videos skipped: too few items")


if __name__ == "__main__":
    only = sys.argv[1:] or ["rates", "news", "videos"]
    if "rates" in only:
        refresh_rates()
    if "news" in only:
        refresh_news()
    if "videos" in only:
        refresh_videos()
