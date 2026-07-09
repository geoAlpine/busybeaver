#!/usr/bin/env python3
"""
SPACE NEEDLE -- TRANSCENDENCE / HITTING-PROBLEM attack, core measurement.

Residual halt target (n>7): m_n = 2^k - 1 (all-ones). HALT <=> m_n + 1 = 2^k.
Equivalently oddpart(m_n + 1) = 1.

KEY IDENTITY (proved below in comments, verified in-code):
  For odd m with v trailing 1-bits, adding 1 clears those v ones and carries,
  so v2(m+1) = v EXACTLY, and
        oddpart(m+1) = (m+1) >> v.
  This = 1  iff  m = 2^v - 1 (all ones)  iff  HALT.
For even m, m+1 is odd so oddpart(m+1) = m+1 (huge; never 1 unless m=0).

So the whole hitting problem is: does  g_n := oddpart(m_n + 1)  ever equal 1?
This script computes g_n exactly (big-int) over the real orbit and reports its
statistics -- in particular the MINIMUM and whether it is bounded away from 1.
"""
import sys

def tz1(m):
    v = 0
    while m & 1:
        v += 1; m >>= 1
    return v

def f(m):
    v = tz1(m)
    return m + 3 * (m >> (v + 1)) + v

def oddpart(x):
    # returns (odd part, v2)
    v = 0
    while x and (x & 1) == 0:
        v += 1; x >>= 1
    return x, v

if __name__ == "__main__":
    GENS = int(sys.argv[1]) if len(sys.argv) > 1 else 20000

    m = 2
    orbit_g = []          # (n, m_odd?, g_n = oddpart(m_n+1), v)
    min_g_odd = None; argmin = None
    n_odd = 0
    # verify the v2(m+1)=v identity along the way
    ident_ok = 0; ident_tot = 0
    small_min = []        # track the smallest g over odd steps

    for n in range(GENS + 1):
        v = tz1(m)
        g, v2 = oddpart(m + 1)
        if m & 1:  # odd milestone -- the only ones that can be all-ones
            n_odd += 1
            ident_tot += 1
            if v2 == v:
                ident_ok += 1
            if min_g_odd is None or g < min_g_odd:
                min_g_odd = g; argmin = (n, m, g, v)
        else:
            # even m: m+1 odd, g = m+1, v2 = 0; identity trivially about odd only
            pass
        if m & 1:
            small_min.append((g, n, v))
        m = f(m)

    print(f"[orbit] {GENS} generations; final width = {m.bit_length()} bits")
    print(f"[parity] odd milestones among first {GENS+1}: {n_odd} "
          f"({100*n_odd/(GENS+1):.1f}%)")
    print(f"[identity v2(m+1)=v on odd m] {ident_ok}/{ident_tot} EXACT "
          f"(=> oddpart(m+1)=(m+1)>>v; g=1 iff all-ones)")
    print(f"[MIN oddpart(m_n+1) over ODD milestones] = {min_g_odd}")
    print(f"   attained at n={argmin[0]}, m={argmin[1] if argmin[1]<10**9 else str(argmin[1])[:20]+'...'}, "
          f"bitlen(m)={argmin[1].bit_length()}, v={argmin[3]}")
    print(f"   => g_n = 1 (HALT) occurs on the orbit? {'YES' if min_g_odd == 1 else 'NO'}")

    # smallest 12 g-values over the whole odd-orbit
    small_min.sort()
    print("\n[smallest 12 oddpart(m_n+1) over odd milestones]  (g, gen n, v=trailing-ones):")
    for g, n, v in small_min[:12]:
        print(f"   g={g:<24d} n={n:<6d} v={v}")
