import numpy as np, math
N=300000
c=8; D=[]
def v2(x):
    r=0
    while x and x&1==0: x>>=1; r+=1
    return r
cps=[]
for n in range(N):
    if c%2==0:
        cp=c//2; cps.append(cp); D.append(v2(3*cp-1))
    c=3*c//2
D=np.array(D); J=len(D); SD=D.sum()
print(f"J={J} cycles, Sigma D_j = {SD} (= odd steps); even-density={J/(J+SD):.4f}")
# (1) PIGEONHOLE: #{D_j>=k} <= (Sigma D_j)/k  [a height-k jump uses k odd steps]. Is it better than Markov?
print("\n(1) pigeonhole #{D_j>=k} vs (Sigma D)/k  [Markov] vs J/2^k [equidist]:")
for k in (1,2,4,8,16):
    cnt=np.sum(D>=k)
    print(f"  k={k:2d}: actual={cnt:6d}  Markov bound (SD/k)={SD/k:9.0f}  equidist J/2^k={J/2**k:8.0f}")
print("  => Markov bound #{D>=k}<=SD/k is just the identity Sigma D=Sum #{D>=k}; gives NO new constraint on SD.")

# (2) GROWTH/Lyapunov: induced orbit growth log2(c'_{j+1})-log2(c'_j) = 0.585*(D_j+1). Bounded average <=> target.
dl=np.diff(np.log2(np.array(cps,dtype=float)))
print(f"\n(2) induced-orbit growth per step log2(c'): mean={dl.mean():.4f} = 0.585*(avg D+1)={0.585*(D.mean()+1):.4f}")
print(f"  target 'Sigma D=O(J)' <=> 'c'_J grows <= exp(O(J))' <=> bounded avg growth -- but the trivial")
print(f"  depth<=0.585*pos allows per-step factor (3/2)^(D+1) UNBOUNDED (large D) => no unconditional bound.")

# (3) ADVERSARIAL: does a Lyapunov function exist? Earlier min-mean-cycle gave adversarial even-density=0,
#     i.e. NO finite-state Lyapunov certificate forces avg D<=2. Confirm the obstruction is genuine.
print("\n(3) Lyapunov: a finite-state Lyapunov bound is PROVABLY impossible (earlier: adversarial min even-density=0).")
print("  So no crude finite-state energy/Lyapunov argument gives avg D<=2 unconditionally.")
print("\nROUTE B (crude methods) VERDICT [honest]: Markov auto-consistent (no constraint); growth parity-blind;")
print("  Lyapunov provably impossible (finite-state). The 250x margin is real but no crude method reaches even")
print("  the weak target Sigma v2(3c'-1)=O(J). The target = 'induced orbit grows <= exp(O(J))' = positive")
print("  density, still open. A genuinely new (non-crude, coupling-respecting) idea is needed.")
