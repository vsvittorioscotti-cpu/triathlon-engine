// Collaudo dello strato Supabase (login + sincronizzazione) con un finto backend in
// memoria che imita GoTrue e PostgREST quanto basta: filtri eq., order, limit, insert
// con return=representation, upsert on_conflict, patch e delete per id.
import { chromium } from "playwright";
import { readFileSync } from "node:fs";
import http from "node:http";
import { join } from "node:path";
import { URL } from "node:url";
import { randomUUID } from "node:crypto";

const site = "/home/claude/te/site";
function parseCsv(txt){ const rows=[];let row=[],cell="",q=false;
  for(let i=0;i<txt.length;i++){const c=txt[i];
    if(q){if(c==='"'){if(txt[i+1]==='"'){cell+='"';i++;}else q=false;}else cell+=c;}
    else if(c==='"')q=true;else if(c===","){row.push(cell);cell="";}
    else if(c==="\n"){row.push(cell);rows.push(row);row=[];cell="";}else if(c!=="\r")cell+=c;}
  if(cell.length||row.length){row.push(cell);rows.push(row);}
  const [h,...b]=rows;return b.filter(r=>r.length===h.length).map(r=>Object.fromEntries(h.map((k,i)=>[k,r[i]===""?null:r[i]])));}
const DB = {
  variante: parseCsv(readFileSync("/home/claude/te/csv/variante.csv","utf8")).sort((a,b)=>a.cod<b.cod?-1:1),
  workout_forza: parseCsv(readFileSync("/home/claude/te/csv/workout_forza.csv","utf8")),
  atleta:[], obiettivo:[], test:[], soglia:[], piano_versione:[], seduta_prescritta:[], seduta_eseguita:[], benessere:[], annotazione:[], decisione:[]
};
const PK = { benessere:["atleta_id","data"], annotazione:["atleta_id","chiave"] };
const USER = { id: randomUUID(), email:"vittorio@esempio.it", pw:"segreto1" };
const log = [];
const readBody = req => new Promise(res => { let d=""; req.on("data", c => d += c); req.on("end", () => res(d ? JSON.parse(d) : null)); });

function applyFilters(rows, sp){
  for (const [k, v] of sp.entries()){
    if (["select","order","limit","offset","on_conflict"].includes(k)) continue;
    const [op, ...rest] = v.split("."); const val = rest.join(".");
    if (op === "eq") rows = rows.filter(r => String(r[k]) === val);
  }
  const order = sp.get("order");
  if (order){ const keys = order.split(",").map(o => o.split(".")); rows = rows.slice().sort((a,b)=>{ for (const [k,d] of keys){ const x=a[k],y=b[k]; if (x==y) continue; return (x<y?-1:1)*(d==="desc"?-1:1);} return 0; }); }
  const off = +(sp.get("offset")||0), lim = +(sp.get("limit")||1000);
  return rows.slice(off, off+lim);
}
const srv = http.createServer(async (req,res)=>{
  const u = new URL(req.url, "http://x"); const json = (code, body) => { res.statusCode = code; res.setHeader("content-type","application/json"); res.end(JSON.stringify(body)); };
  if (u.pathname.startsWith("/auth/v1/")){
    const b = await readBody(req); log.push(`AUTH ${u.pathname}${u.search}`);
    const sess = { access_token:"tok-"+Date.now(), refresh_token:"ref", expires_in:3600, user:{id:USER.id, email:USER.email} };
    if (u.pathname.endsWith("/signup")) return json(200, sess);
    if (u.search.includes("password")) return (b.email===USER.email && b.password===USER.pw) ? json(200, sess) : json(400, {error_description:"Invalid login credentials"});
    if (u.search.includes("refresh_token")) return json(200, sess);
    return json(404, {});
  }
  if (u.pathname.startsWith("/rest/v1/")){
    const t = u.pathname.split("/").pop(); const sp = u.searchParams; const b = await readBody(req);
    const auth = req.headers.authorization || "";
    log.push(`${req.method} ${t}${u.search} ${auth.startsWith("Bearer tok")?"[user]":"[anon]"}`);
    if (!DB[t]) return json(404, {message:"tabella sconosciuta "+t});
    const isLib = ["variante","workout_forza"].includes(t);
    if (!isLib && !auth.startsWith("Bearer tok")) return json(200, []);   // RLS: anon non vede nulla
    if (req.method === "GET") return json(200, applyFilters(DB[t], sp));
    if (req.method === "POST"){
      const rows = Array.isArray(b) ? b : [b]; const out = [];
      for (const r of rows){
        const row = {...r, creato_il:new Date().toISOString()}; if (!row.id && !PK[t]) row.id = randomUUID();
        const pk = PK[t] || ["id"]; const i = DB[t].findIndex(x => pk.every(k => x[k] === row[k]));
        if (i >= 0){ if (!sp.get("on_conflict")) return json(409, {message:"duplicate key"}); DB[t][i] = {...DB[t][i], ...row}; out.push(DB[t][i]); }
        else { DB[t].push(row); out.push(row); }
      }
      return (req.headers.prefer||"").includes("representation") ? json(201, out) : (res.statusCode=201, res.end());
    }
    if (req.method === "PATCH"){ const id = (sp.get("id")||"").replace("eq.",""); const i = DB[t].findIndex(x=>x.id===id); if (i<0) return json(404,{}); DB[t][i] = {...DB[t][i], ...b}; res.statusCode=204; return res.end(); }
    if (req.method === "DELETE"){ const id = (sp.get("id")||"").replace("eq.",""); DB[t] = DB[t].filter(x=>x.id!==id); res.statusCode=204; return res.end(); }
  }
  const f = u.pathname === "/" ? "index.html" : u.pathname.slice(1);
  try { res.setHeader("content-type", f.endsWith(".js") ? "text/javascript" : "text/html"); res.end(readFileSync(join(site,f))); }
  catch { res.statusCode = 404; res.end("no"); }
}).listen(8767);

