#!/usr/bin/env python
# RED TEAM attacks 3-6: independent reconstruction of M(G,a), Z(k,g,a); suffix table audit
# at UNTESTED k (101, 251); spurious-milestone (early-exit) probe; Z(41,3,0) halt reproduction;
# full-generation composition tests M(G,a) -> M(G',a') vs odometer+ledger prediction.
from collections import defaultdict
import sys

def parse(spec):
    T={}
    for k,blk in enumerate(spec.split('_')):
        st="ABCDEF"[k]
        for r in (0,1):
            c=blk[3*r:3*r+3]
            T[(st,r)]=None if c[0]=='-' else (int(c[0]),1 if c[1]=='R' else -1,c[2])
    return T
TT=parse("1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---")

def build_M(G,a):
    """M(G,a): head@0 state E; cells 0..G-1 zero; filler (10)^a 1001 at G."""
    tape={}
    for i in range(a): tape[G+2*i]=1
    tape[G+2*a]=1; tape[G+2*a+3]=1
    return tape,0,'E'

def build_Z(k,g,a):
    """Z(k,g,a): head@0 state E on first 1 of (10)^k 1001, gap 0^g, filler (10)^a 1001."""
    tape={}
    for i in range(k): tape[2*i]=1
    tape[2*k]=1; tape[2*k+3]=1
    f=2*k+4+g
    for i in range(a): tape[f+2*i]=1
    tape[f+2*a]=1; tape[f+2*a+3]=1
    return tape,0,'E'

def parse_filler(f):
    if f.endswith('1001'):
        body=f[:-4]
        if len(body)%2==0 and all(body[i:i+2]=='10' for i in range(0,len(body),2)):
            return len(body)//2
    return None

def run(tape0,pos0,st0,maxsteps,collect_milestones=True,stop_at_gap=None):
    """Run; record every instant where st==E and head strictly left of support and support
       parses as (10)^a 1001 => (step, gap, a). Stop early if gap>=stop_at_gap seen (after
       recording).  Also count unsafe B-reads-1 and F-reads-1. Returns dict."""
    tape=defaultdict(int)
    for kk,v in tape0.items(): tape[kk]=v
    sup=set(kk for kk,v in tape0.items() if v)
    pos=pos0; st=st0
    miles=[]; unsafe=0; f1=0
    for s in range(maxsteps):
        r=tape[pos]; act=TT[(st,r)]
        if act is None:
            return dict(halt=True, steps=s, miles=miles, unsafe=unsafe, f1=f1)
        if st=='B' and r==1 and tape[pos+1]==1: unsafe+=1
        if st=='F' and r==1: f1+=1
        if collect_milestones and st=='E' and sup and pos<min(sup):
            mn=min(sup); mx=max(sup)
            f=''.join(str(tape[i]) for i in range(mn,mx+1))
            a=parse_filler(f)
            gap=mn-pos
            miles.append((s,gap,a))
            if stop_at_gap and gap>=stop_at_gap:
                return dict(halt=False, steps=s, miles=miles, unsafe=unsafe, f1=f1)
        w,d,ns=act
        if w==0: tape.pop(pos,None); sup.discard(pos)
        else: tape[pos]=1; sup.add(pos)
        pos+=d; st=ns
    return dict(halt=False, steps=maxsteps, miles=miles, unsafe=unsafe, f1=f1, timeout=True)

def summarize_miles(miles):
    """Group consecutive-instant milestones; return list of (last_step, max_gap, a_at_max)."""
    out=[]
    cur=[]
    last=-10
    for (s,g,a) in miles:
        if s-last>1000 and cur:
            mg=max(cur,key=lambda x:x[1]); out.append(mg); cur=[]
        cur.append((s,g,a)); last=s
    if cur: out.append(max(cur,key=lambda x:x[1]))
    return out

CFX={0:3,1:5,2:1}
def odo(G): return (4*G)//3 + CFX[G%3]
def delta(G): return {1:-1,2:4,0:6}[G%3]

if __name__=='__main__':
    print("========= (6) Z(41,3,0) halt reproduction =========")
    t,p,s=build_Z(41,3,0)
    r=run(t,p,s,200000)
    print(f"  Z(41,3,0): halt={r['halt']} at step {r['steps']} (claimed 55,170); unsafe={r['unsafe']} f1={r['f1']}")
    # shape check: is Z(41,3,0) in the reachable-form family? reachable k=19+2r odd yes; g=3 => G≡1 mod 3 source;
    # a=0 at g=3 requires prior a=1 at G≡2/0 gen (a'=a+4/+6 => a>=4 after) or ledger path; not claimed reachable.
    for (kk,gg,aa) in [(41,3,1),(41,3,2),(19,3,0),(21,3,0)]:
        t,p,s=build_Z(kk,gg,aa)
        r=run(t,p,s,3_000_000,stop_at_gap=2*kk+5)
        sm=summarize_miles(r['miles'])
        print(f"  Z({kk},{gg},{aa}): halt={r['halt']} steps={r['steps']} unsafe={r['unsafe']} f1={r['f1']} milestones={sm[:3]}")

    print("\n========= (3)+(4) SUFFIX audit: exact landing, untested k, early-exit probe =========")
    # expected: g=3: G'=2k+12, a'=a-1 (a>=2) ; g=4: G'=2k+9, a'=a+4 ; g=5: G'=2k+13, a'=a+6
    exp={3:(lambda k,a:(2*k+12,a-1)),4:(lambda k,a:(2*k+9,a+4)),5:(lambda k,a:(2*k+13,a+6))}
    grid=[(3,[19,21,23,41,101,251],[2,3,8,30]),
          (4,[19,21,23,41,101,251],[0,1,8,30]),
          (5,[19,21,23,41,101,251],[0,1,8,30])]
    allok=True
    for g,kk,aa in grid:
        for k in kk:
            for a in aa:
                Ge,ae=exp[g](k,a)
                t,p,s=build_Z(k,g,a)
                # run long enough to pass the milestone AND go deep into the NEXT generation
                r=run(t,p,s,60_000_000,stop_at_gap=odo(Ge)-1)   # stop only when the NEXT gen's milestone appears
                sm=summarize_miles(r['miles'])
                # first excursion max should be (Ge,ae); second should be odometer(Ge), ae+delta(Ge)
                ok1 = len(sm)>=1 and sm[0][1]==Ge and sm[0][2]==ae
                Ge2,ae2 = odo(Ge), ae+delta(Ge)
                ok2 = len(sm)>=2 and sm[1][1]==Ge2 and sm[1][2]==ae2
                # spurious-milestone probe: any earlier form-match with a DIFFERENT (gap,a) that could
                # fool a first-match detector? i.e. milestone-form instants before the true one with gap>=6
                early=[(st,gg2,aa2) for (st,gg2,aa2) in r['miles'] if st<sm[0][0]-0 and gg2<Ge and gg2>=6 and aa2 is not None]
                flag = "OK " if (ok1 and ok2 and r['unsafe']==0 and r['f1']==0) else "FAIL"
                if flag=="FAIL": allok=False
                print(f"  g={g} k={k:>3} a={a:>2}: {flag} landed={sm[0][:3] if sm else None} exp=({Ge},{ae})"
                      f"  next={'OK' if ok2 else (sm[1] if len(sm)>1 else 'missing')}"
                      f"  unsafe={r['unsafe']} f1={r['f1']} early-form-matches(gap>=6)={len(early)}"
                      + (f" e.g.{early[:2]}" if early else ""))
    print(f"  SUFFIX GRID (incl. k=101,251 UNTESTED in original): all OK = {allok}")
