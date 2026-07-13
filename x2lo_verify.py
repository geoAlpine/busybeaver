import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
TT = {('A',0):(1,+1,'B'),('A',1):(0,+1,'E'),('B',0):(1,+1,'C'),('B',1):None,
      ('C',0):(0,-1,'D'),('C',1):(1,-1,'E'),('D',0):(0,+1,'E'),('D',1):(1,-1,'D'),
      ('E',0):(1,+1,'F'),('E',1):(0,-1,'C'),('F',0):(0,+1,'A'),('F',1):(1,+1,'E')}
# Lean zipper reimplementation with a SYMBOLIC tail sentinel 'B'(=b) then 'R' (rest).
# right = list of cells; when we need to read past concrete cells we hit sentinel -> ERROR (should not happen pre-step250)
class Z:
    def __init__(self,st,pos,left,head,right):
        self.st=st;self.pos=pos;self.left=list(left);self.head=head;self.right=list(right)
    def step(self):
        assert self.head in (0,1), f"read symbolic {self.head} at pos {self.pos}!"
        t=TT[(self.st,self.head)]
        if t is None: return False
        w,mv,ns=t
        self.head=w
        if mv==+1:
            self.left.insert(0,self.head)  # nearest-first: push front
            if self.right: self.head=self.right.pop(0)
            else: self.head=0
        else:
            self.right.insert(0,self.head)
            if self.left: self.head=self.left.pop(0)
            else: self.head=0
        self.st=ns;self.pos+=mv;return True

# START as in the Lean theorem: E,0, left [], head 0, right = 0^21,1,0^6,1,0^6 then (b::R)
# We put a big REAL tail (from build(4)) so reads are safe, but track that head never reaches pos36.
sim=build(4)
realbits=[sim.h]+sim.R[::-1]   # abs pos i -> realbits[i]
# right for Lean start = pos1..end
right0=realbits[1:]
z=Z('E',0,[],realbits[0],right0)
snaps={}
maxpos=0
for k in range(251):
    if k in (0,50,100,150,200,250): snaps[k]=('%s'%z.st, z.pos, list(z.left), z.head, list(z.right))
    maxpos=max(maxpos,z.pos)
    if k<250: z.step()
print("maxpos reached in 0..250:",maxpos, "(must be <36 for symbolic safety)")
# Now emit each chunk with symbolic tail: for a snapshot at step k with head pos p<36,
# the concrete right prefix = cells pos p+1..35, then (b::R). left/head concrete.
def leanlist(bs): return "["+", ".join("true" if x else "false" for x in bs)+"]"
def emit(k):
    st,pos,left,head,right=snaps[k]
    if pos<36:
        # right currently = cells pos+1.. (real). Keep only pos+1..35, replace rest with b::R
        keep=35-pos  # number of concrete cells pos+1..35
        rp=right[:keep]
        rterm = f"({leanlist(rp)} ++ (b :: R))" if rp else "(b :: R)"
        h = "true" if head else "false"
    else:
        rterm="R"; h="b"
    return f"⟨.{st}, {pos}, ⟨{leanlist(left)}, {h}, {rterm}⟩⟩", (st,pos,left,head)
# verify chunk self-consistency: run 50 steps from snap k (with symbolic tail) reach snap k+50
for k in [0,50,100,150,200]:
    st,pos,left,head,right=snaps[k]
    keep=35-pos
    rp=right[:keep]
    # symbolic tail: append a marker we can check isn't read; use real tail beyond for running
    tail_real=right[keep:]  # real cells pos36+
    z2=Z(st,pos,left,head,rp+tail_real)
    ok=True
    for _ in range(50):
        if z2.pos>=36: ok=False  # would read symbolic region
        z2.step()
    tst,tp,tl,th,tr=snaps[k+50]
    match = (z2.st==tst and z2.pos==tp and z2.left==tl and (z2.head==th if tp<36 else True))
    print(f"chunk {k}->{k+50}: head-stays<36 in region ok={ok}  endmatch={match}")
print()
for k in [0,50,100,150,200,250]:
    term,_=emit(k); print(f"C{k} = {term}")
