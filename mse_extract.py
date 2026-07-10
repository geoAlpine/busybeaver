#!/usr/bin/env python3
"""
mse_extract.py -- PROPER milestone-form multiplier extractor (the real per-machine
automation of the hand analysis the 17 named cryptids received).

The coarse tool (me_extract.py) FAILED its gate: rho_time is linear for digit-string
machines, and rho_slow=(p/q)^m is non-identifying WITHOUT the macro-period m
(MULTIPLIER_EXTRACTOR_2026-07-10.md). This proper version supplies m by detecting the
MACRO-PERIOD (config-shape recurrence) and reading the value map directly.

TWO width-independent, IDENTIFYING estimators of the abstract counter's multiplier p/q:

  (T) BLOCK-TRANSFER RATE.  During a macro-sweep a value-x(p/q) counter converts a source
      block to a destination block at the p:q rewrite rate.  At fast-side record milestones,
      RLE the tape; over a window of milestones with a fixed run-count, each run length is
      arithmetic (constant per-milestone increment Delta_r).  The ratio (max +Delta)/(max -Delta)
      is p/q exactly.  Fires for the sweep/sea x3/2 family (Antihydra & kin).

  (S) SAWTOOTH MACRO-PERIOD.  A base-(p/q) odometer resets each macro-period: a value
      observable (total 1s / max 1-run / width) is a sawtooth that peaks then resets.  The
      macro-period is the segment between resets; the ratio of consecutive segment PEAKS is
      p/q (the value map v_{k+1} ~ (p/q) v_k).  Cross-check: the segment START-STEP ratio ~
      (p/q)^2 (total steps ∝ value²), so peak-ratio ~ sqrt(step-ratio).  Fires for the
      base-(p/q) odometers (o4/o5 x4/3, o15/o18 x8/3, Space Needle x5/2).

Each rho is matched to the nearest KNOWN engine {3/2,4/3,8/3,5/2} within tol, else the
nearest simple rational (candidate-new).  Two independent signals agreeing, or the
peak~sqrt(step) self-consistency, raises confidence.

STRICT: every output is [OBSERVED, extractor], NOT a certified engine assignment; decides
NO halting.  An extracted multiplier is strong evidence, not a certified reduction (the
milestone-form still needs a proof).  Interpreter: /Users/aokiyousuke/quantum-ecc/.venv/bin/python
(exact big-int / Fraction).  No machine decided.  No label upgraded.
"""
import sys, math
from fractions import Fraction

NAMED = {  # 17 named cryptids -> (spec, KNOWN multiplier). The VALIDATION GATE.
    "Antihydra":   ("1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA", Fraction(3, 2)),
    "SpaceNeedle": ("1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD", Fraction(5, 2)),
    "o2":  ("1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA", Fraction(3, 2)),  # ceiling
    "o3":  ("1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC", Fraction(4, 3)),
    "o4":  ("1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---", Fraction(4, 3)),
    "o5":  ("1RB0LB_1LC0RE_1LA1LD_0LC---_0RB0RF_1RE1RB", Fraction(4, 3)),
    "o7":  ("1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC", Fraction(3, 2)),  # two-mult B2 (even branch 3/2)
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
           Fraction(5, 2): "x5/2"}


def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if (t[0] == '-' or t[2] in 'Z-')
                       else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M


def rle(tape, lo, hi):
    out = []; i = lo
    while i <= hi:
        s = tape[i]; n = 0
        while i <= hi and tape[i] == s:
            n += 1; i += 1
        out.append((s, n))
    return out


def _feats(tape, lo, hi):
    """One O(width) pass -> (total1, maxrun1, width, RLE-tuple)."""
    r = rle(tape, lo, hi)
    tot1 = sum(n for c, n in r if c == 1)
    mx = max((n for c, n in r if c == 1), default=0)
    return tot1, mx, hi - lo + 1, tuple(r)


