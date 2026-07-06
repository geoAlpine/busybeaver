#!/usr/bin/env python3
"""
o17 ledger-vs-density flavor test (2026-07-06).  [tasks 3-4 of the halt-flavor pin]

o4's ledger: a' = a + delta(G mod 3) -- the branch driver is a FINITE RESIDUE of a 1-D
odometer, so the safety condition is a prefix-sum inequality with drift (+3/gen margin).
o17's candidate "ledger bit": the top-digit marker automaton {3->{3,5}, 5->{3,8=HALT}}
(O17_CORE_TRANSDUCER.md par.7, gate [PROVEN]).  Questions answered here [OBSERVED]:
  (A) Is the marker branch (3->3/5, 5->3/8) a function of ANY finite residue of the
      generation state (tick n mod k, digit-count m mod k, digit-sum S mod k, low digits,
      previous marker, seed j)?   -- the o4-delta-map test.
  (B) Does the fatal-adjacent state 5 RECUR on runners (no-drift exposure), or does the
      orbit drift away from it (o4-style margin)?
  (C) Blank orbit: same marker mechanism? frontier-gate census (state, leading block).
No machine decided; nothing about halting claimed beyond finite checked halts.
"""
import sys
from collections import defaultdict, Counter

SPEC = "1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if t[0] == '-' else
                       (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

M = parse(SPEC)

def blocks_from(tape, i, hi):
    r = []
    while i <= hi:
        while i <= hi and tape[i] == 0: i += 1
        j = i
        while j <= hi and tape[j] == 1: j += 1
        if j > i: r.append(j - i)
        i = j
    return r

def milestones(L, maxsteps):
    """Run core seed 0 A 0 1^L; return (halted, halt_step, list of milestone dicts).
    Milestone = state A reads 0 at the true left frontier (all cells left are 0)."""
    SZ = 1 << 22
    tape = bytearray(SZ); off = SZ // 2
    for i in range(1, L + 1): tape[off + i] = 1
    pos = off; st = 0; step = 0; lo = hi = pos; prevdir = 0
    n = 0  # tick count
    out = []
    while step < maxsteps:
        r = tape[pos]
        if st == 5 and r == 0:
            return True, step, out
        if st == 0 and r == 0 and tape[pos - 1] == 0:
            if not any(tape[i] for i in range(lo, pos)):   # true frontier
                bl = blocks_from(tape, pos + 1, hi)
                marker = bl[0] if bl else 0
                digs = [(x - 2) // 3 for x in bl[1:]]
                out.append(dict(step=step, n=n, marker=marker, m=len(digs),
                                S=sum(digs), d=digs[:3], dl=digs[-1] if digs else -1))
        ww, d, ns = M[st][r]
        if st == 4 and r == 0 and prevdir == -1 and d == 1 and pos >= hi - 3:
            n += 1
        prevdir = d
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    return False, step, out

def main():
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 3_000_000
    halter_caps = {2: 5000, 4: 5000, 5: 900_000, 7: 4_500_000, 8: 10_000,
                   10: 10_000, 12: 20_000, 15: 60_000, 17: 60_000, 19: 150_000, 21: 300_000}
    runners = [1, 3, 6, 9, 11, 13, 14, 16, 18, 20, 22]
    print("=== (A)+(B) core-seed marker itineraries ===")
    trans5 = []   # (features..., outcome) at each 5-milestone
    trans3 = []
    per_seed = {}
    for j in sorted(list(halter_caps) + runners):
        L = 3 * j
        capj = halter_caps.get(j, cap)
        halted, hstep, ms = milestones(L, capj)
        marks = [x['marker'] for x in ms]
        per_seed[j] = (halted, hstep, ms)
        tag = f"HALT@{hstep}" if halted else f"run>{hstep}"
        print(f"  j={j:2d} L={L:3d} {tag:>14}  milestones={len(ms):3d}  markers={marks}")
        seq = ms + ([dict(marker=8, n=None, m=None, S=None, d=None, dl=None, step=hstep)]
                    if halted else [])
        for a, b in zip(seq, seq[1:]):
            feat = dict(j=j, n=a['n'], m=a['m'], S=a['S'],
                        d1=a['d'][0] if a['d'] else -1,
                        d2=a['d'][1] if a['d'] and len(a['d']) > 1 else -1,
                        dl=a['dl'])
            if a['marker'] == 5:
                trans5.append((feat, b['marker']))
            elif a['marker'] == 3:
                trans3.append((feat, b['marker']))
    print()
    print(f"=== (A) branch-determinism search: {len(trans5)} 5-milestone and "
          f"{len(trans3)} 3-milestone transitions ===")
    for name, trans, outs in (("5->{3,8}", trans5, (3, 8)), ("3->{3,5}", trans3, (3, 5))):
        print(f"  branch {name}: outcomes {Counter(o for _, o in trans)}")
        tested = 0; deciders = []
        featnames = (["j"] + [f"n%{k}" for k in range(2, 13)] +
                     [f"m%{k}" for k in range(2, 7)] + [f"S%{k}" for k in range(2, 7)] +
                     ["d1", "d2", "dl", "m", "S"])
        def fval(feat, fn):
            if '%' in fn:
                base, k = fn.split('%'); return feat[base] % int(k)
            return feat[fn]
        for fn in featnames:
            tested += 1
            bymap = defaultdict(set)
            for feat, o in trans:
                bymap[fval(feat, fn)].add(o)
            if all(len(v) == 1 for v in bymap.values()):
                deciders.append(fn)
        # pairs of the residue features
        pairnames = []
        smallfeats = [f"n%{k}" for k in (2, 3, 4, 6)] + ["m%2", "m%3", "S%2", "S%3", "d1", "dl"]
        for i in range(len(smallfeats)):
            for k in range(i + 1, len(smallfeats)):
                bymap = defaultdict(set)
                for feat, o in trans:
                    bymap[(fval(feat, smallfeats[i]), fval(feat, smallfeats[k]))].add(o)
                if all(len(v) == 1 for v in bymap.values()):
                    pairnames.append((smallfeats[i], smallfeats[k]))
        print(f"    single features tested: {tested}; DECIDING: {deciders or 'NONE'}")
        print(f"    residue-feature pairs deciding: {pairnames or 'NONE'}")
    print()
    print("=== (B) 5-visit recurrence on runners (exposure to the fatal branch) ===")
    for j in runners:
        halted, hstep, ms = per_seed[j]
        if halted: continue
        fives = [x['step'] for x in ms if x['marker'] == 5]
        print(f"  j={j:2d}: milestones={len(ms):3d}, 5-milestones={len(fives):3d}, "
              f"last 5 at step {fives[-1] if fives else '-'} (cap {hstep})")
    print()
    print("=== (C) blank-orbit frontier gates (marker mechanism on the real orbit) ===")
    SZ = 1 << 24
    tape = bytearray(SZ); pos = SZ // 2; st = 0; step = 0; lo = hi = pos
    capb = 300_000_000
    gates = []
    while step < capb:
        r = tape[pos]
        if st == 5 and r == 0:
            print(f"  HALT at {step}"); break
        if r == 0 and st in (0, 3) and tape[pos - 1] == 0:   # A or D reads 0, left nb 0
            if not any(tape[i] for i in range(lo, pos)):
                run1 = 0; q = pos + 1
                while tape[q] == 1: run1 += 1; q += 1
                gates.append((step, "AD"[0 if st == 0 else 1], run1))
        ww, d, ns = M[st][r]
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    print(f"  blank orbit {capb} steps: {len(gates)} true-frontier A/D-reads-0 gates")
    for s, stt, run1 in gates:
        print(f"    step {s:>12,}  state {stt}  leading-1-run {run1}")
    dcount = sum(1 for _, stt, _ in gates if stt == 'D')
    print(f"  D-state frontier gates (would HALT): {dcount}")

if __name__ == "__main__":
    main()
