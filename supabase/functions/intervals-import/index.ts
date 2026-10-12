// intervals-import — porta le attività di intervals.icu in seduta_eseguita (C7: il
// terzo scrittore, "dispositivo"). Si chiama dalla pagina con il token dell'utente;
// la funzione risale all'atleta, legge il suo collegamento (chiave API), interroga
// intervals.icu e scrive con il ruolo di servizio. Idempotente su (esterno_fonte,
// esterno_id): ripetere l'import aggiorna, non duplica.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const json = (code: number, body: unknown) =>
  new Response(JSON.stringify(body), { status: code, headers: { ...CORS, "Content-Type": "application/json" } });

// tipo di attività intervals.icu -> disciplina del contratto
function disciplina(tipo: string): string {
  const t = (tipo || "").toLowerCase();
  if (t.includes("swim")) return "Nuoto";
  if (t.includes("ride") || t.includes("bike") || t.includes("cycl") || t === "velomobile") return "Ciclismo";
  if (t.includes("run") || t === "hike" || t === "walk") return t === "walk" || t === "hike" ? "Altro" : "Corsa";
  if (t.includes("weight") || t.includes("strength") || t === "crossfit" || t === "pilates" || t === "yoga") return "Forza";
  return "Altro";
}
const FEEL: Record<number, string> = { 1: "Ottima", 2: "Buona", 3: "Normale", 4: "Scarsa", 5: "Pessima" };
const giorno = (d: Date) => d.toISOString().slice(0, 10);

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return json(405, { errore: "solo POST" });
  const auth = req.headers.get("Authorization") || "";
  if (!auth.startsWith("Bearer ")) return json(401, { errore: "token mancante" });

  const url = Deno.env.get("SUPABASE_URL")!;
  const anon = Deno.env.get("SUPABASE_ANON_KEY")!;
  const service = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
  const asUser = createClient(url, anon, { global: { headers: { Authorization: auth } } });
  const { data: { user }, error: eu } = await asUser.auth.getUser();
  if (eu || !user) return json(401, { errore: "utente non riconosciuto" });

  const db = createClient(url, service);
  const { data: atleta } = await db.from("atleta").select("id").eq("user_id", user.id).maybeSingle();
  if (!atleta) return json(404, { errore: "atleta non trovato" });
  const { data: col } = await db.from("collegamento_intervals").select("*").eq("atleta_id", atleta.id).maybeSingle();
  if (!col) return json(400, { errore: "intervals.icu non collegato: salva athlete id e chiave API nel Setup" });

  let body: { oldest?: string; newest?: string } = {};
  try { body = await req.json(); } catch { /* corpo vuoto */ }
  const oggi = new Date();
  const newest = body.newest || giorno(oggi);
  let oldest = body.oldest;
  if (!oldest) {
    const base = col.ultimo_import ? new Date(col.ultimo_import) : new Date(oggi.getTime() - 90 * 86400000);
    oldest = giorno(new Date(base.getTime() - 7 * 86400000)); // una settimana di sovrapposizione: le attività si rivedono
  }

  // intervals.icu: Basic auth con utente API_KEY
  const cred = btoa(`API_KEY:${col.api_key}`);
  const r = await fetch(`https://intervals.icu/api/v1/athlete/${encodeURIComponent(col.athlete_id || "0")}/activities?oldest=${oldest}&newest=${newest}`,
    { headers: { Authorization: `Basic ${cred}`, "User-Agent": "Mozilla/5.0 triathlon-engine" } });
  if (!r.ok) {
    const txt = (await r.text()).slice(0, 200);
    await db.from("collegamento_intervals").update({ ultimo_esito: `errore ${r.status}: ${txt}`, aggiornato_il: new Date().toISOString() }).eq("atleta_id", atleta.id);
    return json(502, { errore: `intervals.icu ha risposto ${r.status}`, dettaglio: txt });
  }
  const attivita: any[] = await r.json();

  // sedute prescritte della versione corrente, per collegare l'eseguito al prescritto (C1)
  const { data: ver } = await db.from("piano_versione").select("id").eq("atleta_id", atleta.id).order("numero", { ascending: false }).limit(1).maybeSingle();
  const prescritte: Record<string, { id: string; disciplina: string }[]> = {};
  if (ver) {
    const { data: pr } = await db.from("seduta_prescritta").select("id,data,disciplina").eq("versione_id", ver.id).gte("data", oldest).lte("data", newest);
    for (const p of pr || []) (prescritte[p.data] ||= []).push(p);
  }
  const { data: giaCollegate } = await db.from("seduta_eseguita").select("prescritta_id").eq("atleta_id", atleta.id).not("prescritta_id", "is", null);
  const usate = new Set((giaCollegate || []).map((x: any) => x.prescritta_id));

  const righe = attivita.map((a) => {
    const disc = disciplina(a.type);
    const data = String(a.start_date_local || a.start_date || "").slice(0, 10);
    const sec = a.moving_time || a.elapsed_time || 0;
    const dist = a.distance || null;
    let passo: number | null = null;
    if (dist && sec) passo = disc === "Nuoto" ? sec / (dist / 100) : disc === "Corsa" ? sec / (dist / 1000) : null;
    const cand = (prescritte[data] || []).find((p) => p.disciplina === disc && !usate.has(p.id));
    if (cand) usate.add(cand.id);
    return {
      atleta_id: atleta.id, esterno_fonte: "intervals", esterno_id: String(a.id),
      prescritta_id: cand ? cand.id : null,
      data, disciplina: disc, tipo: a.name || a.type || null,
      durata_min: Math.round(sec / 60), distanza_m: dist, dislivello_m: a.total_elevation_gain ?? null,
      passo_s: passo === null ? null : Math.round(passo * 10) / 10,
      potenza_w: a.icu_weighted_avg_watts ?? null, potenza_media_w: a.icu_average_watts ?? a.average_watts ?? null,
      fc_media: a.average_heartrate ?? null, fc_max: a.max_heartrate ?? null,
      rpe: a.icu_rpe ? Math.min(10, Math.max(0, Math.round(a.icu_rpe))) : null,
      carico: a.icu_training_load ?? null, carico_dichiarato: a.icu_training_load != null,
      fonte: "dispositivo", sensazione: a.feel ? FEEL[a.feel] ?? null : null,
      note: [a.type, a.description].filter(Boolean).join(" — ").slice(0, 500) || null,
    };
  }).filter((x) => x.data && x.durata_min > 0);

  let scritte = 0;
  for (let i = 0; i < righe.length; i += 200) {
    const { error } = await db.from("seduta_eseguita").upsert(righe.slice(i, i + 200), { onConflict: "esterno_fonte,esterno_id" });
    if (error) return json(500, { errore: "scrittura fallita", dettaglio: error.message });
    scritte += Math.min(200, righe.length - i);
  }
  const esito = `${scritte} attività dal ${oldest} al ${newest}`;
  await db.from("collegamento_intervals").update({ ultimo_import: new Date().toISOString(), ultimo_esito: esito, aggiornato_il: new Date().toISOString() }).eq("atleta_id", atleta.id);
  return json(200, { ok: true, attivita: attivita.length, scritte, oldest, newest, collegate: righe.filter((x) => x.prescritta_id).length });
});
