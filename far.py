#!/usr/bin/env python
"""
FAR — Finite Automata Reduction (sound non-halting decider via a regular invariant).

Goal: prove a TM never halts by exhibiting a REGULAR set L of configurations with
  (1) start in L, (2) L closed under one TM step, (3) no halting config in L.
Then reachable(start) subset of L and L has no halt => never halts.  SOUND by direct verification
of (1)-(3) on the automaton (no extrapolation; this is the v3-proof discipline at the language level).

This file builds bottom-up, each layer validated against the trusted simulator before trust:
  LAYER 0 (this file, first): configuration-string encoding + single-step REWRITE, validated
           cell-for-cell against the trusted simulator (the G1 discipline).
Later layers (DFA ops, verifier, finder) are added only once LAYER 0 is proven faithful.

Config-string encoding (finite, blanks implicit):
  a config is the list of tape cells over the written window, with the STATE symbol inserted
  immediately BEFORE the head cell.  e.g.  0 1 (B) 1 0   means tape 0 1 1 0, head on cell index 2
  (the second 1), state B.  Symbols: '0','1' tape; 'A'..'F' state markers; head reads the cell
  right after the marker (a trailing blank '0' is appended if the marker is last).
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse

STATES = "ABCDEF"


def step_str(M, s):
    """one TM step on a config string (list of chars). returns (new_string, halted_bool).
    s has exactly one state char; head reads the char immediately after it (append '0' if last)."""
    i = next(k for k, ch in enumerate(s) if ch in STATES)
    q = s[i]
    # head cell is at i+1; append a blank if marker is at the end
    if i + 1 >= len(s):
        s = s + ["0"]
    r = int(s[i + 1])
    tr = M[q].get(r)
    if tr is None:
        return s, True                      # halt
    w, d, ns = tr
    out = list(s)
    out[i + 1] = str(w)                      # write head cell
    del out[i]                              # remove old marker; now w sits at index i
    if d == "R":
        out.insert(i + 1, ns)               # head moves right onto cell after w
    else:
        if i == 0:                          # head moves left off the written window -> fresh blank
            out.insert(0, "0")
            out.insert(0, ns)
        else:
            out.insert(i - 1, ns)           # head moves left onto the cell before w
    # ensure the head cell exists (append blank if marker landed at the right end)
    j = next(k for k, ch in enumerate(out) if ch in STATES)
    if j + 1 >= len(out):
        out.append("0")
    return out, False


def trim(s):
    """strip leading/trailing blank '0' that are not adjacent to the marker (blank-invariance)."""
    j = next(k for k, ch in enumerate(s) if ch in STATES)
    a, b = 0, len(s)
    while a < j and s[a] == "0" and a + 1 < j + 0:   # keep at least up to marker
        a += 1
    # only strip blanks strictly outside [marker, head]; keep marker and head cell
    # head cell index is j+1
    while b - 1 > j + 1 and s[b - 1] == "0":
        b -= 1
    while a < j and s[a] == "0":
        a += 1
    return s[a:b]


def validate(spec, steps=4000):
    """G1: run the string-rewrite and the trusted simulator in lockstep; compare full tape+head+state."""
    M = parse(spec)
    # trusted reference: explicit tape dict
    tape = {}; head = 0; state = "A"
    # string config: just the marker (blank tape)
    s = [state]
    for t in range(steps):
        # decode string -> (state, tape dict, head abs) for comparison
        if s[-1] in STATES:                 # marker last => implicit blank head cell
            s = s + ["0"]
        j = next(k for k, ch in enumerate(s) if ch in STATES)
        st_s = s[j]
        cells = [c for c in s if c not in STATES]
        head_idx = j                      # head cell is the (j)-th tape cell counting non-state chars before marker
        # number of tape chars before marker = j
        tdict = {k: int(c) for k, c in enumerate(cells) if c != "0"}
        # compare to reference (shift to align: both measured from left end of written window)
        rmin = min([head] + list(tape)) if tape else head
        rcells = [tape.get(p, 0) for p in range(rmin, max([head] + list(tape)) + 1)] if (tape or True) else [0]
        rhead = head - rmin
        # string side aligned to its own left
        s_state = st_s
        # build comparable (state, head-relative-content)
        def norm(state_, cells_, h_):
            cs = list(cells_)
            # strip outer blanks but keep head
            lo = 0
            while lo < h_ and lo < len(cs) and cs[lo] == 0:
                lo += 1
            hi = len(cs)
            while hi - 1 > h_ and cs[hi - 1] == 0:
                hi -= 1
            return state_, tuple(cs[lo:hi]), h_ - lo
        ref = norm(state, [tape.get(p, 0) for p in range(rmin, (max([head] + list(tape)) + 1))], head - rmin)
        sst = norm(st_s, [int(c) for c in cells], head_idx)
        if ref != sst:
            return False, t, ref, sst
        # advance reference
        r = tape.get(head, 0); tr = M[state].get(r)
        if tr is None:
            break
        w, d, ns = tr; tape[head] = w; state = ns; head += 1 if d == "R" else -1
        # advance string
        s, halted = step_str(M, s)
        s = trim(s)
        if halted:
            break
    return True, steps, None, None


def main():
    specs = ["1RB0LZ_1LC1RA_0RA0LC", "1RB1LC_0LA0RB_1LA0LZ",
             "1RB0LC_0LA0RA_1LA0LZ", "1RB1RB_1LC0RA_0RA1LB",  # a couple extra
             "1RB0LB_1LC0RC_1RA1LA"]
    for spec in specs:
        ok, t, ref, sst = validate(spec, 4000)
        print(f"{'OK ' if ok else 'FAIL'} {spec}  steps={t}" + ("" if ok else f"  ref={ref} str={sst}"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
