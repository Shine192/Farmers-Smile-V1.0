# Farmers’ Smile — Thailand crop-planning MVP

A mobile browser prototype for exploring crop options in Chiang Mai, Songkhla, and Surat Thani provinces. Built by Shine, Chan, Muay, and James.

## Run the project

**Requirements:** Python 3 for a local server and data preparation; Node.js and npm for the Vite development server and automated tests. The app itself is plain HTML, CSS, and JavaScript with a bundled Leaflet library. No API key, paid model service, or runtime server is needed for the downloaded offline demonstration.

```bash
# From this repository's root, choose one local server:
python3 -m http.server 8000 --directory dist
# Open http://localhost:8000 in your browser.

# Or, with Node.js installed:
npm ci
npm run dev
```

Run `npm test` to check all 72 province, month, and water combinations and offline packaging. To regenerate the prepared files from the included raw weather snapshots, run `python3 scripts/prepare_data.py` and `python3 scripts/package.py`, then test again. Data preparation and packaging use only the Python standard library. `npm ci` installs the Vite development dependency pinned in `package-lock.json`; the browser app has no npm runtime dependency. The standalone `dist/offline.html` can be opened directly after extraction.

**Repository layout:** `dist/` is the working static app and bundled data; `scripts/` holds preparation, packaging, and tests; `SOURCES.md` records data, map, library, and photo credits. `dist/data/bang-klam/` and `dist/data/phunphin/` are internal Southern reference-data identifiers for **Songkhla** and **Surat Thani**. They do not add selectable provinces. The three province names in the interface are the supported locations.

**Team:** Shine — product, research, and AI-assisted prototype development; Chan and Muay — report, narration, and presentation; James — demo video editing. AI tools assisted development; crop results run locally through historical matching and explicit screening rules.

## Submission files in this repository

- **Source code and backup ZIP:** `dist/` contains the runnable mobile web app; `dist/Farmers-Smile-Project.zip` is a downloadable backup of the complete project. `scripts/` contains the data preparation, map preparation, packaging, and test scripts.
- **Dataset:** `dist/data/README.txt` explains the raw NASA POWER responses, processed weather tables, crop assumptions, model files, map boundaries, and validation records in `dist/data/`. This directory is organized by province reference rather than duplicating files in separate raw and processed directories.
- **Dependencies:** `package.json` and `package-lock.json` pin the Vite development dependency. `requirements.txt` documents that the Python scripts use no third-party packages.

The project ZIP includes the small prepared datasets needed to rebuild and explain this prototype. It contains no large external model weights. The only inference at runtime is the bundled historical matcher and explicit crop screening rules; see below for their limits.

## Start here — no coding required

On the first visit, a short optional tour explains the flow. Choose **Show me** to follow it, or skip it. You can replay it later from the **i** help button. The guide is available in Thai and English, and does not add permanent map controls.

1. Tap Chiang Mai, Songkhla, or Surat Thani on the Thailand map. Other provinces are gray and unavailable in this version.
2. Choose a planting month and rain-only or extra water in the sheet that opens. The tour points out each choice.
3. Tap **Find crop ideas**. A short analysis screen appears for about 2–3 seconds.
4. Explore the Thailand-only results map and tap one of the three province labels to compare its crop ideas.
5. Tap a crop to open its details. The tour explains that stars compare historical climate fit; they are not the chance of success. Edit returns to the province map and planting choices.

### Offline demonstration

Use the header Offline mode button and Save offline app (`offline.html`). It downloads as `Farmers-Smile-Offline.html`. Open it in Chrome, Edge, Safari, or Firefox. Disconnect the internet and change the month and water source. All data, crop photos, province map geometry, styles, Leaflet code, and crop-comparison code are embedded. The hosted and saved versions use the same Thailand-only map and need no map tiles. Province selection, map zoom, and crop information work without internet. No paid inference, font service, or CDN is needed.

This is an offline HTML demonstration, not an installed mobile app or a service-worker-cached hosted website. Visiting the hosted website for the first time requires internet and the site's access permissions. Source links require internet. The source-package and README links are hidden in the offline copy because they are separate files.

The project ZIP includes the complete browser app, the offline file, prepared datasets, original NASA response, rebuild script, documentation, and validation results. After extracting the ZIP, `dist/offline.html` opens directly. Alternatively `python3 -m http.server 8000 --directory dist` serves the multi-file version locally; visit http://localhost:8000. Python is optional for the single-file demo.

