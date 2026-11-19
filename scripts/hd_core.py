# -*- coding: utf-8 -*-
"""Home.Direct static-site core: layout, SEO head, icons, form components.
No third-party dependencies (Python 3.9+ standard library only)."""
import datetime
import html
import json
from pathlib import Path

ROOTDIR = Path(__file__).resolve().parent.parent
DOMAIN = "https://home.direct"
SITE = "Home.Direct"
ADSENSE = ('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?'
           'client=ca-pub-6620975821265271" crossorigin="anonymous"></script>')
PUB_ID = "ca-pub-6620975821265271"
PARTNER_URL = "https://web.works/contact"
NOW = datetime.datetime.now(datetime.timezone.utc)
TODAY = NOW.date()
BUILT = NOW.strftime("%B %-d, %Y")
PAGES = []  # (path, priority, changefreq) for sitemap

E = html.escape


def money(n):
    return "${:,.0f}".format(n)


# ---------------------------------------------------------------- icons
_P = {
    "roof": "M3 12l9-8 9 8M5 10v10h14V10M9 20v-6h6v6",
    "home": "M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z",
    "layers": "M12 3l9 5-9 5-9-5 9-5zM3 13l9 5 9-5M3 17.5l9 4.5 9-4.5",
    "window": "M4 3h16v18H4zM12 3v18M4 12h16",
    "droplet": "M12 3s7 7.5 7 12a7 7 0 0 1-14 0c0-4.5 7-12 7-12z",
    "roller": "M4 4h13v5H4zM17 6.5h3v6h-8v3M10 15.5h4V21h-4z",
    "deck": "M3 11h18M3 15h18M3 19h18M5 11v9M19 11v9M8 7l4-3 4 3",
    "fence": "M5 21V7l2-3 2 3v14M15 21V7l2-3 2 3v14M3 11h18M3 17h18",
    "road": "M8 3L4 21M16 3l4 18M12 5v3M12 11v3M12 17v3",
    "sun": "M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8zM12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4",
    "fan": "M12 12m-2 0a2 2 0 1 0 4 0 2 2 0 1 0-4 0M12 10c0-4 1-7 4-7 3 0 2.5 4.5-4 7M14 12c4 0 7 1 7 4 0 3-4.5 2.5-7-4M12 14c0 4-1 7-4 7-3 0-2.5-4.5 4-7M10 12c-4 0-7-1-7-4 0-3 4.5-2.5 7 4",
    "flame": "M12 3c1 3 5 5 5 10a5 5 0 0 1-10 0c0-3 2-4 2-6 2 1 3 3 3 3s1-4 0-7z",
    "bolt": "M13 2L4 14h7l-1 8 9-12h-7l1-8z",
    "foundation": "M3 21h18M5 21V11l7-6 7 6v10M3 17h18M9 13h6",
    "shield": "M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6l8-3z",
    "basement": "M3 10l9-7 9 7M5 9v12h14V9M3 15h18M9 21v-3h6v3",
    "kitchen": "M4 3h16v18H4zM4 9h16M8 6h.01M12 6h.01M9 13h6v5H9z",
    "bath": "M4 12h16v3a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5zM6 12V5a2 2 0 0 1 4 0M7 20l-1 2M17 20l1 2",
    "floor": "M3 3h18v18H3zM3 9h18M3 15h18M9 3v6M15 9v6M9 15v6",
    "garage": "M3 21V9l9-6 9 6v12M7 21v-9h10v9M7 15h10M7 18h10",
    "tree": "M12 22v-6M6 16h12l-3.5-4.5H17L12 4l-5 7.5h2.5z",
    "search": "M11 4a7 7 0 1 0 0 14 7 7 0 0 0 0-14zM21 21l-5-5",
    "menu": "M4 6h16M4 12h16M4 18h16",
    "check": "M20 6L9 17l-5-5",
    "lock": "M5 11h14v10H5zM8 11V7a4 4 0 0 1 8 0v4",
    "wrench": "M15 5a4 4 0 0 0-5 5l-7 7 4 4 7-7a4 4 0 0 0 5-5l-3 3-3-1-1-3z",
    "dollar": "M12 2v20M17 6H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6",
    "calc": "M5 3h14v18H5zM8 7h8M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M16 15v3M8 18h4",
    "chart": "M3 3v18h18M7 15l4-4 3 3 5-6",
    "play": "M4 5h16v14H4zM10 9l5 3-5 3z",
    "news": "M4 4h13v16H5a1 1 0 0 1-1-1zM17 8h3v11a1 1 0 0 1-1 1h-2M8 8h5M8 12h5M8 16h3",
    "calendar": "M4 5h16v16H4zM4 9h16M8 3v4M16 3v4",
    "trophy": "M8 4h8v5a4 4 0 0 1-8 0zM8 6H4v2a3 3 0 0 0 4 3M16 6h4v2a3 3 0 0 1-4 3M12 13v4M8 21h8M9 17h6",
    "heart": "M12 21s-8-5-8-11a4.5 4.5 0 0 1 8-3 4.5 4.5 0 0 1 8 3c0 6-8 11-8 11z",
    "briefcase": "M3 7h18v13H3zM8 7V4h8v3M3 13h18",
    "megaphone": "M3 10v4h4l8 4V6l-8 4zM18 9a3 3 0 0 1 0 6M7 14l1 5h3l-1-4",
    "users": "M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM2 21a7 7 0 0 1 14 0M17 11a3 3 0 1 0 0-6M22 21a6 6 0 0 0-4-5.6",
    "star": "M12 3l2.8 5.8 6.2.9-4.5 4.4 1 6.2L12 17.3l-5.5 3 1-6.2L3 9.7l6.2-.9z",
    "key": "M14 10a4 4 0 1 0-1.2 2.8L21 21M17 17l2-2M19 19l2-2",
    "sign": "M4 3v18M4 5h14l-3 4 3 4H4",
    "handshake": "M2 12l4-4 4 2 3-2 4 2 5 4-6 6-3-2-3 2-3-3zM11 10l3 3",
    "moon": "M20 14A8 8 0 0 1 10 4a8 8 0 1 0 10 10z",
    "clock": "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM12 7v5l3 2",
    "pin": "M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11zM12 8a2 2 0 1 0 0 4 2 2 0 0 0 0-4z",
    "arrow": "M5 12h14M13 6l6 6-6 6",
    "x": "M6 6l12 12M18 6L6 18",
    "spark": "M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6",
    "gift": "M3 8h18v4H3zM5 12v9h14v-9M12 8v13M12 8c-2-4-6-4-6-1 0 1 1 1 6 1M12 8c2-4 6-4 6-1 0 1-1 1-6 1",
}


