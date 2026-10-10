# -*- coding: utf-8 -*-
import sys
sys.path.insert(0,'/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad')
exec(open('/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad/build9_base.py').read())
import importlib, parser as P, obiettivi as OB
importlib.reload(P); importlib.reload(OB)
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule

import json as _js
COEF = _js.load(open('/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad/soglie.json'))['COEFF']
_PD = _js.load(open('/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad/soglie.json'))['PASSI']
GIALLO = PatternFill("solid", fgColor="FFF2CC")
BLU    = Font(name=FONT, size=10, color="0000FF")
ALTA   = PatternFill("solid", fgColor="F7F7F7")


# ==========================================================================
# FOGLIO "Stima Soglie"  (layout ANCORATO)
# ==========================================================================
ws_s = wb.create_sheet("Stima Soglie")
ws_s["A1"] = "Stima delle soglie dai tempi di gara"; ws_s["A1"].font = TITLE
ws_s["A2"] = fix("Questo e' il punto di ingresso di tutto il modello. Inserisci nelle celle gialle le tue "
                 "prestazioni di riferimento: da qui si stimano LT2 e LT1 per ciascuna disciplina, e da quelle "
                 "si derivano per formula tutte e 38 le andature di 'Parametri Atleta'. Sono STIME, non test di "
                 "laboratorio: vanno sostituite appena avrai misure dirette.")
ws_s["A2"].font = Font(name=FONT, size=9, italic=True, color="C00000")

ws_s["A5"] = "1. Corsa a piedi - da una prestazione di gara recente"; ws_s["A5"].font = BOLD
for rr, lab, val in ((6,"Distanza della prova (metri)",10000),(7,"Tempo impiegato (minuti)",50.0)):
    ws_s.cell(row=rr, column=1, value=fix(lab)).font = BODY
    c = ws_s.cell(row=rr, column=2, value=val); c.font = BLU; c.fill = GIALLO; c.border = BRD
ws_s["A8"] = fix("Distanza coperta in 60 minuti (Riegel)"); ws_s["A8"].font = BODY
ws_s["B8"] = "=$B$6*(60/$B$7)^(1/$B$27)"; ws_s["B8"].number_format = '#,##0'
ws_s["A9"] = fix("LT2 corsa (min/km)"); ws_s["A9"].font = BOLD
ws_s["B9"] = "=60/($B$8/1000)"; ws_s["B9"].number_format = '0.000'; ws_s["B9"].font = BOLD
ws_s["C9"] = fix("cioe' l'andatura sostenibile per circa un'ora")
ws_s["C9"].font = Font(name=FONT, size=9, italic=True, color="666666")

ws_s["A11"] = "2. Nuoto - Critical Swim Speed da 400 m e 200 m"; ws_s["A11"].font = BOLD
for rr, lab, val in ((12,"Tempo sui 400 m (secondi)",440.0),(13,"Tempo sui 200 m (secondi)",210.0)):
    ws_s.cell(row=rr, column=1, value=fix(lab)).font = BODY
    c = ws_s.cell(row=rr, column=2, value=val); c.font = BLU; c.fill = GIALLO; c.border = BRD
ws_s["A14"] = fix("CSS (metri al secondo)"); ws_s["A14"].font = BODY
ws_s["B14"] = "=IF($B$12<=$B$13,\"\",(400-200)/($B$12-$B$13))"; ws_s["B14"].number_format = '0.0000'
ws_s["A15"] = fix("LT2 nuoto (min/100 m)"); ws_s["A15"].font = BOLD
ws_s["B15"] = "=IF($B$14=\"\",\"\",(100/$B$14)/60)"; ws_s["B15"].number_format = '0.000'; ws_s["B15"].font = BOLD
ws_s["C15"] = fix("La CSS e' il proxy standard della soglia in acqua")
ws_s["C15"].font = Font(name=FONT, size=9, italic=True, color="666666")

ws_s["A17"] = "3. Ciclismo - da una prova di circa un'ora"; ws_s["A17"].font = BOLD
for rr, lab, val in ((18,"Distanza della prova (km)",40.0),(19,"Tempo impiegato (minuti)",67.0)):
    ws_s.cell(row=rr, column=1, value=fix(lab)).font = BODY
    c = ws_s.cell(row=rr, column=2, value=val); c.font = BLU; c.fill = GIALLO; c.border = BRD
ws_s["A20"] = fix("LT2 ciclismo (min/km)"); ws_s["A20"].font = BOLD
ws_s["B20"] = "=$B$19/$B$18"; ws_s["B20"].number_format = '0.000'; ws_s["B20"].font = BOLD
ws_s["A21"] = fix("Velocita' di soglia (km/h)"); ws_s["A21"].font = BODY
ws_s["B21"] = "=IF($B$20=\"\",\"\",60/$B$20)"; ws_s["B21"].number_format = '0.0'

ws_s["A24"] = "4. Parametri del modello"; ws_s["A24"].font = BOLD
ws_s["A26"] = fix("LT1 come quota della velocita' di soglia"); ws_s["A26"].font = BODY
c = ws_s["B26"]; c.value = 0.85; c.font = BLU; c.fill = GIALLO; c.border = BRD; c.number_format = '0%'
ws_s["C26"] = fix("Confine fra dominio LOW e MODERATE. Valore tipico 0,80-0,88.")
ws_s["C26"].font = Font(name=FONT, size=9, italic=True, color="666666")
ws_s["A27"] = fix("Esponente di Riegel"); ws_s["A27"].font = BODY
c = ws_s["B27"]; c.value = 1.06; c.font = BLU; c.fill = GIALLO; c.border = BRD; c.number_format = '0.00'
ws_s["C27"] = fix("1,06 e' il valore classico. Piu' alto = decadimento piu' rapido sulle lunghe distanze.")
ws_s["C27"].font = Font(name=FONT, size=9, italic=True, color="666666")

ws_s["A30"] = "5. Soglie risultanti - e' qui che pescano gli altri fogli"; ws_s["A30"].font = BOLD
header(ws_s, 31, ["Disciplina","LT2","LT1","Unita'","Dominio LOW","Dominio MODERATE","Dominio HIGH"], "404040")
for k, (nome, cella, un) in enumerate((("Corsa a piedi","$B$9","min/km"),
                                       ("Ciclismo","$B$20","min/km"),
                                       ("Nuoto","$B$15","min/100m"))):
    rr = 32+k
    ws_s.cell(row=rr, column=1, value=nome).font = BODY
    ws_s.cell(row=rr, column=2, value=f"={cella}").number_format = '0.000'
    ws_s.cell(row=rr, column=3, value=f"=IF({cella}=\"\",\"\",{cella}/$B$26)").number_format = '0.000'
    ws_s.cell(row=rr, column=4, value=un)
    ws_s.cell(row=rr, column=5, value=f"=IF($C{rr}=\"\",\"\",\"piu' lento di \"&TEXT($C{rr},\"0.00\"))")
    ws_s.cell(row=rr, column=6, value=f"=IF($B{rr}=\"\",\"\",TEXT($B{rr},\"0.00\")&\" - \"&TEXT($C{rr},\"0.00\"))")
    ws_s.cell(row=rr, column=7, value=f"=IF($B{rr}=\"\",\"\",\"piu' veloce di \"&TEXT($B{rr},\"0.00\"))")
    for j in range(1, 8):
        ws_s.cell(row=rr, column=j).font = BODY; ws_s.cell(row=rr, column=j).border = BRD
        ws_s.cell(row=rr, column=j).alignment = Alignment(horizontal="center" if j > 1 else "left")
for i_, w in enumerate([44,14,14,12,22,22,22], 1):
    ws_s.column_dimensions[get_column_letter(i_)].width = w
STIMA_LT2 = "'Stima Soglie'!$B$32:$B$34"; STIMA_DISC = "'Stima Soglie'!$A$32:$A$34"

# ============================ Parametri Atleta ============================
ZONE = [
 ("corsa_400m","Corsa a piedi","Passo gara sui 400 m",4.00,"min/km"),
 ("corsa_800m","Corsa a piedi","Passo gara sugli 800 m",4.25,"min/km"),
 ("corsa_1600m","Corsa a piedi","Passo gara sui 1.600 m",4.50,"min/km"),
 ("corsa_2000m","Corsa a piedi","Passo gara sui 2.000 m",4.60,"min/km"),
 ("corsa_5km","Corsa a piedi","Passo gara sui 5 km",4.83,"min/km"),
 ("corsa_10km","Corsa a piedi","Passo gara sui 10 km",5.08,"min/km"),
 ("corsa_21km","Corsa a piedi","Passo gara mezza maratona (21 km)",5.42,"min/km"),
 ("corsa_maratona","Corsa a piedi","Passo gara maratona",5.75,"min/km"),
 ("corsa_aerobica","Corsa a piedi","Passo aerobico (lavoro supplementare)",6.25,"min/km"),
 ("corsa_forza","Corsa a piedi","Endurance sulla forza (pendenza 2-4% o giubbotto)",6.75,"min/km"),
 ("corsa_recupero","Corsa a piedi","Camminata / jogging di recupero",8.50,"min/km"),
 ("corsa_RPE_12_14","Corsa a piedi","Fase di base - distanza intermedia (RPE 12-14)",5.75,"min/km"),
 ("corsa_RPE_sotto12","Corsa a piedi","Fase di base - distanza lunga (RPE <12)",6.25,"min/km"),
 ("nuoto_100m","Nuoto","Passo gara sui 100 m",1.50,"min/100m"),
 ("nuoto_200m","Nuoto","Passo gara sui 200 m",1.58,"min/100m"),
 ("nuoto_500m","Nuoto","Passo gara sui 500 m",1.75,"min/100m"),
 ("nuoto_1600m","Nuoto","Passo gara sui 1.600 m",1.92,"min/100m"),
 ("nuoto_2000m","Nuoto","Passo gara sui 2.000 m",1.95,"min/100m"),
 ("nuoto_3200m","Nuoto","Passo gara sui 3.200 m",2.00,"min/100m"),
 ("nuoto_4000m","Nuoto","Passo gara sui 4.000 m",2.05,"min/100m"),
 ("nuoto_blando","Nuoto","Nuoto a ritmo blando",2.33,"min/100m"),
 ("nuoto_recupero","Nuoto","Recupero fra le ripetute",2.33,"min/100m"),
 ("nuoto_forza","Nuoto","Endurance sulla forza con le palette",2.17,"min/100m"),
 ("nuoto_aerobico","Nuoto","Nuoto aerobico (lavoro supplementare)",2.17,"min/100m"),
 ("nuoto_RPE_12_14","Nuoto","Fase di base - distanza intermedia (RPE 12-14)",2.10,"min/100m"),
 ("nuoto_RPE_sotto12","Nuoto","Fase di base - distanza lunga (RPE <12)",2.25,"min/100m"),
 ("bici_800m","Ciclismo","Passo/potenza gara sugli 800 m",1.33,"min/km"),
 ("bici_1600m","Ciclismo","Passo gara sui 1.600 m",1.40,"min/km"),
 ("bici_3200m","Ciclismo","Passo gara sui 3.200 m",1.46,"min/km"),
 ("bici_20km","Ciclismo","Passo gara sui 20 km",1.58,"min/km"),
 ("bici_40km","Ciclismo","Passo gara sui 40 km",1.67,"min/km"),
 ("bici_90km","Ciclismo","Passo gara sui 90 km",1.82,"min/km"),
 ("bici_180km","Ciclismo","Passo gara sui 180 km",2.00,"min/km"),
 ("bici_souplesse","Ciclismo","Giro di recupero in souplesse",2.40,"min/km"),
 ("bici_forza","Ciclismo","Endurance sulla forza (40-60 rpm)",2.31,"min/km"),
 ("bici_aerobica","Ciclismo","Ciclismo aerobico (lavoro supplementare)",2.22,"min/km"),
 ("bici_RPE_12_14","Ciclismo","Fase di base - distanza intermedia (RPE 12-14)",2.10,"min/km"),
 ("bici_RPE_sotto12","Ciclismo","Fase di base - distanza lunga (RPE <12)",2.31,"min/km"),
]
ZONE_SET = {z[0] for z in ZONE}
wp = wb.create_sheet("Parametri Atleta")
wp["A1"] = "Parametri atleta - passi di riferimento"; wp["A1"].font = TITLE
wp["A2"] = ("MODIFICA SOLO LE CELLE GIALLE della colonna D. Il passo va espresso in MINUTI DECIMALI "
            "(4,50 = 4'30\"). Corsa e ciclismo in min/km, nuoto in min/100 m. Anche la colonna D e' un input: "
            "l'obiettivo fisiologico di ogni zona e' una PROPOSTA, cambiala se non ti convince. Tutto il foglio "
            "'Struttura Allenamento' e il foglio 'Controllo Sessioni' si ricalcolano da qui.")
