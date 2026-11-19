# -*- coding: utf-8 -*-
"""Community, business, legal and utility pages for Home.Direct."""
import calendar
from hd_core import (TODAY, PARTNER_URL, E, icon, page, page_hero, faq_html, faq_ld, radios, field, select, zip_field,
                     simple_form, success, CONSENT)
from site_data import CONTEST_THEMES, CONTEST_PRIZES, ROLES, SERVICES

EFFECTIVE = "November 19, 2026"


def _season():
    y, m = TODAY.year, TODAY.month
    last = calendar.monthrange(y, m)[1]
    ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
    return dict(theme=CONTEST_THEMES[m - 1], month=calendar.month_name[m], year=y, start=f"{calendar.month_name[m]} 1, {y}",
                end=f"{calendar.month_name[m]} {last}, {y}", end_iso=f"{y}-{m:02d}-{last:02d}T23:59:59-05:00",
                announce=f"{calendar.month_name[nm]} 15, {ny}", next_theme=CONTEST_THEMES[nm - 1], next_month=calendar.month_name[nm])


# ---------------------------------------------------------------- SUPPORT / DONATE
def build_support():
    faqs = [("Is my donation tax-deductible?", "No. Home.Direct is an independent business, not a registered charity, so contributions are not tax-deductible."),
            ("How is the money used?", "Support goes to the four funds you choose: operations (hosting, data, tools), promotions and marketing, hiring writers/reviewers/creators, and contest prizes. Sponsors are acknowledged on this page with permission."),
            ("Can I donate prizes or products instead?", "Yes — use the sponsor form to offer gift cards, tools or services for the monthly contest."),
            ("Is payment secure?", "Donations are processed by PayPal. We never see or store your card details.")]

    def body(R):
        funds = [("Operations", "server", "Keeps the guides, calculators and auto-updating data free: hosting, data feeds, research and tools.", "home"),
                 ("Promotions & Marketing", "megaphone", "Helps more homeowners find unbiased cost data before they sign a contract.", "megaphone"),
                 ("Hiring Talent", "briefcase", "Pays licensed contractors to fact-check guides and creators to make how-to videos.", "briefcase"),
                 ("Contests & Prizes", "trophy", "Funds monthly gift-card prizes and featured stories for homeowners' best projects.", "trophy")]
        cards = "".join(f'<div class="tier"><span class="card-icon {"coral" if i % 2 else ""}">{icon(ic)}</span><h3>{E(n)}</h3><p class="muted small">{E(d)}</p>'
                        f'<button class="btn sm ghost" type="button" data-purpose-pick="{E(n)}" onclick="document.getElementById(\'give\').scrollIntoView({{behavior:\'smooth\'}})">Fund this</button></div>'
                        for i, (n, _, d, ic) in enumerate(funds))
        purpose = "".join(f'<label class="opt-card"><input type="radio" name="purpose" value="{E(n)}"{" checked" if i == 0 else ""}><span>{E(n)}</span></label>' for i, (n, *_r) in enumerate(funds))
        amounts = "".join(f'<button type="button" data-amount="{a}" aria-pressed="{str(a == 25).lower()}">${a}</button>' for a in (10, 25, 50, 100, 250, 500))
        sponsor = simple_form("sponsor-form", "sponsor", "Sponsor / pledge", f"""<legend>Become a sponsor or pledge support</legend><p class="hint">For larger gifts, recurring sponsorships, prize donations or in-kind support.</p>
<div class="row">{field("Your name", "name", "text", True, "Full name")}{field("Email", "email", "email", True, "you@example.com")}</div>
<div class="row">{field("Organization", "organization", "text", False, "Company (optional)")}{select("Support type", "pledge_type", [("operations", "Operations fund"), ("marketing", "Promotions & marketing"), ("talent", "Hiring talent"), ("prizes", "Contest prizes (cash or gift cards)"), ("in-kind", "In-kind products or services"), ("monthly", "Monthly sponsorship")])}</div>
{select("Amount", "amount", [("under-500", "Under $500"), ("500-2500", "$500 – $2,500"), ("2500-10000", "$2,500 – $10,000"), ("10000+", "$10,000+"), ("in-kind", "In-kind / product")])}
{field("Message", "message", "textarea", False, "Tell us what you'd like to support and how you'd like to be acknowledged.")}""", "Send pledge")
        return page_hero(R, "Support Home.Direct", "Keep unbiased cost guides, calculators and matching free for every homeowner. Choose exactly what your support funds.",
                         [("Support us", None)], "Donate · Sponsor · Pledge") + f"""
<section><div class="wrap"><div class="tiers">{cards}</div></div></section>
<section class="alt" id="give"><div class="wrap grid g2" style="gap:32px;align-items:start">
  <div class="form-shell" data-donate>
    <h2 style="margin-bottom:6px">Give in under a minute</h2><p class="muted small">Secure checkout via PayPal. Cards accepted without a PayPal account.</p>
    <span class="label">1. Choose a fund</span><div class="options two" style="margin-bottom:16px">{purpose}</div>
    <span class="label">2. Choose an amount (USD)</span><div class="amount-pills" style="margin-bottom:10px">{amounts}</div>
    <div class="field"><label for="custom-amount">Or enter an amount</label><input id="custom-amount" type="number" min="1" step="1" placeholder="e.g. 75" inputmode="decimal"></div>
    <button class="btn lg block" type="button" data-donate-go>{icon('heart')} Donate securely with PayPal</button>
    <p class="secure-note">{icon('lock')}<span>You'll complete payment on PayPal's site. Monthly giving can be selected at checkout.</span></p>
  </div>
  <div><div class="form-shell flat">{sponsor}{success("sponsor-form", "Thank you", "We'll reply within two business days to set up your sponsorship or pledge.", R, [("See the contest", "contests.html"), ("Advertise with us", "advertise.html")])}</div></div>
</div></section>
<section><div class="wrap narrow"><h2>Transparency</h2><p>Home.Direct earns revenue from advertising, sponsorships and fees some service providers pay to receive homeowner requests. Donations are optional and do not affect cost data, rankings or which providers we match. Major sponsors are listed here with permission.</p>{faq_html(faqs)}</div></section>"""
    page("support.html", "Support Home.Direct — Donate or Sponsor", "Support free, independent home cost guides and tools. Fund operations, promotions, new talent and monthly contest prizes, or become a sponsor.",
         body, crumbs=[("Support us", None)], ld=[faq_ld(faqs)], priority=0.5)


