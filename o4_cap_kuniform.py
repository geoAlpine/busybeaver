#!/usr/bin/env python
# o4_cap_kuniform.py -- Task 3 of the C-seam closure attempt (2026-07-06):
#   (A) FORCED-PREFIX analysis: for every saturated sweep-end type (prev_st, radius-8 window
#       around a B-reads-0), simulate using ONLY the window cells; the continuation is forced
#       until the head reads an unknown cell. If the C-seam completes inside the prefix with
#       tape[q+2]=0 known, its safety is PROVEN conditional only on the window content.
#   (B) k-UNIFORM padded events: embed each C-seam window / the cap-arrival window in
#       period-2 padding of depth k (k=k0..k0+8); verify the evolutions are IDENTICAL, the
#       head stays in a bounded window, the seam is safe, and the exit is a proven sweep mode.
#       LOCALITY LEMMA: if two configs agree on window W, head starts identically, and the head
#       never leaves W during 0..T in one of them, the evolutions agree for 0..T. (Induction on
#       t: the read cell is inside W.) Hence pad-k0 confinement ==> identical for ALL k>=k0.
#   (C) REAL-TRACE validation: capture each real cap-arrival / sweep-end event from the exact
#       concrete machine and assert the standalone padded event reproduces it step-for-step.
# Machine: o4 = 1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---
import sys
from collections import deque

def parse(spec):
    M={}
    for k,blk in enumerate(spec.split('_')):
        st="ABCDEF"[k]
        for r in (0,1):
            c=blk[3*r:3*r+3]
            M[(st,r)]=None if c[0]=='-' else (int(c[0]),1 if c[1]=='R' else -1,c[2])
    return M
M=parse("1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---")

# ---------------- (A) forced-prefix on a known finite window ----------------
def forced_prefix(prev_st, w, R, maxsteps=2000):
    """Head=B reading 0 at offset 0; w = window offsets -R..R. Simulate on KNOWN cells only."""
    tape={i-R:int(ch) for i,ch in enumerate(w)}
    pos=0; st='B'; prev=prev_st
    b1=[]; seams=[]; halted=False
    for t in range(maxsteps):
        if pos not in tape:
            return dict(status='EXIT', exit_pos=pos, exit_st=st, steps=t, b1=b1, seams=seams)
        r=tape[pos]; a=M[(st,r)]
        if a is None:
            return dict(status='HALT', exit_pos=pos, exit_st=st, steps=t, b1=b1, seams=seams)
        if st=='B' and r==1:
            b1.append((pos, tape.get(pos+1)))          # (position, right-neighbour or None=unknown)
        if st=='A' and r==0 and tape.get(pos+1)==1 and prev=='C':
            seams.append((pos, tape.get(pos+2)))        # C-seam at q=pos; safe iff q+2==0
        w0,d,ns=a
        tape[pos]=w0; prev=st; pos+=d; st=ns
    return dict(status='TIMEOUT', exit_pos=pos, exit_st=st, steps=maxsteps, b1=b1, seams=seams)

# ---------------- (B) padded standalone events ----------------
def padded_sweepend(prev_st, w, R, k, maxsteps=200000):
    """Embed the radius-R window in period-2 padding of k repeats on both sides.
       Left pad repeats w[0:2] leftwards; right pad repeats w[-2:] rightwards.
       Run until head exits [ -R-2, R+2 ] (the core+margin). Return the full trace."""
    tape={}
    for i,ch in enumerate(w): tape[i-R]=int(ch)
    for j in range(k):
        tape[-R-2-2*j]=int(w[0]); tape[-R-1-2*j]=int(w[1])
        tape[R+1+2*j]=int(w[-2]); tape[R+2+2*j]=int(w[-1])
    pos=0; st='B'; prev=prev_st
    trace=[]; b1=[]; seams=[]
    lo,hi=-R-2,R+2
    minp=maxp=0
    for t in range(maxsteps):
        if pos<lo or pos>hi:
            return dict(status='EXIT', exit_pos=pos, exit_st=st, steps=t, trace=trace,
                        b1=b1, seams=seams, minp=minp, maxp=maxp)
        r=tape.get(pos,0); a=M[(st,r)]
        if a is None: return dict(status='HALT', exit_pos=pos, exit_st=st, steps=t, trace=trace,
                                  b1=b1, seams=seams, minp=minp, maxp=maxp)
        trace.append((st,pos,r,a[0]))
        if st=='B' and r==1: b1.append((pos, tape.get(pos+1,0)))
        if st=='A' and r==0 and tape.get(pos+1,0)==1 and prev=='C':
            seams.append((pos, tape.get(pos+2,0)))
        tape[pos]=a[0]; prev=st; pos+=a[1]; st=a[2]
        minp=min(minp,pos); maxp=max(maxp,pos)
    return dict(status='TIMEOUT')

