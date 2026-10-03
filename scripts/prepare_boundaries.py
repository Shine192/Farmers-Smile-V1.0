"""Rebuild the browser boundary layer from the bundled Thailand province map."""
import json
from collections import Counter, defaultdict
from pathlib import Path
root=Path(__file__).resolve().parents[1]
source=root/"dist/data/thailand-districts.geojson"
data=json.loads(source.read_text())
features=data["features"]
country_outline=json.loads((root/"dist/data/thailand-country-outline.json").read_text())["coordinates"]
ids=("chiang-mai-valley","bang-klam","phunphin")
assert len(features)>=900, "Expected the Thailand district background map"
# The bundled ADM2 source contains separate places with duplicate district
# names. Earlier manual name-based grouping accidentally included these three
# distant polygons. Keep the genuine similarly named districts and leave only
# these misassigned source components disabled on the Thailand backdrop.
misplaced={
    ("chiang-mai-valley", "Chom Thong", (100.43,13.65,100.50,13.73)),
    ("phunphin", "Tha Chang", (100.34,14.73,100.43,14.83)),
    ("phunphin", "Wiang Sa", (100.34,18.32,101.12,18.80)),
}
def bbox(feature):
    geom=feature["geometry"]
    polygons=[geom["coordinates"]] if geom["type"]=="Polygon" else geom["coordinates"]
    points=[point for polygon in polygons for ring in polygon for point in ring]
    return (min(p[0] for p in points), min(p[1] for p in points), max(p[0] for p in points), max(p[1] for p in points))
for province_id, name, expected_bbox in misplaced:
    matches=[f for f in features if f["properties"].get("provinceId")==province_id and f["properties"].get("shapeName")==name and all(abs(a-b)<0.02 for a,b in zip(bbox(f),expected_bbox))]
    assert len(matches)==1, f"Expected one misplaced {name} component for {province_id}"
    matches[0]["properties"].pop("provinceId")
source.write_text(json.dumps(data,separators=(",",":")))
assert all(any(f["properties"].get("provinceId")==id for f in features) for id in ids)
outlines={}
for province_id in ids:
    edges=Counter()
    for feature in features:
        if feature["properties"].get("provinceId") != province_id:
            continue
        geom=feature["geometry"]
        polygons=[geom["coordinates"]] if geom["type"]=="Polygon" else geom["coordinates"]
        for polygon in polygons:
            for ring in polygon:
                for a,b in zip(ring,ring[1:]):
                    x=tuple(round(v,5) for v in a[:2]); y=tuple(round(v,5) for v in b[:2])
                    if x!=y: edges[tuple(sorted((x,y)))]+=1
    exposed=[edge for edge,count in edges.items() if count==1]
    adjacent=defaultdict(list)
    for x,y in exposed:
        adjacent[x].append(y); adjacent[y].append(x)
    paths=[]
    while adjacent:
        start=next(iter(adjacent)); path=[start]; prev=None; cur=start
        while True:
            choices=[p for p in adjacent.get(cur,[]) if p!=prev]
            if not choices: break
            nxt=choices[0]; adjacent[cur].remove(nxt); adjacent[nxt].remove(cur)
            if not adjacent[cur]: del adjacent[cur]
            if nxt in adjacent and not adjacent[nxt]: del adjacent[nxt]
            path.append(nxt); prev,cur=cur,nxt
            if cur==start: break
        if len(path)>2: paths.append(path)
    assert paths and all(path[0]==path[-1] for path in paths), f"Province outline is not closed: {province_id}"
    outlines[province_id]=paths
script="globalThis.THAILAND_DISTRICTS="+json.dumps(features,separators=(",",":"))+";globalThis.AREA_BOUNDARIES=Object.fromEntries("+json.dumps(ids)+".map(id=>[id,{type:\"FeatureCollection\",features:globalThis.THAILAND_DISTRICTS.filter(f=>f.properties.provinceId===id)}]));globalThis.PROVINCE_OUTLINES="+json.dumps(outlines,separators=(",",":"))+";globalThis.THAILAND_COUNTRY_OUTLINE="+json.dumps(country_outline,separators=(",",":"))+";\n"
(root/"dist/boundaries.js").write_text(script)
supported=[f for f in features if f["properties"].get("provinceId")]
(root/"dist/data/area-boundaries.geojson").write_text(json.dumps({"type":"FeatureCollection","features":supported},separators=(",",":")))
print(f"Rebuilt the Thailand map with {len(features)} province components, {len(supported)} enabled components and {sum(map(len,outlines.values()))} outline rings")
