# -*- coding: utf-8 -*-
"""Genera le variazioni di ogni allenamento del catalogo.
   distanza: +-10..50%   passo: +-10..30%  (cap voluto per non creare allenamenti impossibili)
   Una variazione di passo sposta la zona -> cambia l'obiettivo -> e' un ALTRO allenamento."""
import sys, re
sys.path.insert(0,'/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad')
import parser as P, obiettivi as OB

K_DIST = [0.50,0.60,0.70,0.80,0.90,1.00,1.10,1.20,1.30,1.40,1.50]
K_PASSO = [0.70,0.80,0.90,1.00,1.10,1.20,1.30]

PASSI = {
 "bici_1600m":1.419,
 "bici_180km":1.971,
 "bici_20km":1.611,
 "bici_3200m":1.523,
 "bici_40km":1.675,
 "bici_800m":1.34,
 "bici_90km":1.821,
 "bici_RPE_12_14":1.971,
 "bici_RPE_sotto12":2.147,
 "bici_aerobica":2.094,
 "bici_forza":2.326,
 "bici_souplesse":2.577,
 "corsa_10km":5.0,
 "corsa_1600m":4.479,
 "corsa_2000m":4.54,
 "corsa_21km":5.229,
 "corsa_400m":4.122,
 "corsa_5km":4.796,
 "corsa_800m":4.297,
 "corsa_RPE_12_14":5.807,
 "corsa_RPE_sotto12":6.315,
 "corsa_aerobica":6.315,
 "corsa_forza":6.736,
 "corsa_maratona":5.451,
 "corsa_recupero":8.42,
 "nuoto_100m":1.623,
 "nuoto_1600m":1.917,
 "nuoto_2000m":1.943,
 "nuoto_200m":1.692,
 "nuoto_3200m":1.998,
 "nuoto_4000m":2.025,
 "nuoto_500m":1.787,
 "nuoto_RPE_12_14":2.178,
 "nuoto_RPE_sotto12":2.396,
 "nuoto_aerobico":2.255,
 "nuoto_blando":2.662,
 "nuoto_forza":2.337,
 "nuoto_recupero":2.662,
}
SOGLIA   = {"Corsa a piedi":"corsa_10km","Ciclismo":"bici_40km","Nuoto":"nuoto_1600m"}
FATT     = {"Nuoto":100,"Corsa a piedi":1000,"Ciclismo":1000}
# bande di passo fisiologicamente praticabili (min/km, nuoto min/100m)
BANDA    = {"Corsa a piedi":(3.20,12.00),"Ciclismo":(1.05,4.00),"Nuoto":(1.25,3.50)}
DURATA_MAX_MIN = 480          # oltre 8 ore una singola seduta non e' praticabile
# IF -> zona (logica TSS): IF = passo di soglia / passo del blocco
IF_ZONA = [(0.70,"Z1"),(0.83,"Z2"),(0.94,"Z3"),(1.03,"Z4"),(99,"Z5")]
ZONA_RANK = {"Z5":1,"Z4":2,"Z3":3,"Z2":4,"Z1":5}

def zona_da_if(v):
    for lim, z in IF_ZONA:
        if v < lim: return z
    return "Z5"

def _blocchi_utili(bs):
    """blocchi con zona nota e una durata calcolabile"""
    out = []
    for b in bs:
        zn = b["zona"]
        if zn not in PASSI: continue
        passo = PASSI[zn]; disc = b["sess"]["disc"]; fatt = FATT[disc]
        rip = b["rip"] or 1
        if b["dist"] is not None:
            dist = rip * b["dist"]; tempo = dist / fatt * passo; modo = "distanza"
        elif b["dur_a"] is not None:
            tempo = rip * (b["dur_a"] + b["dur_b"]) / 2; dist = tempo / passo * fatt; modo = "tempo"
        else:
            continue
        out.append(dict(zona=zn, passo=passo, dist=dist, tempo=tempo, modo=modo,
                        tipo=b["tipo"], fatt=fatt, disc=disc, rip=rip,
                        dist_rip=b["dist"], nel_tot=b.get("nel_totale", True)))
    return out

