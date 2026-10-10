# -*- coding: utf-8 -*-
"""Spacchetta il testo delle serie in blocchi strutturati e parametrizzati."""
import re, sys
sys.path.insert(0,'/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad')
import dati8

# ---------------- utilità numeriche (formato italiano) ----------------
def num(s):
    s = s.strip()
    if ',' in s:
        return float(s.replace('.', '').replace(',', '.'))
    return float(s.replace('.', ''))

def i(x):
    return int(x) if float(x) == int(x) else x

# ---------------- zone di riferimento ----------------
def zona(disc, val, unita):
    m = val * 1000 if unita == 'km' else val
    if disc == "Corsa a piedi":
        return {400:"corsa_400m", 800:"corsa_800m", 1600:"corsa_1600m", 2000:"corsa_2000m",
                5000:"corsa_5km", 10000:"corsa_10km", 21000:"corsa_21km",
                42000:"corsa_maratona"}.get(int(m), f"corsa_{i(m)}m")
    if disc == "Nuoto":
        return f"nuoto_{int(m)}m"
    if disc == "Ciclismo":
        if m >= 20000:
            return f"bici_{i(m/1000)}km"
        return f"bici_{int(m)}m"
    return "n.d."

FATT = {"Nuoto": 100, "Corsa a piedi": 1000, "Ciclismo": 1000}
SUPPL = {"Nuoto": "nuoto_aerobico", "Corsa a piedi": "corsa_aerobica", "Ciclismo": "bici_aerobica"}
RECUP = {"Nuoto": "nuoto_recupero", "Corsa a piedi": "corsa_recupero", "Ciclismo": "bici_souplesse"}

def B(tipo, rip=None, dist=None, dur_a=None, dur_b=None, modo=None, zn=None,
      setp=None, ripp=None, rm=None, nota=None):
    return dict(tipo=tipo, rip=rip, dist=dist, dur_a=dur_a, dur_b=dur_b, modo=modo,
                zona=zn, setp=setp, ripp=ripp, rm=rm, nota=nota)

def d2s(dist, zn):
    return f"{i(dist)}m @{zn}"

