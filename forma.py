import sys, json
from collections import defaultdict
QUI='/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad'
sys.path.insert(0, QUI)
import parser as P, scala2

righe = P.analizza()[0]
sess = defaultdict(list)
for r in righe: sess[r['sid']].append(r)

S = []   # (piano, sett, disc, minuti)
for sid, bs in sess.items():
    s = bs[0]['sess']
    if s['disc'] == 'Riposo': continue
    if s['disc'] == 'Pesi': S.append((s['piano'], s['sett'], 'Pesi', 45.0)); continue
    fatt = scala2.FATT.get(s['disc']); t = 0.0; dist = 0.0; res = False
    for r in bs:
        z = r.get('zona'); rip = r.get('rip') or 1
        if r.get('modo') == 'residuo': res = True; continue
        if z not in scala2.PASSI or fatt is None: continue
        p = scala2.PASSI[z]
        if r.get('dist') is not None: d = rip*r['dist']; dt = d/fatt*p
        elif r.get('dur_a') is not None:
            dt = rip*(r['dur_a']+(r['dur_b'] or r['dur_a']))/2; d = dt/p*fatt
        else: continue
        t += dt
        if r.get('nel_totale', True): dist += d
    ob = bs[0].get('ob_m')
    if res and ob: t += max(0.0, ob-dist)/fatt*scala2.PASSI[scala2.SUPPL[s['disc']]]
    S.append((s['piano'], s['sett'], s['disc'], t))

ORD = ['Triathlon Sprint','Triathlon Olimpico','Half-Ironman','Ironman']
print(f"{'Piano':<20}{'ore/sett':>9}{'sedute':>8}{'durata media':>14}{'piu lunga':>11}{'quota':>8}{'lungo bici':>12}{'lungo corsa':>13}")
for pi in ORD:
    W = sorted({w for p,w,_,_ in S if p == pi})
    ore=[]; n=[]; med=[]; lung=[]; quota=[]; lb=[]; lc=[]
    for w in W:
        ss=[(d,t) for p,x,d,t in S if p==pi and x==w]
        tot=sum(t for _,t in ss)
        if not ss or tot==0: continue
        ore.append(tot/60); n.append(len(ss)); med.append(tot/len(ss))
        mx=max(t for _,t in ss); lung.append(mx); quota.append(mx/tot*100)
        b=[t for d,t in ss if d=='Ciclismo']; c=[t for d,t in ss if d=='Corsa a piedi']
        if b: lb.append(max(b))
        if c: lc.append(max(c))
    f=lambda v: sum(v)/len(v)
    print(f"{pi:<20}{f(ore):9.1f}{f(n):8.1f}{f(med):13.0f}'{f(lung):10.0f}'{f(quota):7.0f}%{max(lb):11.0f}'{max(lc):12.0f}'")
