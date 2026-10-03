# Source register — retrieved September 23, 2026

## Historical weather
NASA POWER daily point API. Coordinates 18.79 N, 98.98 E; 1996-01-01 through 2025-12-31; T2M, T2M_MAX, PRECTOTCORR; agricultural community; JSON output. Raw response and hash included. NASA POWER / MERRA-2 data are gridded, not a local weather-station observation.

- Documentation: https://power.larc.nasa.gov/docs/services/api/temporal/daily/
- Data background: https://power.larc.nasa.gov/docs/faqs/data/
- Exact request: https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M%2CT2M_MAX%2CPRECTOTCORR&community=AG&longitude=98.98&latitude=18.79&start=19960101&end=20251231&format=JSON

## Crop screening inputs
FAO Irrigation Water Management, Chapter 3: Crop Water Needs. Table 7 provides example growing periods and table 14 provides indicative seasonal water requirements. These are not rainfall guarantees or calibrated crop models.

https://www.fao.org/4/s2022e/s2022e07.htm

FAO Ecocrop broad temperature ranges:
- Grain maize (Zea mays): https://ecocrop.apps.fao.org/ecocrop/srv/en/dataSheet?id=2175
- Soybean (Glycine max): https://ecocrop.apps.fao.org/ecocrop/srv/en/dataSheet?id=1150
- Groundnut (Arachis hypogaea): https://ecocrop.apps.fao.org/ecocrop/srv/en/dataSheet?id=2199

## Local relevance, not crop-variety calibration
Chiang Mai Provincial Agricultural Extension Office crop calendar lists maize and soybean. Its seasonal calendar is not automatically encoded into the model: https://chiangmai.doae.go.th/crop-calendar/

Chiang Mai government agricultural development project describes groundnut and Chiang Mai 60 soybean cultivation: https://www.chiangmai.go.th/project/nasiri/nasiri_activity_agi.html

These local sources support a narrow crop selection; they do not validate the prototype's chosen durations, thresholds, weather grid, or recommendations on a user's farm.

## Rights and attribution
Preserve the original source attribution with downloaded data. We include the original NASA API response and our derived tables, plus small structured crop facts and links. We do not bundle copies of full third-party articles or manuals. Review upstream terms before commercial redistribution or a production launch. The crop photo set includes licensed Wikimedia photographs and AI-generated photo-realistic examples for rubber, oil palm, and durian. The current map uses bundled Thai administrative geometry without a tile basemap, including in the standalone offline app.

## Crop photographs
<details><summary>Crop photo credits</summary><p>Maize: <a href="https://commons.wikimedia.org/wiki/File:Yellow_Corn_on_the_Cob_(35115370841).jpg">Willis Lam</a>, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC BY-SA 2.0</a>.</p><p>Soybean: <a href="https://commons.wikimedia.org/wiki/File:Glycine_max_003.JPG">H. Zell</a>; groundnut: <a href="https://commons.wikimedia.org/wiki/File:Arachis-hypogaea-(peanuts).jpg">Texnik</a>. Both <a href="https://creativecommons.org/licenses/by-sa/3.0/">CC BY-SA 3.0</a>.</p><p class="small-note">Photographs resized and displayed with cropping. These photos illustrate crops; they are not photos of farms in the selected area. Photo adaptations retain their respective licenses.</p></details>


## Strawberry and Arabica coffee screening sources
- FAO Ecocrop strawberry (Fragaria × ananassa), species guide, mild conditions and tropical production above 1,000 m: https://ecocrop.apps.fao.org/ecocrop/srv/en/cropView?id=1112 and environmental ranges: https://ecocrop.apps.fao.org/ecocrop/srv/en/dataSheet?id=1112
- FAO Ecocrop Arabica coffee (Coffea arabica), temperature and annual rainfall ranges: https://ecocrop.apps.fao.org/ecocrop/srv/en/dataSheet?id=749
- FAO Arabica Coffee Manual for Lao PDR: altitude, temperature, rainfall distribution, site and long-term crop considerations: https://www.fao.org/4/ae939e/ae939e03.htm
These are broad species-level references, not local yield data. The UI marks both additions as exploratory. Their seasonal water guides are the FAO annual broad range prorated to the weather-window length as a rough comparison. Coffee is a long-lived tree; its displayed window describes weather conditions, not time to first harvest. The area weather reference points are below 1,000 m; farms at higher elevations can differ from these measurements.

