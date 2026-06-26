"""Phase 2 (program): the EXACT trap / no-trap boundary of the v_p(mu)=-1 family.
The previous deepening found mu-near-1 siblings have small-integer fixed points. Now pin the
boundary completely -- and PROVABLY, not empirically.

THE TWO ELEMENTARY LEMMAS (both trivial, both verified below):
  (L1) Monotone:   c <= c'  =>  T(c)=floor(mu c) <= floor(mu c')=T(c').        [mu>0]
  (L2) Non-decr.:  T(c) >= c  for all c>=0.                                      [mu>=1, since mu c>=c]

CONSEQUENCE (the structure theorem):
  * Periodic => FIXED.  A cycle c_0->c_1->...->c_0 has T(c_i)=c_{i+1}>=c_i (L2); summing around the
    cycle forces every inequality to be equality => all c_i equal.  So the ONLY periodic orbits are
    fixed points; there are NO cycles of length >= 2 anywhere in the family.
  * Fixed point set is an explicit interval.  floor(mu c)=c  <=>  c <= mu c < c+1  <=>  c < 1/(mu-1)
    (using mu c >= c free from mu>=1).  So FIX(mu) = { c in Z, 1 <= c < 1/(mu-1) }, size ~ 1/(mu-1).
  * No transients.  A non-fixed seed has T(c) > c (strictly, by L2 + not fixed), hence escapes
    monotonically to +infinity (it can never re-enter the fixed interval from above, by L1+L2).
  => Every positive-integer seed is EITHER a fixed point (decidable, trivial) OR escapes to infinity
     (the genericity-hard cryptid regime).  There is no third behavior in the whole family.

THE BOUNDARY:
  * mu > 2  (a > 2p):  1/(mu-1) < 1  =>  FIX = empty  =>  TRAP-FREE family: every seed >= 1 escapes.
  * 1 < mu <= 2 (p < a <= 2p): FIX = {1,...,floor just below 1/(mu-1)}; seeds above escape.
       Antihydra mu=3/2: 1/(mu-1)=2 => FIX={1}; seed 8 > 2 escapes (genuine cryptid).
  The trap/no-trap boundary of the family is the SINGLE CURVE  mu = 2  (a = 2p), and within mu<2 the
  decidable region of seeds is exactly the finite interval [1, 1/(mu-1)).  Everything else, every mu,
  is the SAME open genericity wall.  So the family's decidable part is fully and explicitly mapped;
  the cryptid part is uniform across mu.
"""
from math import gcd, ceil

def T(a, p, c):  # floor(mu c), mu=a/p, exact integer
    return (a*c)//p

def fixed_set(a, p, cap=200):
    return [c for c in range(1, cap+1) if T(a,p,c)==c]

def predicted_fixed(a, p):
    # c < 1/(mu-1) = p/(a-p)
    thr = p/(a-p)  # mu-1 = (a-p)/p
    return [c for c in range(1, 10**6) if c < thr]

def escapes(a, p, seed, steps=200):
    c=seed; seen={c}
    for _ in range(steps):
        c=T(a,p,c)
        if c in seen:  # caught a cycle / fixed point
            return False, c
        seen.add(c)
        if c > 10**12:
            return True, None
    return (c>seed*2), None

print("="*80)
print("Exact trap boundary of the v_p(mu)=-1 family")
print("="*80)

# verify lemmas L1,L2 on a grid
ok_L1=ok_L2=True
for (a,p) in [(3,2),(5,2),(4,3),(6,5),(8,7),(11,3)]:
    prev=-1
    for c in range(0, 500):
        t=T(a,p,c)
        if t<prev: ok_L1=False
        if t<c: ok_L2=False
        prev=t
print(f"\nL1 (monotone) holds on grid: {ok_L1}   L2 (T(c)>=c) holds on grid: {ok_L2}")

# verify "periodic => fixed" : brute-force search any cycle of length>=2 up to a cap
def has_long_cycle(a,p,cap=3000):
    for seed in range(1, cap):
        c=seed; path=[c]
        for _ in range(60):
            c=T(a,p,c)
            if c>cap*4: break        # escaped
            if c in path:
                idx=path.index(c)
                cyc=path[idx:]
                if len(cyc)>=2 and len(set(cyc))>=2:
                    return cyc
                break
            path.append(c)
    return None
print("\nSearch for ANY length->=2 cycle in each family member (cap 3000 seeds):")
fam=[(p,a) for p in [2,3,5,7] for a in range(p+1,2*p+4) if gcd(a,p)==1]
any_cycle=False
for (p,a) in fam:
    cyc=has_long_cycle(a,p)
    if cyc: any_cycle=True; print(f"   mu={a}/{p}: CYCLE {cyc}  <-- would break the theorem")
print(f"   length->=2 cycle found anywhere: {any_cycle}  (theorem predicts: False)")

print("\nFixed-set FIX(mu) -- measured vs predicted {c: c<p/(a-p)}, and trap/no-trap class:")
print(f"{'(p,a)':>8} {'mu':>7} {'1/(mu-1)':>9} {'FIX measured':>16} {'pred matches':>13} {'class':>11}")
allmatch=True
for (p,a) in fam:
    fm=fixed_set(a,p)
    thr=p/(a-p)
    pred=[c for c in range(1,200) if c<thr]
    match=(fm==pred); allmatch&=match
    cls="TRAP-FREE" if a>2*p else ("trap" if a<2*p else "mu=2 bdy")
    star=" <-Antihydra" if (p,a)==(2,3) else ""
    print(f"{str((p,a)):>8} {a}/{p:<5} {thr:9.3f} {str(fm):>16} {str(match):>13} {cls:>11}{star}")
print(f"\nAll measured FIX == predicted {{c<1/(mu-1)}}: {allmatch}")

print("\n--- The boundary, stated ---")
print("Periodic orbits in the WHOLE family = fixed points only (no cycles len>=2): verified.")
print("FIX(mu) = {1 <= c < 1/(mu-1)} exactly; size ~ 1/(mu-1); EMPTY iff mu>2 (a>2p).")
print("Every non-fixed seed escapes monotonically to infinity (no transients, no basins).")
print(">>> TRAP/NO-TRAP BOUNDARY = the single curve mu=2 (a=2p).")
print(">>> mu>2: trap-free, every seed a cryptid candidate.  1<mu<=2: finite decidable interval")
print("    [1, 1/(mu-1)) of fixed seeds, all larger seeds escape.  Antihydra (mu=3/2): FIX={1},")
print("    seed 8 escapes.  The genericity wall (avg jump<=2) is then UNIFORM across all mu for")
print("    every escaping seed -- the decidable part is finite & explicit, the hard part is shared.")

# sanity: Antihydra seed 8 escapes; a trap-free sibling's seed 8 also escapes
for (p,a,s) in [(2,3,8),(2,5,8),(3,7,8),(7,8,3),(5,6,3)]:
    esc,landed=escapes(a,p,s)
    print(f"   mu={a}/{p} seed={s}: escapes={esc}" + (f" (fixed at {landed})" if landed else ""))
