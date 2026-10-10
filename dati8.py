# -*- coding: utf-8 -*-
# OLIMPICO: completamento 12a settimana (p. 237)
import sys
sys.path.insert(0,'/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad')
import dati7
from dati import MOV_PLIO, SUPPL_NUOTO, SUPPL_CORSA
from dati5 import nuoto_gara_oly, bici_end_oly, nuoto_end_oly

OLY = "Triathlon Olimpico"
MG3 = "Terzo Mesociclo - Fase di preparazione alla gara"
R = "Ripristino"
NEW = []

def add(pag, giorno, disc, focus, vol_txt, vol_num, unita, serie):
    NEW.append(dict(piano=OLY, meso=MG3, sett=12, nota=R, pag=pag, giorno=giorno, disc=disc,
                    focus=focus, vol_txt=vol_txt, vol_num=vol_num, unita=unita, serie=serie,
                    fase="Gara", descr=False))

add(237,"Venerdi","Nuoto","Andatura di gara","1.100 metri",1100,"m",
    nuoto_gara_oly("2 x 300 metri a nuoto alla velocita' prevista sui 1.600 metri, con 30 secondi di riposo."))
add(237,"Sabato","Ciclismo","Endurance","33,6 chilometri",33.6,"km",bici_end_oly("22,4",35,48,25))
add(237,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",
    ["1 x 10 ripetizioni al 50% di 1 RM.", "2 x 3 ripetizioni al 50% di 1 RM, esplosive.", MOV_PLIO])
add(237,"Domenica","Nuoto","Endurance","1.300 metri",1300,"m",nuoto_end_oly(12,15,"800",250))
add(237,"Domenica","Corsa a piedi","Endurance","5,6 chilometri",5.6,"km",[
    "11,2 chilometri o da 20 a 27 minuti di corsa in modo continuato alla velocita' prevista sulla distanza della mezza maratona. [NB: cosi' e' stampato nel libro, ma il valore e' incoerente con l'obiettivo di 5,6 km della sessione e con il dimezzamento della 11a settimana: 5,6 km sarebbe il valore atteso]",
    "12 minuti di lavoro di endurance sulla forza correndo fino ad una pendenza dal 2% al 4% a velocita' aerobica.",
    SUPPL_CORSA])

# la 12a settimana non e' piu' incompleta
TUTTE = []
for s in dati7.TUTTE:
    d = dict(s)
    if d["piano"] == OLY and d.get("nota") == "Ripristino (incompleta)":
        d["nota"] = R
    TUTTE.append(d)
# inserisci le nuove sessioni subito dopo la 12a settimana dell'Olimpico
idx = max(i for i,d in enumerate(TUTTE) if d["piano"]==OLY and d["sett"]==12) + 1
TUTTE = TUTTE[:idx] + NEW + TUTTE[idx:]
