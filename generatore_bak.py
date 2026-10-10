# -*- coding: utf-8 -*-
"""Generatore di piani: dalla dottrina al piano, pescando dalla libreria."""
from openpyxl import load_workbook
from collections import defaultdict
import math, json

F='/mnt/user-data/outputs/Piani_Triathlon_Sprint_Olimpico_Half-Ironman_Ironman.xlsx'
wb=load_workbook(F, data_only=True)

# ---------- libreria ----------
LIB=[]
for r in wb['Variazioni Allenamenti'].iter_rows(min_row=6, values_only=True):
    if not r[0] or r[24]!='Si' or r[27]!='No': continue      # plausibile e non ridondante
    if not r[11] or not r[21]: continue
    LIB.append(dict(cod=r[0], base=r[1], arch=r[2], disc=r[3], ob_libro=r[4],
                    zona=r[13], ob=r[14], dist=r[10], tempo=r[11],
                    edw=r[21], ban=r[22], rtss=r[23]))
print(f"libreria utilizzabile: {len(LIB)} allenamenti")
DOM={'Z1':'LOW','Z2':'LOW','Z3':'MOD','Z4':'HIGH','Z5':'HIGH'}
for x in LIB: x['dom']=DOM.get(x['zona'],'LOW')

# ---------- input atleta ----------
A = dict(gara="Ironman", settimane=36, ore_picco=11.0, ore_oggi=5.0,
         sedute_sett=8, giorno_riposo="Lunedì")

# ---------- 1. architettura ----------
def architettura(n):
    """>20 settimane: due macrocicli. Blocchi di 4 (3 carico + 1 scarico)."""
    blocchi = n//4
    if n <= 20:
        return [("Macrociclo unico", list(range(1, blocchi)))], blocchi
    prep = blocchi//2
    return [("Preparatorio", list(range(1, prep+1))), ("Specifico", list(range(prep+1, blocchi)))], blocchi
MACRO, NB = architettura(A['settimane'])
TAPER_DA = (NB-1)*4+1     # ultimo blocco = taper
print(f"architettura: {A['settimane']} settimane = {NB} blocchi da 4; taper dalla settimana {TAPER_DA}")

# ---------- 2. calendario e carico settimanale ----------
def settimane():
    out=[]
    for w in range(1, A['settimane']+1):
        blocco=(w-1)//4+1; pos=(w-1)%4+1
        macro = next((m for m,bs in MACRO if blocco in bs), "Taper")
        if w >= TAPER_DA: tipo, macro = "Taper", "Taper"
        elif pos==4:      tipo = "Scarico"
        else:             tipo = "Carico"
        out.append(dict(w=w, blocco=blocco, pos=pos, macro=macro, tipo=tipo))
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
        x['ore']=A['ore_picco']*[0.55,0.40,0.25,0.12][min(k,3)]

# ---------- 3. scheletro settimanale e stimoli per fase ----------
SKEL = [("Martedì","Corsa a piedi"),("Mercoledì","Nuoto"),("Mercoledì","Forza"),
        ("Giovedì","Ciclismo"),("Venerdì","Nuoto"),("Venerdì","Forza"),("Sabato","Ciclismo"),
        ("Domenica","Corsa a piedi"),("Domenica","Nuoto")]

# forza a corpo libero - NON viene dal libro, che prescrive solo sala pesi.
# (cod, nome, minuti, zona, dominio, quando)
FORZA = {
 "BW-01": ("Forza generale a corpo libero - circuito full body, 3-4 giri", 35, "Z2", "LOW"),
 "BW-02": ("Resistenza muscolare - circuito lungo ad alte ripetizioni",    40, "Z2", "LOW"),
 "BW-03": ("Core e stabilita' - catena posteriore, anti-rotazione",        25, "Z1", "LOW"),
 "BW-04": ("Forza specifica triathlon - monopodalico, spinte, trazioni",   35, "Z2", "LOW"),
 "BW-05": ("Pliometria e reattivita' - balzi e salti, volume basso",       30, "Z3", "MOD"),
}
PESO_Z = {"Z1":1,"Z2":2,"Z3":3,"Z4":4,"Z5":5}
def forza_del_giorno(macro, tipo, giorno):
    """politica della forza. Nel taper si elimina, come prescrive il libro per pesi e pliometria."""
    if tipo == "Taper":   return None
    if tipo == "Scarico": return "BW-03"
    if macro == "Preparatorio": return "BW-01" if giorno == "Mercoledì" else "BW-02"
    return "BW-04" if giorno == "Mercoledì" else "BW-05"
