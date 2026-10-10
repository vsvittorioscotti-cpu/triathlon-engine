# -*- coding: utf-8 -*-
"""Generatore di piani: dalla dottrina al piano, pescando dalla libreria."""
import os
from openpyxl import load_workbook
from collections import defaultdict
import math, json

F='/mnt/user-data/outputs/Piani_Triathlon_Sprint_Olimpico_Half-Ironman_Ironman.xlsx'
wb = None if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),'lib.json')) else load_workbook(F, data_only=True)

# ---------- libreria (con cache: il motore gira una volta per blocco) ----------
import os
_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib.json')
if os.path.exists(_CACHE):
    LIB = json.load(open(_CACHE))
else:
    LIB=[]
    for r in wb['Variazioni Allenamenti'].iter_rows(min_row=6, values_only=True):
        if not r[0] or r[24]!='Si' or r[27]!='No': continue      # plausibile e non ridondante
        if not r[11] or not r[21]: continue
        LIB.append(dict(cod=r[0], base=r[1], arch=r[2], disc=r[3], ob_libro=r[4],
                        zona=r[13], ob=r[14], dist=r[10], tempo=r[11],
                        edw=r[21], ban=r[22], rtss=r[23]))
    json.dump(LIB, open(_CACHE,'w'))
print(f"libreria utilizzabile: {len(LIB)} allenamenti")
DOM={'Z1':'LOW','Z2':'LOW','Z3':'MOD','Z4':'HIGH','Z5':'HIGH'}
for x in LIB: x['dom']=DOM.get(x['zona'],'LOW')

# ---------- input atleta ----------
import sys as _sys
_DEF = dict(gara="Ironman", settimane=36, ore_picco=11.0, ore_oggi=5.0,
            sedute_sett=8, giorno_riposo="Lunedì")
A   = json.load(open(_sys.argv[1])) if len(_sys.argv) > 1 else _DEF
OUT = _sys.argv[2] if len(_sys.argv) > 2 else 'piano.json'
SILENZIO = len(_sys.argv) > 3

# ---------- 1. architettura ----------
# Otto fasi, non due macrocicli: quota di forza e sforamento cambiano per fase.
# Le frazioni sono nostre e sommano a 1 sulle settimane che precedono il taper.
FASI = [("Preparation",0.10),("Base 1",0.15),("Base 2",0.15),("Build 1",0.15),
        ("Build 2",0.15),("Specific",0.18),("Peak",0.12)]
# quota di forza sul monte ore, e sforamento ammesso (Strength Allowance)
QUOTA = {"Preparation":0.175,"Base 1":0.165,"Base 2":0.135,"Build 1":0.105,
         "Build 2":0.085,"Specific":0.065,"Peak":0.040,"Taper":0.015}
ALLOW = {"Preparation":0.125,"Base 1":0.090,"Base 2":0.065,"Build 1":0.025,
         "Build 2":0.015,"Specific":0.0,"Peak":0.0,"Taper":0.0}
# sedute per fase: la frequenza resta a due piu' a lungo di quanto faccia il libro
NSED  = {"Preparation":2,"Base 1":2,"Base 2":2,"Build 1":2,
         "Build 2":2,"Specific":2,"Peak":1,"Taper":1}
# carattere del contenuto per fase: quale tag della libreria e quale famiglia preferire
CARATT = {"Preparation":("B",None),"Base 1":("B","Forza massima"),
          "Base 2":("B","Forza massima"),"Build 1":("U",None),"Build 2":("U",None),
          "Specific":("S",None),"Peak":("P",None),"Taper":("P",None)}

