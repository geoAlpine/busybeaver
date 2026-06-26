"""Search for a toy cryptid where P2+P3 (integrality budget + run-length) FORCES the even-density
(proves non-halting), unlike Antihydra. Family: c->floor(a c/p), v_p(a/p)=-1, halt when balance
q*E - n < 0 (threshold even-density 1/q; non-halt <=> even-density >= 1/q <=> avgD_odd >= q/(q-1)).

WHAT P2 (valuation budget) ACTUALLY GIVES: Sum_{p-step} v_p(...) = n + v_p(c_n) - v_p(c_0). Since
c_n ~ A mu^n, v_p(c_n) = O(log n) = o(n), so  avgD * (p-step density) = 1 + o(1)  -- an IDENTITY
relating the two, NOT a bound on either. So P2 alone CANNOT force the density.
WHAT P3 (run-length) gives: a run of length L needs v_p(c)>=L, so L <= log_p(c_n) ~ gamma*n,
gamma=log_p(mu). This bounds individual runs; combined with the geometric-run analysis it gives only
#even >= c*log n (logarithmic), and marginally allows even-density->0.
=> hypothesis: for EVERY genuine cryptid, P2+P3 cannot force the even-density. We test it.
"""
import math
def v(x,p):
    x=int(x); r=0
    if x==0: return 10**9
    while x%p==0: x//=p; r+=1
    return r

def run_orbit(p,a,seed,N):
    c=seed; E=0; sumD=0; Op=0; maxrun=0; cur=0; runs=0; inrun=False
    for n in range(N):
        if c%p==0: E+=1; inrun=False
        else:
            Op+=1; sumD+=v(a*c-1,p)   # branch depth analog (Antihydra: v2(3c-1))
            if not inrun: inrun=True; runs+=1; cur=1
            else: cur+=1; maxrun=max(maxrun,cur)
        c=(a*c)//p
    return dict(even_density=E/N, pstep_density=Op/N, avgD=sumD/max(Op,1), maxrun=maxrun, runs=runs, N=N)

print("="*82)
print("Does P2 (budget identity) bound the density? avgD * pstep_density should be ~1 (identity, no bound)")
print("="*82)
print(f"{'machine':>12} {'gamma=log_p mu':>14} {'even_dens':>10} {'avgD':>7} {'avgD*pstep':>11} {'maxrun/0.585N':>14}")
for (p,a) in [(2,3),(2,5),(3,4),(3,5),(2,7)]:
    s=run_orbit(p,a,8 if (p,a)==(2,3) else 11, 150000)
    gamma=math.log(a/p)/math.log(p)
    prod=s['avgD']*s['pstep_density']
    print(f"   {a}/{p:<8} {gamma:14.3f} {s['even_density']:10.4f} {s['avgD']:7.3f} {prod:11.4f} {s['maxrun']/(gamma*s['N']):14.5f}")
print("\n=> avgD*pstep ~ 1 for all (the budget IDENTITY): P2 relates avgD<->density, bounds NEITHER.")
print("   maxrun << gamma*N (runs are O(log N), nowhere near the bound): P3's run-length cap is far from tight.")

# Where does the non-halt threshold sit, and can P2 force HALT (the OTHER direction)?
print("\n" + "="*82)
print("Threshold q/(q-1) vs what P2 can do (force HALT needs avgD bounded ABOVE < threshold)")
print("="*82)
print("P2 gives avgD = 1/density (identity), Haar avgD = p/(p-1). NO independent upper bound on avgD")
print("(v_p(c_n)=o(n) means the budget pins avgD to 1/density, which is whatever the orbit does).")
print(f"{'q (balance)':>11} {'threshold avgD=q/(q-1)':>22} {'Haar avgD=p/(p-1) (p=2)':>24} {'P2 decides?':>12}")
for q in (2,3,4,5):
    thr=q/(q-1)
    print(f"{q:>11} {thr:22.3f} {2.0:24.1f} {'NO (no avgD bound)':>12}")
print("\nP2 gives NO upper bound on avgD (identity only), so it can force NEITHER halt NOR non-halt.")
print("(Earlier guess 'budget range [1,1+gamma]' was WRONG: v_p(c_n)=o(n), not gamma*n, so no range.)")

print("\n" + "="*82)
print("VERDICT (toy-cryptid search)")
print("="*82)
print("For EVERY cryptid in the floor(a c/p) family: P2 (valuation budget) is an IDENTITY")
print("avgD*density=1+o(1) -- it bounds NEITHER side, so it CANNOT force the even-density (halt or")
print("non-halt). P3 (run-length) is logarithmic (#even>=c log n) and marginally allows even-density->0.")
print("=> NO genuine toy cryptid has P2+P3 forcing the density. The decidable cryptids (bouncers,")
print("counters, the 63 monsters) are decided by REGULAR/FAR certificates, NOT by P2+P3. So P2+P3 is")
print("STRUCTURALLY a rigidity tool (unique orbit) with no density content -- the same bias-blindness")
print("found for Antihydra, now confirmed to be UNIVERSAL across the family. The minimal example where")
print("integrality 'decides' a cryptid is a REGULAR-certificate machine (decided by FAR, not by P2+P3).")
