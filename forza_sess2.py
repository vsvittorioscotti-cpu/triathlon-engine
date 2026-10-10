# -*- coding: utf-8 -*-
"""16 workout standardizzati, dai template forniti da Vittorio.
La collocazione di una sessione e' quella del suo esercizio piu' esigente."""
import sys
sys.path.insert(0,'/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad')
import forza2 as F

ZONA_FAM = {"Forza massima":"Z2","Forza funzionale":"Z2","Core e stabilita'":"Z1",
            "Prevenzione":"Z1","Pliometria":"Z3","Bodyweight":"Z3"}
NM_FAM   = {"Forza massima":10,"Forza funzionale":7,"Core e stabilita'":2,
            "Prevenzione":1,"Pliometria":8,"Bodyweight":3}

# (codice, nome, bersaglio, fasi, [(esercizio, serie, ripetizioni)])
W = [
("RUN-A","RUN Strength A","forza monopodalica e piede per la corsa","BUS",
 [("Pogo Jumps",2,20),("Lateral Band Walk",2,12),("Trap Bar Deadlift",4,4),
  ("Bulgarian Split Squat",3,6),("Single-leg RDL",3,6),("Seated Calf Raise",3,10),
  ("Tibialis Raise",2,15),("Pallof Press",3,8)]),
("RUN-B","RUN Strength B","forza bilaterale pesante per la corsa","BU",
 [("Monster Walk",2,12),("Back Squat",4,5),("Romanian Deadlift",3,6),
  ("Step-up alto",3,6),("Standing Calf Raise",3,8),("Eccentric Heel Drops",2,10),
  ("Side Plank",3,40)]),
("RUN-C","RUN Strength C - senza palestra","forza corsa a corpo libero","BUSP",
 [("Single-leg Squat",3,8),("Hamstring Walkout",3,8),("Single-leg Glute Bridge",3,12),
  ("Single-leg Calf Raise",3,15),("Short Foot Exercise",2,10),
  ("Copenhagen Plank",2,25),("Dead Bug",3,8)]),
("BIKE-A","BIKE Strength A","spinta e catena posteriore per la bici","BUS",
 [("Back Squat",4,4),("Leg Press",3,6),("Romanian Deadlift",3,6),("Step-up alto",3,6),
  ("Seated Calf Raise",3,10),("Dead Bug",3,8),("Side Plank",3,40)]),
("BIKE-B","BIKE Strength B","forza-resistenza e stabilita del bacino","BU",
 [("Monster Walk",2,12),("Hack Squat",3,8),("Single-leg Leg Press",3,8),
  ("Hip Thrust",4,8),("Cable Pull Through",3,12),("Copenhagen Plank",2,25),
  ("Suitcase Carry",3,30)]),
("SWIM-A","SWIM Strength A","trazione, spinta e cuffia","BUS",
 [("Pull-up",4,6),("Straight-arm Pulldown",3,8),("One-arm Cable Row",3,8),
  ("Rope Pushdown",3,10),("Face Pull",3,12),("Band External Rotation",2,15),
  ("Serratus Wall Slide",2,12),("Hollow Hold",3,30)]),
("SWIM-B","SWIM Power B","potenza di trazione e rotazione","US",
 [("Medicine Ball Slam",4,5),("Rotational Wall Throw",3,5),("Pull-up",4,4),
  ("Straight-arm Pulldown",3,6),("Scapular Pull-up",3,8),("Half-kneeling Pallof",3,8)]),
("SWIM-C","SWIM Strength C - volume di trazione","tre schemi di trazione diversi","B",
 [("Lat Pulldown",4,8),("Chest Supported Row",3,10),("Cable Pullover",3,10),
  ("One-arm Cable Pulldown",3,8),("Overhead Triceps Extension",3,10),
  ("Prone Y-T-W",2,8),("Cable Anti-Rotation Hold",3,25)]),
("PLYO-A","Plyometric A","potenza e reattivita per la corsa","BUS",
 [("Pogo Jumps",3,20),("Single-leg Pogo",2,10),("Box Jump",4,4),("Broad Jump",3,4),
  ("Lateral Bounds",3,5),("A-Skip",3,20),("Bounds",3,20)]),
("PLYO-B","Plyometric B - basso impatto","stiffness senza carico eccentrico","BUSP",
 [("Low Pogo",3,20),("Ankling",3,20),("A-Skip",3,20),("Quick Contacts",3,15),
  ("Hop and Stick",3,5),("Single-leg Balance",2,30)]),
("STRU-A","Structural A - corsa","manutenzione di piede, caviglia e anca","BUSP",
 [("Single-leg Calf Raise",3,12),("Seated Calf Raise",3,15),("Tibialis Raise",3,15),
  ("Lateral Band Walk",3,12),("Copenhagen Plank",3,25),("Single-leg RDL",2,10,"leggero"),
  ("Short Foot Exercise",2,10),("Dead Bug",3,8)]),
("STRU-B","Structural B - nuoto","manutenzione di spalla e scapola","BUSP",
 [("Band External Rotation",3,15),("Face Pull",3,15),("Y Raise",2,10),("T Raise",2,10),
  ("Serratus Wall Slide",3,10),("Scapular Push-up",2,12),("Side Plank",3,30)]),
("FULL-A","Full Body A","la seduta unica quando si va in palestra una volta","BUS",
 [("Box Jump",3,4),("Medicine Ball Slam",3,5),("Trap Bar Deadlift",4,4),
  ("Bulgarian Split Squat",3,6),("Pull-up",3,6),("Straight-arm Pulldown",3,8),
  ("Seated Calf Raise",3,12),("Face Pull",3,12),("Pallof Press",3,8)]),
("FULL-B","Full Body B - peak","mantenimento, pochi esercizi e poche ripetizioni","SP",
 [("Box Jump",3,3),("Back Squat",3,3),("Bulgarian Split Squat",2,5),("Pull-up",3,5),
  ("Straight-arm Pulldown",2,8),("Seated Calf Raise",2,10),("Pallof Press",2,8)]),
("BW-A","Bodyweight A","forza a corpo libero per casa o viaggio","BUSP",
 [("Split Squat",3,10),("Single-leg Glute Bridge",3,12),("Push-up",3,12),
  ("Single-leg Calf Raise",3,15),("Scapular Push-up",3,12),("Side Plank",3,30),
  ("Dead Bug",3,8),("Pogo Jumps",3,20)]),
("BW-B","Bodyweight B - conditioning","circuito 40/20, solo nei periodi generali","B",
 [("Air Squat",3,30),("Push-up",3,30),("Reverse Lunge",3,30),("Mountain Climber",3,30),
  ("Bear Crawl",3,30),("Burpee",3,30)]),
]

