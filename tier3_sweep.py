import sys, math
def parse(spec):
    M=[]
    for st in spec.split('_'):
        ts=[st[i:i+3] for i in (0,3)]; row=[]
        for t in ts:
            if t[0]=='-' or t[2] in 'Z-': row.append(None)
            else: row.append((int(t[0]), 1 if t[1]=='R' else -1, ord(t[2])-ord('A')))
        M.append(row)
    return M
def run_profile(spec, limit=400000):
    try: M=parse(spec)
    except: return ('PARSE_ERR',)
    SZ=1<<21; tape=bytearray(SZ); off=SZ//2
    pos=off; st=0; lo=pos; hi=pos
    samples={}; checkt=[limit//16,limit//4,limit//2,limit-1]
    for step in range(limit):
        r=tape[pos]
        tr=M[st][r]
        if tr is None: return ('HALT',step)
        w,d,ns=tr; tape[pos]=w; pos+=d; st=ns
        if pos<lo: lo=pos
        if pos>hi: hi=pos
        if step in checkt: samples[step]=hi-lo+1
    ws=[samples.get(t,0) for t in checkt]
    # growth signature
    if ws[0]<1: return ('SMALL', ws)
    wsqrt=[w/math.sqrt(t) for w,t in zip(ws,checkt)]
    ratio_env = wsqrt[-1]/wsqrt[0] if wsqrt[0]>0 else 0  # ~1 poly-envelope, <1 exponential
    growth = ws[-1]/ws[0] if ws[0]>0 else 0
    cls = 'POLY-env' if ratio_env>0.6 else 'EXP-env'
    return ('RUN', ws, round(ratio_env,3), cls)

specs=[l.strip() for l in open('_bbdata/bb6_holdouts_1104.txt') if l.strip()]
print(f"total holdouts: {len(specs)}")
from collections import Counter
cat=Counter(); poly=0; expn=0; halt=0; small=0; err=0; widths_exp=[]
for i,sp in enumerate(specs):
    r=run_profile(sp)
    tag=r[0]
    if tag=='HALT': halt+=1; cat['HALT']+=1
    elif tag=='SMALL': small+=1; cat['SMALL/cycler']+=1
    elif tag=='PARSE_ERR': err+=1
    elif tag=='RUN':
        cat[r[3]]+=1
        if r[3]=='POLY-env': poly+=1
        else: expn+=1
    if (i+1)%200==0: print(f"  ...{i+1} done", file=sys.stderr)
print("\n=== TIER 3 full-frontier classification (1104 holdouts) ===")
for k,v in cat.most_common(): print(f"  {k:18s}: {v}")
print(f"\nhalt-within-limit: {halt}  small/cycler-like: {small}  POLY-envelope: {poly}  EXP-envelope: {expn}  parse-err: {err}")
