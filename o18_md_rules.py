# o18 MULTI-DEFECT TRANSDUCER: the complete pass-rule schema T(m mod 3, w).
# Word w = tuple of (s,b): config 0^inf [F] 1^m (0^{s_1} 1^{b_1}) ... 0^inf, head at anchor.
# One pass (anchored F-entry -> next anchored F-entry) maps (m,w) -> (m',w') with
#   m' = (8m + c)/3, c and w' functions of (m mod 3, w) ONLY  [grid: zero splits].
# Sources: o18_md_probe.py grids (3075 runs + targeted R1/separator scans), all exact,
# unsafe=0 on every non-halting pass. HALT cells are genuine (D reads 1 with left-1).
# Status: [PROVEN on grid] for every rule fired by the fuzz verifier; extension to all
# parameter values is [OBSERVED/exact-fit] pending trace-template certification.

class Unknown(Exception):
    pass

def units(w):
    j = 0
    while j < len(w) and w[j] == (1, 1):
        j += 1
    return j

def pushtail(v, X):
    """Tail after a PUSH consumes a (1,v>=3) block: v>3 leaves (1,v-3); v==3 vanishes,
    incrementing the following separator (double-0 creation)."""
    if v > 3:
        return ((1, v - 3),) + X
    if not X:
        return ()
    (s0, b0), rest = X[0], X[1:]
    return ((s0 + 1, b0),) + rest


def R1(j, X):
    """m=1 (mod 3) branch, w = 1^j (1,2) X  (the EXIT / v=2 region, recursive).
    Returns ('MOVE', c, w') or ('HALT',). Raises Unknown on unpinned cells."""
    p = units(X)
    if p == len(X):  # X = 1^p
        if j == 0:
            w2 = ((1, 4), (1, 1), (1, 1), (1, 1)) + (((1, 2 * p),) if p else ())
            return ('MOVE', -23, w2)
        return ('MOVE', -17, ((1, 2 * j + 2), (1, 2 * p + 6)))
    (s, v), Z = X[p], X[p + 1:]
    if s >= 2:
        if p >= 1:
            # w = 1^j (1,2) 1^p (s>=2,v) Z   [grid j=0..2, p=1..3, s=2..4]
            if j == 0:
                return ('MOVE', -23, ((1, 4), (1, 1), (1, 1), (1, 1)) + _merge(2 * p, s - 2, v) + Z)
            return ('MOVE', -17, ((1, 2 * j + 2),) + _merge(2 * p + 6, s - 2, v) + Z)
        if j == 0:
            return ('MOVE', -23, ((1, 4), (1, 1), (1, 1), (1, 1), (s - 1, v)) + Z)
        # j>=1: emit (1,2j+2), then [6] (+)_{s-2} v :
        if s == 2:
            return ('MOVE', -17, ((1, 2 * j + 2), (1, v + 6)) + Z)
        return ('MOVE', -17, ((1, 2 * j + 2), (1, 6), (s - 2, v)) + Z)
    if v >= 3:
        return ('MOVE', -17, ((1, 2 * j + 6),) + ((1, 1),) * (p + 2) + pushtail(v, Z))
    # v == 2
    if p >= 1:
        inner = R1(p, Z)  # X itself is the word 1^p (1,2) Z
        if inner[0] == 'HALT':
            return ('HALT',)
        ic, iw = inner[1], inner[2]
        if j >= 1:
            return ('MOVE', -17, ((1, 2 * j + 2),) + iw)
        # j == 0: the h_p templates
        q = units(Z)
        if q == len(Z):  # Z = 1^q : "recycle-flavoured" tail, rho = 2q+6
            rho = 2 * q + 6
            return ('MOVE', -23, ((1, 4), (1, 1), (1, 1), (1, 1)) + _hp(p, rho))
        (zs, zv), W = Z[q], Z[q + 1:]
        if zs >= 2 and q == 0:  # Z = (s>=2, b) + W, rho = b+6-ish
            if zs == 2:
                return ('MOVE', -23, ((1, 4), (1, 1), (1, 1), (1, 1)) + _hp(p, zv + 6) + W)
            raise Unknown(('R1 j0 hp gap s>=3', p, zs, zv))
        if zs == 1 and zv >= 3:
            return ('MOVE', -23, ((1, 4), (1, 1), (1, 1), (1, 1), (1, 2 * p))
                    + ((1, 1),) * (q + 2) + pushtail(zv, W))
        raise Unknown(('R1 j0 hp deep', p, Z))
    # p == 0: adjacent (1,2)(1,2)
    inner = R1(0, Z)
    if inner[0] == 'HALT':
        return ('HALT',)
    ic, iw = inner[1], inner[2]
    if ic == -23:
        if j >= 2:
            return ('MOVE', -17, ((1, 2 * j),) + iw)
        return ('HALT',)
    # ic == -17: happens iff Z = 1^q (1,v>=3) W
    if j >= 1:
        return ('MOVE', -17, ((1, 2 * j + 2),) + iw)
    q = units(Z)
    (zs, zv), W = Z[q], Z[q + 1:]
    assert zs == 1 and zv >= 3
    return ('MOVE', -23, ((1, 4), (1, 1), (1, 1), (1, 1), (2, 1))
            + ((1, 1),) * (q + 1) + pushtail(zv, W))


