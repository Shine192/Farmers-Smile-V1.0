"""Embed the browser app into one offline HTML file; package reproducible source."""
from pathlib import Path
import re,zipfile,json,base64
root=Path(__file__).resolve().parents[1];dist=root/'dist'
models={k:json.loads((dist/'data'/k/'model.json').read_text()) for k in ['bang-klam','phunphin']}
(dist/'areas.js').write_text('globalThis.AREA_MODELS={"chiang-mai-valley":globalThis.CLIMATE_DATA,...'+json.dumps(models,ensure_ascii=False,separators=(',',':'))+'};\n')
html=(dist/'index.html').read_text()
html=html.replace('<link rel="stylesheet" href="styles.css">','<style>\n'+(dist/'styles.css').read_text()+'\n</style>')
html=html.replace('<link rel="stylesheet" href="vendor/leaflet.css">','<style>\n'+(dist/'vendor/leaflet.css').read_text()+'\n</style>')
for name in ('vendor/leaflet.js','data.js','areas.js','boundaries.js','engine.js','app.js'):
 html=html.replace(f'<script src="{name}"></script>','<script>\n'+(dist/name).read_text()+'\n</script>')
photos={p.stem:'data:image/jpeg;base64,'+base64.b64encode(p.read_bytes()).decode() for p in (dist/'photos').glob('*.jpg')}
html=html.replace('<script>\n(function(){', '<script>globalThis.OFFLINE_PHOTOS='+json.dumps(photos)+';</script><script>\n(function(){')
(dist/'offline.html').write_text(html)
for name in ('README.md','SOURCES.md'):(dist/name).write_text((root/name).read_text())
with zipfile.ZipFile(dist/'Farmers-Smile-Project.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(root.rglob('*')):
  rel=p.relative_to(root)
  if not p.is_file() or any(part.startswith('.') or part=='__pycache__' for part in rel.parts) or p.suffix in ('.zip','.pyc'):continue
  if rel.parts[0] not in ('dist','scripts') and str(rel) not in ('README.md','SOURCES.md','requirements.txt','package.json','package-lock.json','vite.config.js'):continue
  z.write(p,str(rel))
print('Offline HTML:',(dist/'offline.html').stat().st_size,'bytes; project ZIP:',(dist/'Farmers-Smile-Project.zip').stat().st_size,'bytes')
