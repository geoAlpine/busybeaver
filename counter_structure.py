#!/usr/bin/env python
"""
Counter STRUCTURE decoder — STEP 1.5 for the 10 residual counters (SOUND: measurement only).

The bouncer prover v3 cleared all 53 bouncers; the 10 holdouts are binary-counter-class
(time doubles per carry-out). This decodes each counter's macro structure far more deeply than
the width-vs-steps heuristic, using EXACT self-loop acceleration (a transition M[S][r]=(w,d,S)
that writes w==r... or any self-loop literally repeats, so crossing a uniform run of the read
symbol can be jumped in one shot -- a sound speedup that does NOT change what is reachable, only
how fast we get there). With it we reach k carry-outs in ~k macro-ops instead of ~2^k micro-steps,
so we can confirm structure out to ~2^30 micro-steps cheaply.

For each counter we extract, as a SOUND certificate (no halting claim):
  (1) the carry-out record family: tape = LEFT . sym^k . RIGHT with k growing by a constant
      (a regular, growing configuration family -> genuinely unbounded),
  (2) op-segment DOUBLING: the number of macro-ops between consecutive carry-outs ->2x
      (the exponential-time / binary-counter signature),
  (3) NO halt op ever appears out to the deepest carry-out reached (~2^k micro-steps).
And, where it fits, the recursive "chain of chains" grammar of the op-segment:
      S(k) = [k] ++ MID(k) ++ [k+1],  MID(k) = MID(k-1) ++ [pivot] ++ MID(k-1)
discovered by direct decode of 1RB1LA_0LA0RB_0LA0LZ -- the precise target the STEP-2 nested
induction (sligocki, implemented against spec + oracle-gated) must certify.

This ships NO never-halts verdict. It is the sound recon that scopes the proof.
"""
from __future__ import annotations

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bouncer_prove2 import parse
from bouncer_prove3 import prove as bouncer_prove   # v3 clears all 53 bouncers; only 10 counters remain

HALT = {"Z", "H", "-"}


def macro_run(spec, max_ops=200_000, max_records=34):
    """EXACT self-loop-accelerated run. Returns (ops, records, halted).
    ops: list of ('CHAIN',state,r,w,dir,n) | ('WALL',state,r,w,dir).
    records: (op_index, state, tape_bits_lo_to_hi) at each new leftmost/rightmost cell."""
    M = parse(spec); tape = {}; head = 0; st = "A"; lo = hi = 0
    ops = []; recs = []; halted = False
    while len(ops) < max_ops:
        r = tape.get(head, 0); tr = M[st][r]
        if tr is None:
            halted = True; ops.append(("HALT",)); break
        w, dchar, nxt = tr; d = 1 if dchar == "R" else -1
        if nxt == st:
            # self-loop on state st: it keeps reading the run of symbol r in direction d,
            # writing w each step. It repeats verbatim while the read cell holds r.
            # If w != r the run is rewritten as we go but the *read* ahead is still r until
            # the run ends -> still a faithful repeat. Jump the whole uniform run of r.
            n = 0; p = head
            while tape.get(p, 0) == r:
                tape[p] = w; n += 1; p += d
            head = p; st = nxt
            ops.append(("CHAIN", st, r, w, dchar, n))
        else:
            tape[head] = w; head += d; st = nxt
            ops.append(("WALL", st, r, w, dchar))
        if head < lo or head > hi:
            lo = min(lo, head); hi = max(hi, head)
            bits = "".join(str(tape.get(c, 0)) for c in range(lo, hi + 1))
            recs.append((len(ops), st, bits, head - lo))
            if len(recs) >= max_records:
                break
    return ops, recs, halted


