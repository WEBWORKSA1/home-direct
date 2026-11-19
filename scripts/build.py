#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds every page of Home.Direct into the repository root (GitHub Pages serves main/).
Run:  python scripts/build.py   (also run automatically by .github/workflows/auto-refresh.yml)"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hd_core import (ROOTDIR, DOMAIN, SITE, PARTNER_URL, TODAY, BUILT, PAGES, E, money, icon, page, page_hero, crumbs_html,
                     faq_html, faq_ld, radios, field, select, zip_field, contact_step, form_open, form_close, simple_form,
                     success, yt, CONSENT)
from content_guides import GUIDES, CATEGORIES
from site_data import SERVICES, POPULAR_SERVICES, MONTHS, CONTEST_THEMES, CONTEST_PRIZES, ROI_PROJECTS, ROLES
import pages_more
import pages_tools

G = {g["slug"]: g for g in GUIDES}
DATA = ROOTDIR / "data"


def load(name, default):
    try:
        return json.loads((DATA / name).read_text(encoding="utf-8"))
    except Exception:
        return default


RATES = load("rates.json", {})
NEWS = load("news.json", {"items": []})
VIDEOS = load("videos.json", {"items": []})


# ---------------------------------------------------------------- shared snippets
def rate_strip(R, compact=False):
    if not RATES.get("r30"):
        return ""
    def d(cur, prev):
        if prev is None:
            return ""
        diff = round(cur - prev, 2)
        cls = "up" if diff > 0 else "down"
        arrow = "▲" if diff > 0 else "▼" if diff < 0 else "•"
        return f'<span class="delta {cls}">{arrow} {abs(diff):.2f}</span>'
    asof = RATES.get("as_of_label", RATES.get("as_of", ""))
    link = "" if compact else f'<a class="btn sm teal" href="{R}finance.html#lender-form">Compare lender offers</a>'
    return (f'<div class="rate-strip"><span class="badge">Live rates</span>'
            f'<div class="rate"><span class="muted">30-yr fixed</span><b>{RATES["r30"]:.2f}%</b>{d(RATES["r30"], RATES.get("r30_prev"))}</div>'
            f'<div class="rate"><span class="muted">15-yr fixed</span><b>{RATES["r15"]:.2f}%</b>{d(RATES["r15"], RATES.get("r15_prev"))}</div>'
            f'{link}<span class="rate-src">Freddie Mac PMMS weekly average · {E(asof)}</span></div>')


def news_items(R, limit=8, cats=True):
    items = NEWS.get("items", [])[:limit]
    if not items:
        return '<p class="muted">Headlines refresh automatically every 6 hours.</p>'
    li = []
    for it in items:
        tag = f'<span class="badge {"coral" if it.get("cat") == "Market" else "gold" if it.get("cat") == "Mortgage" else ""} tag">{E(it.get("cat", "News"))}</span>' if cats else ""
        li.append(f'<li data-cat="{E(it.get("cat", "News"))}"><a class="news-item" href="{E(it["link"])}" target="_blank" rel="noopener nofollow">{tag}'
                  f'<div><b>{E(it["title"])}</b><small>{E(it.get("source", ""))} · {E(it.get("date_label", ""))}</small></div></a></li>')
    return '<ul class="news-list">' + "".join(li) + "</ul>"


def video_cards(items, cls="g3"):
    if not items:
        return '<p class="muted">New videos load automatically.</p>'
    return f'<div class="grid {cls}">' + "".join(
        f'<div class="video-card" data-cat="{E(v.get("cat", "all"))}">{yt(v["id"], v["title"])}<b>{E(v["title"])}</b><small>{E(v.get("channel", ""))}{(" · " + E(v["date_label"])) if v.get("date_label") else ""}</small></div>'
        for v in items) + "</div>"


def guide_card(R, g, small=False):
    return (f'<a class="tile" href="{R}cost-guides/{g["slug"]}.html"><span class="card-icon">{icon(g["icon"])}</span>'
            f'<div><b>{E(g["name"])}</b><span>{money(g["low"])} – {money(g["high"])} · typical {money(g["avg"])}</span></div></a>')


def quote_mini(R, service="", title="Get up to 3 free quotes", text="Tell us your ZIP — we'll match you with vetted local pros. Free, no obligation."):
    hidden = f'<input type="hidden" name="service" value="{E(service)}">' if service else ""
    return (f'<div class="card"><span class="badge coral">Free · 60 seconds</span><h3 style="margin-top:10px">{title}</h3><p class="muted small">{text}</p>'
            f'<form data-quick action="{R}get-quotes.html" novalidate>{hidden}<label class="sr-only" for="mini-zip-{service or "x"}">ZIP or postal code</label>'
            f'<input id="mini-zip-{service or "x"}" name="zip" data-zip required placeholder="ZIP / postal code" style="margin-bottom:10px">'
            f'<button class="btn block" type="submit">Get my quotes →</button></form>'
            f'<ul class="checklist small" style="margin:14px 0 0"><li>Pre-screened, insured pros</li><li>Compare prices side by side</li><li>No spam — you choose who to hire</li></ul></div>')


def service_select(R, fid="f-service"):
    return select("What do you need help with?", "service", [], req=True, ph="Choose a service…", fid=fid, groups=SERVICES)