def icon(name, cls=""):
    d = _P.get(name, _P["home"])
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{d}"/></svg>')


LOGO = ('<svg viewBox="0 0 40 40" aria-hidden="true"><rect x=".5" y=".5" width="39" height="39" rx="11" fill="#0d1b2a" stroke="#2b405a"/>'
        '<path d="M9 20.5l11-9 11 9" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M13.5 19.5V30h13V19.5" stroke="#fff" stroke-width="3" fill="none" stroke-linejoin="round"/>'
        '<circle cx="29.5" cy="29.5" r="5" fill="#ff5a36"/></svg>')


def brand(R):
    return f'<a class="brand" href="{R}index.html" aria-label="Home.Direct home">{LOGO}<span>Home<span class="dot">.</span>Direct</span></a>'


# ---------------------------------------------------------------- head / layout
def _ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"


def head(path, title, desc, R, *, ld=None, ads=True, noindex=False, og_type="website", image="assets/img/og-image.png", base_fix=False):
    url = DOMAIN + "/" + ("" if path == "index.html" else path)
    full_title = title if SITE in title else f"{title} | {SITE}"
    lds = "".join(_ld(x) for x in (ld or []))
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    ad = ADSENSE if ads else ""
    # 404.html is served for missing URLs at any depth, so pin relative links to the site root.
    base = ("<script>document.write('<base href=\"'+(/\\.github\\.io$/.test(location.hostname)?'/'+location.pathname.split('/')[1]+'/':'/')+'\">')</script>"
            if base_fix else "")
    return f"""<!DOCTYPE html>
<html lang="en" data-root="{R}">
<head>
<meta charset="utf-8">
{base}
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(full_title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="google-adsense-account" content="{PUB_ID}">
<meta name="theme-color" content="#0d1b2a">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{E(full_title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{R}assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{R}assets/img/apple-touch-icon.png">
<link rel="manifest" href="{R}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{R}assets/css/style.css?v={TODAY.isoformat()}">
<script>(function(){{try{{var t=localStorage.getItem('hd-theme');if(t)document.documentElement.setAttribute('data-theme',t);if(localStorage.getItem('hd-consent')==='npa'){{(window.adsbygoogle=window.adsbygoogle||[]).requestNonPersonalizedAds=1;}}}}catch(e){{}}}})();</script>
{ad}
{lds}
</head>
"""