def _merge(a, k, b):
    """[a] joined to block b by separator k: k=0 merges into one block, else (1,a),(k,b)."""
    if k == 0:
        return ((1, a + b),)
    return ((1, a), (k, b))


def _hp(p, rho):
    """The j=0 delegated 'recycle' tails: h_p(rho). Pinned p=1,2,3 on grid."""
    if p == 1:
        return ((1, 1), (1, rho - 3))
    if p == 2:
        return ((2, rho),)
    if p == 3:
        return ((1, 2), (1, rho))
    raise Unknown(('hp', p, rho))


def T(r, w):
    """One pass on (m = r mod 3, w). Returns ('LAND', c) | ('MOVE', c, w') | ('HALT',)."""
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
        return R1(j, X)
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
    sub = T((v + 2) % 3, X)  # DELEGATION: flush near part, tail processed in branch (v+2)%3
    if sub[0] == 'HALT':
        return ('HALT',)
    if sub[0] == 'LAND':
        return ('LAND', 6 * j + 8 * v - 2 + sub[1])
    return ('MOVE', 6 * j + 8 * v - 2 + sub[1], sub[2])


def predict_chain(m, w, maxp=60):
    """Iterate T symbolically: full chain [(m,w),...] + end ('LAND',L)|('HALT',)|('OVER',)."""
    chain = []
    while len(chain) < maxp:
        chain.append((m, w))
        res = T(m % 3, w)
        if res[0] == 'HALT':
            return chain, ('HALT',)
        if res[0] == 'LAND':
            return chain, ('LAND', (8 * m + res[1]) // 3)
        m, w = (8 * m + res[1]) // 3, res[2]
    return chain, ('OVER',)


def concrete_chain(m, w, maxF=70):
    """All anchored F-entries of a fresh concrete run, + end."""
    from o18_md_probe import word_blocks, parse_word
    from o18_depth_map import run_cfg
    status, fents, steps, unsafe = run_cfg(word_blocks(m, w), maxF=maxF,
                                           budget=500_000_000, lpadf=10)
    chain = [(m, w)]
    for (s, clean, land, R, hp) in fents:
        if clean:
            return chain, ('LAND', land), steps, unsafe
        p = parse_word(R, hp)
        if p is not None:
            chain.append(p)
        elif hp <= 0:
            return chain, ('BADFORM', R, hp), steps, unsafe
    if status == 'HALT':
        return chain, ('HALT',), steps, unsafe
    return chain, (status,), steps, unsafe


# ---------------- fuzz verifier: FULL-CHAIN predict-and-confirm ----------------
if __name__ == '__main__':
    import sys, random
    sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
    from o18_md_probe import wstr
    random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    NW = int(sys.argv[2]) if len(sys.argv) > 2 else 150
    words = set()
    # structured families first: exit products + 2-trains + separator stacks
    for t in (1, 2, 3, 5, 8):
        words.add(((1, 2 * t + 2), (1, 6)))
    words.add(((1, 4), (1, 1), (1, 1), (1, 1)))
    words.update([((1, 2), (1, 2)), ((1, 2), (1, 2), (1, 2)), ((1, 1), (1, 2), (1, 2), (1, 6)),
                  ((3, 4), (2, 2), (1, 5)), ((1, 5), (1, 2), (1, 2)), ((1, 3), (3, 2), (1, 3))])
    while len(words) < NW:
        k = random.randint(1, 6)
        w = tuple((random.choices([1, 1, 1, 2, 3], k=1)[0], random.choice([1, 1, 2, 2, 3, 4, 5, 6, 7, 9]))
                  for _ in range(k))
        words.add(w)
    ms = [40, 41, 42, 100, 101, 102, 301, 302, 303]
    nok = nbad = nunk = nhalt = 0
    unknowns = {}
    bad = []
    for w in sorted(words):
        for m in ms:
            try:
                pch, pend = predict_chain(m, w)
            except Unknown as u:
                nunk += 1
                unknowns.setdefault(str(u.args[0]), []).append((m % 3, w))
                continue
            cch, cend, steps, unsafe = concrete_chain(m, w)
            if pend == ('HALT',):
                nhalt += 1
            if cend[0] in ('OVERFLOW', 'MAXF', 'BUDGET'):
                ok = pch[:len(cch)] == cch and len(cch) >= 2  # prefix agreement
            else:
                ok = pch == cch and pend == cend
            if ok:
                nok += 1
            else:
                nbad += 1
                bad.append((m, w, cch[-1] if cch else None, cend, pch[-1] if pch else None, pend))
    print(f'CHAINS CONFIRMED {nok}  MISMATCH {nbad}  UNKNOWN-cells {nunk}  (predicted halts: {nhalt})')
    for k, v in sorted(unknowns.items()):
        print(f'  UNKNOWN {k}: {len(v)} hits, e.g. {v[0][0]}, {wstr(v[0][1])}')
    for b in bad[:25]:
        print('  BAD', b)
