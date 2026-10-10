import sys, json
from collections import defaultdict
sys.path.insert(0,'/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad')
import parser as P
PASSI = json.load(open('/tmp/claude-0/-home-claude/9a4d6698-6b4d-546b-bf93-5a7477a0c384/scratchpad/soglie.json'))['PASSI']
FATT  = {"Nuoto":100, "Corsa a piedi":1000, "Ciclismo":1000}
SUPPL = {"Nuoto":"nuoto_aerobico", "Corsa a piedi":"corsa_aerobica", "Ciclismo":"bici_aerobica"}
PESI_MIN = 45.0

righe = P.analizza()[0]
sess = defaultdict(list)
for r in righe: sess[r['sid']].append(r)

sett = defaultdict(float); conta = defaultdict(int)
for sid, bs in sess.items():
    s = bs[0]['sess']; disc = s['disc']; key = (s['piano'], s['sett'])
    if disc == 'Riposo': continue
    if disc == 'Pesi':
        sett[key] += PESI_MIN; conta[key] += 1; continue
    fatt = FATT.get(disc); tempo = 0.0; dist_tot = 0.0; residui = []
    for r in bs:
        z = r.get('zona'); rip = r.get('rip') or 1
        if r.get('modo') == 'residuo':
            residui.append(r); continue
        if z not in PASSI or fatt is None: continue
        p = PASSI[z]
        if r.get('dist') is not None:
            d = rip * r['dist']; t = d / fatt * p
        elif r.get('dur_a') is not None:
            t = rip * (r['dur_a'] + (r['dur_b'] or r['dur_a'])) / 2; d = t / p * fatt
        else:
            continue
        tempo += t
        if r.get('nel_totale', True): dist_tot += d
    ob = bs[0].get('ob_m')
    if residui and ob:
        d = max(0.0, ob - dist_tot)
        tempo += d / fatt * PASSI[SUPPL[disc]]
    sett[key] += tempo; conta[key] += 1

ORD = ['Triathlon Sprint','Triathlon Olimpico','Half-Ironman','Ironman']
cum = 0
print(f"{'Piano':<20}{'sett':>5}{'cum':>5}{'ore/sett':>10}{'picco':>8}{'tot h':>8}{'cum h':>8}")
cumh = 0
for pi in ORD:
    ws = sorted(k[1] for k in sett if k[0]==pi)
    ore = [sett[(pi,w)]/60.0 for w in ws]
    cum += len(ws); cumh += sum(ore)
    print(f"{pi:<20}{len(ws):>5}{cum:>5}{sum(ore)/len(ore):>10.1f}{max(ore):>8.1f}{sum(ore):>8.0f}{cumh:>8.0f}")
print()
for pi in ORD:
    ws = sorted(k[1] for k in sett if k[0]==pi)
    print(f"{pi:<20}" + " ".join(f"{sett[(pi,w)]/60.0:.1f}" for w in ws))