def simulate(spec, maxsteps, SZ=1 << 23, tailK=160):
    """Memory-bounded milestone recorder. For each side keep the full per-milestone
    feature list feat=(step,state,total1,maxrun,width) plus a ring buffer of the last
    tailK full RLEs (only the tail is needed by the transfer estimator). A milestone =
    a deduped record-extreme excursion. fast side = the side with more milestones."""
    M = parse(spec)
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    Lf = []; Rf = []; Lr = []; Rr = []   # feats; tail-rle rings (step, rle)
    while step < maxsteps:
        r = tape[pos]
        act = M[st][r] if r < 2 else None
        if act is None:
            outc = 'HALT'; break
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo:
            lo = pos
            t1, mx, w, rt = _feats(tape, lo, hi)
            if Lf and Lf[-1][0] == step - 1:
                Lf[-1] = (step, st, t1, mx, w); Lr[-1] = (step, rt)
            else:
                Lf.append((step, st, t1, mx, w)); Lr.append((step, rt))
                if len(Lr) > tailK:
                    Lr.pop(0)
        elif pos > hi:
            hi = pos
            t1, mx, w, rt = _feats(tape, lo, hi)
            if Rf and Rf[-1][0] == step - 1:
                Rf[-1] = (step, st, t1, mx, w); Rr[-1] = (step, rt)
            else:
                Rf.append((step, st, t1, mx, w)); Rr.append((step, rt))
                if len(Rr) > tailK:
                    Rr.pop(0)
        if pos < 8 or pos > SZ - 8:
            outc = 'OVR'; break
    else:
        outc = 'MAX'
    if len(Rf) >= len(Lf):
        fast, slow, ftail = Rf, Lf, Rr
    else:
        fast, slow, ftail = Lf, Rf, Lr
    return outc, step, fast, slow, ftail, len(Lf), len(Rf)


