#!/usr/bin/env python
"""
o4_gowers_test.py  (2026-07-10)

GENUINELY-NEW tool on the o4 frequency problem: Gowers uniformity norms
U^2, U^3 + inverse-theorem (nilsequence / polynomial-phase) correlation.

Phase function  f(n) = e(W_n / 3) = omega^{W_n mod 3},  omega = e^{2 pi i/3},
on the SPECIFIC o4 orbit (seed G0=43),  W_n = G_n + 14,
odometer  3 G' = 4 G + e(rho),  rho = G mod 3,  e = {0:9,1:14,2:1}.

freq{3|W_n} = 1/3 + (2/3) Re( (1/N) sum f ) is the frequency deviation.

We MEASURE (beyond the U^1 autocorr/entropy probe of FREQUENCY_AXIS_PROBE):
  * DC / mean  (linear U^1 level)
  * ||f||_{U^2} via the exact Fourier identity ||f||_{U^2}^4 = sum_xi |fhat(xi)|^4
  * best linear phase   max_xi |fhat(xi)|        (inverse-U^2 obstruction)
  * ||f||_{U^3} via the derivative recursion
        ||f||_{U^3}^8 = E_h  sum_xi |FT(Delta_h f)(xi)/N|^4,  Delta_h f(x)=f(x+h) conj f(x)
  * best quadratic phase  max_{a,b} |E_n f(n) e(-a n^2 - b n)|  (inverse-U^3 obstruction)
  * a bracket-nilsequence family  e(a n floor(b n))          (2-step nil obstruction)
All against a SHUFFLE control (destroys order, keeps marginal) AND a random
unit-phase control, plus VALIDATION on injected linear/quadratic phases so we
prove the estimator FIRES when genuine structure is present.

Interpreter: quantum-ecc/.venv python.  fhat = expectation-normalized FT (E_x).
"""
import numpy as np
import math, time, sys

W = math.e  # placeholder to avoid name clash; not used
OMEGA = np.exp(2j*np.pi/3)
E = {0:9, 1:14, 2:1}

def orbit_residues(G0=43, N=1<<16):
    """Return int8 array of W_n mod 3 for n in [0,N).  Exact big-int G."""
    G = G0
    r = np.empty(N, dtype=np.int8)
    for n in range(N):
        # W = G+14 ; W mod 3 = (G+14) mod 3 = (G+2) mod 3
        r[n] = (G + 14) % 3
        rho = G % 3
        G = (4*G + E[rho])//3
    return r

# ---------- Gowers machinery (cyclic Z_N, FFT-based) ----------
def fhat(f):
    """expectation-normalized DFT: fhat(xi) = (1/N) sum_x f(x) e(-2pi i x xi/N)."""
    return np.fft.fft(f)/len(f)

def U2_norm(f):
    """||f||_{U^2} = (sum_xi |fhat|^4)^{1/4}. Includes DC."""
    F = fhat(f)
    return (np.sum(np.abs(F)**4).real)**0.25

def best_linear(f, exclude_dc=False):
    """max_xi |fhat(xi)| over the N Fourier frequencies (the best linear phase)."""
    F = np.abs(fhat(f))
    if exclude_dc:
        F = F.copy(); F[0] = 0.0
    k = int(np.argmax(F))
    return F[k], k

def U3_norm(f, hs=None, rng=None, nsample=None):
    """||f||_{U^3}^8 = E_h [ sum_xi |FT(Delta_h f)/N|^4 ].
    If nsample given, average over nsample random shifts h (Monte-Carlo estimate);
    else average over ALL h (exact)."""
    N = len(f)
    fc = np.conj(f)
    if nsample is None:
        hs = range(N)
    elif hs is None:
        hs = rng.integers(0, N, size=nsample)
    acc = 0.0; cnt = 0
    for h in hs:
        dh = np.roll(f, -int(h)) * fc          # Delta_h f(x) = f(x+h) conj f(x)
        F = np.fft.fft(dh)/N
        acc += np.sum(np.abs(F)**4).real
        cnt += 1
    return (acc/cnt)**(1.0/8.0)

