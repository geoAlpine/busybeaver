#!/usr/bin/env python3
"""D8 TEST 2 -- Antihydra M2^odd Cauchy-Schwarz envelope, reproduced and pushed deeper.

Orbit:    c_0 = 8, c -> floor(3c/2).
Renewal:  c'_j = c/2 for each EVEN c in the orbit (renewal_shift.py / alpha_attack.py).
pi_N    = (1/J) sum_{j<J} delta_{c'_j}  on Z/2^k.
C_2(k)  = (1/J^2) sum_r count_r(k)^2               (collision probability)
M2^full(k) = sum_a |pihat(a)|^2 = 2^k C_2(k)       (Parseval)
M2^even(k) = M2^full(k-1) = 2^{k-1} C_2(k-1)       (even chars at scale k = all chars at k-1)
M2^odd(k)  = 2^k C_2(k) - 2^{k-1} C_2(k-1)         (ODD_ADDITIVE_ENERGY.md sec.1)
N_k     = #{j<J : c'_j = 3^{-1} mod 2^k};  N_k = N_{k-1}/2 + eps_k, N_0 = J
avg jump = 1 + (2/J) sum_k eps_k ;  even-density = 1/(1 + avg jump)
Crude sufficient bound:  (2/J) sum_k |eps_k| <= 1
C-S envelope:            2 sum_k 2^{-(k+1)/2} M2^odd(k)^{1/2} <= 1
                 equiv.    sum_k 2^{-(k+1)/2} M2^odd(k)^{1/2} <= 1/4
"""
import sys, time
import numpy as np

J = int(sys.argv[1]) if len(sys.argv) > 1 else 40000
KMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 26
FFTCHECK = int(sys.argv[3]) if len(sys.argv) > 3 else 14
MASK = (1 << 64) - 1

t0 = time.time()
c = 8
low = np.empty(J, dtype=np.uint64)
n_even = n_odd = 0
j = 0
steps = 0
while j < J:
    if c & 1:
        n_odd += 1
    else:
        n_even += 1
        low[j] = np.uint64((c >> 1) & MASK)
        j += 1
    c = (3 * c) >> 1
    steps += 1
t_orbit = time.time() - t0

print("=== D8 TEST 2: Antihydra M2^odd envelope ===")
print(f"J (renewal entries) = {J}   orbit steps = {steps}   "
      f"final c bit-length = {c.bit_length()}")
print(f"orbit wall time = {t_orbit:.1f} s")
print()
print("-- INSTRUMENT VALIDATION (anchors) --")
ed = n_even / (n_even + n_odd)
print(f"even-density = {ed:.5f}   (doc anchor ~ 0.50018)")
print(f"avg jump = #odd/#even = {n_odd/n_even:.5f}   (doc anchor ~ 1.0)")

# ---- N_k and eps_k -------------------------------------------------------
inv3 = pow(3, -1, 1 << KMAX)
Nk = []
for k in range(1, KMAX + 1):
    m = (1 << k) - 1
    Nk.append(int(np.count_nonzero((low & np.uint64(m)) == np.uint64(inv3 & m))))
eps = []
prev = J
for k in range(1, KMAX + 1):
    eps.append(Nk[k - 1] - prev / 2.0)
    prev = Nk[k - 1]
crude = 2.0 / J * sum(abs(e) for e in eps)
avgjump_tel = 1.0 + 2.0 / J * sum(eps)
print(f"avg jump via telescoping 1+(2/J)sum eps = {avgjump_tel:.5f}  "
      f"(direct {n_odd/n_even:.5f})")
print(f"crude bound (2/J) sum|eps_k| = {crude:.4f}   (need <=1; doc anchor ~0.009)")

# ---- C_2(k), M2^odd(k) ---------------------------------------------------
C2 = {0: 1.0}
for k in range(1, KMAX + 1):
    m = np.uint64((1 << k) - 1)
    _, cnt = np.unique(low & m, return_counts=True)
    C2[k] = float(np.sum(cnt.astype(np.float64) ** 2)) / (float(J) ** 2)

