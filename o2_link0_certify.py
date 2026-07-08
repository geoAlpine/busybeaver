#!/usr/bin/env python3
# o2 LINK 0 certified verification (2026-07-08)
#
# CLAIM (Link 0): from any milestone configuration
#     D(a,b):  0^inf [head, state A, on 0] 0 11 (01)^a 0 11 (01)^b 0^inf   (a>=1, b>=0)
# the raw machine o2 = 1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA evolves, with no
# intermediate milestone configuration, exactly to
#     a even:            D((3a+4)/2, b+2)   at head offset -(a+4)
#     a odd, b>=1:       D((3a+7)/2, b-1)   at head offset -(a+5)
#     a odd=3 (4), b=0:  D((9a+29)/4, 1)    at head offset -(5a+25)/2      (escape)
#     a odd=1 (4), b=0:  HALT (F reads 0)   at head offset 2a+8            (halt)
# i.e. the milestone automaton of CRYPTID_SLOWWIDTH_2026-07-04 / X32_FAMILY_REDUCTIONS.
#
# PROOF METHOD (certified trace-template, red-team-corrected form of
# PAPER_TEMPLATE_METHOD.md par.2 / O4_TEMPLATE_CLOSURE_2026-07-06):
#  (0) SWEEP LEMMAS [PROVEN, 2-transition induction from the table]:
#        B1E1 leftward invert  (B:1->1LE, E:1->0LB):  1^{2n} -> (01)^n, head -2n
#        C0A1 rightward invert (C:0->1RA, A:1->1RC):  (01)^n -> 1^{2n}, head +2n
#        (A1C0 = the same 2-cycle entered on the A-phase: (10)^n -> 1^{2n})
#      Conditional: valid while the region ahead is correctly tiled.
#  (1) CUT INVARIANT: every F-event (F is entered only by D:0->0RF; F reads 1 =
#      continue, F reads 0 = HALT) is a structural cut. The global config at cut c
#      is EXACTLY (verified per run, every cut):
#        phase 1, c = 1..ceil(a/2):   W: 0^inf 1^{6c-1} 0 [F:1] (01)^m 0 11 (01)^b 0^inf
#                                        m = a-2c+1 >= 0, head 4c, block left edge -2c
#        phase-1 exit (a even, m=-1): T: 0^inf 1^{3a+5} 0 [F:1] 1 (01)^b 0^inf,  head 2a+4
#        phase 2 (b=0 only), c2>=1:   V: 0^inf 1^{6c2-1} 0 [F:1] (01)^m2 0^inf
#                                        m2 = (3a+7)/2 - 2(c2-1), head -(a+1)+4(c2-1)
#      The mod-4 halt criterion is the PARITY of (3a+7)/2: even (a=3 mod 4) ->
#      phase 2 drains to V(m2=0) and escapes; odd (a=1 mod 4) -> drains to m2=1
#      and the next F-entry reads 0: HALT.
#  (2) UNIT LEMMA [certified trace-template]: from any W/V cut with m >= 1, the next
#      segment is the CANONICAL UNIT k (k = cut index): a fixed 16-item skeleton
#      (14 episode steps + 2 sweeps: B1E1 length 6k+2, C0A1 length 6k+4), 12k+20 steps,
#      touching only [Lk-2, h0+3] (h0 = head at cut, Lk = h0-6k = block left edge),
#      landing on the next cut with block +6 ones, m -= 2, everything right of h0+3
#      UNTOUCHED. Certified by: skeleton identity + exact sweep lengths + EPISODE-
#      LANDMARK PINNING (every episode step at a k-independent offset from h0 or Lk)
#      across every unit instance of every grid run (k up to 500+, both phases, all
#      four branches). The window [h0, h0+3] reads 1,0,1,0 for EVERY m >= 1 (m=1
#      included: the terminator's 0 aligns), so the unit applies uniformly until m < 1.
#  (3) EXIT TEMPLATES [certified trace-template]: the segment from the phase-1/2 exit
#      cut to the landing milestone / mid-landing / halt, one template per class:
#        SUF_EVEN (b>=3 generic; b=0,1,2 per-b variants, par.2.5 small-parameter form),
#        SUF_ODD (b>=1, verified b-uniform: zero b-gradient),
#        MID (b=0, all odd a: phase-1 exit -> phase-2 entry),
#        SUF_ESC (a=3 mod 4), TERMINAL (a=1 mod 4: one more canonical unit, then the
#        F-entry reads 0 = the halt-gate fires; exact final config asserted).
#      Certified by skeleton identity + exactly-affine sweep lengths in (a,b)
#      (exact Fraction fits, verified at every grid point) + landmark pinning
#      (anchors: exit head, right end 2a+2b+5, landing point, block left edge)
#      + exact landings, grids to a >= 1000 / b >= 1000.
#  (4) COMPOSITION (red-team-corrected): the prefix is a fixed 10-step word on the
#      window [-2,4] whose content is milestone-determined for every a>=1; every
#      episode step of every template is landmark-pinned and every parameter-dependent
#      stretch is a proven sweep over a region whose exact content the cut invariant
#      fixes; hence the tape is symbolically reconstructible at every step and the
#      first-divergence argument closes: skeleton identity + affine sweep lengths on
#      the grid certify each lemma on its whole parameter cone. Induction on cuts then
#      gives Link 0 for ALL (a,b), a>=1, b>=0. Epistemic status: certified
#      trace-template method (grid-certified composition argument), NOT a
#      machine-checked symbolic induction -- the same label as o4's body lemma.
#
# SOUNDNESS: every check below is an exact concrete simulation plus exact integer/
# Fraction identities; any failure raises. Nothing here proves non-halting of o2:
# the ledger/hatch condition stays [OPEN]. No machine decided.
import re
import sys
from array import array
from fractions import Fraction

