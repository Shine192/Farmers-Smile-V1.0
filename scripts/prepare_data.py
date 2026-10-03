"""Rebuild the compact climate model and public datasets. Python 3, no packages.
Use --download to refresh the fixed 1996-2025 NASA POWER snapshot.
"""
import json, csv, calendar, math, statistics, hashlib, sys, os
from pathlib import Path
from datetime import date,timedelta
from urllib.request import urlopen
from urllib.parse import urlencode
ROOT=Path(__file__).resolve().parents[1]; AREA=os.environ.get('CROP_AREA','chiang-mai-valley'); NAME=os.environ.get('CROP_NAME','Chiang Mai valley'); LAT=float(os.environ.get('CROP_LAT','18.79')); LON=float(os.environ.get('CROP_LON','98.98')); D=ROOT/'dist'/'data'; D=D if AREA=='chiang-mai-valley' else D/AREA; D.mkdir(parents=True,exist_ok=True)
params=dict(parameters='T2M,T2M_MAX,PRECTOTCORR',community='AG',longitude=LON,latitude=LAT,start='19960101',end='20251231',format='JSON')
url='https://power.larc.nasa.gov/api/temporal/daily/point?'+urlencode(params)
p=D/'nasa-power-1996-2025.json'
if '--download' in sys.argv or not p.exists():
    with urlopen(url,timeout=120) as r:p.write_bytes(r.read())
