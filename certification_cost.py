#!/usr/bin/env python
"""
Certification cost K* — the BB avatar of the cross-resource cost bound.

Unifies with the quantum cross-platform decay (2/(n-1))^K and the SETI codimension P_FP~(ε/B)^(Kν-d):
to certify a machine's behaviour against an answer-blind adversary you must PIN DOWN its update map,
and the cost is the number of independent observations (milestones) needed to do so.

For a machine, `cryptid_map.milestones` gives the orbit v_0,v_1,... (the integer it iterates). We fit
the SIMPLEST model in a hierarchy and report:
  K* = least K such that the model fitted on the first K milestones predicts EVERY later observed
       milestone (so K observations already exclude any other model of that class = certified);
  d  = the model's parameter dimension (the adversary's "degrees of freedom", the SETI d).
A model that needs K*=K means: K-1 observations are spoofable (an adversary fits a different map), K
are not. Cryptids: NO finite-parameter model in the hierarchy predicts the orbit -> K* = inf, d = inf
-> no finite certificate -> the ceiling = BB(6) frontier. This is the cost bound, computed per machine.

Models (the SETI 'd', the BB certificate class):
  affine            v -> a v + b                     d=2  (counter / geometric)
  parity-affine     v -> a_p v + b_p  (p = v mod 2)  d=4  (Collatz-like, FINITE rule)
  parity3-affine    p = v mod 3                       d=6
"""
from __future__ import annotations
import sys, os
from fractions import Fraction
sys.path.insert(0, os.path.dirname(__file__))
from cryptid_map import milestones


def fit_affine(pairs):
    """fit v'=a v + b exactly (Fraction). pairs=[(v,v'),...]. return (a,b) or None if inconsistent."""
    if len(pairs) < 2:
        return None
    (x0, y0), (x1, y1) = pairs[0], pairs[1]
    if x1 == x0:
        return None
    a = Fraction(y1 - y0, x1 - x0); b = Fraction(y0) - a * x0
    if all(Fraction(y) == a * x + b for x, y in pairs):
        return (a, b)
    return None


def fit_model(orbit, m=1):
    """fit a parity(mod m)-piecewise affine model on the whole orbit. return dict cls->(a,b) or None."""
    classes = {}
    for i in range(len(orbit) - 1):
        classes.setdefault(orbit[i] % m, []).append((orbit[i], orbit[i + 1]))
    fits = {}
    for c, pts in classes.items():
        f = fit_affine(pts)
        if f is None:
            return None
        fits[c] = f
    return fits


def predicts(orbit, m, fits):
    """does the mod-m piecewise-affine `fits` correctly predict every step of orbit?"""
    for i in range(len(orbit) - 1):
        c = orbit[i] % m
        if c not in fits:
            return False
        a, b = fits[c]
        if Fraction(orbit[i + 1]) != a * orbit[i] + b:
            return False
    return True


MODELS = [("affine", 1, 2), ("parity-affine", 2, 4), ("parity3-affine", 3, 6)]


def _orbit(spec, steps, side):
    ms = milestones(spec, steps, side)
    raw = [b for _, _, _, b in ms]
    orb = [raw[0]] if raw else []
    for v in raw[1:]:
        if v != orb[-1]:
            orb.append(v)
    return orb


def cost(spec, steps=3_000_000):
    orb = max((_orbit(spec, steps, s) for s in ("L", "R")), key=len)  # richer side
    if len(orb) < 4:
        return {"spec": spec, "milestones": len(orb), "note": "too few", "model": "?",
                "d": "?", "Kstar": "?"}
    for name, m, d in MODELS:
        # K* = least K such that fitting on the first K predicts the WHOLE observed orbit
        for K in range(2, len(orb)):
            fits = fit_model(orb[:K + 1], m)            # first K transitions
            if fits and predicts(orb, m, fits):
                return {"spec": spec, "model": name, "d": d, "Kstar": K,
                        "rule": {c: (str(a), str(b)) for c, (a, b) in fits.items()},
                        "milestones": len(orb)}
    return {"spec": spec, "model": "NONE (non-parametric)", "d": "inf", "Kstar": "inf",
            "milestones": len(orb), "note": "no finite-parameter map fits -> cryptid ceiling"}


def main():
    cases = [
        ("our counter",          "1RB1LC_0LA0RB_1LA0LZ"),
        ("our bouncer",          "1RB0LC_0LA0RA_1LA0LZ"),
        ("parity counter",       "1RB0LZ_1LC1RA_0RA0LC"),
        ("Antihydra (cryptid)",  "1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA"),
        ("Lucy (cryptid)",       "1RB0RD_0RC1RE_1RD0LA_1LE1LC_1RF0LD_---0RA"),
    ]
    print("Certification cost K* (observations to pin the update map) and adversary d.o.f. d:")
    for name, spec in cases:
        r = cost(spec)
        print(f"  {name:<22} model={r.get('model','?'):<22} d={str(r.get('d','?')):<4} "
              f"K*={str(r.get('Kstar','?')):<4} (orbit {r.get('milestones','?')})")
    print()
    print("K*=inf <=> no finite-parameter certificate <=> the cryptid ceiling (BB(6) frontier).")
    print("Avatar of: quantum (2/(n-1))^K cross-platform ; SETI P_FP~(eps/B)^(K*nu - d).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