# ---------------------------------------------------------------- HOME
def build_home():
    popular = ["roof-replacement", "hvac-replacement", "kitchen-remodel", "bathroom-remodel", "window-replacement", "foundation-repair",
               "water-heater-replacement", "siding-replacement", "solar-panels", "basement-waterproofing", "flooring-installation", "deck-building"]
    m = MONTHS[TODAY.month - 1]
    faqs = [
        ("Is Home.Direct really free for homeowners?", "Yes. Guides, calculators and matching are free. We earn from advertising, sponsorships and fees some providers pay when they receive a request — never from you."),
        ("How does pro matching work?", "You describe the project once. We share it with up to three local providers who serve your ZIP or postal code; they contact you with quotes. You decide whether to hire anyone."),
        ("Can I sell my house without an agent here?", "Yes. Our Sell Direct hub compares cash offers, for-sale-by-owner, flat-fee MLS and discount brokers, and can connect you with cash buyers or low-fee options in your area."),
        ("Where do your cost numbers come from?", "Typical installed-cost ranges compiled from published contractor cost guides, supplier pricing and industry surveys, adjusted with regional multipliers in our estimators. Local quotes vary."),
        ("Do you serve Canada?", "Yes. Forms accept U.S. ZIP codes and Canadian postal codes, and our calculators include Canadian mortgage compounding and CAD estimates."),
        ("How current is the information?", "Mortgage rates, housing news and videos refresh automatically several times a day; cost guides are reviewed on a rolling basis."),
    ]
    vids = VIDEOS.get("items", [])[:3]

    def body(R):
        svc_opts = "".join(f'<option value="{v}">{E(l)}</option>' for v, l in POPULAR_SERVICES)
        tiles = "".join(guide_card(R, G[s]) for s in popular)
        tasks = "".join(f'<li><b>{E(t[0])}</b> — <span class="muted">{E(t[1])}</span></li>' for t in m["tasks"][:4])
        return f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div class="fade-in">
      <span class="eyebrow">Free for homeowners · U.S. &amp; Canada</span>
      <h1>Go direct. Every home decision, <em>minus the middleman.</em></h1>
      <p class="lead">Real cost numbers for 24 projects, 12 money calculators, and direct matching with local pros, cash buyers and lenders — no sign-up wall, no spam.</p>
      <ul class="chips">
        <li><a class="chip" href="{R}cost-guides/roof-replacement.html">{icon('roof')}Roof cost</a></li>
        <li><a class="chip" href="{R}tools/mortgage-calculator.html">{icon('calc')}Mortgage calculator</a></li>
        <li><a class="chip" href="{R}tools/net-proceeds-calculator.html">{icon('dollar')}What will I net?</a></li>
        <li><a class="chip" href="{R}maintenance.html">{icon('calendar')}{E(m['name'])} checklist</a></li>
      </ul>
      <div class="trust-row"><span>{icon('check')}100% free to use</span><span>{icon('check')}Up to 3 quotes, you choose</span><span>{icon('check')}Updated every 6 hours</span></div>
    </div>
    <div class="hero-card fade-in">
      <div class="tabs" role="tablist" aria-label="What do you want to do?">
        <button class="tab" role="tab" id="t-hire" aria-controls="p-hire" aria-selected="true">{icon('wrench')}Hire a pro</button>
        <button class="tab" role="tab" id="t-sell" aria-controls="p-sell" aria-selected="false" tabindex="-1">{icon('sign')}Sell my home</button>
        <button class="tab" role="tab" id="t-fin" aria-controls="p-fin" aria-selected="false" tabindex="-1">{icon('key')}Finance</button>
      </div>
      <div class="tabpanel" role="tabpanel" id="p-hire" aria-labelledby="t-hire">
        <h2>Get free quotes from local pros</h2><p class="muted small">Compare up to 3 vetted pros. Takes about 60 seconds.</p>
        <form data-quick action="{R}get-quotes.html" data-hash="#quote" novalidate>
          <div class="field"><label for="h-svc">Project</label><select id="h-svc" name="service" required><option value="">Choose a service…</option>{svc_opts}<option value="other">Something else</option></select></div>
          <div class="field"><label for="h-zip">ZIP or postal code</label><input id="h-zip" name="zip" data-zip required placeholder="e.g. 30301 or M5V 2T6"></div>
          <button class="btn block lg" type="submit">Match me with pros →</button>
        </form>
      </div>
      <div class="tabpanel" role="tabpanel" id="p-sell" aria-labelledby="t-sell" hidden>
        <h2>See every way to sell — side by side</h2><p class="muted small">Cash offers, FSBO, flat-fee MLS or a low-fee agent. Compare your net, then decide.</p>
        <form data-quick action="{R}sell-direct.html" data-hash="#offer-form" novalidate>
          <div class="field"><label for="s-zip">Property ZIP or postal code</label><input id="s-zip" name="zip" data-zip required placeholder="Where is the home?"></div>
          <div class="field"><label for="s-tl">When do you want to sell?</label><select id="s-tl" name="timeline" required><option value="">Choose…</option><option value="asap">ASAP (under 30 days)</option><option value="1-3m">1–3 months</option><option value="3-6m">3–6 months</option><option value="6m+">6+ months</option><option value="research">Just exploring</option></select></div>
          <button class="btn block lg" type="submit">Compare my options →</button>
        </form>
      </div>
      <div class="tabpanel" role="tabpanel" id="p-fin" aria-labelledby="t-fin" hidden>
        <h2>Shop rates without the runaround</h2><p class="muted small">Purchase, refinance, HELOC or renovation loan — get matched with licensed lenders.</p>
        <form data-quick action="{R}finance.html" data-hash="#lender-form" novalidate>
          <div class="field"><label for="f-goal">Goal</label><select id="f-goal" name="goal" required><option value="">Choose…</option><option value="buy">Buy a home</option><option value="refinance">Refinance</option><option value="cash-out">Cash-out refinance</option><option value="heloc">HELOC / home equity</option><option value="renovation-loan">Renovation loan</option></select></div>
          <div class="field"><label for="f-zip">ZIP or postal code</label><input id="f-zip" name="zip" data-zip required placeholder="Property location"></div>
          <button class="btn block lg teal" type="submit">Find my rate →</button>
        </form>
      </div>
    </div>
  </div>
</section>
<section class="section-sm"><div class="wrap">{rate_strip(R)}</div></section>

<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">What are you planning?</span><h2>Know the price before you call anyone</h2><p class="lead">Typical 2026 installed costs, what drives them and how to save — then get quotes in one click.</p></div>
  <div class="grid g3">{tiles}</div>
  <p style="margin-top:22px"><a class="link-arrow" href="{R}cost-guides/index.html">See all 24 cost guides</a></p>
</div></section>

<section class="alt"><div class="wrap">
  <div class="section-head center"><span class="eyebrow">Three ways to go direct</span><h2>One site for the three biggest money moves in a home</h2></div>
  <div class="grid g3">
    <div class="feature f1">{icon('wrench','ghost-icon')}<span class="badge" style="background:rgba(255,255,255,.18);color:#fff">Hire direct</span><h3>Fix, build or upgrade</h3><p>Describe your project once and hear from up to three local pros who actually serve your area. Compare quotes against our cost data.</p><a class="btn light" href="{R}get-quotes.html">Get free quotes</a></div>
    <div class="feature f2">{icon('sign','ghost-icon')}<span class="badge" style="background:rgba(255,255,255,.2);color:#fff">Sell direct</span><h3>Keep more of your equity</h3><p>Compare a cash offer, FSBO, flat-fee MLS and discount brokers on one net-proceeds sheet — the difference is often $10,000+.</p><a class="btn light" href="{R}sell-direct.html">Compare ways to sell</a></div>
    <div class="feature f3">{icon('key','ghost-icon')}<span class="badge" style="background:rgba(255,255,255,.15);color:#fff">Finance direct</span><h3>Borrow smarter</h3><p>Live weekly rates, payment and refinance math, and lender matching for purchases, refis, HELOCs and renovation loans.</p><a class="btn light" href="{R}finance.html">See rates & options</a></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Run the numbers</span><h2>Calculators that answer the real question</h2></div>
  <div class="grid g4">
    <a class="tile" href="{R}tools/mortgage-calculator.html"><span class="card-icon">{icon('calc')}</span><div><b>Mortgage payment</b><span>PITI, PMI & amortization</span></div></a>
    <a class="tile" href="{R}tools/affordability-calculator.html"><span class="card-icon">{icon('home')}</span><div><b>How much house?</b><span>Based on income & debts</span></div></a>
    <a class="tile" href="{R}tools/net-proceeds-calculator.html"><span class="card-icon coral">{icon('dollar')}</span><div><b>Home sale net</b><span>What you walk away with</span></div></a>
    <a class="tile" href="{R}tools/commission-savings-calculator.html"><span class="card-icon coral">{icon('sign')}</span><div><b>Commission savings</b><span>Agent vs FSBO vs cash</span></div></a>
    <a class="tile" href="{R}tools/refinance-calculator.html"><span class="card-icon">{icon('chart')}</span><div><b>Refinance break-even</b><span>Is it worth it?</span></div></a>
    <a class="tile" href="{R}tools/project-cost-estimator.html"><span class="card-icon gold">{icon('wrench')}</span><div><b>Project estimator</b><span>24 projects, local pricing</span></div></a>
    <a class="tile" href="{R}tools/renovation-roi-calculator.html"><span class="card-icon gold">{icon('star')}</span><div><b>Renovation ROI</b><span>What pays back at resale</span></div></a>
    <a class="tile" href="{R}tools/rent-vs-buy-calculator.html"><span class="card-icon">{icon('key')}</span><div><b>Rent vs. buy</b><span>Year-by-year break-even</span></div></a>
  </div>
</div></section>

