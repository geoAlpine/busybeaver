#!/usr/bin/env python
"""
BB(6) novelty oracle — is a machine STILL in the community's undecided/holdout set?

This is the piece we lacked: when a sound decider returns NEVER_HALTS on a 6-state machine, we must
know whether the community has already decided it (then it is a re-decision, not a contribution) or
it is still open (then a SOUND proof would be a genuine contribution — to be scrutinised, never
auto-claimed). For 6 states the "undecided set" IS the holdout list (bbchallenge wiki).

Matching is up to machine ISOMORPHISM, the same way the holdout list is deduplicated:
  - TNF (Tree Normal Form): relabel states by order of first appearance in a 0-before-1 BFS from A,
    so the names are canonical; halts normalised to '---' (the halt action is irrelevant);
  - left-right reversal: flipping every move L<->R gives the mirror machine (halts iff the original
    does). canonical(M) = min(TNF(M), TNF(reverse(M))).
A machine is a "current holdout" iff its canonical form is in the canonicalised holdout set.

Data: _bbdata/bb6_holdouts_1104.txt (April 2026, up to equivalence, from the wiki). Newer/larger
lists exist (17.8M raw, May 2026); this 1104 is the curated still-open residual.
"""
from __future__ import annotations
import os

HERE = os.path.dirname(__file__)
HOLDOUT_FILE = os.path.join(HERE, "_bbdata", "bb6_holdouts_1104.txt")
SC = "ABCDEF"


def parse(spec):
    """spec '1RB1LA_..._0RC---' -> dict state -> [t0, t1], t=(w,d,ns) or None (halt)."""
    blocks = spec.split("_")
    M = {}
    for i, blk in enumerate(blocks):
        st = SC[i]; trs = []
        for k in (0, 3):
            tok = blk[k:k + 3]
            if tok[0] in "-Z" or tok[2] in "-Z" or tok == "---":
                trs.append(None)
            else:
                trs.append((int(tok[0]), tok[1], tok[2]))
        M[st] = trs
    return M


def emit(M, order):
    """emit spec from M with states in `order` (already the canonical labels A,B,...)."""
    relabel = {old: SC[i] for i, old in enumerate(order)}
    out = []
    for old in order:
        blk = ""
        for t in M[old]:
            if t is None:
                blk += "---"
            else:
                blk += f"{t[0]}{t[1]}{relabel[t[2]]}"
        out.append(blk)
    return "_".join(out)


def tnf(M):
    """Tree Normal Form: BFS from A in 0-then-1 order, relabel by first-appearance. halts -> '---'."""
    order = ["A"]; seen = {"A"}
    i = 0
    while i < len(order):
        s = order[i]; i += 1
        for sym in (0, 1):
            t = M[s][sym]
            if t is None:
                continue
            ns = t[2]
            if ns in M and ns not in seen:
                seen.add(ns); order.append(ns)
    # unreachable states (shouldn't appear in TNF inputs) -> append in label order for totality
    for s in SC:
        if s in M and s not in seen:
            seen.add(s); order.append(s)
    return emit(M, order)


def reverse(M):
    """mirror machine: flip every move direction L<->R (tape reversed). Equivalent halting behaviour."""
    flip = {"L": "R", "R": "L"}
    R = {}
    for s, trs in M.items():
        R[s] = [None if t is None else (t[0], flip[t[1]], t[2]) for t in trs]
    return R


def canonical(spec):
    M = parse(spec)
    return min(tnf(M), tnf(reverse(M)))


def load_holdout_canon(path=HOLDOUT_FILE):
    specs = [l.strip() for l in open(path) if l.strip()]
    return {canonical(s) for s in specs}, len(specs)


_CANON = None


def is_holdout(spec):
    """True iff `spec` is (up to isomorphism) in the current BB(6) holdout set = still undecided."""
    global _CANON
    if _CANON is None:
        _CANON, _ = load_holdout_canon()
    return canonical(spec) in _CANON


def main():
    canon, n = load_holdout_canon()
    print(f"loaded {n} holdout reps -> {len(canon)} distinct up to TNF+reversal")
    # sanity: every list entry is a holdout; the machine from INCIDENT 2 is a holdout; cryptids are
    tests = [
        ("INCIDENT-2 machine", "1RB1LA_0LC0RE_1LD1LB_1RE1LF_1RC0RA_0RC---"),
        ("Antihydra",          "1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA"),
        ("a clearly-decided cycler", "1RB---_0RC---_0RD---_0RE---_0LD---"),
    ]
    for name, s in tests:
        print(f"  is_holdout({name}) = {is_holdout(s)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
