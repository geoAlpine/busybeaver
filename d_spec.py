#!/usr/bin/env python3
"""d_spec.py -- cell-resolved SPEC instrument for BB(6) holdout D.

D  = 1RB0RA_1LC0LE_0LD0LB_1RA0LF_1LB0RD_1LD---        (TNF form, 1104 list)
D^R= 1LB0LA_1RC0RE_0RD0RB_1LA0RF_1RB0LD_1RD---        (mirror; L<->R)

PURPOSE: produce the exact milestone family (BOTH tape sides), the epoch phase
decomposition with exact step spans and cell-resolved IN/OUT configs, the
anti-vacuity anchors, and the entry segment, in the `zeros`/`ones`/`pow10`/
`pow01` vocabulary of lean/TapeCalc.lean + lean/O3.lean, so a Lean development
can be written from it.

DISCIPLINE: every printed claim is a MEASUREMENT.  D is [OPEN].  Nothing here
decides D.  `check_anchors()` must reproduce PUBLISHED fingerprints (and a
CONTROL that SHOULD fail must fail) before any other output is trusted.

Vocabulary (matches Lean):
    zeros n = 0^n            ones n  = 1^n
    pow10 n = (1 0)^n        pow01 n = (0 1)^n
Tape convention (TapeCalc.Tape): `left` is stored NEAREST-CELL-FIRST, i.e. the
left word printed here as L = [l0, l1, ...] has l0 = cell at pos-1.

Usage:
    d_spec.py anchors            # self-validation, incl. a control that must FAIL
    d_spec.py milestones [N]     # milestone family, both sides, both parities
    d_spec.py epoch K            # phase decomposition of M1(K) -> M1(K+1)
    d_spec.py entry              # blank tape -> first milestone
    d_spec.py ladder [N]         # (2,4) width/time ladder (x2 control + D)
"""
import sys

# ------------------------------------------------------------------ machines
SPEC_D = "1RB0RA_1LC0LE_0LD0LB_1RA0LF_1LB0RD_1LD---"
SPEC_X2 = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
ST = "ABCDEF"


def parse(spec):
    """spec -> table[state][read] = (write, dir(+1=R,-1=L), next) or None (HALT)."""
    T = []
    for blk in spec.split('_'):
        row = []
        for k in (0, 3):
            f = blk[k:k + 3]
            row.append(None if f[0] == '-' else (int(f[0]), 1 if f[1] == 'R' else -1,
                                                 ord(f[2]) - 65))
        T.append(row)
    return T


def mirror(spec):
    """L<->R in every transition (the reversed machine)."""
    out = []
    for blk in spec.split('_'):
        nb = ''
        for k in (0, 3):
            f = blk[k:k + 3]
            if f[0] == '-':
                nb += f
            else:
                nb += f[0] + ('L' if f[1] == 'R' else 'R') + f[2]
        out.append(nb)
    return '_'.join(out)


SPAN = 1 << 22


class Sim:
    def __init__(self, spec):
        self.T = parse(spec)
        self.tape = bytearray(2 * SPAN)
        self.pos = SPAN
        self.st = 0
        self.t = 0
        self.mn = 0
        self.mx = 0
        self.halted = False

    def run(self, n):
        """advance n steps; returns number actually taken."""
        T, tape = self.T, self.tape
        pos, st = self.pos, self.st
        mn, mx = self.mn, self.mx
        for i in range(n):
            e = T[st][tape[pos]]
            if e is None:
                self.halted = True
                self.pos, self.st, self.mn, self.mx = pos, st, mn, mx
                self.t += i
                return i
            w, d, st = e
            tape[pos] = w
            pos += d
            r = pos - SPAN
            if r > mx:
                mx = r
            elif r < mn:
                mn = r
        self.pos, self.st, self.mn, self.mx = pos, st, mn, mx
        self.t += n
        return n

    def run_to(self, T_):
        assert T_ >= self.t
        self.run(T_ - self.t)

    # ---- observation -------------------------------------------------
    @property
    def rel(self):
        return self.pos - SPAN

    def cell(self, r):
        return self.tape[SPAN + r]

    def bits(self, a, b):
        """bits on [a,b] inclusive, relative coordinates."""
        return list(self.tape[SPAN + a:SPAN + b + 1])

    def left_word(self, depth=None):
        """TapeCalc `left`: nearest-first, from pos-1 down to mn (or depth cells)."""
        lo = self.mn if depth is None else max(self.mn, self.rel - depth)
        return [self.tape[SPAN + r] for r in range(self.rel - 1, lo - 1, -1)]

    def right_word(self, depth=None):
        hi = self.mx if depth is None else min(self.mx, self.rel + depth)
        return [self.tape[SPAN + r] for r in range(self.rel + 1, hi + 1)]

    def head(self):
        return self.cell(self.rel)

    def cfg(self):
        return (ST[self.st], self.rel, tuple(self.left_word()), self.head(),
                tuple(self.right_word()))


