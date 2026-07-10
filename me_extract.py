#!/usr/bin/env python3
"""
me_extract.py -- AUTOMATIC MULTIPLIER EXTRACTOR (the width-independent engine probe).

Goal: read the value-x(p/q) engine of a digit-string counter machine WITHOUT the tape
width, to test whether the 1087 un-catalogued BB(6) holdouts collapse to the ~5 known
engine-classes {x3/2, x4/3, x8/3, x5/2, ceiling-x3/2}. STRICT VALIDATION-FIRST: the tool is
untrusted until it recovers the KNOWN multipliers of the 17 named cryptids. Every output is
[OBSERVED, extractor proxy], NOT a certified engine assignment; it decides NO halting.

The width-independent multiplier signal (task spec, DATA_SUMMARY_2026-07-10 sec 4):
  MILESTONE = a record-extreme excursion (head reaching a new leftmost / new rightmost cell),
  deduped so one outward sweep counts once (the raw per-cell record burst is collapsed).
Three estimators of the multiplier of the abstract counter, all width-independent:
  rho_time = geometric ratio of consecutive inter-milestone STEP-GAPS on the FAST side
             (one milestone per macro-period). For a value-x(p/q) counter whose per-period
             work is proportional to the VALUE (unary width), g_{k+1}/g_k -> p/q.
  rho_slow = noise-filtered geometric ratio of the SLOW-side inter-excursion step-gaps
             (independent cross-check; for a digit-string counter this is (p/q)^m for an
             unknown machine-specific multiplicity m).
  rho_val  = ratio of the tape decoded as a big integer (LSB order) at successive fast
             milestones (a value cross-check).
Agreement of two independent estimators raises confidence.

Interpreter: /Users/aokiyousuke/quantum-ecc/.venv/bin/python  (exact big-int decode).
No machine decided. No label upgraded.
"""
import sys, math
from fractions import Fraction

NAMED = {  # the 17 named cryptids -> (spec, KNOWN multiplier) ; the VALIDATION GATE
    "Antihydra":   ("1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA", Fraction(3, 2)),
    "SpaceNeedle": ("1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD", Fraction(5, 2)),
    "o2":  ("1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA", Fraction(3, 2)),  # ceiling
    "o3":  ("1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC", Fraction(4, 3)),
    "o4":  ("1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---", Fraction(4, 3)),
    "o5":  ("1RB0LB_1LC0RE_1LA1LD_0LC---_0RB0RF_1RE1RB", Fraction(4, 3)),
    "o7":  ("1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC", Fraction(3, 2)),  # two-mult B2
    "o8":  ("1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_---1LE", Fraction(3, 2)),
    "o10": ("1RB1RA_0RC1RC_1LD0LF_0LE1LE_1RA0LB_---0LC", Fraction(3, 2)),
    "o11": ("1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF", Fraction(3, 2)),
    "o12": ("1RB0RE_1LC1LD_0RA0LD_1LB0LA_1RF1RA_---1LB", Fraction(3, 2)),
    "o13": ("1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA", Fraction(3, 2)),
    "o14": ("1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE", Fraction(3, 2)),
    "o15": ("1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA", Fraction(8, 3)),
    "o16": ("1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE", Fraction(3, 2)),
    "o17": ("1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB", None),  # gate-timing, no scalar p/q
    "o18": ("1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---", Fraction(8, 3)),
}

ENGINES = {Fraction(3, 2): "x3/2", Fraction(4, 3): "x4/3", Fraction(8, 3): "x8/3",
           Fraction(5, 2): "x5/2"}  # the KNOWN engine-classes (ceiling-3/2 == 3/2 numeric)


def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if (t[0] == '-' or t[2] in 'Z-')
                       else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M


def simulate(spec, maxsteps, SZ=1 << 23, sample_val=False, max_val=400):
    """Return (outcome, step, Lrec, Rrec[, val_samples]). Lrec/Rrec = step indices at which a
    new leftmost/rightmost record was set. Optionally snapshot fast-side tape decodes."""
    M = parse(spec)
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    Lrec = []; Rrec = []
    Lval = []; Rval = []
    while step < maxsteps:
        r = tape[pos]
        act = M[st][r] if r < 2 else None
        if act is None:
            return ('HALT', step, Lrec, Rrec, Lval, Rval)
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo:
            lo = pos; Lrec.append(step)
            if sample_val and len(Lval) < max_val:
                Lval.append(int.from_bytes(bytes(tape[lo:hi + 1]).replace(b'\x00', b'\x00'), 'little'))
        elif pos > hi:
            hi = pos; Rrec.append(step)
            if sample_val and len(Rval) < max_val:
                Rval.append(int.from_bytes(bytes(tape[lo:hi + 1]), 'little'))
        if pos < 8 or pos > SZ - 8:
            return ('OVR', step, Lrec, Rrec, Lval, Rval)
    return ('MAX', step, Lrec, Rrec, Lval, Rval)


def excursions(recsteps):
    """Collapse a per-cell record burst (consecutive step indices = one outward sweep) to one
    milestone (the sweep apex). Returns the list of apex step indices."""
    if not recsteps:
        return []
    out = [recsteps[0]]
    for i in range(1, len(recsteps)):
        if recsteps[i] - recsteps[i - 1] == 1:
            out[-1] = recsteps[i]
        else:
            out.append(recsteps[i])
    return out


