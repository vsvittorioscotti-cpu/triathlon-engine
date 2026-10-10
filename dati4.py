# -*- coding: utf-8 -*-
# Completamento 8a settimana Half-Ironman (p. 274)
import sys
sys.path.insert(0,'/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad')
import dati3

HIM = "Half-Ironman"
M2 = "Secondo Mesociclo - Fase di preparazione alla gara"
T8 = "Tapering"
GARA = "Questa sessione viene sostituita dalla gara a cui si e' deciso di partecipare."
NOTA_GARA = "Nota del libro: se la gara e' prevista per la domenica, sarebbe opportuno eseguire un breve riscaldamento in ogni disciplina sul percorso di gara, nel caso sia possibile effettuarlo."

# la 8a settimana non e' piu' parziale
TUTTE = []
for s in dati3.TUTTE:
    d = dict(s)
    if d.get("nota") == "Tapering (incompleta)":
        d["nota"] = T8
    TUTTE.append(d)

def add(pag, giorno, disc, focus, vol_txt, vol_num, unita, serie, descr=True):
    TUTTE.append(dict(piano=HIM, meso=M2, sett=8, nota=T8, pag=pag, giorno=giorno, disc=disc,
                      focus=focus, vol_txt=vol_txt, vol_num=vol_num, unita=unita,
                      serie=serie, descr=descr))

add(274,"Giovedi","Corsa a piedi","Andatura di gara","4,8 chilometri",4.8,"km",
    ["Questa sessione viene sostituita dalla gara prevista per la fine della settimana. In questa sessione sono compresi l'allenamento aerobico e solamente uno o due sforzi sui 400 metri all'andatura di gara. Il volume d'allenamento e' il 50%, o meno del 50%, delle sessioni della settimana precedente."])
add(274,"Venerdi","Nuoto","Andatura di gara","1.200 metri",1200,"m",
    ["In questa sessione sono compresi del lavoro aerobico, vari allunghi e solamente uno o due sforzi sui 50 metri ad andatura di gara. Il volume d'allenamento e' il 30%, o meno del 30%, delle sessioni della settimana precedente."])
add(274,"Sabato","Ciclismo","Endurance","Sostituita dalla gara",None,"",[GARA, NOTA_GARA])
add(274,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",
    ["Vanno eliminati l'allenamento con i pesi e gli esercizi di pliometria, prima della gara."])
add(274,"Domenica","Nuoto","Endurance","Sostituita dalla gara",None,"",[GARA])
add(274,"Domenica","Corsa a piedi","Endurance","Sostituita dalla gara",None,"",[GARA])