# ---------------------------------------------------------------- CONTESTS
def build_contests():
    s = _season()
    faqs = [("Is there an entry fee?", "No. Entry is free and no purchase is necessary."), ("Who can enter?", "Legal residents of the 50 U.S. states, D.C. and Canada (excluding Quebec) who are 18 or older, subject to the Official Rules."),
            ("How are winners chosen?", "By a judging panel using the published criteria — this is a skill contest, not a random draw."), ("Do I keep the rights to my photos?", "Yes. You grant Home.Direct a license to display your entry; you keep ownership.")]

    def body(R):
        prizes = "".join(f'<div class="tier{" pop" if i == 0 else ""}"><span class="card-icon gold">{icon("trophy" if i == 0 else "star" if i == 1 else "heart")}</span><h3>{E(a)}</h3><p class="muted">{E(b)}</p></div>' for i, (a, b) in enumerate(CONTEST_PRIZES))
        cats = [(v, l) for _, items in SERVICES for v, l in items][:18]
        form = simple_form("contest-form", "contest", f"Contest entry — {s['theme']}", f"""<legend>Enter: {E(s['theme'])}</legend><p class="hint">Share a before-and-after project you completed (DIY or hired). Upload photos to Google Drive, Dropbox, iCloud or Imgur and paste share links.</p>
<input type="hidden" name="contest_season" value="{E(s['month'])} {s['year']} — {E(s['theme'])}">
<div class="row">{field("First name", "first_name", "text", True, "Jane")}{field("Last name", "last_name", "text", True, "Doe")}</div>
<div class="row">{field("Email", "email", "email", True, "you@example.com")}{field("State or province", "region", "text", True, "e.g. Texas or Ontario")}</div>
<div class="row">{select("Project category", "category", cats)}{field("Project title", "title", "text", True, "Kitchen glow-up under $5k")}</div>
{field("Your story", "story", "textarea", True, "What was the problem, what did you do, what did it cost, and what would you do differently? (80+ characters)", attrs='minlength="80"', err="Please write at least 80 characters.")}
<div class="row">{field("Before photo link", "before_url", "url", True, "https://…", err="Enter a full link starting with https://")}{field("After photo link", "after_url", "url", True, "https://…", err="Enter a full link starting with https://")}</div>
{field("Approximate budget spent", "spent", "text", False, "$4,800")}
<div class="field"><label class="check"><input type="checkbox" name="age_confirm" value="yes" required> <span>I'm 18 or older and a legal resident of an eligible U.S. state, D.C. or Canadian province/territory (excluding Quebec).</span></label><div class="err-msg">Required to enter.</div></div>
<div class="field"><label class="check"><input type="checkbox" name="rules_accept" value="yes" required> <span>I accept the <a href="{R}contest-rules.html" target="_blank">Official Rules</a> and confirm I own or have permission to share these photos.</span></label><div class="err-msg">Required to enter.</div></div>""", "Submit my entry", "Entries are reviewed by our judging panel. We never publish your email.")
        return page_hero(R, f"Monthly contest: {E(s['theme'])}", f"Show us your best home project and win. Entries for {E(s['month'])} close {E(s['end'])} at 11:59 p.m. ET; winners announced by {E(s['announce'])}.",
                         [("Contest", None)], "Free to enter", f'<p style="margin-top:12px"><span class="badge gold" data-countdown="{s["end_iso"]}">Entries open</span></p>') + f"""
<section><div class="wrap"><h2>Prizes this month</h2><div class="tiers t3">{prizes}</div>
<p class="small muted" style="margin-top:12px">Prize pool funded by sponsors and supporters — <a href="{R}support.html">add to the prize fund</a> or <a href="{R}support.html#give">donate a prize</a>.</p></div></section>
<section class="alt"><div class="wrap layout" style="padding-top:10px">
  <div class="form-shell">{form}{success("contest-form", "You're entered", "Good luck! Judges review entries after the deadline and contact winners by email.", R, [("Browse cost guides", "cost-guides/index.html"), ("Support the prize fund", "support.html")])}</div>
  <aside class="aside"><div class="card"><h3>How we judge</h3><ul class="small"><li><b>40%</b> transformation impact</li><li><b>30%</b> quality of workmanship</li><li><b>20%</b> budget smarts</li><li><b>10%</b> story & tips for others</li></ul></div>
  <div class="card"><h3>Next month</h3><p class="small muted">{E(s['next_month'])}: <b>{E(s['next_theme'])}</b>. Start planning your project now.</p></div>
  <div class="card"><h3>Sponsor a prize</h3><p class="small muted">Put your brand in front of motivated homeowners.</p><a class="link-arrow" href="{R}advertise.html">Sponsorship options</a></div></aside>
</div></section>
<section><div class="wrap narrow"><h2>Contest FAQ</h2>{faq_html(faqs)}<p class="notice">No purchase necessary. Void where prohibited. See the <a href="{R}contest-rules.html">Official Rules</a> for eligibility, judging and prize details.</p></div></section>"""
    page("contests.html", f"Home Project Contest — {s['theme']} ({s['month']} {s['year']})", "Enter Home.Direct's free monthly home-project contest. Share your before-and-after, win gift cards and a featured story. No purchase necessary.",
         body, crumbs=[("Contest", None)], ld=[faq_ld(faqs)], priority=0.6, changefreq="weekly")

    def rules(R):
        return page_hero(R, "Official contest rules", f"Home.Direct Monthly Home Project Contest — {E(s['month'])} {s['year']}: “{E(s['theme'])}”. Effective for the current entry period.", [("Contest", "contests.html"), ("Official rules", None)]) + f"""
<section><div class="wrap narrow prose">
<p><b>NO PURCHASE OR PAYMENT OF ANY KIND IS NECESSARY TO ENTER OR WIN. A PURCHASE WILL NOT IMPROVE YOUR CHANCES OF WINNING. VOID WHERE PROHIBITED.</b></p>
<h2>1. Sponsor</h2><p>The contest is sponsored by Home.Direct (“Sponsor”). Questions may be sent through the <a href="{R}contact.html">contact form</a>.</p>
<h2>2. Eligibility</h2><p>Open to legal residents of the 50 United States, the District of Columbia and Canada (excluding the Province of Quebec) who are 18 years of age or older (or the age of majority in their province or territory) at the time of entry. Employees and contractors of Sponsor, its judges and their immediate family and household members are not eligible.</p>
<h2>3. Entry period</h2><p>The current entry period begins at 12:00 a.m. ET on {E(s['start'])} and ends at 11:59 p.m. ET on {E(s['end'])}. Entries received after the deadline are not eligible for this period.</p>
<h2>4. How to enter</h2><p>Complete the entry form on the contest page, including a written description (at least 80 characters) and links to at least one “before” and one “after” photo of a home project you completed or commissioned. Limit one (1) entry per person per entry period. Entries must be original, owned by the entrant (or used with permission), and must not contain identifiable people without their consent, offensive material, or third-party trademarks as a focus.</p>
<h2>5. Judging</h2><p>This is a contest of skill. Eligible entries are judged by a panel selected by Sponsor using these criteria: transformation impact (40%), quality of workmanship (30%), budget smarts (20%) and story and usefulness to other homeowners (10%). In case of a tie, the entry with the higher transformation score wins. Judges' decisions are final.</p>
<h2>6. Prizes</h2><ul>{"".join(f"<li><b>{E(a)}:</b> {E(b)}.</li>" for a, b in CONTEST_PRIZES)}</ul><p>Gift cards are issued by third-party retailers and subject to their terms. Prizes are non-transferable; no substitution except by Sponsor, who may substitute a prize of equal or greater value. Winners are responsible for applicable taxes. Canadian residents selected as potential winners must correctly answer a time-limited, mathematical skill-testing question before being confirmed.</p>
<h2>7. Winner notification</h2><p>Potential winners will be notified by email by {E(s['announce'])} and must respond within seven (7) days and sign any required declaration of eligibility and release, or an alternate winner may be selected.</p>
<h2>8. License to use entries</h2><p>Entrants retain ownership of their photos and text. By entering, entrants grant Sponsor a non-exclusive, royalty-free, worldwide license to display, reproduce and edit (for length and format) the entry on Home.Direct and its newsletters and social channels, with credit by first name and state or province.</p>
<h2>9. Privacy</h2><p>Information collected is used to administer the contest and as described in our <a href="{R}privacy.html">Privacy Policy</a>. We do not publish entrants' email addresses.</p>
<h2>10. General conditions</h2><p>Sponsor may disqualify entries that violate these rules or are submitted fraudulently, and may cancel or modify the contest if it cannot run as planned. Sponsor is not responsible for lost, late or misdirected entries or technical failures. Released parties are not liable for injuries or losses arising from participation or prize acceptance, to the extent permitted by law.</p>
<h2>11. Governing law</h2><p>These rules are governed by the laws applicable in the entrant's jurisdiction of residence where required, and otherwise by the laws of the Province of Quebec and the federal laws of Canada applicable therein.</p>
</div></section>"""
    page("contest-rules.html", "Official Contest Rules", "Official rules for the Home.Direct monthly home project contest: eligibility, entry, judging, prizes and conditions.", rules,
         crumbs=[("Contest", "contests.html"), ("Official rules", None)], priority=0.3)


