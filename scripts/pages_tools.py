# -*- coding: utf-8 -*-
"""Calculator pages for Home.Direct."""
import json
from hd_core import ROOTDIR, E, money, icon, page, page_hero, faq_html, faq_ld
from content_guides import GUIDES
from site_data import ROI_PROJECTS


def _rates():
    try:
        return json.loads((ROOTDIR / "data" / "rates.json").read_text(encoding="utf-8"))
    except Exception:
        return {}


R30 = round(_rates().get("r30", 7.0), 2)
R15 = round(_rates().get("r15", 6.4), 2)


def num(label, name, value, step="any", pre="", suf="", hint=""):
    h = f'<small class="muted">{hint}</small>' if hint else ""
    lab = f"{label}{(' (' + pre + ')') if pre else ''}{(' (' + suf + ')') if suf else ''}"
    return f'<div class="field"><label for="c-{name}">{lab}</label><input id="c-{name}" type="number" name="{name}" value="{value}" step="{step}" inputmode="decimal" min="0">{h}</div>'


def rng(label, name, value, lo, hi, step, suf="", pre=""):
    return (f'<div class="field"><label for="c-{name}">{label}</label><div class="range"><input id="c-{name}" type="range" name="{name}" min="{lo}" max="{hi}" step="{step}" value="{value}" data-suffix="{suf}" data-prefix="{pre}">'
            f'<output for="c-{name}"></output></div></div>')


def seg(label, name, items, checked):
    s = "".join(f'<label><input type="radio" name="{name}" value="{v}"{" checked" if v == checked else ""}><span>{E(t)}</span></label>' for v, t in items)
    return f'<div class="field"><span class="label">{label}</span><div class="seg">{s}</div></div>'


def sel(label, name, items, value):
    o = "".join(f'<option value="{v}"{" selected" if str(v) == str(value) else ""}>{E(t)}</option>' for v, t in items)
    return f'<div class="field"><label for="c-{name}">{label}</label><select id="c-{name}" name="{name}">{o}</select></div>'


def chk(label, name, on=False):
    return f'<label class="check" style="color:var(--text)"><input type="checkbox" name="{name}"{" checked" if on else ""}> <span>{label}</span></label>'


def result(title, big, sub, rows, cta=None, bars=True, R=""):
    dl = "".join(f'<dt>{E(a)}</dt><dd data-out="{b}">—</dd>' for a, b in rows)
    c = f'<a class="btn light" href="{R}{cta[1]}">{E(cta[0])}</a>' if cta else ""
    b = '<div class="bar-chart" data-bars></div>' if bars else ""
    return f'<div class="result"><h3>{E(title)}</h3><div class="big" data-out="{big}">—</div><div class="sub">{sub}</div><dl>{dl}</dl>{b}{c}</div>'


TERMS = [(30, "30 years"), (25, "25 years"), (20, "20 years"), (15, "15 years"), (10, "10 years")]