# ------------------------------------------------------------------ words
def rle(bits):
    out = []
    for b in bits:
        if out and out[-1][0] == b:
            out[-1][1] += 1
        else:
            out.append([b, 1])
    return [(b, n) for b, n in out]


def word(bits):
    """Render a bit list in the Lean vocabulary zeros/ones/pow10/pow01.

    Greedy, deterministic: at each position, prefer the longest (10)^n or (01)^n
    with n>=2, else a maximal constant run.  Trailing 0s are folded into `zeros`.
    """
    toks = []
    i, n = 0, len(bits)
    while i < n:
        # (1 0)^m
        m = 0
        while i + 2 * m + 1 < n and bits[i + 2 * m] == 1 and bits[i + 2 * m + 1] == 0:
            m += 1
        if m >= 2:
            toks.append(f"pow10 {m}")
            i += 2 * m
            continue
        # (0 1)^m
        m = 0
        while i + 2 * m + 1 < n and bits[i + 2 * m] == 0 and bits[i + 2 * m + 1] == 1:
            m += 1
        if m >= 2:
            toks.append(f"pow01 {m}")
            i += 2 * m
            continue
        b = bits[i]
        j = i
        while j < n and bits[j] == b:
            j += 1
        toks.append(f"{'ones' if b else 'zeros'} {j - i}")
        i = j
    return " ++ ".join(toks) if toks else "[]"


def rle_str(bits, maxruns=40):
    r = rle(bits)
    s = " ".join(f"{b}^{n}" for b, n in r[:maxruns])
    if len(r) > maxruns:
        s += f" ... (+{len(r)-maxruns} runs)"
    return s


# ------------------------------------------------------------------ frontier records
def frontier_records(spec, N, side='L'):
    """Return [(t, st, pos, width)] at every new frontier record on `side`."""
    T = parse(spec)
    tape = bytearray(2 * SPAN)
    pos, st = SPAN, 0
    mn = mx = 0
    rec = []
    for t in range(1, N + 1):
        e = T[st][tape[pos]]
        if e is None:
            break
        w, d, st = e
        tape[pos] = w
        pos += d
        r = pos - SPAN
        if r > mx:
            mx = r
            if side == 'R':
                rec.append((t, st, r, mx - mn))
        elif r < mn:
            mn = r
            if side == 'L':
                rec.append((t, st, r, mx - mn))
    return rec


def cluster(rec, factor=1.0):
    """Keep the FIRST record of each cluster: rec[i] starts a cluster when the
    gap to the previous record exceeds factor * (previous record time)."""
    idx = [i for i in range(len(rec)) if i == 0 or rec[i][0] - rec[i - 1][0] > factor * rec[i - 1][0]]
    return [rec[i] for i in idx]


SPEC_DR = mirror(SPEC_D)

# Milestone times M1(k) at head pos -8k, measured on D^R (see D_SPEC_2026-07-26.md).
M1_T = {1: 894, 2: 14130, 3: 66906, 4: 291168, 5: 1196412, 6: 4846662, 7: 19488198}


def dump_at(spec, t, label="", maxruns=60, depth=None):
    s = Sim(spec)
    s.run(t)
    L = s.left_word(depth)
    R = s.right_word(depth)
    print(f"--- {label} t={t}  state={ST[s.st]}  pos={s.rel}  head={s.head()}"
          f"  [mn={s.mn}, mx={s.mx}, width={s.mx-s.mn}]")
    print(f"    L (nearest-first) = {rle_str(L, maxruns)}")
    print(f"    L word            = {word(L)}")
    print(f"    R                 = {rle_str(R, maxruns)}")
    print(f"    R word            = {word(R)}")
    return s


