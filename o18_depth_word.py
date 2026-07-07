# o18 general DEFECT-WORD machine probe.
# Every F-entry config is  0^inf [F] 1^m 0 w 0^inf  where w = 1^{c1} 0 1^{c2} 0 ... 0 1^{ck}
# encoded as the integer list [c1,...,ck] (single-0 separators; all observed defects are single 0s).
# Single-defect family D(m,t,e) = [1]*t + [e].  This script probes the transition
# (m, w) -> (m', w') for GENERAL w, testing the prefix-locality hypothesis:
#   the rewrite depends only on m mod 3 and a bounded/structured prefix of w,
#   with the remainder X carried over inert.
# Pure-table (grid-verified in o18_depth_map.py):
#   m=0 (3): w=1^t+[e], e%3!=2 -> CLEAN LAND L=(8m+8e+6t+{10 if e%3==1 else 12})/3
#            w=1^t+[e], e%3==2 -> (m,w) -> ((8m+8e+6t-19)/3, [6])          [FLUSH]
#   m=1 (3): w=1^j (all units) -> ((8m-17)/3, [2j+6])                      [RECYCLE]
#            w=1^j+[v>=3]+X    -> ((8m-5)/3, 1^{j+2}+[v-3 if v>3]+X)       [PUSH]
#            w=1^j+[2]+X, j>=1 -> ((8m-17)/3, [2j+2]+?)                    [EXIT2]
#            w=[2]+X           -> ((8m-23)/3, [4,1,1,1]+?)                 [EXIT2a]
#   m=2 (3): w=[1]+X           -> ((8m+14)/3, X)                           [POP]
#            w=[a>=2] (only)   -> CLEAN LAND L=(8m+3a+14)/3                [LAND2]
#            w=[a>=2]+X        -> ((8m+3a+11)/3, X)?                       [MERGE?]
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_depth_map import run_cfg

def blocks_of(w):
    b = [(1, w[0])]
    for c in w[1:]:
        b += [(0, 1), (1, c)]
    return b

def parse_list(R, hp):
    """RLE -> (m, [c...]) if form is 1^m (0 1^ci)* with single-0 separators, head@-1."""
    if hp != -1 or not R or R[0][0] != 1:
        return None
    vals = []
    expect_one = True
    for b, c in R:
        if expect_one:
            if b != 1: return None
            vals.append(c)
        else:
            if b != 0 or c != 1: return None
        expect_one = not expect_one
    if expect_one:  # ended on a 0-run (expecting a 1-run next) -> not a valid word
        return None
    return vals

def probe_w(m, w, maxF=3, budget=None):
    blocks = [(1, m)] + ([(0, 1)] + blocks_of(w) if w else [])
    status, fents, steps, unsafe = run_cfg(blocks, maxF=maxF, budget=budget)
    if status == 'HALT':
        return ('HALT', steps, unsafe, None)
    for (s, clean, land, R, hp) in fents:
        if clean:
            return ('LAND', s, unsafe, land)
        vals = parse_list(R, hp)
        if vals is not None:
            return ('MOVE', s, unsafe, (vals[0], vals[1:]))
        if len(R) >= 2 and R[0] == (1, 2) and hp > 0:
            continue  # interior meet form, keep going
        return ('UNPARSED', s, unsafe, (R, hp))
    return (status, steps, unsafe, None)

def predict(m, w):
    """Prefix-locality prediction; None = no prediction."""
    r = m % 3
    if not w:
        return None
    j = 0
    while j < len(w) and w[j] == 1:
        j += 1
    allunits = (j == len(w))
    if r == 1:
        if allunits:
            return ('MOVE', ((8 * m - 17) // 3, [2 * j + 6]))
        v, X = w[j], w[j + 1:]
        if v >= 3:
            nw = [1] * (j + 2) + ([v - 3] if v > 3 else []) + X
            return ('MOVE', ((8 * m - 5) // 3, nw))
        return None  # v == 2: to be learned
    if r == 2:
        if w[0] == 1:
            return ('MOVE', ((8 * m + 14) // 3, w[1:]))
        if len(w) == 1:
            return ('LAND', (8 * m + 3 * w[0] + 14) // 3)
        return ('MOVE', ((8 * m + 3 * w[0] + 11) // 3, w[1:]))  # MERGE hypothesis
    # r == 0
    if allunits:
        return None
    v, X = w[j], w[j + 1:]
    if not X:
        if v % 3 != 2:
            return ('LAND', (8 * m + 8 * v + 6 * j + (10 if v % 3 == 1 else 12)) // 3)
        return ('MOVE', ((8 * m + 8 * v + 6 * j - 19) // 3, [6]))
    return None  # multi-block with m=0 mod 3: to be learned

if __name__ == '__main__':
    tests = [
        # two-block words: near a, far 6 (the reachable EXIT2 products) and variants
        [4, 6], [6, 6], [8, 6], [10, 6], [5, 6], [3, 6], [7, 6], [9, 6],
        # unit-train prefixed two-block
        [1, 4, 6], [1, 1, 4, 6], [1, 6, 6], [1, 1, 8, 6],
        # EXIT2a product
        [4, 1, 1, 1],
        # e=2 with rest
        [2, 6], [1, 2, 6], [1, 1, 2, 6],
        # far tails beyond first non-unit (push locality)
        [1, 3, 5], [1, 5, 6], [3, 3], [5, 5], [1, 1, 3, 4, 6],
        # pop with general rest
        [1, 4, 1, 1, 3], [1, 9, 8],
        # merge with longer rest
        [4, 1, 1, 3], [6, 1, 5],
        # m=0-mod-3 multi-block (rule unknown)
        [9, 8], [3, 6, 6],
    ]
    ms = [40, 41, 42, 101, 102, 103, 301, 302, 303]
    from collections import defaultdict
    newrules = defaultdict(set)
    bad = []
    npred = nconf = 0
    for w in tests:
        for m in ms:
            kind, s, unsafe, out = probe_w(m, tuple(w))
            got = (kind, out)
            exp = predict(m, list(w))
            if exp is not None:
                npred += 1
                if got == exp:
                    nconf += 1
                    tag = 'OK'
                else:
                    tag = f'MISMATCH exp={exp}'
                    bad.append((m, w, got, exp))
            else:
                tag = 'NEW'
                if kind in ('LAND', 'MOVE'):
                    # record law: c = 3m'-8m
                    if kind == 'LAND':
                        newrules[(m % 3, tuple(w))].add(('LAND', 3 * out - 8 * m))
                    else:
                        newrules[(m % 3, tuple(w))].add(('MOVE', 3 * out[0] - 8 * m, tuple(out[1])))
                else:
                    bad.append((m, w, got, None))
            if unsafe:
                bad.append((m, w, 'UNSAFE', unsafe))
            print(f"m={m} w={w} -> {got}  [{tag}]")
        sys.stdout.flush()
    print(f"\npredictions confirmed: {nconf}/{npred}")
    print("\n=== NEW rules learned ===")
    for key in sorted(newrules):
        outs = newrules[key]
        print(f"  m%3={key[0]} w={list(key[1])}: {sorted(outs)}" + ('' if len(outs) == 1 else '  <-- SPLIT'))
    print("\nbad:", bad if bad else "NONE")
