#!/usr/bin/env python3
"""x2ti_island.py -- INDEPENDENT re-reproduction of every load-bearing Track B claim
before it is written into TRACK_B_ROADMAP_2026-07-16.md.  (2026-07-17)

WHY.  TRACK_B_REAUDIT_2026-07-17.md corrects the roadmap on several rows.  Discipline says
a correction must not be propagated on trust: before editing the roadmap I reproduce each
load-bearing number here, on an instrument that shares no code with x2tb_* / x2b5_* /
mse_extract / cd_probe.

WHAT IS REPRODUCED
  (1) B1/B2 pairing: maxrun records identical (2^k-2)?  step-times differ (=> not a TNF
      or mirror relabel, which would preserve step counts exactly)?
  (2) B3/B4 pairing: maxrun records 7*2^k vs 3*2^k  => NOT peak-identical?
  (3) B5: phase-conditioned register (state C at a left-extent record) = 9*2^k-1?
  (4) B5: the per-generation dense floor of full-tape maxrun == 14?  (a per-generation
      MINIMUM -- a different statistic from the post-peak milestone floors 5*2^k+6/+8.)
  (5) The island-wide per-doubling cost ratio (2 = linear/braid-free, 4 = Theta(v^2)).
  (6) W1: is its register a doubler at all, or an arithmetic ramp?

INSTRUMENT DISCIPLINE (the lesson of today, enforced structurally):
  * extent is ALWAYS derived FROM the tape (bytearray.find / .rfind over the whole
    allocated array).  There is no lo/hi parameter anywhere in this file -- the F1
    truncation bug is not expressible against this API.
  * a MINIMUM is only ever taken from a DENSE (stride-1) scan.  Minima over sparse
    record-triggered samples are upper bounds, not floors (fault F2) -- never reported here.
  * a ratio of 4 is reported ONLY for a register that genuinely doubles once per
    macro-generation (fault F3): for a machine whose cost ~ width^2, doubling ANY
    observable gives 4 for free.  doubling_gate() refuses to answer otherwise.
  * exact int arithmetic; on-path from each machine's real blank-tape orbit.

Decides NO halting.  Upgrades NO label.
"""
import sys

CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 12_000_000
SZ = 1 << 15           # tape size; overflow is CHECKED and raised, never assumed away
N = SZ // 2

MACH = {
    'B1': '1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE',
    'B2': '1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD',
    'B3': '1RB0RE_1RC1LF_0LD0RE_---1LE_1RA0LB_1LB0LC',
    'B4': '1RB0RC_1LC1RA_0RF0LD_1LE0RB_1LB0LD_---1RD',
    'B5': '1RB0LB_1LC1LB_1RD1LA_0RE0RE_0RA1RF_---1RD',
    'W1': '1RB0LE_1RC0RF_0RD0RB_1RE0RC_1LA0LA_1RA---',
    'W2': '1RB0LD_1LC0RA_1RA1LB_1LA1LE_1RF0LC_---0RE',
    'W3': '1RB0RB_1LC0LF_1RD0LB_1RE1RC_0RA---_1LA1RE',
}


def parse(spec):
    R = []
    for st in spec.split('_'):
        for t in (st[0:3], st[3:6]):
            if t[0] == '-' or t[2] in '-Z':
                R.append(None)
            else:
                R.append((int(t[0]), 1 if t[1] == 'R' else -1, (ord(t[2]) - ord('A')) * 2))
    return R


def maxrun_and_total(tape):
    """(total1, maxrun) over the FULL tape.  Extent derived from the tape itself."""
    lo = tape.find(1)
    if lo < 0:
        return 0, 0
    hi = tape.rfind(1)
    seg = bytes(tape[lo:hi + 1])
    best = 0
    for r in seg.split(b'\x00'):
        if len(r) > best:
            best = len(r)
    return tape.count(1), best