TOOLS = [
dict(slug="mortgage-calculator", name="Mortgage calculator", short="Monthly payment with taxes, insurance, PMI & amortization", icon="calc", kw="mortgage payment piti amortization canada",
  title="Mortgage Calculator with Taxes, PMI & Amortization (US & Canada)",
  desc="Calculate your monthly mortgage payment including property tax, insurance, PMI and HOA. Amortization schedule and Canadian semi-annual compounding mode.",
  intro="Estimate your full monthly housing payment — principal, interest, property tax, homeowners insurance, PMI and HOA dues — and see how your balance falls over the life of the loan. Switch to Canada mode for semi-annual compounding.",
  calc=lambda R: f"""<div class="calc" data-tool="mortgage"><div>
{num("Home price", "price", 400000, 1000, "$")}{rng("Down payment", "down_pct", 20, 0, 50, 1, "%")}
<div class="row">{num("Interest rate", "rate", R30, 0.01, "", "%", "Prefilled with this week's 30-yr average")}{sel("Loan term", "term", TERMS, 30)}</div>
{seg("Compounding", "country", [("us", "U.S. (monthly)"), ("ca", "Canada (semi-annual)")], "us")}
<div class="row">{num("Property tax / year", "tax", 4400, 50, "$")}{num("Home insurance / year", "insurance", 1800, 50, "$")}</div>
<div class="row">{num("HOA / month", "hoa", 0, 10, "$")}{num("PMI rate if under 20% down", "pmi_rate", 0.5, 0.05, "", "% / yr")}</div></div>
{result("Estimated monthly payment", "total", 'Loan <b data-out="loan"></b> · Down <b data-out="down"></b>', [("Principal & interest", "pi"), ("Property tax", "tax"), ("Insurance", "ins"), ("PMI", "pmi"), ("HOA", "hoa"), ("Total interest", "interest"), ("Payoff date", "payoff")], ("Compare lender offers →", "finance.html#lender-form"), R=R)}
<div style="grid-column:1/-1"><h3>Loan balance over time</h3><canvas class="chart" aria-label="Loan balance chart"></canvas>
<details style="margin-top:14px"><summary><b>Year-by-year amortization schedule</b></summary><div class="table-wrap amort" style="margin-top:10px"><table><thead><tr><th>Year</th><th class="num">Principal</th><th class="num">Interest</th><th class="num">Balance</th></tr></thead><tbody data-amort></tbody></table></div></details></div></div>""",
  how=["Principal and interest use the standard amortization formula: payment = L × r ÷ (1 − (1 + r)<sup>−n</sup>), where L is the loan amount, r the monthly rate and n the number of payments.",
       "Canada mode converts the quoted annual rate to an effective monthly rate using semi-annual compounding, as required for Canadian fixed-rate mortgages: r = (1 + rate/2)<sup>1/6</sup> − 1.",
       "PMI is added only when your down payment is under 20%. Conventional PMI commonly runs 0.3%–1.5% of the loan per year depending on credit and down payment; it can usually be removed once you reach 20% equity. Canadian insured mortgages use a one-time CMHC-style premium instead — add it to the loan amount if it applies to you."],
  tips=["Each 1-point drop in rate on a $320,000 loan saves roughly $200–$220 a month.", "Ask lenders for a Loan Estimate to compare APR, points and fees on the same day.", "Shorter terms (15–20 years) cut total interest dramatically for a higher monthly payment."],
  faqs=[("What is PITI?", "Principal, interest, taxes and insurance — the four core parts of a mortgage payment. Lenders use PITI to qualify you."), ("How much should my mortgage payment be?", "A common guideline is to keep housing costs under 28%–31% of gross monthly income and total debts under 36%–43%."), ("Why is my first payment mostly interest?", "Interest is charged on the outstanding balance, which is highest at the start. Each payment shifts more toward principal over time.")],
  related=["affordability-calculator", "refinance-calculator", "closing-cost-calculator"]),

dict(slug="affordability-calculator", name="How much house can I afford?", short="Price range from income, debts and down payment", icon="home", kw="affordability afford house income dti",
  title="How Much House Can I Afford? Affordability Calculator",
  desc="Find your home price range from income, monthly debts, down payment and today's rates using 28/36, 31/43 and stretch debt-to-income rules.",
  intro="Lenders look at two ratios: housing costs as a share of gross income (front-end) and all debt payments as a share of income (back-end). This calculator finds the highest price that fits both, including taxes, insurance and PMI.",
  calc=lambda R: f"""<div class="calc" data-tool="affordability"><div>
<div class="row">{num("Gross annual income", "income", 120000, 1000, "$")}{num("Monthly debt payments", "debts", 500, 25, "$", "", "Car, student loans, cards, etc.")}</div>
<div class="row">{num("Down payment savings", "down", 60000, 1000, "$")}{num("Interest rate", "rate", R30, 0.01, "", "%")}</div>
<div class="row">{sel("Loan term", "term", TERMS, 30)}{num("Property tax rate", "tax_rate", 1.1, 0.05, "", "% / yr")}</div>
<div class="row">{num("Home insurance / year", "insurance", 1800, 50, "$")}{num("HOA / month", "hoa", 0, 10, "$")}</div>
{seg("Lending profile", "profile", [("conservative", "Conservative 28/36"), ("standard", "Standard 31/43"), ("stretch", "Stretch 36/45")], "standard")}</div>
{result("You can afford about", "price", 'Monthly payment <b data-out="payment"></b>', [("Loan amount", "loan"), ("Max housing budget", "max_housing"), ("Front-end limit", "front"), ("Back-end limit", "back"), ("Your total DTI", "dti")], ("Get pre-qualified →", "finance.html?goal=buy#lender-form"), R=R)}</div>""",
  how=["Front-end ratio: maximum housing payment = gross monthly income × front-end limit.", "Back-end ratio: maximum housing payment = gross monthly income × back-end limit − existing monthly debts. The lower of the two wins.",
       "The calculator then searches for the highest price whose full payment (principal, interest, taxes, insurance, HOA and PMI if under 20% down) fits that budget."],
  tips=["Paying off a $400/month car loan can raise your budget by roughly $50,000–$60,000 at today's rates.", "Keep 3–6 months of expenses in reserve after closing.", "Pre-approval beats pre-qualification when you make offers."],
  faqs=[("What is the 28/36 rule?", "Housing costs at or under 28% of gross income, and total debt payments at or under 36%."), ("Do lenders allow higher ratios?", "Yes. Many conventional and FHA programs approve back-end ratios up to 43%–50% with strong credit or reserves."), ("Should I borrow the maximum?", "Not necessarily. Budget for maintenance (1%–2% of home value per year) and savings goals.")],
  related=["mortgage-calculator", "rent-vs-buy-calculator", "closing-cost-calculator"]),

dict(slug="refinance-calculator", name="Refinance break-even calculator", short="Monthly savings and months to recoup closing costs", icon="chart", kw="refinance refi break even savings",
  title="Refinance Calculator: Break-Even & Savings",
  desc="See your new payment, monthly savings and how many months it takes to recoup refinance closing costs — including cash-out and rolled-in costs.",
  intro="A refinance only pays if you stay long enough to recoup the closing costs. Enter your current loan and a new offer to see monthly savings, the break-even point and the lifetime interest difference.",
  calc=lambda R: f"""<div class="calc" data-tool="refinance"><div>
<div class="row">{num("Current balance", "balance", 300000, 1000, "$")}{num("Current rate", "current_rate", 7.75, 0.01, "", "%")}</div>
<div class="row">{num("Years left on loan", "years_left", 27, 1)}{num("New rate", "new_rate", round(R30 - 0.6, 2), 0.01, "", "%")}</div>
<div class="row">{sel("New term", "new_term", TERMS, 30)}{num("Closing costs", "closing", 6000, 100, "$")}</div>
{num("Cash out", "cash_out", 0, 1000, "$", "", "Optional")}{chk("Roll closing costs into the new loan", "roll_costs")}</div>
{result("Monthly savings", "savings", '<span data-out="verdict"></span>', [("Current payment", "current_payment"), ("New payment", "new_payment"), ("New loan amount", "new_loan"), ("Break-even", "breakeven"), ("Lifetime interest saved", "interest_diff")], ("Get refinance offers →", "finance.html?goal=refinance#lender-form"), R=R)}</div>""",
  how=["Both payments use standard amortization. Break-even = closing costs ÷ monthly savings.", "Lifetime interest saved compares remaining interest on the current loan with total interest on the new loan, minus upfront costs.",
       "Resetting to a new 30-year term can lower the payment while increasing total interest — compare a 20- or 15-year term too."],
  tips=["Ask for a no-closing-cost option and compare it against paying points.", "If you plan to move within 3 years, a refinance rarely pays.", "Keep your remaining term similar to avoid stretching debt."],
  faqs=[("How much should rates drop before refinancing?", "Many borrowers look for 0.75–1 point, but the break-even math matters more than a rule of thumb."), ("Does refinancing hurt my credit?", "A hard inquiry causes a small, temporary dip. Rate-shopping within a short window counts as one inquiry for most scoring models."), ("What is a cash-out refinance?", "Replacing your mortgage with a larger one and taking the difference in cash — useful for big renovations, but it raises your balance.")],
  related=["mortgage-calculator", "home-equity-calculator", "closing-cost-calculator"]),

dict(slug="rent-vs-buy-calculator", name="Rent vs. buy calculator", short="Total cost of renting vs. owning, year by year", icon="key", kw="rent vs buy renting buying",
  title="Rent vs. Buy Calculator: Which Costs Less?",
  desc="Compare the true cost of renting versus buying a home over time, including equity, appreciation, maintenance, selling costs and investment returns.",
  intro="Buying builds equity, but it also brings closing costs, maintenance, property tax and selling costs. Renting keeps your down payment invested. This calculator compares both paths year by year and finds the break-even point.",
  calc=lambda R: f"""<div class="calc" data-tool="rentvsbuy"><div>
<div class="row">{num("Monthly rent", "rent", 2400, 25, "$")}{num("Rent increase / yr", "rent_increase", 3.5, 0.1, "", "%")}</div>
<div class="row">{num("Home price", "price", 450000, 1000, "$")}{num("Down payment", "down_pct", 10, 1, "", "%")}</div>
<div class="row">{num("Mortgage rate", "rate", R30, 0.01, "", "%")}{rng("Years you'll stay", "years", 7, 1, 30, 1, " yrs")}</div>
<div class="row">{num("Home appreciation / yr", "appreciation", 3.5, 0.1, "", "%")}{num("Investment return / yr", "invest_return", 6, 0.1, "", "%")}</div>
<div class="row3">{num("Property tax", "tax_rate", 1.1, 0.05, "", "%")}{num("Maintenance", "maintenance", 1, 0.1, "", "%")}{num("Insurance / yr", "insurance", 1800, 50, "$")}</div>
<div class="row">{num("Selling costs", "sell_cost", 6, 0.5, "", "%")}{num("Buying closing costs", "closing", 3, 0.5, "", "%")}</div></div>
{result("Verdict", "winner", 'Break-even: <b data-out="breakeven"></b>', [("Total rent paid", "rent_total"), ("Renting net cost (after investment growth)", "rent_net"), ("Total cost to own", "buy_total"), ("Equity at sale (after costs)", "equity"), ("Buying net cost", "buy_net")], ("Check what you can afford →", "tools/affordability-calculator.html"), bars=False, R=R)}
<div style="grid-column:1/-1"><h3>Net cost over time <small class="muted">(coral = renting, teal = buying)</small></h3><canvas class="chart" aria-label="Rent vs buy chart"></canvas></div></div>""",
  how=["Buying net cost = down payment + closing costs + every month's mortgage, tax, insurance, maintenance and PMI − equity you'd keep after selling costs.",
       "Renting net cost = all rent paid − growth earned by investing the down payment, closing costs and any monthly difference when owning costs more than renting.", "The break-even year is the first year buying's net cost drops below renting's."],
  tips=["The shorter your stay, the more renting tends to win because closing and selling costs dominate.", "Be conservative with appreciation; national averages hide big local swings.", "Include realistic maintenance — 1%–2% of value per year."],
  faqs=[("Is renting throwing money away?", "No. Rent buys housing and flexibility; owning has its own unrecoverable costs (interest, taxes, maintenance, transaction fees)."), ("What's a good break-even horizon?", "Commonly 4–7 years in balanced markets; longer in expensive metros."), ("Does this include tax benefits?", "No. Deductions only help if you itemize, which most households don't after the higher standard deduction.")],
  related=["affordability-calculator", "mortgage-calculator", "closing-cost-calculator"]),

dict(slug="home-equity-calculator", name="Home equity & HELOC calculator", short="How much you can borrow and what it costs", icon="key", kw="heloc home equity loan borrow",
  title="Home Equity & HELOC Calculator",
  desc="Calculate your home equity, how much you can borrow with a HELOC or home equity loan at 80–90% CLTV, and the interest-only and amortized payments.",
  intro="Most lenders let you borrow up to 80%–90% of your home's value across all loans (combined loan-to-value, or CLTV). See your available line and what a draw would cost each month.",
  calc=lambda R: f"""<div class="calc" data-tool="equity"><div>
<div class="row">{num("Home value", "value", 500000, 1000, "$")}{num("Mortgage balance", "balance", 250000, 1000, "$")}</div>
<div class="row">{sel("Max combined LTV", "cltv", [(80, "80%"), (85, "85%"), (90, "90%")], 85)}{num("HELOC / loan rate", "rate", 8.5, 0.05, "", "%")}</div>
<div class="row">{num("Amount you want", "draw", 50000, 1000, "$")}{num("Repayment term", "term", 10, 1, "", "years")}</div></div>
{result("You may be able to borrow", "max_line", 'Equity <b data-out="equity"></b> (<span data-out="equity_pct"></span>)', [("Interest-only payment", "io_payment"), ("Amortized payment", "amort_payment"), ("CLTV after borrowing", "cltv_after")], ("Compare equity offers →", "finance.html?goal=heloc#lender-form"), R=R)}</div>""",
  how=["Available line = home value × max CLTV − mortgage balance.", "Interest-only payment = amount drawn × rate ÷ 12 (typical during a HELOC draw period).", "Amortized payment spreads principal and interest over the repayment term."],
  tips=["HELOC rates are variable — stress-test a payment 2 points higher.", "A HELOC keeps a low first-mortgage rate intact; a cash-out refi replaces it.", "Use equity for value-adding projects, not consumption."],
  faqs=[("HELOC vs. home equity loan?", "A HELOC is a revolving line with a variable rate; a home equity loan is a lump sum with a fixed rate."), ("What credit score do I need?", "Many lenders look for 680+, with the best rates at 740+."), ("Is HELOC interest tax-deductible?", "In the U.S., potentially, when the money is used to buy, build or substantially improve the home securing the loan. Ask a tax professional.")],
  related=["refinance-calculator", "renovation-roi-calculator", "project-cost-estimator"]),

dict(slug="net-proceeds-calculator", name="Home sale net proceeds calculator", short="What you'll actually walk away with", icon="dollar", kw="net proceeds sell house seller",
  title="Home Sale Net Proceeds Calculator",
  desc="Estimate how much you'll walk away with after selling your home: commissions, closing costs, transfer tax, mortgage payoff, repairs, staging and moving.",
  intro="Sale price isn't what you pocket. Commissions, closing costs, transfer taxes, payoff, repairs and moving can easily eat 8%–12% of the price. Enter your numbers to see your real net.",
  calc=lambda R: f"""<div class="calc" data-tool="netproceeds"><div>
<div class="row">{num("Expected sale price", "price", 450000, 1000, "$")}{num("Mortgage payoff", "payoff", 220000, 1000, "$")}</div>
<div class="row">{num("Listing-agent fee", "listing_pct", 2.75, 0.05, "", "%", "Set 0 for FSBO")}{num("Buyer-agent fee you offer", "buyer_pct", 2.5, 0.05, "", "%")}</div>
<div class="row">{num("Seller closing costs", "closing_pct", 1.5, 0.1, "", "%")}{num("Transfer tax", "transfer_pct", 0.4, 0.05, "", "%")}</div>
<div class="row3">{num("Repairs / credits", "repairs", 5000, 100, "$")}{num("Prep & staging", "prep", 2500, 100, "$")}{num("Moving", "moving", 2500, 100, "$")}</div></div>
{result("Estimated net to you", "net", 'Total selling costs <b data-out="costs"></b> (<span data-out="costs_pct"></span> of price)', [("Commissions", "commission"), ("Closing costs", "closing"), ("Transfer tax", "transfer"), ("Mortgage payoff", "payoff")], ("Compare ways to sell →", "sell-direct.html#offer-form"), R=R)}</div>""",
  how=["Net proceeds = sale price − mortgage payoff − commissions − closing costs − transfer tax − repairs/credits − prep − moving.",
       "Commissions are now negotiable in the U.S.; enter 0% for listing if you sell by owner, and choose whether to offer a buyer-agent fee.", "Capital gains taxes aren't included — U.S. homeowners can usually exclude up to $250,000 ($500,000 married) of gain on a primary residence."],
  tips=["A 1% lower listing fee on a $450,000 sale keeps $4,500 in your pocket.", "Get a pre-listing inspection to avoid surprise credits.", "Compare at least one cash offer against your net — speed has value."],
  faqs=[("What are typical seller closing costs?", "Often 1%–3% of the price, excluding commissions — title, escrow, attorney, transfer taxes and prorated property taxes."), ("Do I have to pay the buyer's agent?", "In the U.S. it's negotiable; many sellers offer a concession to attract more buyers."), ("When do I get my money?", "At closing, typically wired the same day or next business day.")],
  related=["commission-savings-calculator", "closing-cost-calculator", "renovation-roi-calculator"]),

dict(slug="commission-savings-calculator", name="Commission savings calculator", short="Full-service vs. discount vs. flat-fee vs. FSBO vs. cash", icon="sign", kw="commission realtor fee fsbo flat fee mls discount broker",
  title="Real Estate Commission Savings Calculator",
  desc="Compare your net with a full-service agent, discount broker, flat-fee MLS, FSBO and a cash offer. See exactly how much each option saves.",
  intro="How you sell can be worth more than any upgrade. Compare five ways to sell on the same price to see the dollar difference — then decide what the help is worth to you.",
  calc=lambda R: f"""<div class="calc" data-tool="commission"><div>
{num("Expected sale price", "price", 450000, 1000, "$")}{num("Buyer-agent fee you'd offer", "buyer_pct", 2.5, 0.05, "", "%")}
{chk("Offer a buyer-agent fee in agent, discount, flat-fee and FSBO scenarios", "offer_buyer", True)}
{num("Cash-offer discount below market", "cash_discount", 12, 0.5, "", "%", "Cash buyers typically offer 5–20% below market")}
<div class="table-wrap" style="margin-top:8px"><table><thead><tr><th>Option</th><th class="num">Price after fees</th><th class="num">vs. full-service</th></tr></thead><tbody data-table></tbody></table></div></div>
{result("Highest net option", "best", 'Flat-fee MLS saves <b data-out="save"></b> vs. a full-service agent', [], ("Get matched for my option →", "sell-direct.html#offer-form"), R=R)}</div>""",
  how=["Each scenario subtracts its listing fee (2.75%, 1.5%, $499 flat or about $150 for FSBO marketing) and, if selected, the buyer-agent fee.", "The cash-offer scenario applies a discount to the price but no commissions or repairs.", "Closing costs and taxes apply to all scenarios equally, so they're excluded from the comparison."],
  tips=["FSBO saves the most only if you price correctly and sell for close to market.", "Discount brokers often deliver most of the service for half the fee.", "Treat a cash offer as a floor and negotiate."],
  faqs=[("What is a flat-fee MLS listing?", "A licensed broker lists your home on the MLS for a fixed fee (typically $300–$600) while you handle showings and negotiation."), ("Do FSBO homes sell for less?", "Some studies show lower average prices, often because FSBO homes are smaller or priced without data. Good pricing narrows the gap."), ("Are commissions negotiable?", "Always. In the U.S. there is no standard rate.")],
  related=["net-proceeds-calculator", "closing-cost-calculator", "renovation-roi-calculator"]),

dict(slug="closing-cost-calculator", name="Closing cost calculator", short="Itemized buyer or seller closing costs", icon="dollar", kw="closing costs buyer seller fees",
  title="Closing Cost Calculator for Buyers & Sellers",
  desc="Estimate itemized closing costs for buying or selling a home: lender fees, title insurance, escrow, prepaid items, transfer taxes and commissions.",
  intro="Buyers usually pay 2%–5% of the price in closing costs plus the down payment; sellers pay commissions plus 1%–3% in fees and taxes. Choose your side for an itemized estimate.",
  calc=lambda R: f"""<div class="calc" data-tool="closing"><div>
{seg("I'm the", "role", [("buyer", "Buyer"), ("seller", "Seller")], "buyer")}
<div class="row">{num("Purchase / sale price", "price", 400000, 1000, "$")}{num("Down payment (buyers)", "down_pct", 20, 1, "", "%")}</div>
<div class="row">{num("Interest rate (buyers)", "rate", R30, 0.01, "", "%")}{num("Transfer tax (sellers)", "transfer_pct", 0.4, 0.05, "", "%")}</div>
<div class="table-wrap" style="margin-top:8px"><table><thead><tr><th>Item</th><th class="num">Estimate</th></tr></thead><tbody data-table></tbody></table></div></div>
{result("Estimated closing costs", "total", '<span data-out="total_pct"></span> of price', [("Cash to close (buyers)", "cash_needed")], ("Shop lenders →", "finance.html#lender-form"), bars=False, R=R)}</div>""",
  how=["Line items use common national ranges: origination about 0.75% of the loan, title insurance about 0.35%–0.4% of price, settlement $900, recording $275, prepaid interest for 15 days, one year of insurance and three months of tax escrow.", "Seller items include listing and buyer-agent fees, owner's title policy (paid by sellers in many areas), transfer tax, attorney/doc prep and prorated taxes.", "Who pays what varies by state, province and contract — use this as a planning range."],
  tips=["Ask the seller for closing-cost credits in a slower market.", "Compare title and settlement providers — you can often shop for them.", "In Canada, budget for provincial land transfer tax (and municipal tax in Toronto) — first-time buyer rebates may apply."],
  faqs=[("Can closing costs be rolled into the loan?", "Sometimes, via lender credits (a higher rate) or certain refinance programs."), ("What are prepaid items?", "Upfront payments for interest, insurance and property-tax escrow — not lender fees, but cash you need at closing."), ("Who pays the transfer tax?", "It depends on the state or province and local custom; it's negotiable in many areas.")],
  related=["mortgage-calculator", "net-proceeds-calculator", "affordability-calculator"]),

dict(slug="renovation-roi-calculator", name="Renovation ROI calculator", short="Which projects pay back at resale", icon="star", kw="renovation roi resale value cost vs value",
  title="Renovation ROI Calculator: Which Upgrades Pay Back?",
  desc="Estimate how much of a renovation's cost you'll recover at resale, plus energy savings, for 15 common projects from garage doors to kitchen remodels.",
  intro="Small exterior projects often recover more of their cost than big interior remodels. Pick a project, adjust your cost, and see the resale value added, energy savings and true net cost.",
  calc=lambda R: f"""<div class="calc" data-tool="roi"><div>
<div class="field"><label for="c-project">Project</label><select id="c-project" name="project">{"".join(f'<option value="{i}" data-recoup="{r}" data-cost="{c}">{E(n)}</option>' for i, (n, c, r) in enumerate(ROI_PROJECTS))}</select></div>
<div class="row">{num("Your project cost", "cost", ROI_PROJECTS[0][1], 100, "$")}{num("Resale recovery", "recoup", ROI_PROJECTS[0][2], 1, "", "%", "Prefilled with a typical national value")}</div>
<div class="row">{num("Energy savings / year", "energy", 0, 25, "$")}{num("Years until you sell", "years", 5, 1)}</div></div>
{result("Return on investment", "roi", '<span data-out="verdict"></span>', [("Resale value added", "added"), ("Energy savings total", "energy_total"), ("Net cost after resale", "net")], ("Get project quotes →", "get-quotes.html"), R=R)}</div>""",
  how=["Resale value added = project cost × recovery percentage. Recovery values are typical national midpoints drawn from published remodeling cost-versus-value surveys and appraisal practice; local markets vary widely.", "ROI = (value added + energy savings − cost) ÷ cost.", "Projects buyers see first — curb appeal and entry points — tend to recover the most."],
  tips=["Before listing, prioritize paint, flooring refinishing, garage and entry doors.", "Don't over-improve beyond the neighborhood's price ceiling.", "Keep receipts — improvements raise your cost basis for capital gains."],
  faqs=[("Which renovations add the most value?", "Garage door and entry-door replacements, minor kitchen updates, siding and refinishing hardwood consistently recover the highest share of cost."), ("Do pools add value?", "Rarely their full cost; in hot climates they can help, elsewhere they may narrow your buyer pool."), ("Should I renovate before selling?", "Fix defects and refresh cosmetics; skip big remodels unless comparable homes require them.")],
  related=["project-cost-estimator", "net-proceeds-calculator", "home-equity-calculator"]),

dict(slug="project-cost-estimator", name="Project cost estimator", short="24 projects, adjusted for size, quality and location", icon="wrench", kw="project cost estimator estimate renovation",
  title="Home Project Cost Estimator (24 Projects)",
  desc="Estimate the cost of 24 home projects — roofing, HVAC, windows, kitchens, baths, foundations, solar and more — adjusted for size, quality, location and complexity.",
  intro="Pick a project and adjust size, quality, location and complexity. The range uses typical 2026 installed costs per unit plus fixed costs like permits and disposal.",
  calc=lambda R: f"""<div class="calc" data-tool="estimator"><div>
<div class="field"><label for="c-proj">Project</label><select id="c-proj" name="project">{"".join(f'<option value="{g["slug"]}">{E(g["name"])}</option>' for g in sorted(GUIDES, key=lambda x: x["name"]))}</select></div>
<div class="field"><label for="est-size">Size — <span data-out="unit_label"></span></label><div class="range"><input id="est-size" type="range" name="size" min="1" max="100" step="1" value="10"><output data-out="size_val"></output></div></div>
{seg("Quality level", "quality", [("economy", "Economy"), ("standard", "Standard"), ("premium", "Premium")], "standard")}
{seg("Location", "region", [("low", "Lower-cost area"), ("avg", "Average"), ("high", "High-cost metro"), ("ca", "Canada (CAD)")], "avg")}
{seg("Complexity", "complexity", [("simple", "Simple"), ("typical", "Typical"), ("complex", "Complex")], "typical")}</div>
<div class="result"><h3>Estimated range (<span data-out="currency">USD</span>)</h3><div class="big"><span data-out="low">—</span> – <span data-out="high">—</span></div><div class="sub">Midpoint <b data-out="mid"></b> · <span data-out="per_unit"></span></div>
<dl><dt>National typical range</dt><dd data-out="national">—</dd></dl>
<a class="btn light" data-quote-link data-base="{R}get-quotes.html" href="{R}get-quotes.html">Get real quotes →</a><a class="btn ghost" style="color:#fff;border-color:#4a5d74" data-guide-link data-base="{R}cost-guides/" href="{R}cost-guides/index.html">Read the full cost guide</a></div></div>
<script type="application/json" id="guides-data">{json.dumps(sorted([{k: g[k] for k in ("slug", "name", "service", "low", "high", "avg", "unit_low", "unit_high", "fixed_low", "fixed_high", "min_job", "size_min", "size_max", "size_step", "default_size", "size_label", "size_unit")} for g in GUIDES], key=lambda x: x["name"]))}</script>""",
  how=["Estimate = (size × unit cost + fixed costs) × quality × location × complexity.", "Quality multipliers: economy 0.82, standard 1.0, premium 1.38. Location: lower-cost 0.86, average 1.0, high-cost metro 1.22, Canada 1.30 (in CAD).", "Fixed costs cover permits, disposal, setup and similar one-time items; a minimum job charge applies to small projects."],
  tips=["Get three written quotes and compare line items, not totals.", "Off-season scheduling can save 5%–15%.", "Hold a 10%–15% contingency for surprises once walls or roofs are opened."],
  faqs=[("How accurate is this estimator?", "It gives a planning range. Your home's condition, access, materials and local labor rates decide the final price."), ("Why is Canada higher?", "The Canada setting reflects higher material and labor costs plus the currency difference, so results are in CAD."), ("Does it include permits?", "Typical permit and disposal costs are built into the fixed-cost component.")],
  related=["renovation-roi-calculator", "home-equity-calculator", "paint-calculator"]),

dict(slug="paint-calculator", name="Paint calculator", short="Gallons, quarts and cost for any room", icon="roller", kw="paint calculator gallons room",
  title="Paint Calculator: How Much Paint Do I Need?",
  desc="Calculate wall area, gallons and quarts of paint, and cost for any room — accounting for doors, windows, coats and ceilings.",
  intro="Enter your room size, openings and coats. The calculator subtracts doors (about 21 sq ft) and windows (about 15 sq ft) and rounds up to the gallons and quarts you should buy.",
  calc=lambda R: f"""<div class="calc" data-tool="paint"><div>
<div class="row3">{num("Length", "length", 14, 0.5, "", "ft")}{num("Width", "width", 12, 0.5, "", "ft")}{num("Wall height", "height", 8, 0.5, "", "ft")}</div>
<div class="row3">{num("Doors", "doors", 1, 1)}{num("Windows", "windows", 2, 1)}{sel("Coats", "coats", [(1, "1 coat"), (2, "2 coats"), (3, "3 coats")], 2)}</div>
<div class="row">{num("Coverage per gallon", "coverage", 350, 10, "", "sq ft")}{num("Price per gallon", "price_gal", 45, 1, "$")}</div>
{chk("Include the ceiling", "ceiling")}</div>
{result("Paint needed", "gallons", 'Buy: <b data-out="buy"></b>', [("Paintable area", "area"), ("Paint cost", "cost"), ("Pro labor estimate", "pro_cost")], ("Get painting quotes →", "get-quotes.html?service=painting"), bars=False, R=R)}</div>""",
  how=["Wall area = 2 × (length + width) × height − doors × 21 − windows × 15 (+ ceiling if selected).", "Gallons = area × coats ÷ coverage. Most quality paints cover 350–400 sq ft per gallon on smooth walls.", "Pro labor estimate uses $2.25–$4.50 per sq ft of paintable surface."],
  tips=["Prime new drywall, stains and dramatic color changes.", "Buy one extra quart for touch-ups.", "Textured or porous surfaces can cut coverage to 250–300 sq ft per gallon."],
  faqs=[("How much paint for a 12×12 room?", "About 1–1.5 gallons for two coats on 8-ft walls, before openings."), ("Do I need two coats?", "Usually — two coats give even color and durability, especially with color changes."), ("How much does a painter charge per room?", "Typically $400–$1,200 for walls, more with ceilings and trim.")],
  related=["flooring-calculator", "project-cost-estimator", "renovation-roi-calculator"]),

dict(slug="flooring-calculator", name="Flooring calculator", short="Square footage, boxes, waste and installed cost", icon="floor", kw="flooring calculator square feet boxes",
  title="Flooring Calculator: Square Feet, Boxes & Cost",
  desc="Calculate how much flooring to buy — square feet, boxes and waste — plus material and installation cost for LVP, laminate, hardwood, tile and carpet.",
  intro="Measure the room, pick a flooring type and enter box coverage and prices. The calculator adds the right waste factor and rounds up to whole boxes.",
  calc=lambda R: f"""<div class="calc" data-tool="flooring"><div>
<div class="row">{num("Room length", "length", 16, 0.5, "", "ft")}{num("Room width", "width", 14, 0.5, "", "ft")}</div>
{sel("Flooring type", "type", [("lvp", "Luxury vinyl plank (10% waste)"), ("laminate", "Laminate (10%)"), ("hardwood", "Hardwood (10%)"), ("tile", "Tile (12%)"), ("herringbone", "Herringbone / diagonal (15%)"), ("carpet", "Carpet (8%)")], "lvp")}
<div class="row3">{num("Sq ft per box", "box", 22, 0.5)}{num("Material / sq ft", "material", 3.5, 0.05, "$")}{num("Install / sq ft", "labor", 2.5, 0.05, "$")}</div></div>
{result("Total installed cost", "total", 'You need <b data-out="boxes"></b> (<span data-out="need"></span> incl. <span data-out="waste"></span> waste)', [("Room area", "area"), ("Materials", "material"), ("Installation", "labor")], ("Get flooring quotes →", "get-quotes.html?service=flooring"), R=R)}</div>""",
  how=["Area = length × width. Purchase quantity = area × (1 + waste factor), rounded up to whole boxes.", "Waste covers cuts, mistakes and future repairs; patterns need more.", "Installed cost = boxes × box coverage × material price + area × installation price."],
  tips=["Order from the same production lot to avoid color variation.", "Keep a box for future repairs.", "Acclimate wood and LVP for 48–72 hours before installation."],
  faqs=[("How much extra flooring should I buy?", "10% for most straight-lay floors, 12%–15% for tile and patterns."), ("How do I measure an L-shaped room?", "Split it into rectangles, calculate each, then add them."), ("Is LVP cheaper than hardwood?", "Yes — usually half the installed cost or less, and it's waterproof.")],
  related=["paint-calculator", "project-cost-estimator", "renovation-roi-calculator"]),
]


