"""Attack H(d,C) at the LOWEST modulus (conductor 4, chi_{-4}). The character sum
   S_2(N) = sum_{n<N} chi_{-4}(c_n)[c_n odd] = N_1 - N_3   (counts of c_n == 1, 3 mod 4).
EXACT COMBINATORIAL FORMULA (derived from the odd-run lemma): in a maximal odd run of length L
(L = v2(c_start - 1), proven), the members have v2(member - 1) = L, L-1, ..., 1; since c == 1 mod 4
iff v2(c-1)>=2 and c == 3 mod 4 iff v2(c-1)=1, each run contributes (L-1) ones and exactly 1 three.
Hence
   N_1 = sum_runs (L_run - 1) = O - #runs,   N_3 = #runs,   so   S_2 = O - 2*#runs,
where O = #odd steps, #runs = number of maximal odd runs. Therefore
   S_2/O = 1 - 2/avgL,  avgL = O/#runs = average odd-run length,
and  H at conductor 4  (|S_2| = o(N))  <=>  avgL -> 2  (and the favorable sign S_2<=0 <=> avgL<=2).
We verify the exact formula and measure avgL.
"""
import math

def v2(x):
    x=int(x); r=0
    if x==0: return 60
    while x&1==0 and r<60: x>>=1; r+=1
    return r

N=300_000
c=8
O=0; N1=0; N3=0; runs=0; in_run=False
run_lengths=[]; cur=0
for _ in range(N):
    if c&1:                       # odd
        O+=1
        if (c&3)==1: N1+=1
        else: N3+=1
        if not in_run:
            in_run=True; runs+=1; cur=1
        else:
            cur+=1
    else:
        if in_run: run_lengths.append(cur); in_run=False
    c=(3*c)//2
if in_run: run_lengths.append(cur)

S2=N1-N3
print("="*76)
print(f"H at the lowest modulus (chi_{{-4}}, conductor 4)   N={N}, O={O} odd steps")
print("="*76)
print(f"\nN_1 (c==1 mod4) = {N1}   N_3 (c==3 mod4) = {N3}   S_2 = N_1-N_3 = {S2}")
print(f"#odd-runs = {runs}")
print(f"\nEXACT FORMULA  S_2 = O - 2*#runs:  {O} - 2*{runs} = {O-2*runs}   matches S_2={S2}: {O-2*runs==S2}")
print(f"check N_1 = O - #runs: {O-runs} == {N1}: {O-runs==N1}   N_3 = #runs: {runs}=={N3}: {runs==N3}")

avgL=O/runs
print(f"\navg odd-run length avgL = O/#runs = {avgL:.5f}")
print(f"S_2/O = 1 - 2/avgL = {1-2/avgL:+.5f}   (measured S_2/O = {S2/O:+.5f}: {abs((1-2/avgL)-S2/O)<1e-9})")
print(f"|S_2| = {abs(S2)}   vs sqrt(O) = {math.sqrt(O):.0f}  (power-saving if O(sqrt): ratio {abs(S2)/math.sqrt(O):.3f})")

# run-length distribution (should be ~ geometric mean 2 under Haar)
from collections import Counter
rc=Counter(run_lengths)
print(f"\nodd-run length distribution (Haar = geometric, P(L=k)=2^-k, mean 2):")
for k in range(1,9):
    print(f"  L={k}: {rc.get(k,0):>7}  freq {rc.get(k,0)/runs:.4f}  (Haar 2^-{k}={2.0**-k:.4f})")

print("\n" + "="*76)
print("VERDICT (honest)")
print("="*76)
print("EXACT reduction: H at conductor 4  <=>  avgL -> 2  (average odd-run length).")
print("This is the MOST ELEMENTARY form of the lowest-modulus character sum -- a count of odd-runs,")
print("not an abstract character sum. avgL = average of v2(c_start-1) over run-starts; a run-start is")
print("an odd value right after an even step, so avgL is a 2-adic statistic of the EVEN subsequence.")
print("It still FUNNELS: avgL->2 is the single-orbit equidistribution of v2(c-1) at run-starts (no")
print("current tool gives even avgL=2+o(1) for the specified orbit). BUT the reduction is genuine and")
print("clean -- it recasts H(conductor 4) as a run-length law, the combinatorially simplest target,")
print("and exposes the favorable-sign criterion S_2<=0 <=> avgL<=2 (odd runs not too short).")
print("(Identification: S_2 also = the moving diagonal digit -- bits n,n+1 of 3^n c_0 - T_n -- so")
print("conductor 4 IS the moving-middle-digit/Mahler core; no unconditional sub-trivial bound exists.)")
