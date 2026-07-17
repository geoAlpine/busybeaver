#!/usr/bin/env python3
"""x2hi_transport.py -- decompose the blank -> M1(1) run (188 099 steps) BY TRANSPORT.

METHOD (roadmap 1.5 / task method 1-4):
  * NEVER identify a sub-call by length.  Each candidate is an instance of a
    *specific proven Lean theorem*: we match that theorem's IN pattern against the
    real on-path config CELL-FOR-CELL, then VERIFY by running the machine that the
    OUT config is exactly what the theorem asserts.  A window is accepted only if
    the OUT check passes, so a wrong transcription CANNOT silently produce a hit.
  * Tape extent is always DERIVED from the tape (x2hi_sim.extent), never from
    caller-maintained lo/hi.
  * Every pattern below is transcribed from lean/X2.lean by line number (cited).

Each matcher: given a Sim `s`, return (params, count, predicted_cells_delta, dpos, st')
or None.  `predicted_cells_delta` is a dict of ABSOLUTE cell -> bit that the theorem's
OUT asserts; cells not listed are asserted UNCHANGED.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2hi_sim import Sim, clone


def C(s, k):
    """cell at head-relative offset k."""
    return s.cells.get(s.pos + k, 0)


def run1(s, k):
    """length of the 1-run starting at head-relative offset k."""
    n = 0
    while C(s, k + n) == 1:
        n += 1
    return n


def pairs(s, k, a, b, maxn=10**9):
    """number of leading [a,b] pairs starting at head-relative offset k."""
    n = 0
    while n < maxn and C(s, k + 2 * n) == a and C(s, k + 2 * n + 1) == b:
        n += 1
    return n


def lpairs(s, k, a, b):
    """leading [a,b] pairs going LEFT (nearest-first) from head-relative offset k."""
    n = 0
    while C(s, k - 2 * n) == a and C(s, k - 2 * n - 1) == b:
        n += 1
    return n


# ---------------------------------------------------------------- the matchers
# Each returns (name, params, count, delta, dpos, st') or None.

def m_sweepEF(s):
    """X2.lean:229  sweepEF (m p L R):
       steps (2*m) <E,p,(L, false, pow10 m ++ R)>
         = some <E, p+2m, (ones (2m) ++ L, false, R)>"""
    if s.st != 'E' or C(s, 0) != 0:
        return None
    m = pairs(s, 1, 1, 0)
    if m < 1:
        return None
    d = {s.pos + j: 1 for j in range(0, 2 * m)}
    d[s.pos + 2 * m] = 0
    return ('sweepEF', {'m': m}, 2 * m, d, 2 * m, 'E')


def m_ecombChewFold(s):
    """X2.lean:1044  ecombChewFold (v p L R):
       steps (6*v) <E,p,(L, false, false :: (ones (2v+1) ++ R))>
         = some <E, p+2v, (pow01 v ++ L, false, false :: (ones 1 ++ R))>"""
    if s.st != 'E' or C(s, 0) != 0 or C(s, 1) != 0:
        return None
    n = run1(s, 2)
    v = (n - 1) // 2
    if v < 1:
        return None
    d = {s.pos + j: (1 if j % 2 == 0 else 0) for j in range(0, 2 * v)}
    d[s.pos + 2 * v] = 0
    d[s.pos + 2 * v + 1] = 0
    d[s.pos + 2 * v + 2] = 1
    return ('ecombChewFold', {'v': v}, 6 * v, d, 2 * v, 'E')


def m_ecfold(s):
    """X2.lean:1376  ecfold (t p M R):
       steps (2*(t+1)) <E,p,(ones (2t+1) ++ (false :: M), true, R)>
         = some <E, p-2(t+1), (M, false, pow10 (t+1) ++ R)>"""
    if s.st != 'E' or C(s, 0) != 1:
        return None
    n = 0
    while C(s, -1 - n) == 1:
        n += 1
    if n % 2 == 0 or n < 1:      # need ones(2t+1) then a 0 -> run length exactly odd
        return None
    t = (n - 1) // 2
    d = {s.pos - 2 * t - 1 + j: (1 if j % 2 == 0 else 0) for j in range(0, 2 * t + 2)}
    d[s.pos - 2 * t - 2] = 0
    return ('ecfold', {'t': t}, 2 * (t + 1), d, -2 * (t + 1), 'E')


def m_outer_tick(s):
    """X2.lean:1705  outer_tick_noCarry_at (p t M R):
       steps (4t+10) <E,p,(ones (2t+1) ++ (false :: M), false, true :: true :: R)>
         = some <E, p+2, (ones (2t+4) ++ M, false, R)>"""
    if s.st != 'E' or C(s, 0) != 0 or C(s, 1) != 1 or C(s, 2) != 1:
        return None
    n = 0
    while C(s, -1 - n) == 1:
        n += 1
    if n % 2 == 0:
        return None
    t = (n - 1) // 2
    d = {s.pos + j: 1 for j in range(-2 * t - 2, 2)}
    d[s.pos + 2] = 0
    return ('outer_tick_noCarry_at', {'t': t}, 4 * t + 10, d, 2, 'E')


def m_descent_std_tile(s):
    """X2.lean:5047  descent_std_tile (v p L R):
       steps (6v+3) <E,p,(L, false, false :: (ones (2v+1) ++ (false :: false :: R)))>
         = some <E, p+2v+3, (false::false::true::(pow01 v ++ L), false, false :: R)>"""
    if s.st != 'E' or C(s, 0) != 0 or C(s, 1) != 0:
        return None
    n = run1(s, 2)
    if n % 2 == 0 or n < 1:
        return None
    v = (n - 1) // 2
    if C(s, 2 + n) != 0 or C(s, 3 + n) != 0:
        return None
    d = {s.pos + j: (1 if j % 2 == 0 else 0) for j in range(0, 2 * v)}
    d[s.pos + 2 * v] = 1
    d[s.pos + 2 * v + 1] = 0
    d[s.pos + 2 * v + 2] = 0
    d[s.pos + 2 * v + 3] = 0
    d[s.pos + 2 * v + 4] = 0
    return ('descent_std_tile', {'v': v}, 6 * v + 3, d, 2 * v + 3, 'E')


def m_braid_entry(s):
    """X2.lean:5333  braid_entry (p L R):
       steps 2 <E,p,(L, false, true :: true :: R)>
         = some <E, p+2, (true :: true :: L, true, R)>"""
    if s.st != 'E' or C(s, 0) != 0 or C(s, 1) != 1 or C(s, 2) != 1:
        return None
    d = {s.pos: 1, s.pos + 1: 1, s.pos + 2: 1}
    return ('braid_entry', {}, 2, d, 2, 'E')


def m_braid_tile(s):
    """X2.lean:5348  braid_tile (r Lc blk p marker casc):
       steps (8r+10) <E,p,(pow10 (Lc+1) ++ marker, false,
                           pow10 (2r+1) ++ (ones (blk+2) ++ (false::false::casc)))>
         = some <E, p-2, (pow10 Lc ++ marker, false,
                          pow10 (2r+3) ++ (ones blk ++ (false::false::casc)))>"""
    if s.st != 'E' or C(s, 0) != 0:
        return None
    nl = lpairs(s, -1, 1, 0)          # pow10 (Lc+1) on the left
    if nl < 1:
        return None
    Lc = nl - 1
    q = pairs(s, 1, 1, 0)             # pow10 (2r+1) on the right
    if q < 1 or q % 2 == 0:
        return None
    r = (q - 1) // 2
    blk = run1(s, 2 * q + 1) - 2      # ones (blk+2)
    if blk < 0:
        return None
    e = 2 * q + 1 + blk + 2
    if C(s, e) != 0 or C(s, e + 1) != 0:
        return None
    d = {}
    for j in range(0, 2 * (2 * r + 3)):           # pow10 (2r+3) from p-1
        d[s.pos - 1 + j] = 1 if j % 2 == 0 else 0
    for j in range(0, blk):                       # ones blk
        d[s.pos + 4 * r + 5 + j] = 1
    d[s.pos + 4 * r + blk + 5] = 0
    d[s.pos + 4 * r + blk + 6] = 0
    d[s.pos - 2] = 0
    return ('braid_tile', {'r': r, 'Lc': Lc, 'blk': blk}, 8 * r + 10, d, -2, 'E')


def braidRunSteps(r, n):
    """X2.lean:5384"""
    tot = 0
    for i in range(n):
        tot += 8 * (r + i) + 10
    return tot


def m_braid_topgrind(s):
    """X2.lean:5621  braid_topgrind (N Lc p marker casc):
       steps (7 + braidRunSteps 0 N + (4N+4))
         <E,p,(pow01 (Lc+N) ++ marker, false,
               false::false::false::(ones (2N+1) ++ (false::false::casc)))>
         = some <E, p+5+2N, (ones (4N+4) ++ (pow10 Lc ++ (true::marker)), false,
                             false :: casc)>"""
    if s.st != 'E' or C(s, 0) != 0:
        return None
    if C(s, 1) != 0 or C(s, 2) != 0 or C(s, 3) != 0:
        return None
    n = run1(s, 4)
    if n % 2 == 0 or n < 1:
        return None
    N = (n - 1) // 2
    if C(s, 4 + n) != 0 or C(s, 5 + n) != 0:
        return None
    # left: pow01 (Lc+N) = [0,1] repeated, nearest-first
    tot = lpairs(s, -1, 0, 1)
    if tot < N:
        return None
    Lc = tot - N
    d = {}
    for j in range(-2 * N + 1, 2 * N + 5):        # ones (4N+4)
        d[s.pos + j] = 1
    for j in range(0, 2 * Lc):                    # pow10 Lc from p-2N
        d[s.pos - 2 * N - j] = 1 if j % 2 == 0 else 0
    d[s.pos - 2 * N - 2 * Lc] = 1                 # the `true` before marker
    d[s.pos + 2 * N + 5] = 0                      # head
    d[s.pos + 2 * N + 6] = 0
    cnt = 7 + braidRunSteps(0, N) + (4 * N + 4)
    return ('braid_topgrind', {'N': N, 'Lc': Lc}, cnt, d, 5 + 2 * N, 'E')


def m_descent_final_tile(s):
    """X2.lean:5930  descent_final_tile (p L R):
       steps 100 <E,p,(false::false::true::false::L, false,
                       false :: (ones 1 ++ (false::false::(zeros 7 ++ R))))>
         = some <E, p+8, (ones 12 ++ L, false, false::true::false::R)>"""
    if s.st != 'E' or C(s, 0) != 0:
        return None
    if [C(s, -1), C(s, -2), C(s, -3), C(s, -4)] != [0, 0, 1, 0]:
        return None
    if [C(s, 1), C(s, 2)] != [0, 1]:
        return None
    if any(C(s, 3 + i) != 0 for i in range(9)):
        return None
    d = {s.pos + j: 1 for j in range(-4, 8)}
    d[s.pos + 8] = 0
    d[s.pos + 9] = 0
    d[s.pos + 10] = 1
    d[s.pos + 11] = 0
    return ('descent_final_tile', {}, 100, d, 8, 'E')


def m_lowMiddle_fwd(s):
    """X2.lean:2969  lowMiddle_fwd (m p L Y):
       steps (29m) <E,p,(L, false, 1::0::1::0::0::1::(rcomb m ++ Y))>
         = some <E, p+7m, (rdepo m ++ L, false, 1::0::1::0::0::1::Y)>
       rcomb m = (0^6 1)^m  (X2.lean:2915);  rdepo m = (1 0 1 1 1 1 1)^m nearest-first."""
    if s.st != 'E' or C(s, 0) != 0:
        return None
    if [C(s, i) for i in range(1, 7)] != [1, 0, 1, 0, 0, 1]:
        return None
    m = 0
    while [C(s, 7 + 7 * m + i) for i in range(7)] == [0, 0, 0, 0, 0, 0, 1]:
        m += 1
    if m < 1:
        return None
    d = {}
    for i in range(m):                            # rdepo m, nearest-first from p+7m-1
        for j, b in enumerate([1, 0, 1, 1, 1, 1, 1]):
            d[s.pos + 7 * m - 1 - (7 * i + j)] = b
    d[s.pos + 7 * m] = 0
    for i, b in enumerate([1, 0, 1, 0, 0, 1]):
        d[s.pos + 7 * m + 1 + i] = b
    return ('lowMiddle_fwd', {'m': m}, 29 * m, d, 7 * m, 'E')


def _fixed(name, count, lpat, rpat, dpos, out_l, out_r):
    """build a matcher for a FIXED (∀ L R) pattern given as head-relative lists."""
    def f(s):
        if s.st != 'E' or C(s, 0) != 0:
            return None
        for i, b in enumerate(lpat):
            if C(s, -1 - i) != b:
                return None
        for i, b in enumerate(rpat):
            if C(s, 1 + i) != b:
                return None
        d = {}
        for i, b in enumerate(out_l):
            d[s.pos + dpos - 1 - i] = b
        d[s.pos + dpos] = 0
        for i, b in enumerate(out_r):
            d[s.pos + dpos + 1 + i] = b
        return (name, {}, count, d, dpos, 'E')
    return f


# X2.lean:4219 regen4_transport  (= carry_exit_j3, exitSteps 4 = 70)
m_regen4 = _fixed(
    'regen4_transport', 70,
    [1] * 12 + [1, 0, 1, 0, 0, 1, 0],
    [0, 1] + [0] * 11,
    -16,
    [0, 1, 0],
    [0, 0, 0] + [1] * 13 + [0, 0] + [1] * 5 + [0, 0, 1, 0, 0, 0],
)

# X2.lean:4235 regen5_transport  (= carry_exit_j4, exitSteps 5 = 218)
m_regen5 = _fixed(
    'regen5_transport', 218,
    [1] * 28 + [1, 0, 1, 0, 0],
    [0] + [1] * 5 + [0, 0, 1] + [0] * 17,
    -32,
    [0],
    [0, 0, 0] + [1] * 29 + [0, 0] + [1] * 13 + [0, 0] + [1] * 5 + [0, 0, 1, 0],
)

# X2.lean:6513 regen6_transport  (exitSteps 6 = 722)
m_regen6 = _fixed(
    'regen6_transport', 722,
    [1] * 61 + [0, 1, 0, 0, 1],
    [0] + [1] * 13 + [0, 0] + [1] * 5 + [0, 0, 1] + [0] * 34,
    -64,
    [0, 1],
    [0, 0, 0] + [1] * 61 + [0, 0] + [1] * 29 + [0, 0] + [1] * 13
    + [0, 0] + [1] * 5 + [0, 0] + [1] + [0, 0],
)

# X2.lean:7578 regen7_factored  (exitSteps 7 = 2530)
m_regen7 = _fixed(
    'regen7_factored', 2530,
    [1] * 125 + [0, 1, 0, 0, 1],
    [0] + [1] * 29 + [0, 0] + [1] * 13 + [0, 0] + [1] * 5 + [0, 0, 1] + [0] * 66,
    -128,
    [0, 1],
    [0, 0, 0] + [1] * 125 + [0, 0] + [1] * 61 + [0, 0] + [1] * 29 + [0, 0]
    + [1] * 13 + [0, 0] + [1] * 5 + [0, 0] + [1] + [0, 0],
)

MATCHERS = [
    m_regen7, m_regen6, m_regen5, m_regen4, m_braid_topgrind, m_descent_final_tile,
    m_lowMiddle_fwd, m_braid_tile, m_descent_std_tile, m_outer_tick, m_ecombChewFold,
    m_sweepEF, m_ecfold, m_braid_entry,
]


def verify(s, cand):
    """Run the machine `count` steps from `s` and CHECK the theorem's asserted OUT
    cell-for-cell.  Returns True iff the real orbit agrees with the theorem."""
    name, params, count, delta, dpos, st1 = cand
    if count < 1:
        return False
    t = clone(s)
    for _ in range(count):
        if not t.step():
            return False
    if t.st != st1 or t.pos != s.pos + dpos:
        return False
    exp = dict(s.cells)
    for k, b in delta.items():
        if b:
            exp[k] = 1
        else:
            exp.pop(k, None)
    return t.cells == exp


def best(s):
    """the applicable, VERIFIED theorem instance with the largest step count."""
    out = None
    for m in MATCHERS:
        c = m(s)
        if c is None:
            continue
        if out is not None and c[2] <= out[2]:
            continue
        if verify(s, c):
            out = c
    return out


def selfcheck():
    """Transcription self-check: instantiate each lemma's IN pattern with SEVERAL
    tails and confirm the machine reproduces the asserted OUT.  A pattern that is
    mis-transcribed fails here."""
    import random
    random.seed(7)
    print('=== lemma transcription self-check (IN pattern -> machine -> OUT) ===')
    cases = []

    def mk(cells, pos=0, st='E'):
        s = Sim()
        s.st, s.pos = st, pos
        s.cells = {k: v for k, v in cells.items() if v}
        return s

    for trial in range(200):
        L = {-1 - i: random.randint(0, 1) for i in range(60)}
        R = {}
        for name, build in [
            ('sweepEF', lambda m: {**{1 + j: (1 if j % 2 == 0 else 0) for j in range(2 * m)},
                                   **{2 * m + 1 + i: random.randint(0, 1) for i in range(20)}}),
        ]:
            pass
    # exhaustive small-parameter sweep with random tails
    ok = True
    stats = {}
    for trial in range(400):
        tail = {200 + i: random.randint(0, 1) for i in range(30)}
        lt = {-200 - i: random.randint(0, 1) for i in range(30)}
        for m in MATCHERS:
            pass
    # -- direct: build each lemma's IN config explicitly
    def chk(name, cells, want_name, pos=0):
        nonlocal ok
        s = mk(cells, pos=pos)
        c = None
        for mm in MATCHERS:
            r = mm(s)
            if r and r[0] == want_name:
                c = r
                break
        if c is None:
            print('  %-24s NO MATCH' % name)
            ok = False
            return
        good = verify(s, c)
        stats[want_name] = stats.get(want_name, 0) + (1 if good else 0)
        if not good:
            print('  %-24s OUT MISMATCH  params=%s count=%d' % (name, c[1], c[2]))
            ok = False

    for m in range(1, 8):
        cells = {1 + j: (1 if j % 2 == 0 else 0) for j in range(2 * m)}
        cells[2 * m + 1] = 1; cells[2 * m + 2] = 1     # R tail
        chk('sweepEF m=%d' % m, cells, 'sweepEF')

    for v in range(1, 8):
        cells = {1: 0}
        for j in range(2 * v + 1):
            cells[2 + j] = 1
        cells[2 + 2 * v + 1] = 0; cells[2 + 2 * v + 2] = 1
        chk('ecombChewFold v=%d' % v, cells, 'ecombChewFold')

    for t in range(0, 8):
        cells = {0: 1}
        for i in range(2 * t + 1):
            cells[-1 - i] = 1
        cells[-2 - 2 * t] = 0
        cells[1] = 1; cells[2] = 0
        chk('ecfold t=%d' % t, cells, 'ecfold')

    for t in range(0, 8):
        cells = {}
        for i in range(2 * t + 1):
            cells[-1 - i] = 1
        cells[-2 - 2 * t] = 0
        cells[1] = 1; cells[2] = 1
        cells[3] = 1; cells[4] = 0
        chk('outer_tick t=%d' % t, cells, 'outer_tick_noCarry_at')

    for v in range(0, 8):
        cells = {1: 0}
        for j in range(2 * v + 1):
            cells[2 + j] = 1
        cells[3 + 2 * v] = 0; cells[4 + 2 * v] = 0
        cells[5 + 2 * v] = 1
        chk('descent_std_tile v=%d' % v, cells, 'descent_std_tile')

    for N in range(1, 7):
        cells = {1: 0, 2: 0, 3: 0}
        for j in range(2 * N + 1):
            cells[4 + j] = 1
        cells[5 + 2 * N] = 0; cells[6 + 2 * N] = 0
        cells[7 + 2 * N] = 1                      # casc
        for j in range(2 * (N + 3)):              # pow01 (Lc+N), Lc=3
            cells[-1 - j] = 0 if j % 2 == 0 else 1
        cells[-1 - 2 * (N + 3)] = 1               # marker
        chk('braid_topgrind N=%d' % N, cells, 'braid_topgrind')

    cells = {-1: 0, -2: 0, -3: 1, -4: 0, 1: 0, 2: 1}
    for i in range(9):
        cells[3 + i] = 0
    cells[12] = 1
    chk('descent_final_tile', cells, 'descent_final_tile')

    for m in range(1, 6):
        cells = {}
        for i, b in enumerate([1, 0, 1, 0, 0, 1]):
            cells[1 + i] = b
        for i in range(m):
            for j, b in enumerate([0, 0, 0, 0, 0, 0, 1]):
                cells[7 + 7 * i + j] = b
        cells[7 + 7 * m] = 1; cells[8 + 7 * m] = 1
        chk('lowMiddle_fwd m=%d' % m, cells, 'lowMiddle_fwd')

    for r in range(0, 6):
        for blk in range(0, 5):
            q = 2 * r + 1
            cells = {}
            for j in range(2 * q):
                cells[1 + j] = 1 if j % 2 == 0 else 0
            for j in range(blk + 2):
                cells[1 + 2 * q + j] = 1
            cells[1 + 2 * q + blk + 2] = 0
            cells[2 + 2 * q + blk + 2] = 0
            cells[3 + 2 * q + blk + 2] = 1
            for j in range(2 * 4):                 # pow10 (Lc+1), Lc=3
                cells[-1 - j] = 1 if j % 2 == 0 else 0
            cells[-1 - 8] = 1
            chk('braid_tile r=%d blk=%d' % (r, blk), cells, 'braid_tile')

    # regen4 / regen5 / regen6 / regen7: the FIXED patterns, several tails
    fixedcases = [
        ('regen4_transport', [1] * 12 + [1, 0, 1, 0, 0, 1, 0], [0, 1] + [0] * 11),
        ('regen5_transport', [1] * 28 + [1, 0, 1, 0, 0],
         [0] + [1] * 5 + [0, 0, 1] + [0] * 17),
        ('regen6_transport', [1] * 61 + [0, 1, 0, 0, 1],
         [0] + [1] * 13 + [0, 0] + [1] * 5 + [0, 0, 1] + [0] * 34),
        ('regen7_factored', [1] * 125 + [0, 1, 0, 0, 1],
         [0] + [1] * 29 + [0, 0] + [1] * 13 + [0, 0] + [1] * 5 + [0, 0, 1] + [0] * 66),
    ]
    for tl, tr in [(0, 0), (1, 1), (1, 0)]:
        for nm, lpat, rpat in fixedcases:
            cells = {}
            for i, b in enumerate(lpat):
                cells[-1 - i] = b
            for i, b in enumerate(rpat):
                cells[1 + i] = b
            cells[-1 - len(lpat)] = tl
            cells[1 + len(rpat)] = tr
            chk('%s tails=%d%d' % (nm, tl, tr), cells, nm)
    for tl, tr in []:
        lpat = [1] * 12 + [1, 0, 1, 0, 0, 1, 0]
        rpat = [0, 1] + [0] * 11
        cells = {}
        for i, b in enumerate(lpat):
            cells[-1 - i] = b
        for i, b in enumerate(rpat):
            cells[1 + i] = b
        cells[-1 - len(lpat)] = tl
        cells[1 + len(rpat)] = tr
        chk('regen4_transport tails=%d%d' % (tl, tr), cells, 'regen4_transport')

        lpat = [1] * 28 + [1, 0, 1, 0, 0]
        rpat = [0] + [1] * 5 + [0, 0, 1] + [0] * 17
        cells = {}
        for i, b in enumerate(lpat):
            cells[-1 - i] = b
        for i, b in enumerate(rpat):
            cells[1 + i] = b
        cells[-1 - len(lpat)] = tl
        cells[1 + len(rpat)] = tr
        chk('regen5_transport tails=%d%d' % (tl, tr), cells, 'regen5_transport')

    print('  verified OUT for: %s' % sorted(stats))
    print('SELFCHECK: %s' % ('PASS' if ok else 'FAIL'))
    return ok


if __name__ == '__main__':
    sys.exit(0 if selfcheck() else 1)
