#!/usr/bin/env python3
"""Deep-dive the near-x2 cluster: dump macro-structure (RLE at record milestones),
extract the value-map v->v', find halt gate. STRICT observe-only."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle

def sim(spec, maxsteps, SZ=1 << 24):
    M = parse(spec); tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos; snaps = []
    while step < maxsteps:
        r = tape[pos]
        act = M[st][r] if r < 2 else None
        if act is None:
            return ('HALT', step, snaps, tape, lo, hi, pos, st)
        ww, d, ns = act; tape[pos] = ww; pos += d; st = ns; step += 1
        nr = None
        if pos < lo: lo = pos; nr = 'L'
        elif pos > hi: hi = pos; nr = 'R'
        if nr:
            snaps.append((nr, step, st, pos - off, rle(tape, lo, hi)))
        if pos < 8 or pos > SZ - 8:
            return ('OVR', step, snaps, tape, lo, hi, pos, st)
    return ('MAX', step, snaps, tape, lo, hi, pos, st)

def collapse(snaps):
    out = []
    for s in snaps:
        if out and out[-1][0] == s[0] and s[1] - out[-1][1] == 1:
            out[-1] = s
        else:
            out.append(s)
    return out

def rle_str(r, maxblocks=30):
    parts = []
    for c, n in r:
        parts.append(f"{c}^{n}" if n > 1 else f"{c}")
    s = ' '.join(parts)
    if len(r) > maxblocks:
        s = ' '.join(parts[:maxblocks//2]) + ' ... ' + ' '.join(parts[-maxblocks//2:])
    return s

if __name__ == "__main__":
    spec = sys.argv[1]
    cap = int(sys.argv[2]) if len(sys.argv) > 2 else 3_000_000
    outc, step, snaps, tape, lo, hi, pos, st = sim(spec, cap)
    snaps = collapse(snaps)
    L = [s for s in snaps if s[0] == 'L']; R = [s for s in snaps if s[0] == 'R']
    fast = R if len(R) >= len(L) else L
    print(f"spec={spec}")
    print(f"outc={outc} step={step} nL={len(L)} nR={len(R)} fast={'R' if fast is R else 'L'} nfast={len(fast)}")
    print(f"\n--- tail milestones on fast side (RLE) ---")
    for s in fast[-24:]:
        side, stp, state, relpos, r = s
        tot1 = sum(n for c, n in r if c == 1)
        mx = max((n for c, n in r if c == 1), default=0)
        print(f"  step={stp:>10} st={state} nblk={len(r):>3} tot1={tot1:>7} maxrun={mx:>7} w={r and sum(n for _,n in r):>6}  {rle_str(r)}")
