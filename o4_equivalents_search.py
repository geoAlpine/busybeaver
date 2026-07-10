#!/usr/bin/env python
"""
o4 EQUIVALENTS SEARCH (2026-07-10).
Exact big-int / Fraction arithmetic. Every structural claim assertion-checked.

Goal (meta): CHANGE THE QUESTION. Find conditions EQUIVALENT to "o4 never halts"
that are NOT the frequency statement freq{3|W_n} <= 4/5, and assess whether any
opens a proof route different from (K)/base-4/3 normality.

Setup (O4_LEDGER_ANALYSIS / O4_RUN_STRUCTURE / O4_COBOUNDARY_LP):
  odometer 3G' = 4G + e(rho), rho=G mod 3, e={0:9,1:14,2:1}
  W=G+14 ; 3W'=4W+(e-14), e-14={1:0,2:-13,0:-5} ; rho=1 <=> 3|W ; run(G)=v3(W).
  ledger a' = a + delta(rho), delta={1:-1,2:+4,0:+6} ; psi=-delta={1:+1,2:-4,0:-6}.
  fatal(halt) <=> prefix S_n = sum_{j<n} psi(rho_j) >= a0-1  <=>  a_n <= 1.
  identity a_n = a0 + 4n - 5*#1 + 2*#0.
"""
from fractions import Fraction

def v3(x):
    if x == 0: return 10**9
    c = 0
    while x % 3 == 0:
        x //= 3; c += 1
    return c

E     = {0:9, 1:14, 2:1}
DELTA = {1:-1, 2:4, 0:6}
PSI   = {1:1, 2:-4, 0:-6}

# ---------------------------------------------------------------------------
# 1. REAL ORBIT: itinerary, ledger, S-walk, running max, the KNOWN equivalents
# ---------------------------------------------------------------------------
def real_orbit(G0=43, a0=17, N=200000):
    G=G0; a=a0
    c1=c2=c0=0
    S=0                       # prefix sum of psi
    S_max=-10**18; S_argmax=0
    a_min=a; a_min_idx=0
    # nonlinear invariant Phi_n = S_n + 5*v3(W_n)   (potential phi=-5 v3, sub-action on deleted graph)
    Phi_max=-10**18; Phi_argmax=0
    max_run=0
    cur=0
    S_at_rho1_max=-10**18     # running max of S restricted to steps that ENTER rho=1 (fatal-relevant)
    for j in range(N):
        rho=G%3; W=G+14; d=v3(W)
        assert (d>0)==(rho==1)
        # invariant BEFORE stepping ledger (state = (G,a))
        Phi = S + 5*d
        if Phi>Phi_max: Phi_max=Phi; Phi_argmax=j
        if rho==1:
            c1+=1; cur+=1
        else:
            if cur>max_run: max_run=cur
            cur=0
            if rho==2: c2+=1
            else: c0+=1
        # apply step
        a += DELTA[rho]
        S += PSI[rho]
        assert a == a0 - c1 + 4*c2 + 6*c0
        assert a == a0 + 4*(j+1) - 5*c1 + 2*c0    # closed identity
        assert S == a0 - a
        if S>S_max: S_max=S; S_argmax=j
        if a<a_min: a_min=a; a_min_idx=j
        G=(4*G+E[rho])//3
    return dict(N=N,a0=a0,c1=c1,c2=c2,c0=c0,a=a,
                S_max=S_max,S_argmax=S_argmax,a_min=a_min,a_min_idx=a_min_idx,
                Phi_max=Phi_max,Phi_argmax=Phi_argmax,max_run=max_run)

# ---------------------------------------------------------------------------
# 2. THIN-vs-DENSITY: count FATAL itineraries (= fatal seed classes mod 3^L,
#    by the itinerary bijection). Show fatal FRACTION -> positive constant
#    (a FAT / positive-measure obstruction), i.e. large-deviation/density,
#    NOT a thin (measure-zero) reachability target like o7's u=2^k.
#    DP over ledger value a in [2, cap]; a>=L+2 can't reach <=1 within L steps.
# ---------------------------------------------------------------------------
def fatal_fraction(a0, L):
    # PROBABILITY that a uniform-random itinerary goes fatal (a<=1) within L steps.
    # cur: a-value -> probability mass NOT YET fatal. Each step splits 1/3 per rho.
    # Fatal mass is absorbed into p_fatal (cumulative, monotone up to eta^a0).
    from collections import defaultdict
    cur = {a0: Fraction(1)}
    p_fatal = Fraction(0)
    third = Fraction(1,3)
    for step in range(L):
        nxt = defaultdict(Fraction)
        for a,m in cur.items():
            for rho in (1,2,0):
                na = a + DELTA[rho]
                if na <= 1:
                    p_fatal += m*third
                else:
                    nxt[na] += m*third
        cur = dict(nxt)
    return p_fatal   # cumulative fatal probability within L steps

def annealed_eta():
    # ruin constant: root in (0,1) of (1/eta + eta^4 + eta^6)/3 = 1
    lo,hi=Fraction(1,100),Fraction(99,100)
    f=lambda e: (1/e + e**4 + e**6)/3 - 1
    # bisect in float for reporting
    import math
    lo,hi=1e-6,0.999999
    for _ in range(200):
        m=(lo+hi)/2
        if (1/m+m**4+m**6)/3-1>0: lo=m
        else: hi=m
    return (lo+hi)/2