## Added crop photos
- Strawberry: Bruce Dupree / Alabama Extension, CC0 1.0: https://commons.wikimedia.org/wiki/File:Strawberry_Plant_with_Fruit_(close-up).jpg
- Arabica coffee cherries: Roger Burger, CC0 1.0: https://commons.wikimedia.org/wiki/File:Coffee_arabica_cherry.jpg

## Thailand province selection map
The Thailand backdrop is based on geoBoundaries THA ADM2 district geometry, boundary ID THA-ADM2-78962969, reference year 2019. Source: Royal Thai Survey Department / OCHA ROAP. License in the dataset metadata: Creative Commons Attribution 3.0 Intergovernmental Organisations (CC BY 3.0 IGO). Full district geometries are simplified for a compact overview; internal district edges are hidden in the location picker. The 25 Chiang Mai, 16 Songkhla, and 19 Surat Thani districts are grouped into three green province regions. Gray regions are inactive. Map markers show reference locations, not farm plots.

- Repository: https://github.com/wmgeolab/geoBoundaries/tree/main/releaseData/gbOpen/THA/ADM2
- License: https://creativecommons.org/licenses/by/3.0/igo/
- Original dataset: https://data.humdata.org/dataset/thailand-administrative-boundaries
- Chiang Mai district membership: Tourism Authority of Thailand: https://thai.tourismthailand.org/Destinations/Provinces/chiang-mai/101
- Surat Thani membership cross-check: Tourism Authority of Thailand: https://api.tat.or.th/upload/live/multimedia/9359/ESuratthani.pdf
- Songkhla district membership: https://en.wikipedia.org/wiki/Songkhla_province

The grouped component shapes are in `dist/data/area-boundaries.geojson`; the complete muted Thailand backdrop is in `dist/data/thailand-districts.geojson`. `scripts/prepare_boundaries.py` rebuilds the browser layer from that bundled file.

## Crop photographs
<details><summary>Crop photo credits</summary><p>Maize: <a href="https://commons.wikimedia.org/wiki/File:Yellow_Corn_on_the_Cob_(35115370841).jpg">Willis Lam</a>, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC BY-SA 2.0</a>.</p><p>Soybean: <a href="https://commons.wikimedia.org/wiki/File:Glycine_max_003.JPG">H. Zell</a>; groundnut: <a href="https://commons.wikimedia.org/wiki/File:Arachis-hypogaea-(peanuts).jpg">Texnik</a>. Both <a href="https://creativecommons.org/licenses/by-sa/3.0/">CC BY-SA 3.0</a>.</p><p class="small-note">Photographs resized and displayed with cropping. These photos illustrate crops; they are not photos of farms in the selected area. Photo adaptations retain their respective licenses.</p></details>


## Strawberry and Arabica coffee screening sources
- FAO Ecocrop strawberry (Fragaria × ananassa), species guide, mild conditions and tropical production above 1,000 m: https://ecocrop.apps.fao.org/ecocrop/srv/en/cropView?id=1112 and environmental ranges: https://ecocrop.apps.fao.org/ecocrop/srv/en/dataSheet?id=1112
- FAO Ecocrop Arabica coffee (Coffea arabica), temperature and annual rainfall ranges: https://ecocrop.apps.fao.org/ecocrop/srv/en/dataSheet?id=749
- FAO Arabica Coffee Manual for Lao PDR: altitude, temperature, rainfall distribution, site and long-term crop considerations: https://www.fao.org/4/ae939e/ae939e03.htm
These are broad species-level references, not local yield data. The UI marks both additions as exploratory. Their seasonal water guides are the FAO annual broad range prorated to the weather-window length as a rough comparison. Coffee is a long-lived tree; its displayed window describes weather conditions, not time to first harvest. District weather anchors are below 1,000 m; some farms in each large district may be higher.