<section class="alt"><div class="wrap">
  <div class="section-head center"><span class="eyebrow">How matching works</span><h2>Three steps. Zero pressure.</h2></div>
  <div class="steps g3">
    <div class="s"><h3>Tell us once</h3><p>A short form about your project or property — about 60 seconds. ZIP or postal code is all we need to start.</p></div>
    <div class="s"><h3>Get matched</h3><p>Up to three providers who serve your area receive your request. Not 10, not a bidding war on your phone.</p></div>
    <div class="s"><h3>Compare & decide</h3><p>Check quotes against our cost ranges and calculators. Hire whoever you want — or nobody. It's free either way.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Sell direct</span><h2>The same house can net you very different amounts</h2><p class="lead">Illustration on a $450,000 sale with a $220,000 mortgage, assuming you offer a 2.5% buyer-agent fee where relevant.</p></div>
  <div class="table-wrap"><table class="compare"><thead><tr><th>Option</th><th class="num">Seller fees</th><th class="num">Estimated net*</th><th>Speed</th><th>Best for</th></tr></thead><tbody>
    <tr><td>Full-service agent (2.75%)</td><td class="num">$23,625</td><td class="num">$206,375</td><td>30–90 days</td><td>Slow markets, little time</td></tr>
    <tr><td>Discount broker (1.5%)</td><td class="num">$18,000</td><td class="num">$212,000</td><td>30–90 days</td><td>Most sellers who want help</td></tr>
    <tr><td>Flat-fee MLS + FSBO</td><td class="num">$11,750</td><td class="num">$218,250</td><td>30–120 days</td><td>Confident, hands-on sellers</td></tr>
    <tr><td>Cash offer (~12% below market)</td><td class="num">$54,000 discount</td><td class="num">$176,000</td><td>7–30 days</td><td>Speed, repairs, certainty</td></tr>
  </tbody></table></div>
  <p class="small muted">*Before closing costs, repairs and taxes. Run your own numbers with the <a href="{R}tools/commission-savings-calculator.html">commission savings calculator</a>.</p>
  <a class="btn" href="{R}sell-direct.html">Compare my options →</a>
</div></section>

<section class="alt"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Watch & learn</span><h2>Fresh how-to videos from top home channels</h2></div>
  {video_cards(vids)}
  <p style="margin-top:18px"><a class="link-arrow" href="{R}videos.html">Open the video hub</a></p>
</div></section>

<section><div class="wrap">
  <div class="grid g2" style="gap:36px">
    <div><span class="eyebrow">Housing news</span><h2>What's moving the market</h2><p class="muted small">Headlines refresh automatically · last update {E(NEWS.get('updated_label', BUILT))}</p>{news_items(R, 6)}<p style="margin-top:14px"><a class="link-arrow" href="{R}news.html">All headlines</a></p></div>
    <div><span class="eyebrow">This month</span><h2>Your {E(m['name'])} home checklist</h2><p class="muted">{E(m['note'])}</p><ul class="checklist">{tasks}</ul><a class="btn ghost" href="{R}maintenance.html">Open the interactive planner</a>
      <div class="card" style="margin-top:22px"><span class="badge gold">{icon('trophy')} Monthly contest</span><h3 style="margin-top:10px">Show off your best home project</h3><p class="muted small">This month's theme: <b>{E(CONTEST_THEMES[TODAY.month - 1])}</b>. Win a gift card and a featured story.</p><a class="link-arrow" href="{R}contests.html">Enter the contest</a></div>
    </div>
  </div>
</div></section>

<section class="alt"><div class="wrap">
  <div class="grid g3">
    <div class="card"><span class="card-icon coral">{icon('heart')}</span><h3>Support Home.Direct</h3><p class="muted">Keep the guides free and independent. Fund operations, promotion, new talent and contest prizes.</p><a class="link-arrow" href="{R}support.html">Donate or sponsor</a></div>
    <div class="card"><span class="card-icon">{icon('briefcase')}</span><h3>Work with us</h3><p class="muted">Writers, licensed contractor reviewers, video creators and local partnership reps.</p><a class="link-arrow" href="{R}careers.html">See open roles</a></div>
    <div class="card"><span class="card-icon gold">{icon('megaphone')}</span><h3>Pros & advertisers</h3><p class="muted">Exclusive ZIP leads, category sponsorships and newsletter placements.</p><a class="link-arrow" href="{R}pros.html">Grow with Home.Direct</a></div>
  </div>
</div></section>

<section><div class="wrap narrow">
  <div class="section-head center"><span class="eyebrow">FAQ</span><h2>Questions homeowners ask us</h2></div>
  {faq_html(faqs)}
</div></section>

<section class="section-sm"><div class="wrap">
  <div class="cta-band"><div><h2>Ready when you are.</h2><p>One short form. Up to three local quotes. You stay in control.</p></div>
  <form data-quick action="{R}get-quotes.html" class="inline-form" novalidate><label class="sr-only" for="cta-zip">ZIP</label><input id="cta-zip" name="zip" data-zip required placeholder="ZIP or postal code"><button class="btn" type="submit">Get free quotes</button></form></div>
</div></section>
"""
    ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": SITE, "url": DOMAIN + "/",
           "description": "Free home cost guides, calculators and direct matching with local pros, cash buyers and lenders."},
          {"@context": "https://schema.org", "@type": "Organization", "name": SITE, "url": DOMAIN + "/", "logo": DOMAIN + "/assets/img/logo-512.png"},
          faq_ld(faqs)]
    page("index.html", "Home.Direct — Home Costs, Pro Quotes, Sell Direct & Mortgage Tools",
         "Free 2026 cost guides for 24 home projects, mortgage and home-sale calculators, live rates, and direct matching with local pros, cash buyers and lenders.",
         body, ld=ld, priority=1.0, changefreq="daily")


# ---------------------------------------------------------------- GET QUOTES
def quote_form(R):
    popular = "".join(f'<button type="button" class="chip" data-pick="{v}" data-pick-target="q-service">{E(l)}</button>' for v, l in POPULAR_SERVICES)
    return (form_open("quote-form", "quote", "Pro quote request", scored=True, skip=True)
            + f"""<fieldset class="step"><legend>What do you need done?</legend><p class="hint">Pick a popular service or choose from the full list.</p>
<div class="chips" style="margin:0 0 14px">{popular}</div>
{select("Service", "service", [], req=True, ph="Choose a service…", fid="q-service", groups=SERVICES + [("Other", [("other", "Something else")])])}
{zip_field(fid="q-zip")}</fieldset>
<fieldset class="step"><legend>About the project</legend><p class="hint">This helps pros quote accurately.</p>
{radios("scope", [("repair", "Repair", "Fix something broken"), ("replace", "Replace", "Swap old for new"), ("install", "New install", "Add something new"), ("estimate", "Estimate only", "Planning ahead")], label="Type of work")}
{select("Property type", "property_type", [("single-family", "Single-family house"), ("townhouse", "Townhouse"), ("condo", "Condo / apartment"), ("multi-family", "Multi-family (2–4 units)"), ("commercial", "Commercial")])}
{radios("ownership", [("own", "I own it"), ("landlord", "I'm the landlord"), ("buying", "I'm buying it"), ("rent", "I rent")], cls="options two", label="Your relationship to the property")}</fieldset>
<fieldset class="step"><legend>Timing & budget</legend><p class="hint">Pros prioritize clear timelines.</p>
{radios("timeline", [("asap", "ASAP", "Within 1–2 weeks"), ("1-3m", "1–3 months"), ("3-6m", "3–6 months"), ("6m+", "6+ months"), ("research", "Just researching")], label="When do you want to start?")}
{select("Approximate budget", "budget", [("under-1k", "Under $1,000"), ("1-5k", "$1,000 – $5,000"), ("5-15k", "$5,000 – $15,000"), ("15-50k", "$15,000 – $50,000"), ("50k+", "$50,000+"), ("unsure", "Not sure yet")])}
{field("Project details", "details", "textarea", False, "Size, materials, problems you've noticed, access notes…")}
{field("Photo link", "photos", "url", False, "https://… (Google Drive, Dropbox, iCloud)", err="Enter a full link starting with https://")}</fieldset>
{contact_step(R)}""" + form_close("Get my free quotes →"))


def build_quotes():
    faqs = [("How many pros will contact me?", "Up to three. We cap matches so your phone doesn't ring all day."),
            ("Do I have to hire anyone?", "No. Quotes are free and you're never obligated."),
            ("Are the pros licensed and insured?", "We ask partners to confirm licensing and insurance where required, but you should always verify a license with your state or province before signing."),
            ("Why do you need my phone number?", "Most pros confirm details by phone to give an accurate quote. Choose 'email only' under best time if you prefer.")]

    def body(R):
        return page_hero(R, "Get up to 3 free quotes from local pros", "Describe your project once. We match you with providers who serve your ZIP or postal code — then you compare and decide.",
                         [("Get quotes", None)], "Free · No obligation") + f"""
