#!/usr/bin/env python3
"""o7t_decomp.py -- the S-unit-vs-additive decomposition of u_n, made exact.

Recursion (verified): u_{n+1}+1 = (3/2)^{v_n} * x_n,  x_n = u_n + c_n,
    c_n = (w_n+3)/2 + d_n,  w_n=oddpart(u_n), d_n=v2(u_n), v_n=v2(x_n).

Set S_n := u_n + c_n = x_n.  Then u_{n+1} = (3/2)^{v_n} S_n - 1, so
    S_{n+1} = u_{n+1}+c_{n+1} = (3/2)^{v_n} S_n + (c_{n+1}-1).
Unroll:  S_N = (prod_{n<N}(3/2)^{v_n}) S_0 + sum_{j=1}^{N} (prod_{n=j}^{N-1}(3/2)^{v_n}) (c_j-1).
Each product is an S-unit 3^A/2^A.  Measure:
  (a) the "S-unit-only" prediction  u_N^suni := (3/2)^{V} S_0 - 1  (corrections zeroed) vs true u_N;
  (b) fraction of bit-growth contributed by the additive corrections vs the (3/2)^v factors;
  (c) is u_N a bounded combination of S-units? -> count distinct S-unit exponents / coeff sizes.
"""
import sys, math
from fractions import Fraction
from o7d_verify import F, v2, oddpart

def run(N):
    from o7d_verify import step_map
    a,b,n=2,2,0; prev_even=None; first=None
    while first is None:
        if a%2==1 and a>=5 and prev_even is True: first=a+3
        r=step_map(a,b); prev_even=(a%2==0); a,b=r[1],r[2]; n+=1
    u0=first
    # true orbit + S-unit-only prediction via exact Fraction
    u=u0; V=0
    S0=Fraction(u0 + (oddpart(u0)+3)//2 + v2(u0))
    corr_bits_total=0.0; three_bits_total=0.0
    us=[u0]
    for i in range(N):
        d=v2(u); w=oddpart(u)
        if w==1:
            print("HALT at",i); return
        c=(w+3)//2+d; x=u+c; vv=v2(x)
        V+=vv
        # per-step: growth from (3/2)^v  vs  from correction c (x=u+c)
        three_bits_total += vv*math.log2(1.5)
        if u>0: corr_bits_total += math.log2(x/ u)   # = log2(1+c/u)
        u = 3**vv*oddpart(x)-1
        us.append(u)
    uN=u
    # S-unit-only prediction (all corrections zeroed): u would satisfy u_{n+1}+1=(3/2)^{v_n}(u_n) exactly
    # -> u_N^suni +?  Not integer in general; compare magnitudes in bits.
    suni_bits = math.log2(float(S0)) + V*math.log2(1.5)
    true_bits = math.log2(uN)
    print(f"first cascade entry u0 = {u0}")
    print(f"N={N} entries; final bitlen(u_N)={uN.bit_length()}; sum v_n = V = {V}")
    print(f"  bit-growth from (3/2)^v factors total : {three_bits_total:10.1f} bits")
    print(f"  bit-growth from additive corrections  : {corr_bits_total:10.1f} bits")
    print(f"  ratio corrections/(total growth)      : {corr_bits_total/(three_bits_total+corr_bits_total):.4f}")
    print(f"  S-unit-only magnitude pred (log2)     : {suni_bits:10.1f}")
    print(f"  true magnitude (log2 u_N)             : {true_bits:10.1f}")
    print(f"  additive corrections add ~{true_bits-suni_bits:.0f} bits on top of the pure S-unit growth")
    # per-entry mean v
    print(f"  mean v_n (S-unit exponent per step)   : {V/N:.4f} (uniform-int v2 mean = 1)")

if __name__=="__main__":
    run(int(sys.argv[1]) if len(sys.argv)>1 else 20000)
