# Reliable concrete check: does the REAL machine map C(base+j) -> C(base+j+d) exactly, for j=0,1,2?
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

def canon_from_cfg(cfg,n):
    tape,head,state=cfg_to_tape(cfg,n)
    return canon(state, dict(tape), head)
def canon(state, tape, head):
    keys=[k for k,v in tape.items() if v]
    lo=min(keys+[head]); hi=max(keys+[head])
    while lo<head and tape.get(lo,0)==0: lo+=1
    while hi>head and tape.get(hi,0)==0: hi-=1
    return (state, tuple(tape.get(j,0) for j in range(lo,hi+1)), head-lo)

def reaches(spec, src_cfg, n_src, tgt_canon, cap=2_000_000):
    """run real machine from materialized C(n_src); does it reach tgt_canon without halting?"""
    M=parse(spec)
    tape,head,state=cfg_to_tape(src_cfg,n_src); tape=dict(tape)
    tstate=tgt_canon[0]
    for t in range(cap):
        r=tape.get(head,0); tr=M[state].get(r)
        if tr is None: return "HALT"
        w,d,ns=tr; tape[head]=w; state=ns; head+=1 if d=='R' else -1
        if state==tstate and canon(state,tape,head)==tgt_canon: return "REACH@%d"%t
    return "MISS"

reps=[l.strip() for l in open('holdouts3_reps.txt') if l.strip()]
extra=['1RB1LA_0LC0RE_1LD1LB_1RE1LF_1RC0RA_0RC---']
unsound=[]; sound=0; incon=[]
for spec in reps+extra:
    p=wb2_proof(spec)
    if p is None: continue
    start,base,d=p
    res=[]
    for j in range(2):                          # check C(base+j) -> C(base+j+d) for j=0,1
        src=base+j; tgt=canon_from_cfg(start, base+j+d)
        res.append(reaches(spec,start,src,tgt))
    allreach=all(r.startswith("REACH") for r in res)
    if allreach: sound+=1
    elif any(r=="HALT" for r in res): unsound.append((spec,base,d,res)); print("HALT-UNSOUND",spec,base,d,res,flush=True)
    else: 
        unsound.append((spec,base,d,res)); print("NONREACH-UNSOUND %-40s base=%d d=%d %s"%(spec,base,d,res),flush=True)
print("=== wb2 proofs: sound=%d  suspect=%d ==="%(sound,len(unsound)),flush=True)
