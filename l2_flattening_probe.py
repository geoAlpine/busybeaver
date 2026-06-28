#!/usr/bin/env python
"""
L2-FLATTENING PROBE (quenched / deterministic) for the Antihydra orbit.   SOUNDNESS PARAMOUNT.

The one un-closed speculative angle (FRESH_ANGLES_SCOUT.md sec.7): is there a DETERMINISTIC,
single-orbit, finite-N "L2-flattening" of the orbit's own empirical measure mu_N on Z/2^k under
the x3/2 dynamics -- a SELF-GENERATED entropy increase / additive-energy decay that beats additive
concentration WITHOUT assuming equidistribution?  Classical sum-product/Bourgain-Gamburd flattening
flattens a MEASURE (annealed average over random signs).  Here we test the orbit's OWN measure.

Orbit (exact):  h_0 = 8,  h_{n+1} = floor(3 h_n / 2) = h_n + (h_n >> 1).   h_n = floor(8 (3/2)^n).
Residue:        c_n = h_n mod 2^k  = low k bits of h_n  (exact, big-int, no float (3/2)^n).
Empirical measure:  mu_N(r) = (1/N) #{ n<N : c_n = r },  on the group Z/2^k.

Metrics (all on Z/2^k, the correct additive group):
  - collision prob  C2 = sum_r mu(r)^2   (uniform = 2^-k);  Renyi-2 entropy H2 = -log2 C2 (uniform = k).
  - largest atom    max_r mu(r)           (uniform = 2^-k).
  - additive energy E(mu) = sum_t (mu*mu)(t)^2  (circular conv on Z/2^k; uniform = 2^-k, delta = 1).

Baselines:
  (a) RANDOM surrogate: N i.i.d. uniform residues mod 2^k  (= the ANNEALED i.i.d. prediction).
  (b) CONCENTRATED: induced fixed point o=1 (all residues equal -> delta) and an AP/coset-confined
      orbit (high additive energy) -- the "halting/structured" anchor.

Structural check: x3 is a BIJECTION on Z/2^k (3 invertible mod 2^k) => it cannot change C2/E at all;
only the 2-adic carry/shift (drop low bit, pull high bit) can flatten -- i.e. flattening == the
assumed equidistribution.  We verify this explicitly.

0 false proofs: everything below is exact-arithmetic / numpy numerics, labelled [OBSERVED].
.venv python only.
"""
import math
import numpy as np

RNG = np.random.default_rng(20260629)

def orbit_low_bits(Nmax, kbits=14):
    """Return uint16 array of (h_n mod 2^kbits) for n=0..Nmax-1, exact big-int orbit h<-floor(3h/2)."""
    mask = (1 << kbits) - 1
    out = np.empty(Nmax, dtype=np.uint16)
    h = 8
    for n in range(Nmax):
        out[n] = h & mask
        h = h + (h >> 1)        # floor(3h/2), exact
    return out

def metrics(residues, k):
    """collision prob, H2, largest atom, additive energy E(mu) on Z/2^k, for an int residue array."""
    M = 1 << k
    counts = np.bincount(residues & (M - 1), minlength=M).astype(np.float64)
    N = counts.sum()
    mu = counts / N
    C2 = float(np.dot(mu, mu))
    H2 = -math.log2(C2)
    maxatom = float(mu.max())
    # additive energy on Z/2^k via FFT (circular convolution mu*mu)
    fhat = np.fft.fft(mu)
    conv = np.fft.ifft(fhat * fhat).real
    E = float(np.dot(conv, conv))
    return dict(C2=C2, H2=H2, maxatom=maxatom, E=E, M=M, Nsamp=int(N))

def random_metrics(N, k, draws=200):
    """Mean / 95% band of metrics for i.i.d. uniform residues mod 2^k (the annealed prediction)."""
    M = 1 << k
    C2s, Es, maxs = [], [], []
    for _ in range(draws):
        r = RNG.integers(0, M, size=N)
        m = metrics(r, k)
        C2s.append(m["C2"]); Es.append(m["E"]); maxs.append(m["maxatom"])
    def band(x):
        x = np.sort(x); lo = x[int(0.025*len(x))]; hi = x[int(0.975*len(x))]
        return float(np.mean(x)), float(lo), float(hi)
    return dict(C2=band(C2s), E=band(Es), maxatom=band(maxs))

def induced_fixed_point_residues(N, k):
    """o=1 fixed point of induced map -> all residues = 1 (maximally concentrated, delta)."""
    return np.ones(N, dtype=np.int64)

