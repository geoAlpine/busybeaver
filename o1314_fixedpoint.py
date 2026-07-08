#!/usr/bin/env python3
"""
o13/o14 fixed-point deep dive, part 4: FIXED-POINT CLOSED FORMS (2026-07-08).
(The O4_RUN_STRUCTURE / O11_REFILL trick applied to o13/o14's inner x3/2 engines.)

o13 a-start map (parity-dependent correction c in {7,4} = 3d+1):
    even a: a' = 3a/2 + 7        fixed point  x_e = -14   (x = 3x/2+7)
    odd  a: a' = (3a+7)/2        fixed point  x_o = -7     (2x = 3x+7)
  => even-run = v2(a+14),  odd-run = v2(a+7)
  Combined  T13(a) = floor(3a/2) + (7 if a even else 4).

o14 a-start map (SINGLE correction +6, like o11's +4):
    even a: a' = 3a/2 + 6        fixed point  x_e = -12   (x = 3x/2+6)
    odd  a: a' = (3a+11)/2       fixed point  x_o = -11    (2x = 3x+11)
  => even-run = v2(a+12),  odd-run = v2(a+11)
  Combined  T14(a) = floor(3a/2) + 6.   (matched pair x_e,x_o differ by 1, exactly the o11 shape.)

THEOREM [2-line proof + exhaustive check]: on a same-parity run the distance to the
branch fixed point multiplies by exactly 3/2 (3 a 2-adic unit), and branch membership is
the 2-divisibility of that distance; hence the maximal run = v2 of the distance. Same 2-adic
depth process as Antihydra (v2 under x3/2), o11, o4 (v3 under x4/3). Antihydra's own (p,q)=(2,3).
"""
import sys, math

def v2(n):
    return (n & -n).bit_length() - 1 if n else 99

# combined maps
def T13(a):
    return (3 * a) // 2 + (7 if a % 2 == 0 else 4)
def T14(a):
    return (3 * a) // 2 + 6

def run_len(a, T):
    p = a & 1; r = 0
    while (a & 1) == p:
        r += 1; a = T(a)
    return r

SPECS = {
    "o13": (T13, lambda a: v2(a + 7) if a & 1 else v2(a + 14), (-14, -7), (7, 4)),
    "o14": (T14, lambda a: v2(a + 11) if a & 1 else v2(a + 12), (-12, -11), (6, 6)),
}

def check_closed(name, MMAX):
    T, closed, (xe, xo), _ = SPECS[name]
    bad = 0
    for a in range(2, MMAX + 1):
        if run_len(a, T) != closed(a):
            bad += 1
            if bad < 5:
                print(f"  {name} MISMATCH a={a}: run {run_len(a,T)} vs closed {closed(a)}")
    print(f"{name}: even-run=v2(a-({xe}))=v2(a+{-xe}), odd-run=v2(a-({xo}))=v2(a+{-xo}) "
          f"exhaustive a=2..{MMAX}: {MMAX-1-bad}/{MMAX-1} exact")

def check_mirror(name):
    T = SPECS[name][0]
    xe, xo = SPECS[name][2]
    We, Uo = -xe, -xo  # W = a - x_e, U = a - x_o
    bad = 0
    for a in range(2, 5000):
        if a % 2 == 0:
            if 2 * (T(a) + We) != 3 * (a + We): bad += 1
        else:
            if 2 * (T(a) + Uo) != 3 * (a + Uo): bad += 1
    print(f"{name}: mirror W=a+{We} (x3/2 on even) / U=a+{Uo} (x3/2 on odd): {'exact' if bad==0 else f'{bad} FAIL'} on a<5000")

def orbit_astart(spec_str, mstate, N):
    """Extract the on-orbit a-start subsequence from the blank tape milestone chain."""
    from msea_struct2 import parse, rle_blocks
    M = parse(spec_str)
    SZ = 1 << 24
    tape = bytearray(SZ); pos = SZ // 2; st = 0; lo = hi = pos; step = 0
    last = None; astarts = []
    is13 = (mstate == 2)
    while step < N:
        r = tape[pos]; act = M[st][r]
        if act is None: break
        if st == mstate and pos <= lo:
            b = rle_blocks(tape, lo, hi)
            if b != last:
                last = list(b)
                if is13:
                    if len(b) >= 2 and b[1] == 4 and b[0] > 4:
                        astarts.append(b[0])
                else:
                    if len(b) >= 3 and b[1] == 1 and b[2] == 7 and b[0] > 4:
                        astarts.append(b[0])
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
    return astarts

def check_onorbit(name, spec_str, mstate, N):
    T, closed, (xe, xo), corr = SPECS[name]
    astarts = orbit_astart(spec_str, mstate, N)
    # verify a-start recursion a' = T(a) on forward (growing) steps
    bad = tot = 0
    for i in range(len(astarts) - 1):
        a0, a1 = astarts[i], astarts[i + 1]
        if a1 > a0:
            tot += 1
            if a1 != T(a0):
                bad += 1
    print(f"{name}: on-orbit a-start recursion a'=T(a) on {tot} forward epoch-steps: {tot-bad}/{tot} exact"
          f"  (a-starts: {astarts[:14]}...)")
    # run cap on orbit
    if len(astarts) > 3:
        runs = [(a, closed(a), math.log2(a + max(-xe, -xo))) for a in astarts]
        mx = max(runs, key=lambda t: t[1])
        capok = all(r[1] <= r[2] + 1e-9 for r in runs)
        print(f"    run cap run<=log2(a+{max(-xe,-xo)}): max branch-run on a-starts = {mx[1]} at a={mx[0]}; cap ok: {capok}")

if __name__ == "__main__":
    MMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 40_000_000
    S13 = "1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA"
    S14 = "1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE"
    for name in ("o13", "o14"):
        check_closed(name, MMAX)
        check_mirror(name)
    print()
    check_onorbit("o13", S13, 2, N)
    check_onorbit("o14", S14, 4, N)
    print("\nFixed-point run closed forms [PROVEN] (2-line proof + exhaustive); a-start recursion + orbit facts [OBSERVED].")
    print("No machine decided. No label upgraded.")
