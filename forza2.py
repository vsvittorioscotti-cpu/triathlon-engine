# -*- coding: utf-8 -*-
"""Libreria unificata: fonde la prima impostazione (6 famiglie) con il secondo
database (categorie/sottocategorie, costo di fatica, rischio DOMS, collocazione,
alternative, ripetizioni diverse fra base e peak).
Entrambe le fonti sono di Vittorio (10/10/2026). NON derivano dal libro."""
import sys
sys.path.insert(0,'/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad')
from forza_lib import ESERCIZI as BASE1, IDX as IDX1

# ---- esercizi presenti solo nel secondo database ----
# nome|famiglia|distretto|funzione|attrezzo|N|B|C|serie|rip|rec|livello|fasi
RAW2 = """
Belt Squat|Forza massima|quadricipiti/glutei|forza con minor carico lombare|macchina|0|3|2|4|6|150|int|BU
Reverse Sled Drag|Forza funzionale|quadricipiti|forza-resistenza in spinta|slitta|0|3|2|4|25|90|prn|BU
Sled Push|Forza funzionale|quadricipiti/glutei|forza orizzontale|slitta|0|2|2|4|20|90|prn|BU
Cable Pull Through|Forza funzionale|glutei/femorali|schema di hip hinge|cavi|0|2|2|3|12|75|prn|BU
Wall Sit|Forza funzionale|quadricipiti|resistenza locale isometrica|corpo libero|0|2|1|3|45|60|prn|B
Nordic Hamstring|Forza funzionale|femorali|forza eccentrica dei femorali|partner/panca|0|2|3|3|6|120|avz|BU
Clamshell|Prevenzione|gluteo medio|attivazione dell'anca|elastico|0|2|3|2|15|40|prn|BUSP
Banded Hip Extension|Prevenzione|glutei|estensione dell'anca|elastico|0|2|2|3|15|45|prn|BUSP
One-arm Cable Pulldown|Forza funzionale|dorsale|trazione verticale unilaterale|cavi|3|0|0|3|8|90|int|BUSP
Cable Press|Forza funzionale|pettorali/tricipiti|spinta orizzontale al cavo|cavi|2|0|0|3|10|75|prn|BU
Half-kneeling Pallof|Core e stabilita'|obliqui/core|anti-rotazione in appoggio instabile|cavi|3|3|3|3|10|60|prn|BUSP
Cable Anti-Rotation Hold|Core e stabilita'|obliqui|anti-rotazione isometrica|cavi|3|3|3|3|25|60|prn|BUSP
Bear Plank Shoulder Tap|Core e stabilita'|core/spalle|anti-rotazione in quadrupedia|corpo libero|3|2|3|3|16|45|int|BUSP
Offset Farmer Carry|Core e stabilita'|core laterale|anti-inclinazione asimmetrica|manubri|2|3|3|3|30|60|int|BUS
Front Rack Carry|Core e stabilita'|core/tronco|rigidita' del tronco in posizione alta|bilanciere|2|3|3|3|25|75|int|BU
Overhead Carry|Core e stabilita'|spalla/scapole|stabilita' sopra la testa|manubri|3|1|1|3|20|75|avz|BU
Half-kneeling Cable Rotation|Core e stabilita'|obliqui|rotazione controllata|cavi|3|2|2|3|10|60|int|BUS
Low Pogo|Pliometria|piede/caviglia|stiffness a basso impatto|corpo libero|0|1|3|3|20|45|prn|BUSP
Line Hop|Pliometria|caviglia|contatti rapidi|corpo libero|0|1|2|3|20|45|prn|BUS
Reactive Hurdle Jump|Pliometria|catena inferiore|reattivita' su ostacoli|ostacoli|0|1|3|3|6|120|avz|US
Repeated Pogo|Pliometria|piede/caviglia/soleo|stiffness ripetuta|corpo libero|0|1|3|3|25|60|int|BUS
Reactive Box Jump|Pliometria|catena inferiore|potenza reattiva|box|0|1|3|3|5|120|avz|US
Single-leg Broad Jump|Pliometria|glutei/femorali|potenza orizzontale monopodalica|corpo libero|0|1|3|3|4|120|avz|US
Straight-leg Bounds|Pliometria|polpaccio/femorali|propulsione a ginocchio esteso|corpo libero|0|0|3|3|20|90|avz|US
Quick Contacts|Pliometria|caviglia|tempo di contatto minimo|corpo libero|0|0|3|3|15|60|int|BUSP
Rotational Wall Throw|Pliometria|core/rotazione|potenza rotazionale al muro|palla medica|3|2|1|4|6|75|prn|BUS
Scoop Throw|Pliometria|catena posteriore/core|potenza di lancio dal basso|palla medica|3|2|1|3|6|75|prn|BUS
Reverse Scoop Throw|Pliometria|catena posteriore|estensione esplosiva|palla medica|3|2|1|3|6|75|int|BUS
Cossack Squat|Bodyweight|adduttori/glutei|mobilita' e forza sul piano frontale|corpo libero|0|2|2|3|8|60|int|BU
Forward Lunge|Bodyweight|quadricipiti/glutei|schema di affondo|corpo libero|0|2|2|3|10|60|prn|B
Hamstring Walkout|Bodyweight|femorali|controllo eccentrico dei femorali|corpo libero|0|1|3|3|8|60|prn|BU
Wide Push-up|Bodyweight|petto/spalle|variante di spinta|corpo libero|2|0|0|3|12|60|prn|B
Neutral Grip Pull-up|Bodyweight|dorsali|trazione a presa neutra|sbarra|3|0|0|3|6|120|int|BUSP
Inverted Row|Bodyweight|dorsali|trazione orizzontale|sbarra bassa|3|1|1|3|12|60|prn|BUSP
Bench Dip|Bodyweight|tricipiti|spinta assistita|panca|2|0|0|3|12|60|prn|B
Walking Plank|Core e stabilita'|core/spalle|anti-rotazione in transizione|corpo libero|2|2|2|3|12|45|prn|BU
Plank Jack|Bodyweight|core/conditioning|core sotto frequenza|corpo libero|1|1|1|3|20|45|prn|B
Lunge + Knee Drive|Bodyweight|glutei/flessori anca|affondo con spinta|corpo libero|0|2|3|3|12|60|prn|BU
High Knees|Bodyweight|flessori anca|conditioning e frequenza|corpo libero|0|1|2|3|30|45|prn|B
Skater|Bodyweight|gluteo medio|conditioning laterale|corpo libero|0|1|2|3|20|45|prn|B
Mountain Climber|Bodyweight|core/conditioning|conditioning generale|corpo libero|1|1|1|3|30|45|prn|B
"""