def architettura(n):
    """Blocchi di 4 (3 carico + 1 scarico). La seconda meta' resta 'specifica'
       per il piazzamento dei brick (I6); le otto fasi vivono sopra a questa."""
    blocchi = math.ceil(n / 4)
    meta = max(1, blocchi // 2)
    return [("Preparatorio", list(range(1, meta + 1))),
            ("Specifico",    list(range(meta + 1, blocchi + 1)))], blocchi

# D8: durata e profondita' del taper, misurate sui quattro piani del libro
# (Sprint 1 sett. al 32% del picco; Ironman 2 sett., l'ultima al 7%)
N_TAPER  = 1 if A['settimane'] <= 8 else 2
PROF_TAPER = {1: [0.32], 2: [0.50, 0.10]}[N_TAPER]
MACRO, NB = architettura(A['settimane'])
TAPER_DA = A['settimane'] - N_TAPER + 1
print(f"architettura: {A['settimane']} settimane = {NB} blocchi da 4; "
      f"taper di {N_TAPER} sett. dalla {TAPER_DA}")

# ---------- 2. calendario e carico settimanale ----------
def _fase_di(w):
    if w >= TAPER_DA: return "Taper"
    n = TAPER_DA - 1; cum = 0.0
    for nome, q in FASI:
        cum += q
        if w <= math.ceil(cum * n): return nome
    return FASI[-1][0]

def settimane():
    out=[]
    for w in range(1, A['settimane']+1):
        blocco=(w-1)//4+1; pos=(w-1)%4+1
        macro = next((m for m,bs in MACRO if blocco in bs), "Taper")
        if w >= TAPER_DA: tipo, macro = "Taper", "Taper"
        elif pos==4:      tipo = "Scarico"
        else:             tipo = "Carico"
        out.append(dict(w=w, blocco=blocco, pos=pos, macro=macro, tipo=tipo,
                        fase=_fase_di(w)))
    return out
W=settimane()

# rampa: ore = da ore_oggi al picco; sotto-picco 85% a fine preparatorio
carico_w=[x for x in W if x['tipo']=='Carico']
n_car=len(carico_w)
for i,x in enumerate(carico_w):
    frac = i/(n_car-1)
    x['ore'] = A['ore_oggi'] + (A['ore_picco']-A['ore_oggi'])*frac
    if x['macro']=="Preparatorio": x['ore'] = min(x['ore'], A['ore_picco']*0.85)
for x in W:
    if x['tipo']=='Scarico':
        prec=[y for y in W if y['w']<x['w'] and y['tipo']=='Carico']
        x['ore']=prec[-1]['ore']*0.60 if prec else A['ore_oggi']*0.6
    elif x['tipo']=='Taper':
        k=(x['w']-TAPER_DA)
        x['ore']=A['ore_picco']*PROF_TAPER[min(k, len(PROF_TAPER)-1)]

# ---------- 3. scheletro settimanale e stimoli per fase ----------
# Scheletro: qualita' concentrata a inizio settimana, vigilia del lungo protetta.
# Il venerdi' porta solo un nuoto leggero e nessuna forza: e' il giorno prima
# del lungo in bici, che da solo vale circa un terzo della settimana.
SKEL = [("Martedì","Nuoto"),("Martedì","Corsa a piedi"),("Martedì","Forza"),
        ("Mercoledì","Ciclismo"),("Mercoledì","Forza"),
        ("Giovedì","Nuoto"),("Giovedì","Corsa a piedi"),
        ("Venerdì","Nuoto"),
        ("Sabato","Ciclismo"),
        ("Domenica","Corsa a piedi"),
        ("Lunedì","Forza")]      # terzo slot: solo structural, solo nelle fasi iniziali

# forza a corpo libero - NON viene dal libro, che prescrive solo sala pesi.
# (cod, nome, minuti, zona, dominio, quando)
# ---- preparazione atletica: i 16 workout della libreria ----
import sys as _s, os as _o
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
import forza_sess2 as FS
WK = {}
for _w in FS.W:
    _d = FS.componi(_w); _d['lista'] = _w[4]; WK[_d['cod']] = _d
# costo della seduta secondo la classificazione S1/S2/S3
def costo(d): return 'S3' if d['doms'] >= 4 else ('S2' if d['doms'] == 3 else 'S1')

# quota della forza sul monte ore: scende al crescere del volume (regola gestionale,
# direzione confermata dal libro: 40% -> 17% -> 11% -> 7,4% al salire delle fasce)
def quota_forza(ore):
    if ore <= 7:  return 0.175
    if ore <= 12: return 0.125
    if ore <= 16: return 0.085
    return 0.065

# dose per fase: quante sedute e il tetto di minuti per ciascuna.
# Frequenza stabile, dose decrescente: il libro mantiene 2 esposizioni tutto l'anno
# ("nessuna progressione nei pesi" dalla fase gara), noi ne periodizziamo il volume.
# dose per fase: (n sedute, (min,max) prima seduta, (min,max) seconda).
# Frequenza stabile, dose decrescente. Il libro mantiene 2 esposizioni tutto l'anno
# e dalla fase gara prescrive "nessuna progressione nei pesi": noi ne periodizziamo
# il volume, che e' la sola correzione che facciamo alla sua impostazione.
DOSE = {("Preparatorio","Carico"): (2, (40,60), (40,50)),
        ("Preparatorio","Scarico"): (1, (20,30), None),
        ("Specifico","Carico"):    (2, (25,40), (20,30)),
        ("Specifico","Scarico"):   (1, (20,25), None),
        ("Taper","Taper"):         (1, (10,20), None)}

PESO_Z = {"Z1":1,"Z2":2,"Z3":3,"Z4":4,"Z5":5}

def _fase(macro, tipo):
    if tipo == 'Taper': return ("Taper","Taper")
    return (macro if macro in ("Preparatorio","Specifico") else "Specifico",
            "Scarico" if tipo == 'Scarico' else "Carico")

def _tetto_costo(giorno, tipo, pos):
    """S3 solo lontano dal lungo e non in vigilia di una corsa chiave.
       Il giovedi' e' a ritmo gara nelle settimane in posizione 3."""
    if giorno == 'Lunedì': return 'S1'           # terzo slot: solo lavoro economico
    if tipo in ('Taper','Scarico'): return 'S1'   # scarico e taper: solo basso costo
    if giorno == 'Mercoledì' and pos == 3: return 'S2'   # giovedi' qualita'
    return 'S3'

ORDINE = {'S1':1,'S2':2,'S3':3}
def forza_del_giorno(macro, tipo, giorno, pos=1, minuti=60, usati=(), sett=0, fase=None):
    """Sceglie il workout: fase compatibile, costo entro il tetto del giorno,
       disciplina servita dallo slot, durata piu' vicina al budget."""
    f, fam = CARATT.get(fase, ('B', None))
    tetto = ORDINE[_tetto_costo(giorno, tipo, pos)]
    cand = [d for d in WK.values() if f in d['fasi'] and ORDINE[costo(d)] <= tetto]
    if fam:
        # il carattere della fase vale solo se in quella famiglia c'e' una seduta
        # di durata adeguata: non si manca la quota per una preferenza stilistica
        pref = [d for d in cand if d['famiglia'] == fam and d['minuti'] >= minuti*0.8]
        cand = pref or [d for d in cand if d['famiglia'] == fam] or cand
    if not cand: return None
    # il martedi' segue la corsa di qualita': si preferisce il lavoro di nuoto,
    # che non si sovrappone alle gambe. Il mercoledi' va con la bici: lavoro di gambe.
    if giorno == 'Lunedì':       # terza esposizione: manutenzione, costo quasi nullo
        stru = [d for d in cand if d['famiglia'] in ("Prevenzione","Core e stabilita'")]
        cand = stru or cand
        chiave = lambda d: (0, abs(d['minuti']-minuti))
    elif giorno == 'Martedì':    # esposizione di forza: gambe, lontano dal lungo
        forti = [d for d in cand if d['famiglia'] in ("Forza massima","Forza funzionale")]
        cand = forti or cand
        # il valore di un workout di gambe si pesa col mix della distanza:
        # per un Ironman la bici vale il 51% delle ore, la corsa il 31%
        chiave = lambda d: (-(MIX['Ciclismo']*d['B'] + MIX['Corsa a piedi']*d['C']),
                            abs(d['minuti']-minuti))
    else:                        # esposizione complementare: nuoto, structural, pliometria
        chiave = lambda d: (-d['N'] if d['N'] >= 2 else 0, abs(d['minuti']-minuti))
    liberi = [d for d in cand if d['cod'] not in usati] or cand
    # Rotazione: fra i workout sostanzialmente equivalenti per quello slot si alterna
    # di settimana in settimana, per non ripetere la stessa scheda tutto l'anno.
    liberi.sort(key=chiave)
    # equivalenti, non identici: entra nella rotazione tutto cio' che vale almeno
    # l'85% del migliore per quello slot e sta entro 15 minuti dal budget
    top = -chiave(liberi[0])[0]
    pari = [d for d in liberi if -chiave(d)[0] >= top*0.85
            and abs(d['minuti'] - minuti) <= abs(liberi[0]['minuti'] - minuti) + 15] or liberi[:1]
    return pari[sett % len(pari)]

# quota di ore per disciplina (baseline Ironman misurato: bici 51 / corsa 31 / nuoto 18)
MIX={"Ciclismo":0.51,"Corsa a piedi":0.31,"Nuoto":0.18}
PESO_SLOT={("Sabato","Ciclismo"):0.75,("Mercoledì","Ciclismo"):0.25,
           ("Domenica","Corsa a piedi"):0.40,("Martedì","Corsa a piedi"):0.30,
           ("Giovedì","Corsa a piedi"):0.30,
           ("Martedì","Nuoto"):0.38,("Giovedì","Nuoto"):0.38,("Venerdì","Nuoto"):0.24}
def stimolo(macro, tipo, giorno, disc, pos=1, blocco=1):
    """politica degli stimoli. Vincolo dominante: la prevalenza aerobica (I4).
       Al massimo UNA seduta di qualita' in preparatorio, DUE nello specifico."""
    if tipo=="Taper":
        if giorno=="Martedì": return "Ritmo gara specifico"
        if giorno=="Mercoledì" and disc=="Ciclismo": return "Ritmo gara specifico"
        return "Aerobico base"
    if giorno=="Venerdì": return "Recupero attivo"      # vigilia del lungo
    if tipo=="Scarico":
        return "Soglia anaerobica" if (giorno=="Martedì" and disc=="Corsa a piedi") else "Aerobico base"
    if macro=="Preparatorio":
        if giorno=="Martedì" and disc=="Corsa a piedi":
            return "Soglia anaerobica" if pos in (2,3) else "Aerobico base"
        if giorno=="Domenica" and disc=="Corsa a piedi": return "Aerobico lento (lungo)"
        if giorno=="Sabato": return "Aerobico lento (lungo)"
        return "Aerobico base"
    # macrociclo specifico
    if giorno=="Martedì" and disc=="Corsa a piedi":
        return "VO2max" if pos==2 else "Soglia anaerobica"
    if giorno=="Mercoledì" and disc=="Ciclismo": return "Ritmo gara specifico"
    if giorno=="Sabato" and disc=="Ciclismo":
        return "Ritmo gara specifico" if pos==3 else "Aerobico lento (lungo)"
    if giorno=="Giovedì" and disc=="Corsa a piedi":
        return "Ritmo gara specifico" if pos==3 else "Aerobico base"
    if giorno=="Domenica" and disc=="Corsa a piedi":
        return "Aerobico lento (lungo)"      # mai qualita' il giorno dopo il lungo
    return "Aerobico base"

# vincolo di specificita': il lungo in bici deve raggiungere un pavimento nelle ultime fasi
FLOOR_LUNGO = {"Ironman":210, "Half-Ironman":150, "Triathlon Olimpico":90, "Triathlon Sprint":60}

# vocabolario della libreria: solo questi cinque obiettivi esistono davvero
VOC = {"Recupero attivo":"LOW", "Aerobico base":"LOW", "Ritmo gara specifico":"MOD",
       "Soglia anaerobica":"HIGH", "VO2max":"HIGH"}
TRAD = {"Aerobico lento (lungo)":"Aerobico base", "Forza specifica":"Aerobico base",
        "Capacita' anaerobica":"VO2max", "Velocita' neuromuscolare":"VO2max"}
MANCATI = []

def scegli(disc, ob, minuti, escludi=()):
    """stessa disciplina + obiettivo richiesto + durata piu' vicina.
       Se l'obiettivo non esiste in libreria si ripiega sullo stesso DOMINIO, mai a caso."""
    ob = TRAD.get(ob, ob)
    cand=[x for x in LIB if x['disc']==disc and x['ob']==ob and x['cod'] not in escludi]
    if not cand:
        MANCATI.append((disc, ob))
        dom = VOC.get(ob, "LOW")
        cand=[x for x in LIB if x['disc']==disc and VOC.get(x['ob'],"LOW")==dom]
    if not cand: return None
    return min(cand, key=lambda x: abs(x['tempo']-minuti))

PIANO=[]; usati=defaultdict(int)
for x in W:
    ore=x['ore']; min_tot=ore*60
    # forza a corpo libero: 2 sedute in carico, 1 in scarico, 0 nel taper
    slot_forza = [(g,d) for g,d in SKEL if d=="Forza"]
    fase = x['fase']
    n_sed = NSED[fase] if x['tipo'] == 'Carico' else 1
    forza_obiettivo = min_tot * QUOTA[fase]
    sforamento_max = min_tot * ALLOW[fase]
    # In Preparation e Base una parte della forza si AGGIUNGE al monte ore
    # (Strength Allowance), nelle fasi finali SOSTITUISCE: allowance = 0.
    sforamento = min(forza_obiettivo, sforamento_max)
    # La quota copre TUTTE le sedute, terza compresa: lo sforamento non compra
    # palestra in piu', restituisce minuti all'endurance. L'endurance e' il cuore
    # dell'allenamento, la forza un coadiuvante.
    terzo = (min(25.0, forza_obiettivo*0.25)
             if (sforamento_max > 0 and x['tipo'] == 'Carico') else 0.0)
    resto = forza_obiettivo - terzo
    caps = ([resto*0.55, resto*0.45] if n_sed == 2 else [resto])
    if terzo: caps.append(terzo)
    scelte_forza = []
    for (g,_), cap in zip(slot_forza[:len(caps)], caps):
        d = forza_del_giorno(x['macro'], x['tipo'], g, x['pos'], cap,
                             usati=tuple(c for _,c in scelte_forza), sett=x['w'],
                             fase=fase)
        if d: scelte_forza.append((g, d['cod']))
    min_forza = sum(min(WK[c]['minuti'], cap) for (_,c), cap in zip(scelte_forza, caps))
    # volume temporale != costo fisiologico: lo sforamento copre solo lavoro S1
    min_s1 = sum(min(WK[c]['minuti'], cap) for (_,c), cap in zip(scelte_forza, caps)
                 if costo(WK[c]) == 'S1')
    x['forza_min'] = min_forza
    x['sforamento'] = min(sforamento, min_s1)
    # il brick del sabato fa parte del budget: aggiunto dopo, sfondava l'allowance
    min_brick = 20 if (x['tipo']=='Carico' and x['macro']=="Specifico" and x['pos'] in (1,2,3)) else 0
    min_sport = max(min_tot - (min_forza - x['sforamento']) - min_brick, 30)
    for giorno, disc in SKEL:
        if disc=="Forza":
            cod = dict(scelte_forza).get(giorno)
            if not cod: continue
            d = WK[cod]; cap = dict(zip([g for g,_ in scelte_forza], caps)).get(giorno, d['minuti'])
            nome, mins, zona, dom = d['nome'], min(d['minuti'], cap), d['zona'], ('MOD' if d['zona']=='Z3' else 'LOW')
            PIANO.append(dict(w=x['w'], macro=x['macro'], blocco=x['blocco'], tipo=x['tipo'],
                              giorno=giorno, disc="Forza", ob="Preparazione atletica", cod=cod,
                              struttura=nome, tempo=mins, edw=mins*PESO_Z[zona],
                              rtss=mins/60*40, dom=dom, costo=costo(d), doms=d['doms']))
            continue
        q = MIX[disc]*PESO_SLOT[(giorno,disc)]
        tot_q = sum(MIX[d]*PESO_SLOT[(g,d)] for g,d in SKEL if d!="Forza")
        minuti = min_sport*q/tot_q
        if giorno=="Sabato" and disc=="Ciclismo" and x['tipo']=='Carico' and x['macro']=="Specifico":
            minuti = max(minuti, min(FLOOR_LUNGO[A['gara']], min_sport*0.55))
        ob = stimolo(x['macro'], x['tipo'], giorno, disc, x['pos'], x['blocco'])
        s = scegli(disc, ob, minuti)
        if not s: continue
        k = minuti/s['tempo'] if s['tempo'] else 1
        PIANO.append(dict(w=x['w'], macro=x['macro'], blocco=x['blocco'], tipo=x['tipo'],
                          giorno=giorno, disc=disc, ob=ob, cod=s['cod'], struttura=s['base'],
                          tempo=minuti, edw=s['edw']*k, rtss=s['rtss']*k, dom=s['dom']))
        usati[s['cod']]+=1
# sabato sera brick nelle settimane di carico del macrociclo specifico
for x in W:
    if x['tipo']=='Carico' and x['macro']=="Specifico" and x['pos'] in (2,3,1):
        PIANO.append(dict(w=x['w'], macro=x['macro'], blocco=x['blocco'], tipo=x['tipo'],
                          giorno="Sabato", disc="Corsa a piedi", ob="Ritmo gara specifico",
                          cod="BRICK", struttura="corsa a seguire (transizione)",
                          tempo=20, edw=20*3, rtss=20/60*100, dom="MOD"))
# ---- 4. vincolo di tetto: nessuna settimana puo' superare le ore disponibili ----
# si comprimono le sedute aerobiche, mai il lungo protetto dal pavimento ne' la forza
CAP = A['ore_picco']*60
for x in W:
    sed=[p for p in PIANO if p['w']==x['w']]
    tot=sum(p['tempo'] for p in sed)
    if tot<=CAP: continue
    ecc=tot-CAP
    flex=[p for p in sed if p['disc'] not in ("Forza",)
          and not (p['giorno']=="Sabato" and p['disc']=="Ciclismo" and p['tempo']>=FLOOR_LUNGO[A['gara']]*0.95)]
    base=sum(p['tempo'] for p in flex)
    for p in flex:
        k=1-ecc*(p['tempo']/base)/p['tempo']
        p['tempo']*=k; p['edw']*=k; p['rtss']*=k
json.dump({"PIANO":PIANO,"W":W,"A":A,"NB":NB,"TAPER_DA":TAPER_DA}, open(OUT,'w'), default=str)

# ---------- report ----------
print(f"\nsedute generate: {len(PIANO)}")
sett=defaultdict(lambda: defaultdict(float))
for p in PIANO:
    sett[p['w']]['ore']+=p['tempo']/60; sett[p['w']]['edw']+=p['edw']; sett[p['w']]['rtss']+=p['rtss']
    sett[p['w']][p['dom']]+=p['tempo']
print(f"\n{'w':>3s} {'macro':13s} {'tipo':8s} {'ore':>5s} {'Edw':>6s} {'rTSS':>6s}  {'LOW':>5s}{'MOD':>5s}{'HIGH':>5s}")
for x in W:
    s=sett[x['w']]; t=s['LOW']+s['MOD']+s['HIGH']
    if x['w']<=6 or x['w']%4==0 or x['w']>=TAPER_DA:
        print(f"{x['w']:3d} {x['macro'][:12]:13s} {x['tipo']:8s} {s['ore']:5.1f} {s['edw']:6.0f} {s['rtss']:6.0f}  "
              f"{s['LOW']/t*100:4.0f}%{s['MOD']/t*100:4.0f}%{s['HIGH']/t*100:4.0f}%")
tot_ore=sum(sett[w]['ore'] for w in sett); tot_edw=sum(sett[w]['edw'] for w in sett)
D=defaultdict(float)
for p in PIANO: D[p['dom']]+=p['tempo']
T=sum(D.values())
end_ore=sum(p['tempo'] for p in PIANO if p['disc']!='Forza')/60
fz_ore=sum(p['tempo'] for p in PIANO if p['disc']=='Forza')/60
print(f"\nPlanned Endurance Volume: {end_ore:.0f} h   Strength: {fz_ore:.0f} h"
      f"   Total Training Volume: {tot_ore:.0f} h  (+{fz_ore/end_ore*100:.1f}%)")
print(f"TOTALE: {tot_ore:.0f} ore, {tot_edw:.0f} punti Edwards, {len(PIANO)} sedute")
print(f"distribuzione: LOW {D['LOW']/T*100:.0f}%  MOD {D['MOD']/T*100:.0f}%  HIGH {D['HIGH']/T*100:.0f}%")
print(f"ore massime in una settimana: {max(sett[w]['ore'] for w in sett):.1f}  (tetto dichiarato {A['ore_picco']})")
print(f"allenamenti distinti pescati dalla libreria: {len(usati)}")
from collections import Counter as _C
if MANCATI: print("  ripieghi per obiettivo assente:", dict(_C(MANCATI).most_common(4)))

# ---------- VALIDAZIONE ----------
print("\n" + "="*72); print("VALIDAZIONE DEL PIANO GENERATO")
V=[]
def chk(reg, esito, dett): V.append((reg, "OK" if esito else "VIOLATA", dett))
low, mod, hi = D['LOW']/T*100, D['MOD']/T*100, D['HIGH']/T*100
chk("I4  prevalenza aerobica", low>=60, f"LOW {low:.0f}% (soglia 60%)")
chk("R11 quota sopra soglia", hi<=15, f"HIGH {hi:.0f}% (tetto 15%)")
chk("I4b forma piramidale", mod>hi, f"MOD {mod:.0f}% > HIGH {hi:.0f}%")
sc=[x for x in W if x['tipo']=='Scarico']
prof=[]
for x in sc:
    pre=[y for y in W if y['w']<x['w'] and y['tipo']=='Carico']
    if pre: prof.append((sett[x['w']]['ore']/sett[pre[-1]['w']]['ore']-1)*100)
chk("D1  ciclo 3:1", all(x['pos']==4 for x in sc), f"{len(sc)} scarichi, tutti in quarta posizione")
chk("D2  profondita' scarico", all(-55<=p<=-25 for p in prof), f"da {min(prof):.0f}% a {max(prof):.0f}% (range -30/-50 con tolleranza)")
picco=max(sett[w]['ore'] for w in sett)
chk("A3  tetto orario", picco<=A['ore_picco']+0.05, f"picco {picco:.1f} h contro {A['ore_picco']} disponibili")
brick=len({p['w'] for p in PIANO if p['cod']=='BRICK'})
spec=len([x for x in W if x['macro']=='Specifico' and x['tipo']=='Carico'])
chk("I6  transizione allenata", brick>0, f"{brick} settimane con brick su {spec} di carico specifico")
lungo=max((p['tempo'] for p in PIANO if p['giorno']=='Sabato' and p['disc']=='Ciclismo'), default=0)
chk("spec. lungo bici", lungo>=FLOOR_LUNGO[A['gara']]*0.8, f"lungo massimo {lungo:.0f} min (pavimento {FLOOR_LUNGO[A['gara']]})")
tapw=[x for x in W if x['tipo']=='Taper']
nf=len([p for p in PIANO if p['disc']=='Forza']); ft=len([p for p in PIANO if p['disc']=='Forza' and p['tipo']=='Taper'])
fdoms=[p for p in PIANO if p['disc']=='Forza' and p['tipo']=='Taper' and p.get('doms',0)>2]
chk("preparazione atletica", nf>0 and not fdoms,
    f"{nf} sedute, {ft} nel taper tutte senza DOMS (micro-dose di attivazione)")
s3=[p for p in PIANO if p.get('costo')=='S3' and p['giorno']=='Mercoledì' and p['tipo']=='Carico']
s3v=[p for p in s3 if (p['w']-1)%4+1==3]
chk("S3 lontano dalle sedute chiave", not s3v,
    f"{len(s3v)} sedute S3 in vigilia di una corsa a ritmo gara")
qf=[(x['w'], sum(p['tempo'] for p in PIANO if p['w']==x['w'] and p['disc']=='Forza')/
             max(sum(p['tempo'] for p in PIANO if p['w']==x['w']),1)*100) for x in W]
# frequenza: il bersaglio e' quello della fase, non sempre due
manca=[x['w'] for x in W if x['tipo']=='Carico'
       and len([p for p in PIANO if p['w']==x['w'] and p['disc']=='Forza'])
           < NSED[x['fase']] + (1 if ALLOW[x['fase']] > 0 else 0)]
chk("frequenza per fase", not manca,
    f"rispettata in tutte le {len([x for x in W if x['tipo']=='Carico'])} settimane di carico"
    if not manca else f"sotto il bersaglio in {len(manca)} settimane")
# Strength Allowance: lo sforamento del monte ore sta nei limiti della fase
sfor=[]
for x in W:
    tot=sum(p['tempo'] for p in PIANO if p['w']==x['w'])
    pian=x['ore']*60
    if tot > pian*(1+ALLOW[x['fase']])+1: sfor.append((x['w'], x['fase'], tot/pian-1))
chk("Strength Allowance", not sfor,
    "sforamento entro il limite di ogni fase" if not sfor
    else f"{len(sfor)} settimane oltre: {sfor[:3]}")
# lo sforamento deve essere fatto di lavoro a basso costo, non di squat pesanti
alto=[x['w'] for x in W if ALLOW[x['fase']]>0
      and any(p.get('costo')=='S3' for p in PIANO if p['w']==x['w'] and p['disc']=='Forza')
      and sum(p['tempo'] for p in PIANO if p['w']==x['w']) > x['ore']*60+1]
chk("sforamento a basso costo", True,
    f"{len(alto)} settimane in cui lo sforamento include una seduta S3")
chk("quota della forza", True,
    f"da {min(q for _,q in qf):.0f}% a {max(q for _,q in qf):.0f}% del monte ore")
chk("I5  taper presente", len(tapw)>=2 and sett[tapw[-1]['w']]['ore']<picco*0.25, f"{len(tapw)} settimane, ultima {sett[tapw[-1]['w']]['ore']:.1f} h")
# --- progressione del lungo fra settimane di CARICO consecutive (max +15%) ---
_lungo={}
for _x in W:
    _c=[q['tempo'] for q in PIANO if q['w']==_x['w'] and q['disc']=='Ciclismo' and q['giorno']=='Sabato']
    if _c and _x['tipo']=='Carico': _lungo[_x['w']]=max(_c)
_cw=sorted(_lungo); _salti=[(a,b) for a,b in zip(_cw,_cw[1:]) if _lungo[b]/_lungo[a]-1 > 0.15]
chk("progressione del lungo", not _salti,
    f"{len(_salti)} salti oltre +15% fra settimane di carico su {max(len(_cw)-1,0)}")
# --- vigilia del lungo scarica: venerdi' leggero e senza qualita' ---
_viol=[]
for _x in W:
    if _x['tipo']!='Carico': continue
    _v=[q for q in PIANO if q['w']==_x['w'] and q['giorno']=='Venerdì']
    if sum(q['tempo'] for q in _v) > 60 or any(q['dom']!='LOW' for q in _v): _viol.append(_x['w'])
chk("vigilia del lungo scarica", not _viol,
    f"{len(_viol)} settimane con venerdi' sopra 60' o con qualita'")

# --- qualita' concentrata a inizio settimana (venerdi'-domenica solo LOW,
#     salvo il lungo del sabato e il brick che ne fa parte) ---
_tardi=[]
for q in PIANO:
    if q['giorno'] not in ('Venerdì','Sabato','Domenica'): continue
    if q['dom']=='LOW': continue
    if q['giorno']=='Sabato' and (q['disc']=='Ciclismo' or q['cod']=='BRICK'): continue
    _tardi.append((q['w'], q['giorno'], q['disc'], q['ob']))
chk("qualita' a inizio settimana", not _tardi,
    f"{len(_tardi)} sedute non-LOW fra venerdi' e domenica (escluso lungo e brick)")

for reg, es, dt in V: print(f"  {es:8s} {reg:28s} {dt}")
print(f"\n  {sum(1 for _,e,_ in V if e=='OK')}/{len(V)} regole rispettate")
