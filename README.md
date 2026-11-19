# Home.Direct

**Go direct. Every home decision, minus the middleman.** This is a static, self-updating website for homeowners. It has:

- 24 project cost guides with estimators
- 12 home and mortgage calculators
- multi-step lead generation: pro quotes, seller options and lender matching
- live weekly mortgage rates, plus auto-updated housing news and videos
- a maintenance planner, a monthly contest, donations, careers, pro sign-ups and advertising pages

It's monetized with Google AdSense (`ca-pub-6620975821265271`), lead generation, sponsorships and donations, and hosted free on GitHub Pages from the `main` branch.

See **[BUILD-PROMPT.md](BUILD-PROMPT.md)** for the phase-wise build prompt, the concept and the 39-site research summary.

## Structure

| Path | What it is |
|---|---|
| `index.html`, `*.html`, `cost-guides/`, `tools/` | Generated pages (don't hand-edit; edit the scripts and rebuild) |
| `assets/css/style.css` | Design system and components |
| `assets/js/app.js` | Navigation, search, consent, multi-step forms, lead scoring, donations, quiz, planner |
| `assets/js/tools.js` | All calculators and estimators |
| `assets/js/config.js` | Encoded form inbox, optional FormSubmit alias, optional PayPal hosted button ID |
| `scripts/build.py` + `hd_core.py`, `pages_tools.py`, `pages_more.py` | Static site generator (Python standard library only) |
| `scripts/content_guides.py` | Cost-guide data. Add a guide by appending a dict, then rebuild |
| `scripts/site_data.py` | Services, monthly checklist, contest themes and prizes, ROI projects, roles |
| `scripts/refresh.py` + `data/sources.json` | Pulls rates (FRED/Freddie Mac PMMS), news (Google News RSS) and videos (YouTube RSS) |
| `.github/workflows/auto-refresh.yml` | Runs refresh + build every 6 hours and commits; Pages republishes |
| `ads.txt`, `robots.txt`, `sitemap.xml`, `site.webmanifest` | SEO and ads files (sitemap regenerated on every build) |

## Rebuild locally

```bash
python3 scripts/refresh.py   # optional: fetch fresh data (needs internet)
python3 scripts/build.py     # regenerate every page
python3 -m http.server 8000  # preview at http://localhost:8000
```

## Go-live checklist

1. **GitHub Pages:** Settings › Pages › Build and deployment › *Deploy from a branch* › `main` / `/ (root)` › Save.
2. **Custom domain:** Settings › Pages › Custom domain `home.direct` › Save. Then add DNS at your registrar:
   - `A` records for `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153` and `185.199.111.153`
   - `CNAME` for `www` → `webworksa1.github.io`

   When the check passes, tick **Enforce HTTPS**.
3. **Forms:** submit the Contact form once on the live site and click **Activate** in the FormSubmit email. Do this again if you later move from the github.io address to home.direct. FormSubmit's email also gives you a random alias. Paste it into `assets/js/config.js` → `formAlias` so the encoded address isn't used at all.
4. **AdSense:** add `home.direct` in AdSense, confirm `ads.txt` is found, turn on Auto ads, enable *Privacy & messaging › European regulations* (Google-certified CMP), then request review.
5. **Search Console:** add the domain and submit `https://home.direct/sitemap.xml`.

## Editing common things

- **Contest prizes and themes:** `scripts/site_data.py` (`CONTEST_PRIZES`, `CONTEST_THEMES`).
- **Advertising rates:** `scripts/pages_more.py` (`build_pros` → `adv`).
- **Cost ranges:** `scripts/content_guides.py`.
- **News queries and video channels:** `data/sources.json`.
- **Donations:** set `paypalHostedButtonId` in `assets/js/config.js` to use a PayPal hosted button.

© Home.Direct. All rights reserved. Not affiliated with any company using the name "HomeDirect" or similar. See `disclosures.html`.
