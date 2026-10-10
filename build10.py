# -*- coding: utf-8 -*-
import sys, re
sys.path.insert(0,'/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad')
exec(open('/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad/build9_base.py').read())
# -> qui esistono: wb (con i 13 fogli), fix(), FONT, BODY, BOLD, BRD, TITLE, H_FONT, ecc.
import parser as P
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

GIALLO = PatternFill("solid", fgColor="FFF2CC")
VERDE  = PatternFill("solid", fgColor="E2EFDA")
BLU    = Font(name=FONT, size=10, color="0000FF")      # input
NERO   = Font(name=FONT, size=10)                       # formule
H2     = PatternFill("solid", fgColor="404040")

# ==========================================================================
# FOGLIO "Parametri Atleta"
# ==========================================================================
ZONE = [
 # (zona, disciplina, descrizione, passo esempio, unita)
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
            "(4,50 = 4'30\"). Corsa e ciclismo in min/km, nuoto in min/100 m. Tutto il foglio "
            "'Struttura Allenamento' si ricalcola da qui.")
wp["A2"].font = Font(name=FONT, size=9, italic=True, color="666666")
wp["A3"] = ("I valori qui sotto sono SOLO UN ESEMPIO di partenza (atleta amatore): sostituiscili con i tuoi. "
            "Fonte dei nomi zona: le andature di riferimento citate dal libro nelle descrizioni delle serie.")
wp["A3"].font = Font(name=FONT, size=9, italic=True, color="C00000")
header(wp, 5, ["Zona","Disciplina","Descrizione","Passo","Unita' passo","Velocita' (km/h)","Passo (mm:ss)"], "404040")
r = 6
for z, d, desc, passo, un in ZONE:
    wp.cell(row=r, column=1, value=z).font = BOLD
    wp.cell(row=r, column=2, value=d).font = BODY
    wp.cell(row=r, column=3, value=fix(desc)).font = BODY
    c = wp.cell(row=r, column=4, value=passo); c.font = BLU; c.fill = GIALLO; c.number_format = '0.00'
    wp.cell(row=r, column=5, value=un).font = BODY
    if un == "min/km":
        wp.cell(row=r, column=6, value=f"=IF($D{r}=\"\",\"\",60/$D{r})").number_format = '0.0'
    else:
        wp.cell(row=r, column=6, value="-")
    wp.cell(row=r, column=6).font = BODY
    wp.cell(row=r, column=7, value=f'=IF($D{r}="","",TEXT($D{r}/1440,"mm:ss"))').font = BODY
    for j in range(1, 8):
        wp.cell(row=r, column=j).border = BRD
        wp.cell(row=r, column=j).alignment = Alignment(vertical="center",
            horizontal="left" if j in (1,2,3,5) else "center")
    r += 1
ZFIRST, ZLAST = 6, r-1
for i_, w in enumerate([22,16,52,10,14,16,14], 1):
    wp.column_dimensions[get_column_letter(i_)].width = w
wp.freeze_panes = "A6"

# ==========================================================================
# FOGLIO "Struttura Allenamento"
# ==========================================================================
righe, non_parsati = P.analizza()
assert not non_parsati, f"{len(non_parsati)} testi non parsati"

COLS = ["ID sessione","Piano","Fase","Mesociclo","Settimana","Nota settimana","Pagina","Giorno",
        "Disciplina","Focus sessione","Obiettivo sessione (m)","Serie (libro)","Blocco","Tipo",
        "Ripetizioni","Distanza per rip. (m)","Durata per rip. da (min)","Durata per rip. a (min)",
        "Modo","Zona","Unita' passo","Passo","Distanza totale (m)","Tempo totale (min)",
        "Set (pesi)","Rip. (pesi)","% 1RM","Struttura sessione","Note","Testo originale"]
LARG = [11,16,7,30,10,18,8,11,15,22,14,14,8,26,11,13,13,13,16,20,12,9,14,14,9,11,9,60,34,100]
ws = wb.create_sheet("Struttura Allenamento")
header(ws, 1, COLS, "404040")
N = len(righe) + 1
PAR = f"'Parametri Atleta'"

# prima riga di ogni sessione (serve per il blocco residuo)
prima_riga = {}
for k, b in enumerate(righe, start=2):
    prima_riga.setdefault(b["sid"], k)

