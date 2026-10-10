# -*- coding: utf-8 -*-
import re, sys
sys.path.insert(0,'/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad')
import dati2
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

ACC = {'a':'à','e':'è','i':'ì','o':'ò','u':'ù'}
GIORNI = {"Lunedi":"Lunedì","Martedi":"Martedì","Mercoledi":"Mercoledì","Giovedi":"Giovedì","Venerdi":"Venerdì"}
def fix(t):
    if not isinstance(t,str): return t
    t = re.sub(r"([aeiou])'(?![A-Za-z])", lambda m: ACC[m.group(1)], t)
    t = t.replace("Velocita","Velocità")
    for k,v in GIORNI.items(): t = t.replace(k,v)
    return t

ORD = ["Prima Serie","Seconda Serie","Terza Serie","Quarta Serie","Quinta Serie",
       "Sesta Serie","Settima Serie","Ottava Serie"]
FONT = "Arial"
H_FONT = Font(name=FONT, size=10, bold=True, color="FFFFFF")
TITLE  = Font(name=FONT, size=14, bold=True, color="1F3864")
BODY   = Font(name=FONT, size=10)
BOLD   = Font(name=FONT, size=10, bold=True)
THIN   = Side(style="thin", color="BFBFBF")
BRD    = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
FILL_TOT = PatternFill("solid", fgColor="FFF2CC")
COLORI = {"Ironman": ("1F3864","F2F5FA"), "Half-Ironman": ("7B3F00","FBF4EC")}

wb = Workbook(); wb.remove(wb.active)

def header(ws, row, cols, hexcol):
    fill = PatternFill("solid", fgColor=hexcol)
    for i,c in enumerate(cols,1):
        cell = ws.cell(row=row, column=i, value=c)
        cell.font, cell.fill, cell.border = H_FONT, fill, BRD
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = 30

def etichetta(s, i):
    if s["disc"] == "Pesi":
        return "Prescrizione" if (i < 2 and not s.get("descr")) else "Nota"
    if s["disc"] == "Riposo": return "-"
    if s.get("descr"): return "Descrizione"
    return ORD[i] if i < len(ORD) else f"Serie {i+1}"

COLS = ["Piano","Mesociclo","Settimana","Nota settimana","Pagina","Giorno","Disciplina",
        "Focus sessione","Obiettivo volume sessione","Volume","Unità","Serie","Descrizione della serie"]
W = [14,34,10,14,8,11,15,20,24,9,8,14,105]

def costruisci(piano):
    dark, light = COLORI[piano]
    sess = [s for s in dati2.TUTTE if s["piano"] == piano]
    ALT = PatternFill("solid", fgColor=light)

    # --- Dettaglio Serie ---
    ws = wb.create_sheet(f"Dettaglio Serie ({piano})"[:31])
    header(ws, 1, COLS, dark)
    r = 2
    for s in sess:
        for i, testo in enumerate(s["serie"]):
            vals = [piano, fix(s["meso"]), s["sett"], fix(s["nota"]), s["pag"], fix(s["giorno"]),
                    s["disc"], fix(s["focus"]), fix(s["vol_txt"]), s["vol_num"], s["unita"],
                    etichetta(s,i), fix(testo)]
            for j,v in enumerate(vals,1):
                c = ws.cell(row=r, column=j, value=v)
                c.font, c.border = BODY, BRD
                c.alignment = Alignment(vertical="top", wrap_text=(j==13))
                if j in (3,5,10): c.alignment = Alignment(horizontal="center", vertical="top")
                if r % 2 == 0: c.fill = ALT
            r += 1
    for i,w in enumerate(W,1): ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "F2"; ws.auto_filter.ref = f"A1:M{r-1}"

    # --- Riepilogo Sessioni ---
    ws2 = wb.create_sheet(f"Riepilogo Sess. ({piano})"[:31])
    cols2 = COLS[:11] + ["N. serie","Sintesi allenamento"]
    header(ws2, 1, cols2, dark)
    r = 2
    for s in sess:
        vals = [piano, fix(s["meso"]), s["sett"], fix(s["nota"]), s["pag"], fix(s["giorno"]),
                s["disc"], fix(s["focus"]), fix(s["vol_txt"]), s["vol_num"], s["unita"],
                len(s["serie"]), " | ".join(fix(t) for t in s["serie"])]
        for j,v in enumerate(vals,1):
            c = ws2.cell(row=r, column=j, value=v)
            c.font, c.border = BODY, BRD
            c.alignment = Alignment(vertical="top", wrap_text=(j==13))
            if j in (3,5,10,12): c.alignment = Alignment(horizontal="center", vertical="top")
            if r % 2 == 0: c.fill = ALT
        r += 1
    for i,w in enumerate(W[:11]+[9,120],1): ws2.column_dimensions[get_column_letter(i)].width = w
    ws2.freeze_panes = "F2"; ws2.auto_filter.ref = f"A1:M{r-1}"
    LAST = r-1

    # --- Volumi Settimanali (formule sul riepilogo) ---
    ws3 = wb.create_sheet(f"Volumi Sett. ({piano})"[:31])
    ws3["A1"] = f"Volumi settimanali per disciplina - {piano}"; ws3["A1"].font = TITLE
    ws3["A2"] = f"Calcolati con SUMIFS/COUNTIFS sul foglio '{ws2.title}' (colonna Volume). Fonte: piano trascritto dal libro."
    ws3["A2"].font = Font(name=FONT, size=9, italic=True, color="666666")
    header(ws3, 4, ["Mesociclo","Settimana","Nota","Nuoto (m)","Ciclismo (km)","Corsa (km)","Sedute pesi"], dark)
    chiavi = []
    for s in sess:
        k = (s["meso"], s["sett"], s["nota"])
        if k not in chiavi: chiavi.append(k)
    RS = f"'{ws2.title}'"
    r = 5
    for meso, sett, nota in chiavi:
        ws3.cell(row=r, column=1, value=fix(meso))
        ws3.cell(row=r, column=2, value=sett)
        ws3.cell(row=r, column=3, value=fix(nota))
        for col, disc in ((4,"Nuoto"), (5,"Ciclismo"), (6,"Corsa a piedi")):
            ws3.cell(row=r, column=col,
                     value=f'=SUMIFS({RS}!$J$2:$J${LAST},{RS}!$C$2:$C${LAST},$B{r},{RS}!$G$2:$G${LAST},"{disc}")')
        ws3.cell(row=r, column=7,
                 value=f'=COUNTIFS({RS}!$C$2:$C${LAST},$B{r},{RS}!$G$2:$G${LAST},"Pesi")')
        for j in range(1,8):
            c = ws3.cell(row=r, column=j); c.font, c.border = BODY, BRD
            c.alignment = Alignment(horizontal="center" if j>1 else "left", vertical="center")
            if j in (4,5,6): c.number_format = '#,##0.0'
        r += 1
    tot = r
    ws3.cell(row=tot, column=1, value=f"TOTALE {len(chiavi)} settimane").font = BOLD
    for j, col in zip(range(4,8), "DEFG"):
        c = ws3.cell(row=tot, column=j, value=f'=SUM({col}5:{col}{tot-1})')
        c.font, c.border = BOLD, BRD
        c.number_format = '#,##0.0' if j < 7 else '0'
        c.alignment = Alignment(horizontal="center")
    for j in range(1,8):
        ws3.cell(row=tot, column=j).border = BRD
        ws3.cell(row=tot, column=j).fill = FILL_TOT
    for i,w in enumerate([34,11,13,14,15,13,13],1): ws3.column_dimensions[get_column_letter(i)].width = w

