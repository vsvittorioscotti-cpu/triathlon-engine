import sys
from collections import defaultdict
QUI='/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad'
sys.path.insert(0, QUI)
import parser as P, scala2

GIORNI=['Lunedi','Martedi','Mercoledi','Giovedi','Venerdi','Sabato','Domenica']
ORD=['Triathlon Sprint','Triathlon Olimpico','Half-Ironman','Ironman']
PESI_MIN=45.0   # ASSUNZIONE NOSTRA: il libro non da' la durata delle sedute di pesi

righe=P.analizza()[0]
sess=defaultdict(list)
for r in righe: sess[r['sid']].append(r)
S=[]
for sid,bs in sess.items():
    s=bs[0]['sess']
    if s['disc']=='Riposo': continue
    if s['disc']=='Pesi':
        foc=' '.join(sorted({r['tipo'] for r in bs if r['tipo'].startswith('Pesi')}))
        S.append(dict(piano=s['piano'],sett=s['sett'],giorno=s['giorno'],disc='Pesi',
                      min=PESI_MIN,focus=s['focus'],tipo=foc,fase=s['fase'])); continue
    fatt=scala2.FATT.get(s['disc']); t=0.0; d_tot=0.0; res=False
    for r in bs:
        z=r.get('zona'); rip=r.get('rip') or 1
        if r.get('modo')=='residuo': res=True; continue
        if z not in scala2.PASSI or fatt is None: continue
        p=scala2.PASSI[z]
        if r.get('dist') is not None: d=rip*r['dist']; dt=d/fatt*p
        elif r.get('dur_a') is not None: dt=rip*(r['dur_a']+(r['dur_b'] or r['dur_a']))/2; d=dt/p*fatt
        else: continue
        t+=dt
        if r.get('nel_totale',True): d_tot+=d
    ob=bs[0].get('ob_m')
    if res and ob: t+=max(0.0,ob-d_tot)/fatt*scala2.PASSI[scala2.SUPPL[s['disc']]]
    S.append(dict(piano=s['piano'],sett=s['sett'],giorno=s['giorno'],disc=s['disc'],
                  min=t,focus=s['focus'],tipo='',fase=s['fase']))

W=defaultdict(list)
for x in S: W[(x['piano'],x['sett'])].append(x)

print("="*78); print("R1 - la forza sta DENTRO il monte ore settimanale")
dentro=sum(1 for k,v in W.items() if any(x['disc']=='Pesi' for x in v))
print(f"  settimane con almeno una seduta di pesi: {dentro}/{len(W)}")
print("  Le sedute di pesi compaiono nello stesso prospetto settimanale delle tre discipline,")
print("  con giorno assegnato: nel libro non sono un extra fuori conteggio.  -> CONFERMATA")

print("="*78); print("R2 - due sedute di forza a settimana")
for pi in ORD:
    c=[sum(1 for x in W[(pi,w)] if x['disc']=='Pesi') for w in sorted({k[1] for k in W if k[0]==pi})]
    from collections import Counter
    print(f"  {pi:<20}{dict(sorted(Counter(c).items()))}   media {sum(c)/len(c):.1f}")

print("="*78); print("R3 - periodizzazione inversa: forza alta in base, bassa verso la gara")
for pi in ORD:
    ws=sorted({k[1] for k in W if k[0]==pi}); n=len(ws)
    q1=[sum(1 for x in W[(pi,w)] if x['disc']=='Pesi') for w in ws[:n//2]]
    q2=[sum(1 for x in W[(pi,w)] if x['disc']=='Pesi') for w in ws[n//2:]]
    ult=sum(1 for x in W[(pi,ws[-1])] if x['disc']=='Pesi')
    print(f"  {pi:<20}prima meta {sum(q1)/len(q1):.1f}/sett   seconda meta {sum(q2)/len(q2):.1f}/sett   ultima settimana {ult}")

print("="*78); print("R4 - niente forza il giorno PRIMA della seduta piu lunga")
tot=viol=0
for (pi,w),v in W.items():
    lungo=max(v,key=lambda x:x['min'])
    if lungo['disc']=='Pesi': continue
    i=GIORNI.index(lungo['giorno']); prima=GIORNI[(i-1)%7]
    tot+=1
    if any(x['disc']=='Pesi' for x in v if x['giorno']==prima): viol+=1
print(f"  settimane esaminate: {tot}   con pesi in vigilia del lungo: {viol}  ({viol/tot*100:.0f}%)")

print("="*78); print("R5 - la pliometria non cade dopo il lungo o su gambe affaticate")
pl=[x for x in S if x['disc']=='Pesi' and ('otenza' in x['focus'] or 'otenza' in x['tipo'])]
print(f"  sedute di pesi con lavoro di potenza/esplosivo: {len(pl)}")
dopo=0
for x in pl:
    v=W[(x['piano'],x['sett'])]
    lungo=max(v,key=lambda y:y['min'])
    i=GIORNI.index(lungo['giorno'])
    if x['giorno']==GIORNI[(i+1)%7]: dopo+=1
print(f"  di queste, il giorno DOPO il lungo: {dopo}")

print("="*78); print("R6 - hard days hard: la forza si attacca a giorni gia impegnativi")
pg=[]; ng=[]
for (pi,w),v in W.items():
    for g in GIORNI:
        gg=[x for x in v if x['giorno']==g]
        if not gg: continue
        altro=sum(x['min'] for x in gg if x['disc']!='Pesi')
        (pg if any(x['disc']=='Pesi' for x in gg) else ng).append(altro)
print(f"  minuti di endurance nei giorni CON pesi:   {sum(pg)/len(pg):6.0f}'  (n={len(pg)})")
print(f"  minuti di endurance nei giorni SENZA pesi: {sum(ng)/len(ng):6.0f}'  (n={len(ng)})")

print("="*78); print("R9 - la quota di forza scende al crescere del volume settimanale")
print("  ATTENZIONE: dipende dall'assunzione di 45' per seduta, che il libro non da'.")
bande=[(0,7,'<= 7 h','15-20%'),(7,12,'8-12 h','10-15%'),(12,16,'13-16 h','7-10%'),(16,99,'> 16 h','5-8%')]
agg=defaultdict(list)
for (pi,w),v in W.items():
    ore=sum(x['min'] for x in v)/60
    pes=sum(x['min'] for x in v if x['disc']=='Pesi')
    for lo,hi,nome,att in bande:
        if lo<=ore<hi: agg[nome].append(pes/max(sum(x['min'] for x in v),1)*100)
for lo,hi,nome,att in bande:
    q=agg.get(nome,[])
    if q: print(f"  {nome:<10}atteso {att:<9}misurato {sum(q)/len(q):4.1f}%   (n={len(q)} settimane)")

print("="*78); print("R10 - 48 ore fra forza pesante e sessione chiave di corsa")
tot=viol=0
for (pi,w),v in W.items():
    gp=[GIORNI.index(x['giorno']) for x in v if x['disc']=='Pesi']
    for x in v:
        if x['disc']!='Corsa a piedi': continue
        if x['min'] < max(y['min'] for y in v if y['disc']=='Corsa a piedi'): continue
        i=GIORNI.index(x['giorno']); tot+=1
        if any((i-g)%7==1 for g in gp): viol+=1
print(f"  corse chiave esaminate: {tot}   precedute il giorno prima da pesi: {viol}  ({viol/tot*100:.0f}%)")