# ---------- inverse-theorem obstruction searches ----------
def best_quadratic(f, n_alpha=4000, rng=None, alpha_grid=None):
    """max_{a,b} |E_n f(n) e(-a n^2 - b n)|.
    For each a: g(n)=f(n) e(-a n^2); best b = max Fourier coeff of g.
    alpha_grid overrides the sampling (used to probe near a known injected a0)."""
    N = len(f)
    n = np.arange(N)
    n2 = (n.astype(np.float64)**2)
    if alpha_grid is None:
        alpha_grid = rng.random(n_alpha)      # a in [0,1)
    best = 0.0; besta = None
    for a in alpha_grid:
        g = f * np.exp(-2j*np.pi*a*n2)
        c = np.max(np.abs(np.fft.fft(g)))/N
        if c > best:
            best = c; besta = a
    return best, besta

def best_bracket(f, n_ab=1500, rng=None):
    """max over a 2-step bracket-nilsequence family e(a * n * floor(b n)):
    max_{a,b} |E_n f(n) e(-a n floor(b n))|. Representative Heisenberg nilseq."""
    N = len(f)
    n = np.arange(N)
    best = 0.0; bestab=None
    for _ in range(n_ab):
        a = rng.random(); b = rng.random()
        phase = a * n * np.floor(b*n)
        c = abs(np.mean(f*np.exp(-2j*np.pi*phase)))
        if c > best:
            best = c; bestab=(a,b)
    return best, bestab

