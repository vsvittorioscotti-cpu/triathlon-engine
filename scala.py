import sys, json
sys.path.insert(0,'/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad')
import parser as P
S = json.load(open('/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad/soglie.json'))
PASSI = S['PASSI']
PESI_MIN = 45.0

def minuti(r):
    if r['tipo'].startswith('Pesi'):
        return 0.0            # contati a parte, una volta per seduta
    if not r.get('nel_totale'):
        return 0.0
    z = r.get('zona'); 
    if r.get('modo') == 'tempo':
        a, b = r.get('dur_a'), r.get('dur_b')
        if a is None: return 0.0
        return (a + (b if b else a)) / 2.0 * (r.get('rip') or 1)
    if r.get('modo') == 'distanza' and r.get('dist') and z in PASSI:
        d = r['dist'] * (r.get('rip') or 1)
        p = PASSI[z]
        disc = r['sess']['disc']
        return d/100.0*p if disc == 'Nuoto' else d/1000.0*p
    return 0.0

righe = P.analizza()[0]
sett = {}
pesi_sess = set()
for r in righe:
    s = r['sess']; k = (s['piano'], s['sett'])
    sett[k] = sett.get(k, 0.0) + minuti(r)
    if r['tipo'].startswith('Pesi'):
        pesi_sess.add((s['piano'], s['sett'], r['sid']))
for (pi, se, _) in pesi_sess:
    sett[(pi, se)] = sett.get((pi, se), 0.0) + PESI_MIN

ORD = ['Triathlon Sprint','Triathlon Olimpico','Half-Ironman','Ironman']
cum = 0
print(f"{'Piano':<20}{'sett':>5}{'cum':>5}{'ore medie':>11}{'ore picco':>11}{'ore tot':>9}")
for pi in ORD:
    ws = sorted(k[1] for k in sett if k[0]==pi)
    ore = [sett[(pi,w)]/60.0 for w in ws]
    cum += len(ws)
    print(f"{pi:<20}{len(ws):>5}{cum:>5}{sum(ore)/len(ore):>11.1f}{max(ore):>11.1f}{sum(ore):>9.0f}")
print()
for pi in ORD:
    ws = sorted(k[1] for k in sett if k[0]==pi)
    print(f"{pi:<20}" + " ".join(f"{sett[(pi,w)]/60.0:.1f}" for w in ws))