wp["A2"].font = Font(name=FONT, size=9, italic=True, color="666666")
wp["A3"] = ("I valori qui sotto sono SOLO UN ESEMPIO di partenza (atleta amatore): sostituiscili con i tuoi. "
            "I nomi delle zone derivano dalle andature di riferimento citate dal libro nelle descrizioni delle serie.")
wp["A3"].font = Font(name=FONT, size=9, italic=True, color="C00000")
header(wp, 5, ["Zona","Disciplina","Descrizione","Obiettivo fisiologico","% velocita' LT2","Passo","Unita' passo","Velocita' (km/h)","Passo (mm:ss)","Dominio"], "404040")
r = 6
for z, d, desc, passo, un in ZONE:
    wp.cell(row=r, column=1, value=z).font = BOLD
    wp.cell(row=r, column=2, value=d).font = BODY
    wp.cell(row=r, column=3, value=fix(desc)).font = BODY
    c = wp.cell(row=r, column=4, value=OB.ZONA_OBIETTIVO.get(z, "")); c.font = BLU; c.fill = GIALLO
    c = wp.cell(row=r, column=5, value=round(COEF.get(z, 1.0), 4)); c.font = BLU; c.fill = GIALLO; c.number_format = '0.0%'
    wp.cell(row=r, column=6, value=f'=IFERROR(INDEX({STIMA_LT2},MATCH($B{r},{STIMA_DISC},0))/$E{r},"")').number_format = '0.00'
    wp.cell(row=r, column=6).font = BOLD
    wp.cell(row=r, column=7, value=un).font = BODY
    wp.cell(row=r, column=8, value=(f'=IF($F{r}="","",60/$F{r})' if un == "min/km" else "-")).font = BODY
    wp.cell(row=r, column=8).number_format = '0.0'
    wp.cell(row=r, column=9, value=f'=IF($F{r}="","",TEXT($F{r}/1440,"mm:ss"))').font = BODY
    wp.cell(row=r, column=10, value=f'=IF($E{r}<\'Stima Soglie\'!$B$26,"LOW",IF($E{r}<1,"MODERATE","HIGH"))').font = BODY
    for j in range(1, 11):
        wp.cell(row=r, column=j).border = BRD
        wp.cell(row=r, column=j).alignment = Alignment(vertical="center",
            horizontal="left" if j in (1,2,3,4,7) else "center")
    r += 1
ZFIRST, ZLAST = 6, r-1
for i_, w in enumerate([22,16,46,30,15,10,14,16,14,13], 1):
    wp.column_dimensions[get_column_letter(i_)].width = w
wp.freeze_panes = "A6"

# ============================ Struttura Allenamento ============================
righe, non_parsati = P.analizza()
import re as _re
from collections import defaultdict as _dd, Counter as _C
_str = {}; _disc = {}
for _b in righe:
    _str[_b["sid"]] = _b["struttura"]; _disc[_b["sid"]] = _b["sess"]["disc"]
_fam = _dd(list)
for _sid, _st in _str.items():
    _fam[(_disc[_sid], _re.sub(r'[0-9]+', '#', _st))].append(_sid)
_PRE = {"Corsa a piedi":"RUN", "Ciclismo":"BIKE", "Nuoto":"SWIM", "Pesi":"GYM", "Riposo":"REST"}
ARCHET = {}; ARCH_INFO = {}
_cnt = _dd(int)
for (_d, _f), _sids in sorted(_fam.items(), key=lambda x: (x[0][0], -len(x[1]))):
    _cnt[_d] += 1
    _code = f"{_PRE.get(_d,'ALT')}-{_cnt[_d]:02d}"
    for _s in _sids: ARCHET[_s] = _code
    ARCH_INFO[_code] = dict(disc=_d, forma=_f, sids=_sids)
assert not non_parsati, f"{len(non_parsati)} testi non parsati"

COLS = ["ID sessione","Piano","Fase","Mesociclo","Settimana","Nota settimana","Pagina","Giorno",
        "Disciplina","Focus sessione","Obiettivo sessione (m)","Serie (libro)","Blocco","Tipo",
        "Ripetizioni","Distanza per rip. (m)","Durata per rip. da (min)","Durata per rip. a (min)",
        "Modo","Zona","Unita' passo","Passo","Distanza totale (m)","Tempo totale (min)",
        "Nel totale sessione","Set (pesi)","Rip. (pesi)","% 1RM","Archetipo","Obiettivo fisiologico",
        "Zona FC","% FC riserva","Peso Edwards","Coeff. disciplina","Punti Edwards","Punti Banister",
        "Punti andatura (rTSS)","Struttura sessione","Note","Testo originale"]
LARG = [11,16,7,30,10,18,8,11,15,22,14,14,8,26,11,13,13,13,16,20,12,9,14,14,12,9,11,9,13,30,
        10,13,14,15,14,14,20,60,34,100]
NC = len(COLS)
ws = wb.create_sheet("Struttura Allenamento")
header(ws, 1, COLS, "404040")
N = len(righe) + 1
PAR = "'Parametri Atleta'"
prima = {}
for k, b in enumerate(righe, start=2):
    prima.setdefault(b["sid"], k)

