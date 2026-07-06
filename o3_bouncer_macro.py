#!/usr/bin/env python3
# o3 SOUND level-1 macro-machine (2026-07-06) -- port of o4_bouncer_macro.py.
# o3 = 1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC (halt = F reads 0 <=> E reads "00").
# Tape = bytearray (width ~ sqrt(steps): dense representation is right for o3).
# Acceleration = GENERIC VERIFIED p-cycle jump. o3's sweep cycles are p=6 (D=-2),
# p=10 (D=+6), p=20 (D=-6) -- NOT o4's p=2 -- so the jump engine is fully generic:
#   1. from (state,pos) micro-simulate on a scratch overlay until the state returns
#      at nonzero displacement D with the (st,r,w,mv)-word repeating for a full 2nd
#      cycle (translation-invariance certificate ON THE ACTUAL TAPE);
#   2. offline steady-state analysis of the cycle word (cached): demanded FRESH
#      pre-values per cycle (leading edge), the settled |D|-cell write pattern per
#      interior cycle, the LEADING-EDGE PROFILE (exact tape around the head at a
#      cycle start, verified translation-steady), E-reads-0 count/window offsets and
#      neighbour-safety per cycle;
#   3. count how many further cycles the tape ahead satisfies the fresh demands
#      (exact byte comparison), jump m = matched - MARGIN cycles: write settled
#      pattern over the passed region, overwrite the leading-edge profile at the new
#      head, add m*p steps and m-scaled event counts.
# The engine refuses to jump on any anomaly (unknown neighbour, unsteady profile,
# settled-cell count != |D|). SOUNDNESS: the macro is a DISCOVERY/large-scale tool,
# validated empirically below; the proof path (o3_body_proof.py, o3_gen_proof.py)
# is pure concrete.
# Validation battery (run this file):
#   V1 exact tape/state/head/step + event-count equality vs pure concrete;
#   V2 E-reads-0 window-set (radius 5) + unsafe equality vs concrete over 32M steps;
#   V3 blank-tape milestone stream (a,k) at scale vs the o3_ledger.py arithmetic orbit.
import sys, re
from collections import defaultdict

def parse(spec):
    M=[[None,None] for _ in range(6)]
    for kk,blk in enumerate(spec.split('_')):
        for r in (0,1):
            c=blk[3*r:3*r+3]
            M[kk][r]=None if c[0]=='-' else (int(c[0]),1 if c[1]=='R' else -1,"ABCDEF".index(c[2]))
    return M
TM=parse("1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC")
SN="ABCDEF"
PMAX=24
MARGIN=4
W=5

