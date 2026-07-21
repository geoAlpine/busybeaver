"""x2 LEAD LAW (problem B): find the per-level recursion of `leadSteps`/`LeadLaw`.

Faithful re-implementation of X2.lean's `step`/`steps`/`regenIn`/`regenWord`/`ascMarker`
/`descCascade`/`leadRec`.  VALIDATED against the two kernel-proven Lean anchors
(`leadOut_6` = 154 steps, `leadOut_7` = 241 steps) before any measurement is trusted.
"""

# ---------------------------------------------------------------- machine
A, B, C, D, E, F = range(6)
NAMES = "ABCDEF"

# state, head -> (newstate, write, move)  (+1 = right, -1 = left)
TABLE = {
    (A, 0): (B, 1, +1), (A, 1): (E, 0, +1),
    (B, 0): (C, 1, +1), (B, 1): None,          # HALT
    (C, 0): (D, 0, -1), (C, 1): (E, 1, -1),
    (D, 0): (E, 0, +1), (D, 1): (D, 1, -1),
    (E, 0): (F, 1, +1), (E, 1): (C, 0, -1),
    (F, 0): (A, 0, +1), (F, 1): (E, 1, +1),
}


class Cfg:
    """Tape zipper as in X2.lean, but with BOTH lists stored NEAREST-AT-THE-END
    (so mvL/mvR are O(1) pops).  `mk`/`out_left`/`out_right` convert to Lean order."""
    __slots__ = ("st", "pos", "left", "head", "right")

    def __init__(self, st, pos, left, head, right):
        self.st, self.pos = st, pos
        self.left, self.head, self.right = list(left), head, list(right)

    def copy(self):
        return Cfg(self.st, self.pos, self.left, self.head, self.right)

    def key(self):
        return (self.st, self.pos, tuple(self.left), self.head, tuple(self.right))


def step(c):
    t = TABLE[(c.st, c.head)]
    if t is None:
        return None                                   # HALT
    ns, w, mv = t
    c.head = w
    if mv == +1:                                      # mvR
        c.left.append(c.head)
        c.head = c.right.pop() if c.right else 0
    else:                                             # mvL
        # X2.lean's mvL on empty left: ⟨[], h, r⟩ => ⟨[], false, h :: r⟩
        c.right.append(c.head)
        c.head = c.left.pop() if c.left else 0
    c.st, c.pos = ns, c.pos + mv
    return c


def steps(n, c):
    c = c.copy()
    for _ in range(n):
        if step(c) is None:
            return None
    return c


# X2.lean lists are NEAREST-FIRST on both sides; internally we store both
# reversed (nearest last) so that pop()/append() are the zipper moves.
def mk(st, pos, left, head, right):
    return Cfg(st, pos, list(reversed(left)), head, list(reversed(right)))


def out_right(c):
    return list(reversed(c.right))


def out_left(c):
    return list(reversed(c.left))


# ---------------------------------------------------------------- words
def ones(n):
    return [1] * n


def zeros(n):
    return [0] * n


def pow01(n):
    """X2.lean `pow01 n` — checked against the file below."""
    return [0, 1] * n


def descCascade(d):
    if d == 0:
        return ones(1)
    return ones(2 ** (d + 2) - 3) + [0, 0] + descCascade(d - 1)


def regenWord(k):
    return ones(2 ** k - 3) + [0, 1, 0, 0, 1] + pow01(2 ** (k - 1) - 2)


def ascMarker(b, n, m):
    if n == 0:
        return list(m)
    return [0, 0, 1] + pow01(2 ** b - 2) + ascMarker(b + 1, n - 1, m)


def regenIn(k, p, z, marker, R):
    left = ones(2 ** k - 3) + [0, 1, 0, 0, 1] + pow01(2 ** (k - 1) - 2) + list(marker)
    right = [0] + descCascade(k - 4) + zeros(z) + list(R)
    return mk(E, p, left, 0, right)