<section><div class="wrap layout" style="padding-top:0">
  <div><div class="form-shell" id="quote">{quote_form(R)}{success("quote-form", "Request received", "Matched pros typically reach out within one business day. While you wait, check typical prices so you can spot a fair quote.", R)}</div></div>
  <aside class="aside">
    <div class="card"><h3>Why homeowners use Home.Direct</h3><ul class="checklist small"><li>Up to 3 matches — not a bidding frenzy</li><li>Compare quotes against real cost ranges</li><li>U.S. ZIP codes and Canadian postal codes</li><li>No account, no fees, no obligation</li></ul></div>
    <div class="card"><h3>Before you hire</h3><ol class="small muted" style="margin:0;padding-left:1.1em"><li>Get at least three written quotes.</li><li>Verify license and insurance.</li><li>Never pay more than 10–30% up front.</li><li>Get the scope, materials and timeline in writing.</li></ol></div>
    <div class="card"><h3>Popular cost guides</h3><p class="small">{" · ".join(f'<a href="{R}cost-guides/{s}.html">{E(G[s]["name"])}</a>' for s in ["roof-replacement", "hvac-replacement", "kitchen-remodel", "bathroom-remodel", "foundation-repair"])}</p></div>
  </aside>
</div></section>
<section class="alt"><div class="wrap narrow"><h2>Quote FAQ</h2>{faq_html(faqs)}</div></section>"""
    page("get-quotes.html", "Get Free Quotes from Local Home Pros", "Compare up to 3 free quotes from local roofers, HVAC techs, plumbers, remodelers and more. U.S. and Canada. No obligation.",
         body, crumbs=[("Get quotes", None)], ld=[faq_ld(faqs)], active="quotes", sticky=False, priority=0.9)


# ---------------------------------------------------------------- SELL DIRECT
def sell_form(R):
    return (form_open("offer-form", "sell", "Seller request", scored=True, skip=True)
            + f"""<fieldset class="step"><legend>Tell us about the property</legend><p class="hint">We use this to match cash buyers and low-fee options in your area.</p>
{field("Street address", "address", "text", False, "123 Main St (optional — helps cash buyers price it)", attrs='autocomplete="street-address"')}
{zip_field(fid="s-zip-full")}
{radios("property_type", [("single-family", "House"), ("townhouse", "Townhouse"), ("condo", "Condo"), ("multi-family", "Multi-family"), ("mobile", "Mobile / manufactured"), ("land", "Land")], label="Property type")}</fieldset>
<fieldset class="step"><legend>Size & condition</legend><p class="hint">Honest condition = more accurate offers.</p>
<div class="row3">{select("Bedrooms", "beds", [(str(i), str(i) + ("+" if i == 6 else "")) for i in range(1, 7)])}{select("Bathrooms", "baths", [(x, x) for x in ["1", "1.5", "2", "2.5", "3", "3.5", "4+"]])}{field("Approx. sq ft", "sqft", "number", False, "1,800", attrs='inputmode="numeric" min="100"')}</div>
{radios("condition", [("move-in", "Move-in ready", "Updated, no repairs"), ("minor", "Needs minor repairs", "Paint, flooring, fixtures"), ("major", "Needs major repairs", "Roof, HVAC, foundation"), ("distressed", "Distressed / teardown", "Fire, flood, unlivable")], label="Condition")}</fieldset>
<fieldset class="step"><legend>Your goals</legend><p class="hint">There's no wrong answer — this decides which options we show you.</p>
{radios("timeline", [("asap", "ASAP", "Under 30 days"), ("1-3m", "1–3 months"), ("3-6m", "3–6 months"), ("6m+", "6+ months"), ("research", "Just exploring")], label="Timeline")}
{select("Main reason for selling", "reason", [("relocating", "Relocating"), ("upsizing", "Upsizing"), ("downsizing", "Downsizing"), ("inherited", "Inherited property"), ("divorce", "Divorce / separation"), ("financial", "Financial pressure"), ("landlord", "Tired landlord"), ("repairs", "Can't afford repairs"), ("other", "Other")])}
{radios("sell_method", [("cash", "Cash offer", "Fast & certain"), ("fsbo", "Sell it myself", "FSBO + flat-fee MLS"), ("discount", "Low-fee agent", "1–1.5% listing"), ("agent", "Full-service agent", "Negotiate the fee"), ("compare", "Compare all", "Show me the math")], label="How would you like to sell?")}
<div class="row">{field("Price you hope to get", "price_expectation", "text", False, "$450,000")}{field("Approx. mortgage owed", "mortgage_balance", "text", False, "$220,000")}</div></fieldset>
{contact_step(R, "Where should we send your options?", "Cash buyers and partners contact you directly. You're never obligated to accept an offer.")}""" + form_close("See my selling options →"))


def build_sell():
    faqs = [("Is a cash offer always lower than the market?", "Usually. Cash buyers price in repairs, holding costs and profit, so offers often land 5–20% below market value. In exchange you get speed, certainty and no showings. Always compare at least two cash offers against a market-value estimate."),
            ("Can I really sell without an agent?", "Yes. For-sale-by-owner sales are legal everywhere in the U.S. and Canada. A flat-fee MLS listing (typically $300–$600) puts your home on the same databases agents search, and a real estate attorney or notary can handle the contract."),
            ("Do I still have to pay the buyer's agent?", "Not necessarily. Since 2024, U.S. buyer-agent compensation is negotiable and no longer set through the MLS. Many sellers still offer a concession to attract agent-represented buyers — it's your call."),
            ("How do I avoid lowball 'we buy houses' offers?", "Get multiple offers, ask for proof of funds, read the inspection-contingency terms, and be wary of buyers who drop the price after inspection. Never sign an exclusive agreement to receive an offer."),
            ("What does selling cost besides commission?", "Expect roughly 1–3% for closing costs and transfer taxes, plus repairs, staging, moving and any concessions. The net proceeds calculator includes all of these.")]

    def body(R):
        steps = [("Price it right", "Pull recent comparable sales within a half mile and 6 months; adjust for size and condition. Overpricing is the #1 reason FSBO homes sit."),
                 ("Prep & photograph", "Declutter, deep clean, fix the obvious, and invest in professional photos — listings with pro photos get more showings."),
                 ("List everywhere", "A flat-fee MLS listing syndicates to the big portals. Add a yard sign with a QR code."),
                 ("Show & negotiate", "Pre-qualify buyers, require proof of funds or a pre-approval, and compare net — not just price."),
                 ("Close cleanly", "A real estate attorney, title company or notary prepares documents and holds deposits in escrow.")]
        st = "".join(f'<div class="s"><h3>{E(a)}</h3><p>{E(b)}</p></div>' for a, b in steps)
        quiz = f"""<form id="sell-quiz" class="card" novalidate><h3>Which way to sell fits you? (5 questions)</h3>
{radios("q_speed", [("fast", "Within 30 days"), ("normal", "1–3 months"), ("flex", "No rush")], cls="options", label="1. How fast do you need to sell?")}
{radios("q_condition", [("great", "Great"), ("minor", "Needs minor work"), ("major", "Needs major work")], label="2. What shape is the home in?")}
{radios("q_time", [("lots", "Plenty"), ("some", "Some"), ("none", "Very little")], label="3. How much time can you give the sale each week?")}
{radios("q_market", [("hot", "Hot — homes sell fast"), ("normal", "Balanced"), ("slow", "Slow")], label="4. How's your local market?")}
{radios("q_confidence", [("high", "Very confident"), ("mid", "Somewhat"), ("low", "Not at all")], label="5. How confident are you negotiating and handling paperwork?")}
<button class="btn teal" type="submit">Show my best option</button>
<div id="quiz-result" class="callout coral" hidden style="margin-top:18px"><h3></h3><p></p><a class="btn sm" href="#offer-form">Get matched for this option →</a></div></form>"""
        return page_hero(R, "Sell your home direct — and keep more of your equity", "Compare a cash offer, for-sale-by-owner, flat-fee MLS and low-fee agents on one net sheet. Then get matched with the option that pays you most.",
                         [("Sell direct", None)], "Sell direct", f'<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:18px"><a class="btn lg" href="#offer-form">Get my options</a><a class="btn ghost lg" href="{R}tools/net-proceeds-calculator.html">Calculate my net</a></div>') + f"""