def tokens(bits):
    """Same greedy parse as `word`, returned as data: [(kind, n), ...] with
    kind in {'0','1','10','01'}."""
    out = []
    i, n = 0, len(bits)
    while i < n:
        m = 0
        while i + 2 * m + 1 < n and bits[i + 2 * m] == 1 and bits[i + 2 * m + 1] == 0:
            m += 1
        if m >= 2:
            out.append(('10', m)); i += 2 * m; continue
        m = 0
        while i + 2 * m + 1 < n and bits[i + 2 * m] == 0 and bits[i + 2 * m + 1] == 1:
            m += 1
        if m >= 2:
            out.append(('01', m)); i += 2 * m; continue
        b = bits[i]; j = i
        while j < n and bits[j] == b:
            j += 1
        out.append(('1' if b else '0', j - i)); i = j
    return out


def milestone_scan(N, kmax=99, spec=None):
    """One pass over D^R.  A MILESTONE is: a new LEFT-frontier record reached in
    state A at pos = -8k (k>=1).  Prints t, k, and the FULL right word.
    Returns [(k, t, pos, width, tokens)]."""
    spec = spec or SPEC_DR
    T = parse(spec)
    tape = bytearray(2 * SPAN)
    pos, st = SPAN, 0
    mn = mx = 0
    out = []
    for t in range(1, N + 1):
        e = T[st][tape[pos]]
        if e is None:
            print(f"HALT at {t}"); break
        w, d, st = e
        tape[pos] = w
        pos += d
        r = pos - SPAN
        if r > mx:
            mx = r
        elif r < mn:
            mn = r
            if st == 0 and r % 8 == 0:
                k = -r // 8
                R = [tape[SPAN + q] for q in range(r + 1, mx + 1)]
                tk = tokens(R)
                out.append((k, t, r, mx - mn, tk))
                print(f"M1({k})  t={t}  pos={r}  width={mx-mn}  |R|={len(R)}")
                print("      R = " + " ++ ".join(
                    {'0': 'zeros', '1': 'ones', '10': 'pow10', '01': 'pow01'}[a] + f" {b}"
                    for a, b in tk), flush=True)
                if k >= kmax:
                    break
    return out


def compress_rle(rl):
    """RLE -> compact string, collapsing period-2 alternations as [a^i b^j]xN."""
    out, i = [], 0
    while i < len(rl):
        k = i
        while k + 2 < len(rl) and rl[k + 2] == rl[i] and \
              (k + 3 >= len(rl) or rl[k + 3] == rl[i + 1]):
            k += 2
        if k - i >= 4:
            out.append(f"[{rl[i][0]}^{rl[i][1]} {rl[i+1][0]}^{rl[i+1][1]}]x{(k-i)//2+1}")
            i = k + 2
        else:
            out.append(f"{rl[i][0]}^{rl[i][1]}")
            i += 1
    return " ".join(out)


def epoch_decompose(k, verbose=True):
    """Decompose epoch M1(k) -> M1(k+1) into LOW / ENTRY / LADDER / TAIL.

    Rung boundary := a new RIGHT-frontier record set in state D (head then reads 0,
    right side blank).  Returns a dict of measurements."""
    t0, t1 = M1_T[k], M1_T[k + 1]
    s = Sim(SPEC_DR)
    s.run(t0)
    T, tape = s.T, s.tape
    pos, st, mx, mn = s.pos, s.st, s.mx, s.mn
    wall = -8 * k
    rungs = []          # (t, pos)
    last_at_wall = t0   # last time pos <= wall+1  -> end of LOW phase
    for t in range(t0 + 1, t1 + 1):
        e = T[st][tape[pos]]
        w, d, st = e
        tape[pos] = w
        pos += d
        r = pos - SPAN
        if r <= wall + 1:
            last_at_wall = t
        if r > mx:
            mx = r
            if st == 3:                      # state D
                rungs.append((t, r))
    spans = [rungs[i + 1][0] - rungs[i][0] for i in range(len(rungs) - 1)]
    d = dict(k=k, t0=t0, t1=t1, span=t1 - t0, low_end=last_at_wall,
             low_len=last_at_wall - t0, n_rungs=len(rungs),
             rung0=rungs[0], rungN=rungs[-1],
             entry_len=rungs[0][0] - last_at_wall,
             ladder_len=rungs[-1][0] - rungs[0][0],
             tail_len=t1 - rungs[-1][0],
             spans=spans)
    if verbose:
        print(f"=== epoch M1({k}) -> M1({k+1}):  t {t0} -> {t1}   span {t1-t0}")
        print(f"  P1 LOW    {t0} -> {last_at_wall}      len {last_at_wall-t0}")
        print(f"  P2 ENTRY  {last_at_wall} -> {rungs[0][0]}   len {rungs[0][0]-last_at_wall}"
              f"   (first rung boundary at pos {rungs[0][1]})")
        print(f"  P3 LADDER {rungs[0][0]} -> {rungs[-1][0]}  len {rungs[-1][0]-rungs[0][0]}"
              f"   rungs={len(rungs)}  pos {rungs[0][1]} -> {rungs[-1][1]}")
        if spans:
            diffs = sorted(set(spans[i + 1] - spans[i] for i in range(len(spans) - 1)))
            print(f"     rung spans: first={spans[0]} last={spans[-1]} "
                  f"increments={diffs}")
        print(f"  P4 TAIL   {rungs[-1][0]} -> {t1}   len {t1-rungs[-1][0]}")
    return d