## Scope and honest claims

- Three available provinces: Chiang Mai, Songkhla, and Surat Thani. The map colors the 25 Chiang Mai, 16 Songkhla, and 19 Surat Thani district components as single province shapes; their internal district lines are hidden in the picker. Weather comparisons use one coarse NASA POWER grid reference per province, not a province-wide average, farm measurement, or crop inventory. Southern map labels mark reference locations in Bang Klam and Phunphin districts.
- 30 complete calendar years: 1996–2025, 10,958 daily records and 360 monthly summaries PER AREA, with no missing values in the three downloaded variables.
- The comparison pool contains grain maize, soybean, groundnut, strawberry, and Arabica coffee. Songkhla and Surat Thani also include rubber, oil palm, and durian, which OAE provincial statistics identify among Southern agricultural uses. Their 365-day weather windows represent perennial tree crops, not time to harvest. They use broad FAO climate ranges as an exploratory screen; they have no local crop-yield outcome data. Each result keeps only its top three crop screens, rated one to five stars for historical climate fit. Ratings are a simple rule-based ranking, not a success probability, yield forecast, or validated variety recommendation. All three provinces are pilot references, not locally calibrated crop advice.
- 2027 is the planning year, not a claim that the app predicts 2027 weather. The recommendation logic deliberately uses historical comparisons. It would not change merely because the displayed year changes.
- No harvest outcome labels, farm trials, economic returns, yields, crop-success probabilities, actual irrigation availability, soil tests, forecast products, ENSO predictors, humidity, fire, air quality, pest, market, or terrain model.
- Do not claim “84% chance of success,” “reliable next-year forecast,” or guaranteed savings. Soil, flooding/drainage, crop variety, local day length, crop calendars, disease, and market access must be checked before real planting decisions.

## Data provenance

Each reference point has a raw daily API response in its `dist/data/<area>/` folder (the Chiang Mai default is `dist/data/nasa-power-1996-2025.json`). `dist/data/validation.json` records its SHA-256 checksum, source URL, dates, coverage, and checks. Rebuild with Python 3:

```
python3 scripts/prepare_data.py
```

This uses the included snapshot with no internet and no additional packages. To retrieve the same period again, use `python3 scripts/prepare_data.py --download` with an internet connection. Upstream revisions can change the snapshot. Run `python3 scripts/package.py` after changes to rebuild the standalone HTML and ZIP; run `node scripts/test.cjs` before final packaging.

Variables: T2M (daily mean temperature, Celsius), T2M_MAX (daily maximum temperature, Celsius), PRECTOTCORR (daily corrected precipitation, millimetres/day). Local solar time, as returned by the API. Rain below 1 mm is counted as a dry day for this prototype; 35 C is an exploratory hot-day threshold, not a universal crop injury threshold.

The crop JSON contains these published screening inputs:

| Crop | Broad seasonal water guide | Example growing duration | Broad optimal temperature |
|---|---|---|---|
| Grain maize | 500–800 mm | 125 days | 18–33 C |
| Soybean | 450–700 mm | 135 days | 20–33 C |
| Groundnut | 500–700 mm | 130 days | 22–32 C |
| Strawberry | 600–900 mm annual guide; prorated to a 240-day window in the screen | 180–270 days to harvest (FAO Ecocrop) | 11–24 C |
| Arabica coffee | 1,400–2,300 mm annual guide; prorated to a 330-day window in the screen | Perennial; 330-day weather window only | 14–28 C |

Maize, soybean, and groundnut water guides and example durations come from FAO Irrigation Water Management, Chapter 3. Temperature ranges come from FAO Ecocrop. Strawberry and Arabica ranges come from their cited FAO Ecocrop records. For their screen, annual rain ranges are prorated by the number of days in the weather window; this assumes uniform distribution and is only a rough heuristic, not a crop-season water requirement. Durations and all broad species figures are not calibrated to local varieties or yields.

## What the AI actually does

The operative AI component is an instance-based **k-nearest-neighbor historical-season matcher**, with k=7. It is implemented locally in plain JavaScript so it needs no runtime library and no paid AI service. It is a small learned reference dataset, not a large language model or a crop-outcome-trained classifier.

