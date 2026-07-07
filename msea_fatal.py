#!/usr/bin/env python3
"""
Mahler-sea survey — FATAL-SET probe (2026-07-07).
Standalone configs in the reachable-form family: capture a real milestone config
(state, extreme-side head placement, block pattern), then mutate block lengths and run
each mutant bounded. A mutant that HALTS is a concrete member of the fatal set
[PROVEN nonempty by the run]; bounded non-halt proves NOTHING.
Space Needle: re-confirm the known fatal 1^m epoch seeds (cryptid_halt_gates_verify.py).
Decides nothing about the blank-tape orbits.
"""
import sys
from collections import Counter
from msea_struct2 import parse, rle_blocks

SN_ = "ABCDEF"

MACHINES = {
    "o11": ("1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF", 1, 'R'),
    "o12": ("1RB0RE_1LC1LD_0RA0LD_1LB0LA_1RF1RA_---1LB", 2, 'L'),
    "o13": ("1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA", 2, 'L'),
    "o14": ("1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE", 4, 'L'),
    "o16": ("1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE", 0, 'R'),
}

def capture(spec, mstate, side, N, want):
    """Run blank tape; at extreme+state milestones whose RLE matches want(blocks),
    return (blocks, head_rel, gaps) where head_rel is offset from first/last 1,
    gaps = list of 0-run lengths between blocks."""
    M = parse(spec)
    SZ = 1 << 22
    tape = bytearray(SZ)
    pos = SZ // 2
    st = 0
    lo = hi = pos
    step = 0
    while step < N:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            return None
        at_ext = (pos <= lo) if side == 'L' else (pos >= hi)
        if st == mstate and at_ext:
            b = rle_blocks(tape, lo, hi)
            if want(b):
                # first/last 1 positions and inter-block gaps
                a = lo
                while not tape[a]:
                    a += 1
                z = hi
                while not tape[z]:
                    z -= 1
                gaps = []
                run = 0
                for i in range(a, z + 1):
                    if tape[i]:
                        if run:
                            gaps.append(run)
                        run = 0
                    else:
                        run += 1
                head_rel = pos - a if side == 'L' else pos - z
                return dict(blocks=b, gaps=gaps, head_rel=head_rel, state=st)
        ww, d, ns = act
        tape[pos] = ww
        pos += d
        st = ns
        step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
    return None

def run_mutant(spec, blocks, gaps, head_rel, state, side, budget):
    M = parse(spec)
    total = sum(blocks) + sum(gaps) + 64
    SZ = 1 << 20
    tape = bytearray(SZ)
    p = SZ // 2
    first1 = p
    for i, b in enumerate(blocks):
        for j in range(b):
            tape[p] = 1
            p += 1
        if i < len(gaps):
            p += gaps[i]
    last1 = p - 1
    # trailing gap after last block (if captured pattern had more gaps than joints, ignore)
    pos = (first1 + head_rel) if side == 'L' else (last1 + head_rel)
    st = state
    step = 0
    while step < budget:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            return step  # HALT
        ww, d, ns = act
        tape[pos] = ww
        pos += d
        st = ns
        step += 1
    return None

def probe(name, mutants, want, capN=20_000_000, budget=250_000):
    spec, mstate, side = MACHINES[name]
    cap = capture(spec, mstate, side, capN, want)
    if cap is None:
        print(f"=== {name}: no matching milestone captured — SKIP")
        return
    print(f"=== {name}: captured blocks={cap['blocks'][:8]}{'...' if len(cap['blocks'])>8 else ''} "
          f"gaps={cap['gaps'][:8]}{'...' if len(cap['gaps'])>8 else ''} head_rel={cap['head_rel']} state={SN_[cap['state']]}")
    halts = []
    tried = 0
    for blocks, gaps in mutants(cap):
        tried += 1
        h = run_mutant(spec, blocks, gaps, cap['head_rel'], cap['state'], side, budget)
        if h is not None:
            halts.append((blocks, gaps, h))
    print(f"  mutants tried: {tried}; HALTED: {len(halts)}")
    for b, g, h in halts[:10]:
        print(f"    HALT@{h}: blocks={b} gaps={g}")
    print()
    return halts

def o11_mut(cap):
    # family 1^k 0 (10)^m : blocks [k]+[1]*m, gaps all 1
    for k in range(2, 16):
        for m in range(1, 13):
            blocks = [k] + [1] * m
            gaps = [1] * m
            yield blocks, gaps[:len(blocks) - 1]

def o12_mut(cap):
    # family 1^a 0 1^b 0 (10)^m
    for a in range(2, 12):
        for b in range(1, 8):
            for m in (1, 2, 3, 5):
                blocks = [a, b] + [1] * m
                yield blocks, [1] * (len(blocks) - 1)

o13_mut = o12_mut

def o14_mut(cap):
    # captured family [a,1,b,1^m,4,4,2]; mutate a,b,m keep tail
    for a in range(2, 12):
        for b in range(1, 8):
            for m in (1, 2, 4):
                blocks = [a, 1, b] + [1] * m + [4, 4, 2]
                yield blocks, [1] * (len(blocks) - 1)

def o16_mut(cap):
    # family [k | 1^m sea | defect d]; gap after k is 2 (0^2), sea gaps 1
    for k in range(1, 11):
        for m in (1, 2, 3, 5, 8):
            for d in (2, 3, 4, 5, 8):
                blocks = [k] + [1] * m + [d]
                gaps = [2] + [1] * m
                yield blocks, gaps[:len(blocks) - 1]

# --- Space Needle: known fatal 1^m epoch seeds ---
SNTM = "1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD"
def sn_epoch_halts(m):
    M = parse(SNTM)
    SZ = 1 << 21
    tape = bytearray(SZ)
    off = SZ // 2
    for i in range(m):
        tape[off + i] = 1
    pos = off + m
    st = 2
    step = 0
    budget = int(0.6 * m ** 3) + 300000
    while step < budget:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            return step
        ww, d, ns = act
        tape[pos] = ww
        pos += d
        st = ns
        step += 1
    return None

if __name__ == "__main__":
    probe("o11", o11_mut, lambda b: len(b) >= 3 and b[0] > 1 and all(x == 1 for x in b[1:]))
    probe("o12", o12_mut, lambda b: len(b) >= 3 and b[0] > 1 and b[1] == 4 and all(x == 1 for x in b[2:]))
    probe("o13", o13_mut, lambda b: len(b) >= 3 and b[0] > 1 and b[1] == 4 and all(x == 1 for x in b[2:]))
    probe("o14", o14_mut, lambda b: len(b) >= 6 and b[1] == 1 and b[-3:] == [4, 4, 2] and b[2] > 4)
    probe("o16", o16_mut, lambda b: len(b) >= 3 and b[0] > 1 and b[-1] == 4 and all(x == 1 for x in b[1:-1]))
    print("=== SN: known fatal epoch seeds 1^m (state C, head right of block)")
    hs = [(m, sn_epoch_halts(m)) for m in range(1, 33)]
    fatal = [(m, h) for m, h in hs if h is not None]
    print(f"  fatal m in 1..32: {[m for m, _ in fatal]}  (e.g. m={fatal[0][0]} halts @ step {fatal[0][1]})"
          if fatal else "  none in range")
    print("\nFATAL-SET PROBE: a HALT = concrete fatal standalone config [PROVEN by run];")
    print("bounded non-halt proves nothing. No machine decided. No label upgraded.")
