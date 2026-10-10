# -*- coding: utf-8 -*-
# DISTANZA OLIMPICA - settimane 1-12 (pp. 218-236; manca p. 237)
import sys
sys.path.insert(0,'/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad')
import dati4
from dati import (corsa_velocita, bici_velocita, nuoto_velocita, bici_gara, corsa_gara,
                  SUPPL_CORSA, SUPPL_BICI, SUPPL_NUOTO, MOV_BASE, MOV_PLIO, NO_PROGR)

OLY = "Triathlon Olimpico"
MB1 = "Primo Mesociclo - Fase di base"
MB2 = "Secondo Mesociclo - Fase di base"
MG3 = "Terzo Mesociclo - Fase di preparazione alla gara"
NEW = []

def add(meso, sett, nota, pag, giorno, disc, focus, vol_txt, vol_num, unita, serie, fase, descr=False):
    NEW.append(dict(piano=OLY, meso=meso, sett=sett, nota=nota, pag=pag, giorno=giorno, disc=disc,
                    focus=focus, vol_txt=vol_txt, vol_num=vol_num, unita=unita, serie=serie,
                    fase=fase, descr=descr))

# ---------- FASE DI BASE (settimane 1-8): formato a prescrizione, non a serie ----------
PESI_F = ["1 x 12 ripetizioni al 50% di 1 RM.", "2 x da 6 a 8 ripetizioni all'85% di 1 RM.",
          "Tutti i movimenti specifici di ciclismo, di nuoto e di corsa a piedi e i movimenti supplementari."]
PESI_F_LOW = ["1 x 6 ripetizioni al 50% di 1 RM.", "1 x da 3 a 4 ripetizioni all'85% di 1 RM.",
              "Tutti i movimenti specifici di ciclismo, di nuoto e di corsa a piedi e i movimenti supplementari."]
PESI_P = ["1 x 20 ripetizioni al 50% di 1 RM.", "2 x 6 ripetizioni al 50% di 1 RM, esplosive.",
          "Tutti i movimenti specifici di ciclismo, di nuoto e di corsa a piedi, i movimenti supplementari e la pliometria."]
PESI_P_LOW = ["1 x 10 ripetizioni al 50% di 1 RM.", "1 x 6 ripetizioni al 50% di 1 RM, esplosive.",
              "Tutti i movimenti specifici di ciclismo, di nuoto e di corsa a piedi, i movimenti supplementari e la pliometria."]

