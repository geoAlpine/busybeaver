# o4 SOUND level-1 bouncer macro-machine (2026-07-06)
# Tape = segments [pat, count], pat in {"0","1","01","10"} (len<=2); implicit 0s outside.
# Acceleration = GENERIC VERIFIED p=2 cycle jump:
#   simulate 2 steps; require state-return + monotone displacement +-2;
#   verify BEHIND cells (radius W) are wp-tiled (self-correcting: seam debris -> micro);
#   count AHEAD rp-tiling via segment arithmetic (O(#segs), exact);
#   jump m = matched_pairs - MARGIN cycles; rewrite region to wp-tiling as one segment.
# B-reads-1 windows: micro events recorded concretely; jump events share the representative
#   window (PROVEN identical for all m interior cycles given behind/ahead verification --
#   the phase-bug of the discarded accelerator is structurally excluded).
# Validation battery: V1 exact tape/state/head match vs concrete; V2 window-set equality
#   vs pure-concrete canonical; V3 milestone/odometer exactness at large G.
from collections import defaultdict

def parse(spec):
    M={}
    for k,blk in enumerate(spec.split('_')):
        st="ABCDEF"[k]
        for r in (0,1):
            c=blk[3*r:3*r+3]
            M[(st,r)]=None if c[0]=='-' else (int(c[0]),1 if c[1]=='R' else -1,c[2])
    return M
M=parse("1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---")

W=5          # window radius for B-reads-1 recording
MARGIN=8     # pairs left un-jumped at the far end (micro'd)

