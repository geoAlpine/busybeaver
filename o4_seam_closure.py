# o4 SEAM-CLOSURE / large-G saturation (2026-07-06)
# o4: 1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---
# (A) push head-window saturation to G~1e4 : does |W| stay constant?
# (B) push disturbance-width to G~1e4       : stays <= 8?
# (C) trace the LEFT gap-edge seam interaction at two different G : same finite computation?
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

def big(N, R=6):
    tape=defaultdict(int); pos=0; st='A'
    seen=set(); maxpos=0; minpos=0
    # disturbance width tracking
    dist_by_bucket=defaultdict(int)
    b_unsafe=0; b1=0
    milestones=[]  # steps where |W| grows: (step,G,newsize)
    prevsize=0
    report=[]
    nextrep=2000
    for s in range(N):
        r=tape[pos]
        if st=='B' and r==1:
            b1+=1
            if tape.get(pos+1,0)==1: b_unsafe+=1
        win=(st,)+tuple(tape.get(pos+o,0) for o in range(-R,R+1))
        if win not in seen:
            seen.add(win)
        a=M[(st,r)]
        if a is None: return dict(halt=True,step=s)
        w,d,ns=a
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns
        if pos>maxpos: maxpos=pos
        if pos<minpos: minpos=pos
        # disturbance sample
        if s % 20000 == 0 and s>0:
            G=maxpos-minpos
            if len(seen)!=prevsize:
                milestones.append((s,G,len(seen))); prevsize=len(seen)
            # rle disturbance
            keys=sorted(tape.keys())
            if keys:
                lo,hi=keys[0],keys[-1]
                rle=[]; val=tape.get(lo,0); cnt=0
                for q in range(lo,hi+1):
                    v=tape.get(q,0)
                    if v==val: cnt+=1
                    else: rle.append((val,cnt)); val=v; cnt=1
                rle.append((val,cnt))
                zr=sorted([c for (v,c) in rle if v==0],reverse=True)
                biggap=zr[0] if zr else 0
                nonunit=0; skip=False
                for (v,c) in rle:
                    if v==0 and c==biggap and not skip: skip=True; continue
                    if c!=1: nonunit+=c
                bucket=(G//1000)*1000
                dist_by_bucket[bucket]=max(dist_by_bucket[bucket],nonunit)
        if maxpos-minpos>=nextrep and nextrep<=12000:
            report.append((nextrep,s,len(seen),b_unsafe))
            nextrep+=2000
    return dict(halt=False,seen=len(seen),gmax=maxpos-minpos,
                dist=dict(dist_by_bucket),milestones=milestones,
                report=report,b1=b1,b_unsafe=b_unsafe)

if __name__=='__main__':
    print("Pushing to large G (R=6 head-window set, disturbance width, safety)...")
    r=big(130_000_000, R=6)
    print("halt:",r.get('halt'))
    print(f"final Gmax ~ {r['gmax']},  |W|(R=6) = {r['seen']}")
    print(f"B-reads-1 = {r['b1']:,},  UNSAFE = {r['b_unsafe']}")
    print("\n|W| growth milestones (step, G, |W|):")
    for (s,G,sz) in r['milestones']:
        print(f"   step={s:>11,}  G~{G:>6}  |W|={sz}")
    print("\ndisturbance (non-unit-run) width by G bucket:")
    for b in sorted(r['dist']):
        print(f"   G in [{b},{b+1000}): max non-unit width = {r['dist'][b]}")
    print("\n|W| at G milestones (G, step, |W|, cum-unsafe):")
    for (g,s,sz,u) in r['report']:
        print(f"   G>={g:>6}: step={s:>11,}  |W|={sz}  unsafe={u}")
