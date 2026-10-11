# -*- coding: utf-8 -*-
"""Rigenera i riferimenti Python per il test di parità del motore TypeScript.
Da lanciare dalla radice del repo:  python3 engine/test/genera_ref.py
Scrive engine/test/ref/scala.json e engine/test/ref/piano_<caso>.json."""
import json, os, re, subprocess, sys

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REF = os.path.join(RADICE, "engine", "test", "ref")
os.makedirs(REF, exist_ok=True)
sys.path.insert(0, RADICE)
import scala_gen as S

CASI_SCALA = [
    ("vittorio", None, 26, 11.0, 5.0, "Ironman", False),
    ("z36_11", None, 36, 11.0, 5.0, "Ironman", False),
    ("z36_20", None, 36, 20.0, 5.0, "Ironman", False),
    ("sprint24", "Triathlon Sprint", 24, 20.0, 7.0, "Ironman", False),
    ("half14", "Half-Ironman", 14, 28.0, 14.0, "Ironman", False),
    ("z6", None, 6, 11.0, 5.0, "Ironman", False),
    ("oli60", "Triathlon Olimpico", 60, 28.0, 10.0, "Ironman", False),
    ("vittorio_rigido", None, 26, 11.0, 5.0, "Ironman", True),
    ("z104_28_rigido", None, 104, 28.0, 5.0, "Ironman", True),
    ("z52_20_rigido", None, 52, 20.0, 5.0, "Ironman", True),
]
out = {}
for nome, fatto, sett, ore, oggi, ob, rig in CASI_SCALA:
    p = S.livello_scala(fatto, sett, ore, oggi, ob, rig)
    d = dict(input=dict(gradino_fatto=fatto, settimane=sett, ore_disponibili=ore, ore_oggi=oggi,
                        obiettivo=ob, tetto_rigido=rig), piano=p)
    if "errore" not in p:
        d["fabbisogno"] = S.fabbisogno_ore(p)
        d["verifiche"] = S.verifica_I8(p, fatto, ob)
    out[nome] = d
json.dump(out, open(os.path.join(REF, "scala.json"), "w"), indent=1, default=str)
print("scala.json:", len(out), "casi")

CFGS = {
    "sprint12": dict(gara="Triathlon Sprint", settimane=12, ore_picco=7.5, ore_oggi=5.0),
    "sprint8":  dict(gara="Triathlon Sprint", settimane=8, ore_picco=7.5, ore_oggi=5.0),
    "oli16":    dict(gara="Triathlon Olimpico", settimane=16, ore_picco=19.6, ore_oggi=6.4),
    "half8":    dict(gara="Half-Ironman", settimane=8, ore_picco=19.0, ore_oggi=16.7),
    "im12":     dict(gara="Ironman", settimane=12, ore_picco=27.0, ore_oggi=16.2),
    "im36_11":  dict(gara="Ironman", settimane=36, ore_picco=11.0, ore_oggi=5.0),
    "oli20_12": dict(gara="Triathlon Olimpico", settimane=20, ore_picco=12.0, ore_oggi=6.0),
    "im44_20":  dict(gara="Ironman", settimane=44, ore_picco=20.0, ore_oggi=8.0),
}
for k, cfg in CFGS.items():
    cfg = dict(cfg, sedute_sett=8, giorno_riposo="Lunedì")
    fc, fo = os.path.join(REF, f"cfg_{k}.json"), os.path.join(REF, f"piano_{k}.json")
    json.dump(cfg, open(fc, "w"))
    r = subprocess.run([sys.executable, os.path.join(RADICE, "generatore.py"), fc, fo],
                       capture_output=True, text=True, cwd=RADICE)
    if r.returncode:
        print(k, "ERRORE", r.stderr[-400:]); continue
    V = [l.strip() for l in r.stdout.splitlines() if re.match(r"\s*(OK|VIOLATA)\s", l)]
    d = json.load(open(fo)); d["V"] = V
    json.dump(d, open(fo, "w"))
    os.remove(fc)
    print(f"piano_{k}.json: {len(d['PIANO'])} sedute, {sum(1 for v in V if v.startswith('VIOLATA'))} violazioni")
