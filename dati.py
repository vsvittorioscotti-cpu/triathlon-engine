# -*- coding: utf-8 -*-
# Trascrizione piano Ironman - Primo e Secondo Mesociclo, Fase di preparazione alla gara
# Fonte: libro "Distanza Ironman", pagine 277-294

REC_TAPIS = "400 metri di camminata o di jogging per il recupero (in pista) o da 1 a 2 minuti di jogging in souplesse (sul tapis roulant)."
REC_BICI = "Da 1 a 2 minuti in bicicletta per un giro in souplesse."
SUPPL_CORSA = "Della corsa aerobica supplementare per raggiungere l'obiettivo della quantita' complessiva di allenamento."
SUPPL_BICI = "Del ciclismo aerobico supplementare per raggiungere l'obiettivo della quantita' complessiva di allenamento."
SUPPL_NUOTO = "Una serie o del nuoto aerobico supplementare per raggiungere l'obiettivo della quantita' complessiva di allenamento."

def corsa_velocita(n, minuti):
    return [
        f"{n} x 100 metri di allunghi (in pista) o {n} x 20 secondi di corsa (sul tapis roulant) alla velocita' prevista sui 400 metri, con 100 metri di camminata o di jogging (in pista) o 30 secondi di camminata per il recupero dopo essere scesi dal tapis roulant.",
        REC_TAPIS,
        f"{n} x 200 metri di allunghi (in pista) o {n} x 40 secondi di corsa (sul tapis roulant) alla velocita' prevista sugli 800 metri, con 100 metri di camminata o di jogging (in pista) o 40 secondi di camminata per il recupero dopo essere scesi dal tapis roulant.",
        REC_TAPIS,
        f"{n} x 400 metri di allunghi (in pista) o {n} x 90 secondi (sul tapis roulant) alla velocita' prevista sui 1.600 metri, con 100 metri di camminata o di jogging (in pista) o 30 secondi di camminata per il recupero dopo essere scesi dal tapis roulant.",
        REC_TAPIS,
        f"{minuti} minuti di lavoro di endurance sulla forza utilizzando un giubbotto appesantito o con un'inclinazione del tapis roulant. Combinare una velocita' e una pendenza (e un giubbotto appesantito nel caso in cui viene utilizzato) che possano consentire una frequenza cardiaca aerobica non eccessiva. Una pendenza del 2% puo' essere un buon punto di partenza.",
        SUPPL_CORSA,
    ]

def bici_velocita(n, minuti):
    return [
        f"{n} x 200 metri in bicicletta alla velocita' o alla potenza prevista sugli 800 metri, con un riposo uguale (un giro di recupero in souplesse).",
        REC_BICI,
        f"{n} x 400 metri alla velocita' prevista sui 1.600 metri, con 30 secondi per un giro di recupero.",
        REC_BICI,
        f"{n} x 800 metri in bicicletta alla velocita' prevista sui 3.200 metri, con 40 secondi per un giro di recupero.",
        REC_BICI,
        f"Una serie da {minuti} minuti di endurance sulla forza utilizzando un rapporto che produca da 40 a 60 rpm ad un'intensita' aerobica assumendo la posizione che si prevede di utilizzare durante la gara.",
        SUPPL_BICI,
    ]

def nuoto_velocita(n, forza_m):
    return [
        f"{n} x 25 metri a nuoto alla velocita' prevista sui 100 metri, con un riposo uguale.",
        "50 metri a nuoto, a ritmo blando.",
        f"{n} x 50 metri a nuoto alla velocita' prevista sui 200 metri, con 30 secondi di riposo.",
        "50 metri a nuoto, a ritmo blando.",
        f"{n} x 100 metri a nuoto alla velocita' prevista sui 500 metri, con 40 secondi riposo.",
        "100 metri a nuoto, a ritmo blando.",
        f"{forza_m} metri a nuoto di endurance sulla forza ad un'intensita' aerobica utilizzando delle palette.",
        SUPPL_NUOTO,
    ]

def bici_gara(testo):
    return [
        testo,
        "Da 1 a 2 minuti in bicicletta per un giro in souplesse. Utilizzare una cadenza prevista adeguata che sia di aiuto per la scelta dei rapporti da impiegare (vedere il terzo capitolo).",
        SUPPL_BICI,
    ]

def corsa_gara(testo):
    return [testo, SUPPL_CORSA]

