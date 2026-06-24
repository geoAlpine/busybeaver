import sys
from translated_cyclers import decide_translated
from bouncer_prove import prove as ss_prove
from wbounce import prove as wb_prove
specs=[l.strip() for l in open('_bbdata/bb6_holdouts_1104.txt') if l.strip()]
from collections import Counter
res=Counter(); dec=[]
for i,sp in enumerate(specs):
    v="HOLDOUT"
    try:
        if decide_translated(sp, time_limit=100_000, space_limit=40_000)[0]=="NEVER_HALTS": v="TCYC"
        elif ss_prove(sp, steps=8000, max_macro=1200)[0]=="NEVER_HALTS": v="BOUNCE-S"
        elif wb_prove(sp, steps=8000, max_macro=1200)[0]=="NEVER_HALTS": v="BOUNCE-W"
    except Exception: v="ERR"
    res[v]+=1
    if v not in ("HOLDOUT","ERR"): dec.append((sp,v))
print("=== fast deciders (translated-cycler + bouncers) over all 1104 ===")
for k,v in res.most_common(): print(f"  {k}: {v}")
print(f"decided by fast suite: {len(dec)}")
for sp,w in dec[:15]: print(f"  {w}: {sp}")
