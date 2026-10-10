# -*- coding: utf-8 -*-
"""Sessioni di preparazione atletica, composte dalla libreria.
Una sessione non e' "palestra": ha un bersaglio dichiarato (es. Bike Force +
Hip Stability) e si sceglie in base alla fase e alla disciplina da servire."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad')
from forza_lib import ESERCIZI, IDX, durata

# zona cardiaca indicativa e costo neuromuscolare per famiglia.
# STIMA NOSTRA: il libro non da' ne' FC ne' RPE per il lavoro a secco, e il
# modello di carico basato sulla FC sottostima per sua natura la forza pesante.
ZONA_FAM = {"Forza massima":"Z2", "Forza funzionale":"Z2", "Core e stabilita'":"Z1",
            "Prevenzione":"Z1", "Pliometria":"Z3", "Bodyweight":"Z3"}
NM_FAM   = {"Forza massima":10, "Forza funzionale":7, "Core e stabilita'":2,
            "Prevenzione":1, "Pliometria":8, "Bodyweight":3}

# (codice, nome, bersaglio, fasi, [(esercizio, serie), ...])
SESSIONI = [
 ("FA-01","Bike + Run Strength","forza arti inferiori per bici e corsa","BU",
  [("Monster Walk",2),("Single-leg Glute Bridge",2),("Pogo Jumps",2),
   ("Trap Bar Deadlift",4),("Bulgarian Split Squat",3),("Single-leg RDL",3),
   ("Seated Calf Raise",3),("Standing Calf Raise",3),
   ("Pallof Press",3),("Side Plank",3)]),
 ("FA-02","Lower Body Strength - base","forza generale arti inferiori","B",
  [("Lateral Band Walk",2),("Glute Bridge",2),
   ("Back Squat",4),("Romanian Deadlift",3),("Step-up alto",3),
   ("Standing Calf Raise",3),("Tibialis Raise",3),
   ("Dead Bug",3),("Plank",3)]),
 ("FB-01","Swim Strength","trazione, spinta e stabilita' scapolare","BUS",
  [("Pull-up",4),("Straight-arm Pulldown",3),("One-arm Cable Row",3),
   ("Overhead Triceps Extension",3),("Face Pull",3),("Band External Rotation",2),
   ("Serratus Wall Slide",2),("Hollow Hold",3),("Pallof Press",3)]),
 ("FB-02","Swim Strength + Core","trazione e controllo della rotazione","BU",
  [("Lat Pulldown",4),("Cable Pullover",3),("TRX Row",3),("Cable Triceps Pushdown",3),
   ("Prone Y-T-W",2),("Cable External Rotation",3),
   ("Cable Chop",3),("Dead Bug",3),("Side Plank",3)]),
 ("FC-01","Plyometric + Bodyweight","elasticita', potenza e resistenza muscolare","BUS",
  [("Pogo Jumps",3),("Single-leg Pogo",2),
   ("Box Jump",4),("Broad Jump",3),("Lateral Bounds",3),
   ("Medicine Ball Slam",4),("Rotational Throw",3),
   ("Push-up",3),("Walking Lunge",3),("Bear Crawl",3),("Plank Shoulder Tap",3)]),
 ("FC-02","Full Body + Plyometric - base","schema completo a basso carico","B",
  [("Jumping Jack",2),("Air Squat",3),("Push-up",3),("Australian Row",3),
   ("Reverse Lunge",3),("Glute Bridge",3),("Squat Jump",3),
   ("Plank",3),("Bird Dog",3)]),
 ("FD-01","Structural / Prehab","manutenzione di spalla, anca, caviglia","BUSP",
  [("Band External Rotation",2),("Face Pull",2),("Prone Y-T-W",2),
   ("Copenhagen Plank",2),("Lateral Band Walk",2),
   ("Single-leg Calf Raise",3),("Seated Calf Raise",3),("Tibialis Raise",3),
   ("Single-leg Balance",2),("Dead Bug",3)]),
 ("FE-01","Run Economy","stiffness, meccanica e piede","BUSP",
  [("Ankling",3),("A-Skip",3),("High Knees reattivi",3),
   ("Pogo Jumps",3),("Hop and Stick",3),
   ("Eccentric Heel Drops",3),("Short Foot Exercise",2),("Single-leg Balance",2)]),
 ("FF-01","Bike Force + Hip Stability","spinta e stabilita' del bacino","BUS",
  [("Monster Walk",2),("Leg Press",4),("Hip Thrust",4),("Single-leg Leg Press",3),
   ("Cable Hip Abduction",3),("Copenhagen Plank",2),
   ("Suitcase Carry",3),("Dead Bug",3)]),
 ("FG-01","Core + Anti-rotazione","trasferimento di forza fra arti e tronco","BUSP",
  [("Pallof Press",3),("Cable Anti-Rotation",3),("Side Plank",3),
   ("Dead Bug",3),("Bird Dog",3),("Farmer Carry",3),("Hollow Hold",3)]),
 ("FH-01","Mantenimento - peak","conservare la forza senza affaticare","SP",
  [("Bulgarian Split Squat",2),("Single-leg RDL",2),("Straight-arm Pulldown",2),
   ("Face Pull",2),("Pogo Jumps",2),("Pallof Press",2),("Side Plank",2)]),
 ("FT-01","Attivazione - taper","solo attivazione, nessun affaticamento","P",
  [("Monster Walk",2),("Band Pull Apart",2),("Glute Bridge",2),
   ("Single-leg Balance",2),("Dead Bug",2)]),
]

def componi(s):
    cod, nome, bersaglio, fasi, lista = s
    mins = sum(durata(e, n) for e, n in lista)
    fam = {}
    for e, n in lista: fam[IDX[e]['famiglia']] = fam.get(IDX[e]['famiglia'], 0) + durata(e, n)
    dom = max(fam, key=fam.get)
    nm = sum(NM_FAM[IDX[e]['famiglia']] * durata(e, n) for e, n in lista) / max(mins, 1)
    disc = {k: sum(IDX[e][k] * durata(e, n) for e, n in lista) / max(mins, 1) for k in 'NBC'}
    return dict(cod=cod, nome=nome, bersaglio=bersaglio, fasi=fasi, n_es=len(lista),
                minuti=round(mins), famiglia=dom, zona=ZONA_FAM[dom],
                nm=round(nm, 1), N=round(disc['N'],1), B=round(disc['B'],1), C=round(disc['C'],1))

if __name__ == '__main__':
    print(f"{'cod':<7}{'sessione':<30}{'es':>3}{'min':>5}{'zona':>6}{'nm':>5}   {'N':>4}{'B':>4}{'C':>4}  fasi")
    for s in SESSIONI:
        d = componi(s)
        print(f"{d['cod']:<7}{d['nome']:<30}{d['n_es']:3d}{d['minuti']:5d}{d['zona']:>6}{d['nm']:5.1f}   "
              f"{d['N']:4.1f}{d['B']:4.1f}{d['C']:4.1f}  {d['fasi']}")
    print("\ncopertura per fase (sessioni disponibili):")
    for f, nome in (('B','Base'),('U','Build'),('S','Specifico'),('P','Peak')):
        n = [componi(s)['cod'] for s in SESSIONI if f in s[3]]
        print(f"  {nome:<12}{len(n):2d}  {' '.join(n)}")
