# o18 R1-PINNING: EXTENDED transducer T_ext / R1_ext.  Pins the deep-R1 fractal cells
# left Unknown by o18_md_rules.py (517 adversarially-reachable cells,
# O18_INVARIANT_SYNTHESIS_2026-07-07.md §5.4).  The original file is NOT modified.
#
# THE UNIFYING LAW (discovered by concrete probing, this session): the whole j==0 h_p /
# "deep" template ladder of R1 is ONE reduction.  For the v==2 branch
#     word = 1^j (1,2) X,   X = 1^p (1,2) Z     (p >= 0),
# let inner = R1(p, Z)  (the pass-result of the sub-word 1^p (1,2) Z).  Then:
#     inner HALT                    ->  HALT                          [any j]
#     inner ('MOVE', -17, iw):
#         j >= 1                    ->  ('MOVE', -17, (1,2j+2) + iw)
#         j == 0                    ->  ('MOVE', -23, [4,1,1,1] + dec6(iw))
#     inner ('MOVE', -23, iw)       [only p == 0 can produce -23; iw = [4,1,1,1]+tail]:
#         j >= 2                    ->  ('MOVE', -17, (1,2j)   + iw)
#         j == 0                    ->  HALT   (verified shallow AND deep: 30+ shapes,
#                                               4 magnitudes each -- the fatal family)
#         j == 1                    ->  the dec3 law:  HALT iff the first non-unit
#             block of tail is separator-led (s0>=2) or has value <= 2 or is absent;
#             otherwise ('MOVE', -23, (1,4) + 1^7 + dec3(tail)) where dec3 keeps the
#             leading units, subtracts 3 from that block (value 3 -> block vanishes,
#             pushtail-style separator increment on the remainder).
#             *** THIS CORRECTS o18_md_rules.py, WHICH IS UNSOUND HERE: the base rule
#             "inner c=-23 -> HALT for j<=1" is concretely FALSE at j=1 for e.g.
#             w = 1.2.2.1.1 (m=40,100,301,1000: MOVE c=-23, NOT halt).  The base grid
#             never fired those cells; its j<=1 HALT was pinned only on q<=1 tails. ***
# where dec6 subtracts 6 from the leading block of iw:
#     iw = (1,a)+rest, a >= 7       ->  (1,a-6) + rest
#     a == 6, rest = (s0,b0)+r2     ->  (s0+1,b0) + r2      (block vanishes: separator +1)
#     a == 4, rest = (1,b0>=4)+r2   ->  (1,1),(1,b0-3) + r2 (the borrow)
#     anything else                 ->  Unknown             (never observed concretely)
# Every previously pinned j==0 template is an EXACT instance of this law:
#   _hp(1,rho)=dec6((1,4),(1,rho)); _hp(2,rho)=dec6((1,6),(1,rho));
#   _hp(3..,rho)=(1,2p-4),(1,rho)=dec6((1,2p+2),(1,rho)); the zs==2 merge template
#   = dec6(inner s>=2 merge); the zs==1 v>=3 push template = dec6(inner push);
#   the p==0 adjacent-2 (2,1)-template = dec6((1,6)+units+pushtail).
# Verification (this session): (a) T_ext == T on every cell where T is defined
#   (equivalence fuzz, o18_r1_fuzz.py mode 'eq'); (b) all 517 reachable Unknown cells
#   resolved by T_ext match fresh concrete simulation at 4 magnitudes (o18_r1_probe.py
#   + o18_r1_fuzz.py mode 'cells'); (c) systematic family grids H/Hp/G/B1/B2
#   (o18_r1_grid.py) match; (d) full-chain predict-and-confirm fuzz biased into the
#   nested-2 region (o18_r1_fuzz.py mode 'chain').
# Status: [PROVEN on grid] for every (shape, parameter) combination fired by (a)-(d);
# extension to unbounded parameters is [OBSERVED/exact-fit] pending trace-template
# certification -- the same standard as the base table in o18_md_rules.py.
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import units, pushtail, _merge, Unknown


def dec6(iw):
    """Subtract 6 from the leading block of an inner R1 result word."""
    if not iw or iw[0][0] != 1:
        raise Unknown(('dec6 head', iw[:1]))
    a, rest = iw[0][1], iw[1:]
    if a >= 7:
        return ((1, a - 6),) + rest
    if a == 6:
        if not rest:
            raise Unknown(('dec6 a==6 empty tail',))
        (s0, b0), r2 = rest[0], rest[1:]
        return ((s0 + 1, b0),) + r2
    if a == 4:
        if rest and rest[0][0] == 1 and rest[0][1] >= 4:
            return ((1, 1), (1, rest[0][1] - 3)) + rest[1:]
        raise Unknown(('dec6 a==4 borrow', rest[:1]))
    raise Unknown(('dec6 lead', a))


def dec3(tail):
    """The j==1 endgame on an inner -23 word [4,1,1,1]+tail: subtract 3 from the
    first non-unit block of tail.  Returns the rewritten tail, or None for HALT."""
    u = units(tail)
    if u == len(tail):
        return None                       # empty or all-unit tail: HALT
    (s0, b0), rest = tail[u], tail[u + 1:]
    if s0 >= 2 or b0 <= 2:
        return None                       # separator-led or value<=2: HALT
    pre = ((1, 1),) * u
    if b0 == 3:                           # block vanishes: separator increment
        if not rest:
            return pre
        (s1, b1), r2 = rest[0], rest[1:]
        return pre + ((s1 + 1, b1),) + r2
    return pre + ((1, b0 - 3),) + rest


