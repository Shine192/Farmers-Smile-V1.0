(function(root){
'use strict';
function createEngine(D){
const MONTHS=['January','February','March','April','May','June','July','August','September','October','November','December'];
const mean=a=>a.reduce((s,v)=>s+v,0)/a.length;
const quantile=(a,q)=>{let s=[...a].sort((a,b)=>a-b),i=(s.length-1)*q,l=Math.floor(i);return s[l]+(s[Math.ceil(i)]-s[l])*(i-l)};
function validate(month,water,location){if(!Number.isInteger(month)||month<1||month>12)throw Error('Choose a month from January to December.');if(!['rainfed','irrigated'].includes(water))throw Error('Choose how you water your farm.');if(location!==(D.meta.id||'chiang-mai-valley'))throw Error('Choose a supported reference area.');}
function matches(crop,month){
 const avg=D.monthly.filter(r=>r.month===month),temp=mean(avg.map(r=>r.temp)),rain=mean(avg.map(r=>r.rain)),s=D.analog.scales[month-1];
 return D.analog.windows.filter(w=>w.crop===crop.id&&w.month===month).map(w=>({...w,distance:Math.hypot((w.startTemp-temp)/s.temp,(w.startRain-rain)/s.rain)})).sort((a,b)=>a.distance-b.distance||a.year-b.year).slice(0,D.analog.k);
}
function assess(crop,month,water){
 const near=matches(crop,month),rain=mean(near.map(r=>r.rain)),temp=mean(near.map(r=>r.temp)),dry=mean(near.map(r=>r.drySpell));
 // Rain is gross precipitation, not effective crop water. This optimistic upper-bound
 // screen flags deficits; passing it does not establish adequate water or crop success.
 const startRain=mean(near.map(r=>r.startRain));
 const need=crop.water[0],gap=Math.max(0,1-rain/need),cold=Math.max(0,crop.temp[0]-temp),hot=Math.max(0,temp-crop.temp[1]);
 const below=near.filter(r=>r.rain<need).length;
 const tempPenalty=Math.min(1,(cold+hot)/6),dryPenalty=Math.min(1,dry/25);
 const startPenalty=Math.max(0,1-startRain/50);
 const penalty=(water==='rainfed'?gap*.65+below/near.length*.15+dryPenalty*(crop.drought==='medium-high'?.12:.08)+startPenalty*.3:0)+tempPenalty*.35;
 let status,level;
 if(tempPenalty>.5){status='Temperature needs a closer look';level='high'}
 else if(water==='rainfed'&&startRain<50){status='Wait for steadier rain';level='high'}
 else if(water==='rainfed'&&(gap>.25||below>=5)){status='Rain may not be enough';level='high'}
 else if(water==='rainfed'&&(below>=2||dry>=14)){status='Keep a water backup';level='medium'}
 else if(water==='irrigated'){status='Check your water supply';level='medium'}
 else{status='Worth considering';level='low'}
 let reasons=[];
 if(water==='rainfed'&&startRain<50)reasons.push('The starting month was usually dry in the matched years. Rain later in the season will not help seeds that dry out now.');
 if(water==='rainfed')reasons.push(below?`In ${below} of the ${near.length} similar past seasons, total rain was below this crop’s basic water guide.`:'Rain totals cleared the basic water guide in these similar past seasons. Dry spells can still cause problems.');
 else reasons.push('This comparison assumes you can add enough water throughout the season. Having a pump does not guarantee enough water.');
 reasons.push(cold+hot>0?'The season may be cooler or hotter than this crop prefers. Check a suitable local variety.':'The average warmth in similar past seasons was within this crop’s usual growing range.');
 reasons.push(crop.notes);
 const siteCaution=crop.elevationMin&&D.meta.gridElevationM<crop.elevationMin?`The reference weather point is ${Math.round(D.meta.gridElevationM)} m above sea level; this crop’s guide calls for sites above ${crop.elevationMin} m. Your farm may be higher, so check its exact elevation.`:null;
 if(siteCaution)reasons.push(siteCaution);
 const rating=Math.max(1,Math.min(5,Math.round((1-Math.min(1,penalty))*4+1)));
 return {id:crop.id,name:crop.name,thai:crop.thai,emoji:crop.emoji,days:crop.days,perennial:!!crop.perennial,waterGuide:crop.water,rating,siteCaution,rain,temp,dry,startRain,below,penalty,status,level,reasons,years:near.map(r=>r.year),rainRange:[quantile(near.map(r=>r.rain),.1),quantile(near.map(r=>r.rain),.9)],matches:near};
}
function compare({month=5,water='rainfed',location=D.meta.id||'chiang-mai-valley'}={}){
 validate(month,water,location);const started=performance.now();
 let crops=D.crops.map(c=>assess(c,month,water)).sort((a,b)=>a.penalty-b.penalty||a.id.localeCompare(b.id));
 const allRisky=crops.slice(0,3).every(c=>c.level==='high');
 for(const crop of crops){
   const alternatives=MONTHS.map((_,i)=>({month:i+1,...assess(D.crops.find(c=>c.id===crop.id),i+1,water)})).sort((a,b)=>a.penalty-b.penalty||a.month-b.month);
   // Group near-equal screens, not invented exact sowing dates.
   crop.months=alternatives.filter(c=>c.penalty<=alternatives[0].penalty+.06&&c.level!=='high').map(c=>c.month).sort((a,b)=>a-b);
 }
 const history=D.monthly.filter(r=>r.month===month),rain=mean(history.map(r=>r.rain)),temp=mean(history.map(r=>r.temp));
 crops=crops.slice(0,3);
 return {month,water,location,crops,allRisky,closeMatch:Math.abs(crops[0].penalty-crops[1].penalty)<.06,climate:{rain,temp,rainRange:[quantile(history.map(r=>r.rain),.1),quantile(history.map(r=>r.rain),.9)]},elapsedMs:performance.now()-started};
}
return {compare,MONTHS,matches};
}
root.CropEngine={...createEngine(root.CLIMATE_DATA),create:createEngine};if(typeof module!=='undefined')module.exports=root.CropEngine;
})(globalThis);