def a_peaks(k, spec=None):
    """All local maxima of the head position reached in state A during epoch k."""
    spec = spec or SPEC_DR
    t0, t1 = M1_T[k], M1_T[k + 1]
    s = Sim(spec); s.run(t0)
    T, tape = s.T, s.tape
    pos, st = s.pos, s.st
    tops = []; prevd = 0
    for t in range(t0 + 1, t1 + 1):
        e = T[st][tape[pos]]
        w, d, st = e; tape[pos] = w; pos += d
        if d != prevd:
            if d == -1 and st == 0:
                tops.append((t, pos - SPAN))
            prevd = d
    return tops


def segments(k, minlen=3):
    """Split the A-peak sequence of epoch k into maximal LADDER SEGMENTS: runs of
    consecutive peaks with peak-increment exactly +3.  Returns
    [(i0, i1, t_start, t_end, p_start, p_end, nrungs, span0, incs)]."""
    tops = a_peaks(k)
    segs = []; i = 0
    while i < len(tops):
        j = i
        while j + 1 < len(tops) and tops[j + 1][1] - tops[j][1] == 3:
            j += 1
        if j - i + 1 >= minlen:
            sp = [tops[q + 1][0] - tops[q][0] for q in range(i, j)]
            incs = sorted(set(sp[q + 1] - sp[q] for q in range(len(sp) - 1)))
            segs.append((i, j, tops[i][0], tops[j][0], tops[i][1], tops[j][1],
                         j - i + 1, sp[0] if sp else None, incs,
                         tops[j][0] - tops[i][0]))
        i = j + 1
    return segs, tops


def segment_report(k):
    segs, tops = segments(k)
    t0, t1 = M1_T[k], M1_T[k + 1]
    print(f"=== epoch M1({k})->M1({k+1})  t {t0}->{t1}  span {t1-t0}   "
          f"A-peaks={len(tops)}  ladder segments={len(segs)}")
    print("   seg  peaks            rungs  span0   inc     ladder-steps   t-range")
    prev = t0
    for n, (i0, i1, ta, tb, pa, pb, nr, s0, incs, tot) in enumerate(segs):
        print(f"   S{n}   {pa:>6} -> {pb:<6}  {nr:>5}  {s0:>6}  {str(incs):<7} "
              f"{tot:>12}   [{ta} .. {tb}]  gap-in={ta-prev}")
        prev = tb
    print(f"   tail after last segment: {t1-prev}")
    return segs


# ---------------------------------------------------------------- rung tile
def parse_apeak(s):
    """Parse the config at an A-peak of rung r=0 of a segment.

    Expected (Lnear = nearest-first):
        L = 1 1 ++ (0 1)^M ++ 0 0 ++ 1 ++ TAIL
        R = 1 ++ 0^g ++ REST
    Returns (M, g, tailrle, restrle) or None if the shape does not match."""
    L = rle(s.left_word()); R = rle(s.right_word())
    if not L or L[0] != (1, 2):
        return None
    i, M = 1, 0
    while i + 1 < len(L) and L[i] == (0, 1) and L[i + 1] == (1, 1):
        M += 1; i += 2
    if i >= len(L) or L[i] != (0, 2):
        return None
    tail = L[i + 1:]
    if not R or R[0] != (1, 1):
        return None
    if len(R) == 1:
        g, rest = 0, []
    elif R[1][0] == 0:
        g, rest = R[1][1], R[2:]
    else:
        return None
    return M, g, tail, rest