M2odd = {}
for k in range(1, KMAX + 1):
    M2odd[k] = (2.0 ** k) * C2[k] - (2.0 ** (k - 1)) * C2[k - 1]

# ---- FFT cross-check of the identity ------------------------------------
print()
print("-- IDENTITY CROSS-CHECK (direct FFT vs 2^k C2(k) - 2^{k-1} C2(k-1)) --")
print(f"{'k':>3} {'M2odd(fft)':>13} {'M2odd(ident)':>14} {'M2full':>10} "
      f"{'random 2^{k-1}/J':>17} {'reldiff':>10}")
for k in range(2, min(FFTCHECK, KMAX) + 1, 2):
    m = (1 << k) - 1
    h = np.bincount((low & np.uint64(m)).astype(np.int64), minlength=1 << k).astype(np.float64) / J
    F = np.fft.fft(h)
    p = np.abs(F) ** 2
    odd_idx = np.arange(1, 1 << k, 2)
    fftval = float(np.sum(p[odd_idx]))
    ident = M2odd[k]
    rd = abs(fftval - ident) / max(abs(ident), 1e-300)
    print(f"{k:>3} {fftval:>13.6f} {ident:>14.6f} {(2.0**k)*C2[k]:>10.5f} "
          f"{2.0**(k-1)/J:>17.6f} {rd:>10.2e}")

# ---- envelope as a function of k_max ------------------------------------
print()
print("-- M2^odd(k) and envelope partial sums --")
print(f"{'k':>3} {'M2odd(k)':>14} {'random':>12} {'ratio':>7} "
      f"{'term':>10} {'SUM(<=1/4)':>11} {'2*SUM(<=1)':>11}")
S = 0.0
env_at = {}
for k in range(1, KMAX + 1):
    term = 2.0 ** (-(k + 1) / 2.0) * (max(M2odd[k], 0.0) ** 0.5)
    S += term
    env_at[k] = S
    rnd = 2.0 ** (k - 1) / J
    print(f"{k:>3} {M2odd[k]:>14.6f} {rnd:>12.6f} {M2odd[k]/rnd:>7.3f} "
          f"{term:>10.6f} {S:>11.5f} {2*S:>11.5f}")

# ---- natural cutoff: last k with eps_k != 0 ------------------------------
kstar = max([k for k in range(1, KMAX + 1) if eps[k - 1] != 0.0] or [0])
lastN = max([k for k in range(1, KMAX + 1) if Nk[k - 1] > 0] or [0])
print()
print("-- CUTOFF DIAGNOSTICS --")
print(f"N_k > 0 up to k = {lastN};  eps_k != 0 up to k* = {kstar};  log2(J) = {np.log2(J):.2f}")
print(f"envelope 2*SUM at natural cutoff k*={kstar}: {2*env_at.get(kstar,0.0):.5f}  "
      f"(SUM = {env_at.get(kstar,0.0):.5f}, need <= 1/4)")
print(f"envelope 2*SUM at doc cutoff k_max=20   : {2*env_at.get(20,0.0):.5f}  "
      f"(SUM = {env_at.get(20,0.0):.5f})")
print(f"per-level term in the equidistributed regime = 1/(2 sqrt(J)) = "
      f"{1/(2*J**0.5):.6f}; observed mean term k=10..{KMAX} = "
      f"{np.mean([2.0**(-(k+1)/2.0)*max(M2odd[k],0)**0.5 for k in range(10,KMAX+1)]):.6f}")
print()
print("SUMMARY_ROW", J, kstar, lastN, f"{ed:.5f}", f"{crude:.4f}",
      f"{env_at.get(kstar,0.0):.5f}", f"{env_at.get(20,0.0):.5f}",
      f"{env_at.get(KMAX,0.0):.5f}", KMAX)
print()
print(f"elapsed total {time.time()-t0:.1f} s")