def _med(xs):
    xs = sorted(xs)
    return xs[len(xs) // 2] if xs else None


# ---------- estimator (T): block-transfer rate ----------
def est_transfer(ftail):
    """During a macro-sweep the head converts a source run to a dest run at the p:q rewrite
    rate. Over a window of milestones with a fixed run-count, each run length is arithmetic;
    among the runs with a CONSISTENT nonzero per-milestone increment, the ratio
    (max +Delta)/(max -Delta) is p/q. Static runs (increment 0) are ignored, so machines with
    many frozen blocks plus one active +/- pair (o10/o12/o13/o14) are handled.
    ftail = list of (step, RLE-tuple). Returns (Fraction p/q, (nruns, increments)) or (None,None)."""
    if len(ftail) < 10:
        return None, None
    from collections import Counter
    for W in (24, 40, 80):
        tail = [(s, r) for s, r in ftail[-W:]]
        cnt = Counter(len(r) for s, r in tail)
        nruns, freq = cnt.most_common(1)[0]
        if freq < max(6, int(0.6 * len(tail))) or nruns < 2:
            continue
        seq = [r for s, r in tail if len(r) == nruns]
        if len(seq) < 6:
            continue
        incs = []
        for r in range(nruns):
            lens = [seq[k][r][1] for k in range(len(seq))]
            diffs = [lens[k] - lens[k - 1] for k in range(1, len(lens))]
            m = _med(diffs)
            # require a CONSISTENT increment: >=70% of diffs share m's sign (or m==0)
            if m == 0:
                incs.append(0); continue
            agree = sum(1 for d in diffs if (d > 0) == (m > 0) and d != 0)
            incs.append(m if agree >= 0.7 * len(diffs) else 0)
        pos = [x for x in incs if x > 0]
        neg = [-x for x in incs if x < 0]
        if not pos or not neg:
            continue
        mp, mn = max(pos), max(neg)
        if mp > 40 or mn > 40:        # a genuine p:q rewrite uses small integer rates
            continue
        fr = Fraction(mp, mn)
        if 1 < fr <= 5 and fr.denominator <= 9:
            return fr, (nruns, incs)
    return None, None


# ---------- estimator (S): sawtooth macro-period ----------
def _segments(vals):
    """Boundaries where the value jumps up sharply or drops sharply -> macro-resets."""
    n = len(vals); bnds = [0]
    for k in range(1, n):
        p = vals[k - 1]
        if p > 0 and (vals[k] > 1.4 * p or vals[k] < 0.55 * p):
            bnds.append(k)
    bnds.append(n)
    return [(bnds[i], bnds[i + 1]) for i in range(len(bnds) - 1) if bnds[i + 1] - bnds[i] >= 2]


def est_sawtooth(fast):
    """fast = list of (step,state,total1,maxrun,width). Best
    (peak_ratio, step_ratio, nseg, observable, selfconsistent) over observables."""
    if len(fast) < 24:
        return None
    steps = [s[0] for s in fast]
    obs = {
        'total1': [s[2] for s in fast],
        'maxrun': [s[3] for s in fast],
        'width':  [s[4] for s in fast],
    }
    best = None
    for name, vals in obs.items():
        segs = _segments(vals)
        if len(segs) < 5:
            continue
        segs = segs[2:]          # drop transient
        peaks = [max(vals[a:b]) for a, b in segs]
        stimes = [steps[a] for a, b in segs]
        if len(peaks) < 4:
            continue
        pr = [peaks[i + 1] / peaks[i] for i in range(len(peaks) - 1) if peaks[i] > 0]
        tr = [(stimes[i + 1] - stimes[i]) / (stimes[i] - stimes[i - 1])
              for i in range(1, len(stimes) - 1) if stimes[i] - stimes[i - 1] > 0]
        if len(pr) < 3:
            continue
        p_ratio = _med(pr); s_ratio = _med(tr) if tr else None
        # self-consistency: peak-ratio ~ sqrt(step-ratio) for a value-x(p/q), steps ∝ value²
        sc = (s_ratio is not None and s_ratio > 1 and
              abs(p_ratio - math.sqrt(s_ratio)) < 0.2 * p_ratio)
        cand = (p_ratio, s_ratio, len(peaks), name, sc)
        # prefer more segments and self-consistency
        key = (sc, len(peaks))
        if best is None or key > (best[4], best[2]):
            best = cand
    return best


# ---------- estimator (G): slow-side base-odometer power-fit ----------
def _dedupe(vals, steps):
    ov = []; os_ = []
    for v, s in zip(vals, steps):
        if not ov or ov[-1] != v:
            ov.append(v); os_.append(s)
    return ov, os_


def est_slow_geom(slow, tailN=14):
    """Catch the base-(p/q) odometer whose VALUE register lives on the SLOW side (the
    macro-generation record-extremes), not the fast intra-generation crawl.  This is the
    o2/o3 class: the fast side is a LINEAR crawl (+1/milestone), while the odometer grows
    x(p/q) per macro-generation but is only sampled at record-breaking slow-side extremes,
    which SKIP generations irregularly -- so a slow ratio appears as an INTEGER POWER e^n of
    the true multiplier e (o2: 3.55,2.27,1.503 = powers of 3/2; o3: ~1.33 = 4/3).

    Power-fit test (identifying + safe): report a KNOWN engine e only if, over the slow-side
    tail, (i) each record-extreme ratio r_i is a consistent integer power e^{n_i} (n_i>=1),
    AND (ii) the step-ratio tracks value-ratio^2 (steps ∝ value^2, holds at any skip depth).
    Requiring EVERY ratio to be a power of a SINGLE engine is strong enough that no other
    named machine's slow side false-fires.  Returns (Fraction e, observable, nfit, nsc) or None."""
    if len(slow) < 6:
        return None
    best = None
    for name, idx in (('total1', 2), ('maxrun', 3), ('width', 4)):
        vals = [f[idx] for f in slow]; steps = [f[0] for f in slow]
        vals, steps = _dedupe(vals, steps)
        if len(vals) < 6:
            continue
        v = vals[-tailN:]; s = steps[-tailN:]
        pairs = []
        for i in range(len(v) - 1):
            if v[i] > 0 and s[i] > 0:
                r = v[i + 1] / v[i]; sr = s[i + 1] / s[i]
                if r > 1.05:
                    pairs.append((r, sr))
        if len(pairs) < 3:
            continue
        # per-pair self-consistency: step-ratio ~ value-ratio^2 (true at every skip depth)
        sc = [(r, sr) for r, sr in pairs if sr > 1 and abs(sr - r * r) < 0.20 * r * r]
        if len(sc) < 3:
            continue
        for e in ENGINES:
            fe = float(e); ok = 0; devs = []
            for r, sr in sc:
                n = round(math.log(r) / math.log(fe))
                if n < 1:
                    continue
                pred = fe ** n
                dev = abs(r - pred) / pred
                if dev < 0.06:
                    ok += 1; devs.append(dev)
            if ok >= 3 and ok >= 0.8 * len(sc):
                score = (ok / len(sc), -(sum(devs) / len(devs)), ok)
                if best is None or score > best[0]:
                    best = (score, e, name, ok, len(sc))
    if best:
        return (best[1], best[2], best[3], best[4])
    return None


def match_engine(rho, tol=0.05):
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
    if abs(float(fr) - rho) < 0.03 and 1 < float(fr) <= 6:
        return f"~{fr}(cand-new)", fr
    return None, None


def extract(spec, cap=8_000_000):
    outc, step, fast, slow, ftail, nL, nR = simulate(spec, cap)
    tr, tinfo = est_transfer(ftail)
    saw = est_sawtooth(fast)
    sg = est_slow_geom(slow)   # (G) slow-side base-odometer power-fit (o2/o3 class)
    # candidate multipliers with provenance
    cands = []
    if tr is not None:
        cands.append(('transfer', float(tr), tr))
    if saw is not None:
        eng, f = match_engine(saw[0])
        cands.append(('sawtooth', saw[0], f))
    if sg is not None:
        cands.append(('slowgeom', float(sg[0]), sg[0]))
    # decide reported engine: match each candidate to a known engine
    reported = None; rho_rep = None; conf = None; src = None
    matches = []          # (source, eng_label, fraction, rho, is_known)
    for source, rho, _ in cands:
        eng, f = match_engine(rho)
        if eng is None:
            continue
        is_known = not eng.startswith('~')
        # a candidate-new (non-known) label is only trustworthy if the signal is
        # self-consistent (peak~sqrt-step) or two estimators agree -> else drop it.
        if not is_known:
            sc = (source == 'sawtooth' and saw is not None and saw[4])
            if not sc:
                continue
        matches.append((source, eng, f, rho, is_known))
    if matches:
        known = [m for m in matches if m[4]]
        # transfer is the cleaner exact-integer signal; prefer it among known matches
        known.sort(key=lambda m: 0 if m[0] == 'transfer' else 1)
        pick = known[0] if known else matches[0]
        reported = pick[1]; rho_rep = pick[3]; src = pick[0]
        engset = set(m[1] for m in matches)
        if len(matches) >= 2 and len(engset) == 1:
            conf = 'high(2-estimator agree)'
        elif src == 'transfer':
            conf = 'med(exact-transfer)'
        elif saw is not None and saw[4] and src == 'sawtooth':
            conf = 'med(peak~sqrt-step)'
        elif src == 'slowgeom':
            conf = 'med(slow-geom power-fit)'
        else:
            conf = 'low(1-estimator)'
    return dict(outc=outc, step=step, nfast=len(fast), nslow=len(slow), nL=nL, nR=nR,
                transfer=tr, tinfo=tinfo, sawtooth=saw, slowgeom=sg,
                reported=reported, rho=rho_rep, src=src, conf=conf)


def gate(cap=8_000_000):
    print("=== VALIDATION GATE: 17 named cryptids (KNOWN multipliers must be recovered) ===\n")
    print(f"{'name':11}{'true':>6}  {'out':>4}{'nfast':>6}{'nslow':>6}  "
          f"{'transfer':>9} {'saw-peak':>9} {'slow-geom':>10}  {'REPORTED':>9}  {'conf':<24} ok")
    npass = 0; ntest = 0; rows = []
    for name, (sp, true) in NAMED.items():
        c = extract(sp, cap=cap)
        rows.append((name, true, c))
        tr = str(c['transfer']) if c['transfer'] else "-"
        sw = f"{c['sawtooth'][0]:.4f}" if c['sawtooth'] else "-"
        sg = f"{c['slowgeom'][0]}({c['slowgeom'][1]})" if c.get('slowgeom') else "-"
        rep = c['reported'] or "-"
        conf = c['conf'] or "-"
        ok = ""
        if true is not None:
            ntest += 1
            want = ENGINES[true]
            if c['reported'] == want:
                npass += 1; ok = "PASS"
            elif c['reported'] is None:
                ok = "miss"
            else:
                ok = "WRONG"
        else:
            ok = "n/a(o17)"
        print(f"{name:11}{str(float(true)) if true else 'n/a':>6}  {c['outc']:>4}{c['nfast']:>6}{c['nslow']:>6}  "
              f"{tr:>9} {sw:>9} {sg:>10}  {rep:>9}  {conf:<24} {ok}")
    print(f"\nGATE RESULT: recovered {npass}/{ntest} known multipliers "
          f"(0 WRONG required for trust). o17 has no scalar p/q.")
    wrong = [r[0] for r in rows if r[1] is not None and r[2]['reported'] is not None
             and r[2]['reported'] != ENGINES[r[1]]]
    print(f"WRONG (false labels): {wrong if wrong else 'none'}")
    return npass, ntest, rows


if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 8_000_000
    gate(cap)