for k, b in enumerate(righe, start=2):
    s = b["sess"]; disc = s["disc"]
    fatt = 100 if disc == "Nuoto" else 1000
    zn = b["zona"] or ""
    tipo = b["tipo"].replace("Velocita'", "Velocità")
    vals = [b["sid"], s["piano"], s.get("fase","Gara"), fix(s["meso"]), s["sett"], fix(s["nota"]),
            s["pag"], fix(s["giorno"]), disc, fix(s["focus"]), b["ob_m"], b["serie_libro"],
            b["blocco"], tipo, b["rip"], b["dist"], b["dur_a"], b["dur_b"], b["modo"], zn]
    for j, v in enumerate(vals, 1):
        ws.cell(row=k, column=j, value=v)
    if zn in ZONE_SET:
        ws.cell(row=k, column=21, value=f'=IFERROR(INDEX({PAR}!$G${ZFIRST}:$G${ZLAST},MATCH($T{k},{PAR}!$A${ZFIRST}:$A${ZLAST},0)),"")')
        c = ws.cell(row=k, column=22, value=f'=IFERROR(INDEX({PAR}!$F${ZFIRST}:$F${ZLAST},MATCH($T{k},{PAR}!$A${ZFIRST}:$A${ZLAST},0)),"")')
        c.number_format = '0.00'
    W = X = None
    if b["modo"] == "residuo":
        f0 = prima[b["sid"]]
        W = (f'=MAX(0,$K{k}-SUMIFS($W${f0}:$W${k-1},$Y${f0}:$Y${k-1},"Si"))' if k-1 >= f0 else f'=$K{k}')
        X = f'=IF(OR($W{k}="",$V{k}=""),"",$W{k}/{fatt}*$V{k})'
    elif b["modo"] == "riposo uguale":
        X = f'=IF($X{k-1}="","",$X{k-1})'
    elif b["dist"] is not None:
        W = f'=$O{k}*$P{k}'
        X = (f'=$O{k}*AVERAGE($Q{k}:$R{k})' if b["dur_a"] is not None
             else f'=IF($V{k}="","",$W{k}/{fatt}*$V{k})')
    elif b["dur_a"] is not None:
        W = f'=IF($V{k}="","",$O{k}*AVERAGE($Q{k}:$R{k})/$V{k}*{fatt})'
        X = f'=$O{k}*AVERAGE($Q{k}:$R{k})'
    if W: ws.cell(row=k, column=23, value=W).number_format = '#,##0'
    if X: ws.cell(row=k, column=24, value=X).number_format = '0.0'
    ws.cell(row=k, column=25, value=("Si" if b.get("nel_totale", True) else "No") if W else "")
    ws.cell(row=k, column=26, value=b["setp"])
    ws.cell(row=k, column=27, value=b["ripp"])
    ws.cell(row=k, column=28, value=b["rm"])
    ws.cell(row=k, column=29, value=ARCHET.get(b["sid"], ""))
    if zn in ZONE_SET:
        ws.cell(row=k, column=30, value=f'=IFERROR(INDEX({PAR}!$D${ZFIRST}:$D${ZLAST},MATCH($T{k},{PAR}!$A${ZFIRST}:$A${ZLAST},0)),"")')
    elif b["tipo"].startswith("Pesi - forza"):
        ws.cell(row=k, column=30, value="Forza massimale")
    elif b["tipo"].startswith("Pesi - potenza"):
        ws.cell(row=k, column=30, value="Potenza ed endurance muscolare")
    ZC = "'Zone e Carico'"
    _pesi_first = (disc == "Pesi" and b["blocco"] == 1)
    if _pesi_first:   # il libro non da' la durata: usa il parametro editabile
        ws.cell(row=k, column=24, value=f"={ZC}!$B$40").number_format = '0.0'
    _ha_ob = (zn in ZONE_SET) or disc == "Pesi"
    if _ha_ob:
        ws.cell(row=k, column=31, value=f'=IFERROR(INDEX({ZC}!$B$22:$B$32,MATCH($AD{k},{ZC}!$A$22:$A$32,0)),"")')
        ws.cell(row=k, column=32, value=f'=IFERROR(INDEX({ZC}!$D$6:$D$10,MATCH($AE{k},{ZC}!$A$6:$A$10,0)),"")').number_format = '0%'
        ws.cell(row=k, column=33, value=f'=IFERROR(INDEX({ZC}!$E$6:$E$10,MATCH($AE{k},{ZC}!$A$6:$A$10,0)),"")')
        ws.cell(row=k, column=34, value=f'=IFERROR(INDEX({ZC}!$B$35:$B$38,MATCH($I{k},{ZC}!$A$35:$A$38,0)),1)').number_format = '0.00'
        ws.cell(row=k, column=35, value=f'=IF(OR($X{k}="",$AG{k}=""),"",$X{k}*$AG{k}*$AH{k})').number_format = '0.0'
        ws.cell(row=k, column=36, value=f'=IF(OR($X{k}="",$AF{k}=""),"",$X{k}*$AF{k}*0.64*EXP({ZC}!$B$41*$AF{k})*$AH{k})').number_format = '0.0'
    if zn in ZONE_SET and not _pesi_first:
        ws.cell(row=k, column=37, value=(
            f'=IF(OR($X{k}="",$V{k}="",$V{k}=0),"",'
            f'$X{k}/60*(IFERROR(INDEX({ZC}!$C$35:$C$38,MATCH($I{k},{ZC}!$A$35:$A$38,0)),"")/$V{k})^2*100)')).number_format = '0.0'
    ws.cell(row=k, column=38, value=b["struttura"])
    ws.cell(row=k, column=39, value=fix(b["nota"]) if b["nota"] else None)
    ws.cell(row=k, column=40, value=fix(b["testo"]))
    for j in range(1, NC+1):
        c = ws.cell(row=k, column=j)
        c.font = BODY; c.border = BRD
        c.alignment = Alignment(vertical="top", wrap_text=(j in (38,39,40)))
        if j in (1,5,7,11,13,15,16,17,18,23,24,25,26,27,28,31,32,33,34,35,36,37):
            c.alignment = Alignment(horizontal="center", vertical="top")
        if k % 2 == 0: c.fill = ALTA
    for j in (17,18):
        ws.cell(row=k, column=j).number_format = '0.00'
for i_, w in enumerate(LARG, 1):
    ws.column_dimensions[get_column_letter(i_)].width = w
ws.freeze_panes = "O2"
ws.auto_filter.ref = f"A1:{get_column_letter(NC)}{N}"

# ============================ Controllo Sessioni ============================
sessioni = []
for b in righe:
    if not sessioni or sessioni[-1]["sid"] != b["sid"]:
        sessioni.append(dict(sid=b["sid"], sess=b["sess"], ob=b["ob_m"]))
wc = wb.create_sheet("Controllo Sessioni")
wc["A1"] = "Controllo di quadratura: blocchi prescritti vs obiettivo di sessione"; wc["A1"].font = TITLE
wc["A2"] = ("Somma delle distanze dei blocchi contrassegnati 'Si' in 'Nel totale sessione' contro l'obiettivo "
            "dichiarato dal libro. I recuperi espressi a tempo vengono convertiti in distanza usando i passi "
            "di 'Parametri Atleta': cambiando i passi, alcune quadrature possono spostarsi.")
wc["A2"].font = Font(name=FONT, size=9, italic=True, color="666666")
header(wc, 4, ["ID sessione","Piano","Fase","Settimana","Pagina","Giorno","Disciplina","Focus",
               "Obiettivo (m)","Somma blocchi (m)","di cui supplementare (m)","Scarto (m)",
               "Tempo totale (min)","Esito"], "404040")
SA = "'Struttura Allenamento'"
r = 5
for d in sessioni:
    s = d["sess"]
    for j, v in enumerate([d["sid"], s["piano"], s.get("fase","Gara"), s["sett"], s["pag"],
                           fix(s["giorno"]), s["disc"], fix(s["focus"]), d["ob"]], 1):
        wc.cell(row=r, column=j, value=v)
    wc.cell(row=r, column=10, value=f'=SUMIFS({SA}!$W$2:$W${N},{SA}!$A$2:$A${N},$A{r},{SA}!$Y$2:$Y${N},"Si")')
    wc.cell(row=r, column=11, value=f'=SUMIFS({SA}!$W$2:$W${N},{SA}!$A$2:$A${N},$A{r},{SA}!$N$2:$N${N},"Aerobico supplementare")')
    wc.cell(row=r, column=12, value=f'=IF($I{r}="","",$J{r}-$I{r})')
    wc.cell(row=r, column=13, value=f'=SUMIFS({SA}!$X$2:$X${N},{SA}!$A$2:$A${N},$A{r})')
    wc.cell(row=r, column=14, value=(
        f'=IF($I{r}="","n.d.",'
        f'IF(COUNTIFS({SA}!$A$2:$A${N},$A{r},{SA}!$S$2:$S${N},"descrittivo")>0,"Tapering - non quantificato",'
        f'IF(ABS($L{r})<=1,"OK",IF($L{r}>0,"Blocchi oltre obiettivo","Residuo non assegnato"))))'))
    for j in range(1, 15):
        c = wc.cell(row=r, column=j)
        c.font = BODY; c.border = BRD
        c.alignment = Alignment(horizontal="center" if j not in (2,6,7,8,14) else "left", vertical="center")
        if j in (9,10,11,12): c.number_format = '#,##0'
        if j == 13: c.number_format = '0.0'
    r += 1
CLAST = r-1
for i_, w in enumerate([11,18,7,10,8,11,15,22,14,18,24,12,17,26], 1):
    wc.column_dimensions[get_column_letter(i_)].width = w
wc.freeze_panes = "A5"; wc.auto_filter.ref = f"A4:N{CLAST}"
wc.conditional_formatting.add(f"N5:N{CLAST}", CellIsRule(operator="equal", formula=['"OK"'],
    fill=PatternFill("solid", fgColor="C6EFCE")))
wc.conditional_formatting.add(f"N5:N{CLAST}", CellIsRule(operator="equal", formula=['"Blocchi oltre obiettivo"'],
    fill=PatternFill("solid", fgColor="FFC7CE")))
wc.conditional_formatting.add(f"N5:N{CLAST}", CellIsRule(operator="equal", formula=['"Tapering - non quantificato"'],
    fill=PatternFill("solid", fgColor="FFF2CC")))