<section><div class="wrap">
  <div class="section-head"><span class="eyebrow">Your four options</span><h2>Cash offer vs. FSBO vs. flat-fee MLS vs. agent</h2></div>
  <div class="table-wrap"><table class="compare"><thead><tr><th></th><th>Cash offer</th><th>FSBO + flat-fee MLS</th><th>Discount broker</th><th>Full-service agent</th></tr></thead><tbody>
  <tr><td>Typical seller cost</td><td>5–20% below market</td><td>$300–$600 + optional buyer-agent fee</td><td>1–1.5% + buyer-agent fee</td><td>2.5–3% + buyer-agent fee</td></tr>
  <tr><td>Time to close</td><td>7–30 days</td><td>30–120 days</td><td>30–90 days</td><td>30–90 days</td></tr>
  <tr><td>Showings</td><td class="no">None</td><td class="yes">You run them</td><td class="yes">Agent runs them</td><td class="yes">Agent runs them</td></tr>
  <tr><td>Repairs needed</td><td class="yes">None (as-is)</td><td>Usually</td><td>Usually</td><td>Usually</td></tr>
  <tr><td>Your workload</td><td>Lowest</td><td>Highest</td><td>Low</td><td>Lowest</td></tr>
  <tr><td>Best for</td><td>Speed, distressed homes, inheritances</td><td>Hot markets, confident sellers</td><td>Most sellers</td><td>Complex or slow markets</td></tr>
  </tbody></table></div>
</div></section>
<section class="alt"><div class="wrap grid g2" style="gap:30px;align-items:start">{quiz}
  <div><span class="eyebrow">The FSBO playbook</span><h2>Selling it yourself in 5 steps</h2><div class="steps">{st}</div></div></div></section>
<section id="sell-form-section"><div class="wrap layout" style="padding-top:20px">
  <div><span class="eyebrow">Get matched</span><h2>See your real options for this property</h2><p class="muted">Free, no obligation. Cash buyers and low-fee partners respond directly — compare them with the calculators before you decide.</p>
  <div class="form-shell">{sell_form(R)}{success("offer-form", "Thanks", "Partners serving your area will reach out with offers and options. Compare every number against your estimated market value before signing anything.", R, [("Calculate my net proceeds", "tools/net-proceeds-calculator.html"), ("Commission savings", "tools/commission-savings-calculator.html")])}</div></div>
  <aside class="aside">
    <div class="card"><h3>Seller protection checklist</h3><ul class="checklist small"><li>Get 2+ cash offers and a market estimate</li><li>Ask for proof of funds</li><li>Read inspection & cancellation terms</li><li>Never pay to receive an offer</li><li>Use an attorney, notary or title company</li></ul></div>
    <div class="card"><h3>Watch: selling by owner</h3>{yt("KtO-HG6bjCs", "For sale by owner: 10 steps to FSBO success")}</div>
    <div class="card"><h3>Seller tools</h3><p class="small"><a href="{R}tools/net-proceeds-calculator.html">Net proceeds</a> · <a href="{R}tools/commission-savings-calculator.html">Commission savings</a> · <a href="{R}tools/closing-cost-calculator.html">Closing costs</a> · <a href="{R}tools/renovation-roi-calculator.html">Pre-sale ROI</a></p></div>
  </aside>
</div></section>
<section class="alt"><div class="wrap narrow"><h2>Selling FAQ</h2>{faq_html(faqs)}</div></section>"""
    page("sell-direct.html", "Sell Your House Direct: Cash Offers, FSBO & Low-Fee Options", "Compare cash offers, for-sale-by-owner, flat-fee MLS and discount brokers. Calculate your net and get matched with buyers and low-fee options.",
         body, crumbs=[("Sell direct", None)], ld=[faq_ld(faqs)], active="sell", sticky=False, priority=0.9, changefreq="weekly")


# ---------------------------------------------------------------- FINANCE
def sparkline(series, w=520, h=120):
    pts = [v for _, v in series][-52:]
    if len(pts) < 2:
        return ""
    lo, hi = min(pts) - 0.05, max(pts) + 0.05
    xs = [i * (w - 10) / (len(pts) - 1) + 5 for i in range(len(pts))]
    ys = [h - 10 - (p - lo) / (hi - lo) * (h - 20) for p in pts]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="30-year rate trend" style="width:100%;height:auto"><path d="{d}" fill="none" stroke="#0e7c74" stroke-width="3" stroke-linejoin="round"/>'
            f'<circle cx="{xs[-1]:.1f}" cy="{ys[-1]:.1f}" r="5" fill="#ff5a36"/></svg>')


def build_finance():
    faqs = [("Are these the rates I'll get?", "No — they're national weekly averages from Freddie Mac's Primary Mortgage Market Survey. Your rate depends on credit, down payment, loan type, points and lender."),
            ("Is Home.Direct a lender?", "No. We're an information and matching service. If you request offers, we share your request with licensed lenders or brokers who serve your area."),
            ("When does refinancing make sense?", "When you can recoup closing costs through lower payments before you expect to sell or refinance again — use the break-even calculator. A rate drop of 0.75–1 point is a common rule of thumb."),
            ("HELOC or cash-out refinance?", "A HELOC keeps your existing first mortgage and charges a variable rate on what you draw; a cash-out refi replaces the whole mortgage. If your current rate is far below today's, a HELOC usually costs less."),
            ("How do Canadian mortgages differ?", "Canadian fixed rates compound semi-annually, terms are typically 5 years within a 25–30-year amortization, and insured mortgages require CMHC or private default insurance under 20% down. Our mortgage calculator has a Canada mode.")]

    def body(R):
        r30 = RATES.get("r30")
        yago = (f'<p class="small muted">A year ago: 30-yr {RATES["r30_year_ago"]:.2f}% · 15-yr {RATES["r15_year_ago"]:.2f}%</p>' if RATES.get("r30_year_ago") else "")
        form = (form_open("lender-form", "finance", "Lender match request", scored=True, skip=True) + f"""
<fieldset class="step"><legend>What are you looking for?</legend><p class="hint">We'll match you with licensed lenders or brokers in your area.</p>
{radios("goal", [("buy", "Buy a home"), ("refinance", "Refinance"), ("cash-out", "Cash-out refi"), ("heloc", "HELOC / equity"), ("renovation-loan", "Renovation loan")], label="Goal")}
{zip_field(fid="l-zip")}</fieldset>
<fieldset class="step"><legend>The numbers</legend><p class="hint">Estimates are fine.</p>
<div class="row">{field("Home value or purchase price", "property_value", "text", True, "$450,000")}{field("Loan amount needed", "loan_amount", "text", True, "$360,000")}</div>
{radios("credit", [("excellent", "Excellent", "740+"), ("good", "Good", "680–739"), ("fair", "Fair", "620–679"), ("rebuilding", "Rebuilding", "Below 620")], label="Credit score range")}
{select("Property use", "property_use", [("primary", "Primary residence"), ("second", "Second home"), ("investment", "Investment property")])}
{radios("timeline", [("asap", "Ready now"), ("1-3m", "1–3 months"), ("3-6m", "3–6 months"), ("research", "Just comparing")], label="Timeline")}</fieldset>
{contact_step(R, "Where should lenders send offers?", "Checking options doesn't affect your credit score. A lender will ask permission before any credit pull.")}""" + form_close("See my lender options →"))
        return page_hero(R, "Mortgage rates, refinance math & lender matching", "Live weekly rate averages, the calculators that matter, and a direct line to licensed lenders for purchases, refis, HELOCs and renovation loans.",
                         [("Finance", None)], "Finance direct") + f"""
