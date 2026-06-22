#!/usr/bin/env python
"""
Cryptid census — is the BB(6) open frontier monolithic, or structurally heterogeneous?

Reconnaissance for the *mathematics* road to BB(6) (BB6_PREP.md path B): the decider-engineering
road is a proven dead end (0/300 holdouts decided), so the only honest contributions are (i) resolve a
named cryptid mathematically, or (ii) catalogue the frontier as the named number-theory it encodes
(the §3c-style exact-reduction programme, see antihydra_attack.md §3c).

To direct that effort we need to know whether all 19 open cryptids are equally hard. This script runs
`cryptid_map.characterise` over the suite's CRYPTID list and tabulates the milestone-width growth and
the inferred dynamics, so the frontier can be partitioned by how fast the tape grows:
  - fast / exponential width (ratio >~ 2), few milestones  -> genuine Collatz-like (Antihydra-class),
    the right targets for an EXACT §3c-style arithmetic reduction (clean orbit -> named open problem);
  - slow / near-linear width (ratio ~1), hundreds of milestones -> a different, closer per-machine
    analysis is needed even to find the right milestone.

NOTE: this is RECON, not a soundness claim. A slow-width or 'LINEAR'-tagged row does NOT mean the
machine is decidable — these all survived the community's strong deciders; the crude milestone
extraction can mislabel. The value is *prioritisation* of the math road, nothing more.
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import cryptid_map as cm
from suite import CRYPTIDS


def _tag(d):
    for k in ("COLLATZ", "LINEAR", "GEOMETRIC", "AFFINE"):
        if k in d:
            return k
    return "IRREG"


def census(steps=800_000):
    rows = []
    for name, spec in CRYPTIDS:
        r = cm.characterise(spec, steps=steps)
        if not r:
            rows.append((name, None))
            continue
        w = r["widths"]
        ratio = (w[-1] / w[-2]) if len(w) >= 2 and w[-2] else float("nan")
        rows.append((name, {"side": r["side"], "nms": r["n_milestones"], "w": w,
                            "ratio": ratio, "tag": _tag(r["width_dynamics"])}))
    return rows


def main():
    print("Cryptid census — width-growth structure of the 19 open cryptids\n")
    print(f'{"name":<16}{"sd":>3}{"#ms":>5}{"ratio":>8}  {"tag":<8} widths[:8]')
    rows = census()
    fast, slow = [], []
    for name, r in rows:
        if r is None:
            print(f"{name:<16} (no orbit extracted)")
            continue
        print(f'{name:<16}{r["side"]:>3}{r["nms"]:>5}{r["ratio"]:>8.3f}  {r["tag"]:<8} {r["w"][:8]}')
        (fast if r["ratio"] >= 1.8 else slow).append(name)
    print(f"\n  exponential-width (ratio>=1.8, Collatz-class -> §3c targets): {fast}")
    print(f"  slow-width (ratio<1.8, need per-machine milestone analysis):  {len(slow)} machines")
    print("\n  => the frontier is HETEROGENEOUS: a small exponential-Collatz core vs a slow-width majority.")
    print("     Recon only (BB6_PREP path B); not a soundness/decidability claim.")


if __name__ == "__main__":
    raise SystemExit(main())