def _riga(l):
    c=[x.strip() for x in l.split('|')]
    return dict(nome=c[0],famiglia=c[1],distretto=c[2],funzione=c[3],attrezzo=c[4],
                N=int(c[5]),B=int(c[6]),C=int(c[7]),serie=int(c[8]),rip=int(c[9]),
                rec=int(c[10]),livello=c[11],fasi=c[12])

NUOVI = [_riga(l) for l in RAW2.strip().split('\n') if l.strip()]
ESERCIZI = BASE1 + [e for e in NUOVI if e['nome'] not in IDX1]
IDX = {e['nome']: e for e in ESERCIZI}

# ---------------- campi del secondo database ----------------
# Sottocategoria: dedotta dal distretto e dalla funzione
def sottocategoria(e):
    f, d = e['funzione'].lower(), e['distretto'].lower()
    if 'monopodalic' in f or 'unilateral' in f or 'single' in e['nome'].lower() or 'split' in e['nome'].lower(): return 'Single leg'
    if 'scapol' in d or 'cuffia' in d or 'trapezio' in d or 'dentato' in d or 'romboid' in d: return 'Spalla e scapola'
    if 'anti-' in f: return 'Anti-movimento'
    if 'rotazion' in f: return 'Rotazione'
    if 'trazione' in f or 'passata' in f: return 'Trazione'
    if 'spinta' in f: return 'Spinta'
    if 'scapol' in d or 'cuffia' in d: return 'Spalla e scapola'
    if 'piede' in d or 'caviglia' in d or 'soleo' in d or 'polpacc' in d or 'tibiale' in d or 'achille' in d: return 'Piede e caviglia'
    if 'gluteo medio' in d or 'adduttor' in d or 'abduttor' in d: return 'Stabilita anca'
    if e['famiglia']=='Pliometria': return 'Pliometria'
    return 'Bilaterale'

# Costo di fatica e rischio DOMS: regole esplicite, non valori a caso
# due livelli di eccentrico: il Nordic e i balzi sono un'altra cosa rispetto
# agli heel drop, che nei protocolli di tendine si fanno anche tutti i giorni
ECC_ALTO  = ('Nordic','Depth Jump','Drop Jump','Bounds','Straight-leg Bounds',
             'Single-leg Broad Jump','Reactive Hurdle')