NAV_COSTS = ["roof-replacement", "hvac-replacement", "kitchen-remodel", "bathroom-remodel", "window-replacement", "siding-replacement",
             "foundation-repair", "water-heater-replacement", "solar-panels", "flooring-installation"]
NAV_TOOLS = [("mortgage-calculator", "Mortgage calculator", "Payment, PITI & amortization"), ("affordability-calculator", "How much house can I afford?", "DTI-based price range"),
             ("refinance-calculator", "Refinance break-even", "Savings & months to recoup"), ("net-proceeds-calculator", "Home sale net proceeds", "What you'll walk away with"),
             ("commission-savings-calculator", "Commission savings", "Agent vs. FSBO vs. cash offer"), ("project-cost-estimator", "Project cost estimator", "24 projects, local adjustment")]


def header(R, active=""):
    from content_guides import GUIDES
    g = {x["slug"]: x for x in GUIDES}
    costs = "".join(f'<li><a href="{R}cost-guides/{s}.html">{E(g[s]["name"])}<span>{money(g[s]["low"])} – {money(g[s]["high"])}</span></a></li>' for s in NAV_COSTS)
    tools = "".join(f'<li><a href="{R}tools/{s}.html">{E(t)}<span>{E(d)}</span></a></li>' for s, t, d in NAV_TOOLS)

    def cur(key):
        return ' aria-current="page"' if key == active else ""
    return f"""<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><a href="{PARTNER_URL}" target="_blank" rel="noopener">Contact, if you are interested in this website / domain name / <strong>Sponsorship</strong> / <strong>Advertisement</strong> / <strong>Partnership</strong> →</a></div>
<header class="site-header">
  <nav class="wrap nav" aria-label="Main">
    {brand(R)}
    <ul class="nav-links" id="nav-links">
      <li><a href="{R}sell-direct.html"{cur('sell')}>Sell Direct</a></li>
      <li><a href="{R}get-quotes.html"{cur('quotes')}>Get Quotes</a></li>
      <li class="has-dd"><button type="button" aria-expanded="false">Costs ▾</button>
        <ul class="dropdown wide">{costs}<li><a href="{R}cost-guides/index.html"><b>All 24 cost guides →</b><span>Every project, every price range</span></a></li></ul></li>
      <li class="has-dd"><button type="button" aria-expanded="false">Tools ▾</button>
        <ul class="dropdown">{tools}<li><a href="{R}tools/index.html"><b>All 12 calculators →</b></a></li></ul></li>
      <li><a href="{R}finance.html"{cur('finance')}>Finance</a></li>
      <li class="has-dd"><button type="button" aria-expanded="false">Learn ▾</button>
        <ul class="dropdown"><li><a href="{R}videos.html">Video hub<span>Fresh how-tos from top channels</span></a></li><li><a href="{R}news.html">Housing news<span>Auto-updated every 6 hours</span></a></li><li><a href="{R}maintenance.html">Maintenance planner<span>Month-by-month checklist</span></a></li><li><a href="{R}faq.html">FAQ</a></li></ul></li>
      <li class="has-dd"><button type="button" aria-expanded="false">Community ▾</button>
        <ul class="dropdown"><li><a href="{R}contests.html">Monthly contest<span>Win prizes for your best project</span></a></li><li><a href="{R}support.html">Support Home.Direct<span>Donate or sponsor</span></a></li><li><a href="{R}careers.html">Careers & talent<span>Write, review, create</span></a></li><li><a href="{R}pros.html">For pros<span>Get leads in your ZIP</span></a></li><li><a href="{R}advertise.html">Advertise<span>Sponsorships & placements</span></a></li></ul></li>
    </ul>
    <button class="icon-btn search-btn" type="button" data-search-open aria-label="Search the site">{icon('search')}</button>
    <a class="btn sm nav-cta" href="{R}get-quotes.html">Get free quotes</a>
    <button class="icon-btn menu-toggle" type="button" aria-label="Open menu" aria-controls="nav-links" aria-expanded="false">{icon('menu')}</button>
  </nav>
</header>
<div class="scrim"></div>
<div class="search-ov" role="dialog" aria-modal="true" aria-label="Search">
  <div class="search-box"><label class="sr-only" for="site-search">Search Home.Direct</label><input id="site-search" type="search" placeholder="Search guides, calculators, topics…  (press / anytime)" autocomplete="off"><ul class="search-results"></ul></div>
</div>
"""


