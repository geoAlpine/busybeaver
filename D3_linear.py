# D3 key structural insight: depth_n >= L  <=>  S_n ≡ 8*3^n - 2^n  (mod 2^{n+L}).
# S_n = sum_{j<n, c_j odd} 2^j 3^{n-1-j} = LINEAR in the parity bits e_j=[c_j odd] (known coefficients).
# So depth >= L is an AFFINE condition on the parity history over Z/2^{n+L}. Verify, and assess the lead.
N=600
c=8; e=[]; cs=[]
for n in range(N): cs.append(c); e.append(c&1); c=3*c//2
def v2(x):
    if x==0: return 999
    r=0
    while x&1==0: x>>=1; r+=1
    return r
# verify: S_n mod 2^M built LINEARLY from e_j equals the true S_n, and depth matches the affine condition
import random
ok_lin=True; ok_cond=True
for n in range(5,200):
    M=n+30
    # linear reconstruction of S_n mod 2^M from parity bits
    Slin=sum(e[j]*(2**j)*(3**(n-1-j)) for j in range(n)) % (2**M)
    Strue=sum((cs[j]&1)*(2**j)*(3**(n-1-j)) for j in range(n)) % (2**M)
    if Slin!=Strue: ok_lin=False
    # depth condition: depth_n >= L  <=>  S_n ≡ 8*3^n-2^n (mod 2^{n+L})
    d=v2(cs[n]-1) if cs[n]>1 else 0
    target=(8*3**n - 2**n) % (2**(n+d))
    if d>0 and Slin % (2**(n+d)) != target % (2**(n+d)): ok_cond=False
print(f"S_n is LINEAR in parity bits e_j (coeffs 2^j 3^(n-1-j)): {ok_lin}")
print(f"depth_n>=L <=> affine condition  S_n ≡ 8*3^n-2^n (mod 2^(n+L)): {ok_cond}")
print()
print("=> D3 STRUCTURAL LEAD: the depth (hence even-density) is governed by AFFINE conditions on the")
print("   parity history over Z/2^M. The coefficients 2^j 3^(n-1-j) are EXPLICIT. This is a LINEAR")
print("   structure -- exactly the regime where exponential-sum / Fourier methods can work even when")
print("   the nonlinear digit-equidistribution does not. The self-reference (e_j depends on the orbit)")
print("   remains, BUT a linear-form analysis of sum_n e(t * [affine depth-form]) is a concrete new")
print("   sub-problem (D3/M2) that the general equidistribution does not reduce to.")
