#!/usr/bin/env python3
"""x2fg_geom.py -- is the framing glue DERIVED or merely FITTED?

x2fg_law.py's `trailing(k) = 359 + termSteps(k)` is only a derivation if the claim it
rests on is TRUE BY TRANSPORT, namely:

    (T) the last `trailing(k)` steps of REGEN(k) are a k-INDEPENDENT 359-step word,
        followed by the single k-dependent closing block TERM(k).

That claim was READ OFF the `glueSegs` TABLE at k=6,7,8 -- and §5z's table is exactly the
greedy TERM-boundary parse the roadmap says produced the `881` artifact.  So it must be
tested, not inherited.  This probe tests it as a WORD IDENTITY (= trace identity, exact).

It also tests the analogous question for `lead`, and measures the head excursion of the
lead segment DERIVED FROM THE MOVE TRACE (never from a caller-maintained lo/hi), to see
whether the fitted 3*2^(k-1) has a tape-geometry meaning.
"""
import sys
from bisect import bisect_right

sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build, TT

CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 620000
KTOP = int(sys.argv[2]) if len(sys.argv) > 2 else 10

def exitSteps(k):  return 2 ** (2 * k - 3) + k * 2 ** (k - 1) + 2 ** (k - 2) + 2
def termSteps(k):  return 2 ** (k + 1) + k + 5

STS = 'ABCDEF'
SYM = {(s, b): chr(ord('a') + 2 * i + b) for i, s in enumerate(STS) for b in (0, 1)}

print(f"[1] build(2) to n={CAP} ...")
sim = build(2); sim.step(); n0 = sim.n
W, POS, ANCH = [], [], []
while sim.n < CAP:
    W.append(SYM[(sim.st, sim.h)]); POS.append(sim.pos)
    if sim.st == 'E' and sim.h == 0:
        ANCH.append(sim.n)
    if not sim.step():
        break
S = ''.join(W)
print(f"    |S|={len(S)}  anchors={len(ANCH)}\n")

def idx(n): return n - n0

def term_windows(k):
    g = termSteps(k)
    return [(ANCH[i], ANCH[i+1]) for i in range(len(ANCH)-1) if ANCH[i+1]-ANCH[i] == g]

def bylen(k):
    return sorted({(e - exitSteps(k), e) for (s, e) in term_windows(k) if e - exitSteps(k) >= n0})

REF, TI = {}, {}
for k in range(4, KTOP + 1):
    c = bylen(k)
    if not c: continue
    a, b = c[0]
    REF[k] = (a, b, S[idx(a):idx(b)])
assert (REF[4][0], REF[4][1]) == (6638, 6708) and (REF[5][0], REF[5][1]) == (6923, 7141)
for k in sorted(REF):
    _, _, w = REF[k]
    occ, i = [], S.find(w)
    while i != -1:
        occ.append((n0+i, n0+i+len(w))); i = S.find(w, i+1)
    TI[k] = occ

def decompose(k):
    a, b, _ = REF[k]
    boxes = {}
    for kk in range(4, k):
        for (s, e) in TI.get(kk, []):
            if a <= s and e <= b and (e-s) < (b-a):
                boxes.setdefault(s, []).append((e, ('R', kk)))
    for kk in range(3, k+1):
        for (s, e) in term_windows(kk):
            if a <= s and e <= b and (e-s) < (b-a):
                boxes.setdefault(s, []).append((e, ('T', kk)))
    spans, pos = [], a
    while pos < b:
        c = boxes.get(pos)
        if c:
            e, tag = max(c)
            if tag[0] == 'R': spans.append((pos, e, tag[1]))
            pos = e
        else:
            i = bisect_right(ANCH, pos)
            pos = ANCH[i] if i < len(ANCH) and ANCH[i] <= b else b
    return spans

FRAME = {}
for k in range(6, KTOP+1):
    if k not in REF: continue
    a, b, _ = REF[k]
    sp = decompose(k)
    if not sp: continue
    FRAME[k] = (a, b, sp[0][0]-a, b-sp[-1][1], sp[-1][1])

# ---- [2] IS THE TRAILING WORD k-INDEPENDENT? ---------------------------------------
print("[2] claim (T): trailing(k) = [k-independent 359-step word] ++ TERM(k)\n")
print("    (a) the 359-step head of the trailing segment, compared across k as a WORD:\n")
ks = sorted(FRAME)
base = None
allsame = True
for k in ks:
    a, b, lead, trail, last_end = FRAME[k]
    w359 = S[idx(last_end):idx(last_end)+359]
    if base is None:
        base = w359
        print(f"      k={k:<3} reference word (359 chars): {w359[:40]}...")
    else:
        same = (w359 == base)
        allsame = allsame and same
        print(f"      k={k:<3} identical to k={ks[0]}'s: {same}")
