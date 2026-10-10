# -*- coding: utf-8 -*-
"""Stima delle soglie dai tempi di gara, e derivazione delle 38 andature."""
# --- coefficienti: % della VELOCITA' di soglia (LT2) per ogni zona -----------
# corsa e nuoto: esponente di Riegel (v ~ D^-0.06) ancorato alla distanza di soglia
# ciclismo: curva potenza-durata, ancorata ai 40 km (~1 ora)
def riegel(d, d_rif, e=0.06):
    return (d / d_rif) ** (-e)

COEFF = {}
for z, d in (("corsa_400m",400),("corsa_800m",800),("corsa_1600m",1600),("corsa_2000m",2000),
             ("corsa_5km",5000),("corsa_10km",10000),("corsa_21km",21097),("corsa_maratona",42195)):
    COEFF[z] = riegel(d, 11873)          # 11.873 m = distanza percorsa in 60' (soglia)
COEFF.update({"corsa_aerobica":0.80,"corsa_forza":0.75,"corsa_recupero":0.60,
              "corsa_RPE_12_14":0.87,"corsa_RPE_sotto12":0.80})
for z, d in (("nuoto_100m",100),("nuoto_200m",200),("nuoto_500m",500),("nuoto_1600m",1600),
             ("nuoto_2000m",2000),("nuoto_3200m",3200),("nuoto_4000m",4000)):
    COEFF[z] = riegel(d, 1600)           # CSS ~ andatura sui 1.600 m
COEFF.update({"nuoto_blando":0.72,"nuoto_recupero":0.72,"nuoto_forza":0.82,
              "nuoto_aerobico":0.85,"nuoto_RPE_12_14":0.88,"nuoto_RPE_sotto12":0.80})
COEFF.update({"bici_800m":1.25,"bici_1600m":1.18,"bici_3200m":1.10,"bici_20km":1.04,
              "bici_40km":1.00,"bici_90km":0.92,"bici_180km":0.85,"bici_souplesse":0.65,
              "bici_forza":0.72,"bici_aerobica":0.80,"bici_RPE_12_14":0.85,"bici_RPE_sotto12":0.78})

# --- input di esempio: prestazioni di gara ----------------------------------
CORSA_D, CORSA_T = 10000, 50.0      # 10 km in 50'00"
NUOTO_400, NUOTO_200 = 440.0, 210.0 # secondi
BICI_D, BICI_T = 40.0, 67.0         # 40 km in 1h07'

# LT2 corsa: andatura sulla distanza coperta in 60 minuti (Riegel)
D60 = CORSA_D * (60.0 / CORSA_T) ** (1/1.06)
LT2_corsa = 60.0 / (D60/1000)
# LT2 nuoto: Critical Swim Speed
CSS = (400-200) / (NUOTO_400-NUOTO_200)          # m/s
LT2_nuoto = (100/CSS) / 60                        # min/100 m
# LT2 bici: andatura della prova di ~1 ora
LT2_bici = BICI_T / BICI_D
LT2 = {"corsa":LT2_corsa, "nuoto":LT2_nuoto, "bici":LT2_bici}
print("SOGLIE STIMATE (LT2)")
print(f"  corsa   10 km in {CORSA_T:.0f}' -> distanza in 60' = {D60:.0f} m -> LT2 = {LT2_corsa:.3f} min/km")
print(f"  nuoto   400 in {NUOTO_400:.0f}\" / 200 in {NUOTO_200:.0f}\" -> CSS = {CSS:.4f} m/s -> LT2 = {LT2_nuoto:.3f} min/100m")
print(f"  bici    40 km in {BICI_T:.0f}' -> LT2 = {LT2_bici:.3f} min/km ({60/LT2_bici:.1f} km/h)")
K_LT1 = 0.85
print(f"\n  LT1 = {K_LT1:.0%} della velocita' di soglia -> corsa {LT2_corsa/K_LT1:.2f} | nuoto {LT2_nuoto/K_LT1:.2f} | bici {LT2_bici/K_LT1:.2f}")

PASSI = {}
for z, c in COEFF.items():
    d = "corsa" if z.startswith("corsa") else ("nuoto" if z.startswith("nuoto") else "bici")
    PASSI[z] = round(LT2[d] / c, 3)
print("\nANDATURE DERIVATE (estratto)")
for z in ("corsa_400m","corsa_5km","corsa_10km","corsa_21km","corsa_recupero",
          "nuoto_200m","nuoto_1600m","nuoto_3200m","bici_20km","bici_40km","bici_180km","bici_souplesse"):
    print(f"  {z:20s} coeff {COEFF[z]:.3f}  ->  {PASSI[z]:6.2f}")

# --- effetto sul modello a tre domini ---------------------------------------
from openpyxl import load_workbook
from collections import defaultdict
wb = load_workbook('/mnt/user-data/outputs/Piani_Triathlon_Sprint_Olimpico_Half-Ironman_Ironman.xlsx', data_only=True)
SA = list(wb['Struttura Allenamento'].iter_rows(min_row=2, values_only=True))
SOG = {"Corsa a piedi":"corsa_10km","Ciclismo":"bici_40km","Nuoto":"nuoto_1600m"}
PIANI = ("Triathlon Sprint","Triathlon Olimpico","Half-Ironman","Ironman")
d = defaultdict(lambda: defaultdict(float))
for r in SA:
    disc, zona, tempo = r[8], r[19], r[23]
    if disc not in SOG or not zona or zona not in PASSI or not tempo: continue
    IF = PASSI[SOG[disc]] / PASSI[zona]
    k = 'LOW' if IF < K_LT1 else ('MOD' if IF < 1.0 else 'HIGH')
    d[r[1]][k] += tempo
print("\nTRE DOMINI con le soglie STIMATE dai tempi di gara")
print(f"{'piano':22s} {'LOW':>8s} {'MOD':>8s} {'HIGH':>8s}")
for p in PIANI:
    t = sum(d[p].values())
    print(f"  {p:20s} " + " ".join(f"{d[p][k]/t*100:7.1f}%" for k in ('LOW','MOD','HIGH')))
import json; json.dump({"COEFF":COEFF,"PASSI":PASSI,"LT2":LT2}, open('soglie.json','w'))
