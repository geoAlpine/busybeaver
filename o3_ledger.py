#!/usr/bin/env python3
"""
o3 LEDGER (2026-07-06) -- the derived deterministic counter system, iterated far.
From the verified generation laws (o3_gen_proof.py; exact on the grids):
  k>=2:  a%3==1: (a-1, k+2)   a%3==2: ((4a+4)/3, k+1)   a%3==0: (4a/3+3, k-1)
  k==1:  a%3==1: (a-1, 3)     a%3==2: ((4a+4)/3, 2)
         a%9==3: (4a/3+2, 2)  a%9==0: (4a/3+3, 1)       a%9==6: HALT
  k==0:  a%3==0: (a, 1)       a%3==1: (a-1, 2)          a%3==2: HALT
Real blank-tape orbit joins at (a,k)=(6,2) (verified concretely).
This script: (1) checks the iteration against the concretely observed orbit,
(2) iterates the exact map far, tracking min-k at drain events and fatal hits.
All arithmetic exact (bigint). [The map itself is the PROVEN/grid-verified law;
its long-range iteration is exact arithmetic, not simulation.]
"""
OBSERVED=[(6,2),(11,1),(16,2),(15,4),(23,3),(32,4),(44,5),(60,6),(83,5),(112,6),
          (111,8),(151,7),(150,9),(203,8),(272,9),(364,10),(363,12),(487,11),
          (486,13),(651,12),(871,11),(870,13),(1163,12),(1552,13),(1551,15),
          (2071,14),(2070,16),(2763,15),(3687,14),(4919,13)]

def step(a,k):
    r=a%3
    if k>=2:
        if r==1: return (a-1,k+2)
        if r==2: return ((4*a+4)//3,k+1)
        return (4*a//3+3,k-1)
    if k==1:
        if r==1: return (a-1,3)
        if r==2: return ((4*a+4)//3,2)
        r9=a%9
        if r9==3: return (4*a//3+2,2)
        if r9==0: return (4*a//3+3,1)
        return None  # HALT
    # k==0
    if r==0: return (a,1)
    if r==1: return (a-1,2)
    return None  # HALT

if __name__=='__main__':
    import sys
    sys.set_int_max_str_digits(100_000_000)
    # (1) match observed real orbit
    a,k=6,2; ok=True
    for i,(ea,ek) in enumerate(OBSERVED):
        if (a,k)!=(ea,ek):
            ok=False; print(f"MISMATCH at index {i}: computed {(a,k)} observed {(ea,ek)}"); break
        n=step(a,k)
        if n is None: print("unexpected HALT"); ok=False; break
        a,k=n
    print(f"arithmetic orbit matches ALL {len(OBSERVED)} concretely observed generations: {ok}")
    # (2) iterate far
    import time
    a,k=6,2
    mink_at_drain=(10**9,None)   # min k seen AT an a%3==0 event (before drain)
    mink=(10**9,None)
    t0=time.time(); i=0
    N=200_000
    kmin_recent=[]
    while i<N:
        if k<mink[0]: mink=(k,i)
        if a%3==0 and k<mink_at_drain[0]: mink_at_drain=(k,i)
        n=step(a,k)
        if n is None:
            print(f"FATAL HIT at generation {i}: (a digits={len(str(a))}, k={k}, a%9={a%9})")
            break
        a,k=n; i+=1
        if i in (30,100,300,1000,3000,10000,30000,100000,200000) :
            print(f"  gen {i:>7,}: k={k:>8,}  a has {len(str(a))} digits  ({time.time()-t0:.1f}s)")
    else:
        print(f"NO fatal hit in {N:,} generations.")
    print(f"min k over run: {mink[0]} at gen {mink[1]}")
    print(f"min k at a%3==0 (drain) events: {mink_at_drain[0]} at gen {mink_at_drain[1]}")
    print("Fatal set: (k=1 & a%9==6) or (k=0 & a%3==2); k=0/1 only reachable via drains at a%3==0.")