<section class="section-sm"><div class="wrap">{rate_strip(R)}</div></section>
<section><div class="wrap grid g2" style="gap:32px;align-items:start">
  <div class="card"><h3>30-year fixed — last 12 months</h3>{sparkline(RATES.get("series30", []))}{yago}<p class="small muted">Source: Freddie Mac Primary Mortgage Market Survey®, via FRED. Updated automatically each week.</p></div>
  <div><h2>Which tool do you need?</h2><div class="grid g2">
    <a class="tile" href="{R}tools/mortgage-calculator.html"><span class="card-icon">{icon('calc')}</span><div><b>Mortgage payment</b><span>US & Canada modes</span></div></a>
    <a class="tile" href="{R}tools/affordability-calculator.html"><span class="card-icon">{icon('home')}</span><div><b>Affordability</b><span>28/36 & 31/43 rules</span></div></a>
    <a class="tile" href="{R}tools/refinance-calculator.html"><span class="card-icon">{icon('chart')}</span><div><b>Refinance</b><span>Break-even months</span></div></a>
    <a class="tile" href="{R}tools/home-equity-calculator.html"><span class="card-icon">{icon('key')}</span><div><b>Home equity / HELOC</b><span>How much can I borrow?</span></div></a>
    <a class="tile" href="{R}tools/closing-cost-calculator.html"><span class="card-icon gold">{icon('dollar')}</span><div><b>Closing costs</b><span>Buyer & seller</span></div></a>
    <a class="tile" href="{R}tools/rent-vs-buy-calculator.html"><span class="card-icon gold">{icon('key')}</span><div><b>Rent vs. buy</b><span>Break-even year</span></div></a>
  </div></div>
</div></section>
<section class="alt" id="lender-form-section"><div class="wrap layout" style="padding-top:20px">
  <div><span class="eyebrow">Get matched</span><h2>Compare lender offers</h2><div class="form-shell">{form}{success("lender-form", "Request received", "Licensed partners serving your area will follow up. Compare APR, points and closing costs — not just the rate.", R, [("Mortgage calculator", "tools/mortgage-calculator.html"), ("Refinance calculator", "tools/refinance-calculator.html")])}</div></div>
  <aside class="aside"><div class="card"><h3>Shop like a pro</h3><ul class="checklist small"><li>Get 3 Loan Estimates on the same day</li><li>Compare APR, points and lender fees</li><li>Ask about rate locks and float-downs</li><li>Credit inquiries within 14–45 days count as one</li></ul></div>
  <div class="card"><h3>Renovating?</h3><p class="small muted">Price the project first, then match the loan to it.</p><a class="link-arrow" href="{R}tools/project-cost-estimator.html">Project cost estimator</a></div></aside>
</div></section>
<section><div class="wrap narrow"><h2>Mortgage FAQ</h2>{faq_html(faqs)}<p class="notice" style="margin-top:20px">Home.Direct is not a lender, mortgage broker or financial advisor. Rate data are national averages provided for information only. Loan offers come from third parties and are subject to their underwriting and licensing.</p></div></section>"""
    page("finance.html", "Mortgage Rates Today, Refinance & HELOC Tools", f"Live weekly mortgage rates{(' (30-yr ' + format(RATES['r30'], '.2f') + '%)') if RATES.get('r30') else ''}, payment, refinance and HELOC calculators, and lender matching for the U.S. and Canada.",
         body, crumbs=[("Finance", None)], ld=[faq_ld(faqs)], active="finance", priority=0.9, changefreq="weekly")


# ---------------------------------------------------------------- COST GUIDES
def build_guides():
    cats = dict(CATEGORIES)

    def index_body(R):
        bar = "".join(f'<button type="button" data-cat="{k}" aria-pressed="{str(k == "all").lower()}">{E(v)}</button>' for k, v in CATEGORIES)
        cards = "".join(f'<div data-cat="{g["cat"]}">{guide_card(R, g)}</div>' for g in sorted(GUIDES, key=lambda x: x["name"]))
        rows = "".join(f'<tr><td><a href="{R}cost-guides/{g["slug"]}.html">{E(g["name"])}</a></td><td class="num">{money(g["low"])}</td><td class="num">{money(g["avg"])}</td><td class="num">{money(g["high"])}</td><td>{E(g["diy"])}</td></tr>'
                       for g in sorted(GUIDES, key=lambda x: -x["avg"]))
        return page_hero(R, "Home project cost guides for 2026", "Typical installed costs for 24 of the most common home projects — with the factors that move the price, money-saving tips, interactive estimators and the questions to ask before you hire.",
                         [("Cost guides", None)], "Cost guides") + f"""
<section><div class="wrap"><div class="filter-bar" data-filter-group="guide-grid">{bar}</div><div class="grid g3" id="guide-grid">{cards}</div></div></section>
<section class="alt"><div class="wrap"><h2>All projects at a glance</h2><div class="table-wrap"><table><thead><tr><th>Project</th><th class="num">Low</th><th class="num">Typical</th><th class="num">High</th><th>DIY?</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="notice" style="margin-top:16px">Typical U.S. installed costs for 2026, compiled from published contractor cost guides, supplier pricing and industry surveys. Canadian prices usually run 20–35% higher in CAD. Always get written local quotes.</p></div></section>"""
    page("cost-guides/index.html", "Home Improvement Cost Guides (2026 Prices)", "2026 cost guides for roofing, HVAC, windows, siding, kitchens, baths, foundations, solar and more — with estimators and money-saving tips.",
         index_body, crumbs=[("Cost guides", None)], priority=0.9, changefreq="weekly")

    for g in GUIDES:
        build_guide(g, cats)


def build_guide(g, cats):
    slug = g["slug"]
    est_data = json.dumps([{k: g[k] for k in ("slug", "name", "service", "low", "high", "avg", "unit_low", "unit_high", "fixed_low", "fixed_high", "min_job",
                                               "size_min", "size_max", "size_step", "default_size", "size_label", "size_unit")}])

    def body(R):
        rows = "".join(f"<tr><td>{E(a)}</td><td class=\"num\">{E(b)}</td></tr>" for a, b in g["rows"])
        factors = "".join(f"<h3>{E(a)}</h3><p>{E(b)}</p>" for a, b in g["factors"])
        signs = "".join(f"<li>{E(s)}</li>" for s in g["signs"])
        tips = "".join(f"<li>{E(s)}</li>" for s in g["tips"])
        qs = "".join(f"<li>{E(s)}</li>" for s in g["questions"])
        rel = "".join(guide_card(R, G[s]) for s in g["related"] if s in G)
        diy_badge = {"Pro only": "coral", "Skilled DIY": "gold", "DIY-friendly": "ok"}[g["diy"]]
        quote = f"{R}get-quotes.html?service={g['service']}"
        toc = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in [("costs", "Cost breakdown"), ("estimator", "Estimate your project"), ("factors", "What drives the price"),
                                                                      ("signs", "Signs you need it"), ("diy", "DIY or hire a pro?"), ("video", "Watch"), ("save", "How to save"), ("questions", "Questions to ask"), ("faq", "FAQ")])
        hero_extra = (f'<div class="meta-row"><span>Typical: <b>{money(g["avg"])}</b></span><span>Range: <b>{money(g["low"])} – {money(g["high"])}</b></span>'
                      f'<span>Duration: <b>{E(g["duration"])}</b></span><span>Lifespan: <b>{E(g["lifespan"])}</b></span></div>'
                      f'<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:18px"><a class="btn" href="{quote}">Get free {E(g["name"].lower())} quotes</a><a class="btn ghost" href="#estimator">Estimate my cost</a></div>')
        return page_hero(R, f"{E(g['name'])} Cost in 2026", E(g["intro"]), [("Cost guides", "cost-guides/index.html"), (g["name"], None)], cats.get(g["cat"], "Cost guide"), hero_extra) + f"""
