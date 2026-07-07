#!/usr/bin/env python3
"""x32_gate_census.py -- GATE half for the x3/2 balance family: o2, o7, o10 (2026-07-07).

For each machine:
  (1) [PROVEN from table] scan the transition table: the halt transition and its UNIQUE
      predecessor (the only edge into the halt state), printed as a forced chain.
  (2) [OBSERVED] blank-tape census to 20M steps: at every trigger event (the unique
      predecessor's (state, read) fires) record the radius-3/4/5 window around the head
      (pre-write), check the local safety condition, report distinct-window saturation.

Specs verbatim from suite.py / cryptid_halt_gates_verify.py:
  o2  = 1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA   halt F,0; F <- only D,0->0RF
  o7  = 1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC   halt F,0; F <- only C,0->1LF
  o10 = 1RB1RA_0RC1RC_1LD0LF_0LE1LE_1RA0LB_---0LC   halt F,0; F <- only C,1->0LF

Soundness: this script PROVES nothing about halting; it verifies the table-level gate
and reports an [OBSERVED] finite census. No machine decided.
"""
import sys

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if (t[0] == '-' or t[2] == 'Z')
                       else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

SN = "ABCDEF"

MACHINES = [
    ("o2",  "1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA"),
    ("o7",  "1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC"),
    ("o10", "1RB1RA_0RC1RC_1LD0LF_0LE1LE_1RA0LB_---0LC"),
]

def table_gate(M):
    """Find halt transitions and, for each halt state, all edges into it."""
    halts = [(s, r) for s in range(6) for r in range(2) if M[s][r] is None]
    assert len(halts) == 1, halts
    hs, hr = halts[0]
    preds = []
    for s in range(6):
        for r in range(2):
            act = M[s][r]
            if act is not None and act[2] == hs:
                preds.append((s, r, act))
    return hs, hr, preds

def census(name, spec, maxsteps=20_000_000):
    M = parse(spec)
    hs, hr, preds = table_gate(M)
    print(f"\n=== {name} ===  spec {spec}")
    print(f"  halt transition: ({SN[hs]},{hr}) -> HALT")
    for (s, r, act) in preds:
        w, d, ns = act
        print(f"  edge into {SN[hs]}: {SN[s]},{r} -> {w}{'R' if d>0 else 'L'}{SN[ns]}")
    assert len(preds) == 1, f"{name}: halt-state predecessor NOT unique"
    ts, tr, (tw, td, _) = preds[0]
    # After the predecessor fires, head is at pos+td and halt state reads tape[pos+td];
    # the written cell is tape[pos]=tw. Halt <=> the read cell (pre-existing tape) == hr.
    # Fatal condition on the PRE-STEP tape: tape[pos+td] == hr (write does not touch it).
    print(f"  => [PROVEN from table] HALT <=> state {SN[ts]} reads {tr} with "
          f"{'right' if td>0 else 'left'} neighbour == {hr}")

    SZ = 1 << 24
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0
    trig = 0; fires = 0
    wins = {3: {}, 4: {}, 5: {}}   # window -> first-seen step
    lastnew = {3: 0, 4: 0, 5: 0}
    halted = None
    Mloc = M
    while step < maxsteps:
        r = tape[pos]
        act = Mloc[st][r]
        if act is None:
            halted = step; break
        if st == ts and r == tr:
            trig += 1
            if tape[pos + td] == hr:
                fires += 1
            for rad in (3, 4, 5):
                w = bytes(tape[pos - rad:pos + rad + 1])
                if w not in wins[rad]:
                    wins[rad][w] = step
                    lastnew[rad] = step
        w_, d_, ns_ = act
        tape[pos] = w_; pos += d_; st = ns_; step += 1
    print(f"  census to {step:,} steps: trigger ({SN[ts]},{tr}) events = {trig:,}, "
          f"GATE FIRES = {fires}, halted = {halted}")
    for rad in (3, 4, 5):
        print(f"    radius {rad}: {len(wins[rad])} distinct windows, last new at step {lastnew[rad]:,}")
    if fires == 0 and halted is None:
        print(f"  [OBSERVED] gate saturated SAFE: every trigger has the safe neighbour; 0 firings")
    r5 = sorted(wins[5].items(), key=lambda kv: kv[1])
    print("    r=5 windows (tape around head [pre-write], head cell in brackets):")
    for w, t0 in r5:
        s = ''.join(str(b) for b in w)
        print(f"      {s[:5]}[{s[5]}]{s[6:]}   first at step {t0:,}")
    return fires == 0 and halted is None

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000_000
    ok = True
    for name, spec in MACHINES:
        ok &= census(name, spec, n)
    print(f"\nALL GATES: unique-predecessor PROVEN from table; census safe = {ok}")
    print("No machine decided. No label upgraded.")
