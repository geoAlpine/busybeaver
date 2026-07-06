#!/usr/bin/env python
# o4_cap_macro_saturation.py -- extend the sweep-end / cap-arrival TYPE-SET saturation
# evidence to large G using the VALIDATED o4_bouncer_macro machine (2026-07-06).
#
# SOUNDNESS OF THE HOOK (why no event can hide inside a jump):
#   (1) B-reads-0 is NEVER inside a p=2 verified cycle: the only p=2 cycles of o4's table are
#       (B:1->1RF, F:0->0RB) and (D:1->0LE, E:0->1LD)  [B:0->1RC cannot return to B in 2 steps;
#       exhaustively re-checked below].  So every B-reads-0 executes as a micro step.
#   (2) A jump can never carry the head INTO the cap region [rmax-12, rmax]: rightward B1F0
#       jumps stop >= 2*MARGIN=16 cells before the (1,0)-tiling break, and the break is at
#       rmax-1 (the second 0 of the cap 1001) or earlier; leftward D1E0 jumps move away.
#       So every crossing of rmax-12 from outside executes as a micro step.  [checked at runtime]
# VALIDATION: macro type-sets == concrete type-sets over the same step range (V-check below).
import sys, importlib.util
spec=importlib.util.spec_from_file_location("obm","/Users/aokiyousuke/busybeaver/o4_bouncer_macro.py")
obm=importlib.util.module_from_spec(spec); spec.loader.exec_module(obm)
Mach, M, MARGIN = obm.Mach, obm.M, obm.MARGIN

# ---- (1) exhaustive re-check: no p=2 cycle contains a B-read-0 ----
cycles=[]
for s0 in "ABCDEF":
    for v0 in (0,1):
        t0=M[(s0,v0)]
        if t0 is None: continue
        w0,d0,s1=t0
        for v1 in (0,1):
            t1=M[(s1,v1)]
            if t1 is None: continue
            w1,d1,s2=t1
            if s2==s0 and d1==d0 and not (v0==w0==v1==w1):
                cycles.append(((s0,v0),(s1,v1)))
print("p=2 cycles of the table:", cycles)
assert all(not(sx=='B' and vx==0) for cyc in cycles for sx,vx in cyc), "a p=2 cycle reads B:0!"
print("  => no p=2 cycle contains a B-read-0: every B-read-0 is a MICRO step. [PROVEN]")

RSE=10   # sweep-end window radius
DCAP=12  # cap-region distance

class M2(Mach):
    def __init__(self):
        super().__init__()
        self.pst=None; self.was_inside=False
        self.setypes={}; self.captypes={}
        self.se_last_new=-1; self.cap_last_new=-1
        self.jump_cross_violation=0

    def rightmost1(self):
        x=self.abs0; r=None
        for pat,n in self.segs:
            L=len(pat)*n
            if '1' in pat:
                for j in range(L-1,-1,-1):
                    if pat[j%len(pat)]=='1': r=x+j; break
            x+=L
        return r

    def hook(self):
        rmax=self.rightmost1()
        if rmax is not None:
            inside=self.habs>=rmax-DCAP
            if inside and not self.was_inside:
                key=(self.st,self.habs-rmax,
                     ''.join(str(self.read_cell(rmax-16+i)) for i in range(20)))
                if key not in self.captypes:
                    self.captypes[key]=[0,self.steps]; self.cap_last_new=self.steps
                self.captypes[key][0]+=1
            self.was_inside=inside
        if self.st=='B' and self.read_cell(self.habs)==0:
            key=(self.pst,''.join(str(self.read_cell(self.habs-RSE+i)) for i in range(2*RSE+1)))
            if key not in self.setypes:
                self.setypes[key]=[0,self.steps]; self.se_last_new=self.steps
            self.setypes[key][0]+=1

    def run(self,maxsteps=None,targetG=None,assert_segs=100000):
        while not self.halted:
            if maxsteps is not None and self.steps>=maxsteps: return
            if targetG is not None and -self.leftmost>=targetG: return
            self.hook()
            budget=(maxsteps-self.steps) if maxsteps is not None else (1<<62)
            s0=self.st; v0=self.read_cell(self.habs)
            pre_inside=self.was_inside
            m=self.try_jump(budget)
            if m==0:
                self.pst=s0
                self.micro()
            else:
                self.pst=M[(s0,v0)][2]   # last executed half-cycle state
                # runtime check of soundness claim (2): a jump never lands inside the region
                r=self.rightmost1()
                if r is not None and (not pre_inside) and self.habs>=r-DCAP:
                    self.jump_cross_violation+=1
                if len(self.segs)<=4: self.check_milestone()
            if len(self.segs)>assert_segs:
                raise RuntimeError("segment blow-up")

