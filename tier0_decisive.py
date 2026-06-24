import numpy as np, math
# DECISIVE TEST: feed the cascade's top injection with a PROVEN-equidistributed ROTATION sequence
# (the kind Benford/Weyl gives for the real orbit's top bits) instead of independent random bits.
# If parity still decorrelates => proven top (Benford) drives parity equidist via the cascade => REAL PATH.
theta=math.log2(3.0)  # the actual rotation governing the orbit's leading bits (proven equidistributed)
def cascade(depth, T, top_source):
    s=8 % (1<<depth); par=[]
    for t in range(T):
        par.append(s&1)
        tb=top_source(t)
        s = (s & ((1<<(depth-1))-1)) | (tb<<(depth-1))
        s = (3*s)//2 % (1<<depth)
    par=np.array(par,float)
    m=par.mean(); ac=np.mean((par[:-1]-m)*(par[1:]-m))/(par.var()+1e-12)
    # also lag-2,3 autocorr
    acs=[np.mean((par[:-l]-m)*(par[l:]-m))/(par.var()+1e-12) for l in (1,2,3)]
    return 1-m, acs   # even-density, autocorrs
T=300000
# top sources:
import random; random.seed(0)
src_rand = lambda t: random.getrandbits(1)
# rotation top bit: bit of {t*theta} -- proven equidistributed (Weyl). top bit = floor(2*frac(t*theta))
src_rot  = lambda t: int(2*((t*theta)%1.0))&1
# a STRUCTURED/correlated bad source (constant) for contrast
src_bad  = lambda t: 1 if (t%3==0) else 0   # periodic = NOT equidistributed-as-needed
for depth in (16,24):
    e_r,ac_r=cascade(depth,T,src_rand)
    e_o,ac_o=cascade(depth,T,src_rot)
    e_b,ac_b=cascade(depth,T,src_bad)
    print(f"depth={depth}:")
    print(f"  independent-random top : even-density={e_r:.4f} autocorr={[round(x,4) for x in ac_r]}")
    print(f"  ROTATION top (Benford) : even-density={e_o:.4f} autocorr={[round(x,4) for x in ac_o]}  <-- PROVEN source")
    print(f"  periodic-bad top       : even-density={e_b:.4f} autocorr={[round(x,4) for x in ac_b]}")
print("\n=> if ROTATION-top gives even-density>1/3 (ideally ~0.5) & decorrelated, MATCHING random-top,")
print("   then the PROVEN Benford equidistribution of the top, via the cascade, FORCES even-density>1/3.")
print("   That would be a genuine reduction of Antihydra non-halt to BENFORD (proven) -- a real crack.")