# ---------------------------------------------------------------- CAREERS
def build_careers():
    def body(R):
        roles = "".join(f'<div class="card"><span class="badge">Remote · Flexible</span><h3 style="margin-top:10px">{E(t)}</h3><p class="muted">{E(d)}</p><a class="link-arrow" href="#apply" onclick="document.getElementById(\'f-role\').value=\'{v}\'">Apply for this role</a></div>' for v, t, d in ROLES)
        form = simple_form("career-form", "career", "Talent application", f"""<legend>Apply or join the talent network</legend><p class="hint">Tell us what you do best. We review every application.</p>
<div class="row">{field("Full name", "name", "text", True, "Your name")}{field("Email", "email", "email", True, "you@example.com")}</div>
<div class="row">{select("Role", "role", [(v, t) for v, t, _ in ROLES] + [("other", "Something else")])}{field("City / region", "location", "text", True, "e.g. Austin, TX or Montréal, QC")}</div>
<div class="row">{field("Portfolio, LinkedIn or channel", "portfolio", "url", True, "https://…", err="Enter a full link starting with https://")}{select("Experience", "experience", [("0-2", "0–2 years"), ("3-5", "3–5 years"), ("6-10", "6–10 years"), ("10+", "10+ years")])}</div>
<div class="row">{select("Availability", "availability", [("few-hours", "A few hours a week"), ("part-time", "Part-time"), ("full-time", "Full-time"), ("project", "Per project")])}{field("Expected rate", "rate", "text", False, "e.g. $0.15/word, $60/hr, per video")}</div>
{field("Why you?", "message", "textarea", True, "Licenses, trades, topics, past work…")}""", "Send application")
        return page_hero(R, "Careers & talent network", "We're building the most useful home-money resource on the web — and we hire experts, writers and creators to do it.", [("Careers", None)], "We're hiring") + f"""
<section><div class="wrap"><div class="grid g3">{roles}</div></div></section>
<section class="alt" id="apply"><div class="wrap layout" style="padding-top:10px"><div class="form-shell">{form}{success("career-form", "Application received", "Thanks for applying. If there's a fit, we'll reach out with a paid trial assignment.", R, [("Read a cost guide", "cost-guides/roof-replacement.html"), ("About Home.Direct", "about.html")])}</div>
<aside class="aside"><div class="card"><h3>How we work</h3><ul class="checklist small"><li>Remote-first, async</li><li>Paid trial assignments</li><li>Licensed experts credited on pages they review</li><li>Fast payment on approval</li></ul></div></aside></div></section>"""
    page("careers.html", "Careers: Writers, Contractor Reviewers & Creators", "Join Home.Direct's talent network: home-improvement writers, licensed contractor reviewers, video creators, partnership reps and moderators.",
         body, crumbs=[("Careers", None)], priority=0.4)


