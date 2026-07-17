#!/usr/bin/env python3
"""x2ti_tree.py -- TRANSPORT-BASED re-extraction of the REGEN exit tree (2026-07-17).

THE DEFECT BEING FIXED.  The probes grounding lean/X2.lean's exitSteps_tree_5/6/7/8 and
exitArity_grounds (x2ck_regen_seg.py, x2dt_tree8.py) identify a recursive sub-call
"REGEN(k')" by STEP COUNT alone: a window is "a REGEN(k') call" when its length happens to
equal exitSteps(k').  That is a coincidence-prone test, and x2az_verify10.py reported it
admits false positives (only 4/8 REGEN(7)-length windows genuine; one FP inflating
REGEN(10)'s arity 15->16).  Length is not transport.

THE CORRECT TEST (and why it is exact).  In this machine every transition (state,bit) ->
(write, move, next) is a total function of (state,bit) -- see x2bd_sim.TT.  Therefore the
(state, head-bit) symbol WORD emitted over a window DETERMINES, cell for cell:
   * every write performed,
   * every move, hence the whole relative position trace (pos - pos0),
   * the next-state sequence.
So two windows emit the same (st,h) word  <=>  they are the SAME transport, i.e. they read
and write the same local cells with the same head excursion, and differ ONLY in the tape
padding never touched.  That is precisely the content of the Lean `∀ L R` statements
(regen4_transport / regen5_transport / regen_TI_generic).  Word-identity is therefore not a
proxy for the (state,head,dpos) trace test -- it is EQUIVALENT to it, and exact.
(Verified explicitly below: check_word_determines_trace().)

METHOD (ON-PATH, exact bigint, cell-for-cell):
  1. Run x2bd_sim.build(2) -- the ONE orbit; a=5 and a=6 both live here.  Emit the (st,h)
     word S of the whole prefix.
  2. Canonical REGEN(k) reference := the EARLIEST length-candidate window (a TERM(k)-gap
     anchor pair, window = [end - exitSteps(k), end]).  For k=4,5 this must reproduce the
     windows Lean grounds (carry_exit_j3 @ [6638,6708], carry_exit_j4 @ [6923,7141]) --
     asserted, not assumed.
  3. TI class of REGEN(k) := ALL occurrences of that exact word in S (exhaustive substring
     search, every offset, not just anchors).  This is regen_TI_generic's "identical trace
     at all its orbit sites".
  4. Re-extract the tree of each REGEN(k) window using ONLY TI-verified sub-calls, and
     compare, per level, against what lean/X2.lean actually asserts.

All tape extents are derived FROM the emitted word (head excursion computed from the moves),
never from caller-maintained lo/hi.
"""
import sys
from bisect import bisect_left, bisect_right

sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build, TT

CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 620000
KTOP = int(sys.argv[2]) if len(sys.argv) > 2 else 10

# ---- Lean's defs, transcribed verbatim from lean/X2.lean §5z/§5aj ------------------
def exitSteps(k):  return 2 ** (2 * k - 3) + k * 2 ** (k - 1) + 2 ** (k - 2) + 2
def termSteps(k):  return 2 ** (k + 1) + k + 5
def exitArity(k):  return (k - 5) * (k - 4) // 2 if k >= 5 else 0

# symbol alphabet: one char per (state, head-bit)
STS = 'ABCDEF'
SYM = {(s, b): chr(ord('a') + 2 * i + b) for i, s in enumerate(STS) for b in (0, 1)}
MOVE = {SYM[k]: v[1] for k, v in TT.items() if v is not None}


def check_word_determines_trace():
    """The load-bearing claim, verified: (st,h) word -> (write, move, next) is total."""
    ok = True
    for s in STS:
        for b in (0, 1):
            t = TT[(s, b)]
            if t is None:
                continue  # ('B',1) = HALT; absent from any surviving word
            if not (isinstance(t[0], int) and t[1] in (+1, -1) and t[2] in STS):
                ok = False
    return ok