<div class="wrap layout">
<article class="prose">
  <div class="big-price"><div><span>Low end</span><b>{money(g['low'])}</b></div><div class="avg"><span>Typical</span><b>{money(g['avg'])}</b></div><div><span>High end</span><b>{money(g['high'])}</b></div></div>
  <h2 id="costs">{E(g['name'])} cost breakdown</h2>
  <div class="table-wrap"><table><thead><tr><th>Option</th><th class="num">Typical installed cost</th></tr></thead><tbody>{rows}</tbody></table></div>
  <h2 id="estimator">Estimate your {E(g['name'].lower())} cost</h2>
  <div class="calc" data-tool="estimator">
    <div>
      <div class="field"><label for="est-size">{E(g['size_label'])}</label><div class="range"><input id="est-size" type="range" name="size" min="{g['size_min']}" max="{g['size_max']}" step="{g['size_step']}" value="{g['default_size']}"><output data-out="size_val"></output></div></div>
      <div class="field"><span class="label">Quality level</span><div class="seg"><label><input type="radio" name="quality" value="economy"><span>Economy</span></label><label><input type="radio" name="quality" value="standard" checked><span>Standard</span></label><label><input type="radio" name="quality" value="premium"><span>Premium</span></label></div></div>
      <div class="field"><span class="label">Location</span><div class="seg"><label><input type="radio" name="region" value="low"><span>Lower-cost area</span></label><label><input type="radio" name="region" value="avg" checked><span>Average</span></label><label><input type="radio" name="region" value="high"><span>High-cost metro</span></label><label><input type="radio" name="region" value="ca"><span>Canada (CAD)</span></label></div></div>
      <div class="field"><span class="label">Complexity</span><div class="seg"><label><input type="radio" name="complexity" value="simple"><span>Simple</span></label><label><input type="radio" name="complexity" value="typical" checked><span>Typical</span></label><label><input type="radio" name="complexity" value="complex"><span>Complex</span></label></div></div>
    </div>
    <div class="result"><h3>Your estimated range (<span data-out="currency">USD</span>)</h3><div class="big"><span data-out="low">—</span> – <span data-out="high">—</span></div><div class="sub">Midpoint <b data-out="mid">—</b> · <span data-out="per_unit"></span></div>
      <dl><dt>National typical range</dt><dd data-out="national">—</dd><dt>Duration</dt><dd>{E(g['duration'])}</dd></dl>
      <a class="btn light" href="{quote}">Check it against real quotes →</a></div>
  </div>
  <script type="application/json" id="guides-data">{est_data}</script>
  <h2 id="factors">What drives the price</h2>{factors}
  <h2 id="signs">Signs you need {E(g['name'].lower())}</h2><ul class="checklist">{signs}</ul>
  <h2 id="diy">DIY or hire a pro?</h2><p><span class="badge {diy_badge}">{E(g['diy'])}</span></p><p>{E(g['diy_text'])}</p>
  <div class="callout coral"><h4>Get up to 3 free {E(g['name'].lower())} quotes</h4><p>Compare local pros against the ranges above. Free, no obligation.</p>
    <form data-quick action="{R}get-quotes.html" class="inline-form" novalidate style="margin-top:10px"><input type="hidden" name="service" value="{g['service']}"><label class="sr-only" for="inl-zip">ZIP</label><input id="inl-zip" name="zip" data-zip required placeholder="ZIP or postal code"><button class="btn" type="submit">Get quotes</button></form></div>
  <h2 id="video">Watch: {E(g['video'][1])}</h2>{yt(g['video'][0], g['video'][1])}<p class="small muted" style="margin-top:8px">Video plays from YouTube; rights remain with the creator.</p>
  <h2 id="save">How to save on {E(g['name'].lower())}</h2><ul>{tips}</ul>
  <h2 id="questions">Questions to ask before you hire</h2><ol>{qs}</ol>
  <h2 id="faq">{E(g['name'])} FAQ</h2>{faq_html(g['faq'])}
  <p class="notice" style="margin-top:24px">Resale value: {E(g['roi'])}. Cost data: typical U.S. installed prices for 2026 compiled by Home.Direct from published contractor cost guides, supplier pricing and industry surveys; reviewed November 2026. Canadian prices often run 20–35% higher in CAD. Get written local quotes before you decide.</p>
  <h2>Related cost guides</h2><div class="grid g3">{rel}</div>
</article>
<aside class="aside">
  {quote_mini(R, g['service'], f"Get {E(g['name'].lower())} quotes")}
  <div class="card"><h3>On this page</h3><ul class="toc">{toc}</ul></div>
  <div class="card"><h3>Paying for it?</h3><p class="small muted">Compare a HELOC, cash-out refi or renovation loan before you sign a contractor's financing plan.</p><a class="link-arrow" href="{R}finance.html?goal=renovation-loan#lender-form">See financing options</a></div>
</aside>
</div>"""
    ld = [faq_ld(g["faq"]), {"@context": "https://schema.org", "@type": "Article", "headline": f"{g['name']} Cost in 2026", "description": g["intro"][:300],
                             "dateModified": TODAY.isoformat(), "author": {"@type": "Organization", "name": SITE}, "publisher": {"@type": "Organization", "name": SITE}}]
    page(f"cost-guides/{slug}.html", f"{g['name']} Cost (2026): Prices, Estimator & Tips",
         f"{g['name']} costs {money(g['low'])}–{money(g['high'])} in 2026 (typical {money(g['avg'])}). See price breakdowns, a cost estimator, money-saving tips and free local quotes.",
         body, crumbs=[("Cost guides", "cost-guides/index.html"), (g["name"], None)], ld=ld, tools=True, og_type="article", priority=0.8)


# ---------------------------------------------------------------- MAINTENANCE / VIDEOS / NEWS
def build_maintenance():
    data = json.dumps([{"name": m["name"], "short": m["short"], "note": m["note"], "tasks": [list(t) for t in m["tasks"]]} for m in MONTHS])
    faqs = [("How often should I replace my HVAC filter?", "Every 1–3 months for 1-inch filters; every 6–12 months for 4–5-inch media filters. More often with pets or allergies."),
            ("What maintenance prevents the most expensive damage?", "Water management: clean gutters, working sump pumps, sealed windows, and catching small leaks early prevent most big-ticket repairs."),
            ("Does my checklist save?", "Yes — checkmarks are stored in your browser on this device for the current year. Nothing is uploaded.")]

    def body(R):
        return page_hero(R, "Home maintenance planner", "A month-by-month checklist that saves your progress in your browser. Tick tasks off, print it, or get a pro for anything you'd rather not tackle.",
                         [("Maintenance planner", None)], "Interactive") + f"""
<section><div class="wrap" id="planner">
  <div class="month-tabs" role="tablist" aria-label="Months"></div>
  <div class="grid" style="grid-template-columns:1fr auto;align-items:center;gap:20px;margin-bottom:16px"><div><h2 id="month-title" style="margin:0"></h2><p class="muted" id="month-note" style="margin:6px 0 0"></p></div><div class="ring"><b>0%</b></div></div>
  <div id="task-list"></div>
  <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:14px" class="no-print"><button class="btn ghost sm" type="button" data-print>Print this month</button><button class="btn ghost sm" type="button" data-reset>Reset checkmarks</button><a class="btn sm" href="{R}get-quotes.html">Get help from a pro</a></div>
  <script type="application/json" id="tasks-data">{data}</script>