# ---------------------------------------------------------------- PROS & ADVERTISE
def build_pros():
    trades = [(v, l) for _, items in SERVICES for v, l in items]
    faqs = [("How are leads delivered?", "By email in real time, with the homeowner's project details, timeline, budget and contact information."), ("Are leads exclusive?", "You choose: shared (up to 3 pros) or exclusive ZIP territories where available."),
            ("What does it cost?", "Pay-per-lead pricing depends on trade and market. Exclusive territories are priced monthly. Tell us your trade and ZIPs for a quote."), ("Do you vet pros?", "We ask for license and insurance details where required and may remove pros with complaints.")]

    def body(R):
        form = simple_form("pro-form", "pro", "Pro network signup", f"""<legend>Get homeowner leads in your ZIP codes</legend><p class="hint">Tell us about your business — we'll reply with availability and pricing.</p>
<div class="row">{field("Company name", "company", "text", True, "Acme Roofing")}{select("Primary trade", "trade", trades)}</div>
<div class="row">{field("Service ZIP / postal codes", "service_zips", "text", True, "e.g. 30301, 30305 or H2X, H2T")}{field("License number", "license", "text", False, "If your trade requires one")}</div>
{radios("insured", [("yes", "Yes, liability insured"), ("no", "Not yet")], cls="options two", label="Liability insurance")}
<div class="row">{select("Years in business", "years", [("0-2", "0–2"), ("3-5", "3–5"), ("6-10", "6–10"), ("10+", "10+")])}{select("Monthly lead budget", "lead_budget", [("under-500", "Under $500"), ("500-1500", "$500 – $1,500"), ("1500-5000", "$1,500 – $5,000"), ("5000+", "$5,000+")])}</div>
{radios("exclusive", [("shared", "Shared leads"), ("exclusive", "Exclusive ZIP territory"), ("both", "Show me both")], label="Lead type")}
<div class="row">{field("Contact name", "name", "text", True, "Your name")}{field("Email", "email", "email", True, "you@company.com")}</div>
{field("Phone", "phone", "tel", True, "(555) 555-0123")}""", "Request lead pricing")
        return page_hero(R, "Grow with homeowner leads that are ready to hire", "Homeowners use Home.Direct to price projects, then request quotes. Get their requests in your ZIP codes — shared or exclusive.", [("For pros", None)], "For contractors & service pros") + f"""
<section><div class="wrap"><div class="grid g4">
<div class="stat"><b>24</b><span>project categories with cost guides</span></div><div class="stat"><b>≤ 3</b><span>pros per shared request</span></div><div class="stat"><b>US + CA</b><span>ZIP & postal coverage</span></div><div class="stat"><b>Real-time</b><span>email lead delivery</span></div></div></div></section>
<section class="alt"><div class="wrap layout" style="padding-top:10px"><div class="form-shell">{form}{success("pro-form", "Thanks", "We'll reply within two business days with territory availability and pricing.", R, [("Advertising options", "advertise.html"), ("See a cost guide", "cost-guides/roof-replacement.html")])}</div>
<aside class="aside"><div class="card"><h3>What's in a lead</h3><ul class="checklist small"><li>Service, scope and property type</li><li>ZIP / postal code</li><li>Timeline and budget</li><li>Lead score (Hot / Warm / Cool)</li><li>Name, phone, email and best time</li></ul></div></aside></div></section>
<section><div class="wrap narrow"><h2>Pro FAQ</h2>{faq_html(faqs)}</div></section>"""
    page("pros.html", "Contractor Leads: Join the Home.Direct Pro Network", "Get homeowner leads for roofing, HVAC, plumbing, remodeling and more in your ZIP codes. Shared or exclusive territories in the U.S. and Canada.",
         body, crumbs=[("For pros", None)], ld=[faq_ld(faqs)], priority=0.5)

    def adv(R):
        pk = [("Featured Pro listing", "From $49/mo", ["Badge on matching cost guides", "Priority in your ZIPs", "Monthly performance email"]),
              ("Category sponsorship", "From $299/mo", ["Sponsor a cost guide category", "Logo + link on guide pages", "Labeled 'Sponsored'"], True),
              ("Newsletter sponsorship", "From $99/issue", ["Native placement in the monthly home brief", "One link + 60 words", "Audience: active homeowners"]),
              ("Contest prize sponsor", "In-kind or $250+", ["Brand on the monthly contest page", "Winner announcement mention", "Social shout-outs"])]
        pop_badge = '<span class="badge coral">Most popular</span>'
        tiers = "".join(
            '<div class="tier' + (" pop" if len(p) > 3 else "") + '">' + (pop_badge if len(p) > 3 else "")
            + f'<h3>{E(p[0])}</h3><div class="amt">{E(p[1])}</div><ul>' + "".join(f"<li>{E(x)}</li>" for x in p[2])
            + '</ul><a class="btn sm' + ("" if len(p) > 3 else " ghost") + '" href="#ad-form">Request this</a></div>' for p in pk)
        form = simple_form("ad-form-el", "advertise", "Advertising inquiry", f"""<legend>Advertising & sponsorship inquiry</legend><p class="hint">Indicative starting rates; final quotes depend on placement, category and traffic.</p>
<div class="row">{field("Company", "company", "text", True, "Brand or business")}{field("Website", "website", "url", True, "https://…", err="Enter a full link starting with https://")}</div>
<div class="row">{select("Interested in", "ad_type", [("featured-pro", "Featured Pro listing"), ("category", "Category sponsorship"), ("newsletter", "Newsletter sponsorship"), ("contest", "Contest prize sponsorship"), ("leads", "Pay-per-lead / exclusive ZIPs"), ("content", "Content partnership"), ("domain", "Website / domain acquisition")])}{select("Monthly budget", "budget_range", [("under-500", "Under $500"), ("500-2500", "$500 – $2,500"), ("2500-10000", "$2,500 – $10,000"), ("10000+", "$10,000+")])}</div>
<div class="row">{field("Your name", "name", "text", True, "Full name")}{field("Email", "email", "email", True, "you@company.com")}</div>
{field("Goals & timing", "message", "textarea", False, "Markets, audiences, launch date…")}""", "Send inquiry")
        return page_hero(R, "Advertise on Home.Direct", "Reach homeowners while they're pricing projects, comparing ways to sell and shopping for financing.", [("Advertise", None)], "Sponsorships & placements",
                         f'<p style="margin-top:14px"><a class="btn ghost" href="{PARTNER_URL}" target="_blank" rel="noopener">Partnership & domain inquiries →</a></p>') + f"""
<section><div class="wrap"><div class="tiers">{tiers}</div><p class="small muted" style="margin-top:14px">All sponsored placements are clearly labeled. Sponsors never influence cost data, calculator results or editorial rankings.</p></div></section>
<section class="alt" id="ad-form"><div class="wrap narrow"><div class="form-shell">{form}{success("ad-form-el", "Thanks", "We'll send a media kit and availability within two business days.", R, [("For pros", "pros.html"), ("Support Home.Direct", "support.html")])}</div></div></section>"""
    page("advertise.html", "Advertise & Sponsor on Home.Direct", "Featured pro listings, category and newsletter sponsorships, contest prize sponsorships and pay-per-lead options for home brands and contractors.",
         adv, crumbs=[("Advertise", None)], priority=0.5)


