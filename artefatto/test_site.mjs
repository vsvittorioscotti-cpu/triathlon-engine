// Collaudo della pagina statica (site/index.html) con un finto endpoint REST di
// Supabase servito in locale: verifica il caricamento paginato via fetch.
import { chromium } from "playwright";
import { readFileSync } from "node:fs";
import http from "node:http";
import { join } from "node:path";
import { URL } from "node:url";

const site = "/home/claude/te/site";
function parseCsv(txt){ const rows=[];let row=[],cell="",q=false;
  for(let i=0;i<txt.length;i++){const c=txt[i];
    if(q){if(c==='"'){if(txt[i+1]==='"'){cell+='"';i++;}else q=false;}else cell+=c;}
    else if(c==='"')q=true;else if(c===","){row.push(cell);cell="";}
    else if(c==="\n"){row.push(cell);rows.push(row);row=[];cell="";}else if(c!=="\r")cell+=c;}
  if(cell.length||row.length){row.push(cell);rows.push(row);}
  const [h,...b]=rows;return b.filter(r=>r.length===h.length).map(r=>Object.fromEntries(h.map((k,i)=>[k,r[i]===""?null:r[i]])));}
const varianti = parseCsv(readFileSync("/home/claude/te/csv/variante.csv","utf8")).sort((a,b)=>a.cod<b.cod?-1:1);
const workouts = parseCsv(readFileSync("/home/claude/te/csv/workout_forza.csv","utf8"));
let calls = [];
const srv = http.createServer((req,res)=>{
  const u = new URL(req.url, "http://x");
  if (u.pathname.startsWith("/rest/v1/")){
    calls.push(u.pathname + u.search + " apikey=" + (req.headers.apikey||"").slice(0,14));
    const t = u.pathname.split("/").pop();
    const limit = +(u.searchParams.get("limit")||100000), off = +(u.searchParams.get("offset")||0);
    const rows = (t==="variante" ? varianti : workouts).slice(off, off+limit);
    res.setHeader("content-type","application/json"); res.end(JSON.stringify(rows)); return;
  }
  const f = u.pathname === "/" ? "index.html" : u.pathname.slice(1);
  try { res.setHeader("content-type", f.endsWith(".js") ? "text/javascript" : "text/html"); res.end(readFileSync(join(site,f))); }
  catch { res.statusCode = 404; res.end("no"); }
}).listen(8766);

const browser = await chromium.launch({executablePath:"/opt/pw-browsers/chromium-1194/chrome-linux/chrome"});
const page = await (await browser.newContext({viewport:{width:1440,height:1000}})).newPage();
const errors = [];
page.on("pageerror", e => errors.push("PAGEERROR " + e.message));
page.on("console", m => { if (m.type()==="error" && !/fonts|ERR_TUNNEL/.test(m.text())) errors.push(m.text()); });
await page.addInitScript(() => { window.IRONMAN_REST = { url: "http://localhost:8766", key: "sb_publishable_TEST" }; });
await page.goto("http://localhost:8766/");
await page.waitForFunction(() => typeof libStato !== "undefined" && (libStato === "caricate" || libStato === "errore"), null, {timeout: 20000});
const info = await page.evaluate(() => ({ libStato, libErrore, fonte: LIB.fonte, nv: LIB.varianti && LIB.varianti.length, nw: LIB.workouts && LIB.workouts.length,
  piano: (p => p.weeks ? {N:p.N, arrivo:p.scala.arrivo, sedute:p.blocchi.map(b=>b.PIANO.length)} : p)(piano()) }));
console.log(JSON.stringify(info));
console.log("chiamate REST:", calls.length); calls.forEach(c => console.log("  " + c));
await page.evaluate(()=>{ view="setup"; render(); });
await page.waitForTimeout(300);
await page.screenshot({path:"/home/claude/te/artefatto/shot_site_setup.png", fullPage:false});
console.log("errori:", errors);
await browser.close(); srv.close();
