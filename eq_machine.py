#!/usr/bin/env python
"""
(brick a) Witness machine EQ for SLIN ⊋ REG (non-halting certification), conjecture-free.

EQ semi-decides equal blocks: its reachable configs are L^n C R^n (n unbounded), and EVERY unequal
block L^n C R^m (n != m) reaches the halt. Then:
  - any REGULAR certificate L' ⊇ reachable contains L^n C R^n for unbounded n; by the pumping lemma a
    regular L' must then contain some L^n C R^m with n != m (pump one arm) -> a halt-reaching config
    -> L' not halt-free. So NO regular certificate exists.
  - the SEMILINEAR set { #L = #R } is a certificate.
=> SLIN ⊋ REG for non-halting certification, with NO open conjecture.

Alphabet (ints): 0=blank, 1=L, 2=C(center), 3=R, 4=xL(crossed L), 5=xR(crossed R).
Cycle from the milestone (head at C, state CMP): cross-off one L and one R per round; if both arms
empty together -> EQUAL -> uncross and grow both arms by one (-> n+1); if one empties first -> HALT.
This file CONSTRUCTS the transition table and VERIFIES (i) it reaches L^n C R^n for n=0..K from blank
without halting, and (ii) it halts from every unequal block L^a C R^b (a,b <= K, a != b).
"""
from __future__ import annotations

B, L, C, R, XL, XR = 0, 1, 2, 3, 4, 5
HALT = None

# transition table: D[state][symbol] = (write, move, next) or None (halt). move: +1 right, -1 left.
D = {
    # init from blank: write C, then step right onto blank and bounce back to C as CMP (n=0)
    "S":  {B: (C, +1, "S1")},
    "S1": {B: (B, -1, "CMP")},

    # CMP: at C, start a compare round -> go right to find an uncrossed R
    "CMP": {C: (C, +1, "FR")},
    # FR: move right over crossed R looking for an R; blank => right arm has no more R this round
    "FR": {XR: (XR, +1, "FR"), R: (XR, -1, "FL"), B: (B, -1, "CKL")},
    # FL: we crossed an R; go left over xR, C, xL to find a matching uncrossed L
    "FL": {XR: (XR, -1, "FL"), C: (C, -1, "FL"), XL: (XL, -1, "FL"),
           L: (XL, +1, "FR2"), B: (B, +1, "HALTL")},   # L arm empty but R had one -> R>L -> halt
    # FR2: matched a pair; return right to C to start next round (skip xL, then at C go to CMP-ish)
    "FR2": {XL: (XL, +1, "FR2"), C: (C, +1, "FR"), XR: (XR, +1, "FR")},
    # CKL: right arm exhausted this round; check the left arm is also exhausted (all xL)
    "CKL": {XR: (XR, -1, "CKL"), C: (C, -1, "CKL"), XL: (XL, -1, "CKL"),
            L: (XL, +1, "HALTR"),     # left still has an uncrossed L -> L>R -> halt
            B: (B, +1, "UC")},        # both arms fully crossed -> EQUAL -> uncross+grow
    # HALTL / HALTR: reached an inequality -> halt (undefined transitions = halt)
    "HALTL": {B: HALT, L: HALT, C: HALT, R: HALT, XL: HALT, XR: HALT},
    "HALTR": {B: HALT, L: HALT, C: HALT, R: HALT, XL: HALT, XR: HALT},
    # UC: from the far-left blank, sweep RIGHT turning xL->L, xR->R; at the right blank, extend: write
    # an R there (R^(n+1)), then travel left and write an L at the far-left blank (L^(n+1)).
    "UC": {XL: (L, +1, "UC"), C: (C, +1, "UC"), XR: (R, +1, "UC"), B: (R, -1, "GL")},
    "GL": {R: (R, -1, "GL"), C: (C, -1, "GL"), L: (L, -1, "GL"), B: (L, +1, "TOC")},
    # TOC: go right back to C and resume compare (now L^(n+1) C R^(n+1))
    "TOC": {L: (L, +1, "TOC"), C: (C, +1, "CMP0")},
    "CMP0": {R: (R, -1, "CMP")},   # step to land head on C in state CMP
}


def run(cells, head, state, cap=200000):
    """simulate; return ('HALT', t) or ('CAP', config) or ('STUCK', ...). cells: dict pos->sym."""
    tape = dict(cells)
    for t in range(cap):
        s = tape.get(head, B)
        row = D.get(state)
        if row is None or s not in row:
            return ("STUCK", t, state, s)
        tr = row[s]
        if tr is None:
            return ("HALT", t)
        w, mv, ns = tr
        tape[head] = w; head += mv; state = ns
    return ("CAP", tape, head, state)


def milestone_config(n):
    """L^n C R^n, head on C, state CMP."""
    cells = {}
    for i in range(n):
        cells[i] = L
    cells[n] = C
    for i in range(n):
        cells[n + 1 + i] = R
    return cells, n, "CMP"


def reaches_milestones(K=8):
    """(i) from blank, does EQ pass through L^n C R^n (head at C, CMP) for n=0..K, never halting?"""
    tape = {}; head = 0; state = "S"
    seen = set()
    targets = {tuple(sorted(milestone_config(n)[0].items())): n for n in range(K + 1)}
    # also need head/state match -> track when (state==CMP and head on C)
    for t in range(2_000_000):
        if state == "CMP" and tape.get(head, B) == C:
            # canonical milestone: strip blanks
            keys = [k for k, v in tape.items() if v]
            if keys:
                lo, hi = min(keys), max(keys)
                cfg = tuple((i - lo, tape.get(i, B)) for i in range(lo, hi + 1))
                # identify n: count L's
                n = sum(1 for _, v in cfg if v == L)
                if cfg == tuple((i, v) for i, (j, v) in enumerate(
                        sorted(milestone_config(n)[0].items()))):
                    seen.add(n)
        s = tape.get(head, B); row = D.get(state)
        if row is None or s not in row:
            return ("STUCK at", t, state, s, "seen", sorted(seen))
        tr = row[s]
        if tr is None:
            return ("HALTED at", t, "seen", sorted(seen))
        w, mv, ns = tr; tape[head] = w; head += mv; state = ns
        if len(seen) >= K + 1:
            return ("OK reaches n=0..%d" % K, sorted(seen))
    return ("timeout", "seen", sorted(seen))


def unequal_all_halt(K=7):
    """(ii) from every L^a C R^b with a!=b (0<=a,b<=K), does EQ reach HALT?"""
    bad = []
    for a in range(K + 1):
        for b in range(K + 1):
            if a == b:
                continue
            cells = {}
            for i in range(a):
                cells[i] = L
            cells[a] = C
            for i in range(b):
                cells[a + 1 + i] = R
            res = run(cells, a, "CMP")          # head on C, state CMP
            if res[0] != "HALT":
                bad.append((a, b, res[0]))
    return bad


def main():
    print("(i) reaches equal-block milestones from blank:")
    print("   ", reaches_milestones(8))
    print("(ii) every unequal block halts:")
    bad = unequal_all_halt(7)
    print("   ", "ALL UNEQUAL BLOCKS HALT (a,b<=7)" if not bad else f"FAIL: {bad[:8]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
