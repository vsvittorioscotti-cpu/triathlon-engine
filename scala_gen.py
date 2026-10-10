# -*- coding: utf-8 -*-
"""Livello scala (I8): decide QUALE gradino e' raggiungibile, poi quante
settimane spettano a ciascun blocco applicando E7. Il livello blocco
(generatore.py) lavora solo su cio' che questo modulo gli lascia."""
import math, json, os, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))

# gradino, settimane naturali del blocco, ore di picco, ore medie  (dal libro,
# con le soglie ancorate: vedi scala2.py)
SCALA = [
    ("Triathlon Sprint",    8,  7.5,  6.1),
    ("Triathlon Olimpico", 16, 19.6, 12.8),
    ("Half-Ironman",        8, 19.0, 14.3),
    ("Ironman",            12, 27.0, 18.7),
]
NOMI = [g[0] for g in SCALA]

TRANSIZIONE = 2     # settimane di recupero dopo ogni gara          (DEFAULT)
INTRO       = 4     # introduzione per chi parte da zero            (DEFAULT)
RITENZIONE  = 0.85  # quota del picco che si porta al blocco dopo   (HEURISTIC)
PEND_MIN    = 0.05  # E4: pendenza settimanale minima utile
QUOTA_MIN   = 0.50  # E3: partenza minima come quota del picco

def idx_gradino(fatto):
    return NOMI.index(fatto) if fatto in NOMI else -1

def _sett_naturali(i0, i1, da_zero):
    """settimane per salire dai gradini i0+1..i1 compresi, transizioni incluse"""
    n = INTRO if da_zero else 0
    for k in range(i0 + 1, i1 + 1):
        n += SCALA[k][1]
        if k < i1: n += TRANSIZIONE      # gara + recupero fra un gradino e l'altro
    return n

def carico_max(ore_inizio, ore_picco):
    """E3/E4: quante settimane di CARICO una rampa puo' contenere restando utile"""
    if ore_inizio <= 0 or ore_picco <= ore_inizio: return 3
    ore_inizio = max(ore_inizio, ore_picco * QUOTA_MIN)       # E3
    return 1 + math.log(ore_picco / ore_inizio) / math.log(1 + PEND_MIN)   # E4

def livello_scala(gradino_fatto, settimane, ore_disponibili, ore_oggi,
                  obiettivo="Ironman", tetto_rigido=False):
    i0 = idx_gradino(gradino_fatto)
    da_zero = (i0 < 0)
    i_obiettivo = NOMI.index(obiettivo)
    if i_obiettivo <= i0:
        return dict(errore=f"{obiettivo} e' un gradino gia' completato")

    # cancello ORE. La disponibilita' dichiarata e' un punto di partenza, non un
    # muro: puo' restare uguale o crescere. Blocca solo se dichiarata come tetto
    # rigido; altrimenti diventa un FABBISOGNO che il piano mette in conto.
    if tetto_rigido:
        tetto_i = i0
        for k in range(i0 + 1, i_obiettivo + 1):
            if SCALA[k][2] <= ore_disponibili: tetto_i = k
            else: break
    else:
        tetto_i = i_obiettivo
    # cancello TEMPO
    tempo_i = i0
    for k in range(i0 + 1, i_obiettivo + 1):
        if _sett_naturali(i0, k, da_zero) <= settimane: tempo_i = k
        else: break

    arrivo = min(tetto_i, tempo_i)
    if arrivo <= i0:
        serve_t = _sett_naturali(i0, i0 + 1, da_zero)
        return dict(errore="nemmeno il primo gradino e' raggiungibile",
                    gradino_prossimo=NOMI[i0 + 1],
                    settimane_necessarie=serve_t, settimane_disponibili=settimane,
                    ore_necessarie=SCALA[i0 + 1][2], ore_disponibili=ore_disponibili)

    if arrivo == i_obiettivo:
        vincolo = "nessuno: obiettivo raggiungibile"
    else:
        quali = [n for n, g in (("ore", tetto_i), ("tempo", tempo_i)) if g == arrivo]
        vincolo = " e ".join(quali)

    # ---- E7: il surplus si assorbe, non si attende ----
    blocchi = []
    inizio = ore_oggi
    for k in range(i0 + 1, arrivo + 1):
        nome, nat, picco, media = SCALA[k]
        blocchi.append(dict(gradino=nome, settimane=nat, naturali=nat, riempimento=0,
                            picco=picco, ore_inizio=round(inizio, 1),
                            sat=carico_max(inizio, picco)))
        inizio = picco * RITENZIONE
    surplus = settimane - _sett_naturali(i0, arrivo, da_zero)
    resto = surplus % 4
    unita = surplus // 4
    while unita > 0:
        for b in blocchi:                     # dal basso verso l'alto (E7.2)
            if b is blocchi[-1] and len(blocchi) > 1: continue   # il piu' alto mai (E7.5)
            if (b['settimane'] + 4) * 0.75 <= b['sat']:          # E3/E4 (E7.3)
                b['settimane'] += 4; b['riempimento'] += 4
                unita -= 1
                break
        else:
            resto += 4 * unita                # tutti saturi: nessuna unita' va persa
            unita = 0
    return dict(gradino_fatto=gradino_fatto or "nessuno", obiettivo=obiettivo,
                ore_disponibili=ore_disponibili, tetto_rigido=tetto_rigido,
                arrivo=NOMI[arrivo], raggiunge_obiettivo=(arrivo == i_obiettivo),
                vincolo=vincolo, intro=INTRO if da_zero else 0, blocchi=blocchi,
                transizioni=TRANSIZIONE * (len(blocchi) - 1), non_assorbite=resto,
                settimane_disponibili=settimane,
                settimane_usate=(INTRO if da_zero else 0) + sum(b['settimane'] for b in blocchi)
                                 + TRANSIZIONE * (len(blocchi) - 1) + resto)

