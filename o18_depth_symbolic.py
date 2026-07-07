# o18 SYMBOLIC (m,w)-machine: the tower as a defect-word rewrite system.
# State: (m, w) with m integer, w = tuple of 1-run lengths (single-0 separators):
#   config = 0^inf [F] 1^m 0 1^{w1} 0 1^{w2} ... 0 1^{wk} 0^inf ;  w=() means clean C_{m+1}.
# Rules (grid-verified in o18_depth_map.py / o18_depth_word.py; this file only ITERATES them):
#   clean C_N: N%3 in {0,1}: N -> floor(8N/3)+2 (level-0 law, prior notes)
#              N%3 == 2:    -> (m,w) = ((8N-25)/3, (6,))
#   dirty (m,w), branch on m%3, j = number of leading 1s (unit blocks) in w:
#     m%3==1: all-units w=1^j          -> ((8m-17)/3, (2j+6,))                    RECYCLE
#             w=1^j+(v>=3)+X           -> ((8m-5)/3, 1^{j+2}+(v-3 if v>3)+X)      PUSH
#             w=1^j+(2)+X, j>=1        -> ((8m-17)/3, (2j+2,)+X_rule)             EXIT2  [X_rule from probe]
#             w=(2,)+X                 -> ((8m-23)/3, (4,1,1,1)+X_rule)           EXIT2a [from probe]
#     m%3==2: w=(1,)+X                 -> ((8m+14)/3, X)                          POP
#             w=(a>=2,) only           -> LAND L=(8m+3a+14)/3                     LAND2
#             w=(a>=2,)+X              -> ((8m+3a+11)/3, X)                       MERGE  [from probe]
#     m%3==0: w=1^j+(v)  (last block), v%3!=2 -> LAND L=(8m+8v+6j+(10 or 12))/3   LAND0
#             w=1^j+(v)+X or v%3==2:  learned rules from o18_depth_word.py        FLUSH/...
# UNKNOWN cells raise; the driver reports any hit -> incompleteness found.
import sys
from collections import deque

class Unknown(Exception): pass

def step(m, w, exit2_rule=None, flush_multi=None):
    """One transition. Returns ('C', N) for clean landing or ('D', m2, w2)."""
    r = m % 3
    j = 0
    while j < len(w) and w[j] == 1:
        j += 1
    if r == 1:
        if j == len(w):
            return ('D', (8 * m - 17) // 3, (2 * j + 6,))
        v, X = w[j], w[j + 1:]
        if v >= 3:
            nw = (1,) * (j + 2) + ((v - 3,) if v > 3 else ()) + X
            return ('D', (8 * m - 5) // 3, nw)
        # v == 2
        if exit2_rule is None:
            raise Unknown(('m%3=1 v=2', m % 9, w))
        return exit2_rule(m, j, X)
    if r == 2:
        if w[0] == 1:
            return ('D', (8 * m + 14) // 3, w[1:])
        if len(w) == 1:
            return ('C', (8 * m + 3 * w[0] + 14) // 3)
        return ('D', (8 * m + 3 * w[0] + 11) // 3, w[1:])
    # r == 0
    if j == len(w):
        raise Unknown(('m%3=0 all-units', m % 9, w))
    v, X = w[j], w[j + 1:]
    if not X:
        if v % 3 != 2:
            return ('C', (8 * m + 8 * v + 6 * j + (10 if v % 3 == 1 else 12)) // 3)
        return ('D', (8 * m + 8 * v + 6 * j - 19) // 3, (6,))
    if flush_multi is None:
        raise Unknown(('m%3=0 multi-block', m % 9, w))
    return flush_multi(m, j, v, X)

def clean_step(N):
    if N % 3 == 2:
        return ('D', (8 * N - 25) // 3, (6,))
    return ('C', (8 * N) // 3 + 2)

def orbit(N0, gens, exit2_rule=None, flush_multi=None, verbose=False):
    """Iterate; count rule usage; report any Unknown."""
    from collections import Counter
    use = Counter()
    shapes = set()
    state = ('C', N0)
    towers = 0
    maxblocks = 0
    maxdepth = 0
    depth = 0
    try:
        for g in range(gens):
            if state[0] == 'C':
                N = state[1]
                use[f'clean%3={N % 3}'] += 1
                state = clean_step(N)
                depth = 0
                if state[0] == 'D':
                    towers += 1
            else:
                _, m, w = state
                j = 0
                while j < len(w) and w[j] == 1:
                    j += 1
                key = (m % 3, 'units' if j == len(w) else ('v=' + ('1' if w[j] == 1 else '2' if w[j] == 2 else '>=3')), 'last' if j >= len(w) - 1 else 'mid')
                use[str(key)] += 1
                shapes.add(shape_of(w))
                maxblocks = max(maxblocks, len(w))
                depth += 1
                maxdepth = max(maxdepth, depth)
                state = step(m, w, exit2_rule, flush_multi)
            if verbose and g < 60:
                s = state if state[0] == 'C' else ('D', state[1] if state[1] < 10**15 else f'~1e{len(str(state[1]))}', state[2])
                print(g, s)
    except Unknown as u:
        return ('UNKNOWN', g, u.args[0], use, shapes, towers, maxblocks, maxdepth)
    return ('OK', gens, None, use, shapes, towers, maxblocks, maxdepth)

def shape_of(w):
    """Canonical shape: unit-runs collapsed, block values classed."""
    out = []
    i = 0
    while i < len(w):
        if w[i] == 1:
            j = i
            while j < len(w) and w[j] == 1:
                j += 1
            out.append('U')  # a unit train (any length >= 1)
            i = j
        else:
            out.append('2' if w[i] == 2 else 'B')
            i += 1
    return tuple(out)
