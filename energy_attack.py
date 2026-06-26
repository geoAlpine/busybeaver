"""Phase 2: attack avgD_odd >= 3/2 with a SECOND-MOMENT / ENERGY method.
avgD_odd = sum_{k>=1} P(D_i>=k | odd), D_i=v2(3c_i-1). For odd c_i: c_i==1 mod4 -> D=1; c_i==3 mod4 -> D>=2.
With chi = chi_{-4} the nontrivial char mod 4 (chi(1)=+1, chi(3)=-1):
  1[D_i>=2] = (1 - chi(c_i))/2,  so  P(D>=2|odd) = 1/2 - (1/2) avgchi_odd,
  avgD_odd = 1 + P(D>=2|odd) + [deeper terms >=0] = 3/2 - (1/2) avgchi_odd + (bonus>=0).
=> NON-HALT (avgD_odd>=3/2, asymptotic) is IMPLIED by the ONE-SIDED CHARACTER SUM
        S_n := sum_{odd i<n} chi_{-4}(c_i) <= 0   (running),
   and more weakly by avgchi_odd <= 2*(deeper-cylinder bonus). A character sum is the natural home of
   second-moment / large-sieve methods. We test what energy can and cannot do.

ENERGY = the symmetric quadratic form. Additive-energy / collision count at depth 2:
   Energy = #{(i,j) odd: c_i==c_j mod4} = N1^2 + N3^2   (N_r=#odd i with c_i==r mod4, N1+N3=O_n).
Cauchy-Schwarz: N1^2+N3^2 >= O_n^2/2, equality iff N1=N3. Energy bounds |N3-N1| (=|S_n|) but is
SYMMETRIC in (N1,N3) -- it cannot see the SIGN of N3-N1, which is exactly what the criterion needs.
"""
import math
def v2(x):
    x=int(x); r=0
    if x==0: return 10**9
    while x&1==0: x>>=1; r+=1
    return r
def chi4(c):  # nontrivial Dirichlet character mod 4 on odds: +1 if c==1 mod4, -1 if c==3 mod4
    return 1 if c%4==1 else -1

N=300_000
VMASK=(1<<48)-1                 # low bits suffice for v2(3c-1) (capped) and c mod 4
c=8
O=0; S=0; sumD=0
N1=0; N3=0
checkpoints=[10**3,10**4,10**5,3*10**5]
print("="*80)
print("Energy / character-sum attack on  avgD_odd >= 3/2  (Antihydra seed 8)")
print("="*80)
for n in range(1,N+1):
    if c&1:  # odd step
        O+=1; d=v2((3*(c & VMASK)-1) & VMASK); sumD+=d   # v2(3c-1) from low bits (cheap)
        if (c & 3)==1: N1+=1; S+=1     # chi(1)=+1
        else: N3+=1; S-=1              # chi(3)=-1
    c=(3*c)//2
    if n in checkpoints:
        avgD=sumD/O
        avgchi=S/O
        # avgD_odd vs the mod-4 lower bound 3/2 - 1/2 avgchi
        lb=1.5 - 0.5*avgchi
        energy=N1*N1+N3*N3
        emin=O*O/2
        print(f"\nn={n}:  O_n={O}  avgD_odd={avgD:.5f}  (non-halt needs >=1.5)")
        print(f"   character sum  S_n = N3... wait S=sum chi = N1-N3 = {S}   (suff cond for non-halt: S_n<=0)")
        print(f"   avgchi_odd={avgchi:+.5f}   mod-4 lower bound 3/2-avgchi/2 = {lb:.5f}  (<=avgD_odd: {lb<=avgD+1e-9})")
        print(f"   |S_n|={abs(S)}   vs sqrt(O_n)={math.sqrt(O):.1f}  ratio={abs(S)/math.sqrt(O):.3f}  (sqrt-cancellation?)")
        print(f"   ENERGY N1^2+N3^2={energy}  Cauchy-Schwarz min O^2/2={emin:.0f}  excess={energy-emin:.0f}")
        print(f"   excess energy = (N3-N1)^2/2 = S^2/2 = {S*S/2:.0f}  (check: {energy-emin:.0f})")

print("\n" + "="*80)
print("FINDINGS")
print("="*80)
print("1. avgD_odd >= 3/2 - (1/2) avgchi_odd  (+ deeper-cylinder bonus >=0), exact decomposition.")
print("   => non-halt is implied by the ONE-SIDED character sum  S_n = sum_{odd} chi_{-4}(c_i) <= 0.")
print("2. ENERGY = N1^2+N3^2 = O^2/2 + S^2/2. The energy's only orbit-dependent part is S^2 = |imbalance|^2")
print("   -- it pins |S_n| but is SYMMETRIC in (N1,N3): it CANNOT determine the SIGN of S_n = N1-N3.")
print("   The criterion needs the SIGN (S_n<=0). => second-moment/energy is STRUCTURALLY sign-blind here.")
print("3. Empirically |S_n| ~ sqrt(O_n) (square-root cancellation, sign fluctuating) -- so the energy IS")
print("   at the random rate (excess energy ~ O_n, i.e. S^2 ~ O_n). A near-random energy gives")
print("   avgchi_odd = O(1/sqrt n) -> avgD_odd -> 2 (margin holds) -- BUT proving the energy is random-rate")
print("   (|S_n|=o(n)) is itself the single-orbit equidistribution of chi_{-4}(c_i). So energy reduces the")
print("   wall to a SIGNED square-root-cancellation of a character sum it cannot itself certify or sign.")
print("CONCLUSION: second-moment/energy (a) reduces the target to one character sum S_n<=0, (b) is sign-blind")
print("so cannot deliver the one-sided bound, (c) and the magnitude bound it WOULD give (|S_n|=o(n)) is the")
print("equidistribution input. The natural escalation is large-sieve / exponential-sum cancellation for the")
print("SPECIFIED orbit chi_{-4}(c_i) -- the analytic-NT door, now precisely posed.")