def fabbisogno_ore(p):
    """Per ogni blocco: picco richiesto, settimana in cui cade, crescita implicita
       rispetto alla disponibilita' dichiarata oggi. La crescita della disponibilita'
       e' una questione di calendario personale; quella del CARICO resta vincolata
       da H1/E4 e si verifica qui che sia fisiologicamente percorribile."""
    out = []
    w = p['intro']
    disp = p['ore_disponibili']
    for b in p['blocchi']:
        w_picco = w + b['settimane'] - 2          # il picco cade prima del taper
        sett_carico = math.ceil(b['settimane'] * 0.75)
        pend = (b['picco'] / max(b['ore_inizio'], 0.1)) ** (1 / max(sett_carico - 1, 1)) - 1
        # un blocco il cui picco non supera il volume gia' raggiunto non costruisce
        # volume: converte volume in specificita'. E4 non si applica come violazione.
        tipo = ("costruzione" if pend >= PEND_MIN else "specificita' a volume quasi costante")
        out.append(dict(gradino=b['gradino'], picco=b['picco'], settimana=w_picco,
                        serve_in_piu=round(max(0.0, b['picco'] - disp), 1),
                        gia_coperto=(b['picco'] <= disp), disp_al_momento=round(disp, 1),
                        tipo=tipo, pendenza=pend,
                        pendenza_ok=(pend <= 0.15)))
        disp = max(disp, b['picco'])
        w += b['settimane'] + TRANSIZIONE
    return out

def verifica_I8(p, gradino_fatto, obiettivo):
    """undicesima verifica: la scala non si salta e non si supera"""
    V = []
    def chk(reg, ok, dett): V.append((reg, "OK" if ok else "VIOLATA", dett))
    i0 = idx_gradino(gradino_fatto)
    attesi = NOMI[i0 + 1 : NOMI.index(p['arrivo']) + 1]
    ottenuti = [b['gradino'] for b in p['blocchi']]
    chk("I8  nessun gradino saltato", ottenuti == attesi,
        f"{' -> '.join(ottenuti) if ottenuti else 'nessuno'}")
    chk("I8b arrivo non oltre il raggiungibile",
        NOMI.index(p['arrivo']) <= NOMI.index(obiettivo), f"arrivo {p['arrivo']}")
    chk("E7  nulla di assorbibile e' rimasto fuori",
        p['non_assorbite'] < 4 or all((b['settimane'] + 4) * 0.75 > b['sat'] for b in p['blocchi'][:-1] or p['blocchi']),
        f"{p['non_assorbite']} settimane non assorbite")
    chk("E7b il gradino piu' alto non e' riempito",
        len(p['blocchi']) == 1 or p['blocchi'][-1]['riempimento'] == 0,
        "un solo blocco: e' anche il piu' basso, il riempimento gli spetta"
        if len(p['blocchi']) == 1 else
        f"riempimento sul piu' alto: {p['blocchi'][-1]['riempimento']} sett.")
    chk("A3  ore richieste da ogni blocco",
        (not p['tetto_rigido']) or all(b['picco'] <= p['ore_disponibili'] for b in p['blocchi']),
        f"picco massimo {max(b['picco'] for b in p['blocchi']):.1f} h contro {p['ore_disponibili']} dichiarate"
        + ("" if p['tetto_rigido'] else " (tetto non rigido: e' un fabbisogno)"))
    chk("E7c il residuo sta dentro una transizione", p['non_assorbite'] < 4,
        f"{p['non_assorbite']} settimane fuori dai blocchi"
        + (" -> periodo non coperto dalla dottrina" if p['non_assorbite'] >= 4 else ""))
    return V