raw=json.loads(p.read_text()); values=raw['properties']['parameter']
start=date(1996,1,1); end=date(2025,12,31)
keys=[(start+timedelta(days=i)).strftime('%Y%m%d') for i in range((end-start).days+1)]
assert all(set(values[k])==set(keys) for k in ('T2M','T2M_MAX','PRECTOTCORR'))
assert all(math.isfinite(v) and v!=raw['header']['fill_value'] for vs in values.values() for v in vs.values())
assert all(0<=v<1000 for v in values['PRECTOTCORR'].values())
rows=[]
with (D/'daily-weather.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['date','temperature_mean_c','temperature_max_c','rain_mm'])
 for k in keys:w.writerow([f'{k[:4]}-{k[4:6]}-{k[6:]}',values['T2M'][k],values['T2M_MAX'][k],values['PRECTOTCORR'][k]])
for year in range(1996,2026):
 for month in range(1,13):
  ks=[f'{year}{month:02}{day:02}' for day in range(1,calendar.monthrange(year,month)[1]+1)]
  dryrun=longest=0
  for k in ks:
   dryrun=dryrun+1 if values['PRECTOTCORR'][k]<1 else 0;longest=max(longest,dryrun)
  rows.append(dict(year=year,month=month,days=len(ks),temp=round(statistics.mean(values['T2M'][k] for k in ks),4),rain=round(sum(values['PRECTOTCORR'][k] for k in ks),4),dryDays=sum(values['PRECTOTCORR'][k]<1 for k in ks),hotDays=sum(values['T2M_MAX'][k]>=35 for k in ks),longestDry=longest))
with (D/'monthly-weather.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def fit(rs,field,kind):
 xs=[r['year'] for r in rs];ys=[r[field] for r in rs];xm=statistics.mean(xs);ym=statistics.mean(ys)
 slope=sum((x-xm)*(y-ym) for x,y in zip(xs,ys))/(sum((x-xm)**2 for x in xs)+100) if kind=='ridge' else 0
 return dict(center=xm,intercept=ym,slope=slope)
def predict(c,y,field):
 v=c['intercept']+c['slope']*(y-c['center']);return max(0,v) if field=='rain' else v
def errors(field,kind,years):
 es=[]
 for y in years:
  for m in range(1,13):
   train=[r for r in rows if r['year']<=y-2 and r['month']==m]
   target=next(r for r in rows if r['year']==y and r['month']==m)
   es.append(abs(predict(fit(train,field,kind),y,field)-target[field]))
 return statistics.mean(es)
models={};evaluation={}
for field in ('temp','rain'):
 val={k:errors(field,k,range(2016,2021)) for k in ('mean','ridge')}
 choice=min(val,key=val.get)
 models[field]={'kind':choice,'coefficients':[fit([r for r in rows if r['month']==m],field,choice) for m in range(1,13)]}
 evaluation[field]={'selected':choice,'selection_MAE_2016_2020':val,'holdout_MAE_2021_2025':{k:errors(field,k,range(2021,2026)) for k in ('mean','ridge')},'unit':'C' if field=='temp' else 'mm/month'}
# FAO ranges are indicative, not local variety calibration. Durations use published examples.
crops=[
 dict(id='soybean',name='Soybean',thai='ถั่วเหลือง',emoji='🫘',days=135,water=[450,700],temp=[20,33],absolute=[10,38],drought='low-medium',ecoId=1150,notes='Choose a variety suited to local day length. Check that water can drain away.'),
 dict(id='groundnut',name='Groundnut',thai='ถั่วลิสง',emoji='🥜',days=130,water=[500,700],temp=[22,32],absolute=[10,45],drought='low-medium',ecoId=2199,notes='Needs well-drained ground. Avoid fields where water collects.'),
 dict(id='maize',name='Maize',thai='ข้าวโพดเลี้ยงสัตว์',emoji='🌽',days=125,water=[500,800],temp=[18,33],absolute=[10,47],drought='medium-high',ecoId=2175,notes='Keep a water backup for flowering. This guide is for grain maize, not sweet corn.'),
 # Exploratory additions: water amounts are prorated from annual broad FAO Ecocrop
 # ranges by window length; these crops have no local outcome labels in this dataset.
 dict(id='strawberry',name='Strawberry',thai='สตรอว์เบอร์รี',emoji='🍓',days=240,water=[395,592],temp=[11,24],absolute=[6,28],drought='medium',ecoId=1112,elevationMin=1000,notes='Needs mild weather; FAO notes tropical production succeeds above 1,000 m. This reference weather point is lower. Check your exact farm elevation, variety, chilling needs, drainage, and irrigation. The water guide is a rough duration-scaled annual range, not a local field recommendation.'),
 dict(id='coffee',name='Arabica coffee',thai='กาแฟอาราบิก้า',emoji='☕',days=330,water=[1266,2082],temp=[14,28],absolute=[10,34],drought='high',ecoId=749,elevationMin=1000,notes='A long-term tree crop, not a one-season harvest. Site, variety, shade, soil, water through establishment, flowering, and processing access matter. FAO guidance prefers elevations above 1,000 m; this reference point is lower. The water guide is a rough duration-scaled annual range, not a local field recommendation.') ]
if AREA in ('bang-klam','phunphin'):
 crops += [
  dict(id='rubber',name='Rubber tree',thai='ยางพารา',emoji='🌳',days=365,water=[2000,4000],temp=[24,33],absolute=[10,45],drought='high',ecoId=1212,perennial=True,notes='Rubber is a long-term tree crop. A weather match cannot tell whether your soil, drainage, land, or chosen trees will suit it. It takes years before tapping begins.'),
  dict(id='oil-palm',name='Oil palm',thai='ปาล์มน้ำมัน',emoji='🌴',days=365,water=[1500,3000],temp=[20,35],absolute=[12,38],drought='high',ecoId=972,perennial=True,notes='Oil palm is a long-term tree crop. A weather match cannot tell whether your soil, drainage, water supply, or chosen seedlings will suit it. It takes years before harvest.'),
  dict(id='durian',name='Durian',thai='ทุเรียน',emoji='🍈',days=365,water=[1500,2500],temp=[22,40],absolute=[12,45],drought='high',ecoId=963,perennial=True,notes='Durian is a long-term fruit tree. A weather match cannot tell whether your soil, drainage, dry-season water, or chosen variety will suit it. It takes years before harvest.')]
(D/'crops.json').write_text(json.dumps(crops,ensure_ascii=False,indent=2))
meta={'id':AREA,'location':NAME,'latitude':LAT,'longitude':LON,'gridElevationM':raw['geometry']['coordinates'][2],'region':'south' if AREA in ('bang-klam','phunphin') else 'north','start':'1996-01-01','end':'2025-12-31','years':30,'dailyRecords':len(keys),'missingValues':0,'trainingMonths':len(rows),'sourceURL':url,'rawSHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'source':'NASA POWER / MERRA-2','retrieved':'2026-09-23','planningYear':2027,'scope':'One coarse grid reference, not farm-level measurements or local microclimates.'}
# Round only for compact deployment, after fitting/evaluation.
model={'meta':meta,'models':models,'monthly':rows,'evaluation':evaluation,'crops':crops}
(D/'model.json').write_text(json.dumps(model,ensure_ascii=False,separators=(',',':')))
(D/'bundle.js').write_text('globalThis.CLIMATE_DATA='+json.dumps(model,ensure_ascii=False,separators=(',',':'))+';\n')
(D/'validation.json').write_text(json.dumps({'dataChecks':meta,'forecastEvaluation':evaluation,'method':'Monthly ridge regression vs monthly mean. Lambda=100 fixed. Expanding-window two-year-ahead predictions. Model choice on 2016-2020 only; subsequent 2021-2025 comparison is an evaluation, not a new selection step. Final models refit through 2025. Crop ranking has no field outcome validation.','modelJSONBytes':(D/'model.json').stat().st_size,'coefficientBytes':len(json.dumps(models,separators=(',',':')).encode())},indent=2))
print(json.dumps({'records':len(keys),'evaluation':evaluation,'coefficientBytes':len(json.dumps(models,separators=(',',':')).encode())},indent=2))
# Instance-based ML: standardized nearest-neighbor retrieval of complete historical
# crop windows. Crop outcomes are NOT training labels. Daily records are aggregated
# without treating annual rainfall as crop-season water availability.
windows=[]
for c in crops:
 for y in range(1996,2026):
  for m in range(1,13):
   begin=date(y,m,1);finish=begin+timedelta(days=c['days']-1)
   if finish>end:continue
   ks=[(begin+timedelta(days=i)).strftime('%Y%m%d') for i in range(c['days'])]
   dry=longest=0
   for k in ks:
    dry=dry+1 if values['PRECTOTCORR'][k]<1 else 0;longest=max(longest,dry)
   windows.append(dict(crop=c['id'],year=y,month=m,rain=round(sum(values['PRECTOTCORR'][k] for k in ks),2),temp=round(statistics.mean(values['T2M'][k] for k in ks),3),drySpell=longest,hotDays=sum(values['T2M_MAX'][k]>=35 for k in ks),startRain=next(r['rain'] for r in rows if r['year']==y and r['month']==m),startTemp=next(r['temp'] for r in rows if r['year']==y and r['month']==m)))
scales=[dict(temp=max(.1,statistics.pstdev(r['temp'] for r in rows if r['month']==m)),rain=max(1,statistics.pstdev(r['rain'] for r in rows if r['month']==m))) for m in range(1,13)]
model['analog']={'method':'standardized k-nearest-neighbor historical-season retrieval','k':7,'features':['startTemp','startRain'],'scales':scales,'windows':windows,'claim':'Retrieves similar historical growing seasons. Not validated as a seasonal forecast or crop-outcome predictor.'}
(D/'model.json').write_text(json.dumps(model,ensure_ascii=False,separators=(',',':')))
(D/'bundle.js').write_text('globalThis.CLIMATE_DATA='+json.dumps(model,ensure_ascii=False,separators=(',',':'))+';\n')
(D/'historical-crop-windows.json').write_text(json.dumps(windows,separators=(',',':')))
validation=json.loads((D/'validation.json').read_text());validation['modelJSONBytes']=(D/'model.json').stat().st_size;validation['analogModelBytes']=len(json.dumps(model['analog'],separators=(',',':')).encode());validation['analogWindows']=len(windows)
(D/'validation.json').write_text(json.dumps(validation,indent=2))
print('Historical crop windows:',len(windows),'Model bundle bytes:',validation['modelJSONBytes'])

if AREA=='chiang-mai-valley': (ROOT/'dist'/'data.js').write_text((D/'bundle.js').read_text())
