# o18 INVARIANT SYNTHESIS step 4b: EXACT null-model halt probability by DP.
# p(w) = P[uniform-random residue walk from w hits HALT before LAND], computed by value
# iteration on the exact bounded reachable graph.  Universe escapes are censored BOTH ways:
#   lower bound: escaped mass counts as LAND (p_esc = 0)
#   upper bound: escaped mass counts as HALT (p_esc = 1)
# giving rigorous two-sided bounds on the per-excursion halting probability of the
# uniform-itinerary null model ("probviously halting" made quantitative on the word grammar).
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown
from collections import deque

def build(starts, maxlen=14, maxb=60, maxs=6, maxstates=3_000_000):
    idx = {}
    trans = []   # per state: list of 3 outcomes: ('L',)/('H',)/('E',)/('S', j)/('U',)
    q = deque()
    def get(w):
        if w not in idx:
            idx[w] = len(trans)
            trans.append(None)
            q.append(w)
        return idx[w]
    for w in starts:
        get(w)
    while q:
        w = q.popleft()
        i = idx[w]
        if trans[i] is not None:
            continue
        out = []
        for r in (0, 1, 2):
            try:
                res = T(r, w)
            except Unknown:
                out.append(('U',)); continue
            if res[0] == 'HALT':
                out.append(('H',)); continue
            if res[0] == 'LAND':
                out.append(('L',)); continue
            w2 = res[2]
            if len(w2) > maxlen or any(b > maxb or s > maxs for s, b in w2):
                out.append(('E',)); continue
            if len(idx) >= maxstates and w2 not in idx:
                out.append(('E',)); continue
            out.append(('S', get(w2)))
        trans[i] = out
    return idx, trans

def solve(trans, esc_val, unk_val, iters=3000, tol=1e-40):
    """Vectorized value iteration: p = (base + sum over successor slots of p[succ])/3."""
    import numpy as np
    n = len(trans)
    base = np.zeros(n)
    # successor slots: 3 per state; use index n as a sink with p=0
    succ = np.full((n, 3), n, dtype=np.int64)
    for i, out in enumerate(trans):
        for k, o in enumerate(out):
            if o[0] == 'H':
                base[i] += 1.0
            elif o[0] == 'E':
                base[i] += esc_val
            elif o[0] == 'U':
                base[i] += unk_val
            elif o[0] == 'S':
                succ[i, k] = o[1]
    p = np.zeros(n + 1)
    for it in range(iters):
        newp = (base + p[succ].sum(axis=1)) / 3.0
        delta = np.max(np.abs(newp - p[:n]))
        p[:n] = newp
        if delta < tol:
            return p[:n], it
    return p[:n], iters

if __name__ == '__main__':
    starts = [((1, 2 * t + 2), (1, 6)) for t in range(1, 12)]
    starts.append(((1, 4), (1, 1), (1, 1), (1, 1)))
    idx, trans = build(starts)
    n = len(trans)
    nesc = sum(1 for t in trans for o in t if o[0] == 'E')
    nhalt = sum(1 for t in trans for o in t if o[0] == 'H')
    nunk = sum(1 for t in trans for o in t if o[0] == 'U')
    print(f'graph: {n} states; HALT edges {nhalt}, escape edges {nesc}, unknown edges {nunk}')
    plo, it1 = solve(trans, esc_val=0.0, unk_val=0.0)
    phi, it2 = solve(trans, esc_val=1.0, unk_val=1.0)
    print(f'value iteration: {it1}/{it2} sweeps')
    print('per-excursion halt probability under the uniform-itinerary null model:')
    for w in starts:
        i = idx[w]
        print(f'  {str(w)[:44]:46s}  p in [{plo[i]:.3e}, {phi[i]:.3e}]')
    lo = min(plo[idx[w]] for w in starts)
    hi = max(phi[idx[w]] for w in starts)
    print(f'\nbounds over the cone: [{lo:.3e}, {hi:.3e}]')
    if lo > 0:
        print(f'null-model generations to halt: ~[{1/hi:.3e}, {1/lo:.3e}]  '
              f'(true orbit: 122,015 clean generations so far)')