print(f"[0] (st,h) determines (write,move,next): {check_word_determines_trace()}")
print(f"    => (st,h)-word identity == (state,head,dpos)-trace identity  [EXACT]\n")

# ---- [1] emit the orbit word -------------------------------------------------------
print(f"[1] running build(2) to n={CAP} (ON-PATH, exact) ...")
sim = build(2)
sim.step()
n0 = sim.n
W = []           # W[i] = symbol emitted at step n0+i
POS = []         # POS[i] = head position BEFORE step n0+i
ANCH = []        # anchor absolute n where (st=='E' and h==0)
while sim.n < CAP:
    W.append(SYM[(sim.st, sim.h)])
    POS.append(sim.pos)
    if sim.st == 'E' and sim.h == 0:
        ANCH.append(sim.n)
    if not sim.step():
        print("    HALTED")
        break
S = ''.join(W)
print(f"    word length {len(S)} (steps n={n0}..{n0+len(S)}), {len(ANCH)} E-on-0 anchors\n")


def idx(n):
    """absolute step n -> index into S."""
    return n - n0


def rel_trace(n, length):
    """(state, head-bit, dpos) trace -- the criterion as literally stated."""
    i = idx(n)
    if i < 0 or i + length > len(S):
        return None
    p0 = POS[i]
    return tuple((S[t], POS[t] - p0) for t in range(i, i + length))


def head_excursion(n, length):
    """tape extent DERIVED FROM the trace (min/max of actual head positions).
    NEVER from a caller-maintained lo/hi."""
    i = idx(n)
    seg = POS[i:i + length]
    p0 = POS[i]
    return (min(seg) - p0, max(seg) - p0)


# ---- [2] canonical REGEN(k) references ---------------------------------------------
def term_windows(k):
    g = termSteps(k)
    return [(ANCH[i], ANCH[i + 1]) for i in range(len(ANCH) - 1) if ANCH[i + 1] - ANCH[i] == g]


def regen_candidates_bylen(k):
    """THE OLD, DEFECTIVE CRITERION: windows found purely BY LENGTH."""
    return sorted({(e - exitSteps(k), e) for (s, e) in term_windows(k) if e - exitSteps(k) >= n0})


REF = {}
print("[2] canonical REGEN(k) reference windows (earliest length-candidate):")
for k in range(4, KTOP + 1):
    c = regen_candidates_bylen(k)
    if not c:
        print(f"    REGEN({k}): no candidate within n<{CAP}")
        continue
    a, b = c[0]
    REF[k] = (a, b, S[idx(a):idx(b)])
    print(f"    REGEN({k}): [{a},{b}] len={b-a}={exitSteps(k)} "
          f"head-excursion(derived from tape)={head_excursion(a, b - a)}")

# HARD CHECK against what Lean actually grounds.
LEAN_WIN = {4: (6638, 6708), 5: (6923, 7141)}
print("\n    cross-check vs the windows lean/X2.lean grounds:")
for k, (la, lb) in LEAN_WIN.items():
    a, b, _ = REF[k]
    tag = "MATCH" if (a, b) == (la, lb) else f"*** MISMATCH (Lean says [{la},{lb}]) ***"
    print(f"      REGEN({k}) carry_exit_j{k-1}: probe [{a},{b}] vs Lean [{la},{lb}]  {tag}")
    assert (a, b) == (la, lb), "canonical reference disagrees with the Lean grounding"

# ---- [3] the TI class: ALL occurrences of the exact transport word -------------------
print("\n[3] TI classes -- every occurrence of the exact REGEN(k) transport word in S")
print("    (exhaustive over EVERY offset, not only anchors; this is regen_TI_generic)\n")
print(f"    {'k':<3} {'by LENGTH':>10} {'by TRANSPORT':>13} {'FALSE POS':>10}   verdict")
TI = {}
for k in sorted(REF):
    _, _, w = REF[k]
    occ, i = [], S.find(w)
    while i != -1:
        occ.append((n0 + i, n0 + i + len(w)))
        i = S.find(w, i + 1)
    TI[k] = occ
    bylen = regen_candidates_bylen(k)
    fp = [x for x in bylen if x not in set(occ)]
    fn = [x for x in occ if x not in set(bylen)]
    v = "clean" if not fp and not fn else (f"{len(fp)} FALSE POSITIVE(S)" if fp else "") + \
        (f" {len(fn)} length-missed" if fn else "")
    print(f"    {k:<3} {len(bylen):>10} {len(occ):>13} {len(fp):>10}   {v}")
    if fp:
        print(f"        length-matched but NOT the transport: {fp}")
    if fn:
        print(f"        genuine transport the length test MISSES: {fn}")