def run(spec, cap, obs='maxrun', dense_from=None, dense_to=None):
    """Run the blank-tape orbit.  Sample the observable at LEFT/RIGHT-extent records
    (a trigger for WHEN to sample -- never a bound on HOW FAR to scan).
    Returns (records, halted, dense_min) where
      records  = [(step, value)] strictly-increasing record values of the observable,
      dense_min = the TRUE min of full-tape maxrun over [dense_from, dense_to],
                  taken stride-1 (the only sampling that can witness a minimum)."""
    R = parse(spec)
    tape = bytearray(SZ)
    p = N
    s = 0
    n = 0
    lo = hi = p
    recs = []
    best = 0
    dense_min = None
    while n < cap:
        t = R[s + tape[p]]
        if t is None:
            return recs, True, dense_min
        w, d, ns = t
        tape[p] = w
        p += d
        s = ns
        n += 1
        if p < 4 or p > SZ - 4:
            raise RuntimeError('tape exhausted -- widen SZ')
        if p < lo or p > hi:                     # a NEW extent record: sample here
            if p < lo: lo = p
            if p > hi: hi = p
            tot, mr = maxrun_and_total(tape)     # full tape, tape-derived extent
            v = mr if obs == 'maxrun' else tot
            if v > best:
                best = v
                recs.append((n, v))
        if dense_from is not None and dense_from <= n <= dense_to:
            _, mr = maxrun_and_total(tape)       # stride-1, full tape
            if dense_min is None or mr < dense_min:
                dense_min = mr
    return recs, False, dense_min


def doubling_gate(recs):
    """FAULT F3 GUARD.  A genuine doubler sets O(1) records in the top octave; an
    arithmetic ramp sets ~7/8 of the top value.  Refuse to report a ratio otherwise."""
    if not recs:
        return False, 0, 0
    top = recs[-1][1]
    inoct = sum(1 for (_, v) in recs if v > top / 2)
    return inoct <= 12, inoct, top


def ratios(recs):
    """t_k = first step the register reaches V0*2^k;  ratio = t_k/t_{k-1}.
    2 = linear (braid-free).  4 = Theta(v^2) per doubling."""
    if not recs:
        return [], []
    V0 = recs[0][1]
    ts = []
    for k in range(0, 40):
        tgt = V0 * 2 ** k
        hit = next((n for (n, v) in recs if v >= tgt), None)
        if hit is None:
            break
        ts.append((tgt, hit))
    rs = [ts[i][1] / ts[i - 1][1] for i in range(1, len(ts)) if ts[i - 1][1] > 0]
    return ts, rs


