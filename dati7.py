# -*- coding: utf-8 -*-
# SPRINT: completamento 6a settimana + settimane 7 e 8 (pp. 209-215)
import sys
sys.path.insert(0,'/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad')
import dati6
from dati import bici_gara, corsa_gara, MOV_BASE, MOV_PLIO, NO_PROGR
from dati5 import nuoto_gara_oly
from dati6 import (corsa_vel_spr, bici_vel_spr, nuoto_vel_spr,
                   bici_end_spr, nuoto_end_spr, corsa_end_spr, PS_F1, PS_P1, COMB)

SPR = "Triathlon Sprint"
SG2 = "Secondo Mesociclo - Fase di preparazione alla gara"
NEW = []

def add(sett, nota, pag, giorno, disc, focus, vol_txt, vol_num, unita, serie, descr=False):
    NEW.append(dict(piano=SPR, meso=SG2, sett=sett, nota=nota, pag=pag, giorno=giorno, disc=disc,
                    focus=focus, vol_txt=vol_txt, vol_num=vol_num, unita=unita, serie=serie,
                    fase="Gara", descr=descr))

# ===== completamento 6a SETTIMANA (p. 209) =====
add(6,"",209,"Sabato","Ciclismo","Endurance","27,2 chilometri",27.2,"km",bici_end_spr("22,2",45,60))
add(6,"",209,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",PS_P1)
add(6,"",209,"Domenica","Nuoto","Endurance","1.600 metri",1600,"m",nuoto_end_spr(14,17,"900"))
add(6,"",209,"Domenica","Corsa a piedi","Endurance","8,8 chilometri",8.8,"km",corsa_end_spr("5,6",25,30))

# ===== 7a SETTIMANA (pp. 210-212) =====
add(7,"",210,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(7,"",210,"Martedi","Corsa a piedi","Velocita","5,6 chilometri",5.6,"km",corsa_vel_spr(4))
add(7,"",210,"Martedi","Ciclismo","Velocita","17,6 chilometri",17.6,"km",bici_vel_spr(4))
add(7,"",211,"Mercoledi","Nuoto","Velocita","1.100 metri",1100,"m",nuoto_vel_spr(4))
add(7,"",211,"Mercoledi","Pesi","Forza","-",None,"",PS_F1)
add(7,"",211,"Giovedi","Ciclismo","Andatura di gara","17,6 chilometri",17.6,"km",
    bici_gara("4 x 4,8 chilometri in bicicletta alla velocita' prevista sui 20 chilometri, con un giro in souplesse di 1 minuto.")+[COMB])
add(7,"",211,"Giovedi","Corsa a piedi","Andatura di gara","5,6 chilometri",5.6,"km",
    corsa_gara("5 x 1.000 metri di corsa alla velocita' prevista sui 5 chilometri, con 400 metri di camminata o di jogging per il recupero.")+[COMB])
add(7,"",211,"Venerdi","Nuoto","Andatura di gara","1.100 metri",1100,"m",
    nuoto_gara_oly("5 x 200 metri a nuoto alla velocita' prevista sui 1.600 metri, con 30 secondi di riposo."))
add(7,"",212,"Sabato","Ciclismo","Endurance","27,2 chilometri",27.2,"km",bici_end_spr("25,6",55,70))
add(7,"",212,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",PS_P1)
add(7,"",212,"Domenica","Nuoto","Endurance","1.600 metri",1600,"m",nuoto_end_spr(16,20,"1.000"))
add(7,"",212,"Domenica","Corsa a piedi","Endurance","8,8 chilometri",8.8,"km",corsa_end_spr("6,4",30,35))

# ===== 8a SETTIMANA - TAPERING (pp. 213-215) =====
T = "Tapering"
GARA = "Questa sessione viene sostituita dalla gara a cui si e' deciso di partecipare."
NOTA_COMB = "Nota del libro: sarebbe il massimo se l'atleta riuscisse a combinare assieme queste sessioni d'allenamento (vedere il sesto capitolo)."
add(8,T,213,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(8,T,213,"Martedi","Corsa a piedi","Velocita","2,8 chilometri",2.8,"km",corsa_vel_spr(2))
add(8,T,213,"Martedi","Ciclismo","Velocita","8,8 chilometri",8.8,"km",bici_vel_spr(2))
add(8,T,214,"Mercoledi","Nuoto","Velocita","550 metri",550,"m",nuoto_vel_spr(2))
add(8,T,214,"Mercoledi","Pesi","Forza","-",None,"",
    ["1 x 6 ripetizioni al 50% di 1 RM.", "1 x da 3 a 4 ripetizioni all'85% di 1 RM.", NO_PROGR, MOV_BASE])
add(8,T,214,"Giovedi","Ciclismo","Andatura di gara","4,8 chilometri",4.8,"km",
    ["Questa sessione viene sostituita dalla gara prevista per la fine della settimana. Effettuare del ciclismo aerobico con uno o due sforzi di 1 minuto, all'andatura di gara per raggiungere l'obiettivo della quantita' di allenamento, che e' il 50% delle sessioni delle tre settimane precedenti.", NOTA_COMB], descr=True)
add(8,T,214,"Giovedi","Corsa a piedi","Andatura di gara","1.600 metri (= 1,6 chilometri)",1.6,"km",
    ["Questa sessione viene sostituita dalla gara prevista per la fine della settimana. Comprende l'allenamento aerobico e solamente uno o due sforzi sui 400 metri all'andatura di gara. La quantita' di allenamento e' il 50%, o meno del 50%, delle sessioni della settimana precedente.", NOTA_COMB], descr=True)
add(8,T,214,"Venerdi","Nuoto","Andatura di gara","350 metri",350,"m",
    ["Questa sessione viene sostituita dalla gara prevista per la fine della settimana. Comprende l'allenamento aerobico e solamente uno o due sforzi sui 50 metri all'andatura di gara. La quantita' di allenamento e' il 50%, o meno del 50%, delle sessioni della settimana precedente."], descr=True)
add(8,T,215,"Sabato","Ciclismo","Endurance","Sostituita dalla gara",None,"",[GARA], descr=True)
add(8,T,215,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",
    ["Vanno eliminati l'allenamento con i pesi e gli esercizi di pliometria, prima della gara."], descr=True)
add(8,T,215,"Domenica","Nuoto","Endurance","Sostituita dalla gara",None,"",[GARA], descr=True)
add(8,T,215,"Domenica","Corsa a piedi","Endurance","Sostituita dalla gara",None,"",[GARA, NOTA_COMB], descr=True)

# la 6a settimana non e' piu' incompleta
BASE = []
for s in dati6.TUTTE:
    d = dict(s)
    if d["piano"] == SPR and d.get("nota") == "Incompleta":
        d["nota"] = ""
    BASE.append(d)

spr_all = [d for d in BASE if d["piano"] == SPR] + NEW
TUTTE = ([d for d in BASE if d["piano"] == "Triathlon Olimpico"] + spr_all +
         [d for d in BASE if d["piano"] == "Half-Ironman"] +
         [d for d in BASE if d["piano"] == "Ironman"])
