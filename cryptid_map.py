#!/usr/bin/env python
"""
Cryptid characteriser — extract the ITERATED MAP a machine computes, so the BB(6) frontier can be
mapped to the number-theoretic objects it encodes.

A cryptid (Antihydra, ...) is open because halting is equivalent to a Collatz-like statement about an
integer orbit. This tool does NOT prove anything; it reverse-engineers, from simulation, the orbit and
its update rule:
  - find a recurring milestone (head at a left/right extreme in a fixed state) = one "iteration";
  - read an integer parameter at each milestone (here: the tape's written width, and the binary value
    of the written region) -> an orbit v_0, v_1, v_2, ...;
  - classify the dynamics: linear (bouncer), geometric/doubling (counter), or PARITY-PIECEWISE-AFFINE
    (Collatz-like = cryptid) by fitting v_{i+1} as an affine function of v_i split on v_i mod m.
Output: the orbit + the inferred map. For a cryptid this exhibits the Collatz-like rule explicitly.
"""
from __future__ import annotations
import sys, os
from fractions import Fraction
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse


def milestones(spec, steps=2_000_000, side="L"):
    """orbit of (width, binval) at successive `side`-extreme turning points in a fixed state.
    A turning point: the head reaches a new extreme on `side` and the state is the one most common
    there (auto-detected). Returns list of (t, state, width, binval)."""
    M = parse(spec)
    tape = {}; head = 0; state = "A"; lo = hi = 0
    # pass 1: find the most common state at side-extremes
    from collections import Counter
    cnt = Counter()
    for t in range(min(steps, 300000)):
        r = tape.get(head, 0); tr = M[state].get(r)
        if tr is None:
            break
        atext = (head == lo) if side == "L" else (head == hi)
        if atext:
            cnt[state] += 1
        w, d, ns = tr; tape[head] = w; state = ns; head += 1 if d == "R" else -1
        if head < lo: lo = head
        if head > hi: hi = head
    if not cnt:
        return []
    target = cnt.most_common(1)[0][0]
    # pass 2: record (width, binval) each time we're at a side-extreme in `target`
    tape = {}; head = 0; state = "A"; lo = hi = 0
    out = []; lastext = None
    for t in range(steps):
        atext = (head == lo) if side == "L" else (head == hi)
        if atext and state == target and head != lastext:
            cells = [tape.get(j, 0) for j in range(lo, hi + 1)]
            width = hi - lo + 1
            binval = int("".join(map(str, cells)), 2) if any(cells) else 0
            out.append((t, state, width, binval))
            lastext = head
        r = tape.get(head, 0); tr = M[state].get(r)
        if tr is None:
            break
        w, d, ns = tr; tape[head] = w; state = ns; head += 1 if d == "R" else -1
        if head < lo: lo = head
        if head > hi: hi = head
    return out


def classify(seq):
    """seq = list of ints (an orbit). Return a short description of the dynamics."""
    v = [x for x in seq if x is not None]
    if len(v) < 4:
        return "too few milestones"
    diffs = [v[i + 1] - v[i] for i in range(len(v) - 1)]
    ratios = [v[i + 1] / v[i] for i in range(len(v) - 1) if v[i]]
    if len(set(diffs)) == 1:
        return f"LINEAR (bouncer): v -> v + {diffs[0]}"
    if all(d > 0 for d in diffs) and len(set(diffs)) <= 3 and max(diffs) - min(diffs) <= 2:
        return f"~LINEAR (bouncer): step in {sorted(set(diffs))}"
    # geometric?
    if ratios and max(ratios) - min(ratios) < 0.15 and sum(ratios) / len(ratios) > 1.5:
        return f"GEOMETRIC (counter): ratio ~ {sum(ratios)/len(ratios):.3f}"
    # parity-piecewise-affine (Collatz-like): fit v_{i+1}=a*v_i+b per residue class mod m
    for m in (2, 3):
        classes = {}
        ok = True
        for i in range(len(v) - 1):
            cls = v[i] % m
            classes.setdefault(cls, []).append((v[i], v[i + 1]))
        fits = {}
        for cls, pts in classes.items():
            if len(pts) < 2:
                ok = False; break
            (x0, y0), (x1, y1) = pts[0], pts[1]
            if x1 == x0:
                ok = False; break
            a = Fraction(y1 - y0, x1 - x0); b = Fraction(y0) - a * x0
            if all(Fraction(y) == a * x + b for x, y in pts):
                fits[cls] = (a, b)
            else:
                ok = False; break
        if ok and fits:
            rule = "; ".join(f"v%{m}={c}: v->{a}*v+{b}" for c, (a, b) in sorted(fits.items()))
            distinct = len(set(fits.values()))
            if len(fits) >= 2 and distinct >= 2:
                return f"COLLATZ-LIKE (cryptid) mod {m}: {rule}"     # genuinely parity-dependent rule
            return f"AFFINE (counter): v->{next(iter(fits.values()))[0]}*v+{next(iter(fits.values()))[1]}"
    return "IRREGULAR / unrecognised (candidate cryptid; orbit shown)"


def characterise(spec, steps=2_000_000):
    best = None
    for side in ("L", "R"):
        ms = milestones(spec, steps, side)
        if len(ms) >= 4:
            widths = [w for _, _, w, _ in ms]
            bins = [b for _, _, _, b in ms]
            cw = classify(widths); cb = classify(bins)
            # prefer the side/metric that gives a recognised structure
            score = sum("LIKE" in c or "LINEAR" in c or "GEOMETRIC" in c for c in (cw, cb))
            cand = (score, side, ms, cw, cb)
            if best is None or cand[0] > best[0]:
                best = cand
    if best is None:
        return None
    _, side, ms, cw, cb = best
    return {"side": side, "n_milestones": len(ms),
            "widths": [w for _, _, w, _ in ms][:14], "width_dynamics": cw,
            "binvals": [b for _, _, _, b in ms][:10], "binval_dynamics": cb}


def main():
    cases = [
        ("Antihydra (cryptid)", "1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA"),
        ("our counter",         "1RB1LC_0LA0RB_1LA0LZ"),
        ("our bouncer",         "1RB0LC_0LA0RA_1LA0LZ"),
        ("Lucy (cryptid,halts)","1RB0RD_0RC1RE_1RD0LA_1LE1LC_1RF0LD_---0RA"),
    ]
    for name, spec in cases:
        print("=" * 70); print(name, spec)
        r = characterise(spec)
        if r is None:
            print("  no milestone structure found"); continue
        print(f"  side={r['side']}  milestones={r['n_milestones']}")
        print(f"  widths : {r['widths']}")
        print(f"    -> {r['width_dynamics']}")
        print(f"  binvals: {r['binvals']}")
        print(f"    -> {r['binval_dynamics']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
