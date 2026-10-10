# -*- coding: utf-8 -*-
# Half-Ironman settimane 2-8 (pp. 255-273)
import sys
sys.path.insert(0,'/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad')
import dati2
from dati import (corsa_velocita, bici_velocita, nuoto_velocita, bici_gara, corsa_gara,
                  nuoto_gara, bici_endurance, pesi_forza, pesi_potenza, MOV_BASE,
                  SUPPL_CORSA, SUPPL_BICI, SUPPL_NUOTO)

HIM = "Half-Ironman"
M1 = "Primo Mesociclo - Fase di preparazione alla gara"
M2 = "Secondo Mesociclo - Fase di preparazione alla gara"
NEW = []

def add(meso, sett, nota, pag, giorno, disc, focus, vol_txt, vol_num, unita, serie, descr=False):
    NEW.append(dict(piano=HIM, meso=meso, sett=sett, nota=nota, pag=pag, giorno=giorno,
                    disc=disc, focus=focus, vol_txt=vol_txt, vol_num=vol_num,
                    unita=unita, serie=serie, descr=descr))

def nuoto_end_him(mn, mx, metri, forza_m):
    return [
        f"Da {mn} a {mx} minuti o {metri} metri a nuoto in modo continuato, utilizzando almeno un sollevamento della testa ogni 25 metri, o ogni da 12 a 20 bracciate alla velocita' prevista sui 3.200 metri. Indossare l'attrezzatura (gli occhialini, la muta e il costume per la gara) che verra' utilizzata durante la gara.",
        f"{forza_m} metri a nuoto di endurance sulla forza ad un'intensita' aerobica utilizzando delle palette.",
        SUPPL_NUOTO,
    ]

def corsa_end_him(km, mn, mx, minuti):
    return [
        f"{km} chilometri o da {mn} a {mx} minuti di corsa in modo continuato alla velocita' prevista sulla distanza della mezza maratona.",
        f"{minuti} minuti di lavoro di endurance sulla forza correndo fino ad una pendenza dal 2% al 4% a velocita' aerobica.",
        SUPPL_CORSA,
    ]

PF = ("1 x 12 ripetizioni al 50% di 1 RM.", "2 x da 6 a 8 ripetizioni all'85% di 1 RM.")
PF_LOW = ("1 x 6 ripetizioni al 50% di 1 RM.", "1 x da 3 a 4 ripetizioni all'85% di 1 RM.")
PP = ("1 x 20 ripetizioni al 50% di 1 RM.", "2 x 6 ripetizioni al 50% di 1 RM, esplosive.")
PP_LOW = ("1 x 10 ripetizioni al 50% di 1 RM.", "1 x 6 ripetizioni al 50% di 1 RM, esplosive.")