# ---- concrete reference (same instrumentation, exact micro sim) ----
def concrete_types(N):
    tape={}; pos=0; st='A'; prev=None
    rmax=None; ones=0; inside=False
    setypes={}; captypes={}
    for s in range(N):
        r=tape.get(pos,0); a=M[(st,r)]
        assert a is not None
        if rmax is not None:
            ni=pos>=rmax-DCAP
            if ni and not inside:
                key=(st,pos-rmax,''.join(str(tape.get(rmax-16+i,0)) for i in range(20)))
                captypes.setdefault(key,[0,s])[0]+=1
            inside=ni
        if st=='B' and r==0:
            key=(prev,''.join(str(tape.get(pos-RSE+i,0)) for i in range(2*RSE+1)))
            setypes.setdefault(key,[0,s])[0]+=1
        w,d,ns=a
        if w==1:
            if r==0: ones+=1
            tape[pos]=1
            if rmax is None or pos>rmax: rmax=pos
        elif r==1:
            ones-=1; del tape[pos]
            if pos==rmax:
                if ones==0: rmax=None
                else:
                    rmax-=1
                    while tape.get(rmax,0)==0: rmax-=1
        prev=st; pos+=d; st=ns
    return setypes,captypes

if __name__=="__main__":
    targetG=int(sys.argv[1]) if len(sys.argv)>1 else 200_000
    # V-CHECK: macro type-sets == concrete type-sets over 5M steps
    NV=5_000_000
    cse,ccap=concrete_types(NV)
    m=M2(); m.run(maxsteps=NV)
    ok_se=set(m.setypes)==set(cse); ok_cap=set(m.captypes)==set(ccap)
    cnt_se=all(m.setypes[k][0]==cse[k][0] for k in cse) if ok_se else False
    cnt_cap=all(m.captypes[k][0]==ccap[k][0] for k in ccap) if ok_cap else False
    print(f"V-CHECK over {NV:,} steps: sweep-end sets equal={ok_se} counts equal={cnt_se}"
          f" ({len(cse)} types); cap sets equal={ok_cap} counts equal={cnt_cap} ({len(ccap)} types)")
    assert ok_se and ok_cap and cnt_se and cnt_cap, "macro instrumentation disagrees with concrete!"
    # PRODUCTION: extend to targetG
    m=M2(); m.run(targetG=targetG)
    G=max((g for _,g,_ in m.milestones),default=None)
    print(f"\nPRODUCTION: steps={m.steps:,}  milestones={len(m.milestones)}  max G={G:,}")
    print(f"  jump-lands-inside-cap-region violations: {m.jump_cross_violation} (must be 0)")
    assert m.jump_cross_violation==0
    print(f"  unsafe={m.unsafe}  F-reads-1={m.f1}  halted={m.halted}")
    print(f"  sweep-end types={len(m.setypes)}  LAST NEW at step {m.se_last_new:,}")
    print(f"  cap-arrival types={len(m.captypes)}  LAST NEW at step {m.cap_last_new:,}")
    print("  cap-arrival types detail:")
    for k,v in sorted(m.captypes.items(),key=lambda kv:-kv[1][0]):
        print(f"    count={v[0]:>8,} first@{v[1]:>15,}  {k}")
    print("  sweep-end types (top 12 + any first-seen after step 2000):")
    for i,(k,v) in enumerate(sorted(m.setypes.items(),key=lambda kv:-kv[1][0])):
        if i<12 or v[1]>2000:
            print(f"    count={v[0]:>10,} first@{v[1]:>15,}  {k}")