const browser = await chromium.launch({executablePath:"/opt/pw-browsers/chromium-1194/chrome-linux/chrome"});
const ctx = await browser.newContext({viewport:{width:1440,height:1000}});
const page = await ctx.newPage();
const errors = [];
page.on("pageerror", e => errors.push("PAGEERROR " + e.message));
page.on("console", m => { if (m.type()==="error" && !/fonts|ERR_TUNNEL|favicon/.test(m.text())) errors.push(m.text()); });
await page.addInitScript(() => { window.IRONMAN_REST = { url: "http://localhost:8767", key: "anon-test" }; });
await page.goto("http://localhost:8767/");
await page.waitForFunction(() => typeof libStato !== "undefined" && libStato === "caricate", null, {timeout: 20000});

// 1. prima del login: un paio di dati nel browser
await page.evaluate(() => { S.sessions.push({id:uid(), date:todayISO(), disc:"Bici", tipo:"Aerobico base", min:60, rpe:5, feel:"Buona", note:"locale", np:180});
  S.note[3] = "nota locale"; persist("sessions"); persist("config"); });
await page.waitForTimeout(300);
console.log("prima del login:", await page.evaluate(() => ({attivo: SB.attivo(), dot: document.getElementById("saveDot").textContent})));

// 2. login dal pannello Setup
await page.evaluate(() => { view = "setup"; render(); });
await page.fill("#sbEmail", USER.email); await page.fill("#sbPw", "sbagliata");
await page.click("#sbIn"); await page.waitForTimeout(400);
console.log("password sbagliata ->", await page.evaluate(() => document.getElementById("sbMsg").textContent));
await page.fill("#sbPw", USER.pw); await page.click("#sbIn");
await page.waitForFunction(() => SB.attivo(), null, {timeout: 10000});
await page.waitForTimeout(2500);
console.log("dopo il login:", await page.evaluate(() => ({ email: SB.email(), versione: SB.versione() && SB.versione().numero, dot: document.getElementById("saveDot").textContent, sessioni: S.sessions.length })));
console.log("tabelle:", Object.fromEntries(Object.entries(DB).filter(([k])=>!["variante","workout_forza"].includes(k)).map(([k,v])=>[k,v.length])));
console.log("prescritte:", DB.seduta_prescritta.slice(0,2));
console.log("eseguita:", DB.seduta_eseguita[0]);

// 3. modifiche: nuova sessione, modifica, cancellazione; test; benessere; cambio soglia e parametri
await page.evaluate(() => { S.sessions.push({id:uid(), date:todayISO(), disc:"Nuoto", tipo:"Tecnica", min:30, rpe:4, feel:"Buona", note:"", pace:110, dist:1200}); persist("sessions"); });
await page.waitForTimeout(1500);
await page.evaluate(() => { S.sessions[0].min = 45; S.sessions[0].tssOverride = 77; persist("sessions"); S.tests.push({id:uid(), date:todayISO(), tipo:"FTP bici — test 20'", val:230, unit:"W", note:"ok"}); persist("tests");
  S.body[todayISO()] = {peso:74.5, fcRip:47, hrv:65, sonno:7.5, qSonno:4, stress:2, fatica:2, motiv:5, note:"bene"}; persist("body");
  S.setup.ftp = 230; S.setup.oreDisponibili = 12; persist("config"); });
await page.waitForTimeout(2500);
await page.evaluate(() => { S.sessions = S.sessions.filter(s => s.disc !== "Nuoto"); persist("sessions"); });
await page.waitForTimeout(1500);
console.log("dopo le modifiche:", Object.fromEntries(Object.entries(DB).filter(([k])=>!["variante","workout_forza"].includes(k)).map(([k,v])=>[k,v.length])));
console.log("versioni:", DB.piano_versione.map(v=>[v.numero, v.esito, v.parametri.oreDisponibili]), "obiettivi:", DB.obiettivo.map(o=>[o.gradino,o.stato]));
console.log("soglie:", DB.soglia.map(s=>[s.disciplina,s.tipo,s.valore]), "benessere:", DB.benessere[0]);
console.log("eseguita modificata:", DB.seduta_eseguita.map(s=>[s.disciplina, s.durata_min, s.carico, s.carico_dichiarato]));
console.log("dot:", await page.evaluate(() => document.getElementById("saveDot").textContent), "errore:", await page.evaluate(() => SB.errore()));

// 4. ricarica la pagina: la sessione resta e i dati tornano dal database
await page.reload(); await page.waitForFunction(() => SB.attivo(), null, {timeout: 15000}); await page.waitForTimeout(1000);
console.log("dopo reload:", await page.evaluate(() => ({ email: SB.email(), sessioni: S.sessions.length, test: S.tests.length, body: Object.keys(S.body), ftp: S.setup.ftp, ore: S.setup.oreDisponibili, note: S.note, dot: document.getElementById("saveDot").textContent })));
await page.evaluate(() => { view = "setup"; render(); }); await page.waitForTimeout(300);
await page.screenshot({path:"/home/claude/te/artefatto/shot_auth_setup.png", fullPage:false});
console.log("errori:", errors);
console.log("richieste:", log.length);
await browser.close(); srv.close();
