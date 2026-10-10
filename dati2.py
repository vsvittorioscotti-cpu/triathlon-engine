# -*- coding: utf-8 -*-
# Settimane 7-12 Ironman (pp. 295-311) + Half-Ironman 1a settimana (pp. 252-254)
import sys
sys.path.insert(0,'/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad')
from dati import (corsa_velocita, bici_velocita, nuoto_velocita, bici_gara, corsa_gara,
                  nuoto_gara, bici_endurance, nuoto_endurance, corsa_endurance,
                  pesi_forza, pesi_potenza, MOV_BASE, MOV_PLIO,
                  SUPPL_CORSA, SUPPL_BICI, SUPPL_NUOTO, SESSIONI as SESS_1_6)

EXTRA = []
def add(piano, meso, sett, nota, pag, giorno, disc, focus, vol_txt, vol_num, unita, serie, descr=False):
    EXTRA.append(dict(piano=piano, meso=meso, sett=sett, nota=nota, pag=pag, giorno=giorno,
                      disc=disc, focus=focus, vol_txt=vol_txt, vol_num=vol_num,
                      unita=unita, serie=serie, descr=descr))

IM = "Ironman"
HIM = "Half-Ironman"
M2 = "Secondo Mesociclo - Fase di preparazione alla gara"
M3 = "Terzo Mesociclo - Fase di preparazione alla gara"
M1 = "Primo Mesociclo - Fase di preparazione alla gara"