def nuoto_gara(testo, forza_m):
    s = [testo, "100 metri a nuoto, a ritmo blando."]
    if forza_m:
        s.append(f"Una serie di {forza_m} metri a nuoto di endurance sulla forza.")
    s.append(SUPPL_NUOTO)
    return s

def bici_endurance(km, mn, mx, minuti):
    return [
        f"{km} chilometri o da {mn} a {mx} minuti in bicicletta in modo continuato alla cadenza prevista e alla velocita' prevista sui 180 chilometri. Prestare particolare attenzione ai momenti in cui verranno assunti dei liquidi e a quelli in cui si cerchera' di alimentarsi, nello stesso modo che verra' adottato poi nella gara a cui si e' deciso di partecipare.",
        f"Una serie da {minuti} minuti di endurance sulla forza utilizzando un rapporto che produca da 40 a 60 rpm ad un'intensita' aerobica assumendo la posizione che si prevede di utilizzare durante la gara.",
        SUPPL_BICI,
    ]

def nuoto_endurance(mn, mx, metri, forza_m):
    return [
        f"Da {mn} a {mx} minuti o {metri} metri a nuoto in modo continuato, utilizzando almeno un sollevamento della testa ogni 25 metri, o ogni da 12 a 20 bracciate alla velocita' prevista sui 4.000 metri. Indossare l'attrezzatura (gli occhialini, la muta e il costume per la gara) che verra' utilizzata durante la gara. Suddividere questa sessione in sforzi piu' brevi, per consentire delle pause per alimentarsi con il cibo.",
        f"{forza_m} metri a nuoto di endurance sulla forza ad un'intensita' aerobica utilizzando delle palette.",
        SUPPL_NUOTO,
    ]

def corsa_endurance(km, mn, mx, minuti):
    return [
        f"{km} chilometri o da {mn} a {mx} minuti di corsa in modo continuato alla velocita' prevista sulla distanza della maratona. Bisogna includere una breve pausa in cui si passeggia (da 1 a 2 minuti) ogni 1,6 chilometri, per consentire un recupero parziale e un'andatura di gara complessiva piu' veloce.",
        f"{minuti} minuti di lavoro di endurance sulla forza correndo fino ad una pendenza dal 2% al 4% a velocita' aerobica.",
        SUPPL_CORSA,
    ]

MOV_BASE = "Completare tutti i movimenti specifici di ciclismo, di nuoto e di corsa a piedi e i movimenti supplementari."
MOV_PLIO = "Completare tutti i movimenti specifici di ciclismo, di nuoto e di corsa a piedi e i movimenti supplementari, oltre a quelli relativi alla pliometria."
NO_PROGR = "Nessuna progressione nei pesi - Va mantenuto lo stesso numero di ripetizioni e la stessa quantita' di pesi utilizzata durante il periodo di base."

def pesi_forza(r1, r2, nota=False):
    s = [r1, r2]
    if nota:
        s.append(NO_PROGR)
    s.append(MOV_BASE)
    return s

def pesi_potenza(r1, r2, nota=False):
    s = [r1, r2]
    if nota:
        s.append(NO_PROGR)
    s.append(MOV_PLIO)
    return s

# ---- Struttura: (mesociclo, settimana, nota_settimana, pagina, giorno, disciplina, focus, volume_txt, volume_num, unita, serie[])
SESSIONI = []

def add(meso, sett, nota, pag, giorno, disc, focus, vol_txt, vol_num, unita, serie):
    SESSIONI.append(dict(meso=meso, sett=sett, nota=nota, pag=pag, giorno=giorno, disc=disc,
                         focus=focus, vol_txt=vol_txt, vol_num=vol_num, unita=unita, serie=serie))

M1 = "Primo Mesociclo - Fase di preparazione alla gara"
M2 = "Secondo Mesociclo - Fase di preparazione alla gara"

