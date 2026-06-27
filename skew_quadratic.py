"""NEW ANGLE (skew-product / Weyl quadratic): open a provable toolbox via the leading-bit rotation.

The leading phase theta_n = {n*alpha}, alpha=log2(3/2), is a PROVABLY equidistributed irrational rotation
(Weyl). Build a SKEW PRODUCT over it: Anzai's (x+alpha, y+x) has fiber y_n = y0 + n*x0 + alpha*n(n-1)/2, a
QUADRATIC phase {beta n^2 + ...}. Quadratic equidistribution IS provable (Weyl's inequality). So if the
orbit parity carries a skew-product structure over the rotation, its fiber rides a PROVABLE quadratic phase.
We SEARCH for any quadratic/linear phase combination the parity correlates with -- a hit opens the Weyl
quadratic machinery. We test indicators of {beta n^2 + gamma n} for a grid of (beta,gamma) and the natural
alpha-skew value beta=alpha/2.
0 false proofs: report correlations with the null band; a 'hit' is a consistent correlation beating null.
"""
import math

N = 300000
c = 8; r = bytearray(N)
for n in range(N):
    r[n] = c & 1; c = (3 * c) // 2
mu = sum(r) / N
nullstd = 1.0 / math.sqrt(N)

def corr_with_indicator(beta, gamma):
    """corr of r_n with s_n = [ {beta n^2 + gamma n} >= 1/2 ]."""
    s_mu = 0; cov = 0
    # two-pass-free: accumulate
    sm = 0
    vals = []
    cov = 0.0; cnt = 0; ss = 0
    for n in range(N):
        ph = (beta * (n * n) + gamma * n) % 1.0
        s = 1 if ph >= 0.5 else 0
        cov += (r[n] - mu) * s
        ss += s
    s_mean = ss / N
    # cov(r,s) = E[(r-mu)(s-s_mean)] = (1/N)sum (r-mu)s - 0
    c_rs = cov / N
    var_r = mu * (1 - mu); var_s = s_mean * (1 - s_mean)
    return c_rs / math.sqrt(var_r * var_s) if var_s > 0 else 0.0

alpha = math.log2(1.5)
print(f"search: corr(parity, [{{beta n^2 + gamma n}}>=1/2]); null band ~{nullstd:.4f}, N={N}")
print(f"  natural Anzai-skew value beta=alpha/2={alpha/2:.5f}, alpha={alpha:.5f}\n")
best = (0, None)
cands = []
# grid over beta (incl. alpha-related), gamma
betas = [0.0, alpha/2, alpha, alpha/4, 0.5*alpha, math.log2(3)/2, (math.log2(3))%1/2,
         0.1, 0.2, 0.3183, 0.25, 0.7071]
gammas = [0.0, alpha, math.log2(3) % 1, 0.5, 0.3183]
for beta in betas:
    for gamma in gammas:
        cval = corr_with_indicator(beta % 1.0, gamma % 1.0)
        cands.append((abs(cval), cval, beta % 1.0, gamma % 1.0))
cands.sort(reverse=True)
print(f"  {'|corr|':>8} {'corr':>9} {'beta':>9} {'gamma':>9} {'/null':>7}")
for ac, cv, b, g in cands[:8]:
    flag = "  <== HIT?" if ac > 5 * nullstd else ""
    print(f"  {ac:>8.4f} {cv:>+9.4f} {b:>9.5f} {g:>9.5f} {cv/nullstd:>+7.1f}{flag}")

# also: the direct Anzai cocycle -- y_n built by y_{n+1}=y_n + theta_n (mod 1), test sign(y_n - 1/2) vs parity
print(f"\nAnzai cocycle y_{{n+1}}=y_n+{{n*alpha}} (mod1): corr(parity, [y_n>=1/2]):")
y = 0.0; cov = 0.0; ss = 0
ys = []
for n in range(N):
    s = 1 if y >= 0.5 else 0
    cov += (r[n]-mu)*s; ss += s
    y = (y + (n*alpha) % 1.0) % 1.0
s_mean = ss/N; var_s = s_mean*(1-s_mean)
anzai = (cov/N)/math.sqrt(mu*(1-mu)*var_s) if var_s>0 else 0
print(f"  corr = {anzai:+.5f}  ({anzai/nullstd:+.1f} sigma)")

print(f"""
READING (positive search outcome):
  - We scan quadratic/linear phases {{beta n^2 + gamma n}} (the skew-product fibers over the provable
    alpha-rotation) and the explicit Anzai cocycle, looking for ANY correlation with the parity that beats
    the null band ~{nullstd:.4f}. A hit would mean the parity rides a phase whose equidistribution is
    PROVABLE by Weyl's inequality (quadratic) -- opening that machinery.
  - If the best |corr| (top row) is within ~few-sigma of null, the parity is not captured by THESE skew
    phases at THIS order; the search then expands to: (a) higher-degree phases {{beta n^3...}} (still Weyl-
    provable), (b) multi-frequency cocycles, (c) the skew product with the carry as a NON-smooth cocycle
    (Furstenberg-type, where the fiber is driven by the carry digit, not a smooth phase). Each is a live,
    provable-base avenue to build next. The leading-bit rotation as a skew-product BASE is the asset; the
    task is to find the right fiber/cocycle that carries the parity.""")
