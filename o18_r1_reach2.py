# o18 R1-PINNING step 4: re-run the EXACT adversarial reachability closure of the exit
# cone (same starts / caps / budget / BFS order as o18_inv_reach.py) under the EXTENDED
# transducer T_ext.  Questions:
#   (1) how many HALT cells now?  (new fatal cells = cells that were Unknown under T)
#   (2) how many Unknown cells remain (the residual frontier), and where do they raise?
#   (3) does the reachable set change qualitatively (size, LANDs, escapes, censuses)?
import sys, pickle
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown
from o18_md_rules_ext import T_ext
from o18_inv_attractor import units_split
from o18_r1_enum import starts_cone
from collections import deque, Counter

SCR = '/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/8b7a3f39-ce4e-4044-afe8-60ce3b3aedcf/scratchpad'

def reach_ext(starts, maxlen=14, maxb=60, maxs=6, maxstates=3_000_000):
    seen = set(starts)
    par = {w: None for w in starts}
    q = deque(starts)
    escapes = nland = 0
    halts, unks = [], []
    while q and len(seen) < maxstates:
        w = q.popleft()
        for r in (0, 1, 2):
            try:
                res = T_ext(r, w)
            except Unknown as u:
                unks.append((r, w, u.args[0]))
                continue
            if res[0] == 'HALT':
                halts.append((r, w))
                continue
            if res[0] == 'LAND':
                nland += 1
                continue
            w2 = res[2]
            if len(w2) > maxlen or any(b > maxb or s > maxs for s, b in w2):
                escapes += 1
                continue
            if w2 not in seen:
                seen.add(w2)
                par[w2] = (w, r)
                q.append(w2)
    return seen, par, escapes, halts, unks, nland, len(q)

def trace(par, w):
    path = []
    while w is not None:
        pr = par.get(w)
        if pr is None:
            path.append((None, w)); break
        path.append((pr[1], w)); w = pr[0]
    return list(reversed(path))

if __name__ == '__main__':
    starts = starts_cone()
    seen, par, escapes, halts, unks, nland, qrem = reach_ext(starts)
    print(f'[T_ext] reachable exact words: {len(seen)} (queue remaining {qrem}); '
          f'LAND {nland}; escapes {escapes}')
    print(f'[T_ext] HALT cells reached: {len(halts)}   Unknown cells: {len(unks)}')
    # which HALT cells are NEW (Unknown or unreached under the base T)?
    new_halts = []
    for r, w in halts:
        try:
            base = T(r, w)
            is_new = False
        except Unknown:
            is_new = True
        if is_new:
            new_halts.append((r, w))
    print(f'[T_ext] HALT cells that were Unknown under base T: {len(new_halts)}')
    for r, w in new_halts[:12]:
        print(f'   NEW-FATAL r={r} w={w}')
    if new_halts:
        r, w = new_halts[0]
        print('   sample adversarial path to first new fatal cell:')
        for st in trace(par, w):
            print('     ', st)
    from o18_md_rules import units
    hj = Counter()
    for r, w in new_halts:
        hj[(r, units(w))] += 1
    print('   new-fatal (r, lead-units) census:', dict(sorted(hj.items())))
    unkc = Counter((t if isinstance(t, str) else t[0]) for _, _, t in unks)
    print(f'[T_ext] residual Unknown raise-sites:', dict(unkc))
    for u in unks[:10]:
        print('   UNK', u)
    # qualitative censuses (compare against o18_inv_reach.py output)
    sepc, tailv = Counter(), Counter()
    for w in seen:
        blocks = [x for x in units_split(w) if x[0] != 'U']
        for s, b in blocks:
            sepc[s] += 1
        for s, b in blocks[1:]:
            tailv[b if b <= 12 else 'big%d' % (b % 3)] += 1
    print('separator census:', dict(sepc))
    print('tail-value census:', dict(sorted(tailv.items(), key=str)))
    with open(SCR + '/o18_r1_reach2.pkl', 'wb') as f:
        pickle.dump({'halts': halts, 'unks': unks, 'new_halts': new_halts,
                     'traces_new': {w: trace(par, w) for _, w in new_halts}}, f)
    print('dumped ->', SCR + '/o18_r1_reach2.pkl')