1. Daily data are aggregated to monthly totals/averages and complete 125/130/135-day growing windows.
2. Each growing window begins on the first of a month. Windows that run past December 31, 2025 are excluded; cross-year windows otherwise use actual subsequent-year records.
3. For the chosen month, the query is the 30-year historical monthly mean temperature and mean rain. It is NOT live weather or a real seasonal forecast.
4. Candidates are historical windows for the same crop and starting month. Temperature and rainfall differences are standardized by the monthly population standard deviations learned from the 30-year data, with small denominator floors.
5. Euclidean distance selects the seven nearest starting months; ties are ordered by year. Their actual subsequent growing-season data provide the evidence shown in the crop cards.
6. Sourced crop guides and explicit prototype rules determine the comparison. All 30 years inform the monthly query, scales, and candidate pool; not every observation receives equal weight in the final seven-season result.

This is retrospective analog retrieval. No measured forecasting skill is claimed for it. Conditioning on an actual future starting month would be leakage; this implementation queries only a climatological average, and does not use actual 2027 weather. Historical neighbor examples are not independent crop-success observations.

### Transparent screening rules

For each crop, calculate mean total gross rain R, mean temperature T, mean longest dry spell D, mean starting-month rain S, and count B of matched seasons with rain below the lower bound W of the crop's water guide.

- Water shortfall proxy: g=max(0,1-R/W).
- Temperature penalty: t=min(1,(max(0,Tmin-T)+max(0,T-Tmax))/6).
- Dry-spell proxy: d=min(1,D/25).
- Dry-start proxy: s=max(0,1-S/50).
- Rain-only ranking penalty: 0.65*g + 0.15*B/7 + d*(0.12 for maize, otherwise 0.08) + 0.30*s + 0.35*t.
- Extra-water ranking penalty: 0.35*t, explicitly CONDITIONAL on adequate supplemental water. Pump/canal presence does not establish this condition.
- High warning if t>0.5; otherwise for rain-only, S<50 mm gets a dry-start warning; otherwise g>0.25 or B>=5 gets a water warning.
- Rain-only gets a backup-water warning if B>=2 or D>=14. Other rain-only cases say “Worth considering.” All extra-water cases still say “Check your water supply.”
- Crops with penalties differing by under 0.06 are treated as close comparisons in the summary. Alphabetical crop IDs break ties for display; order alone is not evidence of superiority.
- “Months to explore” are months within 0.06 of that crop's minimum penalty, excluding high-warning months. This is NOT a validated planting calendar. It does not prescribe a sowing day. For irrigated farms it can show many months, because the screen assumes extra water and omits day-length and local-season constraints.

All weights, thresholds, k, and tie rules above are prototype design choices, not FAO standards. Gross rainfall is an optimistic upper bound on water supply: runoff, evapotranspiration, soil storage, irrigation losses, and growth-stage water balance are not calculated. Clearing this check cannot establish sufficient water. Excess rain and drainage are qualitative reminders, not modeled flooding risk. These limitations are particularly relevant in steep terrain.

## Forecast experiment — do not hide a negative result

We separately fit 12 monthly ridge trend regressions for temperature and rain (fixed penalty 100) and compare with monthly historical means. Use expanding training windows ending two years before each target year to match the 2025-to-2027 lead time. Select the method on 2016–2020 only, evaluate on subsequent 2021–2025 years, then refit through 2025. No random train/test split is used.

The historical mean won selection for both variables. Holdout mean absolute errors:

| Variable | Historical mean | Ridge trend |
|---|---|---|
| Monthly mean temperature | 0.740 C | 0.780 C |
| Monthly total rain | 42.72 mm | 43.94 mm |

The ridge model is retained as an experiment in the rebuild script and evaluation files, but is not used to claim an accurate 2027 forecast. These metrics evaluate climate estimates, not crop-ranking accuracy, and do not validate the analog matcher as a predictor. A future version needs real seasonal forecast inputs, comparison against climatology, local measurements, and agronomist-reviewed or field outcome data.

## Small-model measurements and testing

`dist/data/validation.json` records the exact prepared-model and analog-model byte sizes. `dist/data/runtime-tests.json` records actual calculation latency on the build machine, environment details, and tested cases. The app measures calculation time on the user's own device on each comparison; this excludes page load, rendering, and download time. The model bundle includes historical examples and metadata, not just coefficients.

The current engine tests cover all 12 months and both water choices for each of three supported provinces, with the top three results rated, invalid inputs, matching original records, dry-season warnings, and late-year growing windows. The offline HTML is checked for embedded scripts and styles, and disables street-map requests on file protocol. The earlier one-area version also passed a Node VM offline form-flow test; that older test is not a claim of physical-device coverage for this mobile update. WebMCP is optional and feature-detected; actual supported-browser validation is unavailable because this preview browser does not expose modelContext.