# ---------------------------------------------------------------- ABOUT / CONTACT / FAQ
def build_about_contact_faq():
    def about(R):
        return page_hero(R, "About Home.Direct", "Home decisions involve big numbers and too many middlemen. We give homeowners the numbers first — then a direct line to the people who can help.", [("About", None)]) + f"""
<section><div class="wrap narrow prose">
<h2>What we do</h2><p>Home.Direct publishes free cost guides for 24 common home projects, twelve calculators for buying, borrowing, selling and renovating, a month-by-month maintenance planner, and curated housing news and videos that refresh automatically. When you're ready, one short form connects you with up to three local providers — contractors, cash buyers, low-fee listing options or licensed lenders.</p>
<h2>How we make money</h2><p>Using Home.Direct is free. We earn revenue from display advertising (Google AdSense), clearly labeled sponsorships, and fees some providers pay when they receive homeowner requests. Optional donations support operations, promotion, hiring talent and contest prizes. None of these change our cost data or calculator math.</p>
<h2>How we build cost data</h2><p>Guides list typical U.S. installed-cost ranges for 2026, compiled from published contractor cost guides, supplier pricing and industry surveys, with notes for Canadian pricing. Estimators apply transparent multipliers for size, quality, location and complexity. Mortgage rates come from Freddie Mac's weekly Primary Mortgage Market Survey via the Federal Reserve Bank of St. Louis (FRED).</p>
<h2>What we are not</h2><p>We are not a contractor, real estate brokerage, lender, mortgage broker, insurer or financial advisor. Always verify licenses, get written quotes and consult qualified professionals for your situation.</p>
<h2>Get in touch</h2><p>Use our <a href="{R}contact.html">contact form</a>. For sponsorship, advertising, partnership or domain inquiries, <a href="{PARTNER_URL}" target="_blank" rel="noopener">contact our partnerships team</a>.</p>
</div></section>"""
    page("about.html", "About Home.Direct", "Home.Direct gives homeowners free cost data, calculators and a direct line to local pros, cash buyers and lenders — without the middleman markup.", about, crumbs=[("About", None)], priority=0.5)

    def contact(R):
        form = simple_form("contact-form", "contact", "Contact message", f"""<legend>Send us a message</legend><p class="hint">We read everything and reply within two business days.</p>
<div class="row">{field("Name", "name", "text", True, "Your name")}{field("Email", "email", "email", True, "you@example.com")}</div>
{select("Topic", "topic", [("general", "General question"), ("partnership", "Partnership / sponsorship"), ("advertising", "Advertising"), ("domain", "Website or domain inquiry"), ("press", "Press"), ("correction", "Report a correction"), ("privacy", "Privacy request"), ("other", "Other")])}
{field("Message", "message", "textarea", True, "How can we help?")}""", "Send message")
        return page_hero(R, "Contact Home.Direct", "Questions, corrections, partnerships or privacy requests — send a note and we'll get back to you.", [("Contact", None)]) + f"""
<section><div class="wrap layout" style="padding-top:10px"><div class="form-shell">{form}{success("contact-form", "Message sent", "Thanks for reaching out. We'll reply within two business days.", R)}</div>
<aside class="aside"><div class="card"><h3>Looking for something else?</h3><ul class="small"><li><a href="{R}get-quotes.html">Get quotes from pros</a></li><li><a href="{R}sell-direct.html">Sell your home</a></li><li><a href="{R}pros.html">Join as a pro</a></li><li><a href="{R}advertise.html">Advertise</a></li><li><a href="{PARTNER_URL}" target="_blank" rel="noopener">Partnership & domain inquiries</a></li></ul></div></aside></div></section>"""
    page("contact.html", "Contact Us", "Contact Home.Direct for questions, corrections, partnerships, advertising or privacy requests.", contact, crumbs=[("Contact", None)], priority=0.4, sticky=False)

    faqs = [("Is Home.Direct free?", "Yes, for homeowners. We're supported by ads, sponsorships, provider fees and optional donations."),
            ("How many companies will contact me after I request quotes?", "Up to three providers who serve your area."),
            ("Do you sell my information?", "We share the details you submit only with the providers matched to your request, and as described in our Privacy Policy. We don't sell lists."),
            ("Are your cost guides accurate for my city?", "They're national typical ranges with regional multipliers. Your local market, home condition and materials decide the final price — always compare written quotes."),
            ("Do you work in Canada?", "Yes. Forms accept Canadian postal codes, calculators include a Canada mortgage mode and estimators can show CAD."),
            ("How often is content updated?", "Rates, news and videos refresh automatically several times a day. Cost guides are reviewed on a rolling basis."),
            ("Can I advertise or sponsor?", "Yes — see Advertise or For Pros, or use the partnership link at the top of every page."),
            ("How do I delete my information?", "Send a privacy request through the contact form and we'll process it as required by applicable law.")]

    def faqp(R):
        return page_hero(R, "Frequently asked questions", "Quick answers about matching, pricing data, privacy and how Home.Direct works.", [("FAQ", None)]) + f'<section><div class="wrap narrow">{faq_html(faqs)}</div></section>'
    page("faq.html", "FAQ", "Answers to common questions about Home.Direct: quotes, matching, cost data, Canada, privacy and advertising.", faqp, crumbs=[("FAQ", None)], ld=[faq_ld(faqs)], priority=0.4)


