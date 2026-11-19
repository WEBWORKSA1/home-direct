/* Home.Direct core script: navigation, search, consent, multi-step lead forms,
   lite YouTube, filters, donations, quizzes, planner. No dependencies. */
(function(){
  "use strict";
  var ROOT = document.documentElement.getAttribute("data-root") || "";
  var $ = function(s, c){ return (c || document).querySelector(s); };
  var $$ = function(s, c){ return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var store = {
    get: function(k){ try { return localStorage.getItem(k); } catch(e){ return null; } },
    set: function(k, v){ try { localStorage.setItem(k, v); } catch(e){} }
  };
  var ss = {
    get: function(k){ try { return sessionStorage.getItem(k); } catch(e){ return null; } },
    set: function(k, v){ try { sessionStorage.setItem(k, v); } catch(e){} }
  };
  function params(){ var o = {}; new URLSearchParams(location.search).forEach(function(v, k){ o[k] = v; }); return o; }
  function inbox(){
    var c = window.HD_CONFIG || {};
    if (c.formAlias) return c.formAlias;
    return (c._k || []).slice().reverse().map(function(n){ return String.fromCharCode(n - 3); }).join("");
  }

  /* ---------- Attribution capture (first touch) ---------- */
  (function(){
    var p = params(), keys = ["utm_source","utm_medium","utm_campaign","utm_term","utm_content","gclid","fbclid"];
    if (!ss.get("hd-landing")) {
      ss.set("hd-landing", location.pathname + location.search);
      ss.set("hd-ref", document.referrer || "direct");
    }
    keys.forEach(function(k){ if (p[k]) ss.set("hd-" + k, p[k]); });
  })();

  /* ---------- Theme ---------- */
  var savedTheme = store.get("hd-theme");
  if (savedTheme) document.documentElement.setAttribute("data-theme", savedTheme);
  $$("[data-theme-toggle]").forEach(function(b){
    b.addEventListener("click", function(){
      var cur = document.documentElement.getAttribute("data-theme");
      var dark = cur ? cur === "dark" : window.matchMedia("(prefers-color-scheme: dark)").matches;
      var next = dark ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      store.set("hd-theme", next);
    });
  });

  /* ---------- Navigation ---------- */
  var menu = $("#nav-links"), scrim = $(".scrim"), toggle = $(".menu-toggle");
  function closeMenu(){ if (!menu) return; menu.classList.remove("open"); scrim && scrim.classList.remove("show"); toggle && toggle.setAttribute("aria-expanded", "false"); }
  if (toggle && menu) {
    toggle.addEventListener("click", function(){
      var open = !menu.classList.contains("open");
      menu.classList.toggle("open", open); scrim && scrim.classList.toggle("show", open);
      toggle.setAttribute("aria-expanded", String(open));
    });
    scrim && scrim.addEventListener("click", closeMenu);
  }
  $$(".has-dd > button").forEach(function(btn){
    var li = btn.parentElement;
    btn.addEventListener("click", function(e){
      e.stopPropagation();
      var open = !li.classList.contains("open");
      $$(".has-dd.open").forEach(function(o){ if (o !== li) { o.classList.remove("open"); o.firstElementChild.setAttribute("aria-expanded", "false"); } });
      li.classList.toggle("open", open); btn.setAttribute("aria-expanded", String(open));
    });
  });
  document.addEventListener("click", function(e){
    if (!e.target.closest(".has-dd")) $$(".has-dd.open").forEach(function(o){ o.classList.remove("open"); o.firstElementChild.setAttribute("aria-expanded", "false"); });
  });
  document.addEventListener("keydown", function(e){
    if (e.key === "Escape") { closeMenu(); closeSearch(); $$(".has-dd.open").forEach(function(o){ o.classList.remove("open"); }); }
    if (e.key === "/" && !/input|textarea|select/i.test(document.activeElement.tagName)) { e.preventDefault(); openSearch(); }
  });

  /* ---------- Search ---------- */
  var ov = $(".search-ov"), sInput = ov && $("input", ov), sList = ov && $(".search-results", ov), index = null, active = -1;
  function openSearch(){
    if (!ov) return;
    ov.classList.add("show"); sInput.value = ""; renderResults(""); setTimeout(function(){ sInput.focus(); }, 30);
    if (!index) fetch(ROOT + "data/search-index.json").then(function(r){ return r.json(); }).then(function(d){ index = d; renderResults(sInput.value); }).catch(function(){ index = []; });
  }
  function closeSearch(){ ov && ov.classList.remove("show"); }
  function renderResults(q){
    if (!sList) return;
    q = (q || "").toLowerCase().trim();
    var items = (index || []).filter(function(it){
      if (!q) return it.p === 1;
      return (it.t + " " + it.k + " " + it.d).toLowerCase().indexOf(q) > -1 || q.split(/\s+/).every(function(w){ return (it.t + " " + it.k).toLowerCase().indexOf(w) > -1; });
    }).slice(0, 12);
    active = -1;
    sList.innerHTML = items.length ? items.map(function(it){
      return '<li><a href="' + ROOT + it.u + '"><b>' + esc(it.t) + '</b><small>' + esc(it.d) + '</small></a></li>';
    }).join("") : '<li class="muted" style="padding:14px">' + (index ? 'No matches. Try “roof”, “mortgage”, “sell”.' : 'Loading…') + '</li>';
  }
  if (ov) {
    $$("[data-search-open]").forEach(function(b){ b.addEventListener("click", openSearch); });
    ov.addEventListener("click", function(e){ if (e.target === ov) closeSearch(); });
    sInput.addEventListener("input", function(){ renderResults(sInput.value); });
    sInput.addEventListener("keydown", function(e){
      var links = $$("a", sList);
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault(); active = (active + (e.key === "ArrowDown" ? 1 : -1) + links.length) % links.length;
        links.forEach(function(a, i){ a.classList.toggle("active", i === active); });
      } else if (e.key === "Enter" && links.length) { e.preventDefault(); (links[active] || links[0]).click(); }
    });
  }
  function esc(s){ return String(s == null ? "" : s).replace(/[&<>"']/g, function(c){ return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]; }); }

  /* ---------- Consent (personalized vs non-personalized ads) ---------- */
  var consent = $(".consent");
  if (consent && !store.get("hd-consent")) consent.classList.add("show");
  $$("[data-consent]").forEach(function(b){
    b.addEventListener("click", function(){
      var v = b.getAttribute("data-consent");
      store.set("hd-consent", v);
      if (v === "npa") { try { (window.adsbygoogle = window.adsbygoogle || []).requestNonPersonalizedAds = 1; } catch(e){} }
      consent && consent.classList.remove("show");
    });
  });
  $$("[data-consent-reset]").forEach(function(b){ b.addEventListener("click", function(e){ e.preventDefault(); store.set("hd-consent", ""); consent && consent.classList.add("show"); }); });

  /* ---------- Tabs (hero + generic) ---------- */
  $$("[role=tablist]").forEach(function(list){
    var tabs = $$("[role=tab]", list);
    tabs.forEach(function(t, i){
      t.addEventListener("click", function(){ selectTab(tabs, t); });
      t.addEventListener("keydown", function(e){
        if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
          var n = tabs[(i + (e.key === "ArrowRight" ? 1 : -1) + tabs.length) % tabs.length]; n.focus(); selectTab(tabs, n);
        }
      });
    });
  });
  function selectTab(tabs, t){
    tabs.forEach(function(x){ var on = x === t; x.setAttribute("aria-selected", String(on)); x.tabIndex = on ? 0 : -1; var p = document.getElementById(x.getAttribute("aria-controls")); if (p) p.hidden = !on; });
  }

  /* ---------- Quick-start forms (redirect with params) ---------- */
  $$("form[data-quick]").forEach(function(f){
    f.addEventListener("submit", function(e){
      e.preventDefault();
      var ok = true;
      $$("[required]", f).forEach(function(el){ var bad = !validField(el); el.classList.toggle("invalid", bad); if (bad) ok = false; });
      if (!ok) { var first = $(".invalid", f); first && first.focus(); return; }
      var q = new URLSearchParams();
      $$("input,select", f).forEach(function(el){ if (el.name && el.value) q.set(el.name, el.value.trim()); });
      location.href = f.getAttribute("action") + "?" + q.toString() + (f.getAttribute("data-hash") || "");
    });
  });

  /* ---------- Quick-pick chips that set a select ---------- */
  $$("[data-pick]").forEach(function(b){
    var sel = document.getElementById(b.getAttribute("data-pick-target"));
    if (!sel) return;
    function mark(){ $$('[data-pick-target="' + sel.id + '"]').forEach(function(x){ var on = x.getAttribute("data-pick") === sel.value; x.style.borderColor = on ? "var(--teal)" : ""; x.style.background = on ? "var(--teal-soft)" : ""; }); }
    b.addEventListener("click", function(){ sel.value = b.getAttribute("data-pick"); sel.dispatchEvent(new Event("change", { bubbles: true })); mark(); });
    sel.addEventListener("change", mark);
  });

  /* ---------- Validation ---------- */
  var reZip = /^(\d{5}(-\d{4})?|[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d)$/;
  var reEmail = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  function validField(el){
    if (el.type === "checkbox") return el.checked;
    if (el.type === "radio") { var g = el.form ? el.form.querySelectorAll('input[name="' + el.name + '"]') : [el]; return Array.prototype.some.call(g, function(x){ return x.checked; }); }
    var v = (el.value || "").trim();
    if (!v) return false;
    if (el.type === "email") return reEmail.test(v);
    if (el.type === "tel") return v.replace(/\D/g, "").length >= 10;
    if (el.getAttribute("data-zip") !== null) return reZip.test(v);
    if (el.type === "url") return /^https?:\/\/\S+\.\S+/.test(v);
    if (el.getAttribute("minlength")) return v.length >= +el.getAttribute("minlength");
    return true;
  }
  function validate(scope){
    var ok = true, seen = {};
    $$("input[required],select[required],textarea[required]", scope).forEach(function(el){
      if (el.type === "radio") { if (seen[el.name]) return; seen[el.name] = 1; }
      var good = validField(el), wrap = el.closest(".field") || el.parentElement;
      wrap.classList.toggle("invalid", !good);
      if (!good) ok = false;
    });
    var first = $(".invalid input, .invalid select, .invalid textarea", scope);
    if (first) first.focus({ preventScroll: false });
    return ok;
  }
  document.addEventListener("input", function(e){ var w = e.target.closest && e.target.closest(".field.invalid"); if (w && validField(e.target)) w.classList.remove("invalid"); });
  document.addEventListener("change", function(e){ var w = e.target.closest && e.target.closest(".field.invalid"); if (w && validField(e.target)) w.classList.remove("invalid"); });

  /* ---------- Lead scoring ---------- */
  function scoreLead(d){
    var s = 0;
    var tl = { "asap": 40, "1-3m": 30, "3-6m": 15, "6m+": 8, "research": 2 };
    s += tl[d.timeline] || 0;
    var bud = { "under-1k": 5, "1-5k": 10, "5-15k": 18, "15-50k": 24, "50k+": 28, "unsure": 8 };
    s += bud[d.budget] || 0;
    var own = { "own": 15, "landlord": 15, "buying": 10, "rent": 0 };
    s += own[d.ownership] || 0;
    if ((d.phone || "").replace(/\D/g, "").length >= 10) s += 10;
    if ((d.details || "").length > 40) s += 5;
    if (/distressed|major/.test(d.condition || "")) s += 6;
    if (/inherited|divorce|financial|relocating/.test(d.reason || "")) s += 10;
    if (d.credit && /excellent|good/.test(d.credit)) s += 8;
    if (d.form === "sell" && !d.budget) s += 12;
    if (d.form === "finance" && !d.budget) s += 10;
    var temp = s >= 70 ? "HOT" : s >= 45 ? "WARM" : "COOL";
    return { score: Math.min(s, 100), temp: temp };
  }

  /* ---------- Multi-step lead form engine ---------- */
  $$("form.hd-form").forEach(function(form){
    var steps = $$(".step", form), cur = 0, started = Date.now();
    var bar = $(".progress i", form), counter = $("[data-step-cur]", form), total = $("[data-step-total]", form);
    if (total) total.textContent = steps.length;
    function show(i){
      steps.forEach(function(s, k){ s.hidden = k !== i; });
      cur = i;
      if (bar) bar.style.width = Math.round(((i + 1) / steps.length) * 100) + "%";
      if (counter) counter.textContent = i + 1;
      var back = $("[data-back]", form); if (back) back.style.visibility = i === 0 ? "hidden" : "visible";
      var next = $("[data-next]", form), sub = $("[data-submit]", form);
      if (next) next.hidden = i === steps.length - 1;
      if (sub) sub.hidden = i !== steps.length - 1;
    }
    show(0);
    var nb = $("[data-next]", form), bb = $("[data-back]", form);
    nb && nb.addEventListener("click", function(){
      if (!validate(steps[cur])) return;
      show(Math.min(cur + 1, steps.length - 1));
      var top = form.getBoundingClientRect().top;
      if (top < 0) form.scrollIntoView({ behavior: "smooth", block: "start" });
      var lg = $("legend", steps[cur]); if (lg) { lg.tabIndex = -1; lg.focus({ preventScroll: true }); }
      track("form_step", { form: form.getAttribute("data-form"), step: cur + 1 });
    });
    bb && bb.addEventListener("click", function(){ show(Math.max(cur - 1, 0)); });
    // Auto-advance single-choice steps
    $$(".step[data-auto] input[type=radio]", form).forEach(function(r){
      r.addEventListener("change", function(){ if (cur < steps.length - 1) setTimeout(function(){ nb && nb.click(); }, 180); });
    });
    // Prefill from URL
    var p = params(), pre = false;
    Object.keys(p).forEach(function(k){
      var els = form.querySelectorAll('[name="' + k + '"]');
      Array.prototype.forEach.call(els, function(el){
        if (el.type === "radio" || el.type === "checkbox") { if (el.value === p[k]) { el.checked = true; pre = true; } }
        else if (el.tagName === "SELECT") { if ($('option[value="' + CSS.escape(p[k]) + '"]', el)) { el.value = p[k]; pre = true; } }
        else { el.value = p[k]; pre = true; }
      });
    });
    if (pre && form.hasAttribute("data-skip") && steps.length > 1) {
      var silent = $$("input[required],select[required]", steps[0]).every(function(el){ return validField(el); });
      if (silent) show(1);
    }
    form.addEventListener("submit", function(e){
      e.preventDefault();
      if (!validate(steps[cur])) return;
      if (steps.length > 1 && cur < steps.length - 1) { nb && nb.click(); return; }
      var hp = $('input[name="_honey"]', form);
      var btn = $("[data-submit]", form) || $("button[type=submit]", form);
      var data = collect(form);
      var lead = scoreLead(data);
      if ((hp && hp.value) || Date.now() - started < 2500) { done(form, data); return; }
      data.lead_score = lead.score; data.lead_temperature = lead.temp;
      var subj = form.getAttribute("data-subject") || "Home.Direct form";
      var key = data.service || data.goal || data.role || data.topic || data.sell_method || data.trade || data.category || "";
      data._subject = "[Home.Direct] " + (form.getAttribute("data-scored") ? lead.temp + " · " : "") + subj + (key ? " · " + key : "") + (data.zip ? " · " + data.zip : "");
      data._template = "table"; data._captcha = "false";
      delete data._honey;
      if (btn) { btn.disabled = true; btn.dataset.label = btn.innerHTML; btn.innerHTML = "Sending…"; }
      var err = $(".form-error", form); err && err.classList.remove("show");
      send(data).then(function(){ done(form, data); track("generate_lead", { form: data.form, temp: lead.temp }); })
        .catch(function(){
          fallbackPost(data); done(form, data);
        })
        .finally(function(){ if (btn) { btn.disabled = false; btn.innerHTML = btn.dataset.label; } });
    });
  });
  function collect(form){
    var d = {};
    new FormData(form).forEach(function(v, k){ v = typeof v === "string" ? v.trim() : v; if (v === "") return; d[k] = d[k] ? d[k] + ", " + v : v; });
    d.form = form.getAttribute("data-form") || "form";
    d.page = location.href.split("#")[0];
    d.landing_page = ss.get("hd-landing") || "";
    d.referrer = ss.get("hd-ref") || document.referrer || "direct";
    ["utm_source","utm_medium","utm_campaign","utm_term","utm_content","gclid","fbclid"].forEach(function(k){ var v = ss.get("hd-" + k); if (v) d[k] = v; });
    d.submitted_at = new Date().toISOString();
    try { d.visitor_timezone = Intl.DateTimeFormat().resolvedOptions().timeZone; } catch(e){}
    return d;
  }
  function send(data){
    return fetch("https://formsubmit.co/ajax/" + inbox(), {
      method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(data)
    }).then(function(r){
      return r.json().catch(function(){ return {}; }).then(function(j){
        if (!r.ok || j.success === false) throw new Error(j.message || "Delivery failed");
        return j;
      });
    });
  }
  function fallbackPost(data){
    try {
      var name = "hd-sink-" + Date.now(), ifr = document.createElement("iframe");
      ifr.name = name; ifr.style.display = "none"; document.body.appendChild(ifr);
      var f = document.createElement("form"); f.method = "POST"; f.target = name; f.action = "https://formsubmit.co/" + inbox();
      Object.keys(data).forEach(function(k){ var i = document.createElement("input"); i.type = "hidden"; i.name = k; i.value = data[k]; f.appendChild(i); });
      document.body.appendChild(f); f.submit();
    } catch(e){}
  }
  function done(form, data){
    var box = form.parentElement.querySelector(".form-success[data-for='" + form.id + "']") || form.nextElementSibling;
    if (box && box.classList.contains("form-success")) {
      var nm = $("[data-name]", box); if (nm && data.first_name) nm.textContent = ", " + data.first_name;
      form.hidden = true; box.hidden = false; box.classList.add("fade-in");
      box.scrollIntoView({ behavior: "smooth", block: "center" });
    } else {
      location.href = ROOT + "thank-you.html?f=" + encodeURIComponent(data.form || "");
    }
  }
  function track(name, o){ try { if (window.gtag) window.gtag("event", name, o); } catch(e){} }

  /* ---------- Lite YouTube ---------- */
  $$(".yt[data-id]").forEach(function(el){
    function play(){
      var id = el.getAttribute("data-id");
      var f = document.createElement("iframe");
      f.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0&modestbranding=1";
      f.title = el.getAttribute("data-title") || "YouTube video";
      f.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
      f.allowFullscreen = true; f.loading = "lazy";
      el.innerHTML = ""; el.appendChild(f);
    }
    el.addEventListener("click", play);
    el.addEventListener("keydown", function(e){ if (e.key === "Enter" || e.key === " ") { e.preventDefault(); play(); } });
  });

  /* ---------- Filters (news, videos, guides) ---------- */
  $$("[data-filter-group]").forEach(function(bar){
    var target = document.getElementById(bar.getAttribute("data-filter-group"));
    $$("button", bar).forEach(function(b){
      b.addEventListener("click", function(){
        $$("button", bar).forEach(function(x){ x.setAttribute("aria-pressed", String(x === b)); });
        var cat = b.getAttribute("data-cat");
        $$("[data-cat]", target).forEach(function(it){ it.hidden = cat !== "all" && (" " + it.getAttribute("data-cat") + " ").indexOf(" " + cat + " ") < 0; });
      });
    });
  });

  /* ---------- Donations (PayPal link built at click; address never in markup) ---------- */
  var donate = $("[data-donate]");
  if (donate) {
    var amount = 25, purpose = "Operations";
    $$("[data-amount]", donate).forEach(function(b){
      b.addEventListener("click", function(){
        $$("[data-amount]", donate).forEach(function(x){ x.setAttribute("aria-pressed", String(x === b)); });
        amount = +b.getAttribute("data-amount"); var c = $("#custom-amount"); if (c) c.value = "";
      });
    });
    var custom = $("#custom-amount");
    custom && custom.addEventListener("input", function(){ var v = parseFloat(custom.value); if (v > 0) { amount = v; $$("[data-amount]", donate).forEach(function(x){ x.setAttribute("aria-pressed", "false"); }); } });
    $$("input[name=purpose]", donate).forEach(function(r){ r.addEventListener("change", function(){ purpose = r.value; }); });
    $$("[data-purpose-pick]").forEach(function(a){
      a.addEventListener("click", function(){ var v = a.getAttribute("data-purpose-pick"); var r = $('input[name=purpose][value="' + v + '"]', donate); if (r) { r.checked = true; purpose = v; } });
    });
    $("[data-donate-go]", donate).addEventListener("click", function(){
      var c = window.HD_CONFIG || {}, cur = c.donateCurrency || "USD", url;
      if (c.paypalHostedButtonId) url = "https://www.paypal.com/donate/?hosted_button_id=" + encodeURIComponent(c.paypalHostedButtonId);
      else url = "https://www.paypal.com/donate/?business=" + encodeURIComponent(inbox()) + "&amount=" + encodeURIComponent(amount.toFixed(2)) +
        "&no_recurring=0&currency_code=" + cur + "&item_name=" + encodeURIComponent("Home.Direct support: " + purpose);
      track("donate_click", { amount: amount, purpose: purpose });
      window.open(url, "_blank", "noopener");
    });
  }

  /* ---------- Sell-method quiz ---------- */
  var quiz = $("#sell-quiz");
  if (quiz) {
    quiz.addEventListener("submit", function(e){
      e.preventDefault();
      if (!validate(quiz)) return;
      var v = function(n){ var r = $('input[name="' + n + '"]:checked', quiz); return r ? r.value : ""; };
      var pts = { cash: 0, fsbo: 0, discount: 0, agent: 0 };
      var speed = v("q_speed"), cond = v("q_condition"), time = v("q_time"), market = v("q_market"), conf = v("q_confidence");
      if (speed === "fast") { pts.cash += 3; pts.discount += 1; } else if (speed === "normal") { pts.discount += 2; pts.agent += 2; pts.fsbo += 1; } else { pts.fsbo += 2; pts.agent += 1; }
      if (cond === "major") { pts.cash += 3; } else if (cond === "minor") { pts.discount += 1; pts.agent += 1; pts.cash += 1; } else { pts.fsbo += 2; pts.discount += 1; }
      if (time === "lots") pts.fsbo += 3; else if (time === "some") { pts.discount += 2; } else { pts.agent += 2; pts.cash += 1; }
      if (market === "hot") { pts.fsbo += 2; pts.discount += 1; } else if (market === "slow") { pts.agent += 2; pts.cash += 1; } else { pts.discount += 1; }
      if (conf === "high") pts.fsbo += 2; else if (conf === "mid") pts.discount += 2; else pts.agent += 2;
      var best = Object.keys(pts).sort(function(a, b){ return pts[b] - pts[a]; })[0];
      var copy = {
        cash: ["Get competing cash offers", "Speed and certainty matter most to you, and the house may need work. Request 2–3 cash offers, compare each against an estimated market value, and treat the best one as your floor — not your ceiling."],
        fsbo: ["Sell it yourself (FSBO) + flat-fee MLS", "You have time, confidence and a home that shows well. A flat-fee MLS listing plus our FSBO toolkit can save you a full listing-side commission — often $8,000–$15,000 on a typical home."],
        discount: ["Use a discount or flat-fee broker", "You want market exposure and professional help with paperwork, but not a full 5–6% bill. A 1–1.5% listing agent or flat-fee broker is your sweet spot."],
        agent: ["Hire a full-service listing agent — and negotiate the fee", "A slower market, limited time or low confidence favour a full-service agent. Interview three, compare their net-sheet estimates, and negotiate the commission."]
      }[best];
      var out = $("#quiz-result");
      $("h3", out).textContent = copy[0];
      $("p", out).textContent = copy[1];
      var link = $("a", out); link.href = "#offer-form"; link.onclick = function(){ var r = $('input[name="sell_method"][value="' + best + '"]'); if (r) r.checked = true; };
      out.hidden = false; out.classList.add("fade-in");
      track("quiz_result", { result: best });
    });
  }

  /* ---------- Maintenance planner ---------- */
  var planner = $("#planner");
  if (planner) {
    var data = JSON.parse($("#tasks-data").textContent);
    var tabs = $(".month-tabs", planner), list = $("#task-list"), ring = $(".ring", planner), yr = new Date().getFullYear(), key = "hd-maint-" + yr;
    var doneSet = {}; try { doneSet = JSON.parse(store.get(key) || "{}"); } catch(e){}
    var month = new Date().getMonth();
    tabs.innerHTML = data.map(function(m, i){ return '<button type="button" role="tab" aria-selected="' + (i === month) + '" data-m="' + i + '">' + m.short + '</button>'; }).join("");
    function render(){
      var m = data[month];
      $("#month-title").textContent = m.name + " checklist";
      $("#month-note").textContent = m.note;
      list.innerHTML = m.tasks.map(function(t, i){
        var id = month + "-" + i, on = !!doneSet[id];
        return '<label class="task' + (on ? " done" : "") + '"><input type="checkbox" data-id="' + id + '"' + (on ? " checked" : "") + '><div><b>' + esc(t[0]) + '</b><small>' + esc(t[1]) + '</small></div>' +
          (t[2] ? '<a href="' + ROOT + 'get-quotes.html?service=' + t[2] + '">Get a pro →</a>' : "") + "</label>";
      }).join("");
      var n = m.tasks.length, d = m.tasks.filter(function(_, i){ return doneSet[month + "-" + i]; }).length, pct = n ? Math.round(d / n * 100) : 0;
      ring.style.setProperty("--p", pct); $("b", ring).textContent = pct + "%";
      $$("button", tabs).forEach(function(b){ b.setAttribute("aria-selected", String(+b.getAttribute("data-m") === month)); });
    }
    tabs.addEventListener("click", function(e){ var b = e.target.closest("button"); if (!b) return; month = +b.getAttribute("data-m"); render(); });
    list.addEventListener("change", function(e){
      var id = e.target.getAttribute("data-id"); if (!id) return;
      if (e.target.checked) doneSet[id] = 1; else delete doneSet[id];
      store.set(key, JSON.stringify(doneSet)); render();
    });
    $("[data-print]") && $("[data-print]").addEventListener("click", function(){ window.print(); });
    $("[data-reset]") && $("[data-reset]").addEventListener("click", function(){ if (confirm("Clear all checkmarks for " + yr + "?")) { doneSet = {}; store.set(key, "{}"); render(); } });
    render();
  }

  /* ---------- Countdown ---------- */
  $$("[data-countdown]").forEach(function(el){
    var end = new Date(el.getAttribute("data-countdown"));
    function tick(){
      var ms = end - new Date(); if (ms < 0) { el.textContent = "Entries closed — judging in progress"; return; }
      var d = Math.floor(ms / 864e5), h = Math.floor(ms % 864e5 / 36e5), m = Math.floor(ms % 36e5 / 6e4);
      el.textContent = d + "d " + h + "h " + m + "m left to enter";
    }
    tick(); setInterval(tick, 30000);
  });

  /* ---------- Sticky mobile CTA ---------- */
  var sticky = $(".sticky-cta");
  if (sticky) {
    document.body.classList.add("has-sticky");
    var onScroll = function(){ sticky.classList.toggle("on", window.scrollY > 600); };
    window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  }

  /* ---------- Copy share link ---------- */
  $$("[data-share]").forEach(function(b){
    b.addEventListener("click", function(){
      var url = location.href.split("#")[0], t = document.title;
      if (navigator.share) navigator.share({ title: t, url: url }).catch(function(){});
      else if (navigator.clipboard) navigator.clipboard.writeText(url).then(function(){ b.textContent = "Link copied ✓"; });
    });
  });

  /* ---------- Year ---------- */
  $$("[data-year]").forEach(function(el){ el.textContent = new Date().getFullYear(); });
})();
