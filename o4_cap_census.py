#!/usr/bin/env python
# o4_cap_census.py -- Task 1+2 of the C-seam closure attempt (2026-07-06):
#   (1) characterize EVERY C-seam event: generation ordinal, position rel. to rightmost 1 (cap),
#       radius-12 and radius-30 windows, last 40 (state,read,write,move) events, q+2 last-writer,
#       length of the alternating filler left of the seam.
#   (2) enumerate cap-ARRIVAL configurations: every time the head enters the cap region
#       (within D=12 of the rightmost 1), record (state, offset rel rmax, 20-cell window).
#       Check saturation (step of last NEW arrival type).
# Machine: o4 = 1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---  (exact concrete simulation, no acceleration)
import sys, json
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

def win(tape, lo, hi):
    return ''.join(str(tape.get(i,0)) for i in range(lo,hi+1))

def run(N, D=12, WL=16, WR=3):
    tape={}; pos=0; st='A'; prev_st=None
    lastw={}
    rmax=None; ones=0
    ring=deque(maxlen=40)
    cseams=[]; eseam_ct=0
    arrivals={}          # key -> [count, first_step, first_rmax]
    last_new=(-1,None)   # (step, key) of last NEW arrival type
    inside=False
    b1=0; unsafe=0
    # sweep-end enumeration: every B-reads-0 (candidate sweep terminator), keyed by
    # (prev state, radius-6 window). C reads pos+1 next iff prev in sweep; the C-seam
    # is the sub-case window[7]=='1' (C:1->0RA) and then A reads 0 with 1 to its right.
    sweepends={}         # key -> [count, first_step]
    se_last_new=-1
    for s in range(N):
        r=tape.get(pos,0)
        a=M[(st,r)]
        if a is None:
            print("HALT at",s); sys.exit(1)
        if rmax is not None:
            now_inside = pos >= rmax-D
            if now_inside and not inside:
                key=(st, pos-rmax, win(tape, rmax-WL, rmax+WR))
                if key not in arrivals:
                    arrivals[key]=[0,s,rmax]
                    last_new=(s,key)
                arrivals[key][0]+=1
            inside=now_inside
        if st=='B':
            if r==1:
                b1+=1
                if tape.get(pos+1,0)==1: unsafe+=1
            else:
                key=(prev_st, win(tape,pos-8,pos+8))
                e=sweepends.get(key)
                if e is None:
                    sweepends[key]=[1,s]; se_last_new=s
                else: e[0]+=1
        if st=='A' and r==0 and tape.get(pos+1,0)==1:
            if prev_st=='C':
                q=pos
                # maximal alternating region ending at q-1, scanning left
                fl=0; i=q-1
                while fl<50000 and tape.get(i,0)!=tape.get(i+1,0):
                    i-=1; fl+=1
                # distance to the gap: nearest run of >=4 zeros strictly left of q
                gz=None; z=0; i=q-1
                while q-i<200000:
                    if tape.get(i,0)==0:
                        z+=1
                        if z>=4: gz=q-(i+3); break
                    else: z=0
                    i-=1
                lmin=min(tape) if tape else None
                cseams.append(dict(
                    idx=len(cseams), step=s, q=q, rmax=rmax, rel=(q-rmax if rmax is not None else None),
                    w12=win(tape,q-12,q+12), w30=win(tape,q-30,q+8),
                    ring=list(ring), lastw_q2=lastw.get(q+2), alt_len=fl,
                    gap_dist=gz, leftmost=lmin))
            else:
                eseam_ct+=1
        w,d,ns=a
        lastw[pos]=(st,r,w)
        if w==1:
            if r==0: ones+=1
            tape[pos]=1
            if rmax is None or pos>rmax: rmax=pos
        else:
            if r==1:
                ones-=1
                del tape[pos]
                if pos==rmax:
                    if ones==0: rmax=None
                    else:
                        rmax-=1
                        while tape.get(rmax,0)==0: rmax-=1
        ring.append((st,r,w,d))
        prev_st=st; pos+=d; st=ns
    return dict(N=N,b1=b1,unsafe=unsafe,eseams=eseam_ct,cseams=cseams,
                arrivals={repr(k):v for k,v in arrivals.items()},
                last_new_step=last_new[0], last_new_key=repr(last_new[1]),
                sweepends={repr(k):v for k,v in sweepends.items()},
                se_last_new=se_last_new,
                final_rmax=rmax)

if __name__=="__main__":
    N=int(sys.argv[1]) if len(sys.argv)>1 else 30_000_000
    out=sys.argv[2] if len(sys.argv)>2 else None
    res=run(N)
    print(f"N={res['N']:,}  B-reads-1={res['b1']:,}  UNSAFE={res['unsafe']}  E-seams={res['eseams']:,}  C-seams={len(res['cseams'])}")
    print(f"last NEW arrival type at step {res['last_new_step']:,} (of {res['N']:,})  |arrival types|={len(res['arrivals'])}")
    print(f"final rmax={res['final_rmax']}")
    print("\n=== ARRIVAL TYPES (state, offset-vs-rmax, window rmax-16..rmax+3) ===")
    for k,v in sorted(res['arrivals'].items(), key=lambda kv:-kv[1][0]):
        print(f"  count={v[0]:>10,}  first@{v[1]:>12,} (rmax={v[2]})  {k}")
    print("\n=== SWEEP-END (B-reads-0) TYPES:", len(res['sweepends']), " last new @ step", res['se_last_new'], "===")
    for k,v in sorted(res['sweepends'].items(), key=lambda kv:-kv[1][0]):
        print("  count=%12s  first@%12s  %s" % (format(v[0],','), format(v[1],','), k))
    print("\n=== C-SEAMS ===")
    for c in res['cseams']:
        print(f"  #{c['idx']:>2} step={c['step']:>12,} q={c['q']:>6} rmax={c['rmax']} rel={c['rel']} alt_len={c['alt_len']} gap_dist={c['gap_dist']} leftmost={c['leftmost']} lastw(q+2)={c['lastw_q2']}")
        print(f"      w12(q+-12) ={c['w12']}   (head A@center reads 0)")
        print(f"      w30(q-30..q+8)={c['w30']}")
    # template check: are all C-seams identical modulo translation (after startup)?
    tmpl={}
    for c in res['cseams']:
        key=(c['rel'],c['w12'],tuple(map(tuple,c['ring'])))
        tmpl.setdefault(key,[]).append(c['idx'])
    print(f"\n=== C-SEAM TEMPLATES (rel, w12, last-40-events) : {len(tmpl)} distinct ===")
    for k,idxs in tmpl.items():
        print(f"  rel={k[0]} w12={k[1]}  instances={idxs}")
    if out:
        with open(out,'w') as f: json.dump(res,f,indent=1,default=repr)
        print("\nJSON dumped to",out)
