#!/usr/bin/env python3
"""x2t_confirm.py -- long exact confirmation for the template writeup:
 (1) run to N steps, exact bytearray; assert never HALT (B reads 1);
 (2) log EVERY rightward-E entry into a maximal 0-run and confirm length is never exactly 3
     and never odd>=3 (record the length histogram of finite gaps);
 (3) verify the super-peak doubling law maxrun: 2^k-2, and the right-cascade recurrence.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle
from collections import Counter

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
M = parse(SPEC)


def run(maxsteps, SZ=1 << 24):
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    finite_gap = Counter()   # lengths of finite maximal 0-runs E enters (exclude background)
    odd_ge3 = 0; gap3 = 0
    peaks = []
    peakbest = 0
    BG = SZ  # sentinel
    while step < maxsteps:
        r = tape[pos]
        if st == 1 and r == 1:
            return dict(halt=True, step=step)
        if st == 4 and r == 0 and pos > lo and tape[pos - 1] == 1:
            j = pos
            while j < SZ and tape[j] == 0: j += 1
            L = j - pos
            # 'background' run: the one that runs to the current right frontier hi
            if j <= hi:  # a genuine finite internal gap (there is a 1 to the right within support)
                finite_gap[L] += 1
                if L >= 3 and L % 2 == 1: odd_ge3 += 1
                if L == 3: gap3 += 1
        act = M[st][r]
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
        if st == 2 and tape[pos] == 0 and pos > off:
            # cheap maxrun update near frontier only when it may set a record
            # measure run ending at pos-1
            k = pos - 1; c = 0
            while k >= lo and tape[k] == 1: c += 1; k -= 1
            if c > peakbest:
                peakbest = c; peaks.append((step, c))
    return dict(halt=False, step=step, finite_gap=finite_gap,
                odd_ge3=odd_ge3, gap3=gap3, peaks=peaks)


if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 5_000_000
    res = run(cap)
    if res['halt']:
        print(f"*** HALT at step {res['step']} ***"); sys.exit()
    print(f"ran {res['step']:,} steps, NO halt.")
    print(f"finite internal gaps E entered: {dict(sorted(res['finite_gap'].items()))}")
    print(f"odd gaps of length>=3 met by E: {res['odd_ge3']}   (length==3: {res['gap3']})")
    print("super-peak maxrun records (step, maxrun); check 2^k-2:")
    for s, c in res['peaks']:
        k = (c + 2)
        pw = bin(k)[2:]
        print(f"   step={s:>10}  maxrun={c:>7}  maxrun+2={k}  ispow2={(k & (k-1))==0}")