ALTA = PatternFill("solid", fgColor="F7F7F7")
for k, b in enumerate(righe, start=2):
    s = b["sess"]; disc = s["disc"]
    fatt = 100 if disc == "Nuoto" else 1000
    zn = b["zona"] or ""
    vals = [b["sid"], s["piano"], s.get("fase","Gara"), fix(s["meso"]), s["sett"], fix(s["nota"]),
            s["pag"], fix(s["giorno"]), disc, fix(s["focus"]), b["ob_m"], b["serie_libro"],
            b["blocco"], b["tipo"].replace("'", "’") if "Velocita" in b["tipo"] else b["tipo"],
            b["rip"], b["dist"], b["dur_a"], b["dur_b"], b["modo"], zn]
    for j, v in enumerate(vals, 1):
        ws.cell(row=k, column=j, value=v)
    # U passo unita' / V passo
    if zn in ZONE_SET:
        ws.cell(row=k, column=21, value=f'=IFERROR(INDEX({PAR}!$E${ZFIRST}:$E${ZLAST},MATCH($T{k},{PAR}!$A${ZFIRST}:$A${ZLAST},0)),"")')
        ws.cell(row=k, column=22, value=f'=IFERROR(INDEX({PAR}!$D${ZFIRST}:$D${ZLAST},MATCH($T{k},{PAR}!$A${ZFIRST}:$A${ZLAST},0)),"")')
        ws.cell(row=k, column=22).number_format = '0.00'
    # W distanza totale / X tempo totale
    W = X = None
    if b["modo"] == "residuo":
        f0 = prima_riga[b["sid"]]
        rng = f"$W${f0}:$W${k-1}" if k-1 >= f0 else None
        W = f'=MAX(0,$K{k}-SUM({rng}))' if rng else f'=$K{k}'
        X = f'=IF(OR($W{k}="",$V{k}=""),"",$W{k}/{fatt}*$V{k})'
    elif b["modo"] == "riposo uguale":
        X = f'=IF($X{k-1}="","",$X{k-1})'
    elif b["dist"] is not None:
        W = f'=$O{k}*$P{k}'
        if b["dur_a"] is not None and b["modo"] != "distanza o tempo":
            X = f'=$O{k}*AVERAGE($Q{k}:$R{k})'
        elif b["dur_a"] is not None:
            X = f'=$O{k}*AVERAGE($Q{k}:$R{k})'
        else:
            X = f'=IF($V{k}="","",$W{k}/{fatt}*$V{k})'
    elif b["dur_a"] is not None:
        W = f'=IF($V{k}="","",$O{k}*AVERAGE($Q{k}:$R{k})/$V{k}*{fatt})'
        X = f'=$O{k}*AVERAGE($Q{k}:$R{k})'
    if W: ws.cell(row=k, column=23, value=W).number_format = '#,##0'
    if X: ws.cell(row=k, column=24, value=X).number_format = '0.0'
    ws.cell(row=k, column=25, value=b["setp"])
    ws.cell(row=k, column=26, value=b["ripp"])
    ws.cell(row=k, column=27, value=b["rm"])
    ws.cell(row=k, column=28, value=b["struttura"])
    ws.cell(row=k, column=29, value=fix(b["nota"]) if b["nota"] else None)
    ws.cell(row=k, column=30, value=fix(b["testo"]))
    for j in range(1, 31):
        c = ws.cell(row=k, column=j)
        c.font = BODY; c.border = BRD
        c.alignment = Alignment(vertical="top", wrap_text=(j in (28,29,30)))
        if j in (1,5,7,11,13,15,16,17,18,23,24,25,26,27):
            c.alignment = Alignment(horizontal="center", vertical="top")
        if k % 2 == 0: c.fill = ALTA
    for j in (17,18):
        ws.cell(row=k, column=j).number_format = '0.00'
for i_, w in enumerate(LARG, 1):
    ws.column_dimensions[get_column_letter(i_)].width = w
ws.freeze_panes = "O2"
ws.auto_filter.ref = f"A1:AD{N}"

