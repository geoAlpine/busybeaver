#!/usr/bin/env python3
"""x2fg_frame.py -- the FRAMING GLUE (lead / trailing) of REGEN(k), BY TRANSPORT.

TASK (ROADMAP_2026-07-17 §1.3.2).  The factorisation of REGEN(k) reads

    REGEN(k) = [lead] . SUB_1 . glue . SUB_2 . ... . SUB_a . [trailing]

with `lead`  = steps from the window start to the FIRST recursive sub-call, and
     `trailing` = steps from the END of the LAST recursive sub-call to the window end.

Transport-verified values existed at only TWO levels (k=6: 154/498 via regen6_factored,
k=7: 241/627 via regen7_factored).  k=8's 424/884 came from the `glueSegs` TABLE -- a
greedy TERM-boundary parse, NOT transport.  Two points cannot establish a law.

METHOD -- identical in kind to x2ti_tree.py, and exact:
  * every transition (state,bit) -> (write,move,next) is a TOTAL function of (state,bit),
    so the (st,h) WORD over a window DETERMINES every write, every move, and the whole
    (state, head, dpos) trace.  Word-identity is not a proxy for the trace test; it IS the
    trace test, and it is a substring search.  (Re-verified here, [0] and [3v].)
  * canonical REGEN(k) reference window := the earliest length-candidate, CROSS-CHECKED
    against the windows lean/X2.lean actually grounds (carry_exit_j3 @ [6638,6708],
    carry_exit_j4 @ [6923,7141]) -- asserted, not assumed.
  * the TI class of REGEN(k) := ALL occurrences of that exact word (every offset).
  * the sub-call decomposition uses ONLY TI-verified sub-calls, maximal-box greedy, and its
    step sum is checked against exitSteps(k) exactly.
  * head excursions are derived FROM the emitted moves, never from caller lo/hi.

NOTHING here is fitted.  The fit + its out-of-sample test live in x2fg_law.py.
"""
import sys
from bisect import bisect_right

sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build, TT

CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 620000
KTOP = int(sys.argv[2]) if len(sys.argv) > 2 else 10

# ---- Lean's defs, transcribed verbatim from lean/X2.lean §5z/§5aj ------------------
def exitSteps(k):  return 2 ** (2 * k - 3) + k * 2 ** (k - 1) + 2 ** (k - 2) + 2
def termSteps(k):  return 2 ** (k + 1) + k + 5
def exitArity(k):  return (k - 5) * (k - 4) // 2 if k >= 5 else 0

STS = 'ABCDEF'
SYM = {(s, b): chr(ord('a') + 2 * i + b) for i, s in enumerate(STS) for b in (0, 1)}


def check_word_determines_trace():
    for s in STS:
        for b in (0, 1):
            t = TT[(s, b)]
            if t is None:
                continue                      # ('B',1) = HALT, absent from any live word
            if not (isinstance(t[0], int) and t[1] in (+1, -1) and t[2] in STS):
                return False
    return True


print(f"[0] (st,h) determines (write,move,next): {check_word_determines_trace()}")
print("    => (st,h)-word identity == (state,head,dpos)-trace identity  [EXACT]\n")

# ---- [1] emit the orbit word -------------------------------------------------------
print(f"[1] running build(2) to n={CAP} (ON-PATH, exact bigint) ...")
sim = build(2)
sim.step()
n0 = sim.n
W, POS, ANCH = [], [], []
while sim.n < CAP:
    W.append(SYM[(sim.st, sim.h)])
    POS.append(sim.pos)
    if sim.st == 'E' and sim.h == 0:
        ANCH.append(sim.n)
    if not sim.step():
        print("    HALTED")
        break
S = ''.join(W)
print(f"    word length {len(S)} (n={n0}..{n0+len(S)}), {len(ANCH)} E-on-0 anchors\n")


def idx(n):
    return n - n0


def rel_trace(n, length):
    i = idx(n)
    if i < 0 or i + length > len(S):
        return None
    p0 = POS[i]
    return tuple((S[t], POS[t] - p0) for t in range(i, i + length))


def head_excursion(n, length):
    """extent DERIVED FROM the tape/move trace -- never from a caller-maintained lo/hi."""
    i = idx(n)
    seg = POS[i:i + length]
    p0 = POS[i]
    return (min(seg) - p0, max(seg) - p0)


# ---- [2] canonical references ------------------------------------------------------
def term_windows(k):
    g = termSteps(k)
    return [(ANCH[i], ANCH[i + 1]) for i in range(len(ANCH) - 1) if ANCH[i + 1] - ANCH[i] == g]


def bylen(k):
    return sorted({(e - exitSteps(k), e) for (s, e) in term_windows(k) if e - exitSteps(k) >= n0})


REF = {}
print("[2] canonical REGEN(k) reference windows:")
for k in range(4, KTOP + 1):
    c = bylen(k)
    if not c:
        print(f"    REGEN({k}): no candidate within n<{CAP}")
        continue
    a, b = c[0]
    REF[k] = (a, b, S[idx(a):idx(b)])
    print(f"    REGEN({k}): [{a},{b}] len={b-a}={exitSteps(k)} "
          f"head-excursion(from tape)={head_excursion(a, b - a)}")