def footer(R, sticky=True, tools=False):
    st = (f'<div class="sticky-cta"><a class="btn" href="{R}get-quotes.html">Get free quotes</a>'
          f'<a class="btn ghost" href="{R}sell-direct.html#offer-form">Sell my home</a></div>') if sticky else ""
    tjs = f'<script src="{R}assets/js/tools.js?v={TODAY.isoformat()}" defer></script>' if tools else ""
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        {brand(R)}
        <p style="margin-top:14px">Go direct. Free cost guides, calculators and matching with local pros, cash buyers and lenders — built for homeowners, not middlemen.</p>
        <div class="foot-news">
          <form class="hd-form" id="news-form" data-form="newsletter" data-subject="Newsletter signup" novalidate>
            <fieldset class="step"><label class="sr-only" for="nl-email">Email</label>
              <div class="inline-form"><input id="nl-email" type="email" name="email" placeholder="Your email for the monthly home brief" required><button class="btn sm" type="submit" data-submit>Subscribe</button></div>
              <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true"></fieldset>
          </form>
          <div class="form-success" data-for="news-form" hidden><p style="color:#9fe3da;margin:8px 0 0">✓ You're in. Watch for the next home brief.</p></div>
        </div>
      </div>
      <div><h4>Homeowners</h4><ul><li><a href="{R}get-quotes.html">Get free quotes</a></li><li><a href="{R}sell-direct.html">Sell direct</a></li><li><a href="{R}cost-guides/index.html">Cost guides</a></li><li><a href="{R}maintenance.html">Maintenance planner</a></li><li><a href="{R}videos.html">Video hub</a></li></ul></div>
      <div><h4>Money</h4><ul><li><a href="{R}finance.html">Finance hub & rates</a></li><li><a href="{R}tools/mortgage-calculator.html">Mortgage calculator</a></li><li><a href="{R}tools/refinance-calculator.html">Refinance calculator</a></li><li><a href="{R}tools/net-proceeds-calculator.html">Net proceeds</a></li><li><a href="{R}tools/index.html">All calculators</a></li></ul></div>
      <div><h4>Community</h4><ul><li><a href="{R}contests.html">Monthly contest</a></li><li><a href="{R}support.html">Support us</a></li><li><a href="{R}careers.html">Careers & talent</a></li><li><a href="{R}news.html">Housing news</a></li><li><a href="{R}about.html">About</a></li></ul></div>
      <div><h4>Business</h4><ul><li><a href="{R}pros.html">For pros</a></li><li><a href="{R}advertise.html">Advertise</a></li><li><a href="{PARTNER_URL}" target="_blank" rel="noopener">Partnerships & domain inquiries</a></li><li><a href="{R}contact.html">Contact</a></li><li><a href="{R}faq.html">FAQ</a></li></ul></div>
    </div>
    <p class="foot-legal">Home.Direct is an independent information and matching service. We are not a contractor, real estate brokerage, lender or insurer, and we don't perform the services described. Cost figures are estimates; always get written quotes. Home.Direct is not affiliated with any company using a similar name — see our <a href="{R}disclosures.html">trademark &amp; copyright disclosure</a>. Some placements are sponsored and we may be compensated when you're matched with a provider.</p>
    <div class="foot-bottom">
      <span>© <span data-year>{TODAY.year}</span> Home.Direct. All rights reserved.</span>
      <span><a href="{R}privacy.html">Privacy</a> · <a href="{R}terms.html">Terms</a> · <a href="{R}disclosures.html">Disclosures &amp; trademarks</a> · <a href="{R}accessibility.html">Accessibility</a> · <a href="#" data-consent-reset>Cookie choices</a> · <button type="button" data-theme-toggle style="background:none;border:0;color:#dbe4ee;cursor:pointer;font:inherit;padding:0">Dark/light</button></span>
    </div>
  </div>