# independent sanity: word-identity really does give trace-identity
print("\n    [verify] word-identity => (state,head,dpos)-trace identity, on real windows:")
for k in sorted(TI):
    if len(TI[k]) >= 2:
        t = [rel_trace(a, exitSteps(k)) for (a, b) in TI[k][:6]]
        t = [x for x in t if x is not None]
        print(f"      REGEN({k}): {len(t)} sites, all (st,h,dpos) traces identical: "
              f"{all(x == t[0] for x in t)}")

# ---- [4] transport-based tree extraction --------------------------------------------
print("\n[4] TRANSPORT-based tree extraction of each REGEN(k)")


def extract(k, sub_source):
    """Cover REGEN(k)'s window by maximal TI-verified sub-calls + TERM blocks + glue.
    sub_source[k'] = list of (start,end) accepted occurrences of REGEN(k')."""
    a, b, _ = REF[k]
    boxes = {}
    for kk in range(4, k):
        for (s, e) in sub_source.get(kk, []):
            if a <= s and e <= b and (e - s) < (b - a):
                boxes.setdefault(s, []).append((e, ('R', kk)))
    for kk in range(3, k + 1):
        for (s, e) in term_windows(kk):
            if a <= s and e <= b and (e - s) < (b - a):
                boxes.setdefault(s, []).append((e, ('T', kk)))
    terms, pos, glue = [], a, 0
    while pos < b:
        c = boxes.get(pos)
        if c:
            e, tag = max(c)          # maximal block at this start
            if glue:
                terms.append(('g', glue)); glue = 0
            terms.append(tag); pos = e
        else:
            i = bisect_right(ANCH, pos)
            nxt = ANCH[i] if i < len(ANCH) and ANCH[i] <= b else b
            glue += nxt - pos; pos = nxt
    if glue:
        terms.append(('g', glue))
    return terms


def render(terms):
    out = []
    for t in terms:
        if t[0] == 'g':   out.append(str(t[1]))
        elif t[0] == 'T': out.append(f"TERM({t[1]})")
        else:             out.append(f"REGEN({t[1]})")
    return ' + '.join(out)


def total(terms):
    return sum(t[1] if t[0] == 'g' else
               (termSteps(t[1]) if t[0] == 'T' else exitSteps(t[1])) for t in terms)


BYLEN = {k: regen_candidates_bylen(k) for k in REF}
print("\n    (A) tree using LENGTH-matched sub-calls   [the OLD, defective method]")
print("    (B) tree using TRANSPORT-verified sub-calls [the CORRECT method]\n")
RESULT = {}
for k in range(5, KTOP + 1):
    if k not in REF:
        continue
    ta = extract(k, BYLEN)
    tb = extract(k, TI)
    ca = [t[1] for t in ta if t[0] == 'R']
    cb = [t[1] for t in tb if t[0] == 'R']
    RESULT[k] = (ta, tb, ca, cb)
    same = "IDENTICAL" if ta == tb else "*** DIFFER ***"
    print(f"  k={k}: arity(length)={len(ca)}  arity(transport)={len(cb)}  "
          f"exitArity({k})={exitArity(k)}   length-tree vs transport-tree: {same}")
    print(f"      calls(transport) = {cb}")
    print(f"      sum = {total(tb)}   exitSteps({k}) = {exitSteps(k)}   "
          f"{'OK' if total(tb) == exitSteps(k) else '*** SUM MISMATCH ***'}")
    if ta != tb:
        print(f"      calls(length)    = {ca}")