class Mach:
    def __init__(self,SZ=1<<26):
        self.SZ=SZ
        self.tape=bytearray(SZ); self.off=SZ//2
        self.pos=self.off; self.st=0; self.steps=0
        self.lo=self.hi=self.pos
        self.halted=False
        self.wins=set(); self.unsafe=0; self.e0=0
        self.milestones=[]
        self.cycle_cache={}

    def micro(self):
        t=self.tape; pos=self.pos
        r=t[pos]; a=TM[self.st][r]
        if a is None:
            self.halted=True; return
        if self.st==4 and r==0:
            self.e0+=1
            self.wins.add(bytes(t[pos-W:pos+W+1]))
            if t[pos+1]!=1: self.unsafe+=1
        w,d,ns=a
        t[pos]=w; pos+=d
        self.pos=pos; self.st=ns; self.steps+=1
        if pos<self.lo: self.lo=pos
        if pos>self.hi: self.hi=pos

    # ---------- cycle detection on the actual tape ----------
    def detect_cycle(self):
        t=self.tape; pos0=self.pos; st0=self.st
        word=[]; writes={}; pos=pos0; st=st0
        rets=[]
        for i in range(2*PMAX):
            r=writes.get(pos)
            if r is None: r=t[pos]
            a=TM[st][r]
            if a is None: break
            w,d,ns=a
            word.append((st,r,w,d))
            writes[pos]=w
            pos+=d; st=ns
            if st==st0 and pos!=pos0:
                rets.append((i+1,pos-pos0))
        for p,D in rets:
            if p>PMAX: continue
            if len(word)>=2*p and word[p:2*p]==word[:p] and D!=0:
                # require D consistent: cycle-2 displacement equals cycle-1
                return p,D,tuple(word[:p])
        return None

    # ---------- offline cycle analysis (cached per word) ----------
    def analyze(self,word,D):
        NC=8; CI=5   # snapshot at cycle CI start; steadiness vs CI+1
        tape={}; pos=0; st=word[0][0]
        last={}; snaps={}
        e0_per=0; unsafe_per=0; winoffs=[]
        for i in range(NC):
            if i in (CI,CI+1):
                snaps[i]=dict(tape)
            for (s,r,w,d) in word:
                if pos not in tape:
                    tape[pos]=r      # demanded fresh value
                if tape[pos]!=r: return None
                if s==4 and r==0 and i==2:
                    nb=tape.get(pos+1)
                    if nb is None: return None
                    if nb!=1: unsafe_per+=1
                    winoffs.append(pos-2*D)   # offset rel cycle-2 start
                    e0_per+=1
                tape[pos]=w; last[pos]=i; pos+=d
        # settled pattern: cells last touched by cycle 2, offsets rel cycle-2 start
        settled=tuple(sorted((c-2*D,tape[c]) for c,i in last.items() if i==2))
        if len(settled)!=abs(D): return None
        # fresh demands of cycle 3 (rel cycle-3 start): first-touch cells of cycle 3
        # replay to find first-touch cells per cycle
        first_cycle={}
        pos=0
        for i in range(NC):
            for (s,r,w,d) in word:
                if pos not in first_cycle: first_cycle[pos]=(i,tape_pre(word,D,pos,i))
                pos+=d
        # simpler: fresh = cells whose first touch is cycle 3, with demanded value
        seen=set(); fresh=[]
        pos=0
        for i in range(NC):
            for (s,r,w,d) in word:
                if pos not in seen:
                    seen.add(pos)
                    if i==3: fresh.append((pos-3*D,r))
                pos+=d
        if not fresh: return None
        # leading-edge profile at a cycle start (touched cells only), rel cycle start;
        # steadiness: profile at CI equals profile at CI+1
        def prof(i):
            base=i*D
            return {c-base:v for c,v in snaps[i].items()}
        pCI={c:v for c,v in prof(CI).items() if -6*abs(D)<=c<=6*abs(D)}
        pCI1={c:v for c,v in prof(CI+1).items() if -6*abs(D)<=c<=6*abs(D)}
        if pCI!=pCI1: return None
        return dict(settled=settled,fresh=tuple(fresh),profile=tuple(sorted(pCI.items())),
                    e0_per=e0_per,unsafe_per=unsafe_per,winoffs=tuple(winoffs))

    def try_jump(self,budget):
        c=self.detect_cycle()
        if c is None: return 0
        p,D,word=c
        info=self.cycle_cache.get(word)
        if word not in self.cycle_cache:
            self.cycle_cache[word]=info=self.analyze(word,D)
        if info is None: return 0
        t=self.tape; pos0=self.pos
        fresh=info['fresh']
        lim=(self.SZ-64-pos0)//D if D>0 else (pos0-64)//(-D)
        lim=min(lim,budget//p)
        m=0
        while m<lim:
            base=pos0+m*D
            ok=True
            for (o,r) in fresh:
                if t[base+o]!=r: ok=False; break
            if not ok: break
            m+=1
        m-=MARGIN
        if m<6: return 0
        # interior settled writes for cycles 0..m-1
        settled=info['settled']
        for i in range(m):
            base=pos0+i*D
            for o,v in settled:
                t[base+o]=v
        # leading-edge profile at new head
        base=pos0+m*D
        for o,v in info['profile']:
            t[base+o]=v
        self.pos=base; self.steps+=m*p
        self.e0+=info['e0_per']*m
        self.unsafe+=info['unsafe_per']*m
        for o in info['winoffs']:
            b2=pos0+1*D
            self.wins.add(bytes(t[b2+o-W:b2+o+W+1]))
        if self.pos<self.lo: self.lo=self.pos
        if self.pos>self.hi: self.hi=self.pos
        return m

    # ---------- milestone ----------
    def check_milestone(self):
        if self.st!=0 or self.pos>self.lo: return
        t=self.tape
        s=t[self.lo:self.hi+1].replace(b'\x01',b'1').replace(b'\x00',b'0').decode()
        m=re.fullmatch(r'00((?:10)*)((?:110)*(?:11)?)0*',s)
        if not m: return
        a=len(m.group(1))//2
        g2=m.group(2)
        if g2=='': k=0
        elif g2=='110'*(len(g2)//3): k=len(g2)//3          # trailing 0 visited
        elif g2=='110'*((len(g2)+1)//3-1)+'11': k=(len(g2)+1)//3
        else: return
        self.milestones.append((self.steps,a,k))

    def run(self,maxsteps):
        while not self.halted and self.steps<maxsteps:
            # milestone check at the instant (state A, head at the left frontier),
            # BEFORE stepping -- covers arrivals via both micro and jump paths
            if self.st==0 and self.pos<=self.lo: self.check_milestone()
            if self.try_jump(maxsteps-self.steps)==0:
                self.micro()

def tape_pre(word,D,pos,i):  # (unused helper kept for clarity)
    return None

# ---------- pure concrete reference ----------
def concrete(N,recwins=False):
    SZ=1<<25
    t=bytearray(SZ); off=SZ//2
    pos=off; st=0; wins=set(); unsafe=0; e0=0
    for s in range(N):
        r=t[pos]; a=TM[st][r]
        if a is None: return ('HALT',s,pos-off,None,wins,unsafe,e0)
        if st==4 and r==0:
            e0+=1
            if recwins: wins.add(bytes(t[pos-W:pos+W+1]))
            if t[pos+1]!=1: unsafe+=1
        w,d,ns=a
        t[pos]=w; pos+=d; st=ns
    return (SN[st],N,pos-off,t,wins,unsafe,e0)

if __name__=='__main__':
    import time
    print("V1: exact equality vs concrete")
    for N in (200_000,1_000_000,5_000_000):
        t0=time.time()
        m=Mach(); m.run(N)
        cst,cn,cpos,ct,_,cu,ce0=concrete(N)
        coff=1<<24
        msup={i:v for i,v in enumerate(m.tape[m.lo:m.hi+1],start=m.lo-m.off) if v}
        lo2=min(msup) if msup else 0; hi2=max(msup) if msup else 0
        csup={}
        for i in range(lo2-8,hi2+9):
            if ct[coff+i]: csup[i]=ct[coff+i]
        ok=(SN[m.st]==cst and (m.pos-m.off)==cpos and m.steps==N and msup==csup
            and m.e0==ce0 and m.unsafe==cu)
        print(f"  N={N:>9}: state {SN[m.st]}=={cst} head {m.pos-m.off}=={cpos} "
              f"tape-eq={msup==csup} e0 {m.e0}=={ce0} unsafe {m.unsafe}=={cu} "
              f"OK={ok} ({time.time()-t0:.1f}s)")
        if not ok: sys.exit("V1 FAILED")
    print("V2: E-reads-0 window-set (r=5) equality over 32M steps")
    t0=time.time()
    m=Mach(); m.run(32_000_000)
    _,_,_,_,cw,cu,ce0=concrete(32_000_000,recwins=True)
    print(f"  macro |S|={len(m.wins)} unsafe={m.unsafe} e0={m.e0} | "
          f"concrete |S|={len(cw)} unsafe={cu} e0={ce0}")
    print(f"  SETS EQUAL: {m.wins==cw}  e0 equal: {m.e0==ce0}  ({time.time()-t0:.1f}s)")
    if m.wins!=cw or m.e0!=ce0:
        print("  macro-only:",m.wins-cw); print("  conc-only:",cw-m.wins); sys.exit("V2 FAILED")
    print("V3: milestone stream vs arithmetic ledger orbit (large scale)")
    t0=time.time()
    m=Mach(); m.run(3_000_000_000)
    ded=[]
    for _,a,k in m.milestones:
        if not ded or ded[-1]!=(a,k): ded.append((a,k))
    from o3_ledger import step as lstep
    try: i0=ded.index((6,2))
    except ValueError: sys.exit("V3 FAILED: (6,2) not found")
    a,k=6,2; okv=True; n_match=0
    for x in ded[i0:]:
        if x!=(a,k): okv=False; print(f"  MISMATCH: milestone {x} vs ledger {(a,k)}"); break
        nx=lstep(a,k)
        if nx is None: break
        a,k=nx; n_match+=1
    print(f"  macro steps={m.steps:,} milestones={len(ded)} matched ledger for {n_match} "
          f"generations: {okv} (final a={ded[-1][0]}, k={ded[-1][1]}) ({time.time()-t0:.1f}s)")
    if not okv: sys.exit("V3 FAILED")
    print("ALL VALIDATIONS PASSED")