</footer>
<div class="consent" role="region" aria-label="Cookie choices"><p>We use cookies to show ads (Google AdSense) and remember your preferences. Choose personalized or non-personalized ads. <a href="{R}privacy.html#cookies">Learn more</a></p><div class="btns"><button class="btn sm ghost" type="button" data-consent="npa">Non-personalized</button><button class="btn sm teal" type="button" data-consent="all">Accept all</button></div></div>
{st}
<script src="{R}assets/js/config.js?v={TODAY.isoformat()}"></script>
<script src="{R}assets/js/app.js?v={TODAY.isoformat()}" defer></script>
{tjs}
</body>
</html>
"""


def crumbs_html(R, items):
    lis = [f'<li><a href="{R}index.html">Home</a></li>']
    for label, href in items:
        lis.append(f'<li><a href="{R}{href}">{E(label)}</a></li>' if href else f'<li aria-current="page">{E(label)}</li>')
    return '<ol class="crumbs">' + "".join(lis) + "</ol>"


def crumbs_ld(items):
    el = [{"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"}]
    for i, (label, href) in enumerate(items, start=2):
        node = {"@type": "ListItem", "position": i, "name": label}
        if href:
            node["item"] = DOMAIN + "/" + href
        el.append(node)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": el}


def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def faq_html(faqs):
    return '<div class="faq">' + "".join(f"<details><summary>{E(q)}</summary><div><p>{E(a)}</p></div></details>" for q, a in faqs) + "</div>"


def page(path, title, desc, body, *, crumbs=None, ld=None, ads=True, noindex=False, active="", sticky=True, tools=False,
         og_type="website", priority=0.6, changefreq="monthly", base_fix=False):
    depth = path.count("/")
    R = "../" * depth
    lds = list(ld or [])
    if crumbs:
        lds.append(crumbs_ld(crumbs))
    out = head(path, title, desc, R, ld=lds, ads=ads, noindex=noindex, og_type=og_type, base_fix=base_fix)
    out += header(R, active)
    out += f'<main id="main">\n{body(R) if callable(body) else body}\n</main>\n'
    out += footer(R, sticky=sticky, tools=tools)
    dest = ROOTDIR / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out, encoding="utf-8")
    if not noindex:
        PAGES.append((path, priority, changefreq))


def page_hero(R, title, lead, crumbs=None, eyebrow="", extra=""):
    cr = crumbs_html(R, crumbs) if crumbs else ""
    eb = f'<span class="eyebrow">{E(eyebrow)}</span>' if eyebrow else ""
    return f'<section class="page-hero"><div class="wrap">{cr}{eb}<h1>{title}</h1><p class="lead">{lead}</p>{extra}</div></section>'


# ---------------------------------------------------------------- form components
def radios(name, items, req=True, cls="options", label="", err="Please choose one."):
    r = " required" if req else ""
    tiles = "".join(
        f'<label class="opt-card"><input type="radio" name="{name}" value="{E(v)}"{r}><span>{E(l)}{f"<small>{E(s)}</small>" if s else ""}</span></label>'
        for v, l, *rest in items for s in [rest[0] if rest else ""])
    lab = f'<span class="label">{label}</span>' if label else ""
    return f'<div class="field">{lab}<div class="{cls}">{tiles}</div><div class="err-msg">{err}</div></div>'


def field(label, name, kind="text", req=True, ph="", opt_label=False, err="", attrs="", fid=None):
    fid = fid or f"f-{name}"
    r = " required" if req else ""
    o = ' <span class="opt">(optional)</span>' if (not req or opt_label) else ""
    if kind == "textarea":
        inp = f'<textarea id="{fid}" name="{name}" placeholder="{E(ph)}"{r} {attrs}></textarea>'
    else:
        inp = f'<input id="{fid}" type="{kind}" name="{name}" placeholder="{E(ph)}"{r} {attrs}>'
    e = err or ("Please enter a valid email." if kind == "email" else "Please enter a valid phone number." if kind == "tel" else "This field is required.")
    return f'<div class="field"><label for="{fid}">{label}{o}</label>{inp}<div class="err-msg">{e}</div></div>'


def select(label, name, items, req=True, ph="Select…", fid=None, groups=None):
    fid = fid or f"f-{name}"
    r = " required" if req else ""
    o = "" if req else ' <span class="opt">(optional)</span>'
    if groups:
        opts = "".join(f'<optgroup label="{E(g)}">' + "".join(f'<option value="{E(v)}">{E(l)}</option>' for v, l in items_) + "</optgroup>" for g, items_ in groups)
    else:
        opts = "".join(f'<option value="{E(v)}">{E(l)}</option>' for v, l in items)
    return f'<div class="field"><label for="{fid}">{label}{o}</label><select id="{fid}" name="{name}"{r}><option value="">{E(ph)}</option>{opts}</select><div class="err-msg">Please make a selection.</div></div>'


def zip_field(name="zip", label="ZIP or postal code", fid=None):
    return field(label, name, "text", True, "e.g. 90210 or H2X 1Y4", err="Enter a 5-digit ZIP or a Canadian postal code.",
                 attrs='data-zip inputmode="text" autocomplete="postal-code" maxlength="10"', fid=fid)


CONSENT = ("I agree that Home.Direct and up to 3 matched providers may contact me by phone, text or email about this request, "
           "including by automated means. Consent is not a condition of purchase; reply STOP to opt out anytime. I accept the "
           '<a href="{R}terms.html" target="_blank">Terms</a> and <a href="{R}privacy.html" target="_blank">Privacy Policy</a>.')


def contact_step(R, legend="Where should we send your matches?", hint="We'll only use this for your request. No spam, ever.", consent=True, phone_req=True):
    c = (f'<div class="field"><label class="check"><input type="checkbox" name="consent" value="yes" required> <span>{CONSENT.format(R=R)}</span></label>'
         f'<div class="err-msg">Please accept to continue.</div></div>') if consent else ""
    return f"""<fieldset class="step"><legend>{legend}</legend><p class="hint">{hint}</p>