def _spacchetta(t):
    return (t[0], t[1], t[2], (t[3] if len(t) > 3 else ''))

def _min(nome, serie, rip):
    e = F.IDX[nome]
    iso = e['funzione'].startswith('anti-') or 'tensione' in e['funzione'] or rip >= 20
    return serie * ((rip if iso else rip*3) + e['rec']) / 60.0

def componi(w):
    cod, nome, bers, fasi, lista = w
    lista = [_spacchetta(t) for t in lista]
    mins = sum(_min(n,s,r) for n,s,r,_ in lista)
    fam = {}
    for n,s,r,_ in lista: fam[F.IDX[n]['famiglia']] = fam.get(F.IDX[n]['famiglia'],0)+_min(n,s,r)
    dom = max(fam, key=fam.get)
    # una prescrizione "leggero" abbassa il DOMS dell'esercizio: dipende dal carico, non solo dal gesto
    dmax = max(min(F.doms(F.IDX[n]), 2) if q=='leggero' else F.doms(F.IDX[n]) for n,_,_,q in lista)
    fmed = sum(F.fatica(F.IDX[n])*_min(n,s,r) for n,s,r,_ in lista)/mins
    disc = {k: sum(F.IDX[n][k]*_min(n,s,r) for n,s,r,_ in lista)/mins for k in 'NBC'}
    coll = ('almeno 48 h prima del lungo' if dmax>=4 else
            'nei giorni gia impegnativi' if dmax==3 else 'libera, anche nei giorni facili')
    return dict(cod=cod,nome=nome,bersaglio=bers,fasi=fasi,n=len(lista),minuti=round(mins),
                famiglia=dom,zona=ZONA_FAM[dom],nm=round(NM_FAM[dom]*0+sum(NM_FAM[F.IDX[n]['famiglia']]*_min(n,s,r) for n,s,r,_ in lista)/mins,1),
                fatica=round(fmed,1),doms=dmax,collocazione=coll,
                N=round(disc['N'],1),B=round(disc['B'],1),C=round(disc['C'],1))

if __name__ == '__main__':
    print(f"{'cod':<8}{'workout':<32}{'es':>3}{'min':>5}{'fat':>5}{'DOMS':>5}{'N':>5}{'B':>5}{'C':>5}  {'fasi':<6}collocazione")
    for w in W:
        d = componi(w)
        print(f"{d['cod']:<8}{d['nome']:<32}{d['n']:3d}{d['minuti']:5d}{d['fatica']:5.1f}{d['doms']:5d}"
              f"{d['N']:5.1f}{d['B']:5.1f}{d['C']:5.1f}  {d['fasi']:<6}{d['collocazione']}")
