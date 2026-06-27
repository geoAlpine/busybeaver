"""Leverage the XOR decomposition  c_n mod 2 = a_n XOR b_n,  a_n=bit_n(8*3^n) [pure power, Subspace-touchable],
b_n=bit_n(T_n) [self-induced carry]. In signs A_n=(-1)^{a_n}, B_n=(-1)^{b_n}, the orbit balance is the
CROSS-CORRELATION  S = sum_n A_n B_n = sum_n (-1)^{c_n mod 2},  and even-density=1/2 <=> S=o(N).
A cross-correlation can vanish without either auto-sum vanishing -- that is the potential leverage.

CRUCIAL probe: B_n is built from the orbit history c_k=a_k XOR b_k (k<n), which CONTAINS the pure-power
bits a_k. So PAST pure-power digits A_{n-j} (j>0) might PREDICT the current carry sign B_n. If they do,
the Subspace-controllable A would give partial control of B = a real handle. We measure the lagged
cross-correlation  X(j) = (1/N) sum_n A_{n-j} B_n  with block-significance (marginal corrs need a sign test).
Also autocorrelations of A and B (the inputs to any van der Corput bound on S).
0 false proofs: a 'handle' is claimed ONLY if a lag's correlation is consistent in sign across blocks AND
beats the shuffle null; otherwise reported as noise.
"""
import math

N = 120000
c = 8; Tn = 0; p3 = 1; p2 = 1
A = []; B = []; C = []  # sign sequences and parity
for n in range(N):
    a = (8 * p3 >> n) & 1
    b = (Tn >> n) & 1
    A.append(1 - 2*a); B.append(1 - 2*b); C.append(c & 1)
    Tn = 3 * Tn + p2 * (c & 1)
    c = (3 * c) // 2
    p3 *= 3; p2 <<= 1

# sanity: A_n*B_n == (-1)^{c_n mod 2}
ok = all(A[n]*B[n] == (1 - 2*C[n]) for n in range(N))
print(f"sanity A_n*B_n == (-1)^(c_n mod2): {'OK' if ok else 'FAIL'}")
S = sum(A[n]*B[n] for n in range(N))
print(f"orbit sign-sum S = sum A_n B_n = {S}  (= {S/N:+.5f} N; even-density-1/2 means S=o(N))")
print(f"  pure-power sign-sum  sum A_n = {sum(A):+d}  ({sum(A)/N:+.5f} N)")
print(f"  carry      sign-sum  sum B_n = {sum(B):+d}  ({sum(B)/N:+.5f} N)")

nullstd = 1/math.sqrt(N)
def lagged_cc(A, B, j):
    # X(j) = mean_n A[n-j]*B[n], n from j..N-1
    s = 0; cnt = 0
    for n in range(j, N):
        s += A[n-j]*B[n]; cnt += 1
    return s/cnt

print(f"\nlagged cross-correlation X(j)=mean A_{{n-j}} B_n  (null std ~{nullstd:.4f}; PAST power predicts carry?)")
print(f"  {'j':>3} {'X(j)':>9} {'/null':>7}")
sig = []
for j in range(0, 25):
    x = lagged_cc(A, B, j)
    sig.append((j, x))
    flag = "  <== signal?" if abs(x) > 5*nullstd else ""
    print(f"  {j:>3} {x:+9.5f} {x/nullstd:+7.1f}{flag}")

# block-significance for the largest |X(j)|
jmax, xmax = max(sig, key=lambda t: abs(t[1]))
Bk = 6; blk = N // Bk
print(f"\nlargest |X(j)| at j={jmax} (X={xmax:+.5f}); block sign test ({Bk} blocks):")
bsigns = []
for i in range(Bk):
    s = 0; cnt = 0
    for n in range(max(jmax, i*blk), (i+1)*blk):
        s += A[n-jmax]*B[n]; cnt += 1
    bx = s/cnt; bsigns.append(bx)
    print(f"    block {i}: {bx:+.5f}")
consistent = all(s > 0 for s in bsigns) or all(s < 0 for s in bsigns)
print(f"    consistent sign: {consistent} -> {'POSSIBLE HANDLE (investigate)' if consistent and abs(xmax)>3*nullstd else 'NOISE (no handle from past power bits)'}")

# autocorrelations (inputs to a van der Corput bound on S)
def autoc(X, h):
    return sum(X[n]*X[n+h] for n in range(N-h))/(N-h)
print(f"\nautocorrelations (van der Corput inputs); null ~{nullstd:.4f}:")
print(f"  {'h':>3} {'A-auto':>9} {'B-auto':>9} {'AB-auto':>9}")
AB = [A[n]*B[n] for n in range(N)]
for h in (1,2,3,5,8,13,21):
    print(f"  {h:>3} {autoc(A,h):+9.5f} {autoc(B,h):+9.5f} {autoc(AB,h):+9.5f}")

print(f"""
READING:
  S = sum A_n B_n is the orbit imbalance (target o(N)). If the lagged cross-correlations X(j) are all
  NOISE (no consistent-sign lag beating null), then the carry sign B_n is decorrelated even from the
  PAST pure-power bits A_{{n-j}} -> the Subspace control of A does NOT reach B by any linear lag; the XOR
  leverage gives no handle, the two Mahler-class sequences are cross-decorrelated 'generically'. If some
  lag shows a consistent handle, the Subspace-controllable A partially predicts the carry -> a crack.
  The autocorrelations being ~null (A, B, AB all white) means a van der Corput / Weyl differencing bound
  on S reduces to differenced sums that are themselves white = no descent (the known differencing fixed
  point), confirming the analytic route funnels here too. Numbers decide.""")