ZONA_SUPPL = {"Corsa a piedi":"corsa_aerobica","Ciclismo":"bici_aerobica","Nuoto":"nuoto_aerobico"}

def genera(base):
    """la zona di riferimento e' quella dell'originale dello stesso allenamento,
       cosi' il confronto e' metodologicamente omogeneo"""
    """base = dict(codice, sid, blocchi, ob_m, disc, focus, archetipo, struttura)
       ritorna la lista delle variazioni"""
    bl = base["blocchi"]; disc = base["disc"]
    if not bl: return []
    soglia = PASSI[SOGLIA[disc]]
    lo, hi = BANDA[disc]
    out = []
    for kd in K_DIST:
        for kp in K_PASSO:
            zone_min = {z: 0.0 for z in ("Z1","Z2","Z3","Z4","Z5")}
            dist_tot = tempo_tot = rtss = 0.0
            ok = True; motivi = []
            ranks = []
            for b in bl:
                passo = b["passo"] * kp
                if passo < lo or passo > hi:
                    ok = False
                    motivi.append(f"{b['zona']} a {passo:.2f} fuori banda")
                if b["modo"] == "distanza":
                    d = b["dist"] * kd; t = d / b["fatt"] * passo
                else:
                    t = b["tempo"] * kd; d = t / passo * b["fatt"]
                IF = soglia / passo
                z = zona_da_if(IF)
                zone_min[z] += t
                rtss += t / 60 * IF ** 2 * 100
                if b["nel_tot"]: dist_tot += d
                tempo_tot += t
                if b["tipo"] not in ("Recupero", "Recupero attivo", "Aerobico supplementare"):
                    ranks.append(z)
            # blocco aerobico supplementare: obiettivo scalato meno tutto il resto
            if base["ha_suppl"] and base["ob_m"]:
                res = base["ob_m"] * kd - dist_tot
                if res > 0:
                    zs = ZONA_SUPPL[disc]; ps = PASSI[zs] * kp
                    if ps < lo or ps > hi:
                        ok = False; motivi.append(f"{zs} a {ps:.2f} fuori banda")
                    ts = res / FATT[disc] * ps
                    IFs = soglia / ps
                    zone_min[zona_da_if(IFs)] += ts
                    rtss += ts / 60 * IFs ** 2 * 100
                    dist_tot += res; tempo_tot += ts
            if tempo_tot > DURATA_MAX_MIN:
                ok = False; motivi.append(f"durata {tempo_tot/60:.1f} h")
            zc = min(ranks, key=lambda z: ZONA_RANK[z]) if ranks else ""
            passo_medio = (tempo_tot / (dist_tot / FATT[disc])) if dist_tot else None
            out.append(dict(
                base=base["codice"], sid=base["sid"], arch=base["archetipo"], disc=disc,
                focus=base["focus"], ob_base=base["ob_fis"],
                kd=kd, kp=kp,
                tipo_var=("Originale" if kd == 1 and kp == 1 else
                          "Solo distanza" if kp == 1 else
                          "Solo passo" if kd == 1 else "Combinata"),
                ofat=(kd == 1 or kp == 1),
                dist=dist_tot, tempo=tempo_tot, passo_medio=passo_medio,
                zona_car=zc, zmin=zone_min, rtss=rtss,
                plaus=ok, motivo="; ".join(dict.fromkeys(motivi))[:120],
            ))
    rif = next((x["zona_car"] for x in out if x["kd"] == 1 and x["kp"] == 1), "")
    for x in out:
        x["zona_rif"] = rif
        x["cambio"] = bool(x["zona_car"]) and bool(rif) and x["zona_car"] != rif
    return out

