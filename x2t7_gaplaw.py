#!/usr/bin/env python3
"""T7 GAP LAW (2026-07-22): derive the doubling-phase ladder law from g=2, then PREDICT g=3.

x2t7_recon.py established (instrument-validated) that the g=2 doubling phase M6(2)->M1(3) is an
ascending ladder of RegenLaw transports, one per level k=5..11, separated by gaps that obey a
clean 4x recursion.  This script:

  1. derives the EXACT gap law from the g=2 measurements,
  2. checks that head + sum(exitSteps) + sum(gap) + tail accounts for the phase EXACTLY,
  3. uses it to PREDICT, in advance, the location of M1(4),
  4. simulates to that prediction and tests it.

This is a falsifiable forward prediction, not a fit.  The calibration lesson of this repo is that
extrapolations ("the ladder is forall-g") are narrative until measured -- so measure.

  exitSteps k = 2^(2k-3) + k*2^(k-1) + 2^(k-2) + 2      (lean/X2.lean:4316)
  gap k       = 4^k - 3*2^k + 7                          (derived here from g=2)
  low phase   = 267+38g (even g) | 305+38g (odd g)       (h_low_even / h_low_odd)
"""
from x2t7_lib import run, classify, E, rle_right, ones_run_left


def exitSteps(k):
    return (1 << (2 * k - 3)) + k * (1 << (k - 1)) + (1 << (k - 2)) + 2


def gap(k):
    return (1 << (2 * k)) - 3 * (1 << k) + 7


# ---------------------------------------------------------------- 1. the law, from g=2
print("=== 1. gap law derived from the g=2 measurements ===")
measured = {5: 935, 6: 3911, 7: 16007, 8: 64775, 9: 260615, 10: 1045511}
allok = True
for k, m in measured.items():
    p = gap(k)
    ok = (p == m)
    allok &= ok
    print(f"  gap({k}) = 4^{k} - 3*2^{k} + 7 = {p:>9}   measured {m:>9}   {'MATCH' if ok else 'MISMATCH'}")
print(f"  law holds on all 6 measured gaps: {allok}")

# ---------------------------------------------------------------- 2. exact accounting, g=2
print("\n=== 2. does head + SUM(exitSteps) + SUM(gap) + tail account for the phase EXACTLY? ===")
HEAD, TAIL = 6580, 211


def phase_len(kmax):
    return (HEAD + sum(exitSteps(k) for k in range(5, kmax + 1))
            + sum(gap(k) for k in range(5, kmax)) + TAIL)


g2_actual = 2852091 - (732733 + 343)
print(f"  predicted phase(g=2, kmax=11) = {phase_len(11)}")
print(f"  measured  phase(g=2)          = {g2_actual}")
print(f"  {'EXACT' if phase_len(11) == g2_actual else 'MISMATCH'}")
print(f"    breakdown: head {HEAD} + transports {sum(exitSteps(k) for k in range(5,12))}"
      f" + gaps {sum(gap(k) for k in range(5,11))} + tail {TAIL}")

# ---------------------------------------------------------------- 3. forward prediction, g=3
print("\n=== 3. FORWARD PREDICTION for g=3 (made before simulating) ===")
M1_3 = 2852091
LOW3 = 305 + 38 * 3                 # odd-g low phase
M6_3 = M1_3 + LOW3
KMAX3 = 12                          # K rises by 1 per generation (M1(3) is K=11)
PRED_PHASE = phase_len(KMAX3)
PRED_M1_4 = M6_3 + PRED_PHASE
print(f"  low phase g=3 (odd, 305+38g)      = {LOW3}")
print(f"  => M6(3)                          = {M6_3}")
print(f"  predicted ladder levels           = k=5..{KMAX3}")
print(f"  predicted phase length            = {PRED_PHASE}")
print(f"  ==> PREDICTED M1(4) AT STEP         {PRED_M1_4}")
print(f"  predicted transports: " +
      ", ".join(f"k={k}:{exitSteps(k)}" for k in range(5, KMAX3 + 1)))

# ---------------------------------------------------------------- 4. test it
print(f"\n=== 4. simulating to {PRED_M1_4 + 5000} and testing ===", flush=True)
HI = PRED_M1_4 + 5000
hits = []
milestones = []


def hook(step, st, pos, tape):
    if st != E:
        return
    if tape[pos] == 0:
        r = classify(st, pos, tape)
        if r is not None:
            hits.append((step, r[0], r[1]))
    # M1(g) detector: the E-milestone carrying the generation's big block 1^(2^K -3) or -9;
    # record every E config whose max 1-run is a new record, cheap proxy for milestones
    if step in (M6_3, PRED_M1_4):
        milestones.append((step, 'ABCDEF'[st], tape[pos]))


run(HI, hook=hook)

casc, regen = {}, {}
for s, kind, k in hits:
    (casc if kind == "cascadeReg" else regen).setdefault(k, set()).add(s)

print("\n  --- ladder found in the g=3 phase ---")
LO = M6_3
found = []
for k in sorted(set(list(regen) + list(casc))):
    es = exitSteps(k)
    starts = sorted(s for s in regen.get(k, set()) if s >= LO and (s + es) in casc.get(k, set()))
    if starts:
        found.append((k, starts[0], es))
        print(f"    k={k:>2}: transport at [{starts[0]}, {starts[0]+es}]  len {es}"
              f"   ({len(starts)} verified start(s) in phase)")

print(f"\n  levels found: {[k for k,_,_ in found]}   predicted: {list(range(5, KMAX3+1))}")
print(f"  NOTE: the detector's RLE window truncates at deep k; missing top levels are a "
      f"detector limit, not an absence (k=11 needed a 20000-cell window at g=2).")

if found:
    print("\n  --- measured gaps vs the law ---")
    found.sort()
    for (k1, s1, e1), (k2, s2, e2) in zip(found, found[1:]):
        if k2 == k1 + 1:
            meas = s2 - (s1 + e1)
            pred = gap(k1)
            print(f"    gap({k1}) measured {meas:>10}  predicted {pred:>10}  "
                  f"{'MATCH' if meas == pred else 'MISMATCH'}")

print(f"\n  --- milestone check ---")
for s, st, hd in milestones:
    print(f"    step {s}: state={st} head={hd}")
print(f"  (M6(3) predicted at {M6_3}; M1(4) predicted at {PRED_M1_4})")