# ============================ Legenda ============================
wl = wb["Legenda"]; r = wl.max_row + 2
for kk, vv in [
 ("--- VARIAZIONI ---", ""),
 ("Foglio 'Variazioni Allenamenti'", "18.249 righe: i 237 allenamenti base quantificabili del catalogo, scalati in distanza (11 livelli: da -50% a +50% a passi del 10%) e in passo (7 livelli: da -30% a +30%). 11 x 7 = 77 combinazioni per allenamento. La colonna 'Una variabile sola' isola le 4.029 righe in cui varia solo la distanza oppure solo il passo."),
 ("Perche' il passo si ferma a +-30%", "Oltre quella soglia si generano andature non praticabili: a -50% un fondo a 5'45\"/km diventerebbe un 2'53\"/km. Il cap e' una scelta esplicita, non un limite tecnico."),
 ("Una variazione e' un ALTRO allenamento", "Cambiare il passo sposta il rapporto con l'andatura di soglia, quindi sposta la zona, quindi cambia l'obiettivo fisiologico. La colonna 'Cambio obiettivo' segnala le righe in cui succede: sono 15.642 su 18.249. Non sono 'lo stesso allenamento piu' facile': sono allenamenti nuovi, con finalita' diversa."),
 ("Come si scala", "Nelle ripetute si scala la distanza della singola ripetuta e si tiene il numero (5 x 1000m a -20% = 5 x 800m), cosi' la struttura resta riconoscibile e il rapporto lavoro/recupero non cambia. I blocchi definiti a tempo scalano nella durata. Il blocco aerobico supplementare si ricalcola come obiettivo scalato meno tutto il resto."),
 ("Colonne 'Gruppo equivalenza' e 'Ridondante'", "Molte variazioni di allenamenti diversi finiscono per coincidere: stessa disciplina, stessa zona, distanza entro 200 m e tempo entro 2 minuti. La prima di ogni gruppo resta, le altre sono marcate Ridondante = Si. Filtrando su No si ottiene l'insieme degli allenamenti realmente distinti."),
 ("Colonna 'Cambio obiettivo'", "Confronta la zona risultante con quella dell'originale dello STESSO allenamento, non con l'etichetta del catalogo: il confronto e' cosi' metodologicamente omogeneo. Variare la sola distanza non cambia quasi mai l'obiettivo, perche' l'obiettivo dipende dal passo; a cambiarlo e' la variazione di velocita'."),
 ("Colonna 'Plausibile'", "No quando almeno un blocco finisce fuori da una banda di passo praticabile per quella disciplina, o quando la seduta supera le 8 ore. Sono 739 righe su 18.249 (4%). Le righe restano nella tabella: filtra tu o lascia filtrare all'algoritmo."),
 ("Cosa e' formula e cosa e' valore", "Punti Edwards e Banister sono formule vive: dipendono dai pesi delle zone, dai coefficienti di disciplina e dal k di Banister, quindi si aggiornano se li cambi. I minuti per zona e i punti andatura sono invece VALORI, calcolati sui passi attuali di 'Parametri Atleta': se modifichi sensibilmente quei passi vanno rigenerati."),
 ("", ""),
 ("--- CARICO E OBIETTIVI DI GARA ---", ""),
 ("Foglio 'Zone e Carico'", "Il modello di carico, tutto in celle gialle modificabili: le 5 zone di FC in % della FC di riserva (Karvonen) con il loro peso, la mappatura obiettivo fisiologico -> zona, i parametri per disciplina (FC max, FC a riposo, coefficiente, passo di soglia) e i due parametri residui (durata di una seduta in sala, k di Banister)."),
 ("AVVERTENZA sulle frequenze cardiache", "Il libro non da' MAI frequenze cardiache: da' andature e RPE. Le zone di FC sono dedotte dall'obiettivo fisiologico, che a sua volta e' dedotto dall'andatura di riferimento. Il punteggio misura quindi lo SFORZO PREVISTO DAL LIBRO, non lo sforzo reale dell'atleta. Diventera' misura vera quando ci si agganceranno i dati dell'orologio."),
 ("Tre punteggi affiancati", "Punti Edwards = minuti x peso della zona x coefficiente di disciplina (lineare, leggibile). Punti Banister = minuti x %FCris x 0,64 x e^(k x %FCris) x coefficiente (esponenziale, penalizza l'alta intensita'). Punti andatura = (minuti/60) x (passo di soglia / passo del blocco)^2 x 100, logica TSS: non usa la FC, quindi non soffre del ritardo cardiaco sugli sforzi brevi e non ha bisogno di coefficienti di disciplina."),
 ("Coefficiente di disciplina", "A parita' di sforzo la FC e' piu' bassa in bici (circa 5-8 battiti) e in acqua (10-15): senza correzione il nuoto risulterebbe sistematicamente piu' leggero di quello che e'. Valori di partenza: corsa 1,00 / bici 0,95 / nuoto 0,90."),
 ("Sedute con i pesi", "Il libro non indica quanto durano. Senza un valore, 88 sessioni peserebbero zero nei totali: si usa il parametro 'Durata stimata di una seduta con i pesi' (45 minuti di default) in 'Zone e Carico'."),
 ("Foglio 'Obiettivi di Carico'", "Il carico aggregato su tre livelli: per settimana (44 righe), per mesociclo e per piano. Per ciascuno: ore, i tre punteggi e la ripartizione delle ore fra nuoto, bici, corsa e pesi."),
 ("Che cosa significa 'obiettivo'", "Il piano del libro E' l'obiettivo: la somma delle sue sedute e' il carico che quel libro ritiene necessario per completare la distanza. E' un riferimento DESCRITTIVO - cosa prescrive questo libro - non una soglia fisiologica validata."),
 ("", ""),
 ("--- CATALOGO E OBIETTIVI ---", ""),
 ("Due tassonomie affiancate", "Obiettivo LIBRO = l'etichetta che il libro stesso da' alla seduta (Velocita', Andatura di gara, Endurance, Distanza intermedia, Distanza lunga, Forza, Potenza): e' un dato trascritto, non un'interpretazione. Obiettivo FISIOLOGICO = una lettura proposta sopra l'andatura di riferimento di ogni zona: va validata e si modifica dalla colonna D di 'Parametri Atleta'."),
 ("Foglio 'Tassonomia Obiettivi'", "I 11 obiettivi fisiologici con descrizione, rango di intensita' e le zone che vi ricadono."),
 ("Foglio 'Catalogo Archetipi'", "42 archetipi: 14 di corsa, 13 di nuoto, 11 di ciclismo, 3 di sala pesi e 1 di riposo. Un archetipo e' una FORMA di allenamento - stessa sequenza di blocchi e stesse zone - che il libro istanzia con parametri diversi. Per ciascuno: obiettivo nelle due tassonomie, numero di istanze e di varianti, piani e settimane in cui compare, range di volume, tempo medio e la ripartizione percentuale del tempo per obiettivo."),
 ("Foglio 'Catalogo Allenamenti'", "251 righe, una per allenamento distinto (stessa forma E stessi parametri). E' la matrice allenamento x obiettivo: le 9 colonne finali dicono che quota del tempo di quella seduta va a ciascun obiettivo fisiologico."),
 ("Obiettivo caratterizzante", "Fra tutti i blocchi della seduta che non sono recupero ne' aerobico di sostegno, vince quello di rango di intensita' piu' basso (cioe' piu' intenso). E' lo stimolo che definisce la seduta, anche quando non e' quello che occupa piu' tempo: una seduta di velocita' dedica in genere il 30-40% del tempo agli allunghi e il resto ad aerobico e forza. Per questo accanto all'etichetta c'e' sempre la ripartizione percentuale."),
 ("Cosa varia dentro un archetipo", "Misurato sulle 33 famiglie con piu' istanze: l'obiettivo di volume della sessione varia in 29, la distanza per ripetizione in 28, le durate dei blocchi in 20, il numero di ripetizioni in 12, la zona/andatura solo in 8. L'andatura e' quindi l'identita' dell'archetipo; a progredire e' la dose, non l'intensita'."),
 ("", ""),
 ("--- SPACCHETTAMENTO PARAMETRICO ---", ""),
 ("Foglio 'Parametri Atleta'", "Le celle gialle della colonna D sono gli UNICI input: il passo di ogni zona di riferimento, in minuti decimali (4,50 = 4'30\"). Corsa e ciclismo in min/km, nuoto in min/100 m. I valori attuali sono un esempio da sostituire con i propri."),
 ("Foglio 'Struttura Allenamento'", "Una riga per ogni BLOCCO elementare (non per serie): l'effort e il suo recupero sono due righe distinte, ognuna con ripetizioni, distanza, durata, zona e passo propri. 2.094 blocchi da 528 sessioni."),
 ("Colonna 'Tipo'", "Velocità - allunghi / Velocità - ripetute / Andatura di gara / Endurance continuato / Endurance sulla forza / Recupero / Recupero attivo / Aerobico supplementare / Riposo / Pesi - forza / Pesi - potenza / Gara / Tapering / Nota."),
 ("Colonne dei parametri", "'Ripetizioni', 'Distanza per rip. (m)', 'Durata per rip. da/a (min)' riportano i parametri come li detta il libro. Le durate sono un intervallo quando il libro dà un range (nei calcoli si usa la media); i secondi di recupero sono convertiti in minuti decimali."),
 ("Colonna 'Modo'", "distanza = blocco definito da una distanza; tempo = da una durata; 'distanza o tempo' = il libro dà entrambe come alternative; 'riposo uguale' = il recupero dura quanto l'effort che lo precede; 'residuo' = lavoro aerobico supplementare, calcolato come obiettivo meno la somma degli altri blocchi; 'descrittivo' = tapering, il libro non quantifica."),
 ("Colonne 'Passo', 'Distanza totale', 'Tempo totale'", "Tutte formule. Passo arriva da 'Parametri Atleta' via INDEX/MATCH sulla Zona. Distanza totale = ripetizioni x distanza, oppure ricavata da durata e passo. Tempo totale = ripetizioni x durata media, oppure distanza/passo quando il libro dà solo la distanza."),
 ("Colonna 'Nel totale sessione'", "Si = il blocco concorre al volume complessivo della sessione. No = e' una porzione gia' compresa in un altro blocco: capita solo nella fase di base, dove i minuti/metri di endurance sulla forza sono una parte della distanza della seduta, non un lavoro aggiuntivo."),
 ("Colonna 'Struttura sessione'", "Notazione sintetica dell'intera sessione, ripetuta su tutte le sue righe. Esempio: '5 x (1000m @corsa_5km + 400m @corsa_recupero) + suppl @corsa_aerobica'."),
 ("Blocco residuo", "L'ultima serie di quasi ogni sessione e' 'lavoro aerobico supplementare per raggiungere l'obiettivo'. La sua distanza non e' nel libro: qui e' calcolata come obiettivo meno tutto il resto, quindi si aggiorna da sola quando cambi i parametri."),
 ("Pesi", "Le sedute con i pesi non hanno distanza ne' passo: usano le colonne 'Set (pesi)', 'Rip. (pesi)' e '% 1RM'."),
 ("Foglio 'Controllo Sessioni'", "Una riga per sessione: confronta la somma dei blocchi con l'obiettivo dichiarato dal libro, e riporta il tempo totale stimato. Serve a validare il modello e a intercettare le incoerenze del libro. 'Blocchi oltre obiettivo' segnala le sessioni in cui il lavoro prescritto supera gia' l'obiettivo, quindi il supplementare risulta zero."),
 ("Esiti del controllo", "OK = i blocchi quadrano con l'obiettivo (357 sessioni). 'Tapering - non quantificato' = settimana di tapering, dove il libro descrive la seduta a parole senza dare serie (16 sessioni). 'n.d.' = riposo, sedute con i pesi o sessioni sostituite dalla gara, che non hanno obiettivo (144). 'Blocchi oltre obiettivo' = 11 sessioni."),
 ("Perche' alcune sessioni non quadrano", "Due cause. (1) Il libro stesso: in alcune sessioni la somma delle ripetute supera l'obiettivo dichiarato, oppure i recuperi non sono conteggiati nel totale. (2) I passi impostati: i blocchi definiti a tempo diventano distanza attraverso il passo, quindi un passo lento su un blocco lungo puo' far sforare la quadratura. Vale la pena ricontrollare l'esito dopo aver messo i propri valori."),
]:
    a = wl.cell(row=r, column=1, value=kk); a.font = BOLD; a.alignment = Alignment(vertical="top")
    b_ = wl.cell(row=r, column=2, value=fix(vv)); b_.font = BODY
    b_.alignment = Alignment(vertical="top", wrap_text=True)
    r += 1



# ==========================================================================
# FOGLIO "Zone e Carico"  (layout ANCORATO: le formule puntano a righe fisse)
# ==========================================================================
wz = wb.create_sheet("Zone e Carico")
wz["A1"] = "Zone di frequenza cardiaca e modello di carico"; wz["A1"].font = TITLE
wz["A2"] = ("Tutte le celle gialle sono input. Il punteggio di ogni blocco nasce qui: zona FC -> peso -> punti. "
            "ATTENZIONE: il libro non da' frequenze cardiache, le zone sono dedotte dall'obiettivo fisiologico. "
            "Il punteggio misura lo SFORZO PREVISTO DAL LIBRO, non il tuo sforzo reale.")
wz["A2"].font = Font(name=FONT, size=9, italic=True, color="C00000")

