# -*- coding: utf-8 -*-
# OLIMPICO settimane 13-16 (pp. 238-249) + SPRINT settimane 1-6 (pp. 202-208)
import sys
sys.path.insert(0,'/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad')
import dati5
from dati import (corsa_velocita, bici_velocita, nuoto_velocita, bici_gara, corsa_gara,
                  REC_TAPIS, REC_BICI, SUPPL_CORSA, SUPPL_BICI, SUPPL_NUOTO,
                  MOV_BASE, MOV_PLIO, NO_PROGR)
from dati5 import bici_vel_oly, nuoto_gara_oly, bici_end_oly, nuoto_end_oly, corsa_end_oly

OLY = "Triathlon Olimpico"
SPR = "Triathlon Sprint"
NEW = []

def add(piano, meso, sett, nota, pag, giorno, disc, focus, vol_txt, vol_num, unita, serie, fase="Gara", descr=False):
    NEW.append(dict(piano=piano, meso=meso, sett=sett, nota=nota, pag=pag, giorno=giorno, disc=disc,
                    focus=focus, vol_txt=vol_txt, vol_num=vol_num, unita=unita, serie=serie,
                    fase=fase, descr=descr))

# =========================================================================
# OLIMPICO - Quarto Mesociclo - Fase di preparazione alla gara (sett. 13-16)
# =========================================================================
MG4 = "Quarto Mesociclo - Fase di preparazione alla gara"
PG_F  = ["1 x 12 ripetizioni al 50% di 1 RM.", "2 x da 6 a 8 ripetizioni all'85% di 1 RM.", MOV_BASE]
PG_FL = ["1 x 6 ripetizioni al 50% di 1 RM.", "1 x da 3 a 4 ripetizioni all'85% di 1 RM.", MOV_BASE]
PG_P  = ["1 x 20 ripetizioni al 50% di 1 RM.", "2 x 6 ripetizioni al 50% di 1 RM, esplosive.", MOV_PLIO]

