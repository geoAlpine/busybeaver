#!/usr/bin/env python3
# Uniform reload-map build & verification for the whole {2,3}-smooth BB(6) cryptid family.
# Interpreter: /Users/aokiyousuke/quantum-ecc/.venv/bin/python  (exact big-int throughout)
#
# UNIFORM RELOAD MAP (derived, PAPER_MIRROR_LADDER uniform fixed-point thm):
#   Each branch map b(v) = (p v + e)/q has integer fixed point x = -e/(p-q).
#   Run i: entry v_i, branch b_i, depth d_i = v_q(v_i - x_{b_i}).
#   Reload unit w_i = (v_i - x_{b_i}) / q^{d_i}  (a q-adic UNIT, gcd(w_i,q)=1).
#   Exit = x_{b_i} + p^{d_i} w_i  = v_{i+1} (entry of next run).
#   => d_{i+1} = v_q( p^{d_i} w_i + Δ_i ),  Δ_i = x_{b_i} - x_{b_{i+1}}   (offset between fixed points)
#      w_{i+1} = ( p^{d_i} w_i + Δ_i ) / q^{d_{i+1}}
# This file DERIVES nothing new by fiat; it VERIFIES the identity on each machine's real orbit.

import sys, random

def vq(n, q):
    if n == 0: return None
    k = 0
    while n % q == 0:
        n //= q; k += 1
    return k

def unit(n, q):        # remove all factors of q, return the q-unit part (as signed int)
    if n == 0: return None
    while n % q == 0: n //= q
    return n

# ---------------------------------------------------------------------------
# Machine registry.  Each machine = (p, q, step(v), branch(v), x[branch]).
#   step: exact integer value map T(v)
#   branch: label of the branch v is in
#   xfix: dict branch-label -> integer fixed point
# All maps are the milestone/inner-engine value maps from the campaign notes.
# ---------------------------------------------------------------------------

def make_pq2(ce, co):
    # generic x3/2 two-branch: T(even)=3v/2+ce, T(odd)=(3v-1)/2+co
    xe = -2*ce; xo = 1-2*co
    def step(v): return (3*v)//2 + ce if v%2==0 else (3*v-1)//2 + co
    def branch(v): return v%2
    return dict(p=3,q=2,step=step,branch=branch,xfix={0:xe,1:xo})

def make_o2():
    # ceiling x3/2: T(even)=3v/2, T(odd)=(3v+1)/2 ; xe=0, xo=-1
    def step(v): return (3*v)//2 if v%2==0 else (3*v+1)//2
    def branch(v): return v%2
    return dict(p=3,q=2,step=step,branch=branch,xfix={0:0,1:-1})

def make_o4():
    # x4/3 three-branch: G' = (4G + e(rho))/3, e={0:9,1:14,2:1}; x_rho = -e(rho)
    E = {0:9,1:14,2:1}
    def step(G): return (4*G + E[G%3])//3
    def branch(G): return G%3
    return dict(p=4,q=3,step=step,branch=branch,xfix={0:-9,1:-14,2:-1})

def make_o15_ideal():
    # IDEALIZED x8/3 three-branch (single-digit corrections; real o15 branching is queue-dependent,
    # O15 note s6 -- this is a MODEL of the depth/reload process, not the machine's full itinerary).
    # rho=0: V'=(8V+9)/3  x=-9/5 -> integer? no. Use integer-fixed queued branch mirror instead:
    # We use the three branches that keep V integer with integer fixed points where available.
    # Cleanest integer-fixed family: use c={0:9,2:11,1:-5}; x_rho=-c/5 (in Z_3).  Runs = v3(5V+c).
    C = {0:9,2:11,1:-5}
    def step(V): return (8*V + C[V%3])//3
    def branch(V): return V%3
    # integer? 8V+C ≡ 0 mod 3: 8V≡2V, C: 9≡0,11≡2,-5≡1 ; 2V+C mod3: V=0:0,V=2:2*2+2=6≡0,V=1:2+1=0 ok
    # fixed points x=-C/5 are 3-adic (not integer); we track depth via v3(5V+c) equivalently.
    return dict(p=8,q=3,step=step,branch=branch,xfix=None,
                run_of=lambda V: vq(5*V + C[V%3], 3), C=C)

