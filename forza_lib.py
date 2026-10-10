# -*- coding: utf-8 -*-
"""Libreria di preparazione atletica per il triatleta.
Fonte: impostazione e liste fornite da Vittorio (10/10/2026). NON viene dal libro.
Campi: nome | famiglia | distretto | funzione | attrezzo | N | B | C | serie | rip | rec_s | livello | fasi
  N/B/C = trasferimento su Nuoto / Bici / Corsa, da 0 (nessuno) a 3 (molto alto)
  fasi  = B(ase) U(build) S(pecifico) P(eak)  -- il taper e' gestito a parte
"""
FAMIGLIE = ["Forza massima", "Forza funzionale", "Core e stabilita'",
            "Prevenzione", "Pliometria", "Bodyweight"]

RAW = """
Back Squat|Forza massima|quadricipiti/glutei/core|forza generale arti inferiori|bilanciere|0|3|3|4|5|180|int|BU
Front Squat|Forza massima|quadricipiti/core|forza e controllo del tronco|bilanciere|0|3|3|4|5|180|avz|BU
Trap Bar Deadlift|Forza massima|glutei/femorali/quadricipiti|estensione potente dell'anca|trap bar|0|3|3|4|4|180|int|BUS
Romanian Deadlift|Forza massima|femorali/glutei|catena posteriore|bilanciere|0|3|3|3|6|150|int|BUS
Leg Press|Forza massima|quadricipiti/glutei|forza elevata a basso rischio|macchina|0|3|2|4|8|150|prn|BU
Hack Squat|Forza massima|quadricipiti|sviluppo forza quadricipite|macchina|0|2|2|3|8|150|int|BU
Hip Thrust|Forza massima|glutei|estensione dell'anca|bilanciere|0|3|2|4|8|120|prn|BUS
Bulgarian Split Squat|Forza funzionale|glutei/quadricipiti|forza monopodalica|manubri|0|3|3|3|6|120|int|BUSP
Split Squat|Forza funzionale|quadricipiti/glutei|controllo monopodalico|manubri|0|2|3|3|8|90|prn|BU
Reverse Lunge|Forza funzionale|glutei/quadricipiti|forza e stabilita'|manubri|0|2|3|3|8|90|prn|BU
Walking Lunge|Forza funzionale|glutei/quadricipiti|forza dinamica|manubri|0|2|3|3|10|90|prn|BU
Step-up alto|Forza funzionale|glutei/quadricipiti|estensione dell'anca|panca/manubri|0|3|3|3|8|90|prn|BUS
Step-down|Forza funzionale|quadricipiti/gluteo medio|controllo eccentrico|panca|0|1|3|3|8|90|prn|BU
Single-leg Leg Press|Forza funzionale|quadricipiti/glutei|forza unilaterale controllata|macchina|0|3|3|3|8|120|prn|BU
Single-leg RDL|Forza funzionale|femorali/glutei|stabilita' e catena posteriore|manubri|0|2|3|3|6|90|int|BUSP
Leg Extension|Forza massima|quadricipiti|accessorio quadricipite|macchina|0|2|1|3|12|90|prn|B
Leg Curl|Forza massima|femorali|equilibrio muscolare|macchina|0|2|2|3|12|90|prn|B
Standing Calf Raise|Prevenzione|gastrocnemio|spinta e ritorno elastico|macchina/manubri|0|1|3|3|8|90|prn|BUSP
Seated Calf Raise|Prevenzione|soleo|resistenza del soleo|macchina|0|1|3|3|10|90|prn|BUSP
Single-leg Calf Raise|Prevenzione|soleo/gastrocnemio|forza monopodalica del polpaccio|corpo libero|0|1|3|3|12|60|prn|BUSP
Bent-knee Calf Raise|Prevenzione|soleo|isolamento del soleo|corpo libero|0|1|3|3|15|60|prn|BUSP
Tibialis Raise|Prevenzione|tibiale anteriore|equilibrio anteriore della gamba|corpo libero|0|1|3|3|15|45|prn|BUSP
Toe Raises|Prevenzione|tibiale|controllo della caviglia|corpo libero|0|0|2|2|15|45|prn|BU
Farmer Walk sulle punte|Prevenzione|polpacci/piede|forza del piede sotto carico|manubri|0|1|2|3|20|60|int|BU
Short Foot Exercise|Prevenzione|arco plantare|sostegno dell'arco|corpo libero|0|0|2|2|10|30|prn|BUSP
Toe Yoga|Prevenzione|intrinseci del piede|controllo delle dita|corpo libero|0|0|2|2|10|30|prn|BU
Eccentric Heel Drops|Prevenzione|polpaccio/Achille|tolleranza del tendine|gradino|0|1|3|3|12|60|prn|BUSP
Lateral Band Walk|Prevenzione|gluteo medio|stabilita' laterale del bacino|elastico|0|2|3|2|15|45|prn|BUSP
Monster Walk|Prevenzione|gluteo medio|attivazione dell'anca|elastico|0|2|3|2|12|45|prn|BUSP
Hip Airplane|Prevenzione|gluteo/controllo anca|controllo rotazionale dell'anca|corpo libero|0|1|3|2|8|45|avz|BUS
Copenhagen Plank|Prevenzione|adduttori|robustezza degli adduttori|panca|0|2|3|2|25|45|avz|BUSP
Single-leg Glute Bridge|Forza funzionale|gluteo|estensione monopodalica|corpo libero|0|2|3|3|12|60|prn|BUSP
Single-leg Hip Thrust|Forza funzionale|gluteo|estensione con stabilizzazione|panca|0|3|3|3|10|90|int|BUS
Cable Hip Abduction|Prevenzione|abduttori|controllo frontale del bacino|cavi|0|1|2|3|12|60|prn|BU
Cable Hip Adduction|Prevenzione|adduttori|equilibrio adduttori-abduttori|cavi|0|1|2|3|12|60|prn|BU
Side Plank + Leg Raise|Core e stabilita'|gluteo medio/core|stabilita' laterale sotto carico|corpo libero|2|3|3|3|10|45|int|BUSP
Pogo Jumps|Pliometria|piede/caviglia/soleo|stiffness e ritorno elastico|corpo libero|0|1|3|3|20|60|prn|BUSP
Ankle Hops|Pliometria|caviglia|reattivita' della caviglia|corpo libero|0|1|3|3|20|60|prn|BUS
Squat Jump|Pliometria|quadricipiti/glutei|potenza concentrica|corpo libero|0|2|3|4|5|90|prn|BUS
Countermovement Jump|Pliometria|quadricipiti/glutei|ciclo allungamento-accorciamento|corpo libero|0|2|3|4|5|90|prn|BUS
Box Jump|Pliometria|quadricipiti/glutei|potenza verticale|box|0|2|3|4|4|120|int|BUS
Depth Jump|Pliometria|catena inferiore|stiffness reattiva|box|0|1|3|3|4|150|avz|US
Drop Jump|Pliometria|catena inferiore|tempo di contatto breve|box|0|1|3|3|5|150|avz|US
Broad Jump|Pliometria|glutei/femorali|potenza orizzontale|corpo libero|0|2|3|3|4|120|int|BUS
Bounds|Pliometria|glutei/femorali|propulsione orizzontale|corpo libero|0|1|3|3|6|120|int|US
Alternate Bounds|Pliometria|glutei/femorali|alternanza propulsiva|corpo libero|0|1|3|3|8|120|int|US
Single-leg Bounds|Pliometria|glutei/polpaccio|propulsione monopodalica|corpo libero|0|1|3|3|5|120|avz|US
Single-leg Pogo|Pliometria|piede/caviglia|stiffness monopodalica|corpo libero|0|1|3|2|10|60|int|BUSP
Single-leg Hop|Pliometria|catena inferiore|potenza monopodalica|corpo libero|0|1|3|3|6|90|int|US
Hop and Stick|Pliometria|catena inferiore|controllo dell'atterraggio|corpo libero|0|1|3|3|5|90|prn|BUS
Lateral Hop|Pliometria|gluteo medio/caviglia|stabilita' frontale|corpo libero|0|1|3|3|8|90|prn|BUS
Skater Jump|Pliometria|glutei/gluteo medio|potenza laterale|corpo libero|0|1|3|3|8|90|prn|BUS
Triple Hop|Pliometria|catena inferiore|potenza ripetuta|corpo libero|0|1|3|3|3|120|avz|US
A-Skip|Pliometria|coordinazione corsa|meccanica di corsa|corpo libero|0|0|3|3|20|45|prn|BUSP
B-Skip|Pliometria|coordinazione corsa|estensione attiva|corpo libero|0|0|3|3|20|45|int|BUSP
High Knees reattivi|Pliometria|flessori anca/caviglia|frequenza e reattivita'|corpo libero|0|0|3|3|20|45|prn|BUSP
Ankling|Pliometria|caviglia/piede|contatto al suolo|corpo libero|0|0|3|3|20|45|prn|BUSP
Quick Feet|Pliometria|caviglia|frequenza di appoggio|corpo libero|0|0|2|3|15|45|prn|BUS
Fast Feet Ladder|Pliometria|caviglia/coordinazione|coordinazione rapida|scaletta|0|0|2|3|15|45|prn|BU
Split Jump|Pliometria|quadricipiti/glutei|potenza alternata|corpo libero|0|2|3|3|6|90|int|BUS
Lateral Bounds|Pliometria|gluteo medio|potenza laterale|corpo libero|0|2|2|3|6|90|int|BUS
Medicine Ball Throw|Pliometria|tronco/spalla|potenza del tronco|palla medica|2|2|1|3|6|90|prn|BUS
Kettlebell Swing|Pliometria|glutei/femorali|estensione esplosiva dell'anca|kettlebell|1|3|2|4|12|90|int|BU
Plank|Core e stabilita'|core anteriore|anti-estensione|corpo libero|3|3|3|3|45|45|prn|BUSP
Long Lever Plank|Core e stabilita'|core anteriore|anti-estensione avanzata|corpo libero|3|3|3|3|30|60|avz|BUS
Side Plank|Core e stabilita'|obliqui/gluteo medio|stabilita' laterale|corpo libero|3|3|3|3|40|45|prn|BUSP
Dead Bug|Core e stabilita'|core profondo|controllo lombo-pelvico|corpo libero|3|3|3|3|8|45|prn|BUSP
Bird Dog|Core e stabilita'|core/estensori|coordinazione crociata|corpo libero|2|3|3|3|8|45|prn|BUSP
Pallof Press|Core e stabilita'|obliqui/core|anti-rotazione|cavi/elastico|3|3|3|3|10|60|prn|BUSP
Cable Anti-Rotation|Core e stabilita'|obliqui|controllo della rotazione|cavi|3|3|2|3|10|60|prn|BUS
Suitcase Carry|Core e stabilita'|core laterale|anti-inclinazione sotto carico|manubri|2|3|3|3|30|60|prn|BUS
Farmer Carry|Core e stabilita'|core/presa|rigidita' del tronco sotto carico|manubri|2|3|3|3|40|60|prn|BUS
Bear Crawl|Core e stabilita'|core/spalle|stabilita' in movimento|corpo libero|2|2|2|3|20|45|prn|BU
Hollow Hold|Core e stabilita'|core anteriore|tensione globale|corpo libero|3|2|2|3|30|45|int|BUSP
Stir the Pot|Core e stabilita'|core profondo|anti-estensione dinamica|fitball|3|3|2|3|10|60|avz|BUS
Stability Ball Rollout|Core e stabilita'|core anteriore|anti-estensione|fitball|3|3|2|3|10|60|int|BUS
Ab Wheel|Core e stabilita'|core anteriore|anti-estensione massimale|ruota|3|3|2|3|8|60|avz|BU
Cable Chop|Core e stabilita'|obliqui|rotazione controllata|cavi|3|2|2|3|10|60|int|BUS
Cable Lift|Core e stabilita'|obliqui|rotazione ascendente|cavi|3|2|2|3|10|60|int|BUS
Body Saw|Core e stabilita'|core anteriore|anti-estensione dinamica|corpo libero|3|2|2|3|10|45|int|BUS
Superman alternato|Core e stabilita'|estensori|catena posteriore|corpo libero|2|2|2|3|10|45|prn|BU
Pull-up|Forza massima|dorsali/bicipiti|trazione verticale|sbarra|3|0|0|4|6|150|avz|BUSP
Chin-up|Forza massima|dorsali/bicipiti|trazione supina|sbarra|3|0|0|4|6|150|int|BU
Lat Pulldown|Forza massima|dorsali|trazione verticale assistita|macchina|3|0|0|4|8|120|prn|BUSP
Straight-arm Pulldown|Forza funzionale|dorsale/gran rotondo|estensione di spalla, passata|cavi|3|0|0|3|10|90|prn|BUSP
Cable Pullover|Forza funzionale|dorsali|estensione di spalla|cavi|3|0|0|3|10|90|prn|BUS
Dumbbell Pullover|Forza funzionale|dorsali|apertura e trazione|manubri|3|0|0|3|10|90|prn|BU
Seated Cable Row|Forza massima|dorsali/romboidi|trazione orizzontale|cavi|3|1|1|4|10|90|prn|BUS
Chest Supported Row|Forza massima|dorsali/scapole|trazione senza carico lombare|macchina|3|1|1|4|10|90|prn|BUS
One-arm Cable Row|Forza funzionale|dorsali/core|trazione unilaterale|cavi|3|1|1|3|8|90|prn|BUSP
One-arm Dumbbell Row|Forza funzionale|dorsali|trazione unilaterale|manubri|3|1|1|3|10|90|prn|BUS
TRX Row|Forza funzionale|dorsali/core|trazione a corpo libero|TRX|3|1|1|3|12|60|prn|BUSP
Cable Triceps Pushdown|Forza funzionale|tricipite|fase di spinta subacquea|cavi|3|0|0|3|10|60|prn|BUSP
Rope Pushdown|Forza funzionale|tricipite|spinta con rotazione|cavi|3|0|0|3|12|60|prn|BUS
Overhead Triceps Extension|Forza funzionale|tricipite|estensione in allungamento|manubri|3|0|0|3|10|60|prn|BU
Close Grip Push-up|Bodyweight|tricipite/petto|spinta a corpo libero|corpo libero|2|0|0|3|12|60|prn|BUSP
Dips|Forza funzionale|tricipite/petto|spinta verticale|parallele|2|0|0|3|8|90|avz|BU
Face Pull|Prevenzione|trapezio medio/cuffia|salute della spalla|cavi/elastico|3|1|1|3|12|60|prn|BUSP
Band Pull Apart|Prevenzione|romboidi/trapezio|retrazione scapolare|elastico|3|1|1|3|15|45|prn|BUSP
Y Raise|Prevenzione|trapezio inferiore|elevazione scapolare|manubri|3|0|0|2|10|45|prn|BUSP
T Raise|Prevenzione|trapezio medio|retrazione|manubri|3|0|0|2|10|45|prn|BUSP
W Raise|Prevenzione|cuffia/trapezio|rotazione esterna scapolare|manubri|3|0|0|2|10|45|prn|BUSP
Prone Y-T-W|Prevenzione|scapole/cuffia|complesso scapolare|corpo libero|3|0|0|2|8|45|prn|BUSP
Scapular Pull-up|Prevenzione|scapole|controllo scapolare in trazione|sbarra|3|0|0|3|8|60|int|BUSP
Scapular Push-up|Prevenzione|dentato anteriore|protrazione scapolare|corpo libero|3|0|0|3|12|45|prn|BUSP
Serratus Wall Slide|Prevenzione|dentato anteriore|ritmo scapolo-omerale|muro|3|0|0|2|12|45|prn|BUSP
Wall Angels|Prevenzione|scapole/mobilita'|mobilita' toracica|muro|3|0|0|2|10|45|prn|BUSP
Cable External Rotation|Prevenzione|cuffia dei rotatori|rotazione esterna|cavi|3|0|0|3|15|45|prn|BUSP
Band External Rotation|Prevenzione|cuffia dei rotatori|rotazione esterna|elastico|3|0|0|3|15|45|prn|BUSP
Side-lying External Rotation|Prevenzione|cuffia dei rotatori|isolamento della cuffia|manubri|3|0|0|2|15|45|prn|BUSP
90/90 External Rotation|Prevenzione|cuffia dei rotatori|rotazione in posizione di nuoto|elastico|3|0|0|2|12|45|int|BUSP
Cuban Rotation|Prevenzione|cuffia/scapole|rotazione completa|manubri|3|0|0|2|10|45|avz|BU
Medicine Ball Slam|Pliometria|dorsale/core|potenza di trazione|palla medica|3|1|1|4|6|90|prn|BUS
Overhead Slam|Pliometria|catena superiore|potenza verticale|palla medica|3|1|1|3|8|90|prn|BUS
Rotational Throw|Pliometria|core/rotazione|potenza rotazionale|palla medica|3|2|1|3|6|90|int|BUS
Shot-put Throw|Pliometria|tronco/spalla|potenza di spinta|palla medica|3|1|1|3|6|90|int|BUS
Half-kneeling Rotational Throw|Pliometria|core/rotazione|rotazione controllata|palla medica|3|2|1|3|6|90|int|BUS
Chest Pass|Pliometria|pettorali/tricipiti|potenza di spinta|palla medica|2|1|1|3|8|60|prn|BU
Air Squat|Bodyweight|quadricipiti/glutei|schema di base|corpo libero|0|2|2|3|15|60|prn|B
Tempo Squat|Bodyweight|quadricipiti/glutei|controllo del tempo|corpo libero|0|2|2|3|10|60|prn|B
Pause Squat|Bodyweight|quadricipiti|forza in posizione|corpo libero|0|2|2|3|8|60|int|BU
Lateral Lunge|Bodyweight|adduttori/glutei|piano frontale|corpo libero|0|2|2|3|10|60|prn|BU
Curtsy Lunge|Bodyweight|gluteo medio|piano trasverso|corpo libero|0|1|2|3|10|60|prn|BU
Single-leg Squat|Bodyweight|quadricipiti/glutei|forza monopodalica|corpo libero|0|2|3|3|8|90|avz|BU
Pistol Squat assistito|Bodyweight|quadricipiti/glutei|monopodalico completo|TRX|0|2|2|3|6|90|avz|BU
Glute Bridge|Bodyweight|glutei|estensione dell'anca|corpo libero|0|2|2|3|15|45|prn|BUSP
Nordic Curl assistito|Bodyweight|femorali|forza eccentrica dei femorali|partner/panca|0|2|3|3|6|90|avz|BU
Push-up|Bodyweight|petto/tricipiti|spinta orizzontale|corpo libero|2|1|1|3|15|60|prn|BUSP
Incline Push-up|Bodyweight|petto/tricipiti|spinta facilitata|panca|2|1|1|3|15|45|prn|B
Decline Push-up|Bodyweight|petto/spalle|spinta con carico maggiore|panca|2|1|1|3|12|60|int|BU
Diamond Push-up|Bodyweight|tricipiti|enfasi tricipite|corpo libero|3|0|0|3|10|60|int|BU
Pike Push-up|Bodyweight|spalle|spinta verticale|corpo libero|2|0|0|3|10|60|int|BU
Australian Row|Bodyweight|dorsali|trazione orizzontale|sbarra bassa|3|1|1|3|12|60|prn|BUSP
Mountain Climber lento|Core e stabilita'|core/spalle|stabilita' in movimento|corpo libero|2|2|2|3|20|45|prn|BU
Crab Walk|Core e stabilita'|catena posteriore|mobilita' e stabilita'|corpo libero|1|1|1|3|20|45|prn|B
Plank Shoulder Tap|Core e stabilita'|core/spalle|anti-rotazione dinamica|corpo libero|3|2|2|3|20|45|prn|BUSP
Plank Walkout|Core e stabilita'|core/spalle|controllo in allungamento|corpo libero|2|2|2|3|8|45|prn|BU
Reverse Plank|Core e stabilita'|catena posteriore|estensione del tronco|corpo libero|2|2|2|3|30|45|prn|BU
Burpee|Bodyweight|generale|conditioning generale|corpo libero|1|1|1|3|12|60|prn|B
Jumping Jack|Bodyweight|generale|riscaldamento e conditioning|corpo libero|1|1|1|3|30|45|prn|B
Squat Thrust|Bodyweight|generale|conditioning|corpo libero|1|1|1|3|12|60|prn|B
Jump Rope|Bodyweight|caviglia/polpaccio|reattivita' e conditioning|corda|0|1|2|3|60|60|prn|BU
Single-leg Balance|Prevenzione|propriocezione|controllo monopodalico|corpo libero|0|1|3|2|30|30|prn|BUSP
"""