# ==========================================================================
# LEGENDA: aggiungi le righe sui nuovi fogli
# ==========================================================================
wl = wb["Legenda"]
r = wl.max_row + 2
extra = [
 ("", ""),
 ("--- SPACCHETTAMENTO PARAMETRICO ---", ""),
 ("Foglio 'Parametri Atleta'", "Le celle gialle della colonna D sono gli UNICI input: il passo di ogni zona di riferimento, in minuti decimali (4,50 = 4'30\"). Corsa e ciclismo in min/km, nuoto in min/100 m. I valori attuali sono un esempio da sostituire con i propri."),
 ("Foglio 'Struttura Allenamento'", "Una riga per ogni BLOCCO elementare di allenamento (non per serie): l'effort e il suo recupero diventano due righe distinte, ognuna con ripetizioni, distanza, durata, zona e passo propri. 2.094 blocchi da 528 sessioni."),
 ("Colonna 'Tipo'", "Classifica il blocco: Velocita' - allunghi / Velocita' - ripetute / Andatura di gara / Endurance continuato / Endurance sulla forza / Recupero / Recupero attivo / Aerobico supplementare / Riposo / Pesi - forza / Pesi - potenza / Gara / Tapering / Nota."),
 ("Colonne 'Ripetizioni', 'Distanza per rip.', 'Durata per rip.'", "I parametri come li detta il libro. Le durate sono un intervallo (da/a) quando il libro dà un range; nei calcoli si usa la media. I secondi di recupero sono convertiti in minuti decimali."),
 ("Colonna 'Modo'", "distanza = il blocco è definito da una distanza; tempo = da una durata; 'distanza o tempo' = il libro dà entrambe come alternative; 'riposo uguale' = il recupero dura quanto l'effort che lo precede; 'residuo' = lavoro aerobico supplementare, calcolato come obiettivo di sessione meno la somma di tutti gli altri blocchi; 'descrittivo' = settimana di tapering, il libro non quantifica."),
 ("Colonne 'Passo', 'Distanza totale', 'Tempo totale'", "Tutte formule. Passo viene da 'Parametri Atleta' via INDEX/MATCH sulla Zona. Distanza totale = ripetizioni x distanza (o ricavata da durata e passo). Tempo totale = ripetizioni x durata media, oppure distanza/passo quando il libro dà solo la distanza."),
 ("Colonna 'Struttura sessione'", "Notazione sintetica dell'intera sessione, ripetuta su tutte le sue righe. Esempio: '5 x (1000m @corsa_5km + 400m @corsa_recupero) + suppl @corsa_aerobica'."),
 ("Blocco residuo", "L'ultima serie di quasi ogni sessione è 'lavoro aerobico supplementare per raggiungere l'obiettivo'. La sua distanza NON è nel libro: qui è calcolata come obiettivo della sessione meno tutto il resto, quindi si aggiorna da sola se cambi i parametri."),

 ("Foglio 'Controllo Sessioni'", "Una riga per sessione: confronta la somma delle distanze dei blocchi con l'obiettivo dichiarato dal libro. Serve a validare il modello e a intercettare le incoerenze del libro stesso. 'Blocchi oltre obiettivo' segnala le sessioni in cui il lavoro prescritto supera gia' l'obiettivo, quindi il supplementare e' zero."),
 ("Sessioni fuori quadratura", "Sono 11 su 260 (~4%). Non sono errori di trascrizione: il libro stesso in alcune sessioni prescrive ripetute la cui somma supera l'obiettivo dichiarato, oppure non conteggia i recuperi nel totale. La piu' vistosa e' Olimpico 12a sett., domenica corsa (il refuso di pag. 237)."),
 ("Pesi", "Le sedute con i pesi non hanno distanza né passo: usano le colonne 'Set (pesi)', 'Rip. (pesi)' e '% 1RM'."),
]
for kk, vv in extra:
    a = wl.cell(row=r, column=1, value=kk); a.font = BOLD; a.alignment = Alignment(vertical="top")
    b_ = wl.cell(row=r, column=2, value=fix(vv)); b_.font = BODY
    b_.alignment = Alignment(vertical="top", wrap_text=True)
    r += 1


# ==========================================================================
# FOGLIO "Controllo Sessioni" - quadratura blocchi vs obiettivo
# ==========================================================================
sessioni = []
for k, b in enumerate(righe, start=2):
    if not sessioni or sessioni[-1]["sid"] != b["sid"]:
        sessioni.append(dict(sid=b["sid"], sess=b["sess"], ob=b["ob_m"]))

