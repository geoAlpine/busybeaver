# Ideal orbit N_{k+1}=floor(8N/3)+2; analyze base-3 digit structure as a defect model.
def b3digits(n):
    d=[]
    while n: d.append(n%3); n//=3
    return d[::-1]  # high to low
N=10
orbit=[N]
for _ in range(4000):
    N=(8*N)//3+2
    orbit.append(N)
# digit-2 density across the orbit's base-3 expansions
tot2=tot=0
trailing=[]   # the low base-3 digits (defect-relevant region)
for N in orbit[100:]:   # skip transient
    ds=b3digits(N)
    tot2+=ds.count(2); tot+=len(ds)
    trailing.append(tuple(ds[-4:]))  # last 4 digits
print(f"digit-2 density in base-3 of ideal orbit: {tot2/tot:.4f}  (random base-3 would be 1/3=.333)")
# how often does the LOW end (units region) have a 2 -- the carry/defect trigger?
from collections import Counter
units=Counter(b3digits(N)[-1] for N in orbit[100:])
print("units digit distribution:", dict(units))
low2=Counter(b3digits(N)[-2] for N in orbit[100:] if len(b3digits(N))>=2)
print("second-lowest digit distribution:", dict(low2))
# A defect (interior 0 / dropped +2) occurred when units digit pattern caused a carry.
# Model: estimate density of epochs where a carry-defect forms.
# Heuristic halt: defect forms with density p, and F-read aligns with prob ~1/width -> sum 1/width converges
# => only finitely many alignment chances if width grows geometrically => HEURISTIC NON-HALT.
import math
widths=orbit
tail_sum=sum(1.0/w for w in widths[7:])  # P(align) ~ c/width each defect epoch
print(f"\nsum of 1/width over epochs >=7: {tail_sum:.4f}  (finite => Borel-Cantelli: finitely many halt-chances)")
print(f"  geometric ratio 8/3 => sum_{{k}} (3/8)^k converges; expected # alignments after epoch 7 ~ O(1/N_7)={1/widths[7]:.2e}")
print("=> HEURISTIC: o18 almost surely NON-HALTS (alignment prob sums to ~0). NOT a proof.")