def _riga(l):
    c = [x.strip() for x in l.split('|')]
    return dict(nome=c[0], famiglia=c[1], distretto=c[2], funzione=c[3], attrezzo=c[4],
                N=int(c[5]), B=int(c[6]), C=int(c[7]), serie=int(c[8]), rip=int(c[9]),
                rec=int(c[10]), livello=c[11], fasi=c[12])

ESERCIZI = [_riga(l) for l in RAW.strip().split('\n') if l.strip()]
IDX = {e['nome']: e for e in ESERCIZI}

def durata(nome, serie=None):
    """minuti stimati: lavoro (3 s per ripetizione, o i secondi stessi se isometrico) + recupero"""
    e = IDX[nome]; s = serie or e['serie']
    iso = e['funzione'].startswith('anti-') or 'tensione' in e['funzione'] or e['rip'] >= 20
    lavoro = e['rip'] if iso else e['rip'] * 3
    return s * (lavoro + e['rec']) / 60.0

if __name__ == '__main__':
    from collections import Counter
    print(f"esercizi in libreria: {len(ESERCIZI)}  (nomi unici: {len(IDX)})")
    print("\nper famiglia:")
    for f, n in Counter(e['famiglia'] for e in ESERCIZI).most_common():
        print(f"  {f:<20}{n:3d}")
    print("\ncon trasferimento alto (3) per disciplina:")
    for k, d in (('N','Nuoto'), ('B','Bici'), ('C','Corsa')):
        print(f"  {d:<8}{sum(1 for e in ESERCIZI if e[k]==3):3d} esercizi")
    print("\nper fase (esercizi disponibili):")
    for f, nome in (('B','Base'), ('U','Build'), ('S','Specifico'), ('P','Peak')):
        print(f"  {nome:<12}{sum(1 for e in ESERCIZI if f in e['fasi']):3d}")
    print("\nattrezzatura richiesta:")
    for a, n in Counter(e['attrezzo'] for e in ESERCIZI).most_common(8):
        print(f"  {a:<20}{n:3d}")
