FARMERS' SMILE V1.0 — DATASET GUIDE

Scope: 1996-01-01 through 2025-12-31, with one coarse NASA POWER weather
reference per supported Thai province: Chiang Mai, Songkhla, Surat Thani.
The data are not farm measurements or province-wide averages. A crop rating
is relative historical climate fit, not a weather, yield, or profit forecast.

RAW / SOURCE FILES
  nasa-power-1996-2025.json                   Chiang Mai NASA POWER response
  bang-klam/nasa-power-1996-2025.json         Songkhla reference response
  phunphin/nasa-power-1996-2025.json          Surat Thani reference response
  thailand-districts.geojson                  Bundled Thai district geometry
  boundary-source.json                        Boundary source metadata/license

Bang Klam and Phunphin are internal reference-data folder names. In the
interface users select Songkhla and Surat Thani provinces, respectively.
These folder names do not represent additional selectable locations. The exact
weather request URLs and raw-file SHA-256 hashes are recorded in each area's
validation.json. See the repository SOURCES.md for source links and credits.

PROCESSED / OUTPUT FILES (repeat in each Southern reference folder)
  daily-weather.csv          One row per calendar day (10,958 per area).
    date                     YYYY-MM-DD
    temperature_mean_c       Daily mean near-surface temperature, Celsius
    temperature_max_c        Daily maximum near-surface temperature, Celsius
    rain_mm                  Daily corrected precipitation, millimetres
  monthly-weather.csv        One row per month (360 per area).
    year, month, days        Calendar month and day count
    temp                     Monthly mean temperature, Celsius
    rain                     Monthly rainfall total, millimetres
    dryDays                  Days with less than 1 mm rain
    hotDays                  Days with daily maximum at least 35 C
    longestDry               Longest run of days with less than 1 mm rain
  crops.json                 Broad crop screening assumptions and notes
  model.json                 Prepared monthly summaries, crop windows and
                             historical-matching inputs
  historical-crop-windows.json  Historical crop-weather comparison windows
  bundle.js                  Browser-ready version of the prepared model
  validation.json            Coverage, source hash, model size and evaluation

ROOT DATA DIRECTORY ALSO CONTAINS
  area-boundaries.geojson, *-province-components.geojson,
  thailand-country-outline.json, thailand-districts.geojson: map geometry.
  runtime-tests.json: recorded build-machine test output.

The runnable app reads bundled dist/data.js, dist/areas.js and
dist/boundaries.js generated from these prepared files. No network data call
is needed when opening the separately saved dist/offline.html demonstration.

To rebuild the Chiang Mai snapshot without downloading, run:
  python3 scripts/prepare_data.py
  python3 scripts/package.py
  npm test

The Southern folders contain their own included raw and processed references.
Re-downloading from the upstream source requires internet and can change the
snapshot. Source credits, assumptions and limitations are in README.md and
SOURCES.md at the repository root.