## Files

- `dist/index.html`, `styles.css`, `app.js`: visible interface and controls.
- `dist/engine.js`: matching and crop-screening logic.
- `dist/data.js`: the browser's prepared local dataset.
- `dist/offline.html`: standalone offline demonstration.
- `dist/data/daily-weather.csv`, `monthly-weather.csv`: analysis-ready data.
- `dist/data/crops.json`: editable sourced crop assumptions.
- `dist/data/model.json`, `historical-crop-windows.json`: compact model inputs.
- `dist/data/validation.json`, `runtime-tests.json`: measurements and checks.
- `scripts/prepare_data.py`, `package.py`, `test.cjs`: reproducibility tools.
- `SOURCES.md`: source links and use notes.

## What to say in the pitch

“We built a mobile crop-planning prototype for Chiang Mai, Songkhla, and Surat Thani reference areas. It uses 30 years of weather history and local crop screening rules, then shows only the three highest-rated options. Ratings summarize how broad crop needs compare with past rain and warmth. They do not predict yields or tell farmers what will happen next year.”

## Team handover

Shine: review interface and product scope. Chan and Muay: validate local farming assumptions with an agricultural adviser, review evidence, prepare narration and report. James: record January rain-only, May rain-only, and an extra-water scenario; show an explanation card and the offline copy. Before competition submission, confirm advance-work, originality, final format, and deadline rules.

## Mobile flow and map update

The mobile interface displays one step at a time and opens crop details in a modal bottom sheet. Technical content and downloads are behind the information button. Selection remains in memory while navigating; no account or location permission is required. No farm GPS coordinates are collected.

The map uses vendored Leaflet 1.9.4 (BSD license included) and bundled Thai boundary geometry. It draws Thailand’s silhouette, the three supported province borders, province names, and crop-fit shading without a tile basemap or neighboring-country details.

New area datasets can be reproduced with:

```
python3 scripts/package.py
node scripts/test.cjs
python3 scripts/package.py
```

The package step rebuilds `areas.js`, embedding the two additional Southern province models alongside the Chiang Mai reference model. Each area has its own forecast evaluation JSON. The older forecast table above describes only the original Chiang Mai reference point; it must not be generalized to the other areas. The user-facing model continues to use historical matching in each province.

For local interactive development, `npm install` then `npm run dev`; the app remains deployed as static assets. Automated checks cover the recommendation engine across 72 area/month/water combinations, offline packaging, and the presence of the bilingual onboarding steps. Visual testing on a physical phone remains to be done.

The model and interaction assets are checked in the bundled app. Browserless validation covers all 72 location, month, and water combinations. Visual testing on a physical phone remains to be done.

## Province map and language
The first step shows a tall Thailand map with Chiang Mai, Songkhla, and Surat Thani highlighted in green. Other provinces are gray and disabled for this version. Internal district lines are suppressed in the picker. Three labeled province areas can be tapped; the map also supports touch zoom and dragging. The app includes an English/Thai switch.

### Mobile layout and offline mode update
All screens, including the full-height map, use the same 480px maximum mobile width. On wide screens the app is centered. On-map +/− buttons are hidden to keep the map clear; touch, wheel, and double-tap zoom still work. The map uses bundled province geometry in both online and offline modes; it does not request map tiles. Save the standalone HTML before disconnecting to reopen the app later. The hosted app does not install a service worker. Crop photographs are bundled locally and embedded in the offline file; credits are in the information panel and SOURCES.md.

Validation for this update: JavaScript syntax and all 72 province, month, and water combinations passed; the top three result limit and each 1–5 climate-fit rating are checked. Local browser UI testing could not run because the browser download was unavailable. No cloud browser was used. Pinch gestures and offline file opening should also be checked on the target phone before the presentation.

### Thai language and simpler map
The app includes an English/Thai switch. Thai is used for the farmer-facing flow, crop names and reasons; scientific names, photo credits, and source records retain their original wording. The area picker and crop results share a simplified Thailand map. It shows Chiang Mai, Songkhla, and Surat Thani with province names and borders; other provinces are gray and unavailable in this version. Selecting a province opens the month and water choices in one sheet.


## Soil data status

The app does not currently display a soil or drainage assessment, and these factors are not included in Version 1.0 crop ratings. On the first screen, tapping a supported province opens the month and water-choice dialog directly; the separate “Choose planting time” button has been removed.
