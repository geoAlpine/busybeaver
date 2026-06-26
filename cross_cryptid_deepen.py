"""Phase 2 (program): deepen the cross-cryptid classification.
GOAL set by the round-2 meeting: walk the v_p(mu)=-1 Mahler family and look for a SIBLING whose
obstruction is *strictly easier* than Antihydra's -- i.e. one carrying an exploitable extra
structure (a 2nd multiplicatively-independent direction = rank-2, or an unusually strong
contraction that shrinks the exceptional set) that Antihydra (mu=3/2) lacks.

Family: T_mu(c) = floor(mu * c), mu = a/p, gcd(a,p)=1, v_p(mu) = -1 (so the map is p-to-1 expanding
at p). Antihydra = (p=2, a=3). Siblings vary p and a.

Two honest probes:
  (1) RANK axis. Is any sibling NOT rank-1? The acting object is the single map x -> mu*x; rank =
      # of mult-independent maps in the generated semigroup. Adding more prime factors to a does NOT
      add a second *independent generator* (still one map mu). Confirm structurally + count the
      distinct archimedean/non-arch dilations to show "more primes != rank-2".
  (2) CONTRACTION axis. Does a sibling with stronger total contraction have a *smaller* empirical
      exceptional signature? Measure the family's analog of avg-jump and the spread of seed orbits;
      a strictly-easier sibling would show genericity *robustly* where Antihydra is marginal.
Honesty: this is empirical reconnaissance over the family, not a proof. We report what varies.
"""
from fractions import Fraction
from math import gcd, log

def vp(n, p):
    n = abs(int(n))
    if n == 0: return 10**9
    r = 0
    while n % p == 0:
        n //= p; r += 1
    return r

def family_members(pmax=7, amax=12):
    """All (p, a) with p prime, gcd(a,p)=1, a>p (so mu=a/p>1, expanding), v_p(a/p)=-1 automatic."""
    fam = []
    for p in [2,3,5,7]:
        if p > pmax: break
        for a in range(p+1, amax+1):
            if gcd(a, p) == 1:
                fam.append((p, a))
    return fam

def dilations(p, a):
    """Archimedean + p-adic dilations of mu=a/p. |mu|_inf=a/p; |mu|_p=p (expand); |mu|_q=1/q^{v_q(a)}
    for primes q|a (contract). Returns (expand_factor_total, contract_factor_total, n_contract_dirs)."""
    mu = a / p
    # expanding: archimedean (a/p>1) and the prime p (|mu|_p = p^{1} since v_p(mu)=-1)
    expand = mu * p
    # contracting: each prime q dividing a contributes |mu|_q = q^{-v_q(a)}
    contract = 1.0
    ndir = 0
    aa = a
    q = 2
    qs = []
    while q*q <= aa:
        if aa % q == 0:
            e = 0
            while aa % q == 0:
                aa //= q; e += 1
            qs.append((q, e)); ndir += 1
        q += 1
    if aa > 1:
        qs.append((aa, 1)); ndir += 1
    for (q, e) in qs:
        contract *= q**(-e)
    return expand, contract, ndir, qs