## Added crop photos
- Strawberry: Bruce Dupree / Alabama Extension, CC0 1.0: https://commons.wikimedia.org/wiki/File:Strawberry_Plant_with_Fruit_(close-up).jpg
- Arabica coffee cherries: Roger Burger, CC0 1.0: https://commons.wikimedia.org/wiki/File:Coffee_arabica_cherry.jpg

## Southern Thailand reference areas and crop screens
Separate NASA POWER daily requests cover Songkhla city (7.1896, 100.5951) and Surat Thani city (9.1382, 99.3217), 1996–2025; exact requests, raw responses and hashes are bundled in each province folder. They are representative grid points only; they do not define province boundaries or farm conditions.

FAO Ecocrop broad climate sheets used for perennial exploratory screens:
- Rubber tree (Hevea brasiliensis): https://ecocrop.apps.fao.org/ecocrop/srv/en/dataSheet?id=1212
- Oil palm (Elaeis guineensis): https://ecocrop.apps.fao.org/ecocrop/srv/en/dataSheet?id=972
- Durian (Durio zibethinus): https://ecocrop.apps.fao.org/ecocrop/srv/en/dataSheet?id=963
These list broad species-level rainfall and temperature ranges and perennial life cycles. The app uses those ranges as screening inputs only; they are not locally calibrated crop prescriptions.

Local-use context is based on Thailand's Office of Agricultural Economics (OAE) official statistics. Its agricultural statistics report province-level para-rubber and oil-palm area and output; OAE also publishes province-level durian production statistics. These support including these crops as regional options, not claims about any individual farm:
- Agricultural Statistics of Thailand, province tables: https://catalog.oae.go.th/en/dataset/ba103542-830f-418a-b614-9645ebbe1a93
- OAE durian production data, province series: https://catalog.oae.go.th/en/dataset/durian_product
- OAE oil palm production data: https://catalog.oae.go.th/en/dataset/dataoae1504
- OAE para-rubber production data: https://catalog.oae.go.th/dataset/groups/dataoae1404

## Top-three rating
The app ranks each area's full crop screen by the existing rain and temperature mismatch penalty, then displays only the top three. Its star rating is a readable transformation of that rule-based penalty. It is not trained on yield outcomes, a probability of success, or a forecast. Southern perennial crops use 365-day weather windows; planting month selects the start of the comparison window and does not represent time to first harvest.


## Province selection map
The available province fills are grouped from Royal Thai Survey Department/OCHA ROAP district boundary geometry (geoBoundaries THA ADM2, CC BY 3.0 IGO). The district-level edges are hidden in the location picker so the map reads as province regions. The enabled districts are grouped into Chiang Mai, Songkhla, and Surat Thani using their administrative membership; disabled areas are shown in gray. Province map markers are reference locations, not farm boundaries.

Province membership cross-checks: Tourism Authority of Thailand, Chiang Mai province overview (25 districts): https://thai.tourismthailand.org/Destinations/Provinces/chiang-mai/101 ; Surat Thani provincial overview: https://api.tat.or.th/upload/live/multimedia/9359/ESuratthani.pdf ; Songkhla district list: https://en.wikipedia.org/wiki/Songkhla_province . The Southern weather models remain coarse nearby grid references rather than province-wide climate averages.


## Soil-map reference (not integrated into Version 1.0)
The Land Development Department’s 1:25,000 soil-group map is a reference for soil-resource and land-use planning. The official dataset description lists soil properties such as texture, drainage, fertility, and depth. The current app does not link to, download, embed, or aggregate this data, and does not use soil data in recommendations. These sources are recorded for possible future development. Field-level soil and drainage still need local checking.

- LDD interactive soil-group map (online): https://sql.ldd.go.th/ldddata/mapsoilA1.html
- Thailand Open Government Data, soil-series 1:25,000 dataset: https://www.data.go.th/dataset/soilseries25000
- LDD soil-group dataset description: https://lddcatalog.ldd.go.th/en/dataset/oss01