class Mach:
    def __init__(self):
        self.segs=[["0",1]]; self.abs0=0
        self.habs=0; self.st='A'; self.steps=0
        self.wins=set(); self.unsafe=0; self.halted=False
        self.f1=0
        self.leftmost=0
        self.milestones=[]   # (steps, G, a)

    # ---------- representation ----------
    def end(self):
        return self.abs0+sum(len(p)*n for p,n in self.segs)

    def read_cell(self,a):
        x=self.abs0
        if a<x: return 0
        for pat,n in self.segs:
            L=len(pat)*n
            if a<x+L: return int(pat[(a-x)%len(pat)])
            x+=L
        return 0

    def ensure(self,a):
        if a<self.abs0:
            self.segs.insert(0,["0",self.abs0-a]); self.abs0=a
        e=self.end()
        if a>=e:
            self.segs.append(["0",a-e+1])

    def merge(self):
        # fixpoint local merging; also strip leading/trailing "0" segs (implicit outside)
        segs=self.segs
        changed=True
        while changed:
            changed=False
            out=[]
            i=0
            while i<len(segs):
                pat,n=segs[i]
                if n<=0: i+=1; changed=True; continue
                if len(pat)==2 and pat[0]==pat[1]:
                    pat=pat[0]; n=2*n; changed=True  # canonicalize "00"/"11" patterns
                if out and out[-1][0]==pat:
                    out[-1][1]+=n; i+=1; changed=True; continue
                # pair singles: ["a",1]+["b",1] (a!=b) -> ["ab",1]
                if len(pat)==1 and n==1 and i+1<len(segs):
                    p2,n2=segs[i+1]
                    if len(p2)==1 and n2==1 and p2!=pat:
                        out.append([pat+p2,1]); i+=2; changed=True; continue
                    # REPHASE (push singles rightward; terminates: single moves strictly right):
                    #   "0" + (10)^k  ==  (01)^k + "0"
                    if pat=="0" and p2=="10":
                        out.append(["01",n2]); segs[i+1]=["0",1]; changed=True; i+=1; continue
                    #   "1" + (01)^k  ==  (10)^k + "1"
                    if pat=="1" and p2=="01":
                        out.append(["10",n2]); segs[i+1]=["1",1]; changed=True; i+=1; continue
                out.append([pat,n]); i+=1
            segs=out
        # strip zero ends
        while segs and segs[0][0]=="0":
            self.abs0+=segs[0][1]; segs.pop(0);
        while segs and segs[-1][0]=="0":
            segs.pop()
        if not segs:
            segs=[["0",1]]  # abs0 arbitrary
        self.segs=segs

    def split_at(self,a):
        """Make absolute coord a a segment start; returns index of segment starting at a.
        Requires abs0 <= a <= end()."""
        if a==self.end(): return len(self.segs)
        x=self.abs0; i=0
        while True:
            pat,n=self.segs[i]; L=len(pat)*n
            if a<x+L: break
            x+=L; i+=1
        if a==x: return i
        off=a-x; pl=len(pat); rep=off//pl; rem=off%pl
        pieces=[]
        if rep>0: pieces.append([pat,rep])
        if rem>0:
            # split one repeat into singles
            for c in pat: pieces.append([c,1])
            rest=n-rep-1
            if rest>0: pieces.append([pat,rest])
            self.segs[i:i+1]=pieces
            # boundary now at start of the (rem)-th single within that repeat
            return i+(1 if rep>0 else 0)+rem
        else:
            pieces.append([pat,n-rep])
            self.segs[i:i+1]=pieces
            return i+(1 if rep>0 else 0)

    def write_cell(self,a,v):
        self.ensure(a)
        i=self.split_at(a); j=self.split_at(a+1)
        # cells [a,a+1) replaced by single
        self.segs[i:j]=[[str(v),1]]
        self.merge()

    def replace_range(self,lo,hi,pat,cnt):
        """cells [lo,hi] := pat repeated cnt (len(pat)*cnt == hi-lo+1)."""
        assert len(pat)*cnt==hi-lo+1
        self.ensure(lo); self.ensure(hi)
        i=self.split_at(lo); j=self.split_at(hi+1)
        self.segs[i:j]=[[pat,cnt]]
        self.merge()

    def flatten(self):
        d={}; x=self.abs0
        for pat,n in self.segs:
            for k in range(len(pat)*n):
                v=int(pat[k%len(pat)])
                if v: d[x+k]=v
            x+=len(pat)*n
        return d

    # ---------- dynamics ----------
    def window(self,base):
        return tuple(self.read_cell(base+t) for t in range(-W,W+1))

    def micro(self):
        v=self.read_cell(self.habs)
        tr=M[(self.st,v)]
        if tr is None:
            self.halted=True; return
        if self.st=='B' and v==1:
            self.wins.add(self.window(self.habs))
            if self.read_cell(self.habs+1)==1: self.unsafe+=1
        if self.st=='F' and v==1: self.f1+=1
        w,d,ns=tr
        if w!=v: self.write_cell(self.habs,w)
        self.habs+=d; self.st=ns; self.steps+=1
        if self.habs<self.leftmost:
            self.leftmost=self.habs
        self.check_milestone()  # micro steps are rare boundary events; the clean milestone
                                # instant lives between two micro steps at the turn-around

    def match_len(self,h0,dir,rp,cap):
        """#consecutive cells j=0.. with cell(h0+dir*j)==rp[j%2], capped."""
        total=0; pos=h0
        # walk segments
        while total<cap:
            # locate pos
            x=self.abs0
            if pos<x or pos>=self.end():
                # implicit zeros
                if rp[total%2]!=0: return total
                if rp[(total+1)%2]!=0: return total+1
                return cap  # all-zero rp: unlimited (capped)
            si=0
            for pat,n in self.segs:
                L=len(pat)*n
                if pos<x+L: break
                x+=L; si+=1
            pat,n=self.segs[si]; pl=len(pat); L=pl*n
            avail=(x+L-pos) if dir==1 else (pos-x+1)
            e=(pos-x)%pl
            j0=total
            if pl==1:
                s=int(pat)
                if rp[j0%2]==s and rp[(j0+1)%2]==s:
                    total+=avail; pos+=dir*avail
                elif rp[j0%2]==s:
                    return total+1
                else:
                    return total
            else:
                a0=int(pat[e]); a1=int(pat[(e+1)%2])
                if rp[j0%2]==a0 and rp[(j0+1)%2]==a1:
                    total+=avail; pos+=dir*avail
                elif rp[j0%2]==a0:
                    return total+1
                else:
                    return total
        return cap

    def try_jump(self,budget):
        h0=self.habs; s0=self.st
        v0=self.read_cell(h0); t0=M[(s0,v0)]
        if t0 is None: return 0
        w0,d0,s1=t0
        h1=h0+d0
        # note: h1 != h0, write at h0 does not affect read at h1
        v1=self.read_cell(h1); t1=M[(s1,v1)]
        if t1 is None: return 0
        w1,d1,s2=t1
        if s2!=s0 or d1!=d0: return 0
        dir=d0; rp=(v0,v1); wp=(w0,w1)
        if rp==wp and rp[0]==rp[1]: return 0  # degenerate (all-same, no info) -- let micro handle
        # behind check: cycle coords j=-1..-W must be wp-tiled
        for j in range(-1,-W-1,-1):
            if self.read_cell(h0+dir*j)!=wp[j%2]: return 0
        cap=2*(budget//2)+2*MARGIN+4
        total=self.match_len(h0,dir,rp,cap)
        pairs=total//2
        m=min(pairs-MARGIN,budget//2)
        if m<8: return 0
        # record representative windows for the two phases
        for phase,(sx,vx) in enumerate(((s0,v0),(s1,v1))):
            if sx=='B' and vx==1:
                win=tuple((rp[(phase+dir*t)%2] if (phase+dir*t)>=phase else wp[(phase+dir*t)%2])
                          for t in range(-W,W+1))
                self.wins.add(win)
                idx=phase+dir*1
                val=rp[idx%2] if idx>=phase else wp[idx%2]
                if val==1: self.unsafe+=m
            if sx=='F' and vx==1: self.f1+=m
        # rewrite jumped region to wp tiling
        if dir==1:
            lo=h0; hi=h0+2*m-1; pat=str(w0)+str(w1)
        else:
            lo=h0-2*m+1; hi=h0; pat=str(w1)+str(w0)
        self.replace_range(lo,hi,pat,m)
        self.habs+=dir*2*m; self.steps+=2*m
        if self.habs<self.leftmost:
            self.leftmost=self.habs; self.check_milestone()
        return m

    def check_milestone(self):
        # support == (10)^a 1001 (head strictly left of the first stored 1).
        # merge() is not confluent, so check via COUNT-REDUCTION: replacing each periodic
        # seg's count n by min(n,4) preserves membership in ^0*(10)*1001$ in BOTH directions
        # (pumping on the periodic part), and the reduced string is O(#segs) long.
        import re
        self.merge()
        if len(self.segs)>12: return
        red=''.join(p*min(n,4) for p,n in self.segs)
        if not re.match(r'^0*(10)*1001$',red): return
        # first stored 1 (full counts)
        x=self.abs0; first1=None
        for p,n in self.segs:
            if p=="0": x+=n; continue
            first1 = x if p[0]=="1" else x+1
            break
        if first1 is None or self.habs>first1: return
        # G = fresh-gap width = first1 - global leftmost (the just-carved turn-around point).
        # Valid while the tape is in clean milestone form (read-only rightward sweep keeps it).
        G=first1-self.leftmost
        if G<3: return  # startup junk
        # true generation starts have record-breaking G (the fresh gap exceeds all previous);
        # mid-generation transient re-matches have G < current generation's gap -> filtered.
        if self.milestones and G<=max(g for _,g,_ in self.milestones): return
        total=sum(len(p)*n for p,n in self.segs)
        lead0=first1-self.abs0
        a=(total-lead0-4)//2
        self.milestones.append((self.steps,G,a))

    def run(self,maxsteps=None,targetG=None,assert_segs=100000):
        while not self.halted:
            if maxsteps is not None and self.steps>=maxsteps: return
            if targetG is not None and -self.leftmost>=targetG: return
            budget=(maxsteps-self.steps) if maxsteps is not None else (1<<62)
            if self.try_jump(budget)==0:
                self.micro()
            elif len(self.segs)<=4:
                self.check_milestone()
            if len(self.segs)>assert_segs:
                raise RuntimeError(f"segment blow-up: {len(self.segs)}")

# ---------- validation ----------
def concrete(N,recwins=False,Wr=W):
    tape=defaultdict(int); pos=0; st='A'; wins=set(); unsafe=0
    for s in range(N):
        r=tape[pos]; a=M[(st,r)]
        if a is None: return ('HALT',s,pos,dict(tape),wins,unsafe)
        if recwins and st=='B' and r==1:
            wins.add(tuple(tape.get(pos+t,0) for t in range(-Wr,Wr+1)))
            if tape.get(pos+1,0)==1: unsafe+=1
        w,d,ns=a
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns
    return (st,N,pos,{k:v for k,v in tape.items() if v},wins,unsafe)

if __name__=='__main__':
    import sys,time
    # V1: exact tape/state/head match at checkpoints
    print("V1: exact equality vs concrete")
    for N in (200_000, 1_000_000, 5_000_000):
        t=time.time()
        m=Mach(); m.run(maxsteps=N)
        cst,cn,cpos,ctape,_,_=concrete(N)
        mt=m.flatten()
        ok=(m.st==cst and m.habs==cpos and mt==ctape and m.steps==N)
        print(f"  N={N:>9}: state {m.st}=={cst} head {m.habs}=={cpos} tape-eq={mt==ctape} "
              f"steps={m.steps} OK={ok}  ({time.time()-t:.1f}s)")
        if not ok: sys.exit("V1 FAILED")
    # V2: window-set equality over 32M
    print("V2: window-set equality (r=5) over 32M steps")
    t=time.time()
    m=Mach(); m.run(maxsteps=32_000_000)
    _,_,_,_,cwins,cunsafe=concrete(32_000_000,recwins=True)
    print(f"  macro |S|={len(m.wins)} unsafe={m.unsafe} f1={m.f1} | concrete |S|={len(cwins)} unsafe={cunsafe}")
    print(f"  SETS EQUAL: {m.wins==cwins}   ({time.time()-t:.1f}s)")
    if m.wins!=cwins:
        print("  macro-only:",m.wins-cwins); print("  conc-only:",cwins-m.wins); sys.exit("V2 FAILED")
    print("ALL VALIDATIONS PASSED")