def main():
    t0=time.time()
    N = 1<<16
    print(f"# o4 Gowers U^2/U^3 + inverse-theorem test   N={N}  seed G0=43")
    print(f"# f(n) = e(W_n/3) = omega^(W_n mod 3),  omega=exp(2pi i/3)\n")

    r = orbit_residues(N=N)
    f = OMEGA**r.astype(np.int64)             # complex unit-modulus, 3 values
    # sanity: residue frequencies & the freq<->S1 dictionary
    cnt = np.bincount(r, minlength=3)
    S1_full = np.sum(f)                        # sum omega^{W}
    Re_over_N = (np.sum(np.exp(2j*np.pi*r/3)).real)/N
    freq1 = cnt[0]/N                           # r==0  <=> W==0 mod3 <=> rho=1 (3|W)
    print("== orbit / frequency sanity ==")
    print(f"  W mod3 counts [0,1,2] = {cnt.tolist()}  (r=0 <=> 3|W_n <=> rho=1)")
    print(f"  freq{{3|W_n}} = {freq1:.5f}   (annealed 1/3, fatal 4/5)")
    print(f"  (1/N) sum f = {S1_full/N:.6f}   |mean f| = {abs(S1_full)/N:.6f}")
    print(f"  Re((1/N)sum f) = {Re_over_N:.6f}  => freq = 1/3+(2/3)Re = {1/3+2/3*Re_over_N:.5f} (check)\n")

    rng = np.random.default_rng(0)

    # ---------- U^2 and best linear phase ----------
    u2 = U2_norm(f)
    lin, lk = best_linear(f, exclude_dc=True)
    dc = abs(S1_full)/N
    print("== U^2 level (linear / Fourier) ==")
    print(f"  ||f||_U2         = {u2:.6e}")
    print(f"  |DC| (mean)      = {dc:.6e}")
    print(f"  best linear phase max_xi|fhat| = {lin:.6e} at xi={lk} (theta={lk/N:.6f})")

    # shuffle control for U2 and best-linear
    n_ctrl=20
    u2s=[]; lins=[]
    for _ in range(n_ctrl):
        g=f.copy(); rng.shuffle(g)
        u2s.append(U2_norm(g)); lins.append(best_linear(g,exclude_dc=True)[0])
    u2s=np.array(u2s); lins=np.array(lins)
    print(f"  shuffle U2       = {u2s.mean():.6e} +/- {u2s.std():.1e}   z={(u2-u2s.mean())/u2s.std():+.2f}")
    print(f"  shuffle best-lin = {lins.mean():.6e} +/- {lins.std():.1e}   z={(lin-lins.mean())/lins.std():+.2f}")
    print(f"  random baseline  N^(-1/4) = {N**-0.25:.6e}   sqrt(logN/N)={math.sqrt(math.log(N)/N):.6e}\n")

    # ---------- U^3 (sampled h) + control ----------
    nsamp = 3000
    t=time.time()
    u3 = U3_norm(f, rng=np.random.default_rng(1), nsample=nsamp)
    print(f"== U^3 level (quadratic / 2-step)  [E over {nsamp} sampled shifts h] ==")
    print(f"  ||f||_U3         = {u3:.6e}   ({time.time()-t:.1f}s)")
    u3s=[]
    for s in range(6):
        g=f.copy(); np.random.default_rng(100+s).shuffle(g)
        u3s.append(U3_norm(g, rng=np.random.default_rng(200+s), nsample=nsamp))
    u3s=np.array(u3s)
    print(f"  shuffle U3       = {u3s.mean():.6e} +/- {u3s.std():.1e}   z={(u3-u3s.mean())/u3s.std():+.2f}")
    print(f"  random baseline  N^(-1/8) = {N**-0.125:.6e}\n")

    # ---------- inverse-U^3: best quadratic phase + bracket nilseq ----------
    t=time.time()
    q, qa = best_quadratic(f, n_alpha=4000, rng=np.random.default_rng(2))
    print("== inverse-theorem obstruction search ==")
    print(f"  best quadratic  max_(a,b)|E f e(-a n^2 - b n)| = {q:.6e}  (a~{qa:.4f})  ({time.time()-t:.1f}s)")
    # control on shuffle
    gsh=f.copy(); np.random.default_rng(7).shuffle(gsh)
    qc,_=best_quadratic(gsh, n_alpha=4000, rng=np.random.default_rng(3))
    print(f"  shuffle quadratic                              = {qc:.6e}")
    br, brab = best_bracket(f, n_ab=1500, rng=np.random.default_rng(4))
    brc,_ = best_bracket(gsh, n_ab=1500, rng=np.random.default_rng(5))
    print(f"  best bracket-nil max|E f e(-a n floor(b n))|   = {br:.6e}  (real)")
    print(f"  shuffle bracket-nil                            = {brc:.6e}")
    print(f"  random baseline for a max over ~4000 tests ~ sqrt(logK/N)-ish = {math.sqrt(math.log(4000)/N):.6e}\n")

    # ---------- VALIDATION: estimator must FIRE on genuine structure ----------
    print("== VALIDATION: does the estimator detect structure when present? ==")
    n=np.arange(N)
    theta=(math.sqrt(5)-1)/2
    flin = np.exp(2j*np.pi*theta*n)                 # pure linear phase
    a0=theta/1.0
    fquad= np.exp(2j*np.pi*(a0*n*n))                # pure quadratic phase
    print(f"  linear  e(theta n): U2={U2_norm(flin):.4e} (BIG), best-lin={best_linear(flin,True)[0]:.4e},"
          f" U3={U3_norm(flin,rng=np.random.default_rng(9),nsample=800):.4e}")
    print(f"  quad e(a n^2): U2={U2_norm(fquad):.4e} (small~random), best-lin={best_linear(fquad,True)[0]:.4e},"
          f" U3={U3_norm(fquad,rng=np.random.default_rng(9),nsample=800):.4e} (BIG)")
    # quadratic-phase search near known a0 should recover it
    grid=a0+np.linspace(-3/N,3/N,7)
    qv,qva=best_quadratic(fquad, alpha_grid=np.concatenate([grid,[a0]]))
    print(f"  quad-search near injected a0={a0:.5f}: recovered corr={qv:.4e} at a={qva:.5f} (should be ~1)")
    print(f"\n# total {time.time()-t0:.1f}s")

if __name__=='__main__':
    main()
