#!/usr/bin/env python3
"""x2c_snap.py -- dump the tape RLE at 'rest' points (head at far right, moving right in a
growth state) and whenever a 0-run of length >=3 appears anywhere on the tape, to see the
REAL reachable configurations and how transient long 0-runs form/close."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
STN = "ABCDEF"
M = parse(SPEC)


def rs(rr, k=60):
    parts = [f"{c}^{n}" if n > 1 else f"{c}" for c, n in rr]
    if len(parts) > k:
        return ' '.join(parts[:k // 2]) + ' ... ' + ' '.join(parts[-k // 2:])
    return ' '.join(parts)


def run(maxsteps, dump_ge=3, SZ=1 << 24):
    tape = bytearray(SZ)
    off = SZ // 2
    pos = off
    st = 0
    step = 0
    lo = hi = pos
    seen_lens = set()
    ndump = 0
    while step < maxsteps and ndump < 40:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            print(f"HALT step={step}")
            return
        # whenever the head is about to READ the left end of a maximal 0-run of odd length>=3
        if r == 0:
            L = 0
            j = pos
            while j < SZ and tape[j] == 0:
                L += 1
                j += 1
            # only report the first time we see each (state,parity,length) combo entering a long run
            if L >= dump_ge and (st, L) not in seen_lens:
                seen_lens.add((st, L))
                par = 'ODD' if L % 2 else 'even'
                rr = rle(tape, max(lo, pos - 30), min(hi, pos + L + 10))
                print(f"[step={step:>10} state={STN[st]} enters 0^{L} ({par})]  local: {rs(rr)}")
                ndump += 1
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
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 5_000_000
    ge = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    run(cap, ge)