# ---------------- il parser ----------------
def parse(t, disc):
    """ritorna (lista di blocchi, notazione sintetica)"""
    S = SUPPL.get(disc, "n.d."); R = RECUP.get(disc, "n.d.")

    # ---- riposo / note testuali -------------------------------------------------
    if t.startswith("Nessun allenamento"):
        return [B("Riposo")], "riposo"
    if (t.startswith("Completare tutti i movimenti") or t.startswith("Tutti i movimenti")
            or t.startswith("Nessuna progressione") or t.startswith("Nota del libro")
            or t.startswith("Vanno eliminati")):
        return [B("Nota", nota=t)], ""
    if t.startswith("Questa sessione viene sostituita dalla gara a cui"):
        return [B("Gara")], "GARA"

    # ---- pesi -------------------------------------------------------------------
    m = re.match(r"^(\d+) x da (\d+) a (\d+) ripetizioni all'(\d+)% di 1 RM\.$", t)
    if m:
        return [B("Pesi - forza", setp=int(m[1]), ripp=f"{m[2]}-{m[3]}", rm=int(m[4]))], f"{m[1]}x{m[2]}-{m[3]}@{m[4]}%1RM"
    m = re.match(r"^(\d+) x (\d+) ripetizioni al(?:l'|\s)\s*(\d+)% di 1 RM(, esplosive)?\.$", t)
    if m:
        tipo = "Pesi - potenza" if m[4] else "Pesi - forza"
        nota = f"{m[1]}x{m[2]}@{m[3]}%1RM" + (" espl" if m[4] else "")
        return [B(tipo, setp=int(m[1]), ripp=int(m[2]), rm=int(m[3]))], nota

    # ---- tapering / sessioni descrittive ----------------------------------------
    if t.startswith("Questa sessione viene sostituita dalla gara prevista") or \
       t.startswith("In questa sessione sono compresi"):
        return [B("Tapering - aerobico + richiami", rip=1, modo="descrittivo", zn=S, nota=t)], "tapering"

    # ---- supplementare aerobico (blocco residuo) --------------------------------
    if (t.startswith("Della corsa aerobica supplementare") or
        t.startswith("Del ciclismo aerobico supplementare") or
        t.startswith("Una serie o del nuoto aerobico supplementare")):
        return [B("Aerobico supplementare", rip=1, modo="residuo", zn=S)], f"suppl @{S}"

    # ---- nuoto: ritmo blando -----------------------------------------------------
    m = re.match(r"^([\d.,]+) metri a nuoto, a ritmo blando\.$", t)
    if m:
        d = num(m[1])
        return [B("Recupero attivo", rip=1, dist=d, modo="distanza", zn="nuoto_blando")], d2s(d, "nuoto_blando")

    # ---- corsa: recupero fra le serie ---------------------------------------------
    m = re.match(r"^([\d.,]+) metri di camminata o di jogging per il recupero \(in pista\) o da (\d+) a (\d+) minuti", t)
    if m:
        d = num(m[1])
        return [B("Recupero", rip=1, dist=d, dur_a=float(m[2]), dur_b=float(m[3]),
                  modo="distanza o tempo", zn="corsa_recupero")], d2s(d, "corsa_recupero")

    # ---- bici: giro in souplesse --------------------------------------------------
    m = re.match(r"^Da (\d+) a (\d+) minuti in bicicletta per un giro in souplesse\.", t)
    if m:
        return [B("Recupero", rip=1, dur_a=float(m[1]), dur_b=float(m[2]),
                  modo="tempo", zn="bici_souplesse")], f"{m[1]}-{m[2]}' @bici_souplesse"

    # ---- endurance sulla forza ----------------------------------------------------
    m = re.match(r"^Una serie da (\d+) minuti di endurance sulla forza utilizzando un rapporto", t)
    if m:
        return [B("Endurance sulla forza", rip=1, dur_a=float(m[1]), dur_b=float(m[1]),
                  modo="tempo", zn="bici_forza")], f"{m[1]}' @bici_forza"
    m = re.match(r"^(\d+)(?: e mezzo)? minuti di lavoro di endurance sulla forza", t)
    if m:
        d = float(m[1]) + (0.5 if " e mezzo" in t[:40] else 0)
        return [B("Endurance sulla forza", rip=1, dur_a=d, dur_b=d,
                  modo="tempo", zn="corsa_forza")], f"{i(d)}' @corsa_forza"
    m = re.match(r"^([\d.,]+) metri a nuoto di endurance sulla forza", t)
    if m:
        d = num(m[1])
        return [B("Endurance sulla forza", rip=1, dist=d, modo="distanza", zn="nuoto_forza")], d2s(d, "nuoto_forza")
    m = re.match(r"^Una serie di ([\d.,]+) metri a nuoto di endurance sulla forza", t)
    if m:
        d = num(m[1])
        return [B("Endurance sulla forza", rip=1, dist=d, modo="distanza", zn="nuoto_forza")], d2s(d, "nuoto_forza")
    m = re.match(r"^Endurance sulla forza: (\d+) minuti\.$", t)
    if m:
        zn = "bici_forza" if disc == "Ciclismo" else "corsa_forza"
        return [B("Endurance sulla forza", rip=1, dur_a=float(m[1]), dur_b=float(m[1]),
                  modo="tempo", zn=zn)], f"{m[1]}' @{zn}"
    m = re.match(r"^Endurance sulla forza: ([\d.,]+) metri\.$", t)
    if m:
        d = num(m[1])
        return [B("Endurance sulla forza", rip=1, dist=d, modo="distanza", zn="nuoto_forza")], d2s(d, "nuoto_forza")

    # ---- fase di base: RPE ---------------------------------------------------------
    m = re.match(r"^([\d.,]+) (chilometri|metri) (?:da 12 a 14|a <12) RPE\.$", t)
    if m:
        d = num(m[1]) * (1000 if m[2] == "chilometri" else 1)
        pre = {"Nuoto": "nuoto", "Corsa a piedi": "corsa", "Ciclismo": "bici"}[disc]
        zn = f"{pre}_RPE_12_14" if "12 a 14" in t else f"{pre}_RPE_sotto12"
        tipo = "Endurance - distanza intermedia" if "12 a 14" in t else "Endurance - distanza lunga"
        return [B(tipo, rip=1, dist=d, modo="distanza", zn=zn)], d2s(d, zn)

    # ---- corsa: allunghi in pista / tapis ------------------------------------------
    m = re.match(r"^(\d+) x ([\d.,]+) metri di allunghi \(in pista\) o \d+ x (\d+) secondi(?: di corsa)? "
                 r"\(sul tapis roulant\) alla velocita' prevista su(?:i|gli) ([\d.,]+) metri, "
                 r"con ([\d.,]+) metri di camminata", t)
    if m:
        n = int(m[1]); d = num(m[2]); sec = float(m[3]); ref = num(m[4]); rd = num(m[5])
        zn = zona(disc, ref, 'm')
        return ([B("Velocita' - allunghi", rip=n, dist=d, dur_a=sec/60, dur_b=sec/60, modo="distanza", zn=zn),
                 B("Recupero", rip=n, dist=rd, modo="distanza", zn="corsa_recupero")],
                f"{n} x ({i(d)}m @{zn} + {i(rd)}m @corsa_recupero)")

    # ---- nuoto: ripetute -------------------------------------------------------------
    m = re.match(r"^(\d+) x ([\d.,]+) metri e (\d+) x ([\d.,]+) metri a nuoto alla velocita' prevista "
                 r"sui ([\d.,]+) metri, con (\d+) secondi di riposo\.$", t)
    if m:
        n1, d1, n2, d2, ref, sec = int(m[1]), num(m[2]), int(m[3]), num(m[4]), num(m[5]), float(m[6])
        zn = zona(disc, ref, 'm')
        return ([B("Andatura di gara", rip=n1, dist=d1, modo="distanza", zn=zn),
                 B("Recupero", rip=n1, dur_a=sec/60, dur_b=sec/60, modo="tempo", zn="nuoto_recupero"),
                 B("Andatura di gara", rip=n2, dist=d2, modo="distanza", zn=zn),
                 B("Recupero", rip=n2, dur_a=sec/60, dur_b=sec/60, modo="tempo", zn="nuoto_recupero")],
                f"{n1} x ({i(d1)}m @{zn} + {i(sec)}\") + {n2} x ({i(d2)}m @{zn} + {i(sec)}\")")
    m = re.match(r"^(\d+) x ([\d.,]+) metri a nuoto alla velocita' prevista sui ([\d.,]+) metri, "
                 r"con (?:(\d+) secondi(?: di)? riposo|un riposo uguale)\.$", t)
    if m:
        n, d, ref = int(m[1]), num(m[2]), num(m[3])
        zn = zona(disc, ref, 'm')
        eff = B("Velocita' / andatura di gara", rip=n, dist=d, modo="distanza", zn=zn)
        if m[4]:
            rec = B("Recupero", rip=n, dur_a=float(m[4])/60, dur_b=float(m[4])/60, modo="tempo", zn="nuoto_recupero")
            note = f"{n} x ({i(d)}m @{zn} + {i(float(m[4]))}\")"
        else:
            rec = B("Recupero", rip=n, modo="riposo uguale", zn="nuoto_recupero")
            note = f"{n} x ({i(d)}m @{zn} + riposo uguale)"
        return [eff, rec], note

    # ---- bici: ripetute in metri ------------------------------------------------------
    m = re.match(r"^(\d+) x ([\d.,]+) metri(?: in bicicletta)? alla velocita'(?: o alla potenza)? prevista "
                 r"su(?:i|gli) ([\d.,]+) metri, con (?:(\d+) secondi per un giro di recupero|"
                 r"un riposo uguale \(un giro di recupero in souplesse\))\.$", t)
    if m:
        n, d, ref = int(m[1]), num(m[2]), num(m[3])
        zn = zona(disc, ref, 'm')
        eff = B("Velocita' - ripetute", rip=n, dist=d, modo="distanza", zn=zn)
        if m[4]:
            rec = B("Recupero", rip=n, dur_a=float(m[4])/60, dur_b=float(m[4])/60, modo="tempo", zn="bici_souplesse")
            note = f"{n} x ({i(d)}m @{zn} + {i(float(m[4]))}\")"
        else:
            rec = B("Recupero", rip=n, modo="riposo uguale", zn="bici_souplesse")
            note = f"{n} x ({i(d)}m @{zn} + riposo uguale)"
        return [eff, rec], note

    # ---- bici: ripetute in chilometri --------------------------------------------------
    m = re.match(r"^(\d+) x ([\d.,]+) chilometri in bicicletta alla velocita' prevista sui ([\d.,]+) chilometri, "
                 r"con (?:da (\d+) a (\d+) minuti|(\d+) minut[oi]) per un giro in souplesse\.$", t)
    if m:
        n, d, ref = int(m[1]), num(m[2])*1000, num(m[3])
        a = float(m[4]) if m[4] else float(m[6]); b = float(m[5]) if m[5] else float(m[6])
        zn = zona(disc, ref, 'km')
        return ([B("Andatura di gara", rip=n, dist=d, modo="distanza", zn=zn),
                 B("Recupero", rip=n, dur_a=a, dur_b=b, modo="tempo", zn="bici_souplesse")],
                f"{n} x ({i(d)}m @{zn} + {i(a)}' @bici_souplesse)")
    m = re.match(r"^(\d+) x ([\d.,]+) chilometri in bicicletta alla velocita' prevista sui ([\d.,]+) chilometri, "
                 r"con un giro in souplesse di (\d+) minuto\.$", t)
    if m:
        n, d, ref, a = int(m[1]), num(m[2])*1000, num(m[3]), float(m[4])
        zn = zona(disc, ref, 'km')
        return ([B("Andatura di gara", rip=n, dist=d, modo="distanza", zn=zn),
                 B("Recupero", rip=n, dur_a=a, dur_b=a, modo="tempo", zn="bici_souplesse")],
                f"{n} x ({i(d)}m @{zn} + {i(a)}' @bici_souplesse)")

    # ---- corsa: ripetute andatura di gara ------------------------------------------------
    m = re.match(r"^(\d+) x ([\d.,]+) (metri|chilometri) di corsa alla velocita' prevista sui ([\d.,]+) (chilometri|metri), "
                 r"con ([\d.,]+) metri di camminata o(?: di)? jogging per il recupero\.$", t)
    if m:
        n = int(m[1]); d = num(m[2]) * (1000 if m[3] == "chilometri" else 1)
        ref = num(m[4]); zn = zona(disc, ref, 'km' if m[5] == "chilometri" else 'm')
        rd = num(m[6])
        return ([B("Andatura di gara", rip=n, dist=d, modo="distanza", zn=zn),
                 B("Recupero", rip=n, dist=rd, modo="distanza", zn="corsa_recupero")],
                f"{n} x ({i(d)}m @{zn} + {i(rd)}m @corsa_recupero)")

    # ---- endurance continuato: bici -------------------------------------------------------
    m = re.match(r"^([\d.,]+) chilometri o da (\d+) a (\d+) minuti in bicicletta in modo continuato "
                 r"alla cadenza prevista e alla velocita' prevista sui ([\d.,]+) chilometri", t)
    if m:
        d = num(m[1])*1000; zn = zona(disc, num(m[4]), 'km')
        return [B("Endurance continuato", rip=1, dist=d, dur_a=float(m[2]), dur_b=float(m[3]),
                  modo="distanza o tempo", zn=zn)], d2s(d, zn)

    # ---- endurance continuato: nuoto -------------------------------------------------------
    m = re.match(r"^Da (\d+) a (\d+) minuti o ([\d.,]+) metri a nuoto in modo continuato", t)
    if m:
        d = num(m[3])
        mr = re.search(r"alla velocita' prevista sui ([\d.,]+) metri", t)
        zn = zona(disc, num(mr[1]), 'm') if mr else "nuoto_aerobico"
        return [B("Endurance continuato", rip=1, dist=d, dur_a=float(m[1]), dur_b=float(m[2]),
                  modo="distanza o tempo", zn=zn)], d2s(d, zn)

    # ---- endurance continuato: corsa --------------------------------------------------------
    m = re.match(r"^([\d.,]+) chilometri o da (\d+) a (\d+) minuti di corsa in modo continuato "
                 r"alla velocita' prevista sulla distanza della (mezza maratona|maratona)", t)
    if m:
        d = num(m[1])*1000
        zn = "corsa_21km" if m[4] == "mezza maratona" else "corsa_maratona"
        nota = "Valore incoerente con l'obiettivo di sessione: vedi Legenda" if "[NB:" in t else None
        return [B("Endurance continuato", rip=1, dist=d, dur_a=float(m[2]), dur_b=float(m[3]),
                  modo="distanza o tempo", zn=zn, nota=nota)], d2s(d, zn)

    return None, None


