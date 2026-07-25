#!/usr/bin/env python3
"""
Route #17 (FFY / Stewart internalization) numerics for the (K) wall.

Object: T(G) = (4G + e(G mod 3))/3 on Z_3, e = {0:9, 1:14, 2:1}.
Seed 43. rho_n = G_n mod 3. phi = freq(rho_n == 1).

Question: does seed-43's orbit carry a SECOND multiplicatively-independent
(base-2) structure that correlates with the base-3 residue rho_n, so that
x2-x3 (Furstenberg/Host/Rudolph) rigidity could bite?

We compute, for n up to N, the integer orbit G_n (exact big-int) and look at
correlations between rho_n (base-3 residue in {0,1,2}) and base-2 features of G_n:
  - parity  p_n   = G_n mod 2
  - v2_n          = 2-adic valuation of G_n
  - pop_n         = popcount(G_n) mod m for small m
We report empirical joint / conditional distributions and a chi-square-style
independence check.
"""

E = {0: 9, 1: 14, 2: 1}

def T(G):
    r = G % 3
    return (4 * G + E[r]) // 3

def popcount(x):
    return bin(x).count("1")

def v2(x):
    if x == 0:
        return -1  # undefined; orbit won't hit 0
    return (x & -x).bit_length() - 1

def run(N, seed=43):
    G = seed
    rho = []
    par = []
    val2 = []
    pop = []
    Gs_small = []
    for n in range(N):
        r = G % 3
        rho.append(r)
        par.append(G % 2)
        val2.append(v2(G))
        pop.append(popcount(G))
        if n < 40:
            Gs_small.append(G)
        G = T(G)
    return rho, par, val2, pop, Gs_small

def freq(seq, val):
    return sum(1 for x in seq if x == val) / len(seq)

def joint_table(a, b, avals, bvals):
    """Return counts[ (av,bv) ] and marginals."""
    import collections
    c = collections.Counter(zip(a, b))
    return c

def chisq_independence(a, b, avals, bvals):
    """Pearson chi-square for independence of categorical a,b."""
    import collections
    N = len(a)
    ca = collections.Counter(a)
    cb = collections.Counter(b)
    cab = collections.Counter(zip(a, b))
    chi = 0.0
    dof = (len(avals) - 1) * (len(bvals) - 1)
    for av in avals:
        for bv in bvals:
            exp = ca[av] * cb[bv] / N
            obs = cab[(av, bv)]
            if exp > 0:
                chi += (obs - exp) ** 2 / exp
    return chi, dof

def main():
    N = 10**4
    rho, par, val2, pop, Gs_small = run(N)

    print("=== Seed-43 orbit, first 40 G_n and residues ===")
    for n, G in enumerate(Gs_small):
        print(f"n={n:2d}  rho={G%3}  par={G%2}  v2={v2(G)}  pop={popcount(G)}  G={G if G < 10**12 else str(G)[:12]+'...('+str(len(str(G)))+' digits)'}")

    print()
    print(f"=== Frequencies over N={N} ===")
    print(f"phi = freq(rho==1) = {freq(rho,1):.5f}")
    print(f"freq(rho==0)       = {freq(rho,0):.5f}")
    print(f"freq(rho==2)       = {freq(rho,2):.5f}")
    print(f"freq(par==0 even)  = {freq(par,0):.5f}")
    print(f"freq(par==1 odd)   = {freq(par,1):.5f}")

    # v2 distribution
    import collections
    cv = collections.Counter(val2)
    print()
    print("=== v2(G_n) distribution (geometric ~1/2^(k+1) if 'random') ===")
    for k in sorted(cv)[:8]:
        print(f"  v2={k}: {cv[k]/N:.5f}  (random ~ {0.5**(k+1):.5f})")

    # popcount mod 2 and mod 3
    pop2 = [x % 2 for x in pop]
    pop3 = [x % 3 for x in pop]

    print()
    print("=== Independence checks (chi-square) ===")
    # rho (3 vals) vs parity (2 vals)
    chi, dof = chisq_independence(rho, par, [0,1,2], [0,1])
    print(f"rho x parity:      chi2={chi:.3f}  dof={dof}  (95% crit ~ {crit95(dof):.2f})")
    # rho vs popcount mod 2
    chi, dof = chisq_independence(rho, pop2, [0,1,2], [0,1])
    print(f"rho x popcount%2:  chi2={chi:.3f}  dof={dof}  (95% crit ~ {crit95(dof):.2f})")
    # rho vs popcount mod 3
    chi, dof = chisq_independence(rho, pop3, [0,1,2], [0,1,2])
    print(f"rho x popcount%3:  chi2={chi:.3f}  dof={dof}  (95% crit ~ {crit95(dof):.2f})")
    # rho vs (v2 capped at 3)
    v2cap = [min(x,3) for x in val2]
    chi, dof = chisq_independence(rho, v2cap, [0,1,2], [0,1,2,3])
    print(f"rho x v2(cap3):    chi2={chi:.3f}  dof={dof}  (95% crit ~ {crit95(dof):.2f})")

    # Conditional: P(rho==1 | parity)
    print()
    print("=== Conditional freq(rho==1 | base-2 feature) ===")
    for pv in [0,1]:
        idx = [i for i in range(N) if par[i]==pv]
        f = sum(1 for i in idx if rho[i]==1)/len(idx)
        print(f"  P(rho==1 | parity={pv}) = {f:.5f}   (base rate {freq(rho,1):.5f}, n={len(idx)})")
    for pv in [0,1]:
        idx = [i for i in range(N) if pop2[i]==pv]
        f = sum(1 for i in idx if rho[i]==1)/len(idx)
        print(f"  P(rho==1 | popcount%2={pv}) = {f:.5f}")

    # Is parity itself deterministic given the orbit? Check autocorrelation of rho
    print()
    print("=== rho autocorrelation (lag 1..5), symbol-1 indicator ===")
    ind = [1 if r==1 else 0 for r in rho]
    m = sum(ind)/N
    for lag in range(1,6):
        cov = sum((ind[i]-m)*(ind[i+lag]-m) for i in range(N-lag))/(N-lag)
        var = sum((x-m)**2 for x in ind)/N
        print(f"  lag {lag}: autocorr = {cov/var:+.4f}")

def crit95(dof):
    # rough chi-square 95% critical values
    table = {1:3.84, 2:5.99, 3:7.81, 4:9.49, 5:11.07, 6:12.59}
    return table.get(dof, dof + 2*(2*dof)**0.5)

if __name__ == "__main__":
    main()