def validate_rung_law(ks=(2, 3, 4, 5, 6), law=lambda M: 6 * M + 15):
    """CHECK the two measured laws on EVERY ladder segment of every epoch:
         (i)  rung span at index r  =  law(M) + 6 r
         (ii) number of rungs        =  min(M + 2, g/3 + 1)   (g=0 <=> main segment)
    Returns (n_checked, failures)."""
    fails = []; n = 0
    for k in ks:
        segs, tops = segments(k)
        for si, (i0, i1, ta, tb, pa, pb, nr, s0, incs, tot) in enumerate(segs):
            s = Sim(SPEC_DR); s.run(ta)
            p = parse_apeak(s)
            n += 1
            if p is None:
                fails.append((k, si, 'SHAPE-MISMATCH', None)); continue
            M, g, tail, rest = p
            if s0 != law(M):
                fails.append((k, si, f'span0 {s0} != law({M})={law(M)}', (M, g)))
            want = M + 2 if not rest else g // 3 + 1
            if nr != want:
                fails.append((k, si, f'nrungs {nr} != {want}', (M, g, bool(rest))))
    return n, fails


def parse_rung(s):
    """Parse an A-peak config against the UNIVERSAL rung shape

        L(nearest-first) = (1 0)^u ++ [1,1] ++ (0 1)^m ++ [0,0] ++ 1^c ++ TAIL
        R                = [1] ++ 0^g ++ REST
        state A, head 0

    Returns dict(u,m,c,g,tail,rest) or None."""
    if s.st != 0 or s.head() != 0:
        return None
    L = rle(s.left_word()); R = rle(s.right_word())
    i, u = 0, 0
    while i + 1 < len(L) and L[i] == (1, 1) and L[i + 1] == (0, 1):
        u += 1; i += 2
    if i >= len(L) or L[i] != (1, 2):
        return None
    i += 1
    m = 0
    while i + 1 < len(L) and L[i] == (0, 1) and L[i + 1] == (1, 1):
        m += 1; i += 2
    if i >= len(L) or L[i] != (0, 2):
        return None
    i += 1
    if i >= len(L) or L[i][0] != 1:
        return None
    c = L[i][1]; tail = L[i + 1:]
    if not R or R[0] != (1, 1):
        return None
    if len(R) == 1:
        g, rest = 0, []
    elif R[1][0] == 0:
        g, rest = R[1][1], R[2:]
    else:
        return None
    return dict(u=u, m=m, c=c, g=g, tail=tail, rest=rest)


