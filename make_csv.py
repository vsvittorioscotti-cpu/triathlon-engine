import csv, json, sys
sys.path.insert(0, ".")
import forza2 as F, forza_sess2 as S

def w(name, cols, rows):
    with open("csv/%s.csv" % name, "w", newline="", encoding="utf-8") as f:
        c = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        c.writeheader()
        c.writerows(rows)
    print(name, len(rows))

w("variante", ["cod","base","arch","disc","ob_libro","zona","ob","dist","tempo","edw","ban","rtss"],
  json.load(open("lib.json")))

ex, seen = [], set()
for e in F.ESERCIZI:
    s = F.scheda(e)
    if s["nome"] in seen: continue
    seen.add(s["nome"])
    ex.append({"nome":s["nome"],"famiglia":s["famiglia"],"sottocat":s.get("sottocat"),
      "distretto":s.get("distretto"),"funzione":s.get("funzione"),"attrezzo":s.get("attrezzo"),
      "n_nuoto":s.get("N"),"b_bici":s.get("B"),"c_corsa":s.get("C"),"serie":s.get("serie"),
      "rip":s.get("rip"),"rec":s.get("rec"),"livello":s.get("livello"),"fasi":s.get("fasi"),
      "fatica":s.get("fatica"),"doms":s.get("doms"),"collocazione":s.get("collocazione"),
      "reps_base":s.get("reps_base"),"reps_peak":s.get("reps_peak"),"alternative":s.get("alternative")})
w("esercizio", ["nome","famiglia","sottocat","distretto","funzione","attrezzo","n_nuoto","b_bici",
  "c_corsa","serie","rip","rec","livello","fasi","fatica","doms","collocazione","reps_base",
  "reps_peak","alternative"], ex)

wk, rows = [], []
for raw in S.W:
    d = S.componi(raw)
    wk.append({"cod":d["cod"],"nome":d["nome"],"bersaglio":d.get("bersaglio"),"fasi":d.get("fasi"),
      "n_esercizi":d.get("n"),"minuti":d.get("minuti"),"famiglia":d.get("famiglia"),
      "zona":d.get("zona"),"nm":d.get("nm"),"fatica":d.get("fatica"),"doms":d.get("doms"),
      "collocazione":d.get("collocazione"),"n_nuoto":d.get("N"),"b_bici":d.get("B"),"c_corsa":d.get("C")})
    for i, t in enumerate(raw[4]):
        rows.append({"workout_cod":raw[0],"ordine":i,"esercizio":t[0],"serie":t[1],"rip":t[2],
                     "qualificatore":(t[3] if len(t) > 3 else None)})
w("workout_forza", ["cod","nome","bersaglio","fasi","n_esercizi","minuti","famiglia","zona","nm",
  "fatica","doms","collocazione","n_nuoto","b_bici","c_corsa"], wk)
w("workout_esercizio", ["workout_cod","ordine","esercizio","serie","rip","qualificatore"], rows)
