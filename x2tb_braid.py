#!/usr/bin/env python3
"""x2tb_braid.py -- THE decisive test, applied island-wide (2026-07-17).

THE TEST (the one that settled B5, 885f6de/6b6d739).  A carry-transparent machine
carries a register v that DOUBLES each macro-generation.  Ask what a doubling COSTS:

    t_k := first step at which the register observable reaches   V0 * 2^k
    ratio_k := t_k / t_{k-1}

    ratio -> 2  ==  cost is LINEAR in the register  ==  braid-FREE
    ratio -> 4  ==  cost is Theta(v^2) = Theta(4^k) ==  the SAME quadratic braid
                    that walls B1/x2 (the shrinking-comb double induction).

Equivalently: log-log slope of t against the register record.  slope 1 = linear,
slope 2 = quadratic.  Both are reported; they are the same content twice, and they
must agree or the reading is not trustworthy.

WHY THIS FORM.  It needs NO per-machine peak law (9*2^k-1 vs 7*2^k vs 2^k-2 all
work), so one instrument covers the whole island and no machine gets a bespoke
reading that could hide a bespoke bug.  It is a MAX/TIMING statistic only -- the
class that survived both instrument faults -- and every observable comes from
x2tb_sim.feats(), whose extent is derived from the tape (fault F1 inexpressible).

Decides NO halting.  No label upgraded.
"""

import sys
from math import log
from x2tb_sim import MACHINES, REGISTER_OBS, OBS_IDX, run


def record_curve(samples, idx):
    """[(step, record_value)] each time the full-tape observable sets a new record."""
    out = []
    best = -1
    for s in samples:
        v = s[idx]
        if v > best:
            best = v
            out.append((s[0], v))
    return out


def thresholds(curve, V0, kmax=14):
    """t_k = first step at which the record reaches >= V0*2^k."""
    res = []
    for k in range(kmax + 1):
        T = V0 * (2 ** k)
        t = next((st for st, v in curve if v >= T), None)
        if t is None:
            break
        res.append((k, T, t))
    return res


def doubling_gate(curve):
    """DOES THE REGISTER ACTUALLY DOUBLE?  The ratio test is MEANINGLESS unless it does.

    This gate is the whole reason the reading can be trusted.  For ANY machine whose
    step count grows like width^2 -- which includes every ordinary quadratic bouncer --
    "the cost to double the observable" is 4x AUTOMATICALLY, with no braid anywhere.
    So a ratio of 4 is evidence of a braid ONLY for a register that genuinely doubles
    once per macro-generation.  W1 fails this gate: its total1 is an arithmetic ramp
    (+~446 per milestone), and reporting "W1: braid" from its ratio-4 would be exactly
    the artifact class this audit exists to catch.

    Test: count distinct record values in the top octave [top/8, top].  A doubler sets
    O(1) records there (it jumps); a linear ramp sets ~7*top/8 of them (it increments).
    Returns (is_doubler, n_records_in_top_octave, top_octave_values).
    """
    if not curve:
        return False, 0, []
    top = curve[-1][1]
    oct_vals = sorted({v for _, v in curve if v >= top / 8})
    return (len(oct_vals) <= 12), len(oct_vals), oct_vals[-6:]


def probe(name, cap, V0=None):
    spec = MACHINES[name]
    ob = REGISTER_OBS[name]
    idx = OBS_IDX[ob]
    outc, step, S = run(spec, cap)
    curve = record_curve(S, idx)
    if not curve:
        print(f"{name}: no record curve")
        return
    top = curve[-1][1]
    if V0 is None:
        V0 = 8
        while V0 * 32 < top:            # keep >=5 doublings inside the run
            V0 *= 2
        V0 = max(8, top // 128 or 8)
    is_doub, noct, octv = doubling_gate(curve)
    print(f"\n=== {name}  {spec}")
    print(f"    outc={outc} steps={step} register={ob} top_record={top} "
          f"nsamp={len(S)} V0={V0}")
    print(f"    doubling gate: {noct} distinct records in top octave, tail {octv}"
          f"  -> {'DOUBLER' if is_doub else 'ARITHMETIC RAMP (not a doubler)'}")
    if not is_doub:
        print("    ==> RATIO TEST INAPPLICABLE: the register does not double, so a "
              "cost-ratio of 4\n        would follow from steps ~ width^2 alone "
              "(any quadratic bouncer) and is NOT\n        evidence of a braid. "
              "No braid verdict is reported for this machine.")
        return name, ob, float('nan'), 'INAPPLICABLE (register not a doubler)'
    th = thresholds(curve, V0)
    print(f"    {'k':>3} {'thresh':>8} {'t_k':>14} {'ratio':>8}")
    prev = None
    ratios = []
    for k, T, t in th:
        r = (t / prev) if prev else 0.0
        if prev:
            ratios.append(r)
        print(f"    {k:>3} {T:>8} {t:>14} {r:>8.3f}" if prev
              else f"    {k:>3} {T:>8} {t:>14} {'-':>8}")
        prev = t
    tail = ratios[-4:]
    med = sorted(tail)[len(tail) // 2] if tail else float('nan')
    verdict = ('LINEAR cost (braid-free)' if med < 2.6
               else 'QUADRATIC cost Theta(v^2)' if med > 3.4 else 'AMBIGUOUS')
    print(f"    tail ratios {[round(x, 3) for x in tail]}  median={med:.3f}"
          f"   exponent log2(ratio)={log(med, 2):.3f}  (1=linear, 2=quadratic)")
    print(f"    ==> {verdict}")
    return name, ob, med, verdict


if __name__ == '__main__':
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 40_000_000
    names = sys.argv[2:] or ['B1', 'B2', 'B3', 'B4', 'B5', 'W1']
    rows = []
    for n in names:
        r = probe(n, cap)
        if r:
            rows.append(r)
    print("\n\n=== ISLAND COST-SIGNATURE TABLE (cap %d) ===" % cap)
    print(f"{'machine':>8} {'register':>8} {'ratio/doubling':>16} {'exponent':>9}  verdict")
    for name, ob, med, verdict in rows:
        e = f"{log(med, 2):.3f}" if med == med else "-"
        m = f"{med:.3f}" if med == med else "-"
        print(f"{name:>8} {ob:>8} {m:>16} {e:>9}  {verdict}")
    print("\nratio 2 (exponent 1) = linear cost per doubling = braid-free")
    print("ratio 4 (exponent 2) = Theta(v^2) cost per doubling = the B1/x2 cost signature")
    print("\nHONESTY: ratio 4 is a COST SIGNATURE, not a structural identification. It shows a")
    print("doubling costs Theta(v^2) -- i.e. it is NOT a single-sweep repack but Theta(v)")
    print("passes over the register. That is the signature the shrinking-comb braid PRODUCES;")
    print("it does not by itself prove the same combinatorial braid (growing-arity digit tree).")
    print("[OBSERVED]. No machine decided. No label upgraded.")
