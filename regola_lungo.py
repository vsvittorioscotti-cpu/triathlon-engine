import sys, json
from collections import defaultdict
QUI='/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad'
sys.path.insert(0, QUI)
import parser as P, scala2   # scala2 ricalcola i minuti col blocco residuo

GIORNI=['Lunedi','Martedi','Mercoledi','Giovedi','Venerdi','Sabato','Domenica']

# --- minuti per seduta, riusando la logica corretta di scala2 ---
righe = P.analizza()[0]
sess = defaultdict(list)
for r in righe: sess[r['sid']].append(r)
minuti_sess = {}
for sid, bs in sess.items():
    s = bs[0]['sess']
    if s['disc'] == 'Riposo': continue
    if s['disc'] == 'Pesi': minuti_sess[sid] = (s, 45.0); continue
    fatt = scala2.FATT.get(s['disc']); tempo = 0.0; dist_tot = 0.0; res = False
    for r in bs:
        z = r.get('zona'); rip = r.get('rip') or 1
        if r.get('modo') == 'residuo': res = True; continue
        if z not in scala2.PASSI or fatt is None: continue
        p = scala2.PASSI[z]
        if r.get('dist') is not None: d = rip*r['dist']; t = d/fatt*p
        elif r.get('dur_a') is not None:
            t = rip*(r['dur_a']+(r['dur_b'] or r['dur_a']))/2; d = t/p*fatt
        else: continue
        tempo += t
        if r.get('nel_totale', True): dist_tot += d
    ob = bs[0].get('ob_m')
    if res and ob: tempo += max(0.0, ob-dist_tot)/fatt*scala2.PASSI[scala2.SUPPL[s['disc']]]
    minuti_sess[sid] = (s, tempo)

# --- giorno del lungo, e peso del giorno prima / dopo ---
giorno_min = defaultdict(float); lungo = {}
for sid,(s,t) in minuti_sess.items():
    k=(s['piano'], s['sett'])
    giorno_min[(k, s['giorno'])] += t
    if t > lungo.get(k,(0,None,None))[0]: lungo[k]=(t, s['giorno'], s['disc'])

print("REGOLA 1 — il giorno prima del lungo e' il piu' leggero?")
print(f"{'piano':<20}{'sett':>5}{'lungo':>22}{'prima':>9}{'dopo':>9}{'media gg':>10}  verdetto")
ok=tot=0; dopo_piu=0
for (pi,se),(t,g,d) in sorted(lungo.items()):
    i=GIORNI.index(g)
    prima=giorno_min.get(((pi,se),GIORNI[(i-1)%7]),0.0)
    dopo =giorno_min.get(((pi,se),GIORNI[(i+1)%7]),0.0)
    altri=[giorno_min.get(((pi,se),x),0.0) for x in GIORNI if x!=g]
    med=sum(altri)/len(altri)
    v = prima <= med
    ok+=v; tot+=1; dopo_piu += (dopo>med)
    if se in (1,7,12,16) or (pi=='Ironman' and se<=3):
        print(f"{pi:<20}{se:5d}{g+' '+d:>22}{prima:8.0f}'{dopo:8.0f}'{med:9.0f}'  {'si' if v else 'NO'}")
print(f"\n  giorno prima piu' leggero della media: {ok}/{tot} settimane ({ok/tot*100:.0f}%)")
print(f"  giorno dopo piu' PESANTE della media:  {dopo_piu}/{tot} settimane ({dopo_piu/tot*100:.0f}%)")

# --- REGOLA 3: crescita del lungo settimana su settimana nel piano generato ---
print("\nREGOLA 3 — crescita del lungo nel piano generato (52 sett., tetto 16 h)")
d=json.load(open(QUI+'/o52.json'))
lg=defaultdict(float)
for p in d['PIANO']:
    if p['disc']=='Ciclismo': lg[p['w']]=max(lg[p['w']], p['tempo'])
W={x['w']:x for x in d['W']}
salti=[]
for w in sorted(lg):
    if w-1 in lg and lg[w-1]>0 and W[w]['tipo']=='Carico' and W[w-1]['tipo']=='Carico':
        g=(lg[w]/lg[w-1]-1)*100
        if g>15: salti.append((w, lg[w-1], lg[w], g))
print(f"  lungo massimo: {max(lg.values()):.0f}' alla settimana {max(lg,key=lg.get)}")
print(f"  salti oltre il +15% fra settimane di carico consecutive: {len(salti)}")
for w,a,b,g in salti[:8]: print(f"    sett {w}: {a:.0f}' -> {b:.0f}'  (+{g:.0f}%)")