ECC_MEDIO = ('Eccentric','Step-down','Walking Lunge','Hamstring Walkout')
ECC = ECC_ALTO + ECC_MEDIO
PESANTI = ('bilanciere','trap bar','slitta')
def fatica(e):
    if e['famiglia']=='Prevenzione': return 1
    if e['famiglia']=="Core e stabilita'": return 2
    if e['famiglia']=='Forza massima': return 5 if e['attrezzo'] in PESANTI else 4
    if e['famiglia']=='Forza funzionale': return 3
    if e['famiglia']=='Pliometria':
        return 5 if any(k in e['nome'] for k in ECC) else (2 if 'Pogo' in e['nome'] or 'Skip' in e['nome'] or 'Ankl' in e['nome'] else 3)
    return 3   # Bodyweight
def doms(e):
    if any(k in e['nome'] for k in ECC_ALTO): return 5
    if any(k in e['nome'] for k in ECC_MEDIO): return 3
    f = fatica(e)
    if e['famiglia']=='Prevenzione': return 1
    if e['famiglia']=="Core e stabilita'": return 2
    d = max(2, f-1)
    # il monopodalico sotto carico e' piu' doloroso di quanto dica la famiglia:
    # posizione profonda e componente eccentrica (riscontro di Vittorio sul Bulgarian)
    if sottocategoria(e)=='Single leg' and e['attrezzo'] not in ('corpo libero','elastico'): d += 1
    return min(5, d)

# Collocazione rispetto alle sedute chiave (deriva da D9 e dal principio
# "hard days hard, easy days easy")
def collocazione(e):
    d, f = doms(e), fatica(e)
    if d <= 2 and f <= 2: return 'libera, anche nei giorni facili'
    if d >= 4: return 'almeno 48 h prima del lungo'
    return 'nei giorni gia impegnativi, mai in vigilia del lungo'

# Ripetizioni: il secondo database distingue base da peak
def reps(e):
    r = e['rip']
    if e['famiglia'] in ('Forza massima','Forza funzionale') and r <= 12:
        return f"{r}-{r+2}", f"{max(3, r-2)}-{max(4, r-1)}"
    return f"{r}", f"{max(1, int(r*0.7))}"

# Alternative: stessa sottocategoria, stesso distretto o profilo di disciplina vicino,
# con costo di fatica uguale o inferiore
def alternative(e, n=2):
    cand = [x for x in ESERCIZI if x['nome'] != e['nome']
            and sottocategoria(x) == sottocategoria(e)
            and fatica(x) <= fatica(e)]
    cand.sort(key=lambda x: (abs(x['N']-e['N'])+abs(x['B']-e['B'])+abs(x['C']-e['C']),
                             abs(fatica(x)-fatica(e))))
    return ' / '.join(x['nome'] for x in cand[:n]) or '-'

def scheda(e):
    rb, rp = reps(e)
    return dict(e, sottocat=sottocategoria(e), fatica=fatica(e), doms=doms(e),
                collocazione=collocazione(e), reps_base=rb, reps_peak=rp,
                alternative=alternative(e))

if __name__ == '__main__':
    from collections import Counter
    print(f"prima libreria: {len(BASE1)}   nuovi dal secondo database: {len(ESERCIZI)-len(BASE1)}   totale: {len(ESERCIZI)}")
    gia = [e['nome'] for e in NUOVI if e['nome'] in IDX1]
    if gia: print(f"gia presenti, non duplicati: {len(gia)} -> {', '.join(gia)}")
    print("\ncosto di fatica (1 = minimo, 5 = massimo):")
    for k,v in sorted(Counter(fatica(e) for e in ESERCIZI).items()): print(f"  {k}: {v:3d} esercizi")
    print("\nrischio DOMS:")
    for k,v in sorted(Counter(doms(e) for e in ESERCIZI).items()): print(f"  {k}: {v:3d} esercizi")
    print("\ncollocazione:")
    for k,v in Counter(collocazione(e) for e in ESERCIZI).most_common(): print(f"  {k:<42}{v:3d}")
    print("\nsottocategorie:")
    for k,v in Counter(sottocategoria(e) for e in ESERCIZI).most_common(): print(f"  {k:<22}{v:3d}")
    print("\nesempio di scheda completa:")
    s = scheda(IDX['Bulgarian Split Squat'])
    for k in ('nome','famiglia','sottocat','distretto','N','B','C','reps_base','reps_peak',
              'serie','rec','fatica','doms','collocazione','alternative'):
        print(f"  {k:<14}{s[k]}")