def costruisci_basi():
    righe, _ = P.analizza()
    per_sid = {}
    for b in righe: per_sid.setdefault(b["sid"], []).append(b)
    # obiettivo caratterizzante originale
    def carat(bs):
        obs = [OB.ZONA_OBIETTIVO[b["zona"]] for b in bs
               if b["zona"] in OB.ZONA_OBIETTIVO and b.get("nel_totale", True)]
        core = [o for o in obs if o not in OB.CONTORNO] or obs
        return min(core, key=lambda o: OB.RANK[o]) if core else ""
    # ricostruisci archetipo e varianti come nel catalogo
    strutt = {s: per_sid[s][0]["struttura"] for s in per_sid}
    disc   = {s: per_sid[s][0]["sess"]["disc"] for s in per_sid}
    fam = {}
    for s, st in strutt.items():
        fam.setdefault((disc[s], re.sub(r'[0-9]+', '#', st)), []).append(s)
    PRE = {"Corsa a piedi":"RUN","Ciclismo":"BIKE","Nuoto":"SWIM","Pesi":"GYM","Riposo":"REST"}
    arche = {}; cnt = {}
    for (d, f), sids in sorted(fam.items(), key=lambda x: (x[0][0], -len(x[1]))):
        cnt[d] = cnt.get(d, 0) + 1
        for s in sids: arche[s] = f"{PRE.get(d,'ALT')}-{cnt[d]:02d}"
    varianti = {}
    for s in sorted(strutt): varianti.setdefault((arche[s], strutt[s]), []).append(s)
    basi = []; prog = {}
    for (code, st), sids in sorted(varianti.items(), key=lambda x: (x[0][0], -len(x[1]))):
        prog[code] = prog.get(code, 0) + 1
        rep = sids[0]
        if disc[rep] in ("Pesi", "Riposo"): continue
        bs = per_sid[rep]
        basi.append(dict(codice=f"{code}.{prog[code]:02d}", sid=rep, archetipo=code,
                         disc=disc[rep], focus=bs[0]["sess"]["focus"], ob_fis=carat(bs),
                         struttura=st, ob_m=bs[0]["ob_m"], blocchi=_blocchi_utili(bs),
                         ha_suppl=any(b["modo"] == "residuo" for b in bs)))
    return basi

def marca_duplicati(tutte, tol_dist=200, tol_tempo=2):
    """marca come ridondanti le variazioni quasi identiche a una gia' presente:
       stessa disciplina, stessa zona, distanza e tempo entro la tolleranza"""
    visti = {}
    for v in tutte:
        if not v["plaus"] or not v["dist"] or not v["tempo"]:
            v["gruppo"] = ""; v["ridondante"] = False; continue
        k = (v["disc"], v["zona_car"],
             round(v["dist"] / tol_dist) * tol_dist,
             round(v["tempo"] / tol_tempo) * tol_tempo)
        g = f'{v["disc"][:4].upper()}-{v["zona_car"]}-{k[2]}-{k[3]}'
        v["gruppo"] = g
        if k in visti:
            v["ridondante"] = True
        else:
            visti[k] = v["base"]; v["ridondante"] = False
    return tutte


if __name__ == "__main__":
    basi = costruisci_basi()
    print("allenamenti base:", len(basi))
    tutte = []
    for b in basi: tutte.extend(genera(b))
    print("variazioni generate:", len(tutte))
    from collections import Counter
    print(" per tipo:", dict(Counter(v["tipo_var"] for v in tutte)))
    print(" OFAT:", sum(1 for v in tutte if v["ofat"]))
    print(" plausibili:", sum(1 for v in tutte if v["plaus"]),
          f"({sum(1 for v in tutte if v['plaus'])/len(tutte)*100:.0f}%)")
    print(" cambio di obiettivo rispetto al base:",
          sum(1 for v in tutte if v["zona_car"] and v["kp"] != 1))
    print()
    print("--- esempio: una seduta di endurance corsa ---")
    ex = [b for b in basi if b["disc"] == "Corsa a piedi" and "Endurance" in str(b["focus"])][0]
    print(" base:", ex["codice"], "|", ex["struttura"][:80])
    for v in genera(ex):
        if v["ofat"] and (v["kd"] != 1 or v["kp"] != 1):
            print(f"   d{(v['kd']-1)*100:+4.0f}% p{(v['kp']-1)*100:+4.0f}%  "
                  f"{v['dist']/1000:6.1f} km  {v['tempo']:6.1f} min  zona {v['zona_car']}  "
                  f"{'OK' if v['plaus'] else 'NO: '+v['motivo'][:40]}")
