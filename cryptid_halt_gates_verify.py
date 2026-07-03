#!/usr/bin/env python3
"""
o11 / o12 / o13 / o14 / o16 halt predicates — the [PROVEN-from-table] halt gates (2026-07-04).
[PROVEN halt gate + OBSERVED never-fires; halting NOT decided.]

Each of these five Type-I (Mahler-3/2) cryptids has a halt whose unique predecessor is a
single transition, so the halt condition reads straight off the table (like o17/o3). We
verify each gate PROVEN-from-table and machine-check that it never fires from the blank
tape (0 exceptions) -- so non-halting is exactly "the gate is never triggered", an
existence/parity event over the machine's ×3/2 Mahler orbit (the (K) wall).

  o11 = 1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF   (halt C,0; C <- only B,0->1LC)
        => HALT <=> state B reads a 0 whose LEFT neighbour is also 0  (a 00).
  o12 = 1RB0RE_1LC1LD_0RA0LD_1LB0LA_1RF1RA_---1LB   (halt F,0; F <- only E,0->1RF)
        => HALT <=> state E reads a 0 whose RIGHT neighbour is also 0  (an E-phase 00).
  o13 = 1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA   (halt E,0; E <- only D,1->1LE)
        => HALT <=> a D,1->1LE step lands the head on a 0 (E reads 0), i.e. D reads a 1
           whose LEFT neighbour is 0.
  o14 = 1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE   (halt F,0; F <- only C,0->1LF)
        => HALT <=> state C reads a 0 whose LEFT neighbour is also 0  (a 00).
  o16 = 1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE   (halt F,0; F <- only E,0->1RF)
        => HALT <=> state E reads a 0 whose RIGHT neighbour is also 0  (a 00).
"""

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

# (name, spec, halt_state, trigger_state, trigger_read, neighbour_dir)
# gate: HALT <=> state `trigger_state` reads `trigger_read` and tape[pos+neighbour_dir]==0.
GATES = [
    ("o11", "1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF", 1, 0, -1),  # B reads 0, left nbr 0
    ("o12", "1RB0RE_1LC1LD_0RA0LD_1LB0LA_1RF1RA_---1LB", 4, 0, +1),  # E reads 0, right nbr 0
    ("o13", "1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA", 3, 1, -1),  # D reads 1, left nbr 0
    ("o14", "1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE", 2, 0, -1),  # C reads 0, left nbr 0
    ("o16", "1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE", 4, 0, +1),  # E reads 0, right nbr 0
]


def audit(name, spec, tstate, tread, ndir, maxsteps):
    M = parse(spec)
    SZ = 1 << 23
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    fires = 0      # gate condition true (== a genuine halt)
    trig = 0       # trigger (state,read) events
    trig_safe = 0  # trigger events where the neighbour is 1 (safe)
    halted = None
    while step < maxsteps:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            halted = step; break
        if st == tstate and r == tread:
            trig += 1
            nb = tape[pos + ndir]
            if nb == 0:
                fires += 1
            else:
                trig_safe += 1
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    return trig, trig_safe, fires, halted, hi - lo + 1


if __name__ == "__main__":
    print("Halt-gate audit (blank tape, PROVEN gate = unique predecessor of the halt state):")
    print(f"  {'machine':7} {'trigger events':>15} {'safe (nbr=1)':>13} {'GATE FIRES':>11} {'halt?':>18}")
    allok = True
    for name, spec, tstate, tread, ndir in GATES:
        trig, safe, fires, halted, W = audit(name, spec, tstate, tread, ndir, 15_000_000)
        tag = f"HALT@{halted}" if halted else f"run (w={W})"
        gate = f"{SN[tstate]} reads {tread}, {'right' if ndir>0 else 'left'} nbr 0"
        ok = (fires == 0 and halted is None and safe == trig)
        allok &= ok
        print(f"  {name:7} {trig:>15} {safe:>13} {fires:>11} {tag:>18}   [{gate}]")
    print()
    print(f"HALT-GATES VERIFIED (each gate PROVEN from table; 0 firings, every trigger safe): {allok}")
    print("So each halts <=> its gate is triggered (a 00 / parity event) over the machine's x3/2")
    print("Mahler orbit -- the (K)/Mahler-3/2 wall. Halting stays [OPEN]. No machine decided.")