def settimana_oly(sett, p1, p2, p3, gio_bici, gio_corsa, ven_nuoto, sab_km, sab_mn, sab_mx, sab_min,
                  dom_mn, dom_mx, dom_m, dom_forza, corsa_km, corsa_mn, corsa_mx, corsa_min):
    add(OLY,MG4,sett,"",p1,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
    add(OLY,MG4,sett,"",p1,"Martedi","Corsa a piedi","Velocita","11,2 chilometri",11.2,"km",corsa_velocita(4,20))
    add(OLY,MG4,sett,"",p1,"Martedi","Ciclismo","Velocita","41,6 chilometri",41.6,"km",bici_vel_oly(4,30))
    add(OLY,MG4,sett,"",p2,"Mercoledi","Nuoto","Velocita","2.200 metri",2200,"m",nuoto_velocita(4,800))
    add(OLY,MG4,sett,"",p2,"Mercoledi","Pesi","Forza","-",None,"",PG_F)
    add(OLY,MG4,sett,"",p2,"Giovedi","Ciclismo","Andatura di gara","41,6 chilometri",41.6,"km",bici_gara(gio_bici))
    add(OLY,MG4,sett,"",p2,"Giovedi","Corsa a piedi","Andatura di gara","12,8 chilometri",12.8,"km",corsa_gara(gio_corsa))
    add(OLY,MG4,sett,"",p3,"Venerdi","Nuoto","Andatura di gara","2.200 metri",2200,"m",nuoto_gara_oly(ven_nuoto))
    add(OLY,MG4,sett,"",p3,"Sabato","Ciclismo","Endurance","68,8 chilometri",68.8,"km",bici_end_oly(sab_km,sab_mn,sab_mx,sab_min))
    add(OLY,MG4,sett,"",p3,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",PG_P)
    add(OLY,MG4,sett,"",p3,"Domenica","Nuoto","Endurance","2.700 metri",2700,"m",nuoto_end_oly(dom_mn,dom_mx,dom_m,dom_forza))
    add(OLY,MG4,sett,"",p3,"Domenica","Corsa a piedi","Endurance","17,6 chilometri",17.6,"km",corsa_end_oly(corsa_km,corsa_mn,corsa_mx,corsa_min))

settimana_oly(13,238,239,240,
  "3 x 8 chilometri in bicicletta alla velocita' prevista sui 40 chilometri, con da 1 a 2 minuti per un giro in souplesse.",
  "3 x 2.000 metri di corsa alla velocita' prevista sui 10 chilometri, con 400 metri di camminata o di jogging per il recupero.",
  "3 x 300 metri a nuoto alla velocita' prevista sui 1.600 metri, con 30 secondi di riposo.",
  "32",50,75,30, 20,25,"1.200",800, "8",30,40,15)
settimana_oly(14,241,242,243,
  "4 x 8 chilometri in bicicletta alla velocita' prevista sui 40 chilometri, con da 1 a 2 minuti per un giro in souplesse.",
  "4 x 2.000 metri di corsa alla velocita' prevista sui 10 chilometri, con 400 metri di camminata o di jogging per il recupero.",
  "3 x 300 metri a nuoto alla velocita' prevista sui 1.600 metri, con 30 secondi di riposo.",
  "38,4",60,85,40, 22,27,"1.400",900, "12,8",35,45,20)
settimana_oly(15,244,245,246,
  "5 x 8 chilometri in bicicletta alla velocita' prevista sui 40 chilometri, con da 1 a 2 minuti per un giro in souplesse.",
  "5 x 2.000 metri di corsa alla velocita' prevista sui 10 chilometri, con 400 metri di camminata o di jogging per il recupero.",
  "5 x 300 metri a nuoto alla velocita' prevista sui 1.600 metri, con 30 secondi di riposo.",
  "44,8",70,95,50, 24,30,"1.600",1000, "11,2",40,55,25)

# --- 16a settimana (Tapering), pp. 247-249 ---
T = "Tapering"
GARA = "Questa sessione viene sostituita dalla gara a cui si e' deciso di partecipare."
NOTA_GARA = "Nota del libro: se la gara e' prevista per la domenica, sarebbe opportuno eseguire un breve riscaldamento in ogni disciplina sul percorso di gara, nel caso sia possibile effettuarlo."
add(OLY,MG4,16,T,247,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(OLY,MG4,16,T,247,"Martedi","Corsa a piedi","Velocita","5,6 chilometri",5.6,"km",corsa_velocita(2,20))
add(OLY,MG4,16,T,247,"Martedi","Ciclismo","Velocita","20,8 chilometri",20.8,"km",bici_vel_oly(2,15))
add(OLY,MG4,16,T,248,"Mercoledi","Nuoto","Velocita","1.100 metri",1100,"m",nuoto_velocita(2,400))
add(OLY,MG4,16,T,248,"Mercoledi","Pesi","Forza","-",None,"",PG_FL)
add(OLY,MG4,16,T,248,"Giovedi","Ciclismo","Andatura di gara","16 chilometri",16,"km",
    ["Questa sessione viene sostituita dalla gara prevista per la fine della settimana. Effettuare del ciclismo aerobico con uno o due sforzi di 1 minuto all'andatura di gara per raggiungere l'obiettivo della quantita' di allenamento, che e' il 50% delle sessioni delle tre settimane precedenti."], descr=True)
add(OLY,MG4,16,T,248,"Giovedi","Corsa a piedi","Andatura di gara","3,2 chilometri",3.2,"km",
    ["Questa sessione viene sostituita dalla gara prevista per la fine della settimana. Comprende l'allenamento aerobico e solamente uno o due sforzi di 400 metri all'andatura di gara. La quantita' di allenamento e' il 50%, o meno del 50%, delle sessioni della settimana precedente."], descr=True)
add(OLY,MG4,16,T,249,"Venerdi","Nuoto","Andatura di gara","800 metri",800,"m",
    ["Questa sessione viene sostituita dalla gara prevista per la fine della settimana. Comprende l'allenamento aerobico e solamente uno o due sforzi sui 50 metri all'andatura di gara. La quantita' di allenamento e' il 50%, o meno del 50%, delle sessioni della settimana precedente."], descr=True)
add(OLY,MG4,16,T,249,"Sabato","Ciclismo","Endurance","Sostituita dalla gara",None,"",[GARA, NOTA_GARA], descr=True)
add(OLY,MG4,16,T,249,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",
    ["Vanno eliminati l'allenamento con i pesi e gli esercizi di pliometria, prima della gara."], descr=True)
add(OLY,MG4,16,T,249,"Domenica","Nuoto","Endurance","Sostituita dalla gara",None,"",[GARA], descr=True)
add(OLY,MG4,16,T,249,"Domenica","Corsa a piedi","Endurance","Sostituita dalla gara",None,"",[GARA], descr=True)

# =========================================================================
# SPRINT
# =========================================================================
SB1 = "Primo Mesociclo - Fase di base"
SG2 = "Secondo Mesociclo - Fase di preparazione alla gara"

PESI_F_B = ["1 x 12 ripetizioni al 50% di 1 RM.", "2 x da 6 a 8 ripetizioni all'85% di 1 RM.",
            "Tutti i movimenti specifici di ciclismo, di nuoto e di corsa a piedi e i movimenti supplementari."]
PESI_FL_B = ["1 x 6 ripetizioni al 50% di 1 RM.", "2 x da 3 a 4 ripetizioni all'85% di 1 RM.",
             "Tutti i movimenti specifici di ciclismo, di nuoto e di corsa a piedi e i movimenti supplementari."]
PESI_P_B = ["1 x 20 ripetizioni al 50% di 1 RM.", "2 x 6 ripetizioni al 50% di 1 RM, esplosive.",
            "Tutti i movimenti specifici di ciclismo, di nuoto e di corsa a piedi, i movimenti supplementari e la pliometria."]
PESI_PL_B = ["1 x 10 ripetizioni al 50% di 1 RM.", "1 x 6 ripetizioni al 50% di 1 RM, esplosive.",
             "Tutti i movimenti specifici di ciclismo, di nuoto e di corsa a piedi, i movimenti supplementari e la pliometria."]

def base_sprint(sett, nota, pag, corsa, bici, nuoto, bici_l, nuoto_l, corsa_l, pf, pp):
    F = "Base"
    def num(v): return float(str(v).replace(".","").replace(",","."))
    add(SPR,SB1,sett,nota,pag,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."],F)
    add(SPR,SB1,sett,nota,pag,"Martedi","Corsa a piedi","Distanza intermedia",f"{corsa} chilometri",num(corsa),"km",[f"{corsa} chilometri da 12 a 14 RPE."],F)
    add(SPR,SB1,sett,nota,pag,"Martedi","Ciclismo","Distanza intermedia",f"{bici} chilometri",num(bici),"km",[f"{bici} chilometri da 12 a 14 RPE."],F)
    add(SPR,SB1,sett,nota,pag,"Mercoledi","Nuoto","Distanza intermedia",f"{nuoto} metri",int(num(nuoto)),"m",[f"{nuoto} metri da 12 a 14 RPE."],F)
    add(SPR,SB1,sett,nota,pag,"Mercoledi","Pesi","Forza","-",None,"",pf,F)
    add(SPR,SB1,sett,nota,pag,"Giovedi","Corsa a piedi","Distanza intermedia",f"{corsa} chilometri",num(corsa),"km",[f"{corsa} chilometri da 12 a 14 RPE."],F)
    add(SPR,SB1,sett,nota,pag,"Giovedi","Ciclismo","Distanza intermedia",f"{bici} chilometri",num(bici),"km",[f"{bici} chilometri da 12 a 14 RPE."],F)
    add(SPR,SB1,sett,nota,pag,"Venerdi","Nuoto","Distanza intermedia",f"{nuoto} metri",int(num(nuoto)),"m",[f"{nuoto} metri da 12 a 14 RPE."],F)
    add(SPR,SB1,sett,nota,pag,"Sabato","Ciclismo","Distanza lunga",f"{bici_l} chilometri",num(bici_l),"km",[f"{bici_l} chilometri a <12 RPE."],F)
    add(SPR,SB1,sett,nota,pag,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",pp,F)
    add(SPR,SB1,sett,nota,pag,"Domenica","Nuoto","Distanza lunga",f"{nuoto_l} metri",int(num(nuoto_l)),"m",[f"{nuoto_l} metri a <12 RPE."],F)
    add(SPR,SB1,sett,nota,pag,"Domenica","Corsa a piedi","Distanza lunga",f"{corsa_l} chilometri",num(corsa_l),"km",[f"{corsa_l} chilometri a <12 RPE."],F)

base_sprint(1,"",202,"4,8","16","1.000","24","1.500","8",PESI_F_B,PESI_P_B)
base_sprint(2,"",202,"5,2","17,6","1.100","26,4","1.650","8,8",PESI_F_B,PESI_P_B)
base_sprint(3,"",203,"5,6","19,2","1.200","28,8","1.800","9,6",PESI_F_B,PESI_P_B)
base_sprint(4,"Ripristino",203,"2,8","9,6","600","14,4","900","4,8",PESI_FL_B,PESI_PL_B)

# --- Fase di preparazione alla gara: nello Sprint le sessioni non hanno serie di endurance sulla forza ---
def corsa_vel_spr(n):
    s = corsa_velocita(n, 0)
    return s[:6] + [SUPPL_CORSA]
def bici_vel_spr(n):
    s = bici_velocita(n, 0)
    return s[:6] + [SUPPL_BICI]
def nuoto_vel_spr(n):
    s = nuoto_velocita(n, 0)
    return s[:6] + [SUPPL_NUOTO]
def bici_end_spr(km, mn, mx):
    return [f"{km} chilometri o da {mn} a {mx} minuti in bicicletta in modo continuato alla cadenza prevista e alla velocita' prevista sui 90 chilometri (si dovrebbe essere in grado di portare a termine questa distanza abbastanza agevolmente). Effettuare l'allenamento sulla propria bicicletta da gara e assumendo la posizione che si prevede di utilizzare durante la gara, prestando particolare attenzione ai momenti in cui verranno assunti dei liquidi e a quelli in cui si cerchera' di alimentarsi, nello stesso modo che verra' adottato poi nella gara a cui si e' deciso di partecipare.", SUPPL_BICI]
def nuoto_end_spr(mn, mx, metri):
    return [f"Da {mn} a {mx} minuti o {metri} metri a nuoto in modo continuato, utilizzando almeno un sollevamento della testa ogni 25 metri, o ogni da 12 a 20 bracciate alla velocita' prevista sui 3.200 metri. Indossare l'attrezzatura (gli occhialini, la muta e il costume per la gara) che verra' utilizzata durante la gara.", SUPPL_NUOTO]
def corsa_end_spr(km, mn, mx):
    return [f"{km} chilometri o da {mn} a {mx} minuti di corsa in modo continuato alla velocita' prevista sulla distanza della mezza maratona.", SUPPL_CORSA]

PS_F1 = ["1 x 12 ripetizioni al 50% di 1 RM.", "2 x da 6 a 8 ripetizioni all'85% di 1 RM.", NO_PROGR, MOV_BASE]
PS_P1 = ["1 x 20 ripetizioni al 50% di 1 RM.", "2 x 6 ripetizioni al 50% di 1 RM, esplosive.", NO_PROGR, MOV_PLIO]
COMB = "Nota del libro: sarebbe il massimo se l'atleta riuscisse a combinare assieme queste sessioni d'allenamento (vedere il sesto capitolo)."

# ===== 5a SETTIMANA (pp. 204-206) =====
add(SPR,SG2,5,"",204,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(SPR,SG2,5,"",204,"Martedi","Corsa a piedi","Velocita","5,6 chilometri",5.6,"km",corsa_vel_spr(2))
add(SPR,SG2,5,"",204,"Martedi","Ciclismo","Velocita","17,6 chilometri",17.6,"km",bici_vel_spr(2))
add(SPR,SG2,5,"",205,"Mercoledi","Nuoto","Velocita","1.100 metri",1100,"m",nuoto_vel_spr(2))
add(SPR,SG2,5,"",205,"Mercoledi","Pesi","Forza","-",None,"",PS_F1)
add(SPR,SG2,5,"",205,"Giovedi","Ciclismo","Andatura di gara","17,6 chilometri",17.6,"km",
    bici_gara("2 x 4,8 chilometri in bicicletta alla velocita' prevista sui 20 chilometri, con un giro in souplesse di 1 minuto.")+[COMB])
add(SPR,SG2,5,"",205,"Giovedi","Corsa a piedi","Andatura di gara","5,6 chilometri",5.6,"km",
    corsa_gara("3 x 1.000 metri di corsa alla velocita' prevista sui 5.000 metri, con 400 metri di camminata o jogging per il recupero.")+[COMB])
add(SPR,SG2,5,"",205,"Venerdi","Nuoto","Andatura di gara","1.100 metri",1100,"m",
    nuoto_gara_oly("3 x 200 metri a nuoto alla velocita' prevista sui 1.600 metri, con 30 secondi di riposo."))
add(SPR,SG2,5,"",206,"Sabato","Ciclismo","Endurance","27,2 chilometri",27.2,"km",bici_end_spr("19,2",35,50))
add(SPR,SG2,5,"",206,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",PS_P1)
add(SPR,SG2,5,"",206,"Domenica","Nuoto","Endurance","1.600 metri",1600,"m",nuoto_end_spr(12,15,"700"))
add(SPR,SG2,5,"",206,"Domenica","Corsa a piedi","Endurance","8,8 chilometri",8.8,"km",corsa_end_spr("4,8",20,25))

# ===== 6a SETTIMANA (pp. 207-208; manca p. 209) =====
I6 = "Incompleta"
add(SPR,SG2,6,I6,207,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(SPR,SG2,6,I6,207,"Martedi","Corsa a piedi","Velocita","5,6 chilometri",5.6,"km",corsa_vel_spr(3))
add(SPR,SG2,6,I6,207,"Martedi","Ciclismo","Velocita","17,6 chilometri",17.6,"km",bici_vel_spr(3))
add(SPR,SG2,6,I6,208,"Mercoledi","Nuoto","Velocita","1.100 metri",1100,"m",nuoto_vel_spr(3))
add(SPR,SG2,6,I6,208,"Mercoledi","Pesi","Forza","-",None,"",PS_F1)
add(SPR,SG2,6,I6,208,"Giovedi","Ciclismo","Andatura di gara","17,6 chilometri",17.6,"km",
    bici_gara("3 x 4,8 chilometri in bicicletta alla velocita' prevista sui 20 chilometri, con un giro in souplesse di 1 minuto.")+[COMB])
add(SPR,SG2,6,I6,208,"Giovedi","Corsa a piedi","Andatura di gara","5,6 chilometri",5.6,"km",
    corsa_gara("4 x 1.000 metri di corsa alla velocita' prevista sui 5 chilometri, con 400 metri di camminata o di jogging per il recupero.")+[COMB])
add(SPR,SG2,6,I6,208,"Venerdi","Nuoto","Andatura di gara","1.100 metri",1100,"m",
    nuoto_gara_oly("4 x 200 metri a nuoto alla velocita' prevista sui 1.600 metri, con 30 secondi di riposo."))

# ---- unione: Olimpico, Sprint, Half-Ironman, Ironman ----
PREC = list(dati5.TUTTE)
oly = [d for d in PREC if d["piano"] == OLY] + [d for d in NEW if d["piano"] == OLY]
spr = [d for d in NEW if d["piano"] == SPR]
TUTTE = oly + spr + [d for d in PREC if d["piano"] == "Half-Ironman"] + [d for d in PREC if d["piano"] == "Ironman"]