MACHINES = {
    'Antihydra': make_pq2(0,0),          # x3/2, x=(0,1)     Δ=∓1
    'o2(ceil)' : make_o2(),              # x3/2, x=(0,-1)    Δ=±1 (negation-conjugate to AH)
    'o11'      : make_pq2(4,4),          # x3/2, x=(-8,-7)   Δ=∓1
    'o16'      : make_pq2(2,2),          # x3/2, x=(-4,-3)   Δ=∓1
    'o14'      : make_pq2(6,6),          # x3/2, x=(-12,-11) Δ=∓1
    'o13'      : make_pq2(7,4),          # x3/2, x=(-14,-7)  Δ=∓7  <-- the outlier offset
    'o4'       : make_o4(),              # x4/3, ℤ_3^×
}

def collect_runs(M, seed, nsteps):
    """Return list of (branch, depth, entry_value) maximal same-branch runs."""
    step, branch = M['step'], M['branch']
    v = seed
    runs = []
    cur_b = branch(v); L = 1; entry = v
    for _ in range(nsteps):
        v = step(v)
        b = branch(v)
        if b == cur_b:
            L += 1
        else:
            runs.append((cur_b, L, entry))
            cur_b = b; L = 1; entry = v
    runs.append((cur_b, L, entry))
    return runs

def verify_machine(name, M, seed, nsteps):
    p, q = M['p'], M['q']
    runs = collect_runs(M, seed, nsteps)
    xfix = M['xfix']
    mm_runlaw = mm_reload = mm_exit = mm_unit = 0
    n_pairs = 0
    if xfix is None:
        # o15 ideal: run law via run_of only (fixed points not integer)
        run_of = M['run_of']
        for (b, L, e) in runs[:-1]:
            if run_of(e) != L: mm_runlaw += 1
        return dict(name=name, runs=len(runs), mm_runlaw=mm_runlaw,
                    mm_reload=None, mm_exit=None, note='ideal (v3 run law only; xfix∉ℤ)')
    # last run is truncated by NSTEPS (its length is not the true maximal run), so it may serve
    # as a predecessor but never as a target: check pairs with i+1 <= len-2.
    for i in range(len(runs)-2):
        b, L, e = runs[i]
        b2, L2, e2 = runs[i+1]
        x = xfix[b]; x2 = xfix[b2]
        # (1) run law
        if vq(e - x, q) != L: mm_runlaw += 1
        # reload objects
        w = unit(e - x, q)                     # q-unit of (e - x)
        Delta = x - x2
        exit_pred = x + (p**L) * w
        # (2) exit == next entry
        if exit_pred != e2: mm_exit += 1
        # (3) reload depth recursion
        if vq((p**L)*w + Delta, q) != L2: mm_reload += 1
        # (4) reload unit recursion
        w2_pred = unit((p**L)*w + Delta, q)
        w2_actual = unit(e2 - x2, q)
        if w2_pred != w2_actual: mm_unit += 1
        n_pairs += 1
    return dict(name=name, runs=len(runs), pairs=n_pairs, mm_runlaw=mm_runlaw,
                mm_reload=mm_reload, mm_exit=mm_exit, mm_unit=mm_unit)

# choose seeds that stay in-domain and grow (documented inner-engine seeds / valid starts)
SEEDS = {
    'Antihydra': 8, 'o2(ceil)': 7, 'o11': 2, 'o16': 2, 'o14': 5, 'o13': 3, 'o4': 43,
}
NSTEPS = 40000   # x3/2 ~ 1 run / 2 steps => ~2e4 runs (>1e4 target); values ~5000 digits (fast)

print("="*78)
print("PART 1 -- UNIFORM RELOAD MAP: verify d_{i+1}=v_q(p^{d_i} w_i + Δ_i) on real orbits")
print("="*78)
print(f"{'machine':11s} {'(p,q)':7s} {'runs':>7s} {'runlaw':>7s} {'exit':>6s} {'reload':>7s} {'unit':>6s}")
for name, M in MACHINES.items():
    r = verify_machine(name, M, SEEDS[name], NSTEPS)
    print(f"{name:11s} ({M['p']},{M['q']})   {r['runs']:>7d} "
          f"{r['mm_runlaw']:>7d} {r['mm_exit']:>6d} {r['mm_reload']:>7d} {r['mm_unit']:>6d}")

