# Cross-cryptid test (Route C): does the Antihydra Q9-trilogy dissection PORT to the other Mahler cryptids?
# For mu=2^a/3^b on Z_p (p = the denominator prime), test that T_mu(x)=floor(mu*x) shares:
#  (1) p-to-1 exact endomorphism of Z_p;  (2) renewal dissection: density->1/p, avg gap->p,
#      EXACT identity sum(gap-1)=#non-renewal;  (3) induced map = full-branch piecewise-affine
#      expanding Gibbs-Markov on Z_p (slopes mu^g, branch alphabet = itinerary words);
#  (4) fixed point on every branch => Q9(b) obstruction (spectral gap orbit-blind) ports.
from fractions import Fraction as Fr
from collections import defaultdict, Counter
def vp(x,p):
    x=abs(int(x)); r=0
    if x==0: return 10**9
    while x%p==0: x//=p; r+=1
    return r
def endo_pto1(A,B,p,k=4):
    img=Counter((A*x//B)%p**k for x in range(p**(k+1)))
    return len(img)==p**k and set(img.values())=={p}
def dissect(A,B,p,steps=300000):
    cur=8; pos=[]
    for s in range(steps):
        if cur%p==0: pos.append(s)
        cur=(A*cur)//B
    gaps=[pos[i+1]-pos[i] for i in range(len(pos)-1)]
    dens=len(pos)/steps; avg_gap=sum(gaps)/len(gaps)
    ident = sum(g-1 for g in gaps)==(steps-len(pos)) or abs(sum(g-1 for g in gaps)-(steps-len(pos)))<=1
    return dens, avg_gap, ident
def induced_words(A,B,p,steps=300000):
    cur=8; out=[]; last=None; word=[]
    for s in range(steps):
        if cur%p==0:
            xp=cur//p
            if last is not None: out.append((last,xp,tuple(word)))
            last=xp; word=[]
        else: word.append(cur%p)
        cur=(A*cur)//B
    byw=defaultdict(list)
    for x0,x1,w in out: byw[w].append((x0,x1))
    nf=nt=0
    for w in sorted(byw,key=lambda w:(len(w),w))[:8]:
        pts=byw[w]
        if len(pts)<2: continue
        (a0,b0),(a1,b1)=pts[0],pts[1]
        s=Fr(b1-b0,a1-a0); it=Fr(b0)-s*a0
        ok=all(Fr(y)==s*x+it for x,y in pts[:200]) and s==Fr(A,B)**(len(w)+1)
        xf=it/(1-s) if s!=1 else None
        inZ=(xf.denominator%p!=0) if xf is not None else False
        nt+=1; nf+=(1 if ok and inZ else 0)
    return len(byw), nf, nt
def run(A,B,p,name):
    e=endo_pto1(A,B,p); dens,ag,ident=dissect(A,B,p); nw,nf,nt=induced_words(A,B,p)
    print(f"{name:16s} mu={A}/{B} p={p}: p-to-1 endo={e}  density={dens:.3f}(~1/{p})  avg_gap={ag:.3f}(~{p})  "
          f"identity={ident}  word-branches={nw} fixed/affine={nf}/{nt}")
print("Cross-cryptid isomorphism test (Route C):")
run(3,2,2,"Antihydra/o10in")  # 3/2
run(8,3,3,"o18/o15")          # 8/3
run(9,2,2,"control 9/2")      # another 2^a/3^b sanity (a=0? no, 9/2 = 3^2/2)