# quota di ore per disciplina (baseline Ironman misurato: bici 51 / corsa 31 / nuoto 18)
MIX={"Ciclismo":0.51,"Corsa a piedi":0.31,"Nuoto":0.18}
PESO_SLOT={("Sabato","Ciclismo"):0.72,("Giovedì","Ciclismo"):0.28,
           ("Domenica","Corsa a piedi"):0.62,("Martedì","Corsa a piedi"):0.38,
           ("Mercoledì","Nuoto"):0.33,("Venerdì","Nuoto"):0.30,("Domenica","Nuoto"):0.37}
def stimolo(macro, tipo, giorno, disc, pos=1, blocco=1):
    """politica degli stimoli. Vincolo dominante: la prevalenza aerobica (I4).
       Al massimo UNA seduta di qualita' in preparatorio, DUE nello specifico."""
    if tipo=="Taper":
        if giorno=="Martedì": return "Ritmo gara specifico"
        if giorno=="Giovedì" and disc=="Ciclismo": return "Ritmo gara specifico"
        return "Aerobico base"
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
    if giorno=="Giovedì" and disc=="Ciclismo": return "Ritmo gara specifico"
    if giorno=="Sabato" and disc=="Ciclismo":
        return "Ritmo gara specifico" if pos==3 else "Aerobico lento (lungo)"
    if giorno=="Domenica" and disc=="Corsa a piedi":
        return "Ritmo gara specifico" if pos==3 else "Aerobico lento (lungo)"
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
    scelte_forza = [(g, forza_del_giorno(x['macro'], x['tipo'], g)) for g,_ in slot_forza]
    scelte_forza = [(g,c) for g,c in scelte_forza if c]
    if x['tipo']=='Scarico': scelte_forza = scelte_forza[:1]
    min_forza = sum(FORZA[c][1] for _,c in scelte_forza)
    min_sport = max(min_tot-min_forza, 30)
    for giorno, disc in SKEL:
        if disc=="Forza":
            cod = dict(scelte_forza).get(giorno)
            if not cod: continue
            nome, mins, zona, dom = FORZA[cod]
            PIANO.append(dict(w=x['w'], macro=x['macro'], blocco=x['blocco'], tipo=x['tipo'],
                              giorno=giorno, disc="Forza", ob="Forza a corpo libero", cod=cod,
                              struttura=nome, tempo=mins, edw=mins*PESO_Z[zona],
                              rtss=mins/60*40, dom=dom))
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
    if x['tipo']=='Carico' and x['macro']=="Specifico" and x['pos'] in (2,3):
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
json.dump({"PIANO":PIANO,"W":W,"A":A,"NB":NB,"TAPER_DA":TAPER_DA}, open('piano.json','w'), default=str)

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
print(f"\nTOTALE: {tot_ore:.0f} ore, {tot_edw:.0f} punti Edwards, {len(PIANO)} sedute")
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
chk("forza a corpo libero", nf>0 and ft==0, f"{nf} sedute, nessuna nel taper (pesi e pliometria eliminati prima della gara)")
chk("I5  taper presente", len(tapw)>=2 and sett[tapw[-1]['w']]['ore']<picco*0.25, f"{len(tapw)} settimane, ultima {sett[tapw[-1]['w']]['ore']:.1f} h")
for reg, es, dt in V: print(f"  {es:8s} {reg:28s} {dt}")
print(f"\n  {sum(1 for _,e,_ in V if e=='OK')}/{len(V)} regole rispettate")