wc = wb.create_sheet("Controllo Sessioni")
wc["A1"] = "Controllo di quadratura: blocchi prescritti vs obiettivo di sessione"
wc["A1"].font = TITLE
wc["A2"] = ("Confronta la somma delle distanze dei blocchi (foglio 'Struttura Allenamento') con l'obiettivo di "
            "quantita' complessiva dichiarato dal libro. Dipende dai passi impostati in 'Parametri Atleta', "
            "perche' i recuperi a tempo vengono convertiti in distanza.")
wc["A2"].font = Font(name=FONT, size=9, italic=True, color="666666")
header(wc, 4, ["ID sessione","Piano","Fase","Settimana","Pagina","Giorno","Disciplina","Focus",
               "Obiettivo (m)","Somma blocchi (m)","di cui supplementare (m)","Scarto (m)",
               "Tempo totale (min)","Esito"], "404040")
SA = "'Struttura Allenamento'"
r = 5
for d in sessioni:
    s = d["sess"]
    wc.cell(row=r, column=1, value=d["sid"])
    wc.cell(row=r, column=2, value=s["piano"])
    wc.cell(row=r, column=3, value=s.get("fase","Gara"))
    wc.cell(row=r, column=4, value=s["sett"])
    wc.cell(row=r, column=5, value=s["pag"])
    wc.cell(row=r, column=6, value=fix(s["giorno"]))
    wc.cell(row=r, column=7, value=s["disc"])
    wc.cell(row=r, column=8, value=fix(s["focus"]))
    wc.cell(row=r, column=9, value=d["ob"])
    wc.cell(row=r, column=10, value=f'=SUMIFS({SA}!$W$2:$W${N},{SA}!$A$2:$A${N},$A{r})')
    wc.cell(row=r, column=11, value=f'=SUMIFS({SA}!$W$2:$W${N},{SA}!$A$2:$A${N},$A{r},{SA}!$N$2:$N${N},"Aerobico supplementare")')
    wc.cell(row=r, column=12, value=f'=IF($I{r}="","",$J{r}-$I{r})')
    wc.cell(row=r, column=13, value=f'=SUMIFS({SA}!$X$2:$X${N},{SA}!$A$2:$A${N},$A{r})')
    wc.cell(row=r, column=14, value=f'=IF($I{r}="","n.d.",IF(ABS($L{r})<=1,"OK",IF($L{r}>0,"Blocchi oltre obiettivo","Residuo non assegnato")))')
    for j in range(1, 15):
        c = wc.cell(row=r, column=j)
        c.font = BODY; c.border = BRD
        c.alignment = Alignment(horizontal="center" if j not in (2,6,7,8,14) else "left", vertical="center")
        if j in (9,10,11,12): c.number_format = '#,##0'
        if j == 13: c.number_format = '0.0'
    r += 1
CLAST = r - 1
for i_, w in enumerate([11,18,7,10,8,11,15,22,14,18,24,12,17,26], 1):
    wc.column_dimensions[get_column_letter(i_)].width = w
wc.freeze_panes = "A5"
wc.auto_filter.ref = f"A4:N{CLAST}"
from openpyxl.formatting.rule import CellIsRule
wc.conditional_formatting.add(f"N5:N{CLAST}",
    CellIsRule(operator="equal", formula=['"OK"'], fill=PatternFill("solid", fgColor="C6EFCE")))
wc.conditional_formatting.add(f"N5:N{CLAST}",
    CellIsRule(operator="equal", formula=['"Blocchi oltre obiettivo"'], fill=PatternFill("solid", fgColor="FFC7CE")))

# ordine fogli: piani, poi i nuovi, poi legenda
NUOVI = ("Legenda","Parametri Atleta","Struttura Allenamento","Controllo Sessioni")
ordine = [n for n in wb.sheetnames if n not in NUOVI]
ordine += ["Parametri Atleta", "Struttura Allenamento", "Controllo Sessioni", "Legenda"]
wb._sheets = [wb[n] for n in ordine]

out = "/mnt/user-data/outputs/Piani_Triathlon_Sprint_Olimpico_Half-Ironman_Ironman.xlsx"
wb.save(out)
print("salvato:", out)
print("blocchi:", len(righe), "| fogli:", wb.sheetnames)