# ---- [5] verdict on the exact Lean theorem statements --------------------------------
print("\n[5] VERDICT on the literal lean/X2.lean theorem statements\n")

LEAN_TREE = {
    5: [('g', 44), ('T', 3), ('g', 76), ('T', 5)],
    6: [('g', 83), ('T', 3), ('g', 47), ('R', 4), ('g', 113), ('T', 3),
        ('g', 122), ('T', 3), ('g', 76), ('T', 6)],
    7: [('g', 170), ('T', 3), ('g', 47), ('R', 4), ('g', 113), ('T', 3), ('g', 78), ('R', 5),
        ('g', 113), ('T', 3), ('g', 881), ('T', 3), ('g', 47), ('R', 4), ('g', 113), ('T', 3),
        ('g', 122), ('T', 3), ('g', 76), ('T', 7)],
    8: [('g', 353), ('T', 3), ('g', 47), ('R', 4), ('g', 113), ('T', 3), ('g', 78), ('R', 5),
        ('g', 113), ('T', 3), ('g', 798), ('R', 6), ('g', 113), ('T', 3), ('g', 3944), ('T', 3),
        ('g', 47), ('R', 4), ('g', 113), ('T', 3), ('g', 78), ('R', 5), ('g', 113), ('T', 3),
        ('g', 881), ('T', 3), ('g', 47), ('R', 4), ('g', 113), ('T', 3), ('g', 122), ('T', 3),
        ('g', 76), ('T', 8)],
}
NAME = {5: 'exitSteps_tree_5', 6: 'exitSteps_tree_6', 7: 'exitSteps_tree_7',
        8: 'exitSteps_tree_8'}

allok = True
for k in sorted(LEAN_TREE):
    if k not in RESULT:
        print(f"  {NAME[k]}: REGEN({k}) not reached at CAP={CAP}"); allok = False; continue
    ta, tb, ca, cb = RESULT[k]
    lean = LEAN_TREE[k]
    lean_calls = [t[1] for t in lean if t[0] == 'R']
    s_ok = total(lean) == exitSteps(k)                 # the arithmetic Lean `decide`s
    c_ok = cb == lean_calls                            # the recursive calls, BY TRANSPORT
    t_ok = tb == lean                                  # the full term-by-term expression
    allok = allok and s_ok and c_ok
    print(f"  {NAME[k]}")
    print(f"      arithmetic sum = exitSteps({k}):            {'HOLDS' if s_ok else 'FALSE'}")
    print(f"      REGEN calls survive transport re-extraction: "
          f"{'HOLDS' if c_ok else 'FAILS'}   Lean={lean_calls}  transport={cb}")
    print(f"      full term-by-term parse reproduced:          "
          f"{'HOLDS' if t_ok else 'differs (glue parse only)'}")
    if not t_ok:
        print(f"          Lean      : {render(lean)}")
        print(f"          transport : {render(tb)}")

print("\n  exitArity_grounds  (exitArity 5,6,7,8 = 0,1,3,6):")
for k in (5, 6, 7, 8):
    if k not in RESULT:
        print(f"      k={k}: not reached"); continue
    _, _, ca, cb = RESULT[k]
    ok = len(cb) == exitArity(k)
    allok = allok and ok
    print(f"      k={k}: exitArity={exitArity(k)}  transport-measured arity={len(cb)}  "
          f"(length-measured {len(ca)})   {'HOLDS' if ok else '*** WRONG ***'}")

print("\n  BEYOND the Lean grounding range (k=9,10), for information only:")
for k in (9, 10):
    if k in RESULT:
        _, _, ca, cb = RESULT[k]
        print(f"      k={k}: exitArity={exitArity(k)}  transport arity={len(cb)}  "
              f"length arity={len(ca)}   {'agree' if len(cb)==exitArity(k) else 'DISAGREE'}")

print("\nVERDICT:", "the Lean groundings SURVIVE transport-based re-extraction"
      if allok else "*** at least one Lean grounding does NOT survive -- see above ***")
