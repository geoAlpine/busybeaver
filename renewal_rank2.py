# Rank-2 search in the renewal structure: branch maps f_D=(3/2)^{D+1}x+s_D are NON-abelian but generate a
# SOLVABLE (metabelian) group Z[1/6] >| <3/2> => AMENABLE => no spectral gap => no rank-2 leverage. Wall=amenability.
from fractions import Fraction as Fr
def fD(D): return (Fr(3)**(D+1)/Fr(2)**(D+1), (Fr(2)**D-Fr(3)**D)/Fr(2)**(D+1))
def comp(f,g): (af,sf),(ag,sg)=f,g; return (af*ag, af*sg+sf)
A=comp(fD(0),fD(1)); B=comp(fD(1),fD(0))
print(f"f0∘f1={A}, f1∘f0={B}, non-abelian: {A!=B} (same linear 27/8, different shift)")
print("group generated = Z[1/6] >| <3/2> = SOLVABLE/metabelian => AMENABLE => no spectral gap/expansion.")
print("=> renewal non-abelianness is AMENABLE (wrong kind); no effective rank-2. The wall is amenability.")