SPEC = "1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA"
STATES = "ABCDEF"

def parse_table(spec):
    tbl = []
    for blk in spec.split('_'):
        for r in (0, 1):
            c = blk[3*r:3*r+3]
            tbl.append(None if c[0] == '-' else (int(c[0]), 1 if c[1] == 'R' else -1,
                                                 STATES.index(c[2])))
    return tbl

TBL = parse_table(SPEC)          # TBL[st*2+r] = (write, dir, newstate) | None
OP = {f"{s}{r}": STATES.index(s)*2 + r for s in STATES for r in (0, 1)}
B1E1 = (OP['B1'], OP['E1'])      # leftward invert sweep cycle
C0A1 = (OP['C0'], OP['A1'])      # rightward invert sweep cycle

def step_map(a, b):
    """the milestone automaton (composed form on the b=0 branch)."""
    if a % 2 == 0:
        return ('D', (3*a + 4)//2, b + 2)
    if b >= 1:
        return ('D', (3*a + 7)//2, b - 1)
    if a % 4 == 1:
        return ('HALT',)
    return ('D', (9*a + 29)//4, 1)

# ---------------------------------------------------------------------------- section 0
def sweep_and_gate_lemmas():
    # halt gate: unique edge into F is D,0 -> 0RF; F halts on 0, continues on 1.
    assert TBL[OP['D0']] == (0, 1, 5) and TBL[OP['F0']] is None and TBL[OP['F1']] == (1, 1, 0)
    assert all(TBL[o] is None or TBL[o][2] != 5 for o in range(12) if o != OP['D0'])
    print("(0) HALT GATE [PROVEN from table]: F entered only by D:0->0RF; halt <=> that D-read-0")
    print("    has right neighbour 0 (F reads it).  => every F-event is a D0-cut; F:1 continues.")
    # B1E1: B on 1 -> write 1, L, E ; E on 1 -> write 0, L, B.
    assert TBL[OP['B1']] == (1, -1, 4) and TBL[OP['E1']] == (0, -1, 1)
    # C0A1: C on 0 -> write 1, R, A ; A on 1 -> write 1, R, C.
    assert TBL[OP['C0']] == (1, 1, 0) and TBL[OP['A1']] == (1, 1, 2)
    print("(0) SWEEP LEMMAS [PROVEN, 2-transition induction]:")
    print("    B1E1: from B on the last 1 of 1^{2n}: each pair 11 -> 01, head -2, state B;")
    print("          induction on n => 1^{2n} -> (01)^n in 2n steps, exits B two left of block.")
    print("    C0A1: from C on the first 0 of (01)^n: each pair 01 -> 11, head +2, state C;")
    print("          induction on n => (01)^n -> 1^{2n} in 2n steps, exits C right of block.")

# ---------------------------------------------------------------------------- simulator
MIL_RE = re.compile(r'^011((?:01)*)011((?:01)*)$')
W_RE = re.compile(r'^(1+)01((?:01)*)011((?:01)*)$')
T_RE = re.compile(r'^(1+)011((?:01)*)$')
V_RE = re.compile(r'^(1+)01((?:01)*)$')

def tape_string(tape, minone, maxone, start=None):
    lo = minone if start is None else start
    while lo <= maxone and not tape.get(lo, 0):
        lo += 1
    hi = maxone
    while hi >= lo and not tape.get(hi, 0):
        hi -= 1
    if hi < lo:
        return None, None
    return ''.join('1' if tape.get(c, 0) else '0' for c in range(lo, hi + 1)), lo

def parse_cut(tape, pos, minone, maxone):
    s, lo1 = tape_string(tape, minone, maxone)
    m = W_RE.match(s)
    if m:
        assert pos == lo1 + len(m.group(1)) + 1
        return ('W', len(m.group(1)), len(m.group(2))//2, len(m.group(3))//2, lo1)
    m = T_RE.match(s)
    if m:
        assert pos == lo1 + len(m.group(1)) + 1
        return ('T', len(m.group(1)), len(m.group(2))//2, lo1)
    m = V_RE.match(s)
    if m:
        assert pos == lo1 + len(m.group(1)) + 1
        return ('V', len(m.group(1)), len(m.group(2))//2, lo1)
    raise AssertionError(f"unparseable cut shape at pos {pos}: {s[:80]}")

def try_milestone(tape, pos, minone, maxone):
    g = tape.get
    if g(pos, 0) or g(pos+1, 0) != 1 or g(pos+2, 0) != 1 or g(pos+3, 0) \
       or g(pos-1, 0) or g(pos-2, 0):
        return None
    for c in range(minone, pos):          # blank strictly left of head
        if g(c, 0):
            return None
    s, lo1 = tape_string(tape, minone, maxone, start=pos)
    if lo1 != pos + 1:
        return None
    m = MIL_RE.match('0' + s)             # from the head cell
    if not m:
        return None
    return (len(m.group(1))//2, len(m.group(2))//2)

def run_transition(a, b, maxsteps=100_000_000):
    """exact raw run from milestone D(a,b) to the FIRST milestone config (or HALT).
    Returns full trace (ops/poss), F-cuts with parsed exact global shapes, landing,
    halt-gate trigger count, span."""
    tape = {}
    s0 = "011" + "01"*a + "011" + "01"*b
    for i, ch in enumerate(s0):
        if ch == '1':
            tape[i] = 1
    minone, maxone = 1, len(s0) - 1
    pos = 0; st = 0
    ops = bytearray(); poss = array('i')
    cuts = []
    lo = 0; hi = maxone
    gate = 0
    g = tape.get
    while True:
        r = g(pos, 0)
        op = st*2 + r
        if st == 0 and r == 0 and ops:
            ab = try_milestone(tape, pos, minone, maxone)
            if ab is not None:
                return dict(res=('D',)+ab, land=pos, ops=ops, poss=poss,
                            cuts=cuts, span=(lo, hi), gate=gate, final=None)
        if st == 5 and r == 1:
            cuts.append((len(ops), pos, parse_cut(tape, pos, minone, maxone)))
        elif op == 6 and g(pos+1, 0) == 0:               # D reads 0, right neighbour 0
            gate += 1
        tr = TBL[op]
        if tr is None:
            s, lo1 = tape_string(tape, minone, maxone)
            return dict(res=('HALT',), land=pos, ops=ops, poss=poss,
                        cuts=cuts, span=(lo, hi), gate=gate, final=(st, pos, r, s, lo1))
        ops.append(op); poss.append(pos)
        w, d, ns = tr
        if w:
            tape[pos] = 1
            if pos < minone: minone = pos
            if pos > maxone: maxone = pos
        elif r:
            del tape[pos]
        pos += d; st = ns
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
        if len(ops) > maxsteps:
            raise AssertionError(f"D({a},{b}): no milestone within {maxsteps} steps")

# ---------------------------------------------------------------------------- expected cuts
def expected_cuts(a, b):
    """the cut invariant: exact predicted (headpos, shape) sequence for D(a,b)."""
    cuts = []
    cmax = a//2 + 1 if a % 2 == 0 else (a + 1)//2
    for c in range(1, cmax):
        cuts.append((4*c, ('W', 6*c - 1, a - 2*c + 1, b, -2*c)))
    if a % 2 == 0:
        cuts.append((2*a + 4, ('T', 3*a + 5, b, -(a + 2))))
    else:
        cuts.append((2*a + 2, ('W', 3*a + 2, 0, b, -(a + 1))))
    if a % 2 == 1 and b == 0:
        mstart = (3*a + 7)//2
        c2max = (3*a + 7)//4 + 1 if a % 4 == 3 else (3*a + 9)//4
        for c2 in range(1, c2max + 1):
            h0 = -(a + 1) + 4*(c2 - 1)
            cuts.append((h0, ('V', 6*c2 - 1, mstart - 2*(c2 - 1), h0 - 6*c2)))
    return cuts

# ---------------------------------------------------------------------------- compression
def compress(ops, poss, i0, i1, minlen=8):
    """period-2 compression -> items ('E', op, pos) | ('S', (op1,op2), len, startpos)."""
    out = []
    i = i0
    while i < i1:
        j = i
        while j + 2 < i1 and ops[j+2] == ops[j]:
            j += 1
        L = j + 2 - i
        if L >= minlen and ops[i] != ops[i+1]:
            take = L - (L % 2)
            out.append(('S', (ops[i], ops[i+1]), take, poss[i]))
            i += take
        else:
            out.append(('E', ops[i], poss[i]))
            i += 1
    return out

def skeleton(items):
    return tuple((it[0], it[1]) for it in items)

# ---------------------------------------------------------------------------- unit canon
def extract_unit_canon(unit_instances):
    """unit_instances: list of (k, h0, items). Build the canonical unit template:
    each episode pinned to h0 ('R') or Lk = h0-6k ('L') at a k-independent offset;
    sweeps: cycle, length = 6k + beta, start pinned."""
    ks = [k for k, _, _ in unit_instances]
    assert len(set(ks)) >= 2
    base = skeleton(unit_instances[0][2])
    for k, h0, items in unit_instances:
        assert skeleton(items) == base, f"unit skeleton differs at k={k}"
    canon = []
    for idx, kind in enumerate(base):
        pi = 2 if kind[0] == 'E' else 3          # position slot (episode pos / sweep start)
        offR = {items[idx][pi] - h0 for k, h0, items in unit_instances}
        offL = {items[idx][pi] - (h0 - 6*k) for k, h0, items in unit_instances}
        if kind[0] == 'E':
            if len(offR) == 1:
                canon.append(('E', kind[1], 'R', offR.pop()))
            elif len(offL) == 1:
                canon.append(('E', kind[1], 'L', offL.pop()))
            else:
                raise AssertionError(f"unit episode {idx} not pinned: R={offR} L={offL}")
        else:
            betas = {items[idx][2] - 6*k for k, h0, items in unit_instances}
            assert len(betas) == 1, f"unit sweep {idx} length not 6k+const: {betas}"
            if len(offR) == 1:
                canon.append(('S', kind[1], betas.pop(), 'R', offR.pop()))
            elif len(offL) == 1:
                canon.append(('S', kind[1], betas.pop(), 'L', offL.pop()))
            else:
                raise AssertionError(f"unit sweep {idx} start not pinned")
    return canon

def check_unit(canon, items, k, h0):
    assert len(items) == len(canon), f"unit item count {len(items)} != {len(canon)}"
    L = h0 - 6*k
    for it, ca in zip(items, canon):
        if ca[0] == 'E':
            assert it[0] == 'E' and it[1] == ca[1], f"unit episode op mismatch k={k}"
            anchor = h0 if ca[2] == 'R' else L
            assert it[2] == anchor + ca[3], f"unit episode pos mismatch k={k}: {it} vs {ca}"
        else:
            assert it[0] == 'S' and it[1] == ca[1], f"unit sweep cycle mismatch k={k}"
            assert it[2] == 6*k + ca[2], f"unit sweep len {it[2]} != 6k+{ca[2]} (k={k})"
            anchor = h0 if ca[3] == 'R' else L
            assert it[3] == anchor + ca[4], f"unit sweep start mismatch k={k}"

# ---------------------------------------------------------------------------- affine fits
def affine_fit_exact(pts):
    """pts: {(x,...) : value}; fit value = c0 + sum ci*xi exactly, verify ALL points.
    Returns tuple of Fractions (c0, c1[, c2])."""
    keys = list(pts)
    dim = len(keys[0])
    if dim == 1:
        xs = sorted({k[0] for k in keys})
        assert len(xs) >= 2
        (x0,), (x1,) = (xs[0],), (xs[1],)
        c1 = Fraction(pts[(x1,)] - pts[(x0,)], x1 - x0)
        c0 = Fraction(pts[(x0,)]) - c1*x0
        for (x,), v in pts.items():
            assert c0 + c1*x == v, f"1D affine fit fails at x={x}"
        return (c0, c1)
    # dim 2
    a0, b0 = keys[0]
    p1 = next(k for k in keys if k[1] == b0 and k[0] != a0)
    p2 = next(k for k in keys if k[0] == a0 and k[1] != b0)
    ca = Fraction(pts[p1] - pts[keys[0]], p1[0] - a0)
    cb = Fraction(pts[p2] - pts[keys[0]], p2[1] - b0)
    c0 = Fraction(pts[keys[0]]) - ca*a0 - cb*b0
    for (x, y), v in pts.items():
        assert c0 + ca*x + cb*y == v, f"2D affine fit fails at ({x},{y})"
    return (c0, ca, cb)

def certify_family(name, instances, anchors):
    """instances: {params: (items, meta)}; anchors: {aname: fn(params)->int}.
    Certifies: skeleton identity; episode+sweep-start landmark pinning; sweep
    lengths exactly affine in params. Returns printable summary."""
    keys = list(instances)
    base = skeleton(instances[keys[0]][0])
    for kk in keys:
        assert skeleton(instances[kk][0]) == base, \
            f"{name}: skeleton differs at {kk}"
    pins = []
    n_sweep = 0
    fits = []
    for idx, kind in enumerate(base):
        # pin position (episode pos or sweep start)
        pos_of = {kk: instances[kk][0][idx][2 if kind[0] == 'E' else 3] for kk in keys}
        pinned = None
        for aname, fn in anchors.items():
            offs = {pos_of[kk] - fn(kk) for kk in keys}
            if len(offs) == 1:
                pinned = (aname, offs.pop())
                break
        assert pinned is not None, \
            f"{name}: item {idx} ({kind}) NOT pinned to any anchor; " \
            f"positions {dict(list(pos_of.items())[:4])}"
        pins.append(pinned)
        if kind[0] == 'S':
            n_sweep += 1
            lens = {kk: instances[kk][0][idx][2] for kk in keys}
            fits.append((idx, affine_fit_exact(lens)))
    from collections import Counter
    pc = Counter(p[0] for p in pins)
    maxoff = max(abs(p[1]) for p in pins)
    print(f"    {name}: {len(keys)} instances, skeleton {len(base)} items "
          f"({n_sweep} sweeps), IDENTICAL; all items pinned "
          f"({dict(pc)}, max |offset| = {maxoff}); sweep lengths exactly affine:")
    for idx, co in fits:
        cyc = base[idx][1]
        cname = ''.join(f"{STATES[o//2]}{o%2}" for o in cyc)
        cs = ' + '.join(str(c) + v for c, v in zip(co, ['', '*a', '*b']) if c or v == '')
        print(f"      sweep@{idx} {cname}: len = {cs}")
    return dict(n=len(keys), skel=base, pins=pins, fits=fits)

# ---------------------------------------------------------------------------- per-run check
class Certifier:
    def __init__(self):
        self.canon = None
        self.units_checked = 0
        self.max_k = 0
        self.families = {n: {} for n in
                         ('SUF_EVEN_G', 'SUF_EVEN_B0', 'SUF_EVEN_B1', 'SUF_EVEN_B2',
                          'SUF_ODD', 'MID', 'SUF_ESC')}
        self.prefix_word = None
        self.step_totals = {}
        self.runs = 0

    def branch(self, a, b):
        if a % 2 == 0:
            return 'EVEN'
        if b >= 1:
            return 'ODD'
        return 'ESC' if a % 4 == 3 else 'HALT'

    def landing(self, a, b):
        br = self.branch(a, b)
        return {'EVEN': -(a + 4), 'ODD': -(a + 5),
                'ESC': -(5*a + 25)//2, 'HALT': 2*a + 8}[br]

    def process(self, a, b, r):
        br = self.branch(a, b)
        # (i) landing = automaton, exactly
        assert r['res'] == step_map(a, b), \
            f"D({a},{b}): landed {r['res']} != automaton {step_map(a, b)}"
        assert r['land'] == self.landing(a, b), \
            f"D({a},{b}): landing pos {r['land']} != {self.landing(a, b)}"
        # (ii) halt-gate safety: fires exactly once (the halt) on HALT, never else
        assert r['gate'] == (1 if br == 'HALT' else 0), \
            f"D({a},{b}): gate fired {r['gate']} times"
        # (iii) cut invariant, every cut exact
        exp = expected_cuts(a, b)
        got = [(pos, shape) for _, pos, shape in r['cuts']]
        assert len(got) == len(exp), f"D({a},{b}): {len(got)} cuts != {len(exp)}"
        for i, ((ph, sh), (gp, gs)) in enumerate(zip(exp, got)):
            assert gp == ph and gs == sh, \
                f"D({a},{b}) cut {i}: got {gs}@{gp}, expected {sh}@{ph}"
        # (iv) segments
        ops, poss = r['ops'], r['poss']
        cutidx = [ci for ci, _, _ in r['cuts']] + [len(ops)]
        # prefix
        pw = (bytes(ops[:cutidx[0]]), tuple(poss[:cutidx[0]]))
        assert cutidx[0] == 10
        if self.prefix_word is None:
            self.prefix_word = pw
        assert pw == self.prefix_word, f"D({a},{b}): prefix word differs"
        # classify segments after each cut
        segs = []
        for i in range(len(cutidx) - 1):
            segs.append((i, cutidx[i], cutidx[i + 1]))
        c_exit1 = a//2 + 1 if a % 2 == 0 else (a + 1)//2       # phase-1 exit cut no.
        n1 = c_exit1                                            # cuts in phase 1
        unit_segs = []           # (k, h0, i0, i1)
        exit_segs = []           # (family, params, i0, i1)
        for i, i0, i1 in segs:
            cno = i + 1          # segment starts at cut cno
            if cno < c_exit1:
                unit_segs.append((cno, exp[cno - 1][0], i0, i1))
            elif cno == c_exit1:
                if br == 'EVEN':
                    fam = 'SUF_EVEN_G' if b >= 3 else f'SUF_EVEN_B{b}'
                    exit_segs.append((fam, (a, b) if b >= 3 else (a,), i0, i1))
                elif br == 'ODD':
                    exit_segs.append(('SUF_ODD', (a, b), i0, i1))
                else:
                    exit_segs.append(('MID', (a,), i0, i1))
            else:
                c2 = cno - c_exit1                              # phase-2 cut index
                shape = exp[cno - 1][1]
                assert shape[0] == 'V'
                m2 = shape[2]
                if m2 >= 2 if br == 'ESC' else m2 >= 3:
                    unit_segs.append((c2, exp[cno - 1][0], i0, i1))
                elif br == 'ESC':
                    assert m2 == 0
                    exit_segs.append(('SUF_ESC', (a,), i0, i1))
                else:
                    assert m2 == 1                              # terminal unit, then HALT
                    unit_segs.append((c2, exp[cno - 1][0], i0, i1))
        # (v) canonical units
        for k, h0, i0, i1 in unit_segs:
            items = compress(ops, poss, i0, i1)
            check_unit(self.canon, items, k, h0)
            # locality: right-touch <= h0+3, left-touch >= Lk-2
            mx = max(poss[i0:i1]); mn = min(poss[i0:i1])
            assert mx == h0 + 3 and mn == h0 - 6*k - 2, \
                f"D({a},{b}) unit k={k}: span [{mn},{mx}] != [{h0-6*k-2},{h0+3}]"
            self.units_checked += 1
            self.max_k = max(self.max_k, k)
        # (vi) collect exit segments for family certification
        for fam, params, i0, i1 in exit_segs:
            items = compress(ops, poss, i0, i1)
            self.families[fam][params] = (items, dict(a=a, b=b))
        # (vii) HALT branch: exact final config
        if br == 'HALT':
            st, pos, rd, s, lo1 = r['final']
            assert st == 5 and rd == 0 and pos == 2*a + 8
            assert s == '1' * ((9*a + 37)//2) and lo1 == -(5*a + 23)//2, \
                f"D({a},0): final tape not the predicted solid block"
        self.step_totals[(a, b)] = len(ops)
        self.runs += 1

def extract_canon_from(a, b):
    r = run_transition(a, b)
    ops, poss = r['ops'], r['poss']
    cutidx = [ci for ci, _, _ in r['cuts']] + [len(ops)]
    exp = expected_cuts(a, b)
    insts = []
    c_exit1 = a//2 + 1 if a % 2 == 0 else (a + 1)//2
    for i in range(len(cutidx) - 1):
        cno = i + 1
        if cno < c_exit1:
            items = compress(ops, poss, cutidx[i], cutidx[i + 1])
            insts.append((cno, exp[cno - 1][0], items))
    return extract_unit_canon(insts), r

# ---------------------------------------------------------------------------- standalone unit
def standalone_unit(canon, k, m):
    """Standalone instance of the unit lemma, far beyond the full-run grids:
    build the V-shape 0^inf 1^{6k-1} 0 [F:1] (01)^m 0^inf (h0 = 0) and run one unit.
    m >= 2: must land exactly on the next cut V(6(k+1)-1, m-2) at h0 = 4;
    m == 1: the unit word runs identically, then the F-entry reads 0: HALT
    (the terminal mechanism of the a = 1 mod 4 branch, in isolation)."""
    tape = {c: 1 for c in range(-6*k, -1)}          # 1^{6k-1}
    tape[0] = 1                                     # the F-read 1
    for i in range(m):
        tape[2 + 2*i] = 1                           # (01)^m
    minone, maxone = -6*k, (2*m if m else 0)
    pos = 0; st = 5
    ops = bytearray(); poss = array('i')
    g = tape.get
    while True:
        r = g(pos, 0)
        if st == 5 and ops:
            if r == 1:
                cut = parse_cut(tape, pos, minone, maxone)
                break
            cut = ('HALTED', pos)
            break
        ops.append(st*2 + r); poss.append(pos)
        w, d, ns = TBL[st*2 + r]
        if w:
            tape[pos] = 1
            if pos < minone: minone = pos
            if pos > maxone: maxone = pos
        elif r:
            del tape[pos]
        pos += d; st = ns
        assert len(ops) < 10**7
    items = compress(ops, poss, 0, len(ops))
    check_unit(canon, items, k, 0)
    assert max(poss) == 3 and min(poss) == -6*k - 2, "standalone unit span"
    assert len(ops) == 12*k + 20, "standalone unit step count"
    if m >= 2:
        assert cut == ('V', 6*(k + 1) - 1, m - 2, -(6*k + 2)) and pos == 4, \
            f"standalone unit landing: {cut} @ {pos}"
    else:
        assert cut == ('HALTED', 4), f"standalone m=1: {cut} @ {pos}"
    return len(ops)

# ---------------------------------------------------------------------------- main
def main():
    sweep_and_gate_lemmas()

    print("\n(1) BLANK-TAPE BASE [concrete, exact]:")
    tape = {}; pos = 0; st = 0; minone = 10**9; maxone = -10**9
    for s in range(1, 200):
        r0 = tape.get(pos, 0)
        w, d, ns = TBL[st*2 + r0]
        if w:
            tape[pos] = 1; minone = min(minone, pos); maxone = max(maxone, pos)
        elif r0:
            del tape[pos]
        pos += d; st = ns
        if st == 0 and tape.get(pos, 0) == 0 and s >= 40:
            ab = try_milestone(tape, pos, min(minone, pos), maxone)
            if ab is not None:
                print(f"    blank -> milestone D{ab} at raw step {s}, head {pos}")
                assert ab == (2, 1) and s == 44
                break
    else:
        raise AssertionError("blank entry not found")

    cert = Certifier()
    print("\n(2) CANONICAL UNIT extraction (reference run D(40,3), k = 1..19):")
    cert.canon, _rref = extract_canon_from(40, 3)
    n_ep = sum(1 for c in cert.canon if c[0] == 'E')
    n_sw = len(cert.canon) - n_ep
    print(f"    unit template: {len(cert.canon)} items = {n_ep} episodes + {n_sw} sweeps")
    for c in cert.canon:
        if c[0] == 'S':
            cyc = ''.join(f"{STATES[o//2]}{o%2}" for o in c[1])
            print(f"      SWEEP {cyc}: length 6k+{c[2]}, start {c[3]}{c[4]:+d}")
    print("    episodes pinned:",
          ' '.join(f"{STATES[c[1]//2]}{c[1]%2}@{c[2]}{c[3]:+d}" for c in cert.canon
                   if c[0] == 'E'))

    print("\n(3) GRID RUNS (full trace, cut invariant, canonical units, exact landings):")
    grids = []
    # EVEN branch
    for a in range(2, 42, 2):
        for b in (0, 1, 2, 3, 4, 7, 10):
            grids.append((a, b))
    for a in (100, 250):
        for b in (0, 1, 2, 3, 7):
            grids.append((a, b))
    grids += [(1000, 3), (6, 50), (6, 251), (6, 1000)]
    # ODD branch
    for a in range(1, 43, 2):
        for b in (1, 2, 3, 7, 10):
            grids.append((a, b))
    for a in (101, 251):
        for b in (1, 3):
            grids.append((a, b))
    grids += [(1001, 3), (7, 50), (7, 1000)]
    # ESC branch (a = 3 mod 4, b = 0)
    grids += [(a, 0) for a in list(range(3, 44, 4)) + [103, 251, 999]]
    # HALT branch (a = 1 mod 4, b = 0)
    grids += [(a, 0) for a in list(range(1, 42, 4)) + [101, 401, 1001]]
    seen = set()
    for a, b in grids:
        if (a, b) in seen:
            continue
        seen.add((a, b))
        r = run_transition(a, b)
        cert.process(a, b, r)
    print(f"    {cert.runs} transitions certified: every landing == automaton, every cut")
    print(f"    shape exact, prefix word identical (10 steps), halt-gate silent except")
    print(f"    the one HALT firing per a=1(4) run.")
    print(f"    canonical units verified: {cert.units_checked} instances, k up to "
          f"{cert.max_k} (both phases, all branches), all pinned, spans exact.")

    print("\n(3b) STANDALONE UNIT INSTANCES far beyond the run grids (k-uniformity):")
    for k in (1000, 5000, 20000):
        for m in (1, 2, 3, 11):
            n = standalone_unit(cert.canon, k, m)
        print(f"    k={k}: V(1^{{6k-1}} 0 [F:1] (01)^m), m in (1,2,3,11): unit word == canon,")
        print(f"      span [-6k-2,+3], {n} = 12k+20 steps; m>=2 lands V(6k+5, m-2) EXACT;")
        print(f"      m=1: identical unit word, then F-entry reads 0 -> HALT (the terminal law)")

    print("\n(3c) SMALL-PARAMETER CONCRETE CORNER (par.2.5): all (a,b) in [1,40]x[0,10]:")
    nc = 0
    for a in range(1, 41):
        for b in range(0, 11):
            if (a, b) in cert.step_totals:
                continue
            r = run_transition(a, b)
            cert.process(a, b, r)
            nc += 1
    print(f"    {nc} further configs, full per-run certification (cuts, units, landing,")
    print(f"    gate), 0 mismatches; total transitions certified: {cert.runs}.")

    print("\n(4) EXIT-TEMPLATE FAMILIES [certified trace-template]:")
    anchors_even = lambda: {
        'F': lambda p: 2*p[0] + 4,                       # phase-1 exit head
        'R': lambda p: 2*p[0] + 2*(p[1] if len(p) > 1 else 0) + 5,   # right end
        'P': lambda p: -(p[0] + 4),                      # landing point
        'L': lambda p: -(p[0] + 2)}                      # block left edge
    anchors_odd = {
        'F': lambda p: 2*p[0] + 2,
        'R': lambda p: 2*p[0] + 2*p[1] + 5,
        'P': lambda p: -(p[0] + 5),
        'L': lambda p: -(p[0] + 1)}
    anchors_mid = {
        'F': lambda p: 2*p[0] + 2,
        'R': lambda p: 2*p[0] + 5,
        'P': lambda p: -(p[0] + 1),                      # phase-2 anchor
        'M': lambda p: -(p[0] + 7)}                      # mid left extreme
    anchors_esc = {
        'F': lambda p: 2*p[0] + 6,
        'P': lambda p: -(5*p[0] + 25)//2,
        'L': lambda p: -(5*p[0] + 21)//2}
    for fam, anc in (('SUF_EVEN_G', anchors_even()), ('SUF_EVEN_B0', anchors_even()),
                     ('SUF_EVEN_B1', anchors_even()), ('SUF_EVEN_B2', anchors_even()),
                     ('SUF_ODD', anchors_odd), ('MID', anchors_mid),
                     ('SUF_ESC', anchors_esc)):
        inst = cert.families[fam]
        assert len(inst) >= 4, f"{fam}: only {len(inst)} instances"
        summary = certify_family(fam, inst, anc)
        if fam == 'SUF_ODD':
            # the b-filler is crossed by NO suffix sweep: every sweep length must
            # have b-gradient exactly 0 (its only contact is one read of its leading 0)
            for idx, co in summary['fits']:
                assert co[2] == 0, f"SUF_ODD sweep@{idx} has b-gradient {co[2]}"
            print("      SUF_ODD: all sweep b-gradients exactly 0 (b-filler untouched)")

    print("\n(5) STEP-COUNT CLOSED FORMS + BLANK-CHAIN CROSS-CHECK:")
    # unit steps: 12k+20 (implied by canon: 14 episodes + (6k+2) + (6k+4))
    def suffix_steps(fam, params):
        items = cert.families[fam][params][0]
        return sum(it[2] if it[0] == 'S' else 1 for it in items)
    fits = {}
    for fam in cert.families:
        pts = {p: suffix_steps(fam, p) for p in cert.families[fam]}
        fits[fam] = affine_fit_exact(pts)
        print(f"    {fam} steps = {fits[fam]}")
    def total_steps(a, b):
        br = cert.branch(a, b)
        J1 = a//2 if a % 2 == 0 else (a - 1)//2
        t = 10 + sum(12*k + 20 for k in range(1, J1 + 1))
        if br == 'EVEN':
            fam = 'SUF_EVEN_G' if b >= 3 else f'SUF_EVEN_B{b}'
            co = fits[fam]
            t += co[0] + co[1]*a + (co[2]*b if len(co) > 2 else 0)
        elif br == 'ODD':
            co = fits['SUF_ODD']
            t += co[0] + co[1]*a + co[2]*b
        else:
            co = fits['MID']
            t += co[0] + co[1]*a
            J2 = (3*a + 7)//4 if br == 'ESC' else (3*a + 9)//4
            t += sum(12*k + 20 for k in range(1, J2 + 1))
            if br == 'ESC':
                co = fits['SUF_ESC']
                t += co[0] + co[1]*a
        assert t == int(t)
        return int(t)
    bad = 0
    for (a, b), T in cert.step_totals.items():
        if total_steps(a, b) != T:
            bad += 1
            print(f"    STEP FORMULA MISMATCH at D({a},{b}): {total_steps(a,b)} != {T}")
    assert bad == 0
    print(f"    closed-form step counts match all {len(cert.step_totals)} runs exactly.")
    # blank chain: 17 automaton transitions from D(2,1); banked raw run had
    # (7187,11) at raw step 62,095,432 (X32_CLEANUP_2026-07-08.md par.1.0)
    st_ab = (2, 1); tot = 44
    for _ in range(17):
        tot += total_steps(*st_ab)
        st_ab = step_map(*st_ab)[1:]
    print(f"    blank chain: 44 + 17 certified transitions -> D{st_ab} at raw step {tot:,}")
    assert st_ab == (7187, 11) and tot == 62_095_432, "blank-chain cross-check failed"
    print("    == the banked 10^8-step raw log (17 transitions, (7187,11)@62,095,432)  EXACT")

    print(f"""
(6) COMPOSITION / VERDICT:
  PREFIX [certified]: fixed 10-step word, window [-2,4], content milestone-determined
    for every a>=1, b>=0; lands cut 1 = W(5, a-1, b).
  UNIT LEMMA [certified trace-template]: W/V-cut with m>=1 -> next cut, canonical
    16-item template, k-uniform (episode-landmark pinning to h0 and Lk = h0-6k;
    sweeps by the 2-transition induction lemmas; touches only [Lk-2, h0+3]; the
    window [h0,h0+3] = 1,0,1,0 for every m>=1). {cert.units_checked} instances,
    k <= {cert.max_k}, zero deviations.
  EXIT TEMPLATES [certified trace-template]: SUF_EVEN (b>=3 generic + b=0,1,2
    variants), SUF_ODD (b>=1, zero b-gradient), MID (all odd a, b=0), SUF_ESC
    (a=3 mod 4), TERMINAL halt (a=1 mod 4: one canonical unit, then the F-entry
    reads 0 -- the unique halt-gate firing; exact final config asserted).
  => induction on cuts: Link 0 holds for ALL (a,b), a>=1, b>=0:
       D(a,b) -> the automaton's D(a',b') / HALT, exactly, with no intermediate
       milestone and no halt-gate firing except the predicted one.
  Cone bounds: templates certified on grids a <= 1001 (units to k = {cert.max_k}),
    b <= 1000, plus the concrete corner [1,40]x[0,10]; validity for all larger
    (a,b) by the red-team-corrected composition argument (landmark pinning =>
    symbolic reconstructibility => first-divergence closes).
  LABEL: o2 Link 0  [OBSERVED, 0-mismatch]  -->  [PROVEN, certified trace-template
    method] (grid-certified composition argument; NOT machine-checked symbolic
    induction -- the same epistemic standard as o4's certified lemmas).
  o2's halting problem stays [OPEN]: the ledger/hatch condition (<== ceiling-(K),
    seed 2) is untouched by this certificate.
  No machine decided. No halting verdict changed.""")

if __name__ == '__main__':
    main()
