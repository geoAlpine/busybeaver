#!/usr/bin/env python3
"""
o17 core (k=0 mod3) deep-dive — the free-running least-significant counter
(2026-07-03).  [OBSERVED, exact TM simulation; halting NOT decided.]

Deepens O17_CORE_TRANSDUCER.md by identifying the SINGLE mechanism behind BOTH
the "unbounded interior digits" and the "polynomial growth" obstructions of
O17_LINEAR_PROVEN.md §6.

The atomic step of the carry cascade is a RIGHT-END INCREMENT (an (E,0) reversal at
the right frontier).  Counting these ticks n=1,2,3,..., the least-significant digit
of the base-3 digit string equals the tick index up to a seed-dependent constant:

        max_digit(n)  =  n - c(L)        [OBSERVED, exact, constant c(L)]

i.e. the bottom digit is a FREE-RUNNING COUNTER = the bounce index itself.  This
one fact yields, with 0 fitting freedom:
    * width(n)  =  3n + O(1)      -> LINEAR SPACE   (the digit string is ~3n cells)
    * step(n)   ~  c2 * n^2       -> QUADRATIC TIME (each tick sweeps ~width cells)
    => width ~ step^(1/2)  (the proven growth of o17_core_growth.py), AND
    => the digits are UNBOUNDED because the bottom counter n grows without bound.
So the two separate [OBSERVED] obstructions are ONE mechanism.

SCOPE: this explains GROWTH and UNBOUNDEDNESS, not halting.  The counter is
free-running; halting is governed by whether/when a left-propagating carry reaches
the left frontier in the D-parity (state D at the gate), which depends on the full
carry history = the Collatz-hard part.  Halting stays [OPEN].  No machine decided.
"""
import math

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if (t[0] == '-' or t[2] == 'Z')
                        else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

M = parse("1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB")


def blocks(tape, lo, hi):
    r = []; i = lo
    while i <= hi:
        s = tape[i]; j = i
        while j <= hi and tape[j] == s: j += 1
        r.append((s, j - i)); i = j
    while r and r[0][0] == 0: r = r[1:]
    while r and r[-1][0] == 0: r = r[:-1]
    return [n for s, n in r if s == 1]


def ticks(L, maxsteps):
    """Return list of (step, width, max_digit) at each right-end increment tick."""
    SZ = 1 << 21
    tape = bytearray(SZ); off = SZ // 2
    for i in range(1, L + 1): tape[off + i] = 1
    pos = off; st = 0; step = 0; lo = hi = pos; prevdir = 0
    out = []
    while step < maxsteps:
        r = tape[pos]
        if st == 5 and r == 0: break
        ww, d, ns = M[st][r]
        if st == 4 and r == 0 and prevdir == -1 and d == 1 and pos >= hi - 3:
            blk = blocks(tape, lo, hi)
            mx = max([(x - 2)//3 for x in blk[1:] if x % 3 == 2] + [0]) if blk else 0
            out.append((step, hi - lo + 1, mx))
        prevdir = d
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    return out


if __name__ == "__main__":
    print("seed  ticks   max_digit=n-c?      width/n   step/n^2   width~n^a  step~n^b")
    allok = True
    for L in (9, 18, 27, 24, 33):
        g = ticks(L, 8_000_000)
        n = len(g) - 1
        if n < 400:
            print(f"L={L:3d}  {n:>5}   (halted/short — skipped)")
            continue
        # c(L) = n - max_digit, check constant over the last ~half of the run
        ks = list(range(n // 2, n, max(1, n // 12)))
        cs = sorted(set(k - g[k][2] for k in ks))
        const = (len(cs) == 1)
        allok &= const
        wn = g[-1][1] / n
        sn2 = g[-1][0] / n**2
        # exponents on the tail
        tail = list(range(n // 3, n))
        def fit(y):
            lx = [math.log(k) for k in tail]; ly = [math.log(y[k]) for k in tail]
            m = len(lx); mx = sum(lx)/m; my = sum(ly)/m
            return sum((lx[i]-mx)*(ly[i]-my) for i in range(m))/sum((lx[i]-mx)**2 for i in range(m))
        Wser = {k: g[k][1] for k in tail}; Sser = {k: g[k][0] for k in tail}
        print(f"L={L:3d}  {n:>5}   c={cs if const else cs}({'const' if const else 'VARIES'})"
              f"    {wn:>5.2f}    {sn2:>6.2f}     {fit(Wser):.3f}      {fit(Sser):.3f}")
    print()
    print(f"max_digit = n - c(L) exactly constant on all long seeds: {allok}")
    print("=> LSB is a free-running counter; width~3n (linear space), step~n^2 (quad time);")
    print("   unbounded digits + polynomial growth are the SAME mechanism.  Halting [OPEN].")