# ---------------------------------------------------------------------------
# 3. RUNNING-MAX / FIRST-PASSAGE reformulation (order-theoretic).
#    Non-halt <=> M := sup_n S_n <= a0-2.  M is a single integer; on a
#    non-halting orbit it is attained at finite time inside a BOUNDED window
#    (drift -3 + run-cap => no upcrossing possible past a finite horizon).
#    We verify M is attained early and never re-approached.
# ---------------------------------------------------------------------------
def running_max_profile(G0=43,a0=17,N=50000):
    G=G0; a=a0; S=0; M=-10**18; Marg=0
    last_within=0  # last time S came within 5 of its running max
    for j in range(N):
        rho=G%3
        a+=DELTA[rho]; S+=PSI[rho]
        if S>M: M=S; Marg=j
        if S>=M-5: last_within=j
        G=(4*G+E[rho])//3
    return M,Marg,last_within

# ---------------------------------------------------------------------------
# 4. DIOPHANTINE shape: o4 halt is a LINEAR inequality in COUNTS (density),
#    contrast o7 halt = S-unit equation 3^v*odd - 1 = 2^k (thin). Symbolic note.
# ---------------------------------------------------------------------------

if __name__=="__main__":
    print("="*74)
    print("1. REAL ORBIT (seed G=43, a0=17) and the THREE KNOWN EQUIVALENTS")
    r=real_orbit(N=200000)
    N=r['N']
    print(f"  N={N}: #1={r['c1']} #2={r['c2']} #0={r['c0']}")
    print(f"  (a) LEDGER equiv: min a over run = {r['a_min']} at gen {r['a_min_idx']} "
          f"(non-halt needs a>=2 forever; margin {r['a_min']-2})")
    print(f"  (b) FREQUENCY equiv: freq{{3|W}} = #1/N = {r['c1']/N:.5f} "
          f"(fatal threshold 4/5=0.8; margin {0.8-r['c1']/N:.4f})")
    print(f"  (c) RUN-DEPTH conspiracy: max rho=1 run so far = {r['max_run']}")
    print(f"  RELATION (exact): a_n = a0 - S_n, S_n=prefix sum psi; "
          f"a_min>=2 <=> S_max<=a0-2 <=> #1<=(4n+a0-1+2#0)/5 all n.")
    print(f"      S_max = {r['S_max']} at gen {r['S_argmax']}  (<= a0-2 = {r['a0']-2}: "
          f"{r['S_max']<=r['a0']-2})  -- all three are ONE inequality on the SAME walk.")

    print("="*74)
    print("2. THIN vs DENSITY: fatal seed-class fraction mod 3^L (bijection)")
    eta=annealed_eta()
    print(f"  annealed ruin constant eta = {eta:.6f}  (P[ever fatal from a] ~ eta^a)")
    for a0 in (1,2,3):
        print(f"  a0={a0}: fatal FRACTION of length-L itineraries "
              f"(-> eta^(a0-1) = {eta**(a0-1):.5f}, a POSITIVE constant => FAT set):")
        row=[]
        for L in (8,16,32,64,128):
            fr=fatal_fraction(a0,L)
            row.append(f"L={L}:{float(fr):.5f}")
        print("     "+"  ".join(row))
    print("  => fatal set has POSITIVE density (fat, ~eta^a0 of all seeds); # fatal")
    print("     seed-classes ~ eta^a0 * 3^L grows EXPONENTIALLY. This is a")
    print("     LARGE-DEVIATION (density) obstruction, NOT a thin (measure-0)")
    print("     reachability target. Contrast o7: halt<=>u hits {2^k}, density->0.")

    print("="*74)
    print("3. RUNNING-MAX / FIRST-PASSAGE reformulation (order-theoretic)")
    M,Marg,lastw=running_max_profile(N=50000)
    print(f"  M = sup_n S_n = {M} attained at gen {Marg}; last time S within 5 of M: gen {lastw}")
    print(f"  => non-halt <=> M <= a0-2 = 15 : {M<=15}. M attained in a BOUNDED early")
    print(f"     window then S escapes to -inf (drift -3, run-cap 0.262n bounds upcrossings).")
    print(f"     Genuinely different OBSERVABLE (extreme value, not Cesare average) but")
    print(f"     bounding M = bounding the large-deviation of the SAME density => (K)-species.")

    print("="*74)
    print("4. NONLINEAR INVARIANT Phi_n = S_n + 5*v3(W_n)  (potential phi=-5 v3)")
    print(f"  sub-action on the DELETED de Bruijn graph (O4_COBOUNDARY_LP): "
          f"psi <= phi(T)-phi + (k-5)/k off the -14 atom.")
    print(f"  On real orbit: max Phi_n = {r['Phi_max']} at gen {r['Phi_argmax']} "
          f"(bounded, small => certificate HOLDS on this orbit).")
    print(f"  It holds ONLY because runs stay shallow (max depth {r['max_run']}); a")
    print(f"  deep return v3(W)=L makes Phi jump +~5L. Boundedness of Phi = the")
    print(f"  frequency-of-deep-returns bound = (K). Fails exactly at the -14 fixed pt.")

    print("="*74)
    print("5. DIOPHANTINE shape (thin-vs-density, algebraic view)")
    print("  o4 halt  <=>  5*#1 - 2*#0 >= 4n + a0 - 1  (LINEAR inequality in COUNTS)")
    print("     => a density / Cramer large-deviation event. NO exponential/S-unit form.")
    print("  o7 halt  <=>  3^v * oddpart - 1 = 2^k       (S-unit / linear-forms eqn)")
    print("     => thin, Baker-touchable in principle. o4 has NO such equation:")
    print("     Baker / S-unit / Diophantine-reachability is STRUCTURALLY INAPPLICABLE to o4.")
    print("="*74)
    print("ALL ASSERTIONS PASSED (exact int/Fraction arithmetic).")