def leadRec(j):
    """leadRec 0 = 154 ; leadRec (n+1) = leadRec n + 3*2^(n+5) - 9  (X2.lean)."""
    v = 154
    for n in range(j):
        v = v + 3 * 2 ** (n + 5) - 9
    return v


def leadSteps(k):
    return leadRec(k - 6)


def leadOut(k, p, marker, R):
    """The RHS of LeadLaw k."""
    return regenIn(4, p + 2 ** (k - 1) - k + 4, 2 ** (k - 1) + 1,
                   ascMarker(4, k - 6, regenWord(k) + list(marker)), R)


def same(c1, c2):
    return (c1.st == c2.st and c1.pos == c2.pos and c1.left == c2.left
            and c1.head == c2.head and c1.right == c2.right)


# ---------------------------------------------------------------- validation
def validate():
    print("=== VALIDATION against the kernel-proven Lean anchors ===")
    print("leadSteps 6 == 154 :", leadSteps(6) == 154)
    print("leadSteps 7 == 241 :", leadSteps(7) == 241)
    ok = True
    for k in (6, 7):
        for marker, R in (([], []), ([1, 0, 1], [0, 1, 1, 0])):
            got = steps(leadSteps(k), regenIn(k, 0, 2 ** (k - 1) + 9, marker, R))
            want = leadOut(k, 0, marker, R)
            r = got is not None and same(got, want)
            ok &= r
            print(f"  leadOut_{k} marker={marker} R={R}: {r}")
    # CONTROL that MUST fail: off-by-one step count
    bad = steps(leadSteps(7) + 1, regenIn(7, 0, 2 ** 6 + 9, [], []))
    ctl = bad is not None and same(bad, leadOut(7, 0, [], []))
    print("  CONTROL (241+1 steps, must be False):", ctl)
    # CONTROL that MUST fail: wrong ascMarker depth
    got = steps(leadSteps(7), regenIn(7, 0, 2 ** 6 + 9, [], []))
    wrong = regenIn(4, 0 + 2 ** 6 - 7 + 4, 2 ** 6 + 1,
                    ascMarker(4, 7 - 6 + 1, regenWord(7) + []), [])
    print("  CONTROL (ascMarker depth+1, must be False):", same(got, wrong))
    print("VALIDATION PASSED:", ok and not ctl)
    return ok and not ctl


if __name__ == "__main__":
    validate()


# ---------------------------------------------------------------- measurement
def as_regenIn(c, R, shapes):
    """If `c` is `regenIn j p z marker R`-shaped for some j in `shapes`, return
    (j, p, z, marker).  Detected from the RIGHT register (= [0] ++ descCascade (j-4)
    ++ zeros z ++ R) and the LEFT word (= regenWord j ++ marker).  Definitions only."""
    if c.st != E or c.head != 0:
        return None
    right, left = out_right(c), out_left(c)
    for j, pre, w in shapes:
        if len(pre) > len(right) or right[:len(pre)] != pre:
            continue
        rest = right[len(pre):]
        if len(R) and rest[len(rest) - len(R):] != list(R):
            continue
        z = len(rest) - len(R)
        if any(rest[:z]):
            continue
        if len(w) > len(left) or left[:len(w)] != w:
            continue
        return (j, c.pos, z, left[len(w):])
    return None


def scan(k, marker=(), R=(), jmax=None):
    """Every time in the level-k lead at which the config is regenIn-shaped."""
    jmax = jmax if jmax is not None else k
    shapes = [(j, [0] + descCascade(j - 4), regenWord(j)) for j in range(4, jmax + 1)]
    T = leadSteps(k)
    c = regenIn(k, 0, 2 ** (k - 1) + 9, marker, R).copy()
    hits = []
    for t in range(T + 1):
        r = as_regenIn(c, R, shapes)
        if r:
            hits.append((t,) + r[:3] + (len(r[3]),))
        if t < T and step(c) is None:
            break
    return T, hits