# ============ SETTIMANA 7 (pp. 295-297) ============
add(IM,M2,7,"",295,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(IM,M2,7,"",295,"Martedi","Corsa a piedi","Velocita","20,8 chilometri",20.8,"km",corsa_velocita(4,40))
add(IM,M2,7,"",295,"Martedi","Ciclismo","Velocita","96 chilometri",96,"km",bici_velocita(4,70))
add(IM,M2,7,"",296,"Mercoledi","Nuoto","Velocita","3.600 metri",3600,"m",nuoto_velocita(4,1400))
add(IM,M2,7,"",296,"Mercoledi","Pesi","Forza","-",None,"",pesi_forza("1 x 12 ripetizioni al 50% di 1 RM.","2 x da 6 a 8 ripetizioni all'85% di 1 RM."))
add(IM,M2,7,"",296,"Giovedi","Ciclismo","Andatura di gara","96 chilometri",96,"km",bici_gara("3 x 28,8 chilometri in bicicletta alla velocita' prevista sui 90 chilometri, con 5 minuti per un giro in souplesse."))
add(IM,M2,7,"",296,"Giovedi","Corsa a piedi","Andatura di gara","20,8 chilometri",20.8,"km",corsa_gara("3 x 4,8 chilometri di corsa alla velocita' prevista sui 21 chilometri, con 800 metri di camminata o di jogging per il recupero."))
add(IM,M2,7,"",296,"Venerdi","Nuoto","Andatura di gara","3.600 metri",3600,"m",nuoto_gara("2 x 900 metri a nuoto alla velocita' prevista sui 2.000 metri, con 60 secondi di riposo.",1400))
add(IM,M2,7,"",297,"Sabato","Ciclismo","Endurance","168 chilometri",168,"km",bici_endurance("96",180,240,70))
add(IM,M2,7,"",297,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",pesi_potenza("1 x 20 ripetizioni al 50% di 1 RM.","2 x 6 ripetizioni al 50% di 1 RM, esplosive."))
add(IM,M2,7,"",297,"Domenica","Nuoto","Endurance","6.000 metri",6000,"m",nuoto_endurance(49,70,"3.500",1400))
add(IM,M2,7,"",297,"Domenica","Corsa a piedi","Endurance","33,6 chilometri",33.6,"km",corsa_endurance("20,8",104,130,45))

# ============ SETTIMANA 8 - RIPRISTINO (pp. 298-300) ============
R = "Ripristino"
add(IM,M2,8,R,298,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(IM,M2,8,R,298,"Martedi","Corsa a piedi","Velocita","10,4 chilometri",10.4,"km",corsa_velocita(2,20))
add(IM,M2,8,R,298,"Martedi","Ciclismo","Velocita","48 chilometri",48,"km",bici_velocita(2,30))
add(IM,M2,8,R,299,"Mercoledi","Nuoto","Velocita","1.600 metri",1600,"m",nuoto_velocita(2,700))
add(IM,M2,8,R,299,"Mercoledi","Pesi","Forza","-",None,"",pesi_forza("1 x 6 ripetizioni al 50% di 1 RM.","1 x da 3 a 4 ripetizioni all'85% di 1 RM."))
add(IM,M2,8,R,299,"Giovedi","Ciclismo","Andatura di gara","48 chilometri",48,"km",bici_gara("2 x 14,4 chilometri in bicicletta alla velocita' prevista sui 90 chilometri, con 3 minuti per un giro in souplesse."))
add(IM,M2,8,R,299,"Giovedi","Corsa a piedi","Andatura di gara","9,6 chilometri",9.6,"km",corsa_gara("3 x 2.400 metri di corsa alla velocita' prevista sui 21 chilometri, con 800 metri di camminata o di jogging per il recupero."))
add(IM,M2,8,R,299,"Venerdi","Nuoto","Andatura di gara","1.600 metri",1600,"m",nuoto_gara("3 x 300 metri a nuoto alla velocita' prevista sui 2.000 metri, con 60 secondi di riposo.",None))
add(IM,M2,8,R,300,"Sabato","Ciclismo","Endurance","83,2 chilometri",83.2,"km",bici_endurance("48",90,120,35))
add(IM,M2,8,R,300,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",pesi_potenza("1 x 10 ripetizioni al 50% di 1 RM.","1 x 6 ripetizioni al 50% di 1 RM, esplosive."))
add(IM,M2,8,R,300,"Domenica","Nuoto","Endurance","3.000 metri",3000,"m",nuoto_endurance(28,40,"2.000",700))
add(IM,M2,8,R,300,"Domenica","Corsa a piedi","Endurance","16,8 chilometri",16.8,"km",corsa_endurance("8",40,50,"20 e mezzo"))

# ============ SETTIMANA 9 (pp. 301-303) ============
add(IM,M2,9,"",301,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(IM,M2,9,"",301,"Martedi","Corsa a piedi","Velocita","20,8 chilometri",20.8,"km",corsa_velocita(4,40))
add(IM,M2,9,"",301,"Martedi","Ciclismo","Velocita","96 chilometri",96,"km",bici_velocita(4,70))
add(IM,M2,9,"",302,"Mercoledi","Nuoto","Velocita","3.600 metri",3600,"m",nuoto_velocita(4,1400))
add(IM,M2,9,"",302,"Mercoledi","Pesi","Forza","-",None,"",pesi_forza("1 x 12 ripetizioni al 50% di 1 RM.","2 x da 6 a 8 ripetizioni all'85% di 1 RM."))
add(IM,M2,9,"",302,"Giovedi","Ciclismo","Andatura di gara","96 chilometri",96,"km",bici_gara("4 x 4,8 chilometri in bicicletta alla velocita' prevista sui 20 chilometri, con 1 minuto per un giro in souplesse."))
add(IM,M2,9,"",302,"Giovedi","Corsa a piedi","Andatura di gara","20,8 chilometri",20.8,"km",corsa_gara("6 x 800 metri di corsa alla velocita' prevista sui 5 chilometri, con 400 metri di camminata o di jogging per il recupero."))
add(IM,M2,9,"",302,"Venerdi","Nuoto","Andatura di gara","3.600 metri",3600,"m",nuoto_gara("5 x 100 metri a nuoto alla velocita' prevista sui 500 metri, con 30 secondi di riposo.",1400))
add(IM,M2,9,"",303,"Sabato","Ciclismo","Endurance","176 chilometri",176,"km",bici_endurance("108,8",204,272,70))
add(IM,M2,9,"",303,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",pesi_potenza("1 x 20 ripetizioni al 50% di 1 RM.","2 x 6 ripetizioni al 50% di 1 RM, esplosive."))
add(IM,M2,9,"",303,"Domenica","Nuoto","Endurance","6.000 metri",6000,"m",nuoto_endurance(42,60,"3.000",1400))
add(IM,M2,9,"",303,"Domenica","Corsa a piedi","Endurance","36,8 chilometri",36.8,"km",corsa_endurance("22,4",112,140,45))

# ============ SETTIMANA 10 (pp. 304-306) ============
add(IM,M3,10,"",304,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(IM,M3,10,"",304,"Martedi","Corsa a piedi","Velocita","17,6 chilometri",17.6,"km",corsa_velocita(3,30))
add(IM,M3,10,"",304,"Martedi","Ciclismo","Velocita","80 chilometri",80,"km",bici_velocita(3,60))
add(IM,M3,10,"",305,"Mercoledi","Nuoto","Velocita","3.200 metri",3200,"m",nuoto_velocita(3,1200))
add(IM,M3,10,"",305,"Mercoledi","Pesi","Forza","-",None,"",pesi_forza("1 x 12 ripetizioni al 50% di 1 RM.","2 x da 6 a 8 ripetizioni all'85% di 1 RM."))
add(IM,M3,10,"",305,"Giovedi","Ciclismo","Andatura di gara","80 chilometri",80,"km",bici_gara("2 x 12,8 chilometri in bicicletta alla velocita' prevista sui 40 chilometri, con 5 minuti per un giro in souplesse."))
add(IM,M3,10,"",305,"Giovedi","Corsa a piedi","Andatura di gara","17,6 chilometri",17.6,"km",corsa_gara("4 x 1.600 metri di corsa alla velocita' prevista sui 10 chilometri, con 400 metri di camminata o di jogging per il recupero."))
add(IM,M3,10,"",305,"Venerdi","Nuoto","Andatura di gara","3.200 metri",3200,"m",nuoto_gara("4 x 300 metri a nuoto alla velocita' prevista sui 1.600 metri, con 30 secondi di riposo.",1200))
add(IM,M3,10,"",306,"Sabato","Ciclismo","Endurance","180 chilometri",180,"km",bici_endurance("96",180,240,60))
add(IM,M3,10,"",306,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",pesi_potenza("1 x 20 ripetizioni al 50% di 1 RM.","2 x 6 ripetizioni al 50% di 1 RM, esplosive."))
add(IM,M3,10,"",306,"Domenica","Nuoto","Endurance","5.000 metri",5000,"m",nuoto_endurance(35,50,"2.500",1200))
add(IM,M3,10,"",306,"Domenica","Corsa a piedi","Endurance","28,8 chilometri",28.8,"km",corsa_endurance("19,2",96,120,40))

# ============ SETTIMANA 11 (pp. 307-309) ============
add(IM,M3,11,"",307,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(IM,M3,11,"",307,"Martedi","Corsa a piedi","Velocita","12,8 chilometri",12.8,"km",corsa_velocita(2,20))
add(IM,M3,11,"",307,"Martedi","Ciclismo","Velocita","40 chilometri",40,"km",bici_velocita(2,30))
add(IM,M3,11,"",308,"Mercoledi","Nuoto","Velocita","1.600 metri",1600,"m",nuoto_velocita(2,600))
add(IM,M3,11,"",308,"Mercoledi","Pesi","Forza","-",None,"",pesi_forza("1 x 12 ripetizioni al 50% di 1 RM.","2 x da 6 a 8 ripetizioni all'85% di 1 RM."))
add(IM,M3,11,"",308,"Giovedi","Ciclismo","Andatura di gara","40 chilometri",40,"km",bici_gara("1 x 28,8 chilometri in bicicletta alla velocita' prevista sui 90 chilometri, con 5 minuti per un giro in souplesse."))
add(IM,M3,11,"",308,"Giovedi","Corsa a piedi","Andatura di gara","12,8 chilometri",12.8,"km",corsa_gara("2 x 2.400 metri di corsa alla velocita' prevista sui 21 chilometri, con 400 metri di camminata o di jogging per il recupero."))
add(IM,M3,11,"",308,"Venerdi","Nuoto","Andatura di gara","1.600 metri",1600,"m",nuoto_gara("1 x 600 metri a nuoto alla velocita' prevista sui 2.000 metri, con 60 secondi di riposo.",600))
add(IM,M3,11,"",309,"Sabato","Ciclismo","Endurance","80 chilometri",80,"km",bici_endurance("48",90,120,30))
add(IM,M3,11,"",309,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",pesi_potenza("1 x 20 ripetizioni al 50% di 1 RM.","2 x 6 ripetizioni al 50% di 1 RM, esplosive."))
add(IM,M3,11,"",309,"Domenica","Nuoto","Endurance","3.000 metri",3000,"m",nuoto_endurance(28,40,"2.000",600))
add(IM,M3,11,"",309,"Domenica","Corsa a piedi","Endurance","18,4 chilometri",18.4,"km",corsa_endurance("8,8",44,55,"20 e mezzo"))

# ============ SETTIMANA 12 - TAPERING (pp. 310-311) ============
T = "Tapering"
GARA = "Questa sessione viene sostituita dalla gara a cui si e' deciso di partecipare."
NOTA_GARA = "Nota del libro: se la gara e' prevista per la domenica, sarebbe opportuno eseguire un breve riscaldamento in ogni disciplina sul percorso di gara, nel caso sia possibile effettuarlo."
add(IM,M3,12,T,310,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(IM,M3,12,T,310,"Martedi","Corsa a piedi","Velocita","4,8 chilometri",4.8,"km",
    ["In questa sessione sono compresi del lavoro aerobico, vari allunghi e solamente uno o due sforzi sui 400 metri ad andatura di gara. Il volume e' il 30%, o meno del 30%, delle sessioni d'allenamento della precedente settimana."], descr=True)
add(IM,M3,12,T,310,"Martedi","Ciclismo","Velocita","24 chilometri",24,"km",
    ["In questa sessione sono compresi del lavoro aerobico, vari allunghi e solamente uno o due sforzi di 1 minuto ad andatura di gara. Il volume d'allenamento e' il 30%, o meno del 30%, delle sessioni della precedente settimana."], descr=True)
add(IM,M3,12,T,310,"Mercoledi","Nuoto","Velocita","1.000 metri",1000,"m",[
    "1 x 25 metri a nuoto alla velocita' prevista sui 100 metri, con un riposo uguale.",
    "50 metri a nuoto, a ritmo blando.",
    "1 x 50 metri a nuoto alla velocita' prevista sui 200 metri, con 30 secondi di riposo.",
    "50 metri a nuoto, a ritmo blando.",
    "1 x 100 metri a nuoto alla velocita' prevista sui 500 metri, con 40 secondi riposo.",
    "100 metri a nuoto, a ritmo blando.",
    SUPPL_NUOTO])
add(IM,M3,12,T,310,"Mercoledi","Pesi","Forza","-",None,"",pesi_forza("1 x 6 ripetizioni al 50% di 1 RM.","1 x da 3 a 4 ripetizioni all'85% di 1 RM."))
add(IM,M3,12,T,311,"Giovedi","Ciclismo","Andatura di gara","24 chilometri",24,"km",
    ["Questa sessione viene sostituita dalla gara prevista per la fine della settimana. Effettuare del ciclismo aerobico con uno o due sforzi di 1 minuto all'andatura di gara per raggiungere l'obiettivo della quantita' di allenamento, che e' il 50% delle sessioni delle tre settimane precedenti."], descr=True)
add(IM,M3,12,T,311,"Giovedi","Corsa a piedi","Andatura di gara","4,8 chilometri",4.8,"km",
    ["Questa sessione viene sostituita dalla gara prevista per la fine della settimana. In questa sessione sono compresi l'allenamento aerobico e solamente uno o due sforzi sui 400 metri all'andatura di gara. Il volume d'allenamento e' il 50%, o meno del 50%, delle sessioni della settimana precedente."], descr=True)
add(IM,M3,12,T,311,"Venerdi","Nuoto","Andatura di gara","1.000 metri",1000,"m",
    ["In questa sessione sono compresi del lavoro aerobico, vari allunghi e solamente uno o due sforzi sui 50 metri ad andatura di gara. Il volume d'allenamento e' il 30%, o meno del 30%, delle sessioni della settimana precedente."], descr=True)
add(IM,M3,12,T,311,"Sabato","Ciclismo","Endurance","Sostituita dalla gara",None,"",[GARA, NOTA_GARA], descr=True)
add(IM,M3,12,T,311,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",
    ["Vanno eliminati l'allenamento con i pesi e gli esercizi di pliometria, prima della gara."], descr=True)
add(IM,M3,12,T,311,"Domenica","Nuoto","Endurance","Sostituita dalla gara",None,"",[GARA], descr=True)
add(IM,M3,12,T,311,"Domenica","Corsa a piedi","Endurance","Sostituita dalla gara",None,"",[GARA], descr=True)

# ============ HALF-IRONMAN - 1a SETTIMANA (pp. 252-254) ============
NO_PROGR = "Nessuna progressione nei pesi - Va mantenuto lo stesso numero di ripetizioni e la stessa quantita' di pesi utilizzata durante il periodo di base."
add(HIM,M1,1,"",252,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(HIM,M1,1,"",252,"Martedi","Corsa a piedi","Velocita","14,4 chilometri",14.4,"km",corsa_velocita(4,25))
add(HIM,M1,1,"",252,"Martedi","Ciclismo","Velocita","40 chilometri",40,"km",bici_velocita(4,50))
add(HIM,M1,1,"",253,"Mercoledi","Nuoto","Velocita","2.400 metri",2400,"m",nuoto_velocita(4,800))
add(HIM,M1,1,"",253,"Mercoledi","Pesi","Forza","-",None,"",pesi_forza("1 x 12 ripetizioni al 50% di 1 RM.","2 x da 6 a 8 ripetizioni all'85% di 1 RM.",True))
add(HIM,M1,1,"",253,"Giovedi","Ciclismo","Andatura di gara","44,8 chilometri",44.8,"km",bici_gara("3 x 11,2 chilometri in bicicletta alla velocita' prevista sui 90 chilometri, con 5 minuti per un giro in souplesse."))
add(HIM,M1,1,"",253,"Giovedi","Corsa a piedi","Andatura di gara","14,4 chilometri",14.4,"km",corsa_gara("3 x 3,2 chilometri di corsa alla velocita' prevista sui 21 chilometri, con 400 metri di camminata o di jogging per il recupero."))
add(HIM,M1,1,"",254,"Venerdi","Nuoto","Andatura di gara","2.400 metri",2400,"m",nuoto_gara("3 x 500 metri a nuoto alla velocita' prevista sui 2.000 metri, con 60 secondi di riposo.",None))
add(HIM,M1,1,"",254,"Sabato","Ciclismo","Endurance","76,8 chilometri",76.8,"km",bici_endurance("44,8",85,105,50))
add(HIM,M1,1,"",254,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",pesi_potenza("1 x 20 ripetizioni al 50% di 1 RM.","2 x 6 ripetizioni al 50% di 1 RM, esplosive."))
add(HIM,M1,1,"",254,"Domenica","Nuoto","Endurance","3.000 metri",3000,"m",[
    "Da 24 a 30 minuti o 1.600 metri a nuoto in modo continuato, utilizzando almeno un sollevamento della testa ogni 25 metri, o ogni da 12 a 20 bracciate alla velocita' prevista sui 3.200 metri. Indossare l'attrezzatura (gli occhialini, la muta e il costume per la gara) che verra' utilizzata durante la gara.",
    "800 metri a nuoto di endurance sulla forza ad un'intensita' aerobica utilizzando delle palette.",
    SUPPL_NUOTO])
add(HIM,M1,1,"",254,"Domenica","Corsa a piedi","Endurance","19,2 chilometri",19.2,"km",[
    "11,2 chilometri o da 60 a 80 minuti di corsa in modo continuato alla velocita' prevista sulla distanza della mezza maratona.",
    "25 minuti di lavoro di endurance sulla forza correndo fino ad una pendenza dal 2% al 4% a velocita' aerobica.",
    SUPPL_CORSA])

# ---- unione con le settimane 1-6 (tutte Ironman) ----
TUTTE = []
for s in SESS_1_6:
    d = dict(s); d["piano"] = IM; d["descr"] = False
    TUTTE.append(d)
TUTTE.extend(EXTRA)
