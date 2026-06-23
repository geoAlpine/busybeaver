import math
# width grows ~(8/3)^k; tail sum of 1/width converges. Compute via logs.
# N_7 = 10373 (verified). N_k ~ N_7 * (8/3)^(k-7).
logN7=math.log(10373); r=math.log(8/3)
tail=0.0
for k in range(7,400):
    logw=logN7+(k-7)*r
    tail+=math.exp(-logw)
print(f"sum_{{k>=7}} 1/N_k = {tail:.6e}")
print(f"  geometric: (1/N_7)/(1-3/8) = {(1/10373)/(1-3/8):.6e}")
print()
print("HEURISTIC MODEL for o18 (parallels Antihydra's even-density argument):")
print("- ideal orbit base-3 digit-2 density = 1/3 (equidistributed, verified numerically)")
print("- a halt needs an interior F-read (only during a defect epoch) to align with a residual 1")
print("- P(alignment at epoch k) ~ O(1/N_k) since the F-read position vs tail-1 is ~1-in-width")
print(f"- sum_k P(align) ~ {tail:.2e} << 1  => expected # of halt-alignments after epoch 7 ~ 0")
print("=> Borel-Cantelli HEURISTIC: o18 almost surely NON-HALTS. (NOT a proof: same wall as Antihydra.)")
print()
print("Why it is NOT a proof (the irreducible gap):")
print("- B-C needs INDEPENDENCE of the alignment events; here positions are DETERMINED by the orbit's")
print("  base-3 carries, not random. Proving non-alignment = proving a specific digit of a x(8/3) orbit")
print("  never lands at a self-referential spot = the Erdos-class ternary-digit statement. Open.")
