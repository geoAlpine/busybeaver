# Verify the EXACT halt criterion. Reviewer's point: non-halt <=> depth=o(n) is overstated.
# The true criterion is about the BALANCE 3E_n - n >= 0 (halt when balance reaches -1).
N=100000
c=8; E=0; balance_min=999; running_density_min=1.0
for n in range(N):
    if n>0:
        bal=3*E-n
        balance_min=min(balance_min,bal)
        running_density_min=min(running_density_min, E/n)
    if c%2==0: E+=1
    c=3*c//2
print(f"exact criterion: non-halt <=> balance_n = 3E_n - n >= 0 for ALL n  <=>  running even-density E_n/n >= 1/3 for ALL n")
print(f"  over n<{N}: min balance = {balance_min}  (>=0 => still non-halting so far)")
print(f"  min running even-density E_n/n = {running_density_min:.4f}  (>= 1/3 = {1/3:.4f}? {running_density_min>=1/3})")
print()
print("REVIEWER IS RIGHT:")
print(" - non-halt <=> (3E_n - n >= 0 for ALL n) = running even-density >= 1/3 at EVERY prefix.")
print(" - 'depth = o(n)' is NOT equivalent: it is part of a SUFFICIENT heuristic (via the v2/odd-run analysis),")
print("   and non-halt does NOT force depth sublinear. The <=> chain conflated sufficient conditions.")
print(" - Correct framing: equidistribution / depth=o(n) ==> (heuristically) running density >1/3 ==> non-halt.")
print("   These are SUFFICIENT, not equivalent. (H) REDUCES to / IS SUFFICIENT FOR non-halt, not <=>.")
