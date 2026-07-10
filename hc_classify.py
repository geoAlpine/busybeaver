#!/usr/bin/env python3
"""
hc_classify.py -- HOLDOUT sweep, PASS 2: species classifier (the genuinely-new pass).
For each machine (blank tape), extract a recurrent frontier-milestone and measure the
multiplier of its abstract counter, three independent ways:
  rho_time  = ratio of consecutive inter-milestone STEP GAPS  (cost/macro-step ~ counter value)
  rho_width = ratio of consecutive milestone TAPE WIDTHS
  rho_val   = ratio of consecutive milestone tape-as-integer DECODES
Match a stable rho against the named engine set {3/2,4/3,8/3,5/2,2,3,...}. Report the
multiplier ONLY when a probe is clean & stable; else 'no clean multiplier'. This OBSERVES a
growth ratio; it DECIDES nothing about halting.
Interpreter: /Users/aokiyousuke/quantum-ecc/.venv/bin/python  (exact big-int decode).
"""
import sys, math
from fractions import Fraction

NAMED = {
    "Antihydra": "1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA",
    "SpaceNeedle": "1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD",
    "o2": "1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA",
    "o3": "1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC",
    "o4": "1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---",
    "o5": "1RB0LB_1LC0RE_1LA1LD_0LC---_0RB0RF_1RE1RB",
    "o7": "1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC",
    "o8": "1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_---1LE",
    "o10": "1RB1RA_0RC1RC_1LD0LF_0LE1LE_1RA0LB_---0LC",
    "o11": "1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF",
    "o12": "1RB0RE_1LC1LD_0RA0LD_1LB0LA_1RF1RA_---1LB",
    "o13": "1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA",
    "o14": "1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE",
    "o15": "1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA",
    "o16": "1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE",
    "o17": "1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB",
    "o18": "1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---",
}

# engine catalogue: multiplier -> name
ENGINES = {
    Fraction(3, 2): "x3/2", Fraction(4, 3): "x4/3", Fraction(8, 3): "x8/3",
    Fraction(5, 2): "x5/2", Fraction(2, 1): "x2", Fraction(3, 1): "x3",
    Fraction(5, 3): "x5/3", Fraction(5, 4): "x5/4", Fraction(7, 4): "x7/4",
    Fraction(7, 3): "x7/3", Fraction(9, 4): "x9/4", Fraction(7, 5): "x7/5",
    Fraction(9, 8): "x9/8", Fraction(9, 5): "x9/5", Fraction(4, 1): "x4",
}


def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if (t[0] == '-' or t[2] in 'Z-')
                        else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M


def collect_milestones(spec, maxsteps, SZ=1 << 22, max_ms=8000):
    """Record a frontier event on EVERY boundary touch (pos==lo or pos==hi), keyed by
    (side, state, symbol-read). Capture (step, width). No integer decode (uninformative:
    full-tape value ~ 2^width). Returns per-key event lists."""
    M = parse(spec)
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    from collections import defaultdict
    ev = defaultdict(list)   # (side,state,sym) -> [(step, width)]
    counts = defaultdict(int)
    while step < maxsteps:
        r = tape[pos]
        act = M[st][r] if r < 2 else None
        if act is None:
            return ('HALT', step, ev)
        ww, d, ns = act
        if pos == lo or pos == hi:
            key = ('L' if pos == lo else 'R', st, r)
            if counts[key] < max_ms:
                ev[key].append((step, hi - lo + 1))
                counts[key] += 1
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo:
            lo = pos
        elif pos > hi:
            hi = pos
    return ('MAX', step, ev)


def stable_ratio(seq):
    """Given a numeric sequence, return (rho, frac_or_None, spread) using the tail.
    rho = median consecutive ratio over the last portion; spread = IQR-ish of those ratios."""
    seq = [x for x in seq if x is not None and x > 0]
    if len(seq) < 8:
        return None, None, None
    tail = seq[len(seq) // 2:]         # drop transient
    ratios = []
    for i in range(1, len(tail)):
        if tail[i - 1] > 0:
            ratios.append(tail[i] / tail[i - 1])
    ratios = [r for r in ratios if r > 0.05]
    if len(ratios) < 6:
        return None, None, None
    ratios.sort()
    n = len(ratios)
    med = ratios[n // 2]
    spread = ratios[int(0.75 * n)] - ratios[int(0.25 * n)]
    return med, None, spread


def match_engine(rho, tol=0.02):
    if rho is None:
        return None
    best = None; bd = tol
    for f, name in ENGINES.items():
        d = abs(rho - float(f))
        if d < bd:
            bd = d; best = (f, name)
    return best


def classify(spec, maxsteps=3_000_000):
    out, step, ev = collect_milestones(spec, maxsteps)
    # choose the milestone key that GROWS (step-gaps increasing) with the most events
    best = None
    for key, lst in ev.items():
        if len(lst) < 16:
            continue
        steps = [e[0] for e in lst]
        widths = [e[1] for e in lst]
        gaps = [steps[i] - steps[i - 1] for i in range(1, len(steps))]
        if len(gaps) < 12:
            continue
        # growth score: is the tail-gap much bigger than the head-gap?
        h = sorted(gaps[:len(gaps) // 3]); t = sorted(gaps[2 * len(gaps) // 3:])
        gh = h[len(h) // 2] if h else 1; gt = t[len(t) // 2] if t else 1
        growth = gt / max(gh, 1)
        r_time, _, s_time = stable_ratio(gaps)
        r_wid, _, s_wid = stable_ratio(widths)
        cand = dict(key=(key[0], chr(ord('A') + key[1]), key[2]), n=len(lst),
                    growth=growth, r_time=r_time, s_time=s_time, r_wid=r_wid, s_wid=s_wid)
        score = growth * math.log(len(lst) + 1)
        if best is None or score > best[0]:
            best = (score, cand)
    if best is None:
        return dict(halt=(out == 'HALT'), out=out, key=None)
    c = best[1]; c['halt'] = (out == 'HALT'); c['out'] = out
    picks = []
    for r, s, src in [(c['r_time'], c['s_time'], 'time'),
                      (c['r_wid'], c['s_wid'], 'width')]:
        m = match_engine(r)
        if m is not None and s is not None and s < 0.05:
            picks.append((s, str(m[1]), src, r))
    picks.sort()
    c['engine'] = picks[0] if picks else None
    c['allpicks'] = picks
    return c


if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 3_000_000
    print(f"=== calibration on the 17 named cryptids (cap={cap}) ===")
    print(f"{'name':12} {'ms':>14} {'n':>5} {'grow':>6} {'r_time':>8} {'r_wid':>8}  engine")
    for name, sp in NAMED.items():
        c = classify(sp, cap)
        if c.get('key') is None:
            print(f"{name:12} (no growing milestone; out={c.get('out')})")
            continue
        rt = f"{c['r_time']:.3f}" if c['r_time'] else "  -  "
        rw = f"{c['r_wid']:.3f}" if c['r_wid'] else "  -  "
        eng = c['engine'][1] + f"({c['engine'][2]},{c['engine'][3]:.3f})" if c['engine'] else "-"
        print(f"{name:12} {str(c['key']):>14} {c['n']:>5} {c['growth']:>6.2f} {rt:>8} {rw:>8}  {eng}")
