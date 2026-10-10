# -*- coding: utf-8 -*-
import sys
sys.path.insert(0,'/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad')
exec(open('/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad/build9_base.py').read())
import importlib, parser as P, obiettivi as OB
importlib.reload(P); importlib.reload(OB)
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule

GIALLO = PatternFill("solid", fgColor="FFF2CC")
BLU    = Font(name=FONT, size=10, color="0000FF")
ALTA   = PatternFill("solid", fgColor="F7F7F7")

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
header(wp, 5, ["Zona","Disciplina","Descrizione","Obiettivo fisiologico","Passo","Unita' passo","Velocita' (km/h)","Passo (mm:ss)"], "404040")
r = 6
for z, d, desc, passo, un in ZONE:
    wp.cell(row=r, column=1, value=z).font = BOLD
    wp.cell(row=r, column=2, value=d).font = BODY
    wp.cell(row=r, column=3, value=fix(desc)).font = BODY
    c = wp.cell(row=r, column=4, value=OB.ZONA_OBIETTIVO.get(z, "")); c.font = BLU; c.fill = GIALLO
    c = wp.cell(row=r, column=5, value=passo); c.font = BLU; c.fill = GIALLO; c.number_format = '0.00'
    wp.cell(row=r, column=6, value=un).font = BODY
    wp.cell(row=r, column=7, value=(f'=IF($E{r}="","",60/$E{r})' if un == "min/km" else "-")).font = BODY
    wp.cell(row=r, column=7).number_format = '0.0'
    wp.cell(row=r, column=8, value=f'=IF($E{r}="","",TEXT($E{r}/1440,"mm:ss"))').font = BODY
    for j in range(1, 9):
        wp.cell(row=r, column=j).border = BRD
        wp.cell(row=r, column=j).alignment = Alignment(vertical="center",
            horizontal="left" if j in (1,2,3,4,6) else "center")
    r += 1
ZFIRST, ZLAST = 6, r-1
for i_, w in enumerate([22,16,52,30,10,14,16,14], 1):
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
        "Struttura sessione","Note","Testo originale"]
LARG = [11,16,7,30,10,18,8,11,15,22,14,14,8,26,11,13,13,13,16,20,12,9,14,14,12,9,11,9,13,30,60,34,100]
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
        ws.cell(row=k, column=21, value=f'=IFERROR(INDEX({PAR}!$F${ZFIRST}:$F${ZLAST},MATCH($T{k},{PAR}!$A${ZFIRST}:$A${ZLAST},0)),"")')
        c = ws.cell(row=k, column=22, value=f'=IFERROR(INDEX({PAR}!$E${ZFIRST}:$E${ZLAST},MATCH($T{k},{PAR}!$A${ZFIRST}:$A${ZLAST},0)),"")')
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
    ws.cell(row=k, column=31, value=b["struttura"])
    ws.cell(row=k, column=32, value=fix(b["nota"]) if b["nota"] else None)
    ws.cell(row=k, column=33, value=fix(b["testo"]))
    for j in range(1, NC+1):
        c = ws.cell(row=k, column=j)
        c.font = BODY; c.border = BRD
        c.alignment = Alignment(vertical="top", wrap_text=(j in (31,32,33)))
        if j in (1,5,7,11,13,15,16,17,18,23,24,25,26,27,28):
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

NUOVI = ("Legenda","Parametri Atleta","Struttura Allenamento","Controllo Sessioni","Tassonomia Obiettivi","Catalogo Archetipi","Catalogo Allenamenti")
ordine = [n for n in wb.sheetnames if n not in NUOVI] + \
         ["Parametri Atleta","Tassonomia Obiettivi","Catalogo Archetipi","Catalogo Allenamenti",
          "Struttura Allenamento","Controllo Sessioni","Legenda"]
wb._sheets = [wb[n] for n in ordine]

out = "/mnt/user-data/outputs/Piani_Triathlon_Sprint_Olimpico_Half-Ironman_Ironman.xlsx"
wb.save(out)
print("salvato | blocchi:", len(righe), "| sessioni:", len(sessioni), "| archetipi:", len(ARCH_INFO), "| varianti:", len(varianti))