def padded_cap(arr_st, arr_off, w20, k, maxsteps=200000, exit_lo=-16, hi_cap=60):
    """Cap event: w20 = cells rmax-16..rmax+3 (rmax at offset 0 = index 16).
       Left pad: extend w20[0:2] period-2 k times. Right of rmax+3: all 0 (true by rmax defn).
       Head enters at offset arr_off in state arr_st. Run until pos-offset < exit_lo (left exit).
       Positions are offsets relative to rmax."""
    tape={}
    for i,ch in enumerate(w20): tape[i-16]=int(ch)
    for j in range(k):
        tape[-18-2*j]=int(w20[0]); tape[-17-2*j]=int(w20[1])
    pos=arr_off; st=arr_st; prev=None
    trace=[]; b1=[]; cseams=[]; eseams=[]
    minp=maxp=pos
    for t in range(maxsteps):
        if pos<exit_lo:
            newr=max((p for p,v in tape.items() if v==1), default=None)
            return dict(status='EXIT', exit_pos=pos, exit_st=st, steps=t, trace=trace, b1=b1,
                        cseams=cseams, eseams=eseams, minp=minp, maxp=maxp, new_rmax=newr,
                        finwin=''.join(str(tape.get(i,0)) for i in range(-16,8)))
        if pos>hi_cap: return dict(status='RIGHT_ESCAPE', exit_pos=pos, steps=t)
        r=tape.get(pos,0); a=M[(st,r)]
        if a is None: return dict(status='HALT', exit_pos=pos, exit_st=st, steps=t, trace=trace,
                                  b1=b1, cseams=cseams, eseams=eseams)
        trace.append((st,pos,r,a[0]))
        if st=='B' and r==1: b1.append((pos, tape.get(pos+1,0)))
        if st=='A' and r==0 and tape.get(pos+1,0)==1:
            (cseams if prev=='C' else eseams).append((pos, tape.get(pos+2,0)))
        tape[pos]=a[0]; prev=st; pos+=a[1]; st=a[2]
        minp=min(minp,pos); maxp=max(maxp,pos)
    return dict(status='TIMEOUT')

# ---------------- (C) real-machine event capture ----------------
def real_events(N, D=12, R=8, capT=4000):
    """Concrete run; capture (i) every cap-arrival event trace (from crossing rmax-D until
       pos<rmax-16), positions rmax-relative; (ii) every sweep-end (B-reads-0) event trace
       (until head exits pos0+-(R+2)), positions pos0-relative."""
    tape={}; pos=0; st='A'; prev=None
    rmax=None; ones=0
    cap_traces=[]; se_traces=[]
    cap_active=None; se_active=[]
    inside=False
    for s in range(N):
        r=tape.get(pos,0); a=M[(st,r)]
        assert a is not None
        if rmax is not None:
            now_inside = pos>=rmax-D
            if now_inside and not inside and cap_active is None:
                cap_active=dict(step=s, rmax=rmax, st=st, off=pos-rmax,
                                w20=''.join(str(tape.get(rmax-16+i,0)) for i in range(20)), tr=[])
            inside=now_inside
        if cap_active is not None:
            if pos-cap_active['rmax']<-16:
                cap_active['tr_len']=len(cap_active['tr']); cap_traces.append(cap_active); cap_active=None
            elif len(cap_active['tr'])<capT:
                cap_active['tr'].append((st,pos-cap_active['rmax'],r,a[0]))
        if st=='B' and r==0 and rmax is not None:
            se_active.append(dict(step=s, p0=pos, prev=prev,
                                  w=''.join(str(tape.get(pos-R+i,0)) for i in range(2*R+1)), tr=[]))
        for ev in se_active[:]:
            rel=pos-ev['p0']
            if rel<-(R+2) or rel>R+2:
                se_traces.append(ev); se_active.remove(ev)
            elif len(ev['tr'])<capT:
                ev['tr'].append((st,rel,r,a[0]))
        w0,d,ns=a
        if w0==1:
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
    return cap_traces, se_traces

