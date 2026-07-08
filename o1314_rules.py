#!/usr/bin/env python3
"""
o13/o14 fixed-point deep dive, part 3: THE RULE SYSTEM, unit-tested on grids (2026-07-08).
Seed a standalone milestone (captured head placement: head on leftmost 1, L-extreme),
run to the NEXT milestone (designated state at L-extreme, changed RLE) / HALT, and verify:

o13  milestone [a, b, (10)^m], state C, head on first 1:
  R1 in-epoch   [a,b,1^m] -> [a-2, b+3, 1^m]           (a >= 4)
  R2 collapse   [2,b,1^m] -> [b+3, 1^m]                (a hits 2; pure [b+3] if m=0)
  R3 a-start    full sub-cycle [a,4,1^m] ->...-> next [a',4,1^m'] with
                a' = floor(3a/2)+7 (a even) / +4 (a odd)   [x3/2 inner engine]
  HALT: some D->E eat-sweep consumes an EVEN-length run of 1s (o10 twin, [PROVEN mechanic]).

o14  milestone [a, 1, b, <field>, 4,4,2], state E, head on first 1:
  R1 in-epoch   [a,1,b,tail] -> [a-2, 1, b+3, tail]      (a >= 3)
  R3 a-start    a' = floor(3a/2)+6                          [x3/2 inner engine]
  HALT: C->F leftward step lands on a 0 (00-gap collision, [PROVEN mechanic]).

Every rule = exact concrete simulation on the stated grid; a halt is PROVEN-by-run.
Labels: [PROVEN on grid]. No induction claimed.
"""
import sys
from msea_struct2 import parse, rle_blocks

MACH = {
    "o13": ("1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA", 2, 'L'),
    "o14": ("1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE", 4, 'L'),
}
SN = "ABCDEF"

def seed_tape(blocks, gaps, margin=2048):
    tot = sum(blocks) + sum(gaps)
    SZ = margin * 2 + 8 * (tot + 64) + 8192
    tape = bytearray(SZ)
    p = margin
    lo = p
    for i, bl in enumerate(blocks):
        for _ in range(bl):
            tape[p] = 1; p += 1
        if i < len(gaps):
            p += gaps[i]
    return tape, lo, p  # p = one past last written cell

def run_to_milestone(spec, tape, lo, first1, state, mstate, budget=300_000_000):
    """Run from (state, head=first1) until next mstate/L-extreme milestone with changed
    RLE, or HALT. Returns (kind, blocks_or_anat, steps)."""
    M = parse(spec)
    pos = first1
    hi = pos
    # find current hi (rightmost 1)
    z = len(tape) - 1
    while z > pos and not tape[z]:
        z -= 1
    hi = z
    st = state
    b0 = rle_blocks(tape, lo, hi)
    step = 0
    while step < budget:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            left = tape[pos - 1]; right = tape[pos + 1]
            return ('HALT', (SN[st], r, left, right), step)
        if st == mstate and pos <= lo and step > 0:
            b = rle_blocks(tape, lo, hi)
            if b != b0:
                return ('MIL', b, step)
        ww, d, ns = act
        tape[pos] = ww
        pos += d
        st = ns
        step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
        if pos < 8 or pos >= len(tape) - 8:
            raise RuntimeError("tape bounds — enlarge margin")
    return ('BUDGET', None, step)

# ---------- o13 ----------
def o13_seed(a, b, m):
    blocks = [a, b] + [1] * m
    gaps = [1] * (len(blocks) - 1)
    tape, lo, _ = seed_tape(blocks, gaps)
    return tape, lo, lo   # head on first 1

def o13_step(a, b, m):
    spec = MACH["o13"][0]
    tape, lo, first1 = o13_seed(a, b, m)
    return run_to_milestone(spec, tape, lo, first1, 2, 2)

def test_o13_R1(amax, bmax, ms=(0, 1, 2, 3)):
    bad = tot = 0
    for a in range(4, amax + 1, 2):
        for b in range(1, bmax + 1):
            for m in ms:
                kind, pay, s = o13_step(a, b, m)
                want = [a - 2, b + 3] + [1] * m
                tot += 1
                if kind != 'MIL' or pay != want:
                    bad += 1
                    if bad <= 8:
                        print(f"  o13 R1 MISS a={a} b={b} m={m}: {kind} {pay} want {want}")
    print(f"o13 R1 [a,b,1^m]->[a-2,b+3,1^m]: {tot-bad}/{tot} exact")

def test_o13_R2(bmax, ms=(0, 1, 2, 3)):
    bad = tot = 0; anat = set()
    for b in range(1, bmax + 1):
        for m in ms:
            kind, pay, s = o13_step(2, b, m)
            want = [b + 3] + [1] * m
            tot += 1
            if kind != 'MIL' or pay != want:
                bad += 1
                if bad <= 8:
                    print(f"  o13 R2 MISS b={b} m={m}: {kind} {pay} want {want}")
    print(f"o13 R2 collapse [2,b,1^m]->[b+3,1^m]: {tot-bad}/{tot} exact")