LEAN_WIN = {4: (6638, 6708), 5: (6923, 7141)}
print("\n    cross-check vs the windows lean/X2.lean grounds:")
for k, (la, lb) in LEAN_WIN.items():
    a, b, _ = REF[k]
    print(f"      REGEN({k}) carry_exit_j{k-1}: probe [{a},{b}] vs Lean [{la},{lb}]  "
          f"{'MATCH' if (a, b) == (la, lb) else '*** MISMATCH ***'}")
    assert (a, b) == (la, lb), "canonical reference disagrees with the Lean grounding"

# ---- [3] TI classes ----------------------------------------------------------------
TI = {}
print("\n[3] TI classes (exhaustive substring search over EVERY offset)")
for k in sorted(REF):
    _, _, w = REF[k]
    occ, i = [], S.find(w)
    while i != -1:
        occ.append((n0 + i, n0 + i + len(w)))
        i = S.find(w, i + 1)
    TI[k] = occ
    fp = [x for x in bylen(k) if x not in set(occ)]
    print(f"    k={k:<3} by-length {len(bylen(k)):>3}   by-TRANSPORT {len(occ):>3}   "
          f"false-positives rejected {len(fp)}")

print("\n[3v] word-identity => (st,h,dpos)-trace identity, on the real windows:")
for k in sorted(TI):
    t = [rel_trace(a, exitSteps(k)) for (a, _) in TI[k][:6]]
    t = [x for x in t if x is not None]
    if len(t) >= 2:
        print(f"      REGEN({k}): {len(t)} sites, all traces identical: "
              f"{all(x == t[0] for x in t)}")

# ---- [4] decomposition + the FRAMING GLUE ------------------------------------------
def decompose(k):
    """Maximal-box cover of REGEN(k)'s window by TI-verified sub-calls / TERM blocks.
    Returns (terms, subcall_spans) where subcall_spans are the RECURSIVE REGEN sub-calls
    in orbit order -- the framing glue is read off THOSE, by transport."""
    a, b, _ = REF[k]
    boxes = {}
    for kk in range(4, k):
        for (s, e) in TI.get(kk, []):
            if a <= s and e <= b and (e - s) < (b - a):
                boxes.setdefault(s, []).append((e, ('R', kk)))
    for kk in range(3, k + 1):
        for (s, e) in term_windows(kk):
            if a <= s and e <= b and (e - s) < (b - a):
                boxes.setdefault(s, []).append((e, ('T', kk)))
    terms, spans, pos, glue = [], [], a, 0
    while pos < b:
        c = boxes.get(pos)
        if c:
            e, tag = max(c)
            if glue:
                terms.append(('g', glue)); glue = 0
            terms.append(tag)
            if tag[0] == 'R':
                spans.append((pos, e, tag[1]))
            pos = e
        else:
            i = bisect_right(ANCH, pos)
            nxt = ANCH[i] if i < len(ANCH) and ANCH[i] <= b else b
            glue += nxt - pos; pos = nxt
    if glue:
        terms.append(('g', glue))
    return terms, spans


def total(terms):
    return sum(t[1] if t[0] == 'g' else
               (termSteps(t[1]) if t[0] == 'T' else exitSteps(t[1])) for t in terms)


print("\n[4] FRAMING GLUE by transport\n")
print(f"    {'k':<3} {'exitSteps':>10} {'arity':>6} {'lead':>7} {'trailing':>9}  "
      f"{'sum-check':>10}  calls")
DATA = {}
for k in range(6, KTOP + 1):
    if k not in REF:
        continue
    a, b, _ = REF[k]
    terms, spans = decompose(k)
    assert total(terms) == exitSteps(k), f"k={k} sum mismatch"
    if not spans:
        continue
    lead = spans[0][0] - a
    trailing = b - spans[-1][1]
    DATA[k] = (lead, trailing, [s[2] for s in spans], exitSteps(k))
    print(f"    {k:<3} {exitSteps(k):>10} {len(spans):>6} {lead:>7} {trailing:>9}  "
          f"{'OK':>10}  {[s[2] for s in spans]}")

# ---- [5] cross-check the two levels the ROADMAP calls transport-verified ------------
print("\n[5] cross-check vs the roadmap's transport-verified table")
GOLD = {6: (154, 498), 7: (241, 627)}          # from regen6_factored / regen7_factored
for k, (l, t) in GOLD.items():
    ml, mt = DATA[k][0], DATA[k][1]
    print(f"    k={k}: roadmap lead/trailing {l}/{t}   measured {ml}/{mt}   "
          f"{'MATCH' if (ml, mt) == (l, t) else '*** MISMATCH ***'}")
    assert (ml, mt) == (l, t), "framing glue disagrees with the green Lean factorisation"

print("\n[5b] k=8's glueSegs-TABLE value (424/884) -- NOW tested by transport:")
ml, mt = DATA[8][0], DATA[8][1]
print(f"    table 424/884   transport {ml}/{mt}   "
      f"{'CONFIRMED' if (ml, mt) == (424, 884) else '*** TABLE WAS WRONG ***'}")

print("\n[6] the transport-verified framing-glue table (k=6..%d):\n" % KTOP)
print("    | k | lead | trailing | exitSteps | arity |")
print("    |---|------|----------|-----------|-------|")
for k in sorted(DATA):
    l, t, calls, es = DATA[k]
    print(f"    | {k} | {l} | {t} | {es} | {len(calls)} |")

import json
open('/tmp/x2fg_data.json', 'w').write(json.dumps({str(k): DATA[k] for k in DATA}))
print("\n[data written to /tmp/x2fg_data.json for x2fg_law.py]")