print(f"\n      => the 359-step tail glue is k-INDEPENDENT: {allsame}")

print("\n    (b) the REMAINDER of the trailing segment is exactly TERM(k):\n")
tok = True
for k in ks:
    a, b, lead, trail, last_end = FRAME[k]
    rest_start = last_end + 359
    rest_len = b - rest_start
    tw = [(s, e) for (s, e) in term_windows(k) if s == rest_start and e == b]
    ok = (rest_len == termSteps(k)) and bool(tw)
    tok = tok and ok
    print(f"      k={k:<3} remainder = {rest_len:<6} termSteps({k})={termSteps(k):<6} "
          f"is a TERM({k}) window at [{rest_start},{b}]: {bool(tw)}   "
          f"{'OK' if ok else '*** NO ***'}")
print(f"\n      => trailing(k) = 359 + termSteps(k) is DERIVED, not fitted: {allsame and tok}")

# ---- [3] the LEAD: is it k-independent?  Where does the k-dependence live? ----------
print("\n[3] the LEAD segment\n")
print("    (a) is the lead word k-independent?  (it cannot be -- lead(k) grows)\n")
for k in ks:
    a, b, lead, trail, _ = FRAME[k]
    print(f"      k={k:<3} lead={lead:<6}")
print("\n    (b) THE NESTING LAW -- common PREFIX / SUFFIX of the lead words:\n")
def leadword(k):
    return S[idx(FRAME[k][0]):idx(FRAME[k][0])+FRAME[k][2]]
for i in range(len(ks)-1):
    k1, k2 = ks[i], ks[i+1]
    w1, w2 = leadword(k1), leadword(k2)
    p = 0
    while p < min(len(w1), len(w2)) and w1[p] == w2[p]: p += 1
    s_ = 0
    while s_ < min(len(w1), len(w2)) and w1[-1-s_] == w2[-1-s_]: s_ += 1
    print(f"      k={k1}->{k2}: |lead| {len(w1)}->{len(w2)}   common prefix {p:<5} "
          f"common suffix {s_}   (lead({k1})={len(w1)})")

print("\n    (c) claim (L): leadword(k+1) = P_(k+1) ++ leadword(k)  EXACTLY,")
print("        i.e. level k's ENTIRE lead is a literal suffix of level k+1's.\n")
nest_ok = True
for i in range(len(ks)-1):
    k1, k2 = ks[i], ks[i+1]
    w1, w2 = leadword(k1), leadword(k2)
    ok = w2.endswith(w1)
    nest_ok = nest_ok and ok
    P = len(w2) - len(w1)
    pred = 3 * 2**(k2-2) - 9
    print(f"      leadword({k2}) endswith leadword({k1}): {str(ok):<5}   "
          f"|P_{k2}| = {P:<5} 3*2^({k2}-2)-9 = {pred:<5} "
          f"{'OK' if P == pred else '*** NO ***'}")
    nest_ok = nest_ok and (P == pred)
print(f"\n      => the lead RECURSION  lead(k+1) = lead(k) + 3*2^(k-1) - 9  is a WORD")
print(f"         identity, not a numeric fit: {nest_ok}")
print(f"         base case lead(6) = 154 [measured].  Closed form: 3*2^(k-1) - 9k + 112.")

print("\n    (d) head excursion of the lead segment, DERIVED FROM THE MOVE TRACE")
print("        (min/max of actual head positions; never a caller lo/hi):\n")
print(f"      {'k':<4} {'lead':>7} {'excursion (lo,hi)':>22} {'span':>7} {'2^k':>7} "
      f"{'lead/2^k':>9}")
for k in ks:
    a, b, lead, trail, _ = FRAME[k]
    i = idx(a); seg = POS[i:i+lead]; p0 = POS[i]
    lo, hi = min(seg)-p0, max(seg)-p0
    print(f"      {k:<4} {lead:>7} {str((lo,hi)):>22} {hi-lo:>7} {2**k:>7} "
          f"{lead/2**k:>9.3f}")
print("\n      lead/2^k -> 1.5 : the fitted 3*2^(k-1) IS one-and-a-half sweeps of the")
print("      1^(2^k-3) block.  But the excursion alone does not FORCE the additive 112;")
print("      that constant remains [OBSERVED].")