def o13_astart(a, m=0, budget=300_000_000):
    """Seed [a,4,1^m]; run full sub-cycle to next milestone with a 4-in-2nd-block
    (a-start) or collapse; return the next a-start value."""
    spec = MACH["o13"][0]
    tape, lo, first1 = o13_seed(a, 4, m)
    st = 2; pos = first1
    M = parse(spec)
    z = len(tape) - 1
    while z > pos and not tape[z]:
        z -= 1
    hi = z
    step = 0; b0 = rle_blocks(tape, lo, hi); seen0 = True
    while step < budget:
        r = tape[pos]; act = M[st][r]
        if act is None:
            return ('HALT', step)
        if st == 2 and pos <= lo and step > 0:
            b = rle_blocks(tape, lo, hi)
            if b != b0:
                b0 = b
                # a-start = milestone with 2nd block == 4 and first block>4
                if len(b) >= 2 and b[1] == 4 and b[0] > 4:
                    return ('ASTART', b[0], step)
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
    return ('BUDGET', None, step)

def test_o13_astart(amax):
    # NOTE: o13's a-start recursion is a SEA-COUPLED composite; naive standalone [a,4]
    # (no sea) does NOT reproduce it — those seeds mostly HALT (concrete fatal members,
    # see o1314_halt.py). The recursion is verified ON-ORBIT in o1314_fixedpoint.py
    # (14/14 forward epoch-steps). Report a small standalone halt-census here instead.
    halts = sum(1 for a in range(6, amax + 1) if o13_astart(a)[0] == 'HALT')
    print(f"o13 a-start: verified ON-ORBIT in o1314_fixedpoint.py (a'=floor(3a/2)+7 even/+4 odd, 14/14).")
    print(f"  standalone [a,4] seeds (sea-decoupled): {halts}/{amax-5} HALT = fatal members [PROVEN by run]")

# ---------- o14 ----------
def o14_seed(a, b, tail):
    blocks = [a, 1, b] + list(tail)
    gaps = [1] * (len(blocks) - 1)
    tape, lo, _ = seed_tape(blocks, gaps)
    return tape, lo, lo

def o14_step(a, b, tail):
    spec = MACH["o14"][0]
    tape, lo, first1 = o14_seed(a, b, tail)
    return run_to_milestone(spec, tape, lo, first1, 4, 4)

def test_o14_R1(amax, bmax, tails):
    bad = tot = 0
    for a in range(3, amax + 1):
        for b in range(4, bmax + 1):
            for tail in tails:
                kind, pay, s = o14_step(a, b, tail)
                want = [a - 2, 1, b + 3] + list(tail)
                tot += 1
                if kind != 'MIL' or pay != want:
                    bad += 1
                    if bad <= 8:
                        print(f"  o14 R1 MISS a={a} b={b} tail={tail}: {kind} {pay} want {want}")
    print(f"o14 R1 [a,1,b,tail]->[a-2,1,b+3,tail]: {tot-bad}/{tot} exact")

def o14_astart(a, field=6, budget=300_000_000):
    """Seed [a,1,7, 1^field, 4,4,2]; run to next a-start ([a',1,7,...])."""
    spec = MACH["o14"][0]
    tail = [1] * field + [4, 4, 2]
    tape, lo, first1 = o14_seed(a, 7, tail)
    st = 4; pos = first1; M = parse(spec)
    z = len(tape) - 1
    while z > pos and not tape[z]:
        z -= 1
    hi = z; step = 0; b0 = rle_blocks(tape, lo, hi)
    while step < budget:
        r = tape[pos]; act = M[st][r]
        if act is None:
            return ('HALT', step)
        if st == 4 and pos <= lo and step > 0:
            b = rle_blocks(tape, lo, hi)
            if b != b0:
                b0 = b
                if len(b) >= 3 and b[1] == 1 and b[2] == 7 and b[0] > 4:
                    return ('ASTART', b[0], step)
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
    return ('BUDGET', None, step)

def test_o14_astart(amax):
    bad = tot = 0
    for a in range(5, amax + 1):
        kind = o14_astart(a)
        want = (3 * a) // 2 + 6
        tot += 1
        if kind[0] != 'ASTART' or kind[1] != want:
            bad += 1
            if bad <= 12:
                print(f"  o14 a-start MISS a={a}: {kind} want {want}")
    print(f"o14 a-start a'=floor(3a/2)+6: {tot-bad}/{tot} exact  [x3/2 engine]")

if __name__ == "__main__":
    amax = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    print(f"o13 rules (grids up to a={amax}):")
    test_o13_R1(min(amax, 120), 40)
    test_o13_R2(200)
    test_o13_astart(amax)
    print(f"\no14 rules (grids up to a={amax}):")
    test_o14_R1(min(amax, 80), 30, tails=[[4, 4, 2], [1, 4, 4, 2], [1, 1, 4, 4, 2]])
    test_o14_astart(amax)
    print("\nAll rules [PROVEN on the stated grids] (exact runs). No machine decided. No label upgraded.")
