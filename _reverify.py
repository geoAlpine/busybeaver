from wbounce2 import find_periodic_growth, build, faithful, closure as wclosure
from bouncer_prove_sound import records
from wsim import step as wstep, cfg_to_tape, exps_valid
from collections import defaultdict
from bouncer_prove2 import parse

def wb2_proof(spec):
    M=parse(spec); recs,h=records(spec,20000)
    if h: return None
    buckets=defaultdict(list)
    for r in recs: buckets[(r[2],r[1])].append(r)
    for key,rs in buckets.items():
        if len(rs)<3: continue
        for i in range(len(rs)-2):
            g=find_periodic_growth(rs[i],rs[i+1])
            if not g: continue
            b=build(rs[i],g)
            if not b: continue
            start,base=b
            if base<1 or not faithful(start,base,rs[i]): continue
            cfg=start
            for s in range(6000):
                cfg,op=wstep(M,cfg)
                if op[0] in ('HALT','STUCK'): break
                if not exps_valid(cfg,base): break
                if s>=1:
                    d=wclosure(start,cfg)
                    if d: return start,base,d
    return None

def mat(cfg,n):
    tape,head,state=cfg_to_tape(cfg,n)
    lo=min([head]+list(tape)); hi=max([head]+list(tape))
    return state,tuple(tape.get(j,0) for j in range(lo,hi+1)),head-lo

def visited_sequence(spec,start,base,d,maxn=6,cap=400000):
    M=parse(spec)
    targets={}
    tstates=set()
    for n in range(base,base+maxn*d+1):
        s,c,hh=mat(start,n); targets[(s,c,hh)]=n; tstates.add(s)
    tape={};state='A';head=0;seq=[]
    lo=hi=0
    for t in range(cap):
        if state in tstates:
            cur=(state,tuple(tape.get(j,0) for j in range(lo,hi+1)),head-lo)
            n=targets.get(cur)
            if n is not None and (not seq or seq[-1]!=n): 
                seq.append(n)
                if len(seq)>=5: break
        r=tape.get(head,0);tr=M[state].get(r)
        if tr is None: break
        w,dd,ns=tr; tape[head]=w; state=ns; head+=1 if dd=='R' else -1
        if head<lo: lo=head
        if head>hi: hi=head
    return seq

reps=[l.strip() for l in open('holdouts3_reps.txt') if l.strip()]
extra=['1RB1LA_0LC0RE_1LD1LB_1RE1LF_1RC0RA_0RC---']
bad=[]
for spec in reps+extra:
    p=wb2_proof(spec)
    if p is None: continue
    start,base,d=p
    seq=visited_sequence(spec,start,base,d)
    expect=list(range(base,base+d*len(seq),d))[:len(seq)]
    ok=(len(seq)>=2 and seq==expect)
    if not ok:
        bad.append((spec,base,d,seq))
        print('UNSOUND %-40s base=%d d=%d expect=%s real=%s'%(spec,base,d,expect,seq),flush=True)
print('=== %d wb2-proofs concretely UNSOUND ==='%len(bad),flush=True)
