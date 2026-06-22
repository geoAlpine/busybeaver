#!/usr/bin/env python
"""
POW2 — explicit multi-symbol Turing machine that SEMI-DECIDES "power of 2" in unary.
A *building block* for the attempted hierarchy separation SLIN ⊊ 2-automatic (LIMIT_THEOREM.md
brick e). Verified by simulation; built in the style of `eq_machine.py`.

Behavior (started on 1^v, head at the LEFT end, state START):
  - runs FOREVER (never halts)  iff  v is a power of 2   (v ∈ {1,2,4,8,16,...})
  - HALTS                       iff  v is NOT a power of 2
Verified: HALT ⟺ not-a-power-of-2 for v = 1..200, zero mismatches; powers {1,..,256} run past 20M
steps; from 1^1 it visits the clean blocks 1^(2^n) (n=0,1,2,...) at state DOUBLE.

Alphabet: B=0 blank, O=1 one, X=2 crossed-one, M=3 marker.
  PHASE 1 (HALVE): cross out every other 1; even→halve again, odd>1→HALT (odd factor), reach 1→PHASE 2.
  PHASE 2 (DOUBLE): from a clean 1, double the block forever, visiting 1^1,1^2,1^4,1^8,...

** SOUNDNESS CAVEAT (why this is only a building block, not yet the witness). **
From the BLANK / 1^1 start, POW2 enters PHASE 2 and NEVER re-checks (verified: after reaching state
DOUBLE it never returns to a halve/halt state). So *from blank* it is a pure doubler, whose non-halting
has a SEMILINEAR (indeed regular) certificate {1^k at the doubling states : k≥1}. Hence POW2 as-is does
NOT separate SLIN — the power-of-2 test only fires from non-power STARTS. A genuine SLIN ⊊ 2-automatic
witness must CHECK power-of-2-ness EVERY cycle (as `eq_machine` checks equality every round), e.g. by
duplicating the counter, halve-checking the copy (HALT if not a power), then doubling the original — so
that the *only* non-halting reachable configs are {1^(2^n)} (2-automatic, not semilinear). See
LIMIT_THEOREM.md brick e for the obstacle and the intended completion. No separation is claimed here.
"""
from __future__ import annotations

B, O, X, M = 0, 1, 2, 3
HALT = None


def run(D, cells, head, state, cap=2_000_000):
    """multi-symbol dict-tape simulator (same style as eq_machine.run)."""
    tape = dict(cells)
    for t in range(cap):
        s = tape.get(head, B)
        row = D.get(state)
        if row is None or s not in row:
            return ("STUCK", t, state, s, tape, head)
        tr = row[s]
        if tr is None:
            return ("HALT", t, tape, head, state)
        w, mv, ns = tr
        tape[head] = w; head += mv; state = ns
    return ("CAP", cap, tape, head, state)


