import math
# D3 carry calculus foundation. Verify exact identities; set up the depth formula; probe the Baker angle.
N=4000
c=8; S=0; cs=[]; Ss=[]
for n in range(N):
    cs.append(c); Ss.append(S)
    S=3*S+(2**n)*(c&1)   # S_{n+1}=3S_n+2^n[c_n odd]
    c=3*c//2
# (1) verify 2^n c_n = 8*3^n - S_n
ok=all(cs[n]*(2**n)==8*3**n - Ss[n] for n in range(0,300))
print(f"identity 2^n c_n = 8*3^n - S_n  holds (n<300): {ok}")
# (2) depth_n = v2(c_n - 1); also = v2(8*3^n - S_n - 2^n) - n
def v2(x):
    if x==0: return 999
    r=0
    while x&1==0: x>>=1; r+=1
    return r
ok2=all( (v2(cs[n]-1) if cs[n]>1 else 0) == v2(8*3**n - Ss[n] - 2**n)-n for n in range(2,300))
print(f"depth_n = v2(8*3^n - S_n - 2^n) - n  holds: {ok2}")
# (3) BAKER PROBE: a long odd-run (depth>=L) means c_n ≡ 1 mod 2^L. Is c_n ever close to 2^m+1 (powers)?
#     measure: min over n of |c_n - nearest (2^m + 1)| / c_n -- if bounded below, depth bounded.
#     Actually: depth_n = trailing zeros of c_n - 1; check if depth_n is ever close to log2(c_n).
print("\ndepth_n vs log2(c_n) (trivial bound depth<=log2 c_n ~ 0.585n):")
maxratio=0
for n in range(2,N):
    d=v2(cs[n]-1) if cs[n]>1 else 0
    lg=math.log2(cs[n]) if cs[n]>1 else 1
    maxratio=max(maxratio, d/lg)
print(f"  max over n<{N} of depth_n/log2(c_n) = {maxratio:.4f}  (1.0 would saturate the trivial bound)")
print(f"  i.e. depth stays below {maxratio:.3f}*log2(c_n) empirically; trivial proof only gives <1.0")
# (4) the SELF-REFERENCE obstacle: depth_n depends on S_n (low bits), S_n depends on the parity history.
#     Show: v2(8*3^n - S_n - 2^n) -- the carry into bit (n+depth) -- needs S_n's bits, = parity history.
print("\nself-reference: S_n = sum_{j<n, c_j odd} 2^j 3^{n-1-j}  (carries the WHOLE parity history)")
print("=> the depth at step n is a function of which earlier c_j were odd = exactly what we want to bound.")
print("   Baker bounds |3^n - 2^m| (c_n away from powers of 2) UNCONDITIONALLY, but the depth condition")
print("   involves S_n not c_n alone => Baker does not directly apply. The S_n self-reference is the wall.")
