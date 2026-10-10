# -*- coding: utf-8 -*-
# Mappatura zona -> obiettivo fisiologico. E' un'INTERPRETAZIONE sopra il libro:
# il libro dà solo l'andatura di riferimento, la lettura fisiologica è una proposta da validare.
TASSONOMIA = [
 # (obiettivo, rank intensita' (1 = piu' intenso), descrizione)
 ("Velocita' neuromuscolare", 1, "Sforzi brevissimi ad andatura molto superiore a quella di gara: reclutamento, meccanica, tolleranza alla velocita'."),
 ("Capacita' anaerobica",     2, "Ripetute brevi sopra soglia, con forte produzione di lattato: tolleranza e potenza lattacida."),
 ("VO2max",                   3, "Ripetute all'andatura dei 1.600 m / 5 km (nuoto 500 m, bici 3.200 m): massimo consumo di ossigeno."),
 ("Soglia anaerobica",        4, "Andatura dei 10 km (nuoto 1.600 m, bici 20 km): soglia, la zona che alza il tetto sostenibile."),
 ("Ritmo gara specifico",     5, "Andatura prevista sulla distanza di gara: adattamento specifico, pacing, alimentazione."),
 ("Forza specifica",          6, "Endurance sulla forza nel gesto: pendenza o giubbotto in corsa, 40-60 rpm in bici, palette in acqua."),
 ("Aerobico base",            7, "Lavoro aerobico di sostegno, compreso quello supplementare per raggiungere l'obiettivo di volume."),
 ("Aerobico lento (lungo)",   8, "Volume a bassa intensita' (RPE <12): base aerobica, efficienza, capillarizzazione."),
 ("Recupero attivo",          9, "Camminata, jogging, souplesse, nuoto blando fra le ripetute: dissipazione, nessuno stimolo."),
 ("Forza massimale",          6, "Sala pesi sulla forza: 85% di 1 RM."),
 ("Potenza ed endurance muscolare", 6, "Sala pesi su potenza e resistenza muscolare: carichi al 50% esplosivi, pliometria."),
]
RANK = {t[0]: t[1] for t in TASSONOMIA}

ZONA_OBIETTIVO = {
 "corsa_400m":"Velocita' neuromuscolare", "bici_800m":"Velocita' neuromuscolare", "nuoto_100m":"Velocita' neuromuscolare",
 "corsa_800m":"Capacita' anaerobica",     "bici_1600m":"Capacita' anaerobica",    "nuoto_200m":"Capacita' anaerobica",
 "corsa_1600m":"VO2max", "corsa_2000m":"VO2max", "corsa_5km":"VO2max", "bici_3200m":"VO2max", "nuoto_500m":"VO2max",
 "corsa_10km":"Soglia anaerobica", "bici_20km":"Soglia anaerobica", "nuoto_1600m":"Soglia anaerobica",
 "corsa_21km":"Ritmo gara specifico", "corsa_maratona":"Ritmo gara specifico",
 "bici_40km":"Ritmo gara specifico", "bici_90km":"Ritmo gara specifico", "bici_180km":"Ritmo gara specifico",
 "nuoto_2000m":"Ritmo gara specifico", "nuoto_3200m":"Ritmo gara specifico", "nuoto_4000m":"Ritmo gara specifico",
 "corsa_forza":"Forza specifica", "bici_forza":"Forza specifica", "nuoto_forza":"Forza specifica",
 "corsa_aerobica":"Aerobico base", "bici_aerobica":"Aerobico base", "nuoto_aerobico":"Aerobico base",
 "corsa_RPE_12_14":"Aerobico base", "bici_RPE_12_14":"Aerobico base", "nuoto_RPE_12_14":"Aerobico base",
 "corsa_RPE_sotto12":"Aerobico lento (lungo)", "bici_RPE_sotto12":"Aerobico lento (lungo)",
 "nuoto_RPE_sotto12":"Aerobico lento (lungo)",
 "corsa_recupero":"Recupero attivo", "bici_souplesse":"Recupero attivo",
 "nuoto_recupero":"Recupero attivo", "nuoto_blando":"Recupero attivo",
}
# obiettivi che NON caratterizzano una sessione (sono contorno)
CONTORNO = {"Recupero attivo", "Aerobico base"}
# le colonne della matrice allenamento x obiettivo
MATRICE = [t[0] for t in TASSONOMIA if t[0] not in ("Forza massimale","Potenza ed endurance muscolare")]