def geom_ratio(steps, filt=False, drop_frac=0.34):
    """Robust geometric ratio of consecutive inter-milestone step-gaps via log-linear
    regression of log(gap) vs index. filt=True keeps only >=median gaps (removes spurious
    tiny excursions on the slow side). Returns (ratio, n_used) or (None,0)."""
    if len(steps) < 6:
        return None, 0
    gaps = [steps[i] - steps[i - 1] for i in range(1, len(steps))]
    gaps = [g for g in gaps if g > 0]
    if filt:
        thr = sorted(gaps)[len(gaps) // 2]
        gaps = [g for g in gaps if g >= thr]
    else:
        gaps = gaps[int(len(gaps) * drop_frac):]  # drop transient head
    if len(gaps) < 4:
        return None, 0
    ly = [math.log(g) for g in gaps]; xs = list(range(len(gaps)))
    n = len(xs); mx = sum(xs) / n; my = sum(ly) / n
    den = sum((x - mx) ** 2 for x in xs)
    if den == 0:
        return None, 0
    slope = sum((xs[i] - mx) * (ly[i] - my) for i in range(n)) / den
    return math.exp(slope), n


def val_ratio(vals):
    """Median consecutive ratio of a value-sample sequence (tail half)."""
    vals = [v for v in vals if v and v > 0]
    if len(vals) < 8:
        return None
    tail = vals[len(vals) // 2:]
    lr = [math.log(tail[i]) - math.log(tail[i - 1])
          for i in range(1, len(tail)) if tail[i - 1] > 0]
    if len(lr) < 4:
        return None
    lr.sort()
    med = lr[len(lr) // 2]
    return math.exp(med) if med < 30 else float('inf')


def match_engine(rho, tol=0.04):
    """Nearest KNOWN engine within tol, else nearest simple rational (denominator<=9)."""
    if rho is None or rho <= 1.0:
        return None, None
    best = None; bd = tol
    for f in ENGINES:
        d = abs(rho - float(f))
        if d < bd:
            bd = d; best = f
    if best is not None:
        return ENGINES[best], best
    fr = Fraction(rho).limit_denominator(9)
    if abs(float(fr) - rho) < 0.02 and float(fr) > 1.0:
        return f"~{fr}(cand-new)", fr
    return None, None


def extract(spec, cap=3_000_000, sample_val=False):
    """Full extractor. Returns a dict of all estimators + engine match + agreement flag."""
    out, step, Lrec, Rrec, Lval, Rval = simulate(spec, cap, sample_val=sample_val)
    Lx = excursions(Lrec); Rx = excursions(Rrec)
    # fast side = more excursions (one per macro-period); slow side = fewer
    if len(Rx) >= len(Lx):
        fast, slow, fval = Rx, Lx, Rval
    else:
        fast, slow, fval = Lx, Rx, Lval
    rho_time, n_t = geom_ratio(fast, filt=False)
    rho_slow, n_s = geom_ratio(slow, filt=True)
    rho_v = val_ratio(fval) if sample_val else None
    # primary engine call from rho_time (the task's primary width-independent estimator)
    eng_t, f_t = match_engine(rho_time)
    # slow-side: report (p/q)^m best decomposition for each known engine
    slow_hits = []
    if rho_slow and rho_slow > 1.02:
        for f in ENGINES:
            for m in range(1, 7):
                if abs(rho_slow ** (1.0 / m) - float(f)) < 0.03:
                    slow_hits.append((ENGINES[f], m))
    agree = (eng_t is not None and rho_v is not None and f_t is not None
             and abs(rho_v - float(f_t)) < 0.04)
    return dict(out=out, step=step, nfast=len(fast), nslow=len(slow),
                rho_time=rho_time, rho_slow=rho_slow, rho_val=rho_v,
                eng_time=eng_t, slow_hits=slow_hits, agree=agree)


def gate():
    print("=== VALIDATION GATE: 17 named cryptids (KNOWN multipliers must be recovered) ===")
    print(f"{'name':11} {'true':>7} {'out':>4} {'nfast':>6} {'nslow':>5} "
          f"{'rho_time':>9} {'rho_slow':>9} {'rho_val':>8}  time-engine   slow (p/q)^m")
    npass = 0; ntest = 0
    for name, (sp, true) in NAMED.items():
        c = extract(sp, cap=8_000_000, sample_val=True)
        rt = f"{c['rho_time']:.4f}" if c['rho_time'] else "   -  "
        rs = f"{c['rho_slow']:.4f}" if c['rho_slow'] else "   -  "
        rv = f"{c['rho_val']:.3f}" if c['rho_val'] else "  -  "
        et = c['eng_time'] or "-"
        sh = ",".join(f"{n}^{m}" for n, m in c['slow_hits'][:4]) or "-"
        tstr = f"{float(true):.4f}" if true else "  n/a"
        ok = ""
        if true is not None:
            ntest += 1
            # PASS iff a primary estimator recovers the true multiplier within tol
            recovered = (c['eng_time'] is not None and c['eng_time'].startswith(ENGINES.get(true, "###")))
            if recovered:
                npass += 1; ok = " PASS"
            else:
                ok = " miss"
        print(f"{name:11} {tstr:>7} {c['out']:>4} {c['nfast']:>6} {c['nslow']:>5} "
              f"{rt:>9} {rs:>9} {rv:>8}  {et:<12} {sh}{ok}")
    print(f"\nGATE RESULT: primary estimator (rho_time) recovered {npass}/{ntest} known "
          f"multipliers.")
    print("The extractor is TRUSTED for the 1104 only if this gate passes cleanly.")
    return npass, ntest


if __name__ == "__main__":
    gate()