def stampa(p):
    if 'errore' in p:
        print("  NON REALIZZABILE:", p['errore'])
        for k, v in p.items():
            if k != 'errore': print(f"    {k}: {v}")
        return
    print(f"  gradino di partenza : {p['gradino_fatto']}")
    print(f"  obiettivo richiesto : {p['obiettivo']}")
    print(f"  arrivo realistico   : {p['arrivo']}" +
          ("" if p['raggiunge_obiettivo'] else "   <-- l'obiettivo NON e' raggiungibile"))
    print(f"  vincolo che morde   : {p['vincolo']}")
    print(f"  settimane           : {p['settimane_usate']} usate su {p['settimane_disponibili']}")
    if p['intro']: print(f"    introduzione            {p['intro']:2d} sett.")
    for b in p['blocchi']:
        extra = f"  (+{b['riempimento']} di riempimento E7)" if b['riempimento'] else ""
        print(f"    {b['gradino']:<20}{b['settimane']:2d} sett."
              f"  picco {b['picco']:4.1f} h  da {b['ore_inizio']:4.1f} h{extra}")
    if p['transizioni']: print(f"    transizioni post-gara   {p['transizioni']:2d} sett.")
    if p['non_assorbite']:
        coda = " -> fuori dalla dottrina (periodo fra due stagioni)" if p['non_assorbite'] >= 4 else " (assorbite dalle transizioni)"
        print(f"    non assorbite           {p['non_assorbite']:2d} sett.{coda}")

def genera_blocchi(p, ore_oggi, sedute_sett=8, giorno_riposo="Lunedi"):
    """Livello 2: per ogni blocco della scala chiama il motore con le SUE settimane."""
    out = []
    inizio = ore_oggi
    for i, b in enumerate(p['blocchi']):
        cfg = dict(gara=b['gradino'], settimane=b['settimane'], ore_picco=b['picco'],
                   ore_oggi=inizio, sedute_sett=sedute_sett, giorno_riposo=giorno_riposo)
        fc = os.path.join(QUI, f"cfg_{i}.json"); fo = os.path.join(QUI, f"piano_{i}.json")
        json.dump(cfg, open(fc, 'w'))
        r = subprocess.run([sys.executable, '-I', os.path.join(QUI, 'generatore.py'), fc, fo],
                           capture_output=True, text=True, cwd=QUI)
        if r.returncode != 0:
            out.append(dict(gradino=b['gradino'], errore=r.stderr.strip()[-400:])); continue
        d = json.load(open(fo))
        out.append(dict(gradino=b['gradino'], sedute=len(d['PIANO']),
                        ore=sum(x['tempo'] for x in d['PIANO']) / 60,
                        report=r.stdout, file=fo))
        inizio = b['picco'] * RITENZIONE
    return out

if __name__ == '__main__':
    CASI = [
        ("Vittorio: da zero, 26 sett. alla prima gara, tetto 11 h", None, 26, 11.0, 5.0, "Ironman"),
        ("Da zero, 36 settimane, tetto 11 h",                       None, 36, 11.0, 5.0, "Ironman"),
        ("Da zero, 36 settimane, tetto 20 h",                       None, 36, 20.0, 5.0, "Ironman"),
        ("Sprint fatto, 24 settimane, tetto 20 h",   "Triathlon Sprint", 24, 20.0, 7.0, "Ironman"),
        ("Half fatto, 14 settimane, tetto 28 h",         "Half-Ironman", 14, 28.0, 14.0, "Ironman"),
        ("Da zero, 6 settimane, tetto 11 h",                        None,  6, 11.0, 5.0, "Ironman"),
        ("Olimpico fatto, 60 settimane, tetto 28 h", "Triathlon Olimpico", 60, 28.0, 10.0, "Ironman"),
    ]
    for titolo, fatto, sett, picco, oggi, ob in CASI:
        print("=" * 78); print(titolo); print("-" * 78)
        p = livello_scala(fatto, sett, picco, oggi, ob)
        stampa(p)
        if 'errore' not in p:
            for reg, es, dt in verifica_I8(p, fatto, ob):
                print(f"      {es:8s} {reg:38s} {dt}")
        print()