def base(meso, sett, nota, pag, corsa_int, corsa_f, bici_int, bici_f, nuoto_int, nuoto_f,
         bici_lunga, bici_lunga_f, nuoto_lungo, nuoto_lungo_f, corsa_lunga, corsa_lunga_f,
         pesi_forza, pesi_pot):
    F = "Base"
    def s(v, unit, forza):
        r = [f"{v} {unit} da 12 a 14 RPE." if unit else v]
        if forza: r.append(f"Endurance sulla forza: {forza}.")
        return r
    def sl(v, unit, forza):
        r = [f"{v} {unit} a <12 RPE."]
        if forza: r.append(f"Endurance sulla forza: {forza}.")
        return r
    add(meso,sett,nota,pag,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."],F)
    add(meso,sett,nota,pag,"Martedi","Corsa a piedi","Distanza intermedia",f"{corsa_int} chilometri",
        float(str(corsa_int).replace(",",".")),"km",s(corsa_int,"chilometri",corsa_f),F)
    add(meso,sett,nota,pag,"Martedi","Ciclismo","Distanza intermedia",f"{bici_int} chilometri",
        float(str(bici_int).replace(",",".")),"km",s(bici_int,"chilometri",bici_f),F)
    add(meso,sett,nota,pag,"Mercoledi","Nuoto","Distanza intermedia",f"{nuoto_int} metri",
        int(str(nuoto_int).replace(".","")),"m",s(nuoto_int,"metri",nuoto_f),F)
    add(meso,sett,nota,pag,"Mercoledi","Pesi","Forza","-",None,"",pesi_forza,F)
    add(meso,sett,nota,pag,"Giovedi","Corsa a piedi","Distanza intermedia",f"{corsa_int} chilometri",
        float(str(corsa_int).replace(",",".")),"km",s(corsa_int,"chilometri",corsa_f),F)
    add(meso,sett,nota,pag,"Giovedi","Ciclismo","Distanza intermedia",f"{bici_int} chilometri",
        float(str(bici_int).replace(",",".")),"km",s(bici_int,"chilometri",bici_f),F)
    add(meso,sett,nota,pag,"Venerdi","Nuoto","Distanza intermedia",f"{nuoto_int} metri",
        int(str(nuoto_int).replace(".","")),"m",s(nuoto_int,"metri",nuoto_f),F)
    add(meso,sett,nota,pag,"Sabato","Ciclismo","Distanza lunga",f"{bici_lunga} chilometri",
        float(str(bici_lunga).replace(",",".")),"km",sl(bici_lunga,"chilometri",bici_lunga_f),F)
    add(meso,sett,nota,pag,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",pesi_pot,F)
    add(meso,sett,nota,pag,"Domenica","Nuoto","Distanza lunga",f"{nuoto_lungo} metri",
        int(str(nuoto_lungo).replace(".","")),"m",sl(nuoto_lungo,"metri",nuoto_lungo_f),F)
    add(meso,sett,nota,pag,"Domenica","Corsa a piedi","Distanza lunga",f"{corsa_lunga} chilometri",
        float(str(corsa_lunga).replace(",",".")),"km",sl(corsa_lunga,"chilometri",corsa_lunga_f),F)

R = "Ripristino"
base(MB1,1,"",218,"11,2","10 minuti","32","20 minuti","1.600","400 metri","51,2","20 minuti","2.200","400 metri","14,4","10 minuti",PESI_F,PESI_P)
base(MB1,2,"",219,"12","12 minuti","35,2","25 minuti","1.800","500 metri","57,6","25 minuti","2.400","500 metri","15,2","12 minuti",PESI_F,PESI_P)
base(MB1,3,"",220,"12,8","15 minuti","38,4","30 minuti","2.000","600 metri","64","30 minuti","2.600","600 metri","16","15 minuti",PESI_F,PESI_P)
base(MB1,4,R,221,"6,4","8 minuti","19,2","15 minuti","1.000","300 metri","20","15 minuti","1.300","300 metri","8",None,PESI_F_LOW,PESI_P_LOW)
base(MB2,5,"",222,"12,8","15 minuti","38,4","30 minuti","2.000","600 metri","64","30 minuti","2.600","600 metri","16","15 minuti",PESI_F,PESI_P)
base(MB2,6,"",223,"13,6","20 minuti","41,6","40 minuti","2.200","700 metri","70,4","40 minuti","2.800","700 metri","17,6","20 minuti",PESI_F,PESI_P)
base(MB2,7,"",224,"14,4","25 minuti","44,8","50 minuti","2.400","800 metri","76,8","50 minuti","3.000","800 metri","19,2","25 minuti",PESI_F,PESI_P)
base(MB2,8,R,225,"7,2","12 minuti","22,4","25 minuti","1.200","400 metri","38,4","25 minuti","1.500","400 metri","9,6","12 minuti",PESI_F_LOW,PESI_P_LOW)

# ---------- FASE DI PREPARAZIONE ALLA GARA (settimane 9-12) ----------
G = "Gara"
# NB: nel libro l'Ottava Serie delle sedute di ciclismo sulla velocita' recita
# "Della corsa aerobica supplementare" (refuso tipografico): trascritto com'e' stampato.
def bici_vel_oly(n, minuti):
    s = bici_velocita(n, minuti)
    s[7] = SUPPL_CORSA
    return s

def nuoto_gara_oly(testo):
    return [testo, "100 metri a nuoto, a ritmo blando.", SUPPL_NUOTO]

def bici_end_oly(km, mn, mx, minuti):
    return [
        f"{km} chilometri o da {mn} a {mx} minuti in bicicletta in modo continuato alla cadenza prevista e alla velocita' prevista sui 90 chilometri. Prestare particolare attenzione ai momenti in cui verranno assunti dei liquidi e a quelli in cui si cerchera' di alimentarsi, nello stesso modo che verra' adottato poi nella gara a cui si e' deciso di partecipare.",
        f"Una serie da {minuti} minuti di endurance sulla forza utilizzando un rapporto che produca da 40 a 60 rpm ad un'intensita' aerobica assumendo la posizione che si prevede di utilizzare durante la gara.",
        SUPPL_BICI,
    ]

def nuoto_end_oly(mn, mx, metri, forza_m):
    return [
        f"Da {mn} a {mx} minuti o {metri} metri a nuoto in modo continuato, utilizzando almeno un sollevamento della testa ogni 25 metri, o ogni da 12 a 20 bracciate alla velocita' prevista sui 3.200 metri. Indossare l'attrezzatura (gli occhialini, la muta e il costume per la gara) che verra' utilizzata durante la gara.",
        f"{forza_m} metri a nuoto di endurance sulla forza ad un'intensita' aerobica utilizzando delle palette.",
        SUPPL_NUOTO,
    ]

def corsa_end_oly(km, mn, mx, minuti):
    return [
        f"{km} chilometri o da {mn} a {mx} minuti di corsa in modo continuato alla velocita' prevista sulla distanza della mezza maratona.",
        f"{minuti} minuti di lavoro di endurance sulla forza correndo fino ad una pendenza dal 2% al 4% a velocita' aerobica.",
        SUPPL_CORSA,
    ]

PG_F  = ["1 x 12 ripetizioni al 50% di 1 RM.", "2 x da 6 a 8 ripetizioni all'85% di 1 RM.", MOV_BASE]
PG_F1 = ["1 x 12 ripetizioni al 50% di 1 RM.", "2 x da 6 a 8 ripetizioni all'85% di 1 RM.", NO_PROGR, MOV_BASE]
PG_FL = ["1 x 6 ripetizioni al 50% di 1 RM.", "1 x da 3 a 4 ripetizioni all'85% di 1 RM.", MOV_BASE]
PG_P  = ["1 x 20 ripetizioni al 50% di 1 RM.", "2 x 6 ripetizioni al 50% di 1 RM, esplosive.", MOV_PLIO]
PG_P1 = ["1 x 20 ripetizioni al 50% di 1 RM.", "2 x 6 ripetizioni al 50% di 1 RM, esplosive.", NO_PROGR, MOV_PLIO]

# ===== 9a SETTIMANA (pp. 226-228) =====
add(MG3,9,"",226,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."],G)
add(MG3,9,"",226,"Martedi","Corsa a piedi","Velocita","11,2 chilometri",11.2,"km",corsa_velocita(4,20),G)
add(MG3,9,"",226,"Martedi","Ciclismo","Velocita","38,4 chilometri",38.4,"km",bici_vel_oly(4,30),G)
add(MG3,9,"",227,"Mercoledi","Nuoto","Velocita","2.200 metri",2200,"m",nuoto_velocita(4,800),G)
add(MG3,9,"",227,"Mercoledi","Pesi","Forza","-",None,"",PG_F1,G)
add(MG3,9,"",227,"Giovedi","Ciclismo","Andatura di gara","41,6 chilometri",41.6,"km",bici_gara("3 x 8 chilometri in bicicletta alla velocita' prevista sui 40 chilometri, con da 1 a 2 minuti per un giro in souplesse."),G)
add(MG3,9,"",227,"Giovedi","Corsa a piedi","Andatura di gara","12,8 chilometri",12.8,"km",corsa_gara("3 x 2.000 metri di corsa alla velocita' prevista sui 10 chilometri, con 400 metri di camminata o di jogging per il recupero."),G)
add(MG3,9,"",228,"Venerdi","Nuoto","Andatura di gara","2.200 metri",2200,"m",nuoto_gara_oly("3 x 300 metri a nuoto alla velocita' prevista sui 1.600 metri, con 30 secondi di riposo."),G)
add(MG3,9,"",228,"Sabato","Ciclismo","Endurance","68,8 chilometri",68.8,"km",bici_end_oly("32",50,75,30),G)
add(MG3,9,"",228,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",PG_P1,G)
add(MG3,9,"",228,"Domenica","Nuoto","Endurance","2.700 metri",2700,"m",nuoto_end_oly(20,25,"1.200",800),G)
add(MG3,9,"",228,"Domenica","Corsa a piedi","Endurance","17,6 chilometri",17.6,"km",corsa_end_oly("8",30,40,15),G)

# ===== 10a SETTIMANA (pp. 229-231) =====
add(MG3,10,"",229,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."],G)
add(MG3,10,"",229,"Martedi","Corsa a piedi","Velocita","11,2 chilometri",11.2,"km",corsa_velocita(4,20),G)
add(MG3,10,"",229,"Martedi","Ciclismo","Velocita","38,4 chilometri",38.4,"km",bici_vel_oly(4,30),G)
add(MG3,10,"",230,"Mercoledi","Nuoto","Velocita","2.200 metri",2200,"m",nuoto_velocita(4,800),G)
add(MG3,10,"",230,"Mercoledi","Pesi","Forza","-",None,"",PG_F,G)
add(MG3,10,"",230,"Giovedi","Ciclismo","Andatura di gara","41,6 chilometri",41.6,"km",bici_gara("4 x 8 chilometri in bicicletta alla velocita' prevista sui 40 chilometri, con da 1 a 2 minuti per un giro in souplesse."),G)
add(MG3,10,"",230,"Giovedi","Corsa a piedi","Andatura di gara","12,8 chilometri",12.8,"km",corsa_gara("4 x 2.000 metri di corsa alla velocita' prevista sui 10 chilometri, con 400 metri di camminata o di jogging per il recupero."),G)
add(MG3,10,"",231,"Venerdi","Nuoto","Andatura di gara","2.200 metri",2200,"m",nuoto_gara_oly("3 x 300 metri a nuoto alla velocita' prevista sui 1.600 metri, con 30 secondi di riposo."),G)
add(MG3,10,"",231,"Sabato","Ciclismo","Endurance","68,8 chilometri",68.8,"km",bici_end_oly("38,4",60,85,40),G)
add(MG3,10,"",231,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",PG_P,G)
add(MG3,10,"",231,"Domenica","Nuoto","Endurance","2.700 metri",2700,"m",nuoto_end_oly(22,27,"1.400",900),G)
add(MG3,10,"",231,"Domenica","Corsa a piedi","Endurance","17,6 chilometri",17.6,"km",corsa_end_oly("12,8",35,45,20),G)

# ===== 11a SETTIMANA (pp. 232-234) =====
add(MG3,11,"",232,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."],G)
add(MG3,11,"",232,"Martedi","Corsa a piedi","Velocita","11,2 chilometri",11.2,"km",corsa_velocita(4,20),G)
add(MG3,11,"",232,"Martedi","Ciclismo","Velocita","38,4 chilometri",38.4,"km",bici_vel_oly(4,30),G)
add(MG3,11,"",233,"Mercoledi","Nuoto","Velocita","2.200 metri",2200,"m",nuoto_velocita(4,800),G)
add(MG3,11,"",233,"Mercoledi","Pesi","Forza","-",None,"",PG_F,G)
add(MG3,11,"",233,"Giovedi","Ciclismo","Andatura di gara","41,6 chilometri",41.6,"km",bici_gara("5 x 8 chilometri in bicicletta alla velocita' prevista sui 40 chilometri, con da 1 a 2 minuti per un giro in souplesse."),G)
add(MG3,11,"",233,"Giovedi","Corsa a piedi","Andatura di gara","12,8 chilometri",12.8,"km",corsa_gara("5 x 2.000 metri di corsa alla velocita' prevista sui 10 chilometri, con 400 metri di camminata o di jogging per il recupero."),G)
add(MG3,11,"",234,"Venerdi","Nuoto","Andatura di gara","2.200 metri",2200,"m",nuoto_gara_oly("5 x 300 metri a nuoto alla velocita' prevista sui 1.600 metri, con 30 secondi di riposo."),G)
add(MG3,11,"",234,"Sabato","Ciclismo","Endurance","68,8 chilometri",68.8,"km",bici_end_oly("44,8",70,95,50),G)
add(MG3,11,"",234,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",PG_P,G)
add(MG3,11,"",234,"Domenica","Nuoto","Endurance","2.700 metri",2700,"m",nuoto_end_oly(24,30,"1.600",1000),G)
add(MG3,11,"",234,"Domenica","Corsa a piedi","Endurance","17,6 chilometri",17.6,"km",corsa_end_oly("11,2",40,55,25),G)

# ===== 12a SETTIMANA - RIPRISTINO (pp. 235-236; manca p. 237) =====
R12 = "Ripristino (incompleta)"
add(MG3,12,R12,235,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."],G)
add(MG3,12,R12,235,"Martedi","Corsa a piedi","Velocita","5,6 chilometri",5.6,"km",corsa_velocita(2,20),G)
add(MG3,12,R12,235,"Martedi","Ciclismo","Velocita","19,2 chilometri",19.2,"km",bici_vel_oly(2,15),G)
add(MG3,12,R12,236,"Mercoledi","Nuoto","Velocita","1.100 metri",1100,"m",nuoto_velocita(2,400),G)
add(MG3,12,R12,236,"Mercoledi","Pesi","Forza","-",None,"",PG_FL,G)
add(MG3,12,R12,236,"Giovedi","Ciclismo","Andatura di gara","20,8 chilometri",20.8,"km",bici_gara("2 x 8 chilometri in bicicletta alla velocita' prevista sui 40 chilometri, con da 1 a 2 minuti per un giro in souplesse."),G)
add(MG3,12,R12,236,"Giovedi","Corsa a piedi","Andatura di gara","6,4 chilometri",6.4,"km",corsa_gara("2 x 2.000 metri di corsa alla velocita' prevista sui 10 chilometri, con 400 metri di camminata o di jogging per il recupero."),G)

# ---- unione: Olimpico prima, poi Half-Ironman, poi Ironman ----
PREC = []
for s in dati4.TUTTE:
    d = dict(s); d["fase"] = "Gara"
    PREC.append(d)
TUTTE = NEW + [d for d in PREC if d["piano"] == "Half-Ironman"] + [d for d in PREC if d["piano"] == "Ironman"]