# ---------------------------------------------------------------- LEGAL
def build_legal():
    def privacy(R):
        return page_hero(R, "Privacy policy", f"Effective {EFFECTIVE}. How Home.Direct collects, uses and protects information.", [("Privacy", None)]) + f"""
<section><div class="wrap narrow prose">
<h2>Who we are</h2><p>Home.Direct (“we”, “us”) operates this website. Contact us about privacy through our <a href="{R}contact.html">contact form</a> (choose “Privacy request”).</p>
<h2>Information we collect</h2><ul><li><b>Information you submit</b> in forms: name, email, phone, ZIP or postal code, property and project details, budget and timeline, and any links you provide.</li><li><b>Automatic information</b>: pages visited, referring page, campaign tags (UTM), browser and device data, and approximate location derived from IP address by our service providers.</li><li><b>Local storage</b>: your theme, cookie choice and maintenance-planner checkmarks are stored in your own browser and are not sent to us.</li></ul>
<h2>How we use information</h2><ul><li>To match your request with up to three providers who serve your area and to deliver your request to them.</li><li>To respond to messages, contest entries, applications, pledges and advertising inquiries.</li><li>To operate, secure and improve the site, and to show advertising.</li><li>To send the newsletter if you opt in (unsubscribe anytime).</li></ul>
<h2>How information is shared</h2><ul><li><b>Matched providers</b> receive the details of your specific request so they can contact you.</li><li><b>Service providers</b> that process data for us: FormSubmit (form delivery), GitHub Pages (hosting), Google (fonts and advertising), YouTube (video playback when you press play) and PayPal (donations).</li><li><b>Legal</b>: when required by law or to protect rights and safety.</li></ul><p>We do not sell lists of personal information.</p>
<h2 id="cookies">Cookies and advertising</h2><p>Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this and other websites. Google's use of advertising cookies enables it and its partners to serve ads based on your visits to our site and/or other sites on the Internet. You can opt out of personalized advertising at <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Google Ads Settings</a> or <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">aboutads.info</a>. You can also choose “Non-personalized” in our cookie banner (<a href="#" data-consent-reset>change your choice</a>). Learn more about <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">how Google uses data from partner sites</a>. Visitors in the EEA, UK and Switzerland are shown a consent message from a Google-certified consent platform where required.</p>
<h2>Your rights</h2><p>Depending on where you live — including under the GDPR, U.S. state privacy laws such as the CCPA/CPRA, Canada's PIPEDA and Quebec's Law 25 — you may have rights to access, correct, delete or port your information, to withdraw consent, and to opt out of certain sharing. Submit a request via the contact form; we'll verify and respond within the time required by law.</p>
<h2>Retention & security</h2><p>We keep submissions only as long as needed for the purposes above or as required by law. Forms are transmitted over HTTPS. No method of transmission is 100% secure.</p>
<h2>Children</h2><p>This site is not directed to children under 16, and we don't knowingly collect their information.</p>
<h2>Changes</h2><p>We may update this policy; the effective date above will change when we do.</p>
</div></section>"""
    page("privacy.html", "Privacy Policy", "How Home.Direct collects, uses and protects information, including cookies, Google AdSense advertising and your privacy rights.", privacy, crumbs=[("Privacy", None)], priority=0.3)

    def terms(R):
        return page_hero(R, "Terms of use", f"Effective {EFFECTIVE}. Please read these terms before using Home.Direct.", [("Terms", None)]) + f"""
<section><div class="wrap narrow prose">
<h2>1. Acceptance</h2><p>By using Home.Direct you agree to these Terms and our <a href="{R}privacy.html">Privacy Policy</a>.</p>
<h2>2. What we provide</h2><p>Home.Direct provides general information, estimates and calculators, and a service that forwards your requests to third-party providers. We are not a contractor, real estate brokerage or agent, lender, mortgage broker, insurer, appraiser or financial, legal or tax advisor, and nothing on this site is professional advice.</p>
<h2>3. Estimates and data</h2><p>Cost ranges, rates and calculator results are estimates for planning only and may not reflect your situation or current prices. Always obtain written quotes, Loan Estimates and professional advice before making decisions.</p>
<h2>4. Third-party providers</h2><p>Providers you are matched with are independent businesses. We don't guarantee their work, licensing, pricing, availability or conduct. You are responsible for verifying licenses and insurance, reviewing contracts and choosing whether to hire anyone.</p>
<h2>5. Communications consent</h2><p>When you submit a request and check the consent box, you authorize Home.Direct and up to three matched providers to contact you about that request by phone, text or email, including by automated means. Consent is not a condition of purchase. You may opt out at any time.</p>
<h2>6. Your submissions</h2><p>You agree to provide accurate information and not to submit unlawful, infringing or misleading content. Contest entries are also governed by the <a href="{R}contest-rules.html">Official Rules</a>.</p>
<h2>7. Donations</h2><p>Donations are voluntary, processed by PayPal, non-refundable except where required by law, and not tax-deductible.</p>
<h2>8. Intellectual property</h2><p>Site text, design, calculators and compilations are © Home.Direct. Third-party trademarks, videos and headlines belong to their owners. See our <a href="{R}disclosures.html">disclosures</a>.</p>
<h2>9. Disclaimer and limitation of liability</h2><p>The site is provided “as is” without warranties of any kind. To the fullest extent permitted by law, Home.Direct is not liable for indirect, incidental or consequential damages, or for any loss arising from your use of the site or dealings with third parties.</p>
<h2>10. Governing law</h2><p>These Terms are governed by the laws of the Province of Quebec and the federal laws of Canada applicable therein, without regard to conflict-of-law rules, except where consumer-protection law of your place of residence requires otherwise.</p>
<h2>11. Changes</h2><p>We may update these Terms; continued use means you accept the updated Terms.</p>
</div></section>"""
    page("terms.html", "Terms of Use", "Terms governing use of Home.Direct, its estimates, calculators, matching service, contests and donations.", terms, crumbs=[("Terms", None)], priority=0.3)

    def disc(R):
        return page_hero(R, "Disclosures, trademarks & copyright", f"Effective {EFFECTIVE}. Who we are — and who we are not.", [("Disclosures", None)]) + f"""
<section><div class="wrap narrow prose">
<h2 id="trademark">Trademark disclosure</h2><p><b>“Home.Direct”</b> is the name of this website, always written with the dot as part of the name, and refers only to this independent information and matching service at the Home.Direct domain.</p>
<p>Home.Direct is <b>not affiliated with, endorsed by, sponsored by or connected to</b> any company, product or service that uses the name or mark “HomeDirect”, “Home Direct”, “Homes Direct” or similar wording — including, without limitation, HomeDirect, Inc. and its HOMEDIRECT USA delivery and logistics marks, the owner of the HOMEDIRECT MORTGAGE mark, Homes Direct, Inc. (HD HOMES DIRECT), or any bank, lender, mortgage company, furniture or home-delivery business, retailer, builder or real estate company operating under a similar name. All such names and marks are the property of their respective owners. We do not offer delivery, logistics, banking or mortgage-lending services, and nothing on this site should be understood as coming from those companies.</p>
<p>If you believe content on this site infringes your trademark, please contact us through the <a href="{R}contact.html">contact form</a> (topic: “Other”) and we will review it promptly.</p>
<h2 id="copyright">Copyright notice</h2><p>© {TODAY.year} Home.Direct. All rights reserved. Original text, cost compilations, calculators, page designs, graphics and code on this site are protected by copyright. You may link to our pages and quote short excerpts with attribution; other reproduction requires written permission.</p>
<p><b>Third-party content:</b> Embedded YouTube videos remain the property of their creators and are played through YouTube's player under its terms; we are not affiliated with those channels. News headlines link to the original publishers and remain their property. Mortgage rate data is from Freddie Mac's Primary Mortgage Market Survey® via FRED®, Federal Reserve Bank of St. Louis. Google, AdSense, YouTube, PayPal, Freddie Mac and other names are trademarks of their respective owners.</p>
<p><b>Copyright complaints:</b> send a notice through our contact form identifying the work, the material on our site and your contact details, with a statement of good-faith belief and accuracy. We respond to valid notices and remove infringing material.</p>
<h2 id="advertising">Advertising & compensation disclosure</h2><p>This site displays ads from Google AdSense and may display clearly labeled sponsored placements. Some service providers pay Home.Direct when they receive homeowner requests or are featured. This compensation may influence which providers participate in matching but never changes our cost data, calculator math or editorial content.</p>
<h2 id="professional">Not professional advice</h2><p>Home.Direct is not a contractor, real estate brokerage, lender, mortgage broker, insurer, appraiser or financial, legal or tax advisor. Information is general and for educational purposes. Verify licenses and consult qualified professionals.</p>
<h2 id="estimates">Estimates</h2><p>Cost figures are typical ranges compiled from published contractor cost guides, supplier pricing and industry surveys, and may differ from your local market. Tax-credit information reflects rules as we understand them as of the effective date (for example, the U.S. Section 25C and 25D homeowner energy credits ended for property placed in service after December 31, 2025) — confirm with a tax professional.</p>
</div></section>"""
    page("disclosures.html", "Disclosures, Trademark & Copyright Notice", "Home.Direct trademark disclosure (not affiliated with any 'HomeDirect' company), copyright notice, advertising and compensation disclosures.", disc, crumbs=[("Disclosures", None)], priority=0.3)

    def access(R):
        return page_hero(R, "Accessibility statement", "We want Home.Direct to work for everyone.", [("Accessibility", None)]) + f"""
<section><div class="wrap narrow prose"><p>We aim to conform to the Web Content Accessibility Guidelines (WCAG) 2.1 Level AA. The site uses semantic HTML, labeled form fields, keyboard-accessible menus, visible focus indicators, sufficient color contrast, reduced-motion support and a dark mode.</p>
<p>Embedded videos and third-party ads may not fully meet these standards. If you run into a barrier, tell us through the <a href="{R}contact.html">contact form</a> with the page address and the issue, and we'll work to fix it and provide the information in another way.</p></div></section>"""
    page("accessibility.html", "Accessibility Statement", "Home.Direct's commitment to accessibility and how to report a barrier.", access, crumbs=[("Accessibility", None)], priority=0.2)