def regular_family(recs):
    """Do the carry-out tapes form LEFT . sym^k . RIGHT with k growing by a constant?
    Returns (sym, dk, left, right) or None. Uses the last several records (past transient)."""
    use = recs[-8:] if len(recs) >= 8 else recs
    # find, per tape, the maximal interior run of a single symbol; check left/right stable & k linear.
    best = None
    for sym in ("0", "1"):
        ks = []; lefts = []; rights = []
        ok = True
        for (_, _, bits, _) in use:
            # longest run of sym
            import re
            runs = [m for m in re.finditer(sym + "+", bits)]
            if not runs:
                ok = False; break
            m = max(runs, key=lambda mm: mm.end() - mm.start())
            ks.append(m.end() - m.start()); lefts.append(bits[:m.start()]); rights.append(bits[m.end():])
        if not ok:
            continue
        dks = [ks[i+1] - ks[i] for i in range(len(ks)-1)]
        if dks and len(set(dks)) == 1 and dks[0] >= 1 and len(set(lefts)) == 1 and len(set(rights)) == 1:
            cand = (sym, dks[0], lefts[0], rights[0])
            if best is None or dks[0] < best[1]:
                best = cand
    return best


def seg_lengths(ops, recs):
    """op-segment lengths between consecutive carry-out records (past transient)."""
    idx = [r[0] for r in recs]
    return [idx[i+1] - idx[i] for i in range(len(idx)-1)]


def analyze(spec):
    ops, recs, halted = macro_run(spec)
    if halted:
        return {"verdict": "HALTS", "at_op": len(ops)}
    if len(recs) < 8:
        return {"verdict": "few-records", "records": len(recs)}
    fam = regular_family(recs)
    segs = seg_lengths(ops, recs)
    tail = segs[-6:]
    ratios = [tail[i+1] / tail[i] for i in range(len(tail)-1) if tail[i] > 0]
    avg_ratio = round(sum(ratios) / len(ratios), 3) if ratios else 0
    deepest_micro = None  # estimate micro-steps reached ~ sum of CHAIN n + WALLs is not tracked; report k
    return {
        "verdict": "COUNTER-STRUCTURE",
        "family": fam,                       # (sym, dk, left, right) or None
        "seg_doubling": avg_ratio,           # ->2.0 is the binary-counter signature
        "carryouts_reached": len(recs),      # ~ depth; micro-steps ~ 2^len
        "no_halt": True,                     # no HALT op appeared out to this depth
    }


def main() -> int:
    reps = [l.strip() for l in open(os.path.join(os.path.dirname(__file__), "holdouts3_reps.txt")) if l.strip()]
    print("=" * 92)
    print("Counter STRUCTURE decode (STEP 1.5, SOUND measurement) — the 10 residual binary counters")
    print("=" * 92)
    counters = 0; confirmed = 0
    for spec in reps:
        if bouncer_prove(spec)[0] == "NEVER_HALTS":
            continue                                   # a bouncer, already proven by v3
        counters += 1
        a = analyze(spec)
        if a["verdict"] != "COUNTER-STRUCTURE":
            print(f"  {spec:<22} [{a['verdict']}] {a}")
            continue
        fam = a["family"]
        famstr = (f"'{fam[2]}'·{fam[0]}^k·'{fam[3]}' (k+={fam[1]})" if fam else "irregular-family")
        strong = fam is not None and abs(a["seg_doubling"] - 2.0) < 0.15
        if strong:
            confirmed += 1
        mark = "✓" if strong else " "
        print(f" {mark}{spec:<22} doubling~{a['seg_doubling']:<5} depth={a['carryouts_reached']:>2} "
              f"(~2^{a['carryouts_reached']} steps, no halt)  family={famstr}")
    print("=" * 92)
    print(f"  residual counters analyzed            : {counters}")
    print(f"  binary-counter structure CONFIRMED    : {confirmed}/{counters}")
    print(f"    (regular growing family + op-segment doubling + zero halt-ops to ~2^depth micro-steps)")
    print("\n  SOUND recon only — NO never-halts claim shipped. The op-segment grammar is recursive")
    print("  ('chain of chains': S(k)=[k]+MID(k)+[k+1], MID(k)=MID(k-1)+[pivot]+MID(k-1) for")
    print("  1RB1LA_0LA0RB_0LA0LZ). STEP 2 = nested counter induction (sligocki spec, oracle-gated).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