wz["A4"] = "1. Zone di frequenza cardiaca - metodo Karvonen (% della FC di riserva)"; wz["A4"].font = BOLD
header(wz, 5, ["Zona","% FCris da","% FCris a","% FCris rappresentativa","Peso Edwards","Descrizione","Fattore Banister"], "404040")
ZONE_FC = [("Z1",0.30,0.45,0.375,1,"Recupero: dissipazione, nessuno stimolo adattativo"),
           ("Z2",0.45,0.60,0.525,2,"Aerobico: base, efficienza, capillarizzazione"),
           ("Z3",0.60,0.75,0.675,3,"Medio / ritmo gara: adattamento specifico"),
           ("Z4",0.75,0.88,0.815,4,"Soglia: alza il tetto sostenibile"),
           ("Z5",0.88,1.00,0.940,5,"Massimale: VO2max, lattacido, velocita'")]
r = 6
for z, a, b_, m, p, d in ZONE_FC:
    wz.cell(row=r, column=1, value=z).font = BOLD
    for j, v in ((2,a),(3,b_),(4,m),(5,p)):
        c = wz.cell(row=r, column=j, value=v); c.font = BLU; c.fill = GIALLO
        c.number_format = '0.0%' if j < 5 else '0'
    wz.cell(row=r, column=6, value=fix(d)).font = BODY
    wz.cell(row=r, column=7, value=f'=IF($D{r}="","",$D{r}*0.64*EXP($B$41*$D{r}))').number_format = '0.000'
    wz.cell(row=r, column=7).font = BODY
    for j in range(1,8):
        wz.cell(row=r, column=j).border = BRD
        wz.cell(row=r, column=j).alignment = Alignment(horizontal="center" if 1 < j < 6 else "left", vertical="center")
    r += 1

wz["A12"] = "2. Frequenze cardiache dell'atleta e zone in battiti"; wz["A12"].font = BOLD
wz["A13"] = fix("Compila FC max e FC a riposo nella tabella 4 in fondo: i battiti qui sotto si calcolano da soli con "
                "la formula di Karvonen -> FC = FCriposo + %FCris x (FCmax - FCriposo).")
wz["A13"].font = Font(name=FONT, size=9, italic=True, color="666666")
header(wz, 15, ["Disciplina","FC riserva","Z1 (bpm)","Z2 (bpm)","Z3 (bpm)","Z4 (bpm)","Z5 (bpm)"], "404040")
for i_, d in enumerate(("Corsa a piedi","Ciclismo","Nuoto")):
    rr = 16 + i_; src = 35 + i_
    wz.cell(row=rr, column=1, value=d).font = BODY
    wz.cell(row=rr, column=2, value=f'=IF(OR($D${src}="",$E${src}=""),"",$D${src}-$E${src})')
    for j in range(3, 8):
        zr = 6 + (j - 3)
        wz.cell(row=rr, column=j, value=(
            f'=IF($B{rr}="","",TEXT(ROUND($E${src}+$B${zr}*$B{rr},0),"0")&"-"&'
            f'TEXT(ROUND($E${src}+$C${zr}*$B{rr},0),"0"))'))
    for j in range(1, 8):
        wz.cell(row=rr, column=j).font = BODY; wz.cell(row=rr, column=j).border = BRD
        wz.cell(row=rr, column=j).alignment = Alignment(horizontal="center" if j > 1 else "left")

wz["A20"] = "3. Da obiettivo fisiologico a zona di frequenza cardiaca"; wz["A20"].font = BOLD
header(wz, 21, ["Obiettivo fisiologico","Zona FC"], "404040")
OB_ZONA = {"Recupero attivo":"Z1", "Aerobico lento (lungo)":"Z2", "Aerobico base":"Z2",
           "Ritmo gara specifico":"Z3", "Forza specifica":"Z3", "Soglia anaerobica":"Z4",
           "VO2max":"Z5", "Capacita' anaerobica":"Z5", "Velocita' neuromuscolare":"Z5",
           "Forza massimale":"Z2", "Potenza ed endurance muscolare":"Z3"}
r = 22
for _o, _rk, _de in OB.TASSONOMIA:
    wz.cell(row=r, column=1, value=fix(_o)).font = BODY
    c = wz.cell(row=r, column=2, value=OB_ZONA.get(_o, "Z2")); c.font = BLU; c.fill = GIALLO
    for j in (1, 2):
        wz.cell(row=r, column=j).border = BRD
        wz.cell(row=r, column=j).alignment = Alignment(horizontal="center" if j == 2 else "left")
    r += 1

wz["A33"] = "4. Parametri per disciplina"; wz["A33"].font = BOLD
header(wz, 34, ["Disciplina","Coeff. carico","Passo di soglia","FC max","FC riposo","Zona di soglia usata"], "404040")
SOGLIA = {"Corsa a piedi":("corsa_10km",190,55), "Ciclismo":("bici_40km",182,55),
          "Nuoto":("nuoto_1600m",178,55), "Pesi":("",0,0)}
COEFF = {"Corsa a piedi":1.00, "Ciclismo":0.95, "Nuoto":0.90, "Pesi":1.00}
r = 35
for d, (zk, fcm, fcr) in SOGLIA.items():
    wz.cell(row=r, column=1, value=d).font = BODY
    c = wz.cell(row=r, column=2, value=COEFF[d]); c.font = BLU; c.fill = GIALLO; c.number_format = '0.00'
    if zk:
        wz.cell(row=r, column=3, value=f'=IFERROR(INDEX({PAR}!$F${ZFIRST}:$F${ZLAST},MATCH($F{r},{PAR}!$A${ZFIRST}:$A${ZLAST},0)),"")').number_format = '0.00'
        for j, v in ((4, fcm), (5, fcr)):
            c = wz.cell(row=r, column=j, value=v); c.font = BLU; c.fill = GIALLO
        c = wz.cell(row=r, column=6, value=zk); c.font = BLU; c.fill = GIALLO
    for j in range(1, 7):
        wz.cell(row=r, column=j).border = BRD
        wz.cell(row=r, column=j).alignment = Alignment(horizontal="center" if j > 1 else "left")
    r += 1

wz["A39"] = "5. Altri parametri"; wz["A39"].font = BOLD
wz["A40"] = fix("Durata stimata di una seduta con i pesi (min)"); wz["A40"].font = BODY
c = wz["B40"]; c.value = 45; c.font = BLU; c.fill = GIALLO; c.border = BRD
wz["C40"] = fix("Il libro non indica la durata delle sedute in sala: senza questo valore 88 sessioni peserebbero zero.")
wz["C40"].font = Font(name=FONT, size=9, italic=True, color="666666")
wz["A41"] = fix("k della formula di Banister"); wz["A41"].font = BODY
c = wz["B41"]; c.value = 1.92; c.font = BLU; c.fill = GIALLO; c.border = BRD; c.number_format = '0.00'
wz["C41"] = fix("1,92 per gli uomini, 1,67 per le donne (Banister, 1991).")
wz["C41"].font = Font(name=FONT, size=9, italic=True, color="666666")
wz["A43"] = fix("Formule usate")
wz["A43"].font = BOLD
for i_, t in enumerate([
    "Punti Edwards  =  minuti x peso della zona x coefficiente di disciplina",
    "Punti Banister =  minuti x %FCris x 0,64 x e^(k x %FCris) x coefficiente di disciplina",
    "Punti andatura =  (minuti / 60) x (passo di soglia / passo del blocco)^2 x 100   [logica TSS]",
    "Il coefficiente di disciplina corregge il fatto che a parita' di sforzo la FC e' piu' bassa in bici (~ -5/8 bpm) e in acqua (~ -10/15 bpm).",
]):
    wz.cell(row=44+i_, column=1, value=fix(t)).font = BODY
for i_, w in enumerate([46,16,22,16,16,26,18], 1): wz.column_dimensions[get_column_letter(i_)].width = w


# ==========================================================================
# FOGLIO "Obiettivi di Carico"
# ==========================================================================
wo = wb.create_sheet("Obiettivi di Carico")
wo["A1"] = "Obiettivi di carico - quanto serve per arrivare in fondo a ciascuna gara"; wo["A1"].font = TITLE
wo["A2"] = fix("Il piano del libro E' l'obiettivo: sommando le sue sedute si ottiene il carico che quel libro ritiene "
               "necessario per completare la distanza. E' un riferimento DESCRITTIVO (cosa prescrive questo libro), "
               "non una soglia fisiologica. Tutti i valori sono formule: cambiando i passi o le zone si aggiornano.")
wo["A2"].font = Font(name=FONT, size=9, italic=True, color="666666")

_SAX = f"{SA}!$X$2:$X${N}"; _SAI = f"{SA}!$AI$2:$AI${N}"
_SAJ = f"{SA}!$AJ$2:$AJ${N}"; _SAK = f"{SA}!$AK$2:$AK${N}"
_PI = f"{SA}!$B$2:$B${N}"; _ME = f"{SA}!$D$2:$D${N}"; _SE = f"{SA}!$E$2:$E${N}"; _DI = f"{SA}!$I$2:$I${N}"

def _blocco_carico(riga, crit):
    """crit = lista di (range, valore) gia' formattati"""
    cr = ",".join(f"{rg},{vl}" for rg, vl in crit)
    return [f'=SUMIFS({_SAX},{cr})/60', f'=SUMIFS({_SAI},{cr})',
            f'=SUMIFS({_SAJ},{cr})', f'=SUMIFS({_SAK},{cr})'] + \
           [f'=SUMIFS({_SAX},{cr},{_DI},"{d}")/60' for d in ("Nuoto","Ciclismo","Corsa a piedi","Pesi")]

INTEST = ["Ore","Punti Edwards","Punti Banister","Punti andatura","Ore nuoto","Ore bici","Ore corsa","Ore pesi"]

# --- tabella 1: per settimana ---
righe_w, visti = [], set()
for b in righe:
    s_ = b["sess"]; k = (s_["piano"], s_["meso"], s_["sett"])
    if k not in visti:
        visti.add(k); righe_w.append((s_["piano"], s_["meso"], s_["sett"], s_["nota"]))