costruisci("Ironman")
costruisci("Half-Ironman")

# ============ LEGENDA ============
ws4 = wb.create_sheet("Legenda")
ws4["A1"] = "Piani di allenamento - Fase di preparazione alla gara"; ws4["A1"].font = TITLE
righe = [
    ("Fonte", "Trascrizione delle pagine fotografate del libro (sezioni 'Distanza Ironman' e 'Distanza Half-Ironman')."),
    ("", ""),
    ("IRONMAN - copertura", "Settimane 1-12, pagine 277-311. Primo Mesociclo: sett. 1-4 (la 4a e' di Ripristino). Secondo Mesociclo: sett. 5-9 (la 8a e' di Ripristino). Terzo Mesociclo: sett. 10-12 (la 12a e' di Tapering)."),
    ("HALF-IRONMAN - copertura", "Solo 1a settimana del Primo Mesociclo, pagine 252-254. Le settimane successive non sono state fotografate."),
    ("Perche' due sezioni", "Ironman e Half-Ironman sono due piani distinti, con volumi e andature di riferimento diversi: hanno fogli separati e non vanno sommati tra loro."),
    ("", ""),
    ("Fogli 'Dettaglio Serie'", "Una riga per ogni serie di ogni sessione, con il testo integrale della descrizione."),
    ("Fogli 'Riepilogo Sess.'", "Una riga per sessione, con tutte le serie concatenate nella colonna 'Sintesi allenamento'."),
    ("Fogli 'Volumi Sett.'", "Totali per disciplina calcolati con formule SUMIFS/COUNTIFS sul relativo foglio di riepilogo."),
    ("", ""),
    ("Struttura settimana tipo", "Lunedì: riposo - Martedì: corsa + ciclismo (velocità) - Mercoledì: nuoto (velocità) + pesi (forza) - Giovedì: ciclismo + corsa (andatura di gara) - Venerdì: nuoto (andatura di gara) - Sabato: ciclismo (endurance) + pesi (potenza ed endurance muscolare) - Domenica: nuoto + corsa (endurance)."),
    ("Colonna 'Volume'", "Valore numerico dell'obiettivo di quantità complessiva della sessione: metri per il nuoto, chilometri per ciclismo e corsa. Vuota per le sedute di pesi, per il riposo e per le sessioni della 12a settimana sostituite dalla gara."),
    ("Ultima serie", "In quasi tutte le sessioni l'ultima serie e' del lavoro aerobico supplementare per raggiungere l'obiettivo di volume della sessione."),
    ("Etichetta 'Descrizione'", "Usata nella 12a settimana (Tapering) e nelle sedute pesi, dove il libro non numera le serie ma descrive la sessione a testo."),
    ("Settimane di Ripristino", "Ironman 4a e 8a settimana: volumi e serie ridotti circa del 50% rispetto alla settimana precedente."),
    ("12a settimana (Tapering)", "Le sessioni di sabato e domenica sono sostituite dalla gara. Pesi e pliometria vanno eliminati prima della gara."),
    ("Nota pesi settimana 1", "Nella 1a settimana (sia Ironman sia Half-Ironman) il libro specifica: nessuna progressione nei pesi rispetto al periodo di base."),
]
r = 3
for k, v in righe:
    a = ws4.cell(row=r, column=1, value=k); a.font = BOLD; a.alignment = Alignment(vertical="top")
    b = ws4.cell(row=r, column=2, value=fix(v)); b.font = BODY
    b.alignment = Alignment(vertical="top", wrap_text=True)
    r += 1
ws4.column_dimensions["A"].width = 30
ws4.column_dimensions["B"].width = 115

out = "/mnt/user-data/outputs/Piano_Ironman_e_Half-Ironman_Preparazione_Gara.xlsx"
wb.save(out)
print("salvato:", out)