# ---------------------------------------------------------------- UTILITY
def build_utility():
    def thanks(R):
        return f"""<section class="hero"><div class="wrap narrow center"><div class="form-success" style="padding-top:0"><div class="ok-ring">{icon('check')}</div><h1>Thank you!</h1>
<p class="lead">Your submission was received. If you requested quotes or offers, matched providers typically reach out within one business day.</p>
<div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap"><a class="btn" href="{R}cost-guides/index.html">Browse cost guides</a><a class="btn ghost" href="{R}tools/index.html">Use the calculators</a></div></div></div></section>"""
    page("thank-you.html", "Thank you", "Your submission was received.", thanks, ads=False, noindex=True, sticky=False)

    def nf(R):
        return f"""<section class="hero"><div class="wrap narrow center"><span class="eyebrow">404</span><h1>That page moved out.</h1><p class="lead">Try searching, or start from one of these:</p>
<div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap"><a class="btn" href="index.html">Home</a><a class="btn ghost" href="get-quotes.html">Get quotes</a><a class="btn ghost" href="cost-guides/index.html">Cost guides</a><button class="btn ghost" type="button" data-search-open>Search the site</button></div></div></section>"""
    page("404.html", "Page not found", "This page doesn't exist.", nf, ads=False, noindex=True, sticky=False, base_fix=True)


def build_all():
    build_support()
    build_contests()
    build_careers()
    build_pros()
    build_about_contact_faq()
    build_legal()
    build_utility()