wo["A4"] = "1. Carico settimanale"; wo["A4"].font = BOLD
header(wo, 5, ["Piano","Mesociclo","Settimana","Nota"] + [fix(x) for x in INTEST], "404040")
r = 6
for pi, me, se, no in righe_w:
    for j, v in enumerate([pi, fix(me), se, fix(no)], 1): wo.cell(row=r, column=j, value=v)
    for j, f_ in enumerate(_blocco_carico(r, [(_PI, f'$A{r}'), (_SE, f'$C{r}')]), 5):
        c = wo.cell(row=r, column=j, value=f_)
        c.number_format = '0.0' if j in (5,9,10,11,12) else '#,##0'
    for j in range(1, 13):
        c = wo.cell(row=r, column=j); c.font = BODY; c.border = BRD
        c.alignment = Alignment(horizontal="center" if j >= 3 else "left", vertical="center")
        if r % 2 == 0: c.fill = ALTA
    r += 1
W1 = r - 1

# --- tabella 2: per mesociclo ---
r += 2
wo.cell(row=r, column=1, value="2. Carico per mesociclo").font = BOLD
header(wo, r+1, ["Piano","Mesociclo","Settimane","-"] + [fix(x) for x in INTEST], "404040")
r += 2
mes, vistim = [], set()
for b in righe:
    s_ = b["sess"]; k = (s_["piano"], s_["meso"])
    if k not in vistim: vistim.add(k); mes.append(k)
for pi, me in mes:
    ss = sorted({b["sess"]["sett"] for b in righe if b["sess"]["piano"] == pi and b["sess"]["meso"] == me})
    for j, v in enumerate([pi, fix(me), f"{min(ss)}-{max(ss)}", ""], 1): wo.cell(row=r, column=j, value=v)
    for j, f_ in enumerate(_blocco_carico(r, [(_PI, f'$A{r}'), (_ME, f'$B{r}')]), 5):
        c = wo.cell(row=r, column=j, value=f_)
        c.number_format = '0.0' if j in (5,9,10,11,12) else '#,##0'
    for j in range(1, 13):
        c = wo.cell(row=r, column=j); c.font = BODY; c.border = BRD
        c.alignment = Alignment(horizontal="center" if j >= 3 else "left", vertical="center")
    r += 1

# --- tabella 3: totale di piano ---
r += 2
wo.cell(row=r, column=1, value="3. Obiettivo totale per completare la gara").font = BOLD
header(wo, r+1, ["Piano","Settimane","Sessioni","-"] + [fix(x) for x in INTEST], "404040")
r += 2
for pi in ("Triathlon Sprint","Triathlon Olimpico","Half-Ironman","Ironman"):
    ss = {b["sess"]["sett"] for b in righe if b["sess"]["piano"] == pi}
    sess_n = len({b["sid"] for b in righe if b["sess"]["piano"] == pi})
    for j, v in enumerate([pi, len(ss), sess_n, ""], 1): wo.cell(row=r, column=j, value=v)
    for j, f_ in enumerate(_blocco_carico(r, [(_PI, f'$A{r}')]), 5):
        c = wo.cell(row=r, column=j, value=f_)
        c.number_format = '0.0' if j in (5,9,10,11,12) else '#,##0'
    for j in range(1, 13):
        c = wo.cell(row=r, column=j); c.font = BOLD; c.border = BRD; c.fill = FILL_TOT
        c.alignment = Alignment(horizontal="center" if j >= 2 else "left", vertical="center")
    r += 1
for i_, w in enumerate([18,34,12,16,10,15,15,15,11,11,11,11], 1):
    wo.column_dimensions[get_column_letter(i_)].width = w
wo.freeze_panes = "E6"


# ==========================================================================
# FOGLIO "Variazioni Allenamenti"
# ==========================================================================
import variazioni as VAR
importlib.reload(VAR)
_basi = VAR.costruisci_basi()
_tutte = []
for _b in _basi: _tutte.extend(VAR.genera(_b))
VAR.marca_duplicati(_tutte)
ZON_OB = {"Z1":"Recupero attivo","Z2":"Aerobico base","Z3":"Ritmo gara specifico",
          "Z4":"Soglia anaerobica","Z5":"VO2max"}

wx = wb.create_sheet("Variazioni Allenamenti")
wx["A1"] = "Variazioni degli allenamenti - lo spazio delle possibilita'"; wx["A1"].font = TITLE
wx["A2"] = fix("Ogni allenamento del catalogo viene scalato in distanza (+-10..50%) e in passo (+-10..30%, cap "
               "voluto per non generare andature impossibili). Nelle ripetute si scala la distanza della ripetuta "
               "e si tiene il numero: 5 x 1000m a -20% diventa 5 x 800m. Il blocco aerobico supplementare si "
               "ricalcola sul nuovo obiettivo di volume.")
wx["A2"].font = Font(name=FONT, size=9, italic=True, color="666666")
wx["A3"] = fix("ATTENZIONE: cambiare il passo cambia la zona, quindi cambia l'OBIETTIVO. Una variazione non e' lo "
               "stesso allenamento piu' facile o piu' duro: e' un altro allenamento. La colonna 'Cambio obiettivo' "
               "dice quando succede. Minuti per zona e punti andatura sono calcolati sui passi attuali di "
               "'Parametri Atleta': se li cambi molto vanno rigenerati. I punti Edwards e Banister restano formule vive.")
wx["A3"].font = Font(name=FONT, size=9, italic=True, color="C00000")

COLX = ["Codice variazione","Allenamento base","Archetipo","Disciplina","Obiettivo libro",
        "Obiettivo fisiologico base","Delta distanza","Delta passo","Tipo variazione","Una variabile sola",
        "Distanza totale (m)","Tempo totale (min)","Passo medio","Zona risultante",
        "Obiettivo fisiologico risultante","Cambio obiettivo",
        "Min Z1","Min Z2","Min Z3","Min Z4","Min Z5",
        "Punti Edwards","Punti Banister","Punti andatura","Plausibile","Motivo"]
header(wx, 5, [fix(c) for c in COLX], "404040")
ZC = "'Zone e Carico'"
r = 6
for v in _tutte:
    _ob_ris = ZON_OB.get(v["zona_car"], "")
    _cod = f'{v["base"]}|D{(v["kd"]-1)*100:+03.0f}|P{(v["kp"]-1)*100:+03.0f}'
    vals = [_cod, v["base"], v["arch"], v["disc"], fix(v["focus"]), fix(v["ob_base"]),
            v["kd"]-1, v["kp"]-1, v["tipo_var"], "Si" if v["ofat"] else "No",
            round(v["dist"]), round(v["tempo"], 1),
            round(v["passo_medio"], 2) if v["passo_medio"] else None,
            v["zona_car"], fix(_ob_ris), "Si" if v["cambio"] else "No"]
    for j, val in enumerate(vals, 1): wx.cell(row=r, column=j, value=val)
    for j, z in enumerate(("Z1","Z2","Z3","Z4","Z5"), 17):
        wx.cell(row=r, column=j, value=round(v["zmin"][z], 1)).number_format = '0.0'
    _cf = f'IFERROR(INDEX({ZC}!$B$35:$B$38,MATCH($D{r},{ZC}!$A$35:$A$38,0)),1)'
    _ed = "+".join(f'${col}{r}*{ZC}!$E${6+i}' for i, col in enumerate("QRSTU"))
    _ba = "+".join(f'${col}{r}*{ZC}!$G${6+i}' for i, col in enumerate("QRSTU"))
    wx.cell(row=r, column=22, value=f'=({_ed})*{_cf}').number_format = '0.0'
    wx.cell(row=r, column=23, value=f'=({_ba})*{_cf}').number_format = '0.0'
    wx.cell(row=r, column=24, value=round(v["rtss"], 1)).number_format = '0.0'
    wx.cell(row=r, column=25, value="Si" if v["plaus"] else "No")
    wx.cell(row=r, column=26, value=fix(v["motivo"]) or None)
    wx.cell(row=r, column=27, value=v["gruppo"] or None)
    wx.cell(row=r, column=28, value="Si" if v["ridondante"] else "No")
    for j in range(1, len(COLX)+1):
        c = wx.cell(row=r, column=j); c.font = BODY; c.border = BRD
        c.alignment = Alignment(vertical="center", horizontal="center" if j >= 7 else "left")
        if j in (7, 8): c.number_format = '+0%;-0%;0%'
        if j == 11: c.number_format = '#,##0'
        if j in (12, 13): c.number_format = '0.0'
    r += 1
XLAST = r-1
for i_, w in enumerate([24,16,11,15,20,28,12,11,15,17,16,15,12,12,28,15,
                        9,9,9,9,9,14,14,14,12,40,26,12], 1):
    wx.column_dimensions[get_column_letter(i_)].width = w
wx.freeze_panes = "G6"; wx.auto_filter.ref = f"A5:{get_column_letter(len(COLX))}{XLAST}"
wx.conditional_formatting.add(f"Y6:Y{XLAST}", CellIsRule(operator="equal", formula=['"No"'],
    fill=PatternFill("solid", fgColor="FFC7CE")))
wx.conditional_formatting.add(f"P6:P{XLAST}", CellIsRule(operator="equal", formula=['"Si"'],
    fill=PatternFill("solid", fgColor="FFF2CC")))
wx.conditional_formatting.add(f"AB6:AB{XLAST}", CellIsRule(operator="equal", formula=['"Si"'],
    fill=PatternFill("solid", fgColor="EDEDED")))


# ==========================================================================
# FOGLIO "Regole di Costruzione"
# ==========================================================================
wr = wb.create_sheet("Regole di Costruzione")
wr["A1"] = "Regole di costruzione del piano - con status, verifica sui dati e trigger di adattamento"; wr["A1"].font = TITLE
wr["A2"] = fix("Lo STATUS dice quanto pesa una regola. INVARIANT = principio robusto, si applica sempre. "
               "DEFAULT = scelta efficace ma sostituibile. HEURISTIC = guardrail del nostro generatore, NON una "
               "soglia fisiologica dimostrata. ADAPTIVE = dipende dalla risposta dell'atleta. DEPRECATED = "
               "formulazione superata, conservata per tracciabilita'. Confondere i livelli e' il modo piu' rapido "
               "per costruire un algoritmo che sbaglia con sicurezza.")
wr["A2"].font = Font(name=FONT, size=9, italic=True, color="666666")
COLR = ["ID","Status","Categoria","Regola","Sprint","Olimpico","Half-Ironman","Ironman",
        "Trigger di adattamento","Fonte","Evidenza e note"]