# ===== 2a SETTIMANA (pp. 255-257) =====
add(M1,2,"",255,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(M1,2,"",255,"Martedi","Corsa a piedi","Velocita","16 chilometri",16,"km",corsa_velocita(4,30))
add(M1,2,"",255,"Martedi","Ciclismo","Velocita","51,2 chilometri",51.2,"km",bici_velocita(4,60))
add(M1,2,"",256,"Mercoledi","Nuoto","Velocita","2.600 metri",2600,"m",nuoto_velocita(4,900))
add(M1,2,"",256,"Mercoledi","Pesi","Forza","-",None,"",pesi_forza(*PF))
add(M1,2,"",256,"Giovedi","Ciclismo","Andatura di gara","51,2 chilometri",51.2,"km",bici_gara("3 x 12,8 chilometri in bicicletta alla velocita' prevista sui 90 chilometri, con 5 minuti per un giro in souplesse."))
add(M1,2,"",256,"Giovedi","Corsa a piedi","Andatura di gara","16 chilometri",16,"km",corsa_gara("3 x 4 chilometri di corsa alla velocita' prevista sui 21 chilometri, con 400 metri di camminata o di jogging per il recupero."))
add(M1,2,"",257,"Venerdi","Nuoto","Andatura di gara","2.600 metri",2600,"m",nuoto_gara("3 x 600 metri a nuoto alla velocita' prevista sui 2.000 metri, con 60 secondi di riposo.",None))
add(M1,2,"",257,"Sabato","Ciclismo","Endurance","86,4 chilometri",86.4,"km",bici_endurance("48",95,120,60))
add(M1,2,"",257,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",pesi_potenza(*PP))
add(M1,2,"",257,"Domenica","Nuoto","Endurance","3.200 metri",3200,"m",nuoto_end_him(28,34,"1.800",900))
add(M1,2,"",257,"Domenica","Corsa a piedi","Endurance","20,8 chilometri",20.8,"km",corsa_end_him("12,8",70,90,30))

# ===== 3a SETTIMANA (pp. 258-260) =====
add(M1,3,"",258,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(M1,3,"",258,"Martedi","Corsa a piedi","Velocita","17,6 chilometri",17.6,"km",corsa_velocita(4,35))
add(M1,3,"",258,"Martedi","Ciclismo","Velocita","57,6 chilometri",57.6,"km",bici_velocita(4,70))
add(M1,3,"",259,"Mercoledi","Nuoto","Velocita","2.800 metri",2800,"m",nuoto_velocita(4,1000))
add(M1,3,"",259,"Mercoledi","Pesi","Forza","-",None,"",pesi_forza(*PF))
add(M1,3,"",259,"Giovedi","Ciclismo","Andatura di gara","57,6 chilometri",57.6,"km",bici_gara("3 x 14,4 chilometri in bicicletta alla velocita' prevista sui 90 chilometri, con 5 minuti per un giro in souplesse."))
add(M1,3,"",259,"Giovedi","Corsa a piedi","Andatura di gara","17,6 chilometri",17.6,"km",corsa_gara("3 x 4,8 chilometri di corsa alla velocita' prevista sui 21 chilometri, con 400 metri di camminata o di jogging per il recupero."))
add(M1,3,"",260,"Venerdi","Nuoto","Andatura di gara","2.800 metri",2800,"m",nuoto_gara("3 x 700 metri a nuoto alla velocita' prevista sui 2.000 metri, con 60 secondi di riposo.",None))
add(M1,3,"",260,"Sabato","Ciclismo","Endurance","96 chilometri",96,"km",bici_endurance("51,2",105,135,70))
add(M1,3,"",260,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",pesi_potenza(*PP))
add(M1,3,"",260,"Domenica","Nuoto","Endurance","3.400 metri",3400,"m",nuoto_end_him(32,38,"2.000",1000))
add(M1,3,"",260,"Domenica","Corsa a piedi","Endurance","20,8 chilometri",20.8,"km",corsa_end_him("14,4",80,100,35))

# ===== 4a SETTIMANA - RIPRISTINO (pp. 261-263) =====
R = "Ripristino"
add(M1,4,R,261,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(M1,4,R,261,"Martedi","Corsa a piedi","Velocita","8,8 chilometri",8.8,"km",corsa_velocita(2,17))
add(M1,4,R,261,"Martedi","Ciclismo","Velocita","28,8 chilometri",28.8,"km",bici_velocita(2,35))
add(M1,4,R,262,"Mercoledi","Nuoto","Velocita","1.400 metri",1400,"m",nuoto_velocita(2,500))
add(M1,4,R,262,"Mercoledi","Pesi","Forza","-",None,"",pesi_forza(*PF_LOW))
add(M1,4,R,262,"Giovedi","Ciclismo","Andatura di gara","28,8 chilometri",28.8,"km",bici_gara("3 x 7,2 chilometri in bicicletta alla velocita' prevista sui 90 chilometri, con 3 minuti per un giro in souplesse."))
add(M1,4,R,262,"Giovedi","Corsa a piedi","Andatura di gara","8,8 chilometri",8.8,"km",corsa_gara("3 x 2.400 metri di corsa alla velocita' prevista sui 21 chilometri, con 400 metri di camminata o di jogging per il recupero."))
add(M1,4,R,263,"Venerdi","Nuoto","Andatura di gara","1.400 metri",1400,"m",nuoto_gara("3 x 350 metri a nuoto alla velocita' prevista sui 2.000 metri, con 60 secondi di riposo.",None))
add(M1,4,R,263,"Sabato","Ciclismo","Endurance","48 chilometri",48,"km",bici_endurance("25,6",105,135,35))
add(M1,4,R,263,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",pesi_potenza(*PP_LOW))
add(M1,4,R,263,"Domenica","Nuoto","Endurance","1.700 metri",1700,"m",nuoto_end_him(16,19,"1.000",500))
add(M1,4,R,263,"Domenica","Corsa a piedi","Endurance","11,2 chilometri",11.2,"km",corsa_end_him("7,2",40,50,"17 e mezzo"))

# ===== 5a SETTIMANA (pp. 264-266) =====
add(M2,5,"",264,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(M2,5,"",264,"Martedi","Corsa a piedi","Velocita","17,6 chilometri",17.6,"km",corsa_velocita(4,35))
add(M2,5,"",264,"Martedi","Ciclismo","Velocita","57,6 chilometri",57.6,"km",bici_velocita(4,70))
add(M2,5,"",265,"Mercoledi","Nuoto","Velocita","2.800 metri",2800,"m",nuoto_velocita(4,1000))
add(M2,5,"",265,"Mercoledi","Pesi","Forza","-",None,"",pesi_forza(*PF))
add(M2,5,"",265,"Giovedi","Ciclismo","Andatura di gara","57,6 chilometri",57.6,"km",bici_gara("3 x 14,4 chilometri in bicicletta alla velocita' prevista sui 90 chilometri, con 5 minuti per un giro in souplesse."))
add(M2,5,"",265,"Giovedi","Corsa a piedi","Andatura di gara","17,6 chilometri",17.6,"km",corsa_gara("3 x 4,8 chilometri di corsa alla velocita' prevista sui 21 chilometri, con 400 metri di camminata o di jogging per il recupero."))
add(M2,5,"",266,"Venerdi","Nuoto","Andatura di gara","2.800 metri",2800,"m",nuoto_gara("2 x 800 metri e 1 x 400 metri a nuoto alla velocita' prevista sui 2.000 metri, con 60 secondi di riposo.",None))
add(M2,5,"",266,"Sabato","Ciclismo","Endurance","96 chilometri",96,"km",bici_endurance("51,2",110,145,70))
add(M2,5,"",266,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",pesi_potenza(*PP))
add(M2,5,"",266,"Domenica","Nuoto","Endurance","3.400 metri",3400,"m",nuoto_end_him(32,38,"2.000",1000))
add(M2,5,"",266,"Domenica","Corsa a piedi","Endurance","22,4 chilometri",22.4,"km",corsa_end_him("14,4",80,100,35))

# ===== 6a SETTIMANA (pp. 267-269) =====
NO_PROGR = True
add(M2,6,"",267,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(M2,6,"",267,"Martedi","Corsa a piedi","Velocita","19,2 chilometri",19.2,"km",corsa_velocita(4,40))
add(M2,6,"",267,"Martedi","Ciclismo","Velocita","64 chilometri",64,"km",bici_velocita(4,80))
add(M2,6,"",268,"Mercoledi","Nuoto","Velocita","3.000 metri",3000,"m",nuoto_velocita(4,1100))
add(M2,6,"",268,"Mercoledi","Pesi","Forza","-",None,"",pesi_forza(*PF, nota=True))
add(M2,6,"",268,"Giovedi","Ciclismo","Andatura di gara","64 chilometri",64,"km",bici_gara("3 x 16 chilometri in bicicletta alla velocita' prevista sui 90 chilometri, con 5 minuti per un giro in souplesse."))
add(M2,6,"",268,"Giovedi","Corsa a piedi","Andatura di gara","19,2 chilometri",19.2,"km",corsa_gara("3 x 5,6 chilometri di corsa alla velocita' prevista sui 21 chilometri, con 400 metri di camminata o di jogging per il recupero."))
add(M2,6,"",269,"Venerdi","Nuoto","Andatura di gara","3.000 metri",3000,"m",nuoto_gara("2 x 900 metri e 1 x 200 metri a nuoto alla velocita' prevista sui 2.000 metri, con 60 secondi di riposo.",None))
add(M2,6,"",269,"Sabato","Ciclismo","Endurance","105,6 chilometri",105.6,"km",bici_endurance("54,4",115,150,80))
add(M2,6,"",269,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",pesi_potenza(*PP))
add(M2,6,"",269,"Domenica","Nuoto","Endurance","3.800 metri",3800,"m",nuoto_end_him(36,42,"2.200",1100))
add(M2,6,"",269,"Domenica","Corsa a piedi","Endurance","19,2 chilometri",19.2,"km",corsa_end_him("16",90,110,40))

# ===== 7a SETTIMANA (pp. 270-272) =====
T7 = "Tapering (solo Corsa a piedi)"
add(M2,7,T7,270,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(M2,7,T7,270,"Martedi","Corsa a piedi","Velocita","12,8 chilometri",12.8,"km",corsa_velocita(2,25))
add(M2,7,T7,270,"Martedi","Ciclismo","Velocita","70,4 chilometri",70.4,"km",bici_velocita(4,90))
add(M2,7,T7,271,"Mercoledi","Nuoto","Velocita","3.200 metri",3200,"m",nuoto_velocita(4,1200))
add(M2,7,T7,271,"Mercoledi","Pesi","Forza","-",None,"",pesi_forza(*PF))
add(M2,7,T7,271,"Giovedi","Ciclismo","Andatura di gara","70,4 chilometri",70.4,"km",bici_gara("3 x 17,6 chilometri in bicicletta alla velocita' prevista sui 90 chilometri, con 5 minuti per un giro in souplesse."))
add(M2,7,T7,271,"Giovedi","Corsa a piedi","Andatura di gara","12,8 chilometri",12.8,"km",corsa_gara("3 x 2,4 chilometri di corsa alla velocita' prevista sui 21 chilometri, con 400 metri di camminata o di jogging per il recupero."))
add(M2,7,T7,272,"Venerdi","Nuoto","Andatura di gara","3.200 metri",3200,"m",nuoto_gara("2 x 1.000 metri a nuoto alla velocita' prevista sui 2.000 metri, con 60 secondi di riposo.",None))
add(M2,7,T7,272,"Sabato","Ciclismo","Endurance","115,2 chilometri",115.2,"km",bici_endurance("57,6",120,155,90))
add(M2,7,T7,272,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",pesi_potenza(*PP))
add(M2,7,T7,272,"Domenica","Nuoto","Endurance","4.000 metri",4000,"m",nuoto_end_him(40,46,"2.400",1200))
add(M2,7,T7,272,"Domenica","Corsa a piedi","Endurance","12,8 chilometri",12.8,"km",corsa_end_him("8",45,55,25))

# ===== 8a SETTIMANA - TAPERING (p. 273, parziale) =====
T8 = "Tapering (incompleta)"
add(M2,8,T8,273,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(M2,8,T8,273,"Martedi","Corsa a piedi","Velocita","6,4 chilometri",6.4,"km",
    ["In questa sessione sono compresi del lavoro aerobico, vari allunghi e solamente uno o due sforzi sui 400 metri ad andatura di gara. Il volume e' il 30%, o meno del 30%, delle sessioni d'allenamento della precedente settimana."], descr=True)
add(M2,8,T8,273,"Martedi","Ciclismo","Velocita","22,4 chilometri",22.4,"km",
    ["In questa sessione sono compresi del lavoro aerobico, vari allunghi e solamente uno o due sforzi di 1 minuto ad andatura di gara. Il volume d'allenamento e' il 30%, o meno del 30%, delle sessioni della precedente settimana."], descr=True)
add(M2,8,T8,273,"Mercoledi","Nuoto","Velocita","1.600 metri",1600,"m",[
    "2 x 25 metri a nuoto alla velocita' prevista sui 100 metri, con un riposo uguale.",
    "50 metri a nuoto, a ritmo blando.",
    "2 x 50 metri a nuoto alla velocita' prevista sui 200 metri, con 30 secondi di riposo.",
    "50 metri a nuoto, a ritmo blando.",
    "2 x 100 metri a nuoto alla velocita' prevista sui 500 metri, con 40 secondi riposo.",
    "100 metri a nuoto, a ritmo blando.",
    SUPPL_NUOTO])
add(M2,8,T8,273,"Mercoledi","Pesi","Forza","-",None,"",pesi_forza(*PF_LOW))
add(M2,8,T8,273,"Giovedi","Ciclismo","Andatura di gara","16 chilometri",16,"km",
    ["Questa sessione viene sostituita dalla gara prevista per la fine della settimana. Effettuare del ciclismo aerobico con uno o due sforzi di 1 minuto all'andatura di gara per raggiungere l'obiettivo della quantita' di allenamento, che e' il 50% delle sessioni delle tre settimane precedenti."], descr=True)

TUTTE = list(dati2.TUTTE) + NEW