</div></section>
<section class="alt"><div class="wrap narrow"><h2>Maintenance FAQ</h2>{faq_html(faqs)}</div></section>"""
    page("maintenance.html", "Home Maintenance Checklist by Month (Interactive)", "A free, interactive month-by-month home maintenance checklist that saves your progress. Prevent costly repairs year-round.",
         body, crumbs=[("Maintenance planner", None)], ld=[faq_ld(faqs)], priority=0.7)


def build_videos():
    items = VIDEOS.get("items", [])
    chans = sorted({v.get("channel", "") for v in items if v.get("channel")})

    def body(R):
        bar = '<button type="button" data-cat="all" aria-pressed="true">All</button>' + "".join(f'<button type="button" data-cat="{E(c)}" aria-pressed="false">{E(c)}</button>' for c in chans)
        cards = "".join(f'<div class="video-card" data-cat="{E(v.get("channel", ""))}">{yt(v["id"], v["title"])}<b>{E(v["title"])}</b><small>{E(v.get("channel", ""))}{(" · " + E(v["date_label"])) if v.get("date_label") else ""}</small></div>' for v in items)
        guide_vids = "".join(f'<div class="video-card">{yt(g["video"][0], g["video"][1])}<b>{E(g["video"][1])}</b><small><a href="{R}cost-guides/{g["slug"]}.html">{E(g["name"])} cost guide</a></small></div>' for g in GUIDES[:12])
        return page_hero(R, "Home improvement video hub", f"The newest how-to and project videos from leading home channels, refreshed automatically. Last update: {E(VIDEOS.get('updated_label', BUILT))}.",
                         [("Videos", None)], "Watch & learn") + f"""
<section><div class="wrap"><div class="filter-bar" data-filter-group="vid-grid">{bar}</div><div class="grid g3" id="vid-grid">{cards or '<p class="muted">New videos load automatically.</p>'}</div></div></section>
<section class="alt"><div class="wrap"><h2>Project walkthroughs from our cost guides</h2><div class="grid g3">{guide_vids}</div>
<p class="notice" style="margin-top:18px">Videos are embedded with YouTube's privacy-enhanced player and load only when you press play. All rights belong to their creators; Home.Direct is not affiliated with these channels.</p></div></section>"""
    page("videos.html", "Home Improvement Videos: Latest How-Tos", "Watch the latest home improvement, repair and renovation videos from top channels — auto-updated — plus walkthroughs for 24 projects.",
         body, crumbs=[("Videos", None)], priority=0.6, changefreq="daily")


def build_news():
    items = NEWS.get("items", [])
    cats = []
    for it in items:
        if it.get("cat") and it["cat"] not in cats:
            cats.append(it["cat"])

    def body(R):
        bar = '<button type="button" data-cat="all" aria-pressed="true">All</button>' + "".join(f'<button type="button" data-cat="{E(c)}" aria-pressed="false">{E(c)}</button>' for c in cats)
        return page_hero(R, "Housing & home improvement news", f"Headlines on mortgage rates, the housing market, home improvement and insurance from publishers across the web. Refreshed automatically — last update {E(NEWS.get('updated_label', BUILT))}.",
                         [("News", None)], "Auto-updated") + f"""
<section><div class="wrap layout" style="padding-top:0"><div><div class="filter-bar" data-filter-group="news-wrap">{bar}</div><div id="news-wrap">{news_items(R, 60)}</div>
<p class="notice" style="margin-top:20px">Headlines and links point to the original publishers; we don't reproduce articles. Inclusion isn't endorsement.</p></div>
<aside class="aside">{rate_strip(R, compact=True)}{quote_mini(R)}</aside></div></section>"""
    page("news.html", "Housing Market & Mortgage News Today", "Auto-updated headlines on mortgage rates, home prices, the housing market, home improvement and insurance in the U.S. and Canada.",
         body, crumbs=[("News", None)], priority=0.6, changefreq="hourly")


# ---------------------------------------------------------------- site files
def write_support_files():
    # search index
    idx = [{"t": "Get free quotes", "d": "Match with up to 3 local pros", "u": "get-quotes.html", "k": "contractor hire quote estimate pro", "p": 1},
           {"t": "Sell direct", "d": "Cash offers, FSBO, flat-fee MLS, low-fee agents", "u": "sell-direct.html", "k": "sell house cash offer fsbo realtor commission", "p": 1},
           {"t": "Mortgage rates & finance", "d": "Live rates, lender matching", "u": "finance.html", "k": "mortgage rate refinance heloc lender loan", "p": 1},
           {"t": "Maintenance planner", "d": "Month-by-month checklist", "u": "maintenance.html", "k": "maintenance checklist seasonal", "p": 1},
           {"t": "Video hub", "d": "Latest how-to videos", "u": "videos.html", "k": "video youtube how to diy", "p": 0},
           {"t": "Housing news", "d": "Auto-updated headlines", "u": "news.html", "k": "news market housing", "p": 0},
           {"t": "Monthly contest", "d": "Win prizes for your project", "u": "contests.html", "k": "contest prize giveaway win", "p": 0},
           {"t": "Support Home.Direct", "d": "Donate or sponsor", "u": "support.html", "k": "donate donation sponsor support", "p": 0},
           {"t": "Careers & talent", "d": "Writers, reviewers, creators", "u": "careers.html", "k": "jobs careers hiring work", "p": 0},
           {"t": "For pros", "d": "Exclusive ZIP leads", "u": "pros.html", "k": "contractor leads join network", "p": 0},
           {"t": "Advertise", "d": "Sponsorships & placements", "u": "advertise.html", "k": "advertise sponsorship ads", "p": 0},
           {"t": "Contact", "d": "Send us a message", "u": "contact.html", "k": "contact email help", "p": 0}]
    for g in GUIDES:
        idx.append({"t": f"{g['name']} cost", "d": f"{money(g['low'])}–{money(g['high'])} · typical {money(g['avg'])}", "u": f"cost-guides/{g['slug']}.html",
                    "k": f"{g['name']} {g['service']} {g['cat']} price cost estimate", "p": 1 if g["slug"] in ("roof-replacement", "hvac-replacement", "kitchen-remodel", "bathroom-remodel") else 0})
    for t in pages_tools.TOOLS:
        idx.append({"t": t["name"], "d": t["short"], "u": f"tools/{t['slug']}.html", "k": t.get("kw", "calculator"), "p": 1 if t["slug"] in ("mortgage-calculator", "net-proceeds-calculator") else 0})
    (DATA / "search-index.json").write_text(json.dumps(idx, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (DATA / "guides.json").write_text(json.dumps(GUIDES, ensure_ascii=False, indent=1), encoding="utf-8")

    # sitemap
    urls = []
    for path, pr, cf in sorted(set(PAGES)):
        loc = DOMAIN + "/" + ("" if path == "index.html" else path)
        urls.append(f"<url><loc>{loc}</loc><lastmod>{TODAY.isoformat()}</lastmod><changefreq>{cf}</changefreq><priority>{pr:.1f}</priority></url>")
    (ROOTDIR / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
    (ROOTDIR / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /thank-you.html\nDisallow: /scripts/\n\nUser-agent: Mediapartners-Google\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n", encoding="utf-8")
    (ROOTDIR / "ads.txt").write_text("google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0\n", encoding="utf-8")
    (ROOTDIR / "site.webmanifest").write_text(json.dumps({"name": SITE, "short_name": SITE, "start_url": "./index.html", "display": "standalone",
                                                          "background_color": "#fbf8f3", "theme_color": "#0d1b2a",
                                                          "icons": [{"src": "assets/img/logo-192.png", "sizes": "192x192", "type": "image/png"},
                                                                    {"src": "assets/img/logo-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=1), encoding="utf-8")
    (ROOTDIR / ".nojekyll").write_text("", encoding="utf-8")


def main():
    build_home()
    build_quotes()
    build_sell()
    build_finance()
    build_guides()
    build_maintenance()
    build_videos()
    build_news()
    pages_tools.build_all()
    pages_more.build_all()
    write_support_files()
    print(f"Built {len(PAGES)} indexable pages on {TODAY.isoformat()}")


if __name__ == "__main__":
    main()