# ---------------- esecuzione ----------------
def analizza():
    righe = []
    non_parsati = []
    sid = 0
    for s in dati8.TUTTE:
        sid += 1
        disc = s["disc"]
        ob = s["vol_num"]
        ob_m = None
        if ob is not None:
            ob_m = ob * (1000 if s["unita"] == "km" else 1)
        blocchi = []
        notazioni = []
        for idx, testo in enumerate(s["serie"]):
            bl, nota = parse(testo, disc)
            if bl is None:
                non_parsati.append((disc, testo))
                bl, nota = [B("Non parsato", nota=testo)], ""
            etich = etichetta(s, idx)
            for b in bl:
                b["serie_libro"] = etich
                b["testo"] = testo
            blocchi.extend(bl)
            if nota:
                notazioni.append(nota)
        struttura = " + ".join(notazioni)
        for k, b in enumerate(blocchi, 1):
            # Nella FASE DI BASE il libro indica i minuti/metri di endurance sulla forza come
            # PARTE della distanza della sessione, non come lavoro aggiuntivo: non va sommato.
            nel_tot = not (s.get("fase") == "Base" and b["tipo"] == "Endurance sulla forza")
            righe.append(dict(sid=sid, sess=s, blocco=k, struttura=struttura, ob_m=ob_m,
                              nel_totale=nel_tot, **b))
    return righe, non_parsati

ORD = ["Prima Serie","Seconda Serie","Terza Serie","Quarta Serie","Quinta Serie",
       "Sesta Serie","Settima Serie","Ottava Serie"]
def etichetta(s, idx):
    if s["disc"] == "Riposo": return "-"
    if s.get("fase") == "Base":
        return "Prescrizione" if s["disc"] != "Pesi" else ("Prescrizione" if idx < 2 else "Movimenti")
    if s["disc"] == "Pesi":
        return "Prescrizione" if (idx < 2 and not s.get("descr")) else "Nota"
    if s.get("descr"): return "Descrizione"
    return ORD[idx] if idx < len(ORD) else f"Serie {idx+1}"

if __name__ == "__main__":
    righe, np_ = analizza()
    print("blocchi generati:", len(righe))
    print("testi NON parsati:", len(np_))
    from collections import Counter
    for (d, t), n in Counter(np_).most_common(20):
        print("  !", d, "|", t[:110])
    print()
    for k, v in Counter(r["tipo"] for r in righe).most_common():
        print(f"  {v:5d}  {k}")