def med(x):
    x = sorted(x)
    return x[len(x) // 2] if x else float('nan')


print(f"=== INDEPENDENT Track B reproduction (cap {CAP:,}, tape-derived extent) ===\n")

# ---- (1)(2) the pairing tests --------------------------------------------------------
print("--- (1)(2) PAIRING: maxrun records + their step-times ---\n")
REC = {}
for m in ('B1', 'B2', 'B3', 'B4'):
    recs, halted, _ = run(MACH[m], CAP, 'maxrun')
    REC[m] = recs
    vals = [v for (_, v) in recs][-8:]
    steps = [n for (n, _) in recs][-4:]
    print(f"  {m}: maxrun records (last 8) {vals}")
    print(f"      their step-times   (last 4) {steps}   halted={halted}")

print("\n  B1 vs B2:  (compare the REGISTER CASCADE 2^k-2, not the startup transient --")
print("             the pairing claim is about the register law, and both machines have")
print("             a short transient prefix before the cascade locks in)")
CASC = {2 ** k - 2 for k in range(2, 20)}
c1 = [(n, v) for (n, v) in REC['B1'] if v in CASC and v >= 14]
c2 = [(n, v) for (n, v) in REC['B2'] if v in CASC and v >= 14]
L = min(len(c1), len(c2))
print(f"\n    B1 cascade values: {[v for (_, v) in c1][:L]}")
print(f"    B2 cascade values: {[v for (_, v) in c2][:L]}")
print(f"    cascade VALUES identical over the common {L}: "
      f"{[v for (_, v) in c1][:L] == [v for (_, v) in c2][:L]}")
print(f"    (and they are 2^k-2: {[v for (_,v) in c1][:L] == [2**k - 2 for k in range(4, 4+L)]})")
print(f"\n    B1 cascade step-times: {[n for (n, _) in c1][:L]}")
print(f"    B2 cascade step-times: {[n for (n, _) in c2][:L]}")
st_same = [n for (n, _) in c1][:L] == [n for (n, _) in c2][:L]
print(f"    step-times identical: {st_same}")
print("    => a TNF/mirror relabel would preserve step counts EXACTLY.  "
      f"{'They do NOT -- B2 is a genuinely DISTINCT machine with an identical register law.' if not st_same else 'They DO.'}")

print("\n  B3 vs B4:")
v3 = [v for (_, v) in REC['B3']]
v4 = [v for (_, v) in REC['B4']]
print(f"    B3 maxrun records: {v3[-8:]}")
print(f"    B4 maxrun records: {v4[-8:]}")
print(f"    peak-identical: {v3 == v4}")
for nm, vv in (('B3', v3), ('B4', v4)):
    for base in (7, 3, 5, 9):
        ks = [v / base for v in vv[-6:]]
        if all(abs(x - round(x)) < 1e-9 and round(x) & (round(x) - 1) == 0 for x in ks if x >= 1):
            print(f"    {nm} last-6 records are {base}*2^k: {vv[-6:]}")
            break

# ---- (5)(6) the island-wide cost ratio, F3-gated --------------------------------------
print("\n--- (5)(6) PER-DOUBLING COST RATIO (F3 doubling_gate enforced) ---\n")
print(f"  {'m':<4}{'obs':<8}{'gate':<22}{'median ratio':>13}   verdict")
OBS = {'B1': 'maxrun', 'B2': 'maxrun', 'B3': 'total1', 'B4': 'total1',
       'W1': 'total1', 'W2': 'total1', 'W3': 'total1'}
RATIO = {}
for m, o in OBS.items():
    recs, halted, _ = run(MACH[m], CAP, o)
    ok, inoct, top = doubling_gate(recs)
    ts, rs = ratios(recs)
    if not ok:
        print(f"  {m:<4}{o:<8}{'FAIL ('+str(inoct)+' recs in top octave)':<22}"
              f"{'--':>13}   INAPPLICABLE -- not a doubler (F3)")
        RATIO[m] = None
        continue
    r = med(rs)
    RATIO[m] = r
    v = 'QUADRATIC Theta(v^2)' if 3.5 < r < 4.6 else ('LINEAR (braid-free!)' if 1.7 < r < 2.3
                                                      else 'indeterminate')
    print(f"  {m:<4}{o:<8}{'pass ('+str(inoct)+' in top octave)':<22}{r:>13.3f}   {v}")

# W1 in detail -- is it a ramp?
print("\n  W1 detail (is the register a doubler or an arithmetic ramp?):")
recs, _, _ = run(MACH['W1'], CAP, 'total1')
vals = [v for (_, v) in recs]
print(f"    total1 records: {len(vals)} of them; first 8 {vals[:8]}, last 4 {vals[-4:]}")
if len(vals) > 8:
    d = [vals[i + 1] - vals[i] for i in range(len(vals) - 1)]
    print(f"    consecutive record increments: first 8 {d[:8]}")
    big = [x for x in d if x > 100]
    print(f"    increments > 100: {big[:8]}   (a DOUBLER's increments track v, a RAMP's are ~const)")
recs_mr, _, _ = run(MACH['W1'], CAP, 'maxrun')
print(f"    W1 maxrun records: {[v for (_,v) in recs_mr]}   "
      f"(maxrun bounded => no long run ever forms => no binary register)")

# ---- (3) B5's phase-conditioned register ----------------------------------------------
print("\n--- (3) B5: the phase-conditioned register (state C at a left-extent record) ---\n")


def b5_phase(cap):
    """EVERY phase milestone (full-tape maxrun at a left-extent record in state C).
    NOT record-filtered: the phase series rises and resets, so a running-max filter
    would turn it into a ramp and destroy the register."""
    R = parse(MACH['B5'])
    tape = bytearray(SZ)
    p = N; s = 0; n = 0; lo = hi = p
    out = []
    while n < cap:
        t = R[s + tape[p]]
        if t is None:
            break
        w, d, ns = t
        tape[p] = w; p += d; s = ns; n += 1
        if p < 4 or p > SZ - 4:
            raise RuntimeError('tape exhausted -- widen SZ')
        rec = p < lo                     # LEFT-extent record ...
        if p < lo: lo = p
        if p > hi: hi = p
        if rec and s == 4:               # ... in state C  (the phase; C -> index 4)
            out.append((n, maxrun_and_total(tape)[1]))
    return out


def first_attainment(traj, family):
    """First step at which the phase register attains each family value.
    A TIMING statistic on a max -- the class that survives partial views of the orbit."""
    out, seen = [], set()
    for step, v in traj:
        if v in family and v not in seen:
            seen.add(v)
            out.append((v, step))
    return sorted(out)


ph = b5_phase(CAP)
print(f"  {len(ph)} phase milestones; the series RISES AND RESETS "
      f"(first 24 values {[v for (_, v) in ph][:24]})")
print("  -- so it is NOT record-filtered: a running max would flatten it into a ramp.\n")
FAMILY = {9 * 2 ** k - 1 for k in range(1, 12)}
pk = first_attainment(ph, FAMILY)
print(f"  family 9*2^k-1 = {sorted(FAMILY)[:7]}   (family INHERITED from 6b6d739/885f6de,")
print("   not re-derived here; what IS re-derived is that it is attained, and WHEN)")
print(f"\n  {'peak':>8}{'first attained at step':>24}{'ratio':>9}")
prev, rs = None, []
for v, s in pk:
    if prev:
        rs.append(s / prev)
        print(f"  {v:>8}{s:>24,}{s/prev:>9.3f}")
    else:
        print(f"  {v:>8}{s:>24,}{'-':>9}")
    prev = s
if rs:
    print(f"\n  per-doubling ratios: {[round(r, 3) for r in rs]}")
    print(f"  median of the last 4: {med(rs[-4:]):.3f}")
    print(f"  => {'QUADRATIC Theta(v^2) -- BRAID-BOUND' if 3.4 < med(rs[-4:]) < 4.7 else 'LINEAR?' if med(rs[-4:]) < 2.6 else '?'}")
B5R = med(rs[-4:]) if rs else float('nan')

# and the GLOBAL B5 record, to show why the phase conditioning was necessary (fault F3)
grec, _, _ = run(MACH['B5'], CAP, 'maxrun')
ok, inoct, top = doubling_gate(grec)
gv = [v for (_, v) in grec][-6:]
print(f"\n  B5 GLOBAL maxrun record: {len(grec)} records, last 6 {gv}")
print(f"  increments there: {[gv[i+1]-gv[i] for i in range(len(gv)-1)]}  (an arithmetic RAMP)")
print(f"  doubling_gate: {'pass' if ok else 'FAIL'} ({inoct} records in the top octave)")
print("  => reading a ratio off the GLOBAL record would be the F3 artifact.  The phase")
print("     conditioning is what makes B5's register visible at all.")

# ---- (4) B5's per-generation dense floor = 14? ----------------------------------------
print("\n--- (4) B5: the per-generation DENSE floor of full-tape maxrun ---\n")
print("  (a per-generation MINIMUM.  Minima are taken stride-1 ONLY -- maxrun can drop by")
print("   an arbitrary amount in ONE step when a write splits a run, so no stride>1 is sound.)")
peaks = [(s, v) for (v, s) in pk]           # (step, value) of each register peak
print(f"\n  generations delimited by the register peaks: {[v for (_, v) in peaks]}")
DENSE_BUDGET = int(sys.argv[2]) if len(sys.argv) > 2 else 400_000
print(f"\n  {'gen':<5}{'from peak':>10}{'to peak':>9}{'TRUE min maxrun (dense stride-1)':>36}")
for i in range(len(peaks) - 1):
    a, va = peaks[i]
    b, vb = peaks[i + 1]
    if b - a > DENSE_BUDGET:
        print(f"  {i:<5}{va:>10}{vb:>9}"
              f"{'(not scanned: ' + format(b - a, ',') + ' steps > budget)':>36}")
        continue
    _, _, dmin = run(MACH['B5'], b + 1, 'maxrun', dense_from=a, dense_to=b)
    print(f"  {i:<5}{va:>10}{vb:>9}{dmin:>36}")

print("\n=== SUMMARY OF WHAT REPRODUCED ===")
print("  ratios: " + ', '.join(f"{m} {RATIO[m]:.2f}" for m in RATIO if RATIO[m]) +
      f", B5 {B5R:.2f}")
found2 = [m for m in RATIO if RATIO[m] and 1.7 < RATIO[m] < 2.3]
print(f"  ratio-2 (braid-free) machines found: {found2 if found2 else 'NONE'}")
print("\nNo machine decided. No label upgraded.")