def build_all():
    T = {t["slug"]: t for t in TOOLS}

    def index_body(R):
        cards = "".join(f'<a class="tile" href="{R}tools/{t["slug"]}.html"><span class="card-icon">{icon(t["icon"])}</span><div><b>{E(t["name"])}</b><span>{E(t["short"])}</span></div></a>' for t in TOOLS)
        return page_hero(R, "Free home & mortgage calculators", "Twelve calculators for the biggest home money decisions — buying, borrowing, selling and renovating. No sign-up, works in USD or CAD.",
                         [("Calculators", None)], "Tools") + f'<section><div class="wrap"><div class="grid g3">{cards}</div></div></section>'
    page("tools/index.html", "Home & Mortgage Calculators (Free)", "Free mortgage, affordability, refinance, HELOC, rent-vs-buy, net proceeds, commission, closing cost, renovation ROI, project, paint and flooring calculators.",
         index_body, crumbs=[("Calculators", None)], priority=0.8)

    for t in TOOLS:
        def body(R, t=t):
            how = "".join(f"<p>{p}</p>" for p in t["how"])
            tips = "".join(f"<li>{E(x)}</li>" for x in t["tips"])
            rel = "".join(f'<a class="tile" href="{R}tools/{s}.html"><span class="card-icon">{icon(T[s]["icon"])}</span><div><b>{E(T[s]["name"])}</b><span>{E(T[s]["short"])}</span></div></a>' for s in t["related"])
            return page_hero(R, E(t["name"][0].upper() + t["name"][1:]), E(t["intro"]), [("Calculators", "tools/index.html"), (t["name"], None)], "Calculator") + f"""
<section style="padding-top:36px"><div class="wrap">{t["calc"](R)}</div></section>
<section class="alt"><div class="wrap grid g2" style="gap:36px;align-items:start">
  <div class="prose"><h2>How this calculator works</h2>{how}<h2>Pro tips</h2><ul>{tips}</ul></div>
  <div><h2>FAQ</h2>{faq_html(t["faqs"])}<p class="notice" style="margin-top:16px">Results are estimates for planning only and are not financial, tax or legal advice. Confirm figures with licensed professionals.</p></div>
</div></section>
<section><div class="wrap"><h2>Related calculators</h2><div class="grid g3">{rel}</div></div></section>"""
        ld = [faq_ld(t["faqs"]), {"@context": "https://schema.org", "@type": "WebApplication", "name": t["title"], "applicationCategory": "FinanceApplication",
                                   "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}]
        page(f"tools/{t['slug']}.html", t["title"], t["desc"], body, crumbs=[("Calculators", "tools/index.html"), (t["name"], None)], ld=ld, tools=True, priority=0.8)