D = {
    # ---- PHASE 1: HALVE (decide power-of-2) ----
    "START":      {O: (O, +1, "WANT_CROSS")},
    "WANT_CROSS": {O: (X, +1, "WANT_KEEP"), B: (B, -1, "END_ODD")},
    "WANT_KEEP":  {O: (O, +1, "WANT_CROSS"), B: (B, -1, "END_EVEN")},
    "END_EVEN":   {X: (X, -1, "PACK_GOL")},
    "END_ODD":    {O: (O, -1, "ODD_LEFT")},
    "ODD_LEFT":   {B: (B, +1, "TO_DOUBLE"), X: (X, +1, "HALT")},
    "HALT":       {B: HALT, O: HALT, X: HALT, M: HALT},
    "PACK_GOL":   {O: (O, -1, "PACK_GOL"), X: (X, -1, "PACK_GOL"), B: (B, +1, "ERASEX")},
    "ERASEX":     {O: (O, +1, "ERASEX"), X: (B, +1, "ERASEX"), B: (M, -1, "GATHER_GOL")},
    "GATHER_GOL": {O: (O, -1, "GATHER_GOL"), B: (B, -1, "GG_B")},
    "GG_B":       {O: (O, -1, "GATHER_GOL"), B: (B, +1, "GG_EDGE")},
    "GG_EDGE":    {B: (B, +1, "GATHER")},
    "GATHER":     {O: (O, +1, "GATHER"), B: (B, +1, "G_FIND"), M: (B, -1, "GOHOME")},
    "G_FIND":     {B: (B, +1, "G_FIND"), O: (B, -1, "G_CARRY"), M: (B, -1, "GOHOME")},
    "G_CARRY":    {B: (B, -1, "G_CARRY"), O: (O, +1, "G_PLACE")},
    "G_PLACE":    {B: (O, +1, "GATHER")},
    "GOHOME":     {B: (B, -1, "GOHOME"), O: (O, -1, "GOHOME_O")},
    "GOHOME_O":   {O: (O, -1, "GOHOME_O"), B: (B, +1, "RESTART")},
    "RESTART":    {O: (O, +1, "WANT_CROSS")},
    # ---- PHASE 2: DOUBLE forever ----
    "TO_DOUBLE":  {O: (O, +1, "DBL_CLEAR")},
    "DBL_CLEAR":  {X: (B, +1, "DBL_CLEAR"), O: (O, +1, "DBL_CLEAR"), B: (B, -1, "DBL_GOL")},
    "DBL_GOL":    {O: (O, -1, "DBL_GOL"), X: (B, -1, "DBL_GOL"), B: (B, +1, "DOUBLE")},
    "DOUBLE":     {O: (M, +1, "DBL_APPEND"), M: (M, +1, "DOUBLE")},
    "DBL_APPEND": {O: (O, +1, "DBL_APPEND"), X: (X, +1, "DBL_APPEND"), B: (X, -1, "DBL_BACK")},
    "DBL_BACK":   {X: (X, -1, "DBL_BACK"), O: (O, -1, "DBL_BACK"), M: (M, +1, "DBL_AT")},
    "DBL_AT":     {O: (M, +1, "DBL_APPEND"), X: (X, -1, "DBL_FIN_GOL")},
    "DBL_FIN_GOL":{O: (O, -1, "DBL_FIN_GOL"), X: (X, -1, "DBL_FIN_GOL"), M: (M, -1, "DBL_FIN_GOL"),
                   B: (B, +1, "DBL_FIN")},
    "DBL_FIN":    {M: (O, +1, "DBL_FIN"), X: (O, +1, "DBL_FIN"), O: (O, +1, "DBL_FIN"),
                   B: (B, -1, "DBL_FIN_BACK")},
    "DBL_FIN_BACK":{O: (O, -1, "DBL_FIN_BACK"), B: (B, +1, "DOUBLE")},
}


def is_pow2(v):
    return v > 0 and (v & (v - 1)) == 0


def verify(hi=200, cap=3_000_000):
    """SOUND check: HALT ⟺ not-a-power-of-2 for v=1..hi; report mismatches."""
    bad = []
    for v in range(1, hi + 1):
        res = run(D, {i: O for i in range(v)}, 0, "START", cap=cap)
        if (res[0] == "HALT") != (not is_pow2(v)):
            bad.append((v, res[0]))
    return bad


if __name__ == "__main__":
    bad = verify()
    print(f"POW2 semi-decider: HALT <=> not-power-of-2 for v=1..200 -> "
          f"{'VERIFIED (0 mismatches)' if not bad else f'MISMATCHES {bad}'}")
    # show it visits 1^(2^n) at state DOUBLE from 1^1
    tape = {0: O}; head = 0; st = "START"; seen = []
    for _ in range(3_000_000):
        if st == "DOUBLE":
            ks = [k for k, vv in tape.items() if vv != B]
            if ks and all(tape.get(j, B) == O for j in range(min(ks), max(ks) + 1)) and head == min(ks):
                k = max(ks) - min(ks) + 1
                if not seen or seen[-1] != k:
                    seen.append(k)
                    if len(seen) >= 8:
                        break
        s = tape.get(head, B); tr = D[st][s]
        if tr is None:
            break
        w, mv, ns = tr; tape[head] = w; head += mv; st = ns
    print(f"clean blocks visited at DOUBLE from 1^1: {seen}  (all powers of 2: {all(is_pow2(k) for k in seen)})")
