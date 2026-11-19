/* Home.Direct calculators. Each <div data-tool="name"> recalculates live on input. */
(function(){
  "use strict";
  var $ = function(s, c){ return (c || document).querySelector(s); };
  var $$ = function(s, c){ return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  function money(n, d){ if (!isFinite(n)) return "—"; var neg = n < 0; n = Math.abs(n); var s = n.toLocaleString("en-US", { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }); return (neg ? "−$" : "$") + s; }
  function short(n){ if (!isFinite(n)) return "—"; var a = Math.abs(n); if (a >= 1e6) return (n < 0 ? "−" : "") + "$" + (a / 1e6).toFixed(2) + "M"; if (a >= 1e4) return (n < 0 ? "−" : "") + "$" + Math.round(a / 1e3) + "k"; return money(n); }
  function pct(n, d){ return isFinite(n) ? n.toFixed(d == null ? 1 : d) + "%" : "—"; }
  function reader(root){
    return function(name, def){
      var el = root.querySelector('[name="' + name + '"]');
      if (!el) return def;
      if (el.type === "radio") { var c = root.querySelector('[name="' + name + '"]:checked'); return c ? c.value : def; }
      if (el.type === "checkbox") return el.checked;
      if (el.tagName === "SELECT" && isNaN(parseFloat(el.value))) return el.value;
      var v = parseFloat(String(el.value).replace(/[,$\s%]/g, ""));
      return isFinite(v) ? v : def;
    };
  }
  function out(root, key, val){ $$('[data-out="' + key + '"]', root).forEach(function(el){ el.textContent = val; }); }
  function bars(el, rows){
    if (!el) return;
    var max = Math.max.apply(null, rows.map(function(r){ return Math.abs(r[1]); }).concat([1]));
    el.innerHTML = rows.map(function(r){ return '<div class="bar"><span>' + r[0] + '</span><i class="' + (r[2] || "") + '" style="width:' + Math.max(2, Math.abs(r[1]) / max * 100) + '%"></i><b>' + short(r[1]) + "</b></div>"; }).join("");
  }
  function payment(principal, annualRate, years, canada){
    var n = years * 12; if (principal <= 0) return 0;
    var r = canada ? Math.pow(1 + annualRate / 200, 1 / 6) - 1 : annualRate / 1200;
    if (r === 0) return principal / n;
    return principal * r / (1 - Math.pow(1 + r, -n));
  }
  function monthlyRate(annualRate, canada){ return canada ? Math.pow(1 + annualRate / 200, 1 / 6) - 1 : annualRate / 1200; }
  function chart(canvas, series, opts){
    if (!canvas || !canvas.getContext) return;
    var dpr = window.devicePixelRatio || 1, w = canvas.clientWidth || 600, h = canvas.clientHeight || 240;
    canvas.width = w * dpr; canvas.height = h * dpr;
    var ctx = canvas.getContext("2d"); ctx.scale(dpr, dpr); ctx.clearRect(0, 0, w, h);
    var pad = { l: 56, r: 12, t: 14, b: 26 }, all = [];
    series.forEach(function(s){ all = all.concat(s.data); });
    var max = Math.max.apply(null, all.concat([1])), min = Math.min(0, Math.min.apply(null, all.concat([0])));
    var n = series[0].data.length, cs = getComputedStyle(document.documentElement);
    var gridC = cs.getPropertyValue("--line").trim() || "#e6dfd3", txt = cs.getPropertyValue("--muted").trim() || "#5a6676";
    ctx.font = "11px Inter, system-ui, sans-serif"; ctx.fillStyle = txt; ctx.strokeStyle = gridC; ctx.lineWidth = 1;
    for (var g = 0; g <= 4; g++) {
      var y = pad.t + (h - pad.t - pad.b) * g / 4, val = max - (max - min) * g / 4;
      ctx.beginPath(); ctx.moveTo(pad.l, y); ctx.lineTo(w - pad.r, y); ctx.stroke();
      ctx.fillText(short(val), 4, y + 4);
    }
    var lbl = opts && opts.labels || [];
    var step = Math.max(1, Math.ceil(n / 8));
    for (var i = 0; i < n; i += step) { var x = pad.l + (w - pad.l - pad.r) * (n === 1 ? 0 : i / (n - 1)); ctx.fillText(lbl[i] != null ? lbl[i] : i + 1, x - 6, h - 8); }
    series.forEach(function(s){
      ctx.beginPath(); ctx.strokeStyle = s.color; ctx.lineWidth = 2.5;
      s.data.forEach(function(v, i){
        var x = pad.l + (w - pad.l - pad.r) * (n === 1 ? 0 : i / (n - 1)), y = pad.t + (h - pad.t - pad.b) * (1 - (v - min) / (max - min || 1));
        i ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
      });
      ctx.stroke();
      if (s.fill) { ctx.lineTo(w - pad.r, h - pad.b); ctx.lineTo(pad.l, h - pad.b); ctx.closePath(); ctx.fillStyle = s.fill; ctx.fill(); }
    });
  }

  var tools = {
    mortgage: function(root, v){
      var price = v("price", 400000), downPct = v("down_pct", 20), rate = v("rate", 7), years = v("term", 30), canada = v("country", "us") === "ca";
      var down = price * downPct / 100, loan = price - down;
      var pi = payment(loan, rate, years, canada);
      var tax = v("tax", price * 0.011) / 12, ins = v("insurance", 1800) / 12, hoa = v("hoa", 0);
      var pmiRate = v("pmi_rate", 0.5), pmi = downPct < 20 ? loan * pmiRate / 100 / 12 : 0;
      var total = pi + tax + ins + hoa + pmi;
      var r = monthlyRate(rate, canada), bal = loan, yearly = [], balances = [loan], interestTot = 0, months = years * 12, rows = "";
      var yP = 0, yI = 0;
      for (var m = 1; m <= months; m++) {
        var it = bal * r, pr = Math.min(pi - it, bal); bal -= pr; interestTot += it; yP += pr; yI += it;
        if (m % 12 === 0 || m === months) { yearly.push([Math.ceil(m / 12), yP, yI, Math.max(bal, 0)]); balances.push(Math.max(bal, 0)); yP = 0; yI = 0; }
      }
      out(root, "total", money(total)); out(root, "pi", money(pi)); out(root, "tax", money(tax)); out(root, "ins", money(ins));
      out(root, "hoa", money(hoa)); out(root, "pmi", money(pmi)); out(root, "loan", money(loan)); out(root, "down", money(down));
      out(root, "interest", money(interestTot)); out(root, "cost", money(interestTot + loan));
      var d = new Date(); d.setMonth(d.getMonth() + months); out(root, "payoff", d.toLocaleDateString("en-US", { month: "short", year: "numeric" }));
      var tb = $("[data-amort]", root);
      if (tb) tb.innerHTML = yearly.map(function(y){ return "<tr><td>" + y[0] + '</td><td class="num">' + money(y[1]) + '</td><td class="num">' + money(y[2]) + '</td><td class="num">' + money(y[3]) + "</td></tr>"; }).join("");
      bars($("[data-bars]", root), [["Principal & int.", pi], ["Property tax", tax, "g"], ["Insurance", ins, "g"], ["PMI", pmi, "c"], ["HOA", hoa, "c"]]);
      chart($("canvas", root), [{ data: balances, color: "#0e7c74", fill: "rgba(14,124,116,.10)" }], { labels: balances.map(function(_, i){ return i; }) });
    },
    affordability: function(root, v){
      var income = v("income", 120000), debts = v("debts", 500), down = v("down", 60000), rate = v("rate", 7), years = v("term", 30);
      var taxRate = v("tax_rate", 1.1), ins = v("insurance", 1800) / 12, hoa = v("hoa", 0), profile = v("profile", "standard");
      var ratios = { conservative: [0.28, 0.36], standard: [0.31, 0.43], stretch: [0.36, 0.45] }[profile] || [0.31, 0.43];
      var maxHousing = Math.max(0, Math.min(income / 12 * ratios[0], income / 12 * ratios[1] - debts));
      function housing(p){ var loan = Math.max(p - down, 0); var pmi = down / p < 0.2 ? loan * 0.005 / 12 : 0; return payment(loan, rate, years) + p * taxRate / 100 / 12 + ins + hoa + pmi; }
      var lo = down, hi = down + 5e6;
      for (var i = 0; i < 60; i++) { var mid = (lo + hi) / 2; if (housing(mid) > maxHousing) hi = mid; else lo = mid; }
      var price = maxHousing > ins + hoa ? lo : down;
      out(root, "price", money(price)); out(root, "payment", money(housing(price))); out(root, "loan", money(Math.max(price - down, 0)));
      out(root, "front", pct(ratios[0] * 100, 0)); out(root, "back", pct(ratios[1] * 100, 0)); out(root, "max_housing", money(maxHousing));
      out(root, "dti", pct((housing(price) + debts) / (income / 12) * 100));
      bars($("[data-bars]", root), [["Conservative", estimate(0.28, 0.36)], ["Standard", estimate(0.31, 0.43), "g"], ["Stretch", estimate(0.36, 0.45), "c"]]);
      function estimate(f, b){ var mh = Math.max(0, Math.min(income / 12 * f, income / 12 * b - debts)); var l = down, h = down + 5e6; for (var k = 0; k < 50; k++) { var m = (l + h) / 2; if (housing(m) > mh) h = m; else l = m; } return l; }
    },
    refinance: function(root, v){
      var bal = v("balance", 300000), cur = v("current_rate", 7.5), left = v("years_left", 27), nr = v("new_rate", 6.5), nt = v("new_term", 30), cc = v("closing", 6000), cash = v("cash_out", 0), roll = v("roll_costs", false);
      var curPay = payment(bal, cur, left), newLoan = bal + cash + (roll ? cc : 0), newPay = payment(newLoan, nr, nt);
      var save = curPay - newPay, upfront = roll ? 0 : cc;
      var be = save > 0 ? (roll ? 0 : Math.ceil(cc / save)) : Infinity;
      var curInt = curPay * left * 12 - bal, newInt = newPay * nt * 12 - newLoan;
      out(root, "current_payment", money(curPay)); out(root, "new_payment", money(newPay)); out(root, "savings", money(save));
      out(root, "breakeven", !isFinite(be) ? "Never (payment rises)" : be === 0 ? "Immediate (costs rolled in)" : be + " months (" + (be / 12).toFixed(1) + " yrs)");
      out(root, "interest_diff", money(curInt - newInt - upfront)); out(root, "new_loan", money(newLoan));
      out(root, "verdict", save <= 0 ? "Payment goes up — refinance only makes sense for cash-out or a shorter term." : be <= 36 ? "Strong case: you recoup costs in 3 years or less." : be <= 60 ? "Reasonable if you'll stay 5+ years." : "Weak case: break-even is over 5 years.");
      bars($("[data-bars]", root), [["Current payment", curPay, "c"], ["New payment", newPay]]);
    },
    rentvsbuy: function(root, v){
      var rent = v("rent", 2400), rentUp = v("rent_increase", 3.5), price = v("price", 450000), downPct = v("down_pct", 10), rate = v("rate", 7), term = v("term", 30), yrs = Math.max(1, Math.round(v("years", 7)));
      var appr = v("appreciation", 3.5), taxR = v("tax_rate", 1.1), maint = v("maintenance", 1), ins = v("insurance", 1800), inv = v("invest_return", 6), sell = v("sell_cost", 6), close = v("closing", 3);
      var down = price * downPct / 100, loan = price - down, pi = payment(loan, rate, term), r = rate / 1200, mi = inv / 1200;
      // Renter invests the upfront cash (down payment + closing) instead; that growth offsets rent.
      var upfront = down + price * close / 100, invested = upfront, contributed = upfront;
      var bal = loan, value = price, rentNow = rent, rentCost = 0, buyCost = upfront, rentLine = [0], buyLine = [0], breakEven = null, rentNetF = 0;
      for (var m = 1; m <= yrs * 12; m++) {
        var it = bal * r, pr = Math.min(pi - it, bal); bal = Math.max(bal - pr, 0);
        value *= Math.pow(1 + appr / 100, 1 / 12);
        var own = (bal > 0 || pr > 0 ? pi : 0) + value * taxR / 100 / 12 + value * maint / 100 / 12 + ins / 12 + (downPct < 20 && bal > loan * 0.78 ? loan * 0.005 / 12 : 0);
        buyCost += own; rentCost += rentNow;
        var extra = Math.max(own - rentNow, 0);
        invested = invested * (1 + mi) + extra; contributed += extra;
        if (m % 12 === 0) {
          rentNow *= 1 + rentUp / 100;
          var equity = value * (1 - sell / 100) - bal, buyNet = buyCost - equity;
          var rentNet = rentCost - (invested - contributed); // rent paid minus growth on the renter's invested cash
          buyLine.push(buyNet); rentLine.push(rentNet); rentNetF = rentNet;
          if (breakEven === null && buyNet < rentNet) breakEven = m / 12;
        }
      }
      var finalEquity = value * (1 - sell / 100) - bal, buyNetF = buyCost - finalEquity;
      out(root, "rent_total", money(rentCost)); out(root, "buy_total", money(buyCost)); out(root, "equity", money(finalEquity)); out(root, "rent_net", money(rentNetF));
      out(root, "buy_net", money(buyNetF)); out(root, "winner", buyNetF < rentNetF ? "Buying wins by " + money(rentNetF - buyNetF) : "Renting wins by " + money(buyNetF - rentNetF));
      out(root, "breakeven", breakEven ? "Year " + breakEven : "Not within " + yrs + " years");
      chart($("canvas", root), [{ data: rentLine, color: "#ff5a36" }, { data: buyLine, color: "#0e7c74" }], { labels: rentLine.map(function(_, i){ return "Y" + i; }) });
    },
    equity: function(root, v){
      var value = v("value", 500000), bal = v("balance", 250000), cltv = v("cltv", 85), rate = v("rate", 8.5), draw = v("draw", 50000), years = v("term", 10);
      var maxLine = Math.max(0, value * cltv / 100 - bal), equity = value - bal, use = Math.min(draw, maxLine);
      out(root, "equity", money(equity)); out(root, "equity_pct", pct(equity / value * 100, 0)); out(root, "max_line", money(maxLine));
      out(root, "io_payment", money(use * rate / 1200)); out(root, "amort_payment", money(payment(use, rate, years)));
      out(root, "cltv_after", pct((bal + use) / value * 100));
      bars($("[data-bars]", root), [["Mortgage balance", bal, "c"], ["Borrowable equity", maxLine], ["Protected cushion", Math.max(value - bal - maxLine, 0), "g"]]);
    },
    netproceeds: function(root, v){
      var price = v("price", 450000), payoff = v("payoff", 220000), listPct = v("listing_pct", 2.75), buyPct = v("buyer_pct", 2.5), closePct = v("closing_pct", 1.5), transfer = v("transfer_pct", 0.4), repairs = v("repairs", 5000), prep = v("prep", 2500), moving = v("moving", 2500);
      var comm = price * (listPct + buyPct) / 100, closing = price * closePct / 100, tt = price * transfer / 100, total = comm + closing + tt + repairs + prep + moving, net = price - payoff - total;
      out(root, "net", money(net)); out(root, "commission", money(comm)); out(root, "closing", money(closing)); out(root, "transfer", money(tt));
      out(root, "costs", money(total)); out(root, "costs_pct", pct(total / price * 100)); out(root, "payoff", money(payoff));
      bars($("[data-bars]", root), [["Net to you", net], ["Mortgage payoff", payoff, "g"], ["Commissions", comm, "c"], ["Closing + tax", closing + tt, "c"], ["Repairs/prep/move", repairs + prep + moving, "c"]]);
    },
    commission: function(root, v){
      var price = v("price", 450000), buyer = v("buyer_pct", 2.5), offerBuyer = v("offer_buyer", true), cashDisc = v("cash_discount", 12), payBuyer = offerBuyer ? price * buyer / 100 : 0;
      var rows = [
        ["Full-service agent (2.75%)", price - price * 0.0275 - payBuyer],
        ["Discount broker (1.5%)", price - price * 0.015 - payBuyer],
        ["Flat-fee MLS ($499)", price - 499 - payBuyer],
        ["FSBO, no MLS", price - 150 - payBuyer],
        ["Cash offer (−" + cashDisc + "%, no fees)", price * (1 - cashDisc / 100)]
      ];
      var tb = $("[data-table]", root), best = rows.slice().sort(function(a, b){ return b[1] - a[1]; })[0];
      if (tb) tb.innerHTML = rows.map(function(r){ return "<tr><td>" + r[0] + '</td><td class="num">' + money(r[1]) + '</td><td class="num">' + money(r[1] - rows[0][1]) + "</td></tr>"; }).join("");
      out(root, "best", best[0]); out(root, "save", money(rows[2][1] - rows[0][1]));
      bars($("[data-bars]", root), rows.map(function(r, i){ return [r[0].split(" (")[0], r[1], i === 4 ? "c" : i === 0 ? "g" : ""]; }));
    },
    closing: function(root, v){
      var role = v("role", "buyer"), price = v("price", 400000), downPct = v("down_pct", 20), transfer = v("transfer_pct", 0.4), rate = v("rate", 7);
      var loan = price * (1 - downPct / 100), items;
      if (role === "buyer") {
        items = [["Loan origination (0.75%)", loan * 0.0075], ["Appraisal", 650], ["Home inspection", 475], ["Lender's title insurance", price * 0.0035], ["Settlement / escrow fee", 900], ["Recording & gov. fees", 275], ["Prepaid interest (15 days)", loan * rate / 100 / 365 * 15], ["Homeowners insurance (12 mo.)", 1800], ["Tax escrow (3 mo.)", price * 0.011 / 4], ["Survey & pest", 450]];
      } else {
        items = [["Listing-side commission (2.75%)", price * 0.0275], ["Buyer-agent concession (2.5%)", price * 0.025], ["Owner's title policy", price * 0.004], ["Settlement / escrow fee", 900], ["Transfer tax (" + transfer + "%)", price * transfer / 100], ["Attorney / doc prep", 750], ["Payoff & recording fees", 200], ["Pro-rated property tax", price * 0.011 / 6]];
      }
      var total = items.reduce(function(s, i){ return s + i[1]; }, 0);
      out(root, "total", money(total)); out(root, "total_pct", pct(total / price * 100));
      var tb = $("[data-table]", root); if (tb) tb.innerHTML = items.map(function(i){ return "<tr><td>" + i[0] + '</td><td class="num">' + money(i[1]) + "</td></tr>"; }).join("");
      out(root, "cash_needed", role === "buyer" ? money(total + price * downPct / 100) : "—");
    },
    roi: function(root, v){
      var sel = root.querySelector('[name="project"]'), opt = sel.options[sel.selectedIndex];
      if (root._last !== sel.value) { root.querySelector('[name="recoup"]').value = opt.getAttribute("data-recoup"); root.querySelector('[name="cost"]').value = opt.getAttribute("data-cost"); root._last = sel.value; }
      var cost = v("cost", 30000), rec = v("recoup", 70), energy = v("energy", 0), yrs = v("years", 5);
      var added = cost * rec / 100, net = cost - added - energy * yrs, roi = (added + energy * yrs - cost) / cost * 100;
      out(root, "added", money(added)); out(root, "net", money(net)); out(root, "roi", pct(roi)); out(root, "energy_total", money(energy * yrs));
      out(root, "verdict", roi >= 0 ? "Pays for itself by sale time." : roi > -30 ? "Mostly recouped — worth it if you'll enjoy it." : "Do it for lifestyle, not resale.");
      bars($("[data-bars]", root), [["Project cost", cost, "c"], ["Resale value added", added], ["Energy savings", energy * yrs, "g"]]);
    },
    estimator: function(root, v){
      var data = root._guides || (root._guides = JSON.parse((document.getElementById("guides-data") || {}).textContent || "[]"));
      var sel = root.querySelector('[name="project"]'), g = null, i;
      if (sel) { for (i = 0; i < data.length; i++) if (data[i].slug === sel.value) g = data[i]; } else g = data[0];
      if (!g) return;
      var size = root.querySelector('[name="size"]');
      if (root._slug !== g.slug) {
        root._slug = g.slug; size.min = g.size_min; size.max = g.size_max; size.step = g.size_step; size.value = g.default_size;
        out(root, "unit_label", g.size_label); var cta = $("[data-guide-link]", root); if (cta) cta.href = cta.getAttribute("data-base") + g.slug + ".html";
        var q = $("[data-quote-link]", root); if (q) q.href = q.getAttribute("data-base") + "?service=" + g.service;
      }
      var n = parseFloat(size.value) || g.default_size;
      var qm = { economy: 0.82, standard: 1, premium: 1.38 }[v("quality", "standard")] || 1;
      var rm = { low: 0.86, avg: 1, high: 1.22, ca: 1.3 }[v("region", "avg")] || 1;
      var cm = { simple: 0.9, typical: 1, complex: 1.2 }[v("complexity", "typical")] || 1;
      var low = (n * g.unit_low + g.fixed_low) * qm * rm * cm, high = (n * g.unit_high + g.fixed_high) * qm * rm * cm;
      low = Math.max(low, g.min_job * rm); high = Math.max(high, low * 1.15);
      out(root, "size_val", n.toLocaleString("en-US") + " " + g.size_unit);
      out(root, "low", money(Math.round(low / 10) * 10)); out(root, "high", money(Math.round(high / 10) * 10)); out(root, "mid", money(Math.round((low + high) / 20) * 10));
      out(root, "per_unit", money((low + high) / 2 / n, n < 50 ? 0 : 2) + " per " + g.size_unit.replace(/s$/, ""));
      out(root, "national", money(g.low) + " – " + money(g.high));
      out(root, "currency", v("region", "avg") === "ca" ? "CAD" : "USD");
    },
    paint: function(root, v){
      var L = v("length", 14), W = v("width", 12), H = v("height", 8), doors = v("doors", 1), wins = v("windows", 2), coats = v("coats", 2), cov = v("coverage", 350), ceiling = v("ceiling", false), ppg = v("price_gal", 45);
      var wall = 2 * (L + W) * H - doors * 21 - wins * 15, ceil = ceiling ? L * W : 0, area = Math.max(wall, 0) + ceil;
      var gal = area * coats / cov, galR = Math.ceil(gal * 4) / 4;
      out(root, "area", Math.round(area).toLocaleString() + " sq ft"); out(root, "gallons", galR.toFixed(2) + " gal");
      out(root, "buy", Math.floor(galR) + " gal + " + Math.round((galR - Math.floor(galR)) * 4) + " qt"); out(root, "cost", money(Math.ceil(galR) * ppg));
      out(root, "pro_cost", money(area * 2.25) + " – " + money(area * 4.5));
    },
    flooring: function(root, v){
      var L = v("length", 16), W = v("width", 14), type = v("type", "lvp"), box = v("box", 22), mat = v("material", 3.5), lab = v("labor", 2.5);
      var waste = { lvp: 10, laminate: 10, hardwood: 10, tile: 12, herringbone: 15, carpet: 8 }[type] || 10;
      var area = L * W, need = area * (1 + waste / 100), boxes = Math.ceil(need / box), matCost = boxes * box * mat, labCost = area * lab;
      out(root, "area", Math.round(area).toLocaleString() + " sq ft"); out(root, "need", Math.ceil(need).toLocaleString() + " sq ft"); out(root, "waste", waste + "%");
      out(root, "boxes", boxes + " boxes"); out(root, "material", money(matCost)); out(root, "labor", money(labCost)); out(root, "total", money(matCost + labCost));
      bars($("[data-bars]", root), [["Materials", matCost], ["Installation", labCost, "c"]]);
    }
  };

  $$("[data-tool]").forEach(function(root){
    var fn = tools[root.getAttribute("data-tool")]; if (!fn) return;
    var queued = false, v = reader(root);
    function run(){ queued = false; try { fn(root, v); } catch(e){ if (window.console) console.warn(e); } }
    function q(){ if (!queued) { queued = true; requestAnimationFrame(run); } }
    root.addEventListener("input", q); root.addEventListener("change", q);
    $$("input[type=range]", root).forEach(function(r){
      var o = root.querySelector('output[for="' + r.id + '"]');
      function sync(){ if (o) o.textContent = (r.getAttribute("data-prefix") || "") + Number(r.value).toLocaleString("en-US") + (r.getAttribute("data-suffix") || ""); }
      r.addEventListener("input", sync); sync();
    });
    window.addEventListener("resize", q);
    run();
  });
})();