header(wr, 4, COLR, "404040")
L = "libro (misurato)"; T = "letteratura"; M = "nostro modello"; LT = "libro + letteratura"
REGOLE = [
 ("D0","INVARIANT","Zone","Le zone devono essere individuali e ancorate fisiologicamente",
  "si'","si'","si'","si'","soglie LT1/LT2 misurate sull'atleta",T,
  "Le 5 zone operative restano per prescrivere; ogni analisi di distribuzione passa per i 3 domini (<LT1 / LT1-LT2 / >LT2). Prerequisito a tutto il resto: senza, nessuna percentuale di zona e' affermabile."),
 ("I1","INVARIANT","Principi","Specificita' crescente verso la gara","si'","si'","si'","si'","-",LT,
  "Confermato dal libro: il rapporto fra lavoro a ritmo gara e lavoro generico cresce nelle fasi finali."),
 ("I2","INVARIANT","Principi","Sovraccarico progressivo","si'","si'","si'","si'","-",LT,"Confermato in tutti e quattro i piani."),
 ("I3","INVARIANT","Principi","Alternanza fra stimolo e recupero","si'","si'","si'","si'","-",LT,"Confermato: scarico ogni 4 settimane senza eccezioni."),
 ("I4","INVARIANT","Intensita'","Prevalenza di lavoro a bassa intensita' a ogni distanza","si'","si'","si'","si'","-",LT,
  "Regge in tutte e 15 le combinazioni di soglia provate: HIGH non supera mai il 14% ed e' sempre il dominio piu' piccolo."),
 ("I5","INVARIANT","Ciclo","Taper pre-gara","si'","si'","si'","si'","-",LT,"Confermato. Distinto dalla settimana di scarico: sono due cose diverse."),
 ("I6","INVARIANT","Combinati","Allenamento della transizione bici-corsa","si'","si'","si'","si'","-",T,
  "Il libro lo fa solo nello Sprint: e' una sua lacuna. La letteratura documenta alterazioni della running economy dopo la bici a tutte le distanze."),
 ("I7","INVARIANT","Mix","Mantenimento di tutte e tre le discipline","si'","si'","si'","si'","-",LT,"Nessuna disciplina scende sotto il carico di mantenimento."),
 ("D1","DEFAULT","Ciclo","Rapporto carico : scarico","3:1","3:1","3:1","3:1","fatica accumulata, eta', storico -> 2:1",L,
  "Il libro usa 3:1 ovunque. Nessuna evidenza robusta impone 2:1 per l'Ironman: il rapporto dipende dal carico assoluto e dalla risposta, non dalla distanza di gara."),
 ("D2","DEFAULT","Ciclo","Profondita' dello scarico","-40%","-40%","-40%","-40%","fatica bassa -25/-35, normale -35/-45, alta -45/-55",LT,
  "Range operativo -30/-50%. Il -41/-60% documentato riguarda il TAPER, non la settimana di scarico: non va trasferito."),
 ("D3","DEFAULT","Struttura","Schema settimanale dei giorni","fisso","fisso","fisso","fisso","tempo disponibile dell'atleta",L,
  "Mar corsa+bici / Mer nuoto+pesi / Gio bici+corsa gara / Ven nuoto / Sab bici+pesi / Dom nuoto+corsa. Identico nei 4 piani, 44 settimane su 44."),
 ("D4","DEFAULT","Mix","Ripartizione ore fra le discipline","B41/C34/N25","B45/C33/N21","B48/C33/N19","B51/C31/N18","coefficiente sul limitante dell'atleta",L,
  "La quota bici cresce con la distanza, il nuoto cala. E' una regola di distanza, non di periodizzazione."),
 ("D5","DEFAULT","Combinati","Frequenza dei brick per fase","base: no / build: 1-2 sett / spec: regolare / taper: micro-brick",
  "idem","idem","idem","fase del piano e distanza",T,
  "Sostituisce sia il 'solo Sprint' del libro sia l'1/settimana della dottrina. Per l'Ironman non serve 180 km + lungo: basta allenare la transizione controllando il danno muscolare."),
 ("D6","DEFAULT","Intensita'","Densita' di carico","121 pt/h","134 pt/h","140 pt/h","139 pt/h","-",L,
  "Quasi costante fra i piani: il libro scala il volume, mai l'intensita'. Coerente con il risultato sugli archetipi."),
 ("H1","HEURISTIC","Progressione","Pendenza settimanale nel blocco di carico","+5/+15%","+5/+15%","+5/+15%","+5/+15%","risposta individuale al carico",M,
  "Banda del GENERATORE, non soglia fisiologica. La letteratura non sostiene nemmeno la regola del 10% e non ha identificato un limite universale di rischio."),
 ("H2","HEURISTIC","Tempo","Dominio di validita' del generatore","5-20 sett.","5-20 sett.","5-20 sett.","5-20 sett.","-",M,
  "NON 'un piano deve durare 5-20 settimane'. Fuori da quell'intervallo si cambia architettura, non si stira il template. Esistono preparazioni 70.3 documentate su 20 settimane."),
 ("H3","HEURISTIC","Tempo","Punto di partenza come quota del picco","50-70%","50-70%","50-70%","50-70%","carico gia' tollerato dall'atleta",M,
  "Nel libro sta fra il 64% e il 77%. Il vero ancoraggio non e' una percentuale astratta ma il carico che l'atleta sostiene oggi."),
 ("A1","ADAPTIVE","Ciclo","Override 2:1","-","-","-","-","fatica alta OR recupero scarso OR carico alto per l'atleta",T,
  "Il rapporto non dipende dalla distanza in se'. Regola: default 3:1, passa a 2:1 quando il costo di recupero lo richiede."),
 ("A2","ADAPTIVE","Ciclo","Carico dopo lo scarico","-","-","-","-","recupero ok -> >= carico pre-scarico; non ok -> inferiore",L,
  "Nel metodo del libro lo scarico non resetta la progressione (+71/+111%). Formulazione prudente: torna nella regione del carico gia' tollerato, salvo segnali contrari."),
 ("A3","ADAPTIVE","Struttura","Frequenza settimanale","-","-","-","-","tempo disponibile e livello dell'atleta",T,
  "Ordine di progressione: volume per seduta -> specificita' -> intensita' -> frequenza. La frequenza si tocca per ultima."),
 ("A4","ADAPTIVE","Mix","Priorita' sulla disciplina limitante","-","-","-","-","limitante identificato, senza scendere sotto il mantenimento",T,
  "carico_disciplina = baseline_distanza x modificatore_limitante x modificatore_fase."),
 ("A5","ADAPTIVE","Intensita'","Forma della distribuzione oltre la quota LOW","-","-","-","-","fase, atleta, richieste di gara",T,
  "Piramidale o polarizzata: la letteratura non impone un modello unico. Nelle pratiche d'elite censite le piramidali superano le polarizzate."),
 ("X1","DEPRECATED","Intensita'","'Polarizzata per distanza: Sprint Z4-Z5, Ironman Z2'","-","-","-","-","-",T,
  "Non sostenibile. Sostituita da I4 + A5. Nei dati tutti e quattro i piani sono piramidali."),
 ("X2","DEPRECATED","Intensita'","'Lo Sprint del libro e' il piano piu' aerobico dei quattro'","-","-","-","-","-",M,
  "ERRORE DELLA PRIMA STESURA. Con le 5 zone non ancorate risultava Z2 76%; con i 3 domini lo Sprint e' il MENO aerobico (LOW 49% contro 65% dell'Ironman). Era un artefatto della mappatura."),
 ("X3","DEPRECATED","Mix","Rotazione obbligatoria della disciplina prioritaria","-","-","-","-","-",T,
  "Sostituita da A4. La block periodization ha supporto, ma nessuna evidenza impone un ciclo mese-bici / mese-corsa / mese-nuoto."),
 ("X4","DEPRECATED","Struttura","'La frequenza deve crescere 4 -> 5 -> 6'","-","-","-","-","-",T,
  "Come la sua opposta ('11 sedute fisse e' la regola'). Entrambe descrivono un profilo di atleta, non una legge. Sostituite da A3."),
 ("X5","DEPRECATED","Ciclo","'Chi riparte piano dopo lo scarico spreca la supercompensazione'","-","-","-","-","-",M,
  "Piu' forte di quanto i dati mostrino. Sostituita da A2."),
]
r = 5
for reg in REGOLE:
    for j, v in enumerate(reg, 1): wr.cell(row=r, column=j, value=fix(str(v)))
    for j in range(1, 12):
        c = wr.cell(row=r, column=j); c.font = BODY; c.border = BRD
        c.alignment = Alignment(vertical="top", wrap_text=(j in (4,9,11)),
                                horizontal="center" if 5 <= j <= 8 else "left")
    wr.cell(row=r, column=1).font = BOLD; wr.cell(row=r, column=2).font = BOLD
    r += 1
RLAST = r-1
for i_, w in enumerate([7,14,14,42,17,17,17,17,38,17,105], 1):
    wr.column_dimensions[get_column_letter(i_)].width = w
wr.freeze_panes = "D5"; wr.auto_filter.ref = f"A4:K{RLAST}"
for val, col in (("INVARIANT","C6EFCE"), ("DEFAULT","DDEBF7"), ("HEURISTIC","FFF2CC"),
                 ("ADAPTIVE","E4DFEC"), ("DEPRECATED","FFC7CE")):
    wr.conditional_formatting.add(f"B5:B{RLAST}",
        CellIsRule(operator="equal", formula=[f'"{val}"'], fill=PatternFill("solid", fgColor=col)))


# ==========================================================================
# TASSONOMIA + CATALOGHI
# ==========================================================================
from collections import Counter as _Ct, defaultdict as _dd2

# --- obiettivo fisiologico caratterizzante per sessione -------------------
_bl_sid = _dd2(list)
for _b in righe:
    _bl_sid[_b["sid"]].append(_b)
CARAT = {}
for _sid, _bs in _bl_sid.items():
    _obs = [OB.ZONA_OBIETTIVO[_b["zona"]] for _b in _bs
            if _b["zona"] in OB.ZONA_OBIETTIVO and _b.get("nel_totale", True)]
    _core = [o for o in _obs if o not in OB.CONTORNO]
    _pool = _core or _obs
    if _pool:
        CARAT[_sid] = min(_pool, key=lambda o: OB.RANK[o])
    else:
        _d = _bs[0]["sess"]["disc"]; _f = _bs[0]["sess"]["focus"]
        _tp = {b["tipo"] for b in _bs}
        if _d == "Riposo":                       CARAT[_sid] = "Recupero completo"
        elif _d == "Pesi":                       CARAT[_sid] = "Forza massimale" if _f == "Forza" else "Potenza ed endurance muscolare"
        elif any(t.startswith("Tapering") for t in _tp): CARAT[_sid] = "Affinamento pre-gara"
        elif "Gara" in _tp:                      CARAT[_sid] = "Gara"
        else:                                    CARAT[_sid] = "n.d."