def coset_confined_residues(N, k, step=None):
    """A structured high-additive-energy anchor: residues confined to a short AP / coset r = c*step."""
    M = 1 << k
    if step is None:
        step = M >> 2  # subgroup of index 4 -> only 4 residues, high additive energy
    # walk a fixed AP deterministically
    return (np.arange(N) * step) % M

# -------------------------------------------------------------------------------------------------
def main():
    print("="*92)
    print("L2-FLATTENING PROBE  (quenched/deterministic, Antihydra orbit h<-floor(3h/2), h0=8)")
    print("="*92)

    Nmax = 100_000
    KMAX = 14
    print(f"\nGenerating exact orbit residues (low {KMAX} bits), N={Nmax} ...")
    res = orbit_low_bits(Nmax, KMAX)
    print("  done.  (e.g. first 8 residues mod 256:", list(int(x)&255 for x in res[:8]), ")")

    ks = [4, 6, 8, 10]
    checkpoints = [100, 1000, 10000, 100000]

    # ---- 1+2. flattening of mu_N: collision prob / H2 / largest atom vs N, vs random, vs concentrated
    for k in ks:
        M = 1 << k
        print("\n" + "-"*92)
        print(f"[k={k}]  Z/2^{k} ({M} cells).  Uniform target: C2=2^-{k}={2.0**-k:.3e}, H2={k}, "
              f"maxatom={2.0**-k:.3e}, E=2^-{k}={2.0**-k:.3e}")
        print(f"  {'N':>8} | {'C2(orbit)':>11} {'C2/unif':>8} {'H2':>6} {'maxatom':>9} {'mx/unif':>8} | "
              f"{'C2(rand)mean':>12} {'rand95band':>22} | orbit-vs-random")
        for N in checkpoints:
            if N > Nmax: continue
            mo = metrics(res[:N].astype(np.int64), k)
            mr = random_metrics(N, k, draws=120 if N<=10000 else 40)
            c2m, c2lo, c2hi = mr["C2"]
            inside = "INSIDE band" if c2lo <= mo["C2"] <= c2hi else ("BELOW(sub-random!)" if mo["C2"]<c2lo else "ABOVE(concentr.)")
            print(f"  {N:>8} | {mo['C2']:>11.4e} {mo['C2']*M:>8.3f} {mo['H2']:>6.3f} "
                  f"{mo['maxatom']:>9.4e} {mo['maxatom']*M:>8.3f} | "
                  f"{c2m:>12.4e} [{c2lo:.3e},{c2hi:.3e}] | {inside}")

    # ---- 3. additive energy E(A): sub-random / random / concentrated ?
    print("\n" + "="*92)
    print("ADDITIVE ENERGY  E(mu) = sum_t (mu*mu)(t)^2  on Z/2^k   (uniform=2^-k, delta=1; smaller=flatter)")
    print("="*92)
    for k in ks:
        M = 1 << k
        N = 100000
        mo = metrics(res[:N].astype(np.int64), k)
        mr = random_metrics(N, k, draws=60)
        Em, Elo, Ehi = mr["E"]
        # concentrated baselines
        mfix = metrics(induced_fixed_point_residues(N, k), k)
        mcos = metrics(coset_confined_residues(N, k), k)
        unif = 2.0**-k
        print(f"\n[k={k}] N={N}:  uniform E={unif:.4e}")
        print(f"    orbit         E={mo['E']:.4e}   (E/uniform={mo['E']/unif:6.3f})")
        print(f"    random surr.  E={Em:.4e}   95%=[{Elo:.3e},{Ehi:.3e}]   (E/uniform={Em/unif:6.3f})")
        print(f"    concentrated: fixed-pt o=1 E={mfix['E']:.4e} (E/unif={mfix['E']/unif:.2e}), "
              f"coset-AP E={mcos['E']:.4e} (E/unif={mcos['E']/unif:.2e})")
        verdict = ("SUB-RANDOM" if mo['E'] < Elo else "RANDOM (in band)" if mo['E'] <= Ehi else "CONCENTRATED (above)")
        print(f"    => orbit additive energy is: {verdict}")

    # ---- 4. flattening RATE: how fast does C2 - 2^-k decay in N?  orbit vs random (1/N)
    print("\n" + "="*92)
    print("FLATTENING RATE:  excess collision  C2(N) - 2^-k  vs N.  Random surrogate decays ~ (1-2^-k)/N.")
    print("="*92)
    for k in [6, 8]:
        M = 1 << k; unif = 2.0**-k
        Ns = np.unique(np.geomspace(M*4, Nmax, 18).astype(int))
        ex_orbit, ex_rand = [], []
        for N in Ns:
            mo = metrics(res[:N].astype(np.int64), k)
            mr = random_metrics(int(N), k, draws=30)
            ex_orbit.append(mo['C2'] - unif)
            ex_rand.append(mr['C2'][0] - unif)
        ex_orbit = np.array(ex_orbit); ex_rand = np.array(ex_rand)
        # fit log(excess) ~ b log N  (only where positive)
        def fit(ex):
            m = ex > 0
            if m.sum() < 3: return float('nan')
            return float(np.polyfit(np.log(Ns[m]), np.log(ex[m]), 1)[0])
        print(f"\n[k={k}]  excess-collision decay exponent (C2-2^-k ~ N^b):")
        print(f"    orbit  b = {fit(ex_orbit):+.3f}   random b = {fit(ex_rand):+.3f}   (random theory = -1)")
        print(f"    sample: N={Ns[0]} orbit_excess={ex_orbit[0]:.3e} rand_excess={ex_rand[0]:.3e};  "
              f"N={Ns[-1]} orbit_excess={ex_orbit[-1]:.3e} rand_excess={ex_rand[-1]:.3e}")

    # ---- 5. STRUCTURAL: x3 is a bijection on Z/2^k => cannot flatten.  Demonstrate on the orbit measure.
    print("\n" + "="*92)
    print("STRUCTURAL CHECK:  x3 mod 2^k is a BIJECTION (3 invertible) => leaves C2/E INVARIANT.")
    print("  (So no L2-flattening can come from the x3 expansion; only the 2-adic carry/shift can,")
    print("   and THAT shift is exactly the equidistribution one is trying to prove.)")
    print("="*92)
    for k in [8, 10]:
        M = 1 << k
        r = res[:Nmax].astype(np.int64) & (M-1)
        m0 = metrics(r, k)
        r3 = (3 * r) % M                       # push by x3 (bijection)
        m3 = metrics(r3, k)
        # push by the actual dynamics = time-shift of the orbit's residues
        m_shift = metrics(res[1:Nmax].astype(np.int64) & (M-1), k)
        print(f"\n[k={k}] N={Nmax}:")
        print(f"    C2(mu)            = {m0['C2']:.6e}   E={m0['E']:.6e}")
        print(f"    C2(x3 push mu)    = {m3['C2']:.6e}   E={m3['E']:.6e}   (identical: x3 bijection)")
        print(f"    C2(time-shift mu) = {m_shift['C2']:.6e}   E={m_shift['E']:.6e}   (~unchanged: measure stationary)")

    # ---- 6. SUB-PROGRESSION concentration: max non-trivial Fourier coeff of mu (more sensitive than L4)
    print("\n" + "="*92)
    print("SUB-PROGRESSION NON-CONCENTRATION:  max_{xi!=0} |mu_hat(xi)|  (peak at a dual subgroup = ")
    print("  concentration on an AP/coset).  Random surrogate ~ sqrt(M-1)/sqrt(N)/... ; orbit vs random.")
    print("="*92)
    for k in [8, 10]:
        M = 1 << k
        ro = res[:Nmax].astype(np.int64) & (M-1)
        mu = np.bincount(ro, minlength=M).astype(np.float64) / Nmax
        muhat = np.abs(np.fft.fft(mu))
        peak_o = float(muhat[1:].max())          # exclude DC (xi=0)
        argpk = int(1 + np.argmax(muhat[1:]))
        # random band
        peaks = []
        for _ in range(60):
            r = RNG.integers(0, M, size=Nmax)
            mr = np.bincount(r, minlength=M).astype(np.float64)/Nmax
            peaks.append(float(np.abs(np.fft.fft(mr))[1:].max()))
        peaks = np.sort(peaks)
        rlo, rhi = peaks[1], peaks[-2]
        loc = "INSIDE rand band" if rlo <= peak_o <= rhi else ("BELOW(sub-random)" if peak_o<rlo else "ABOVE(concentr.)")
        print(f"\n[k={k}] N={Nmax}: max|mu_hat(xi!=0)| orbit={peak_o:.4e} at xi={argpk} "
              f"(coset-AP anchor peak={1.0/4:.3f}); random mean={peaks.mean():.4e} "
              f"band=[{rlo:.3e},{rhi:.3e}] -> {loc}")

    print("\n" + "="*92)
    print("See L2_FLATTENING_PROBE.md for the honest verdict.")
    print("="*92)

if __name__ == "__main__":
    main()