<div class="row">{field("First name", "first_name", "text", True, "Jane", attrs='autocomplete="given-name"')}{field("Last name", "last_name", "text", True, "Doe", attrs='autocomplete="family-name"')}</div>
<div class="row">{field("Email", "email", "email", True, "you@example.com", attrs='autocomplete="email"')}{field("Phone", "phone", "tel", phone_req, "(555) 555-0123", attrs='autocomplete="tel"')}</div>
{select("Best time to reach you", "best_time", [("morning", "Morning"), ("afternoon", "Afternoon"), ("evening", "Evening"), ("anytime", "Anytime"), ("email-only", "Email only, please")], req=False)}
{c}
<label class="check"><input type="checkbox" name="newsletter" value="yes"> <span>Send me the free monthly home brief (costs, rates, seasonal checklists).</span></label>
</fieldset>"""


def form_open(fid, name, subject, scored=False, skip=False):
    sc = ' data-scored="1"' if scored else ""
    sk = " data-skip" if skip else ""
    return (f'<form class="hd-form" id="{fid}" data-form="{name}" data-subject="{E(subject)}"{sc}{sk} novalidate>'
            '<div class="progress"><i></i></div><div class="step-count"><span>Step <b data-step-cur>1</b> of <b data-step-total>1</b></span><span>Free · No obligation</span></div>')


def form_close(submit="Submit", note="Your details are encrypted in transit and only shared for this request."):
    return (f'<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">'
            f'<div class="form-error" role="alert"></div>'
            f'<div class="form-nav"><button type="button" class="btn ghost" data-back>← Back</button>'
            f'<button type="button" class="btn" data-next>Continue →</button><button type="submit" class="btn" data-submit hidden>{submit}</button></div>'
            f'<p class="secure-note">{icon("lock")}<span>{note}</span></p></form>')


def simple_form(fid, name, subject, inner, submit="Send", note="We reply within 2 business days. Your address is never published."):
    return (f'<form class="hd-form" id="{fid}" data-form="{name}" data-subject="{E(subject)}" novalidate><fieldset class="step">{inner}</fieldset>'
            f'<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true"><div class="form-error" role="alert"></div>'
            f'<div class="form-nav" style="justify-content:flex-start"><button type="submit" class="btn" data-submit>{submit}</button></div>'
            f'<p class="secure-note">{icon("lock")}<span>{note}</span></p></form>')


def success(fid, title, text, R, links=None):
    ls = links or [("Browse cost guides", "cost-guides/index.html"), ("Try the calculators", "tools/index.html")]
    btns = "".join(f'<a class="btn {"" if i == 0 else "ghost"} sm" href="{R}{h}">{E(t)}</a> ' for i, (t, h) in enumerate(ls))
    return (f'<div class="form-success" data-for="{fid}" hidden><div class="ok-ring">{icon("check")}</div>'
            f'<h3>{title}<span data-name></span>!</h3><p class="muted">{text}</p><div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap">{btns}</div></div>')


def yt(vid, title, cls=""):
    return (f'<div class="yt {cls}" data-id="{E(vid)}" data-title="{E(title)}" tabindex="0" role="button" aria-label="Play video: {E(title)}">'
            f'<img src="https://i.ytimg.com/vi/{E(vid)}/hqdefault.jpg" alt="" loading="lazy" width="480" height="360">'
            f'<button type="button" tabindex="-1" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></button></div>')
