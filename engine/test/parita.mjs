// Test di parità: il motore TS deve riprodurre gli output di scala_gen.py e
// generatore.py sugli stessi input. I riferimenti stanno in test/ref/ e si
// rigenerano con `python3 test/genera_ref.py` dalla radice del repo.
import { readFileSync, readdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const qui = dirname(fileURLToPath(import.meta.url));
const E = await import(join(qui, "..", "dist", "engine.mjs"));

// ---- CSV minimale con virgolette (quello che scrive csv.DictWriter) ----
function parseCsv(txt) {
  const rows = []; let row = [], cell = "", q = false;
  for (let i = 0; i < txt.length; i++) {
    const c = txt[i];
    if (q) {
      if (c === '"') { if (txt[i + 1] === '"') { cell += '"'; i++; } else q = false; }
      else cell += c;
    } else if (c === '"') q = true;
    else if (c === ",") { row.push(cell); cell = ""; }
    else if (c === "\n") { row.push(cell); rows.push(row); row = []; cell = ""; }
    else if (c !== "\r") cell += c;
  }
  if (cell.length || row.length) { row.push(cell); rows.push(row); }
  const [h, ...body] = rows;
  return body.filter((r) => r.length === h.length).map((r) => Object.fromEntries(h.map((k, i) => [k, r[i] === "" ? null : r[i]])));
}
const csvDir = join(qui, "..", "..", "csv");
const VARIANTI = parseCsv(readFileSync(join(csvDir, "variante.csv"), "utf8"));
const WORKOUTS = parseCsv(readFileSync(join(csvDir, "workout_forza.csv"), "utf8"));

// ---- confronto ----
let errori = 0, confronti = 0;
const norm = (s) => String(s).replace(/(\d)\.0\b/g, "$1");
function eq(a, b, path, tol = 1e-9) {
  confronti++;
  if (typeof a === "number" && typeof b === "number") {
    if (Number.isNaN(a) && Number.isNaN(b)) return;
    const d = Math.abs(a - b);
    if (d > tol * Math.max(1, Math.abs(a), Math.abs(b))) fail(path, a, b);
    return;
  }
  if (Array.isArray(a) && Array.isArray(b)) {
    if (a.length !== b.length) return fail(path + ".length", a.length, b.length);
    a.forEach((x, i) => eq(x, b[i], `${path}[${i}]`, tol));
    return;
  }
  if (a && b && typeof a === "object" && typeof b === "object") {
    for (const k of Object.keys(b)) eq(a[k], b[k], `${path}.${k}`, tol);
    return;
  }
  if (typeof a === "string" && typeof b === "string") { if (norm(a) !== norm(b)) fail(path, a, b); return; }
  if (a === null && b === undefined) return;
  if (a !== b) fail(path, a, b);
}
function fail(path, a, b) {
  errori++;
  if (errori <= 40) console.log(`  DIFF ${path}: ts=${JSON.stringify(a)} py=${JSON.stringify(b)}`);
}

// ---- livello 1 ----
const refScala = JSON.parse(readFileSync(join(qui, "ref", "scala.json"), "utf8"));
console.log("Livello 1 — scala");
for (const [nome, caso] of Object.entries(refScala)) {
  const i = caso.input;
  const p = E.livelloScala(i.gradino_fatto, i.settimane, i.ore_disponibili, i.ore_oggi, i.obiettivo, i.tetto_rigido);
  const prima = errori;
  eq(p, caso.piano, `${nome}.piano`);
  if (!E.isErrore(p)) {
    eq(E.fabbisognoOre(p), caso.fabbisogno, `${nome}.fabbisogno`);
    eq(E.verificaI8(p, i.gradino_fatto, i.obiettivo), caso.verifiche, `${nome}.verifiche`);
  }
  console.log(`  ${errori === prima ? "ok " : "ERR"} ${nome}`);
}

// ---- livello 2 ----
console.log("Livello 2 — generatore");
for (const f of readdirSync(join(qui, "ref")).filter((f) => f.startsWith("piano_")).sort()) {
  const ref = JSON.parse(readFileSync(join(qui, "ref", f), "utf8"));
  const prima = errori;
  const out = E.generaBlocco(ref.A, E.normalizzaVarianti(VARIANTI), E.normalizzaWorkout(WORKOUTS));
  eq(out.NB, ref.NB, `${f}.NB`); eq(out.TAPER_DA, ref.TAPER_DA, `${f}.TAPER_DA`);
  eq(out.W, ref.W, `${f}.W`);
  eq(out.PIANO, ref.PIANO, `${f}.PIANO`);
  const V = out.verifiche.map(([reg, es, dt]) => `${es.padEnd(8)} ${reg.padEnd(28)} ${dt}`.trim());
  eq(V.map((s) => s.replace(/\s+/g, " ")), ref.V.map((s) => s.replace(/\s+/g, " ")), `${f}.V`);
  console.log(`  ${errori === prima ? "ok " : "ERR"} ${f.replace(/^piano_|\.json$/g, "")}  ${out.PIANO.length} sedute, ${out.verifiche.filter((v) => v[1] === "OK").length}/${out.verifiche.length} regole`);
}

console.log(`\n${confronti} confronti, ${errori} differenze`);
process.exit(errori ? 1 : 0);