# =================== SETTIMANA 1 (pp. 277-279) ===================
add(M1,1,"",277,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(M1,1,"",277,"Martedi","Corsa a piedi","Velocita","19,2 chilometri",19.2,"km",corsa_velocita(4,40))
add(M1,1,"",277,"Martedi","Ciclismo","Velocita","72 chilometri",72,"km",bici_velocita(4,60))
add(M1,1,"",278,"Mercoledi","Nuoto","Velocita","3.200 metri",3200,"m",nuoto_velocita(4,1200))
add(M1,1,"",278,"Mercoledi","Pesi","Forza","-",None,"",pesi_forza("1 x 12 ripetizioni al 50% di 1 RM.","2 x da 6 a 8 ripetizioni all'85% di 1 RM.",True))
add(M1,1,"",278,"Giovedi","Ciclismo","Andatura di gara","72 chilometri",72,"km",bici_gara("4 x 4,8 chilometri in bicicletta alla velocita' prevista sui 20 chilometri, con 1 minuto per un giro in souplesse."))
add(M1,1,"",278,"Giovedi","Corsa a piedi","Andatura di gara","19,2 chilometri",19.2,"km",corsa_gara("6 x 800 metri di corsa alla velocita' prevista sui 5 chilometri, con 400 metri di camminata o di jogging per il recupero."))
add(M1,1,"",278,"Venerdi","Nuoto","Andatura di gara","3.200 metri",3200,"m",nuoto_gara("5 x 100 metri a nuoto alla velocita' prevista sui 500 metri, con 30 secondi di riposo.",1200))
add(M1,1,"",279,"Sabato","Ciclismo","Endurance","120 chilometri",120,"km",bici_endurance("57,6",108,144,60))
add(M1,1,"",279,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",pesi_potenza("1 x 20 ripetizioni al 50% di 1 RM.","2 x 6 ripetizioni al 50% di 1 RM, esplosive.",True))
add(M1,1,"",279,"Domenica","Nuoto","Endurance","4.500 metri",4500,"m",nuoto_endurance(35,50,"2.500",1200))
add(M1,1,"",279,"Domenica","Corsa a piedi","Endurance","24 chilometri",24,"km",corsa_endurance("16",80,100,45))

# =================== SETTIMANA 2 (pp. 280-282) ===================
add(M1,2,"",280,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(M1,2,"",280,"Martedi","Corsa a piedi","Velocita","17,6 chilometri",17.6,"km",corsa_velocita(4,35))
add(M1,2,"",280,"Martedi","Ciclismo","Velocita","64 chilometri",64,"km",bici_velocita(4,55))
add(M1,2,"",281,"Mercoledi","Nuoto","Velocita","3.000 metri",3000,"m",nuoto_velocita(4,1100))
add(M1,2,"",281,"Mercoledi","Pesi","Forza","-",None,"",pesi_forza("1 x 12 ripetizioni al 50% di 1 RM.","2 x da 6 a 8 ripetizioni all'85% di 1 RM."))
add(M1,2,"",281,"Giovedi","Ciclismo","Andatura di gara","64 chilometri",64,"km",bici_gara("3 x 12,8 chilometri in bicicletta alla velocita' prevista sui 40 chilometri, con 5 minuti per un giro in souplesse."))
add(M1,2,"",281,"Giovedi","Corsa a piedi","Andatura di gara","17,6 chilometri",17.6,"km",corsa_gara("6 x 1.600 metri di corsa alla velocita' prevista sui 10 chilometri, con 400 metri di camminata o di jogging per il recupero."))
add(M1,2,"",281,"Venerdi","Nuoto","Andatura di gara","3.000 metri",3000,"m",nuoto_gara("4 x 300 metri a nuoto alla velocita' prevista sui 1.600 metri, con 30 secondi di riposo.",1200))
add(M1,2,"",282,"Sabato","Ciclismo","Endurance","105,6 chilometri",105.6,"km",bici_endurance("51,2",96,128,55))
add(M1,2,"",282,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",pesi_potenza("1 x 20 ripetizioni al 50% di 1 RM.","2 x 6 ripetizioni al 50% di 1 RM, esplosive."))
add(M1,2,"",282,"Domenica","Nuoto","Endurance","4.000 metri",4000,"m",nuoto_endurance(28,40,"2.000",1200))
add(M1,2,"",282,"Domenica","Corsa a piedi","Endurance","20,8 chilometri",20.8,"km",corsa_endurance("12,8",64,80,40))

# =================== SETTIMANA 3 (pp. 283-285) ===================
add(M1,3,"",283,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(M1,3,"",283,"Martedi","Corsa a piedi","Velocita","19,2 chilometri",19.2,"km",corsa_velocita(4,40))
add(M1,3,"",283,"Martedi","Ciclismo","Velocita","80 chilometri",80,"km",bici_velocita(4,60))
add(M1,3,"",284,"Mercoledi","Nuoto","Velocita","3.200 metri",3200,"m",nuoto_velocita(4,1000))
add(M1,3,"",284,"Mercoledi","Pesi","Forza","-",None,"",pesi_forza("1 x 12 ripetizioni al 50% di 1 RM.","2 x da 6 a 8 ripetizioni all'85% di 1 RM."))
add(M1,3,"",284,"Giovedi","Ciclismo","Andatura di gara","80 chilometri",80,"km",bici_gara("2 x 28,8 chilometri in bicicletta alla velocita' prevista sui 90 chilometri, con 5 minuti per un giro in souplesse."))
add(M1,3,"",284,"Giovedi","Corsa a piedi","Andatura di gara","19,2 chilometri",19.2,"km",corsa_gara("3 x 4,8 chilometri di corsa alla velocita' prevista sui 21 chilometri, con 800 metri di camminata o di jogging per il recupero."))
add(M1,3,"",284,"Venerdi","Nuoto","Andatura di gara","3.200 metri",3200,"m",nuoto_gara("2 x 800 metri a nuoto alla velocita' prevista sui 2.000 metri, con 60 secondi di riposo.",1200))
add(M1,3,"",285,"Sabato","Ciclismo","Endurance","136 chilometri",136,"km",bici_endurance("70,4",105,135,60))
add(M1,3,"",285,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",pesi_potenza("1 x 20 ripetizioni al 50% di 1 RM.","2 x 6 ripetizioni al 50% di 1 RM, esplosive."))
add(M1,3,"",285,"Domenica","Nuoto","Endurance","5.000 metri",5000,"m",nuoto_endurance(42,60,"3.000",1200))
add(M1,3,"",285,"Domenica","Corsa a piedi","Endurance","27,2 chilometri",27.2,"km",corsa_endurance("17,6",88,110,40))

# =================== SETTIMANA 4 - RIPRISTINO (pp. 286-288) ===================
R = "Ripristino"
add(M1,4,R,286,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(M1,4,R,286,"Martedi","Corsa a piedi","Velocita","9,6 chilometri",9.6,"km",corsa_velocita(2,20))
add(M1,4,R,286,"Martedi","Ciclismo","Velocita","40 chilometri",40,"km",bici_velocita(2,30))
add(M1,4,R,287,"Mercoledi","Nuoto","Velocita","1.600 metri",1600,"m",nuoto_velocita(2,600))
add(M1,4,R,287,"Mercoledi","Pesi","Forza","-",None,"",pesi_forza("1 x 6 ripetizioni al 50% di 1 RM.","1 x da 3 a 4 ripetizioni all'85% di 1 RM."))
add(M1,4,R,287,"Giovedi","Ciclismo","Andatura di gara","40 chilometri",40,"km",bici_gara("2 x 14,4 chilometri in bicicletta alla velocita' prevista sui 90 chilometri, con 3 minuti per un giro in souplesse."))
add(M1,4,R,287,"Giovedi","Corsa a piedi","Andatura di gara","9,6 chilometri",9.6,"km",corsa_gara("2 x 2.400 metri di corsa alla velocita' prevista sui 21 chilometri, con 800 metri di camminata o di jogging per il recupero."))
add(M1,4,R,287,"Venerdi","Nuoto","Andatura di gara","1.600 metri",1600,"m",nuoto_gara("3 x 350 metri a nuoto alla velocita' prevista sui 2.000 metri, con 60 secondi di riposo.",None))
add(M1,4,R,288,"Sabato","Ciclismo","Endurance","67,2 chilometri",67.2,"km",bici_endurance("35,2",66,88,30))
add(M1,4,R,288,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",pesi_potenza("1 x 10 ripetizioni al 50% di 1 RM.","1 x 6 ripetizioni al 50% di 1 RM, esplosive."))
add(M1,4,R,288,"Domenica","Nuoto","Endurance","2.500 metri",2500,"m",nuoto_endurance(21,30,"1.500",600))
add(M1,4,R,288,"Domenica","Corsa a piedi","Endurance","13,6 chilometri",13.6,"km",corsa_endurance("6,4",32,40,"20 e mezzo"))

# =================== SETTIMANA 5 (pp. 289-291) ===================
add(M2,5,"",289,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(M2,5,"",289,"Martedi","Corsa a piedi","Velocita","20,8 chilometri",20.8,"km",corsa_velocita(4,45))
add(M2,5,"",289,"Martedi","Ciclismo","Velocita","88 chilometri",88,"km",bici_velocita(4,70))
add(M2,5,"",290,"Mercoledi","Nuoto","Velocita","3.400 metri",3400,"m",nuoto_velocita(4,1000))
add(M2,5,"",290,"Mercoledi","Pesi","Forza","-",None,"",pesi_forza("1 x 12 ripetizioni al 50% di 1 RM.","2 x da 6 a 8 ripetizioni all'85% di 1 RM."))
add(M2,5,"",290,"Giovedi","Ciclismo","Andatura di gara","88 chilometri",88,"km",bici_gara("4 x 4,8 chilometri in bicicletta alla velocita' prevista sui 20 chilometri, con 1 minuto per un giro in souplesse."))
add(M2,5,"",290,"Giovedi","Corsa a piedi","Andatura di gara","20,8 chilometri",20.8,"km",corsa_gara("6 x 800 metri di corsa alla velocita' prevista sui 5 chilometri, con 400 metri di camminata o di jogging per il recupero."))
add(M2,5,"",290,"Venerdi","Nuoto","Andatura di gara","3.400 metri",3400,"m",nuoto_gara("5 x 100 metri a nuoto alla velocita' prevista sui 500 metri, con 30 secondi di riposo.",1300))
add(M2,5,"",291,"Sabato","Ciclismo","Endurance","152 chilometri",152,"km",bici_endurance("83,2",156,208,70))
add(M2,5,"",291,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",pesi_potenza("1 x 20 ripetizioni al 50% di 1 RM.","2 x 6 ripetizioni al 50% di 1 RM, esplosive."))
add(M2,5,"",291,"Domenica","Nuoto","Endurance","5.000 metri",5000,"m",nuoto_endurance(42,60,"3.000",1300))
add(M2,5,"",291,"Domenica","Corsa a piedi","Endurance","30,4 chilometri",30.4,"km",corsa_endurance("19,2",96,120,45))

# =================== SETTIMANA 6 (pp. 292-294) ===================
add(M2,6,"",292,"Lunedi","Riposo","Nessun allenamento","-",None,"",["Nessun allenamento."])
add(M2,6,"",292,"Martedi","Corsa a piedi","Velocita","17,6 chilometri",17.6,"km",corsa_velocita(3,35))
add(M2,6,"",292,"Martedi","Ciclismo","Velocita","72 chilometri",72,"km",bici_velocita(3,60))
add(M2,6,"",293,"Mercoledi","Nuoto","Velocita","3.200 metri",3200,"m",nuoto_velocita(3,1200))
add(M2,6,"",293,"Mercoledi","Pesi","Forza","-",None,"",pesi_forza("1 x 12 ripetizioni al 50% di 1 RM.","2 x da 6 a 8 ripetizioni all'85% di 1 RM."))
add(M2,6,"",293,"Giovedi","Ciclismo","Andatura di gara","72 chilometri",72,"km",bici_gara("4 x 12,8 chilometri in bicicletta alla velocita' prevista sui 40 chilometri, con 5 minuti per un giro in souplesse."))
add(M2,6,"",293,"Giovedi","Corsa a piedi","Andatura di gara","17,6 chilometri",17.6,"km",corsa_gara("6 x 1.600 metri di corsa alla velocita' prevista sui 10 chilometri, con 400 metri di camminata o di jogging per il recupero."))
add(M2,6,"",293,"Venerdi","Nuoto","Andatura di gara","3.200 metri",3200,"m",nuoto_gara("5 x 300 metri a nuoto alla velocita' prevista sui 1.600 metri, con 30 secondi di riposo.",1200))
add(M2,6,"",294,"Sabato","Ciclismo","Endurance","112 chilometri",112,"km",bici_endurance("57,6",108,144,60))
add(M2,6,"",294,"Sabato","Pesi","Potenza ed endurance muscolare","-",None,"",pesi_potenza("1 x 20 ripetizioni al 50% di 1 RM.","2 x 6 ripetizioni al 50% di 1 RM, esplosive."))
add(M2,6,"",294,"Domenica","Nuoto","Endurance","4.500 metri",4500,"m",nuoto_endurance(35,50,"2.500",1200))
add(M2,6,"",294,"Domenica","Corsa a piedi","Endurance","22,4 chilometri",22.4,"km",corsa_endurance("14,4",72,90,45))