def scan_right(k, marker=(), R=()):
    """Times at which the RIGHT register is exactly [0]++descCascade d ++ blanks++R,
    for each cascade depth d -- i.e. the cascade-block boundaries.  Right register only;
    state/pos/left recorded but NOT constrained."""
    T = leadSteps(k)
    pres = [(d, [0] + descCascade(d)) for d in range(0, k - 3)]
    c = regenIn(k, 0, 2 ** (k - 1) + 9, marker, R).copy()
    first = {}
    for t in range(T + 1):
        right = out_right(c)
        for d, pre in pres:
            if d in first:
                continue
            if len(pre) <= len(right) and right[:len(pre)] == pre:
                rest = right[len(pre):]
                if len(R) and rest[len(rest) - len(R):] != list(R):
                    continue
                z = len(rest) - len(R)
                if any(rest[:z]):
                    continue
                first[d] = (t, NAMES[c.st], c.pos, z, len(c.left))
        if t < T and step(c) is None:
            break
    return T, first


# ---------------------------------------------------------------- THE HOP
def ascLayer(b):
    """One `ascMarker` layer, as it sits in the LEFT list (nearest-first)."""
    return [0, 0, 1] + pow01(2 ** b - 2)


def peelSteps(d):
    """Measured cost of peeling cascade block d:  3*2^(d+2) - 9."""
    return 3 * 2 ** (d + 2) - 9


def peel_in(p, W, d, Rest):
    return mk(E, p, W, 0, [0] + descCascade(d) + list(Rest))


def peel_out(p, W, d, Rest):
    return mk(E, p + 2 ** (d + 2) - 1, ascLayer(d + 1) + list(W), 0,
              [0] + descCascade(d - 1) + list(Rest))


def test_peel(ds, Ws, Rests):
    """PEEL LEMMA: free left word W, free tail Rest."""
    allok = True
    for d in ds:
        for wi, W in enumerate(Ws):
            for ri, Rest in enumerate(Rests):
                got = steps(peelSteps(d), peel_in(0, W, d, Rest))
                ok = got is not None and same(got, peel_out(0, W, d, Rest))
                allok &= ok
                if not ok:
                    print(f"   FAIL d={d} W#{wi} Rest#{ri}")
    return allok


def minpos(k, marker=(), R=()):
    """Minimum head position reached during the level-k lead (start = 0)."""
    c = regenIn(k, 0, 2 ** (k - 1) + 9, marker, R).copy()
    lo = 0
    for _ in range(leadSteps(k)):
        if step(c) is None:
            return None
        lo = min(lo, c.pos)
    return lo


# --------------------------------------------- THE GENERIC ONES-BLOCK TRANSIT
def transit_in(p, W, m, Tail):
    return mk(E, p, W, 0, [0] + ones(2 * m + 1) + [0, 0] + list(Tail))


def transit_out(p, W, m, Tail):
    return mk(E, p + 2 * m + 3, [0, 0, 1] + pow01(m) + list(W), 0, [0] + list(Tail))


def transit_cost(m):
    return 6 * m + 3


def test_transit(ms, Ws, Tails):
    bad = []
    for m in ms:
        for wi, W in enumerate(Ws):
            for ti, Tail in enumerate(Tails):
                g = steps(transit_cost(m), transit_in(0, W, m, Tail))
                if not (g is not None and same(g, transit_out(0, W, m, Tail))):
                    bad.append((m, wi, ti))
    return bad


# ---------------------------------------------------------------- TAIL + GENLEAD
def tail_in(p, V, S):
    return mk(E, p, [0, 0, 1, 0] + list(V), 0, [0] + ones(1) + zeros(9) + list(S))


def tail_out(p, V, S):
    return mk(E, p + 8, ones(12) + list(V), 0, [0] + ones(1) + zeros(1) + list(S))


def genlead_in(p, W, d, S):
    return mk(E, p, W, 0, [0] + descCascade(d) + zeros(9) + list(S))


def genlead_out(p, W, d, S):
    return mk(E, p + 2 ** (d + 3) - d,
              regenWord(4) + ascMarker(4, d - 2, W), 0,
              [0] + descCascade(0) + zeros(1) + list(S))


def genlead_cost(d):
    return leadRec(d - 2)