def R1_ext(j, X):
    """m=1 (mod 3) branch, word = 1^j (1,2) X.  Same contract as o18_md_rules.R1,
    with the v==2 region closed by the unified inner+dec6 law."""
    p = units(X)
    if p == len(X):  # X = 1^p
        if j == 0:
            w2 = ((1, 4), (1, 1), (1, 1), (1, 1)) + (((1, 2 * p),) if p else ())
            return ('MOVE', -23, w2)
        return ('MOVE', -17, ((1, 2 * j + 2), (1, 2 * p + 6)))
    (s, v), Z = X[p], X[p + 1:]
    if s >= 2:  # unchanged from o18_md_rules.R1 (pinned)
        if p >= 1:
            if j == 0:
                return ('MOVE', -23, ((1, 4), (1, 1), (1, 1), (1, 1)) + _merge(2 * p, s - 2, v) + Z)
            return ('MOVE', -17, ((1, 2 * j + 2),) + _merge(2 * p + 6, s - 2, v) + Z)
        if j == 0:
            return ('MOVE', -23, ((1, 4), (1, 1), (1, 1), (1, 1), (s - 1, v)) + Z)
        if s == 2:
            return ('MOVE', -17, ((1, 2 * j + 2), (1, v + 6)) + Z)
        return ('MOVE', -17, ((1, 2 * j + 2), (1, 6), (s - 2, v)) + Z)
    if v >= 3:  # PUSH (pinned)
        return ('MOVE', -17, ((1, 2 * j + 6),) + ((1, 1),) * (p + 2) + pushtail(v, Z))
    # ---- v == 2: THE UNIFIED LAW ----
    inner = R1_ext(p, Z)
    if inner[0] == 'HALT':
        return ('HALT',)
    ic, iw = inner[1], inner[2]
    if ic == -17:
        if j >= 1:
            return ('MOVE', -17, ((1, 2 * j + 2),) + iw)
        return ('MOVE', -23, ((1, 4), (1, 1), (1, 1), (1, 1)) + dec6(iw))
    # ic == -23: only reachable with p == 0 (adjacent 2s)
    if j >= 2:
        return ('MOVE', -17, ((1, 2 * j),) + iw)
    if j == 0:
        return ('HALT',)
    # j == 1: the dec3 law (corrects the base rule's blanket HALT)
    if iw[:4] != ((1, 4), (1, 1), (1, 1), (1, 1)):
        raise Unknown(('j1 ic-23 prefix', iw[:4]))
    t3 = dec3(iw[4:])
    if t3 is None:
        return ('HALT',)
    return ('MOVE', -23, ((1, 4),) + ((1, 1),) * 7 + t3)


def T_ext(r, w):
    """One pass on (m = r mod 3, w).  Identical to o18_md_rules.T outside the R1
    v==2 region; delegates to R1_ext there (and recursively via r==0 delegation)."""
    if not w:
        raise Unknown(('empty word', r))
    j = units(w)
    if r == 2:
        s, b = w[0]
        X = w[1:]
        if s == 1:
            if not X:
                return ('LAND', 3 * b + 14)
            return ('MOVE', (14 if b == 1 else 3 * b + 11), X)
        return ('MOVE', 11, ((s - 1, b),) + X)
    if r == 1:
        if j == len(w):
            return ('MOVE', -17, ((1, 2 * j + 6),))
        (s, v), X = w[j], w[j + 1:]
        if s >= 2:
            if s == 2:
                return ('MOVE', -17, ((1, 2 * j + 6 + v),) + X)
            return ('MOVE', -17, ((1, 2 * j + 6), (s - 2, v)) + X)
        if v >= 3:
            return ('MOVE', -5, ((1, 1),) * (j + 2) + pushtail(v, X))
        return R1_ext(j, X)
    # r == 0
    if j == len(w):
        return ('LAND', 6 * j + 12)
    (s, v), X = w[j], w[j + 1:]
    if s == 2:
        if not X:
            return ('LAND', 6 * j + 3 * v + 12)
        return ('MOVE', 6 * j + 3 * v + 9, X)
    if s >= 3:
        return ('MOVE', 6 * j + 9, ((s - 2, v),) + X)
    # s == 1
    if not X:
        if v % 3 == 2:
            return ('MOVE', 6 * j + 8 * v - 19, ((1, 6),))
        return ('LAND', 6 * j + 8 * v + (10 if v % 3 == 1 else 12))
    sub = T_ext((v + 2) % 3, X)
    if sub[0] == 'HALT':
        return ('HALT',)
    if sub[0] == 'LAND':
        return ('LAND', 6 * j + 8 * v - 2 + sub[1])
    return ('MOVE', 6 * j + 8 * v - 2 + sub[1], sub[2])


def predict_chain_ext(m, w, maxp=60):
    """Iterate T_ext symbolically (same contract as o18_md_rules.predict_chain)."""
    chain = []
    while len(chain) < maxp:
        chain.append((m, w))
        res = T_ext(m % 3, w)
        if res[0] == 'HALT':
            return chain, ('HALT',)
        if res[0] == 'LAND':
            return chain, ('LAND', (8 * m + res[1]) // 3)
        m, w = (8 * m + res[1]) // 3, res[2]
    return chain, ('OVER',)
