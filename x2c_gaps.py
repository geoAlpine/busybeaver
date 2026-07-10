#!/usr/bin/env python3
"""x2c_gaps.py -- (1) PROVE the finite local sweep/gap rules by direct enumeration.
(2) Extract the reachable gap-structure: at each right-frontier turnaround (a 'rest'
milestone) record the full left-to-right sequence of maximal 0-run lengths (gaps) between
1-blocks, to read the grammar. (3) During sweeps, record the gaps the E-scanner actually
meets and their parity, tracking how transient large even gaps form."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
STN = "ABCDEF"
M = parse(SPEC)


def prove_local_gap_rules():
    """Directly enumerate the outcome of the E-scanner meeting a gap 0^g followed by 1,
    for g=1..8, with the head E on the LEFT 0 of the gap, right context a 1-block, left
    context irrelevant (rule is local to the gap+first following 1). Exhaustive, exact."""
    print("=== Local E-scanner gap rules (PROVEN by direct enumeration) ===")
    results = {}
    for g in range(1, 9):
        # tape: [1]  0^g  1^4   with E on the first 0 of the gap
        SZ = g + 12
        tape = bytearray(SZ)
        tape[0] = 1
        base = 1
        for i in range(g):
            tape[base + i] = 0
        for i in range(4):
            tape[base + g + i] = 1
        pos = base
        st = 4  # E
        step = 0
        outcome = None
        while step < 200:
            r = tape[pos] if 0 <= pos < SZ else 0
            if st == 1 and r == 1:
                outcome = 'HALT'
                break
            act = M[st][r]
            ww, d, ns = act
            if 0 <= pos < SZ:
                tape[pos] = ww
            pos += d
            st = ns
            step += 1
            # exit when head leaves the gap region to the right past the block, or to the left
            if pos < 0 or pos > base + g + 3:
                outcome = f'{STN[st]} exit {"R" if pos > base else "L"}'
                break
        par = 'ODD' if g % 2 else 'even'
        results[g] = outcome
        flag = '   <== HALT' if outcome == 'HALT' else ''
        print(f"  gap 0^{g} ({par:4}): -> {outcome} in {step} steps{flag}")
    return results


def gap_sequence(tape, L0, R0):
    """left-to-right list of maximal 0-run lengths strictly between the first and last 1."""
    r = rle(tape, L0, R0)
    return [n for c, n in r if c == 0]


def run_rest_gaps(maxsteps, SZ=1 << 22):
    tape = bytearray(SZ)
    off = SZ // 2
    pos = off
    st = 0
    step = 0
    lo = hi = pos
    last = 0
    dumps = 0
    print("\n=== Reachable REST gap-sequences (at right-frontier turnaround) ===")
    while step < maxsteps and dumps < 16:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            print(f"HALT step={step}")
            return
        if st == 2 and r == 0 and pos > last + 3:
            L0 = lo
            while L0 < pos and tape[L0] == 0:
                L0 += 1
            R0 = pos - 1
            while R0 > L0 and tape[R0] == 0:
                R0 -= 1
            gaps = gap_sequence(tape, L0, R0)
            mx = max(gaps) if gaps else 0
            odd3 = [g for g in gaps if g >= 3 and g % 2 == 1]
            print(f"  w={pos-L0:>5} gaps(L->R)={gaps}  max={mx}  odd>=3:{odd3}")
            last = pos
            dumps += 1
        ww, d, ns = act
        tape[pos] = ww
        pos += d
        st = ns
        step += 1
        if pos < lo:
            lo = pos
        elif pos > hi:
            hi = pos


if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    prove_local_gap_rules()
    run_rest_gaps(cap)