def validate(ks=(2, 3, 4, 5, 6), span_law=lambda u, m: 6 * (u + m) + 15,
             rung_law=lambda m, g, rest: min(m + 2, g // 3 + 1) if rest else m + 2,
             quiet=False):
    """Check the two universal laws on EVERY ladder segment of epochs `ks`.
    Returns (n_segments, n_parsed, failures)."""
    fails = []; n = 0; parsed = 0
    for k in ks:
        segs, tops = segments(k)
        for si, (i0, i1, ta, tb, pa, pb, nr, s0, incs, tot) in enumerate(segs):
            n += 1
            s = Sim(SPEC_DR); s.run(ta)
            p = parse_rung(s)
            if p is None:
                fails.append((k, si, 'SHAPE-MISMATCH (not the universal rung shape)',
                              f'state={ST[s.st]} head={s.head()} pos={s.rel}'))
                continue
            parsed += 1
            want_s = span_law(p['u'], p['m'])
            if s0 != want_s:
                fails.append((k, si, f"span0 {s0} != {want_s}",
                              f"u={p['u']} m={p['m']}"))
            want_n = rung_law(p['m'], p['g'], p['rest'])
            if nr != want_n:
                fails.append((k, si, f"nrungs {nr} != {want_n}",
                              f"m={p['m']} g={p['g']} rest={bool(p['rest'])}"))
            if incs not in ([6], []):
                fails.append((k, si, f"span increments {incs} != [6]", None))
    if not quiet:
        print(f"segments={n}  parsed as universal rung={parsed}  failures={len(fails)}")
        for f in fails:
            print("   FAIL", f)
    return n, parsed, fails


M1_T[8] = 78148404
M1_T[9] = 312959448


def ladder_fingerprint(spec, N, name=""):
    """Reproduce candD_deep.py's (2,4) ladder fingerprint: cluster frontier records
    by relative gap and report the width / time ratios of the last clusters."""
    T = parse(spec)
    tape = bytearray(2 * SPAN)
    pos, st = SPAN, 0
    mn = mx = 0
    recL, recR = [], []
    status = 'RUN'
    for t in range(1, N + 1):
        e = T[st][tape[pos]]
        if e is None:
            status = f'HALT@{t}'; break
        w, d, st = e
        tape[pos] = w
        pos += d
        r = pos - SPAN
        if r > mx:
            mx = r; recR.append((t, mx - mn))
        elif r < mn:
            mn = r; recL.append((t, mx - mn))
    print(f"=== {name} [{status}] N={N}")
    for side, rec in (('L', recL), ('R', recR)):
        for f in (0.25, 1.0, 2.0):
            if len(rec) < 4:
                continue
            idx = [i for i in range(len(rec))
                   if i == 0 or rec[i][0] - rec[i - 1][0] > f * rec[i - 1][0]]
            ws = [rec[i][1] for i in idx][-8:]; ts = [rec[i][0] for i in idx][-8:]
            if len(ws) < 4:
                continue
            wr = [round(ws[i + 1] / ws[i], 4) for i in range(len(ws) - 1) if ws[i]]
            tr = [round(ts[i + 1] / ts[i], 3) for i in range(len(ts) - 1) if ts[i]]
            print(f"  {side} gap>{f}t  ws={ws}\n        w={wr}\n        t={tr}", flush=True)


# ---------------------------------------------------------------- milestone family
def a_of(k):   return 39 * 2 ** (k - 1) - 4          # last comb length
def G_of(k):   return 57 * 2 ** (k - 3) - 3 * k + 9  # gap before the last comb (k>=4)
def w_of(k):   return 117 * 2 ** (k - 1) + 3 * k - 55  # milestone width


def milestone_word(k):
    """PREDICTED right word at M1(k), as a token list [('0',n)|('10',n)|('1',n)].
    Built ONLY from the closed forms; k >= 4."""
    blocks = []                       # (gap, comb) left-to-right
    # from the end: j = 1 is the last block
    jmax = k // 2 if k % 2 == 0 else (k - 1) // 2
    for j in range(jmax, 1, -1):      # j = jmax .. 2  (left to right)
        e = k - 2 * j
        if e == 0:
            blocks.append((33, 66))                       # even bottom
        elif e == 1:
            blocks.append((60, 132))                      # odd bottom
        else:
            blocks.append((33 * 2 ** (e - 1) + 12, 66 * 2 ** e))
    if k % 2 == 1:
        blocks = [(2, 4), (5, 15)] + blocks
    blocks.append((G_of(k), a_of(k)))
    toks = []
    for g, c in blocks:
        toks.append(('0', g)); toks.append(('10', c))
    toks.append(('1', 1))
    return toks


def check_milestone_family(ks=(4, 5, 6, 7, 8, 9), pred=milestone_word):
    """Compare the PREDICTED milestone word against the measured one."""
    meas = {}
    s = Sim(SPEC_DR)
    ok = []
    for k in sorted(ks):
        s2 = Sim(SPEC_DR); s2.run(M1_T[k])
        tk = tokens(s2.right_word())
        meas[k] = tk
        p = pred(k)
        agree = (tk == p) and s2.st == 0 and s2.rel == -8 * k and s2.left_word() == [] \
                and s2.head() == 0
        ok.append((k, agree))
        if not agree:
            print(f"  k={k} MISMATCH")
            print(f"     measured  {tk}")
            print(f"     predicted {p}")
            print(f"     st={ST[s2.st]} pos={s2.rel} (want -{8*k}) L={s2.right_word()[:0]}"
                  f" head={s2.head()} |L|={len(s2.left_word())}")
    return ok, meas


def budget_check(ks=(2, 3, 4, 5, 6, 7)):
    """The epoch decomposition must account for EVERY step:
       epoch = gap0 + S0 + gap1 + S1 + ... + gap_k + S_k + tail."""
    out = []
    for k in ks:
        segs, tops = segments(k)
        tot = 0; prev = M1_T[k]
        for (i0, i1, ta, tb, pa, pb, nr, s0, incs, t_) in segs:
            tot += (ta - prev) + t_; prev = tb
        tot += M1_T[k + 1] - prev
        out.append((k, tot, M1_T[k + 1] - M1_T[k], tot == M1_T[k + 1] - M1_T[k]))
    return out


# ---------------------------------------------------------------- self-validation
def check_anchors(full=False):
    """Reproduce PUBLISHED fingerprints before anything else here is trusted, and
    run three CONTROLS that MUST fail.  Returns True iff every check has the
    expected outcome."""
    ok = True

    def rep(name, got, want):
        nonlocal ok
        good = got == want
        ok &= good
        print(f"  [{'ok ' if good else 'BAD'}] {name}: {got}" + ("" if good else f"  want {want}"))

    print("A. published M0 milestone table (PHASEB_D_M0_2026-07-26.md), on D^R")
    rec = cluster(frontier_records(SPEC_DR, 5 * 10 ** 6, 'L'), 1.0)
    got = [(t, ST[s], p, w) for t, s, p, w in rec]
    rep("clustered L-records",
        got[2:],
        [(160, 'A', -4, 20), (894, 'A', -8, 50), (14130, 'A', -16, 185),
         (66906, 'A', -24, 422), (291168, 'A', -32, 893), (1196412, 'A', -40, 1832),
         (4846662, 'A', -48, 3707)])

    print("B. milestone family, BOTH sides, k=4..9 (state A, pos -8k, left BLANK, right word)")
    res, _ = check_milestone_family()
    rep("all k agree", all(v for _, v in res), True)

    print("C. universal rung laws on every ladder segment of epochs 2..7")
    n, parsed, f = validate(ks=(2, 3, 4, 5, 6, 7), quiet=True)
    rep("segments/parsed/failures", (n, parsed, len(f)), (33, 30, 3))

    print("D. step budget closes exactly (no unaccounted steps)")
    rep("all epochs", all(e for *_, e in budget_check((2, 3, 4, 5, 6))), True)

    print("CONTROLS (each MUST fail)")
    _, _, f1 = validate(ks=(4, 5, 6), span_law=lambda u, m: 6 * (u + m) + 14, quiet=True)
    rep("C1 span=6(u+m)+14 fails", len(f1) > 0, True)
    _, _, f2 = validate(ks=(4, 5, 6), span_law=lambda u, m: 6 * m + 15, quiet=True)
    rep("C2 span=6m+15 (one-sided reading) fails", len(f2) > 0, True)
    r3, _ = check_milestone_family(ks=(4, 6), pred=lambda k: [('0', 33), ('10', k)])
    rep("C3 M0 word 'zeros 33 ++ pow10 k' fails", all(not v for _, v in r3), True)

    if full:
        print("E. (2,4) ladder fingerprint at 1.2e8 -- x2 control and D")
        ladder_fingerprint(SPEC_X2, 12 * 10 ** 7, 'x2 (control)')
        ladder_fingerprint(SPEC_D, 12 * 10 ** 7, 'D (forward TNF)')
    print("ANCHORS", "PASS" if ok else "FAIL")
    return ok


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'anchors'
    if cmd == 'anchors':
        check_anchors(full='--full' in sys.argv)
    elif cmd == 'milestones':
        milestone_scan(int(sys.argv[2]) if len(sys.argv) > 2 else 4 * 10 ** 8)
    elif cmd == 'epoch':
        segment_report(int(sys.argv[2]))
    elif cmd == 'entry':
        for t in (160, 894, 14130, 66906, 291168):
            dump_at(SPEC_DR, t, 'entry', maxruns=8)
    elif cmd == 'ladder':
        N = int(sys.argv[2]) if len(sys.argv) > 2 else 12 * 10 ** 7
        ladder_fingerprint(SPEC_X2, N, 'x2 (control)')
        ladder_fingerprint(SPEC_D, N, 'D (forward TNF)')
