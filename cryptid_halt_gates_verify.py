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
    ("SN",  "1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD", 2, 0, -1),  # C reads 0, left nbr 0
]

# Space Needle's gate is NOT vacuous (it DOES halt for some 1^m seeds); the blank orbit
# just avoids the halt set. Verify the PROVEN gate fires exactly on the (corrected) halt set.
SN_TM = "1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD"

def sn_epoch_halts(m):
    """True SN milestone: 1^m block, head on the 0 right of it, state C. Does the epoch halt?"""
    M = parse(SN_TM)
    SZ = 1 << 21
    tape = bytearray(SZ); off = SZ // 2
    for i in range(m): tape[off + i] = 1
    pos = off + m; st = 2; step = 0; lo = off; hi = off + m - 1
    budget = int(0.6 * m**3) + 300000
    while step < budget:
        r = tape[pos]; act = M[st][r]
        if act is None: return True
        ww, d, ns = act; tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    return False

def allones(m): return set(bin(m)[2:]) == {'1'}


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
    print(f"HALT-GATES VERIFIED (each gate PROVEN from table; 0 firings from blank, every trigger safe): {allok}")
    print("Type I (o11,o12,o13,o14,o16): halts <=> gate fires = a 00/parity event over a x3/2 Mahler orbit.")
    print()
    print("Space Needle -- the gate is NOT vacuous (halts for some 1^m seeds); blank orbit avoids the halt set.")
    halts = [m for m in range(1, 65) if sn_epoch_halts(m)]
    nonAO = [m for m in halts if not allones(m)]
    print(f"  PROVEN gate 'C reads a 00' fires (epoch halts) exactly for m in {halts}  (m<=64)")
    print(f"  = all-ones {[m for m in range(1,65) if allones(m)]} PLUS {nonAO} (NOT all-ones -- agent's clean claim corrected)")
    print("  => SN halts <=> the scalar orbit m,f(m),f^2(m),... (f(m)=m+3*floor(m/2^(v+1))+v) reaches this halt set;")
    print("     the blank orbit 2,5,9,16,40,... avoids it in range => [OPEN], generalized-Collatz reachability.")
    print("\nHalting stays [OPEN] for all six. No machine decided. No label upgraded.")
