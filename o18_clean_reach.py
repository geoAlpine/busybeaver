# o18 CLEANUP task 2b (2026-07-08): (i) does the 97-pass fatal witness survive under
# the corrected transducer T_ext?  (edge-by-edge re-application + final-cell HALT);
# (ii) re-run the exact adversarial reachability of o18_inv_reach.py with T_ext:
# how many reachable HALT cells / Unknown cells remain (base run: 491 HALTs, 517
# Unknowns on the 3M-state budget-capped closure)?
import sys, pickle
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown
from o18_md_rules_ext import T_ext
from o18_inv_reach import waiting2
from collections import deque

SCR = '/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/8b7a3f39-ce4e-4044-afe8-60ce3b3aedcf/scratchpad'

def witness_check():
    with open(SCR + '/witness_path.pkl', 'rb') as f:
        words, residues = pickle.load(f)
    print(f'witness: {len(words)} words, {len(residues)} passes')
    nagree = ndiff = 0
    for i in range(len(words) - 1):
        r, w = residues[i], words[i]
        a = T(r, w)
        try:
            b = T_ext(r, w)
        except Unknown as u:
            print(f'  edge {i}: T_ext Unknown {u.args[0]} (base was {a})'); ndiff += 1
            continue
        if b != a:
            print(f'  edge {i}: base {a}  !=  ext {b}'); ndiff += 1
            continue
        if b[0] != 'MOVE' or b[2] != words[i + 1]:
            print(f'  edge {i}: ext does not reproduce the path edge: {b}'); ndiff += 1
            continue
        nagree += 1
    fa = T(residues[-1], words[-1])
    fb = T_ext(residues[-1], words[-1])
    print(f'  edges where T_ext == base T == path edge: {nagree}/{len(words)-1}; '
          f'differences: {ndiff}')
    print(f'  final fatal cell (r={residues[-1]}, {words[-1]}): base {fa}  ext {fb}  '
          f'{"-- HALT under BOTH" if fa[0] == fb[0] == "HALT" else "-- MISMATCH!"}')
    return ndiff == 0 and fa[0] == fb[0] == 'HALT'

def reach(TT, starts, maxlen=14, maxb=60, maxs=6, maxstates=3_000_000):
    seen = set(starts)
    q = deque(starts)
    escapes = nland = 0
    halts, unks = [], []
    nw2 = 0
    while q and len(seen) < maxstates:
        w = q.popleft()
        for r in (0, 1, 2):
            try:
                res = TT(r, w)
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
                q.append(w2)
                if waiting2(w2):
                    nw2 += 1
    return seen, escapes, halts, unks, nw2, nland, len(q)

if __name__ == '__main__':
    print('=== (i) 97-pass witness under T_ext ===')
    ok = witness_check()
    print(f'WITNESS SURVIVES UNDER T_ext: {"YES" if ok else "NO"}')

    print('\n=== (ii) adversarial reachability from the exit cone under T_ext ===', flush=True)
    starts = []
    for t in range(1, 12):
        starts.append(((1, 2 * t + 2), (1, 6)))
    starts.append(((1, 4), (1, 1), (1, 1), (1, 1)))
    for t in range(0, 9):
        for e in range(1, 25):
            starts.append(((1, 1),) * t + ((1, e),))
    seen, escapes, halts, unks, nw2, nland, qrem = reach(T_ext, starts)
    print(f'reachable exact words: {len(seen)} (queue remaining {qrem}); LAND edges {nland}')
    print(f'escapes: {escapes}')
    hcells = sorted(set(halts))
    ucells = sorted(set((r, w) for r, w, _ in unks))
    print(f'reachable HALT cells: {len(hcells)}  (base run: 491)')
    print(f'reachable Unknown cells: {len(ucells)}  (base run: 517)')
    from collections import Counter
    ucen = Counter(str(u[2]) for u in unks)
    for k, v in sorted(ucen.items()):
        print(f'   UNK {k}: {v}')
    for h in hcells[:8]:
        print('   HALT cell: r=%d %s' % h)
    with open(SCR + '/o18_clean_reach.pkl', 'wb') as f:
        pickle.dump({'halts': hcells, 'unks': ucells, 'nseen': len(seen),
                     'escapes': escapes, 'nw2': nw2}, f)