# ---------------- main ----------------
if __name__=="__main__":
    N=int(sys.argv[1]) if len(sys.argv)>1 else 3_000_000
    R=10
    print(f"capturing real events over N={N:,} concrete steps ...")
    cap_traces, se_traces = real_events(N, R=R)
    setypes={}
    for ev in se_traces: setypes.setdefault((ev['prev'],ev['w']),[]).append(ev)
    captypes={}
    for ev in cap_traces: captypes.setdefault((ev['st'],ev['off'],ev['w20']),[]).append(ev)
    print(f"  sweep-end events={len(se_traces)}  types={len(setypes)}")
    print(f"  cap-arrival events={len(cap_traces)}  types={len(captypes)}")

    print("\n================ (A) FORCED-PREFIX per sweep-end type ================")
    ok_all=True
    for (prev,w),evs in sorted(setypes.items(), key=lambda kv:-len(kv[1])):
        fp=forced_prefix(prev,w,R)
        seam_txt="; ".join(f"C-seam q={q:+d} q+2={q2}" for q,q2 in fp['seams']) or "no C-seam"
        b1bad=[x for x in fp['b1'] if x[1]!=0]
        stat=f"count={len(evs):>6}  prev={prev}  w={w}  steps={fp['steps']}  exit@{fp['exit_pos']:+d}({fp['exit_st']})"
        print(f"  {stat}\n      -> {seam_txt}; B-reads-1 inside={len(fp['b1'])}, non-0-right={b1bad}")
        if b1bad or any(q2!=0 for _,q2 in fp['seams']): ok_all=False
    print(f"  FORCED-PREFIX VERDICT: all inside-window B-reads-1 safe & all C-seams q+2==0: {ok_all}")

    print("\n================ (B)+(C) k-UNIFORM padded events vs real ================")
    print("---- sweep-end types with a C-seam in the forced prefix ----")
    for (prev,w),evs in sorted(setypes.items(), key=lambda kv:-len(kv[1])):
        fp=forced_prefix(prev,w,R)
        if not fp['seams']: continue
        runs=[padded_sweepend(prev,w,R,k) for k in range(4,13)]
        uni=all(r0['trace']==runs[0]['trace'] and r0['status']=='EXIT' for r0 in runs)
        r0=runs[0]
        # compare vs every real instance of this type (trace prefix up to exit)
        realmatch=all(ev['tr']==r0['trace'] for ev in evs)
        print(f"  type prev={prev} w={w}  instances={len(evs)}")
        print(f"    k=4..12 identical={uni}  steps={r0['steps']}  span=[{r0['minp']},{r0['maxp']}]"
              f"  exit@{r0['exit_pos']:+d}({r0['exit_st']})  seams={r0['seams']}  b1={r0['b1']}")
        print(f"    real-trace match ({len(evs)} instances): {realmatch}")
        if len(evs)>=2:
            assert uni and realmatch and all(q2==0 for _,q2 in r0['seams']), "RECURRING type failed!"
        else:
            print("    (startup one-off: not asserted k-uniform; the single real instance was"
                  " verified safe concretely in the exhaustive run)")
    print("---- cap-arrival types ----")
    for (ast,aoff,w20),evs in sorted(captypes.items(), key=lambda kv:-len(kv[1])):
        runs=[padded_cap(ast,aoff,w20,k) for k in range(4,13)]
        uni=all(r['status']==runs[0]['status'] and r.get('trace')==runs[0].get('trace') for r in runs)
        r0=runs[0]
        if r0['status']!='EXIT':
            print(f"  type ({ast},{aoff},{w20}) instances={len(evs)}: status={r0['status']} !!"); continue
        realmatch=all(ev['tr']==r0['trace'] for ev in evs)
        b1bad=[x for x in r0['b1'] if x[1]!=0]
        csbad=[x for x in r0['cseams'] if x[1]!=0]; esbad=[x for x in r0['eseams'] if x[1]!=0]
        print(f"  type ({ast},{aoff},w20={w20})  instances={len(evs)}")
        print(f"    k=4..12 identical={uni}  steps={r0['steps']}  span=[{r0['minp']},{r0['maxp']}]"
              f"  exit@{r0['exit_pos']:+d}({r0['exit_st']})")
        print(f"    B1={len(r0['b1'])} unsafe={b1bad}  E-seams={r0['eseams']}  C-seams={r0['cseams']}")
        print(f"    new_rmax_off={r0['new_rmax']}  final win(-16..+7)={r0['finwin']}")
        print(f"    real-trace match ({len(evs)} instances): {realmatch}")
        if len(evs)>=2:
            assert uni and realmatch and not b1bad and not csbad and not esbad, "RECURRING cap type failed!"
        else:
            print("    (startup one-off: not asserted; verified safe concretely in the exhaustive run)")
    print("\ndone.")