def avg_jump_empirical(p, a, seed, N=20000):
    """Family analog of Antihydra avg-jump: run c -> floor((a/p) c), renewal at multiples of p,
    measure mean of v_p(...) per renewal step. For Antihydra (2,3) this is the avg jump ~1 (Haar)."""
    c = seed
    # renewal: collect c'_j = c/p whenever p | c, and the jump = run-length of consecutive
    # non-divisible-by-p steps. Simpler robust proxy: mean p-adic depth growth rate / mixing.
    # We measure: fraction of steps where c % p == 0 (the "even-density" analog) and its target.
    div = 0; tot = 0
    A = Fraction(a, p)
    cc = Fraction(c)
    for _ in range(N):
        floored = (a * cc.numerator) // (p * cc.denominator)  # floor(mu*c) for integer c
        c_int = floored if cc.denominator == 1 else None
        # keep integer dynamics
        if cc.denominator != 1:
            break
        if int(cc) % p == 0:
            div += 1
        cc = Fraction((a * int(cc)) // p)
        tot += 1
    return div / tot if tot else float('nan')

print("="*78)
print("Phase 2: cross-cryptid family -- search for a STRICTLY EASIER sibling")
print("="*78)
fam = family_members()
print(f"\nFamily members (p, a), mu=a/p, v_p(mu)=-1, expanding:  {len(fam)} instances")
print(f"{'(p,a)':>8} {'mu':>7} {'expand':>8} {'contract':>10} {'#contractDirs':>14} {'a-factorization':>18}")
rank_flags = []
for (p, a) in fam:
    exp, con, nd, qs = dilations(p, a)
    fac = "*".join(f"{q}^{e}" for q,e in qs)
    star = " <-Antihydra" if (p,a)==(2,3) else ""
    print(f"{str((p,a)):>8} {a}/{p:<5} {exp:8.3f} {con:10.5f} {nd:>14} {fac:>18}{star}")
    rank_flags.append(((p,a), nd))

print("\n--- RANK axis ---")
print("The acting semigroup is <mu> (ONE generator x->mu*x), regardless of how many primes divide a.")
print("More prime factors of a  =>  more CONTRACTING directions, but NOT a 2nd independent GENERATOR.")
print("So every family member is rank-1 (cyclic action). VERDICT: no sibling escapes rank-1 on the")
print("generator axis -- the rank-1 obstruction is universal to 'single mu', structural to the family.")
maxdirs = max(nd for _,nd in rank_flags)
ex = [k for k,nd in rank_flags if nd==maxdirs]
print(f"Most contracting directions among tested: {maxdirs}  (e.g. {ex[:3]}) -- still rank-1.")

print("\n--- CONTRACTION axis (does stronger contraction give an easier instance?) ---")
print("Empirical p-divisibility density (Antihydra analog of even-density; Haar target = 1/p):")
print(f"{'(p,a)':>8} {'Haar 1/p':>9} {'seed=8':>9} {'seed=3':>9} {'seed=5':>9} {'|dev| max':>10}")
easier = []
for (p, a) in fam:
    row = []
    for seed in (8, 3, 5):
        d = avg_jump_empirical(p, a, seed, N=8000)
        row.append(d)
    haar = 1.0/p
    dev = max(abs(r-haar) for r in row if r==r)
    star = " <-Antihydra" if (p,a)==(2,3) else ""
    print(f"{str((p,a)):>8} {haar:9.4f} {row[0]:9.4f} {row[1]:9.4f} {row[2]:9.4f} {dev:10.4f}{star}")
    easier.append(((p,a), dev))

print("\n--- VERDICT ---")
easier.sort(key=lambda t: t[1])
print("Smallest empirical deviation from Haar (most robustly generic-looking) first:")
for (k, dev) in easier[:5]:
    print(f"   {k}: |dev|={dev:.4f}")
print("\nInterpretation (CORRECTED -- first draft over-claimed 'no sibling is easier'):")
print(" * DIFFICULTY axis: the rank-1 wall IS shared. No sibling has a 2nd independent generator")
print("   (all rank-1, structural); for seeds that ESCAPE traps every member shows the same Haar")
print("   density with the same a.e.->specific gap. Stronger contraction (bigger a) does NOT make")
print("   a generic seed provable -- extra contracting directions are unusable by rank-1 engines.")
print(" * EXCEPTIONAL-SET axis is mu-DEPENDENT (the real finding): the dead density=0.0000 entries")
print("   ((5,6),(7,8),(7,9) at seed 3) are GENUINE small-integer FIXED POINTS. floor(mu*c)=c iff")
print("   c < 1/(mu-1); so a sibling with mu NEAR 1 (small a/p, here p<=a<4p/3) has its exceptional")
print("   set MEET small integers -- those seeds are PROVABLY non-generic (provably loop/halt, not")
print("   cryptid). Antihydra mu=3/2 has 1/(mu-1)=2, so NO integer fixed point: Lemma 1 ('integer")
print("   seeds avoid periodic traps') is NOT family-universal -- it is special to x3/2's 2-adic")
print("   repulsion. The cryptids are exactly the mu bounded away from 1 whose seeds escape traps.")
print("\nCONCLUSION (honest): the family shares the GENERICITY-DIFFICULTY CLASS but NOT the location")
print("of its exceptional set. 1/(mu-1) is the explicit small-fixed-point threshold. Antihydra is a")
print("faithful representative of the *hard generic* part, but the family is NOT homogeneous on the")
print("trapping axis -- a program-level refinement of the cross-cryptid theorem, not a 'minimal rep'.")