_SS = {b["sid"]: b["sess"] for b in righe}
_OBM = {b["sid"]: b["ob_m"] for b in righe}
_STR = {b["sid"]: b["struttura"] for b in righe}

# --- foglio Tassonomia Obiettivi -----------------------------------------
wt = wb.create_sheet("Tassonomia Obiettivi")
wt["A1"] = "Tassonomia degli obiettivi"; wt["A1"].font = TITLE
wt["A2"] = ("Due letture affiancate. L'obiettivo DEL LIBRO e' l'etichetta che il libro stesso da' alla seduta "
            "('Attenzione rivolta sulla velocita' nel Nuoto'): e' un dato, non un'interpretazione. "
            "L'obiettivo FISIOLOGICO e' una proposta costruita sopra l'andatura di riferimento di ogni zona: "
            "va validata, e si cambia dalla colonna D del foglio 'Parametri Atleta'.")
wt["A2"].font = Font(name=FONT, size=9, italic=True, color="666666")
header(wt, 4, ["Obiettivo fisiologico","Rango intensita'","Descrizione","Zone che vi ricadono"], "404040")
r = 5
_perob = _dd2(list)
for _z, _o in OB.ZONA_OBIETTIVO.items(): _perob[_o].append(_z)
for _o, _rk, _de in OB.TASSONOMIA:
    wt.cell(row=r, column=1, value=fix(_o)).font = BOLD
    wt.cell(row=r, column=2, value=_rk)
    wt.cell(row=r, column=3, value=fix(_de))
    wt.cell(row=r, column=4, value=", ".join(sorted(_perob.get(_o, []))) or "(sala pesi)")
    for j in range(1, 5):
        c = wt.cell(row=r, column=j); c.font = BOLD if j == 1 else BODY; c.border = BRD
        c.alignment = Alignment(vertical="top", wrap_text=(j in (3, 4)),
                                horizontal="center" if j == 2 else "left")
    r += 1
wt.cell(row=r+1, column=1, value="Rango intensita'").font = BOLD
wt.cell(row=r+1, column=3, value=fix("1 = stimolo piu' intenso, 9 = piu' blando. Serve a scegliere l'obiettivo "
    "CARATTERIZZANTE di una seduta: fra tutti i blocchi che non sono recupero o aerobico di sostegno, "
    "vince quello di rango piu' basso.")).alignment = Alignment(wrap_text=True, vertical="top")
wt.cell(row=r+1, column=3).font = BODY
for i_, w in enumerate([32,16,78,60], 1): wt.column_dimensions[get_column_letter(i_)].width = w

# --- helper per i cataloghi -----------------------------------------------
MAT = OB.MATRICE
SAW, SAX = "$W", "$X"
def _mat_cols(riga, key_col, key_ref):
    """9 formule: % del tempo di sessione per obiettivo fisiologico"""
    out = []
    for _o in MAT:
        out.append(f'=IFERROR(SUMIFS({SA}!$X$2:$X${N},{SA}!{key_col}$2:{key_col}${N},{key_ref},'
                   f'{SA}!$AD$2:$AD${N},"{_o}")/SUMIFS({SA}!$X$2:$X${N},{SA}!{key_col}$2:{key_col}${N},{key_ref}),"")')
    return out

# --- foglio Catalogo Archetipi -------------------------------------------
wa = wb.create_sheet("Catalogo Archetipi")
wa["A1"] = "Catalogo archetipi - la libreria degli allenamenti"; wa["A1"].font = TITLE
wa["A2"] = ("Ogni riga e' una FORMA di allenamento: la stessa struttura di blocchi e zone, istanziata dal libro "
            "con parametri diversi settimana dopo settimana. Le percentuali sono la quota di TEMPO "
            "dedicata a ciascun obiettivo, su tutte le istanze dell'archetipo.")
wa["A2"].font = Font(name=FONT, size=9, italic=True, color="666666")
COLA = (["Archetipo","Disciplina","Obiettivo libro","Obiettivo fisiologico caratterizzante",
         "Istanze","Varianti","Piani","Settimane","Volume min (m)","Volume max (m)",
         "Tempo medio (min)","Forma"] + [f"% {o}" for o in MAT])
header(wa, 4, [fix(c) for c in COLA], "404040")
r = 5
for _code in sorted(ARCH_INFO):
    inf = ARCH_INFO[_code]; sids = inf["sids"]
    vols = [_OBM[s] for s in sids if _OBM[s] is not None]
    piani = sorted({_SS[s]["piano"] for s in sids})
    setts = sorted({_SS[s]["sett"] for s in sids})
    vals = [_code, inf["disc"],
            fix(_Ct(_SS[s]["focus"] for s in sids).most_common(1)[0][0]),
            fix(_Ct(CARAT[s] for s in sids).most_common(1)[0][0]),
            len(sids), len({_STR[s] for s in sids}),
            ", ".join(p.replace("Triathlon ", "") for p in piani),
            f"{min(setts)}-{max(setts)}" if len(setts) > 1 else str(setts[0]),
            min(vols) if vols else None, max(vols) if vols else None,
            f'=IFERROR(SUMIFS({SA}!$X$2:$X${N},{SA}!$AC$2:$AC${N},$A{r})/$E{r},"")',
            fix(inf["forma"])]
    for j, v in enumerate(vals, 1): wa.cell(row=r, column=j, value=v)
    for j, f_ in enumerate(_mat_cols(r, "$AC", f"$A{r}"), 13):
        c = wa.cell(row=r, column=j, value=f_); c.number_format = '0%'
    for j in range(1, len(COLA)+1):
        c = wa.cell(row=r, column=j); c.font = BODY; c.border = BRD
        c.alignment = Alignment(vertical="top", wrap_text=(j == 12),
                                horizontal="center" if j in (5,6,8,9,10,11) or j >= 13 else "left")
        if j in (9,10): c.number_format = '#,##0'
        if j == 11: c.number_format = '0'
    r += 1
ALAST = r-1
for i_, w in enumerate([12,15,20,32,9,10,26,12,13,13,14,68] + [15]*len(MAT), 1):
    wa.column_dimensions[get_column_letter(i_)].width = w
wa.freeze_panes = "E5"; wa.auto_filter.ref = f"A4:{get_column_letter(len(COLA))}{ALAST}"

# --- foglio Catalogo Allenamenti (una riga per variante) -------------------
varianti = _dd2(list)
for _sid in sorted(_STR): varianti[(ARCHET[_sid], _STR[_sid])].append(_sid)
wv = wb.create_sheet("Catalogo Allenamenti")
wv["A1"] = "Catalogo allenamenti - ogni variante con il suo obiettivo"; wv["A1"].font = TITLE
wv["A2"] = ("Una riga per allenamento distinto (stessa struttura E stessi parametri). Le percentuali sono la "
            "quota di tempo per obiettivo, calcolate sulla sessione rappresentativa indicata in colonna K.")
wv["A2"].font = Font(name=FONT, size=9, italic=True, color="666666")
COLV = (["Codice","Archetipo","Disciplina","Obiettivo libro","Obiettivo fisiologico caratterizzante",
         "Volume obiettivo (m)","Ricorrenze","Piani","Settimane","Sessione rappresentativa",
         "Tempo totale (min)","Struttura"] + [f"% {o}" for o in MAT])
header(wv, 4, [fix(c) for c in COLV], "404040")
r = 5
prog = _dd2(int)
for (_code, _st), sids in sorted(varianti.items(), key=lambda x: (x[0][0], -len(x[1]))):
    prog[_code] += 1
    rep = sids[0]
    piani = sorted({_SS[s]["piano"] for s in sids})
    setts = sorted({_SS[s]["sett"] for s in sids})
    vals = [f"{_code}.{prog[_code]:02d}", _code, _SS[rep]["disc"], fix(_SS[rep]["focus"]),
            fix(CARAT[rep]), _OBM[rep], len(sids),
            ", ".join(p.replace("Triathlon ", "") for p in piani),
            ", ".join(str(x) for x in setts), rep,
            f'=IFERROR(SUMIFS({SA}!$X$2:$X${N},{SA}!$A$2:$A${N},$J{r}),"")', fix(_st)]
    for j, v in enumerate(vals, 1): wv.cell(row=r, column=j, value=v)
    for j, f_ in enumerate(_mat_cols(r, "$A", f"$J{r}"), 13):
        c = wv.cell(row=r, column=j, value=f_); c.number_format = '0%'
    for j in range(1, len(COLV)+1):
        c = wv.cell(row=r, column=j); c.font = BODY; c.border = BRD
        c.alignment = Alignment(vertical="top", wrap_text=(j == 12),
                                horizontal="center" if j in (6,7,10,11) or j >= 13 else "left")
        if j == 6: c.number_format = '#,##0'
        if j == 11: c.number_format = '0'
        if r % 2 == 0: c.fill = ALTA
    r += 1
VLAST = r-1
for i_, w in enumerate([12,12,15,20,32,15,12,26,22,20,15,90] + [15]*len(MAT), 1):
    wv.column_dimensions[get_column_letter(i_)].width = w
wv.freeze_panes = "F5"; wv.auto_filter.ref = f"A4:{get_column_letter(len(COLV))}{VLAST}"

NUOVI = ("Legenda","Stima Soglie","Parametri Atleta","Zone e Carico","Obiettivi di Carico","Variazioni Allenamenti","Regole di Costruzione","Struttura Allenamento","Controllo Sessioni","Tassonomia Obiettivi","Catalogo Archetipi","Catalogo Allenamenti")
ordine = [n for n in wb.sheetnames if n not in NUOVI] + \
         ["Regole di Costruzione","Stima Soglie","Parametri Atleta","Zone e Carico","Obiettivi di Carico","Tassonomia Obiettivi",
          "Catalogo Archetipi","Catalogo Allenamenti","Variazioni Allenamenti",
          "Struttura Allenamento","Controllo Sessioni","Legenda"]
wb._sheets = [wb[n] for n in ordine]

out = "/mnt/user-data/outputs/Piani_Triathlon_Sprint_Olimpico_Half-Ironman_Ironman.xlsx"
wb.save(out)
print("salvato | variazioni:", len(_tutte), "| settimane:", len(righe_w), "| blocchi:", len(righe), "| sessioni:", len(sessioni), "| archetipi:", len(ARCH_INFO), "| varianti:", len(varianti))