# o15 idealized (separate: v3 run law only, fixed pts not integer)
r15 = verify_machine('o15*ideal', MACHINES_o15 := make_o15_ideal(), 20, 40000)
print(f"{'o15*ideal':11s} (8,3)   {r15['runs']:>7d} {r15['mm_runlaw']:>7d}   -- reload needs queue ({r15['note']})")

print("\nAll mismatch columns should be 0 (runlaw/exit/reload/unit).")

# ---------------------------------------------------------------------------
print("\n"+"="*78)
print("PART 2 -- CLASSIFICATION: offsets, place, cumulative vs resetting")
print("="*78)
print("Offset Δ_{even->odd} = x_even - x_odd  (invariant of the reload map up to shift):")
for name in ['Antihydra','o2(ceil)','o11','o16','o14','o13']:
    M = MACHINES[name]; xe, xo = M['xfix'][0], M['xfix'][1]
    print(f"  {name:11s} x=({xe:+d},{xo:+d})  Δ_eo = {xe-xo:+d}   Δ_oe = {xo-xe:+d}")
print(f"  {'o4':11s} x=(0:{MACHINES['o4']['xfix'][0]},1:{MACHINES['o4']['xfix'][1]},2:{MACHINES['o4']['xfix'][2]})  place ℤ_3^×")
print("""
  => x3/2 Δ=∓1 CLASS {Antihydra,o11,o16,o14}: identical reload map (global shift), place ℤ_2^×.
     o2(ceil) Δ=±1: SAME map up to w->-w (negation) conjugacy on ℤ_2^×.
     o13 Δ=∓7: a DIFFERENT reload map at the same place (branch fixed pts 7 apart, not
               shift/negation-conjugate to Δ=±1).
     o4: place ℤ_3^× -- a different p-adic place entirely.
""")

# ---------------------------------------------------------------------------
print("="*78)
print("PART 3a -- 'SAME MAP, DIFFERENT SEED': the x3/2 Δ=∓1 family is literally ONE map")
print("="*78)
# mirror coordinate: W = v - x_even makes even branch pure ×3/2 and reproduces the STANDARD
# Collatz-x3/2 map even->3W/2, odd->(3W-1)/2 exactly, for every Δ=∓1 machine.
def standard_step(W):  # the canonical ⌊3W/2⌋ engine (Antihydra in W=v)
    return (3*W)//2 if W%2==0 else (3*W-1)//2
for name in ['Antihydra','o11','o16','o14']:
    M = MACHINES[name]; xe = M['xfix'][0]
    v = SEEDS[name]; ok = True
    for _ in range(3000):
        W = v - xe
        if standard_step(W) != M['step'](v) - xe:  # mirror step matches standard
            ok = False; break
        v = M['step'](v)
    print(f"  {name:11s}: mirror W=v-({xe}) obeys standard ⌊3W/2⌋ engine  -> {'IDENTICAL (0 mismatch/3000)' if ok else 'DIFFERS'}")
print("  => Antihydra/o11/o16/o14 are the SAME dynamical system on different seeds W0.")
# show o13 is NOT: no global shift s makes both branches standard (offset 7 != 1)
print("  o13: branch-fixed-point gap = 7 (invariant under any shift) != 1 => NOT the standard map.")

print("\n"+"="*78)
print("PART 3b -- CROSS-MACHINE TRANSFER TEST: does one orbit's reload-unit equidistribution")
print("          imply another's? (same map, different seed; and different places)")
print("="*78)
# Take Antihydra map on two different seeds -> two reload-unit sequences in ℤ_2^×.
# If a bound transferred, the residue sequences (w_i mod 2^k) would be functionally related.
# Measure correlation of (w_i mod 2^k) between the two orbits.
def reload_unit_seq(step_fn, xe_dict, branch_fn, q, seed, nseeds_runs):
    # returns list of q-units w_i for maximal runs
    runs = []
    v = seed; cur_b = branch_fn(v); L=1; entry=v; steps=0
    seq=[]
    while len(seq) < nseeds_runs and steps < 4_000_000:
        v = step_fn(v); steps+=1
        b = branch_fn(v)
        if b==cur_b: L+=1
        else:
            x = xe_dict[cur_b]
            seq.append(unit(entry - x, q) % (2**16))   # q-unit residue mod 2^16
            cur_b=b; L=1; entry=v
    return seq

