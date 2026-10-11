// Collaudo locale della pagina con Chromium: librerie in cache, nessun connettore.
import { chromium } from "playwright";
import { readFileSync, writeFileSync } from "node:fs";
import http from "node:http";
import { join } from "node:path";

const dir = "/home/claude/te/artefatto";
function parseCsv(txt){ const rows=[];let row=[],cell="",q=false;
  for(let i=0;i<txt.length;i++){const c=txt[i];
    if(q){if(c==='"'){if(txt[i+1]==='"'){cell+='"';i++;}else q=false;}else cell+=c;}
    else if(c==='"')q=true;else if(c===","){row.push(cell);cell="";}
    else if(c==="\n"){row.push(cell);rows.push(row);row=[];cell="";}else if(c!=="\r")cell+=c;}
  if(cell.length||row.length){row.push(cell);rows.push(row);}
  const [h,...b]=rows;return b.filter(r=>r.length===h.length).map(r=>Object.fromEntries(h.map((k,i)=>[k,r[i]===""?null:r[i]])));}
const varianti = parseCsv(readFileSync("/home/claude/te/csv/variante.csv","utf8"));
const workouts = parseCsv(readFileSync("/home/claude/te/csv/workout_forza.csv","utf8"));
const LIBJSON = JSON.stringify({varianti, workouts, loadedAt:"2026-10-11T22:00:00.000Z", fonte:"test"});

const page_html = `<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"><style>:root{color-scheme:light}body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;background:#faf9f5;color:#141413}img{max-width:100%}[hidden]:not([hidden=until-found]){display:none!important}</style></head><body>` + readFileSync(join(dir,"ironman226.html"),"utf8") + "</body></html>";
const srv = http.createServer((req,res)=>{
  if (req.url.startsWith("/engine.js")) { res.setHeader("content-type","text/javascript"); res.end(readFileSync(join(dir,"engine.js"))); }
  else { res.setHeader("content-type","text/html"); res.end(page_html); }
}).listen(8765);

const browser = await chromium.launch({executablePath:"/opt/pw-browsers/chromium-1194/chrome-linux/chrome"});
const ctx = await browser.newContext({viewport:{width:1440,height:1000}});
const page = await ctx.newPage();
const errors = [];
page.on("console", m => { if (m.type()==="error") errors.push(m.text()); });
page.on("pageerror", e => errors.push("PAGEERROR " + e.message));
await page.addInitScript((lib) => { localStorage.setItem("ironman226.lib.v1", lib); }, LIBJSON);
await page.goto("http://localhost:8765/");
await page.waitForTimeout(1500);
const info = await page.evaluate(() => { const p = piano(); return {N:p.N, arrivo:p.scala&&p.scala.arrivo, sett:settimaneAllaGara(),
  blocchi:(p.blocchi||[]).map(b=>[b.A.gara,b.A.settimane,b.PIANO.length]), nonAss:p.scala&&p.scala.non_assorbite, intro:p.scala&&p.scala.intro,
  today: todayISO(), start: startDate()}; });
console.log(JSON.stringify(info));
for (const v of ["dashboard","forma","atp","calendario","diario","corpo","test","zone","setup"]) {
  await page.evaluate((v)=>{ view=v; if(v==="calendario") calWeek=20; render(); }, v);
  await page.waitForTimeout(300);
  await page.screenshot({path:`/home/claude/te/artefatto/shot_${v}.png`, fullPage: v!=="atp"});
}
// cambio setup: tetto rigido 20h, 52 settimane
await page.evaluate(()=>{ S.setup.oreDisponibili=20; S.setup.tettoRigido=true; S.setup.raceDate="2027-10-10"; PLAN_CACHE.key=null; view="atp"; render(); });
await page.waitForTimeout(300);
console.log(JSON.stringify(await page.evaluate(()=>{ const p=piano(); return {N:p.N, arrivo:p.scala.arrivo, vincolo:p.scala.vincolo, blocchi:p.blocchi.map(b=>[b.A.gara,b.A.settimane,b.PIANO.length, b.verifiche.filter(v=>v[1]==="OK").length])}; })));
await page.screenshot({path:`/home/claude/te/artefatto/shot_atp52.png`, fullPage:false});
console.log("errori console:", errors.length, errors.slice(0,5));
await browser.close(); srv.close();