AH = MACHINES['Antihydra']
seqA = reload_unit_seq(AH['step'], AH['xfix'], AH['branch'], 2, 8,   9000)
seqB = reload_unit_seq(AH['step'], AH['xfix'], AH['branch'], 2, 100, 9000)  # different seed, SAME map
n = min(len(seqA), len(seqB))
# correlation of low bit (w_i mod 4) across the two independent seeds
def corr_bits(a, b, mod):
    a=[x%mod for x in a[:n]]; b=[x%mod for x in b[:n]]
    ma=sum(a)/n; mb=sum(b)/n
    num=sum((a[i]-ma)*(b[i]-mb) for i in range(n))
    da=(sum((x-ma)**2 for x in a))**.5; db=(sum((x-mb)**2 for x in b))**.5
    return num/(da*db) if da*db>0 else 0.0
for mod in (4,8,16):
    print(f"  Antihydra-map seed8 vs seed100, corr(w_i mod {mod:2d}) = {corr_bits(seqA,seqB,mod):+.4f}")
print("  => ~0: the SAME map on two seeds gives statistically unrelated reload-unit sequences.")
print("     Single-orbit equidistribution is PER-SEED; identity of the map transfers NO bound.")

# place mismatch: Antihydra depths (v2) vs o4 depths (v3) -- different p-adic character, no ring map
O4 = MACHINES['o4']
d_ah = [L for (_,L,_) in collect_runs(AH, 8, 40000)][:15]
d_o4 = [L for (_,L,_) in collect_runs(O4, 43, 40000)][:15]
print(f"\n  Antihydra depth seq (v2): {d_ah}")
print(f"  o4        depth seq (v3): {d_o4}")
print("  => reload maps live in ℤ_2^× vs ℤ_3^×; no continuous ring map ℤ_2->ℤ_3 => no reduction.")

# ---------------------------------------------------------------------------
print("\n"+"="*78)
print("PART 4 -- annealed model: resetting (sparse-sampled) units look i.i.d.; cumulative correlate")
print("="*78)
# cumulative (Antihydra): consecutive w_i are the deterministic recursion -> low but nonzero structure
# resetting sea (o11): decisive draws are T^{e_n}(2) at doubly-exp-sparse e_n -> decorrelated samples.
def lag1_autocorr_lowbit(seq, mod):
    a=[x%mod for x in seq]; m=sum(a)/len(a); N=len(a)
    num=sum((a[i]-m)*(a[i+1]-m) for i in range(N-1)); den=sum((x-m)**2 for x in a)
    return num/den if den>0 else 0.0
print(f"  Antihydra (cumulative) lag-1 autocorr of (w_i mod 4): {lag1_autocorr_lowbit(seqA,4):+.4f}")
# o11 sea sampled at sparse indices e_n ~ (3/4)T^{e_{n-1}}(2): approximate by wide stride on T^i(2)
def o11_sea(N, stride):
    m=2; samples=[]; i=0
    while len(samples)<N and i< 3_000_000:
        m = (3*m)//2 + 4 if m%2==0 else (3*m+7)//2
        i+=1
        if i % stride == 0: samples.append((m+8) % (2**16))   # W=m+8 unit residue
    return samples
sea = o11_sea(4000, 20)   # sparse stride mimics self-determined sampling (values kept modest)
print(f"  o11 sea sampled@stride20 lag-1 autocorr of (W mod 4): {lag1_autocorr_lowbit(sea,4):+.4f}")
print("  Both ~0 numerically; but 'i.i.d.-ness' of the sampled residues IS the per-orbit")
print("  equidistribution = (K). The resetting/annealed model is a MODEL, not a theorem.")

print("\nDONE. No machine decided. No label upgraded.")
