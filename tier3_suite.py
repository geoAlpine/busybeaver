import sys
from suite import verdict
specs=[l.strip() for l in open('_bbdata/bb6_holdouts_1104.txt') if l.strip()]
from collections import Counter
res=Counter(); decided=[]
for i,sp in enumerate(specs):
    try:
        v,which=verdict(sp, sim_cap=200_000, bsteps=8000, bmacro=1200)
    except Exception as e:
        v,which="ERR",str(e)[:30]
    res[v]+=1
    if v=="NEVER_HALTS": decided.append((sp,which))
    if v=="HALTS": decided.append((sp,which))
    if (i+1)%100==0: print(f"  {i+1}/1104 done: {dict(res)}", file=sys.stderr)
print("=== SOUND SUITE over all 1104 holdouts ===")
for k,v in res.most_common(): print(f"  {k}: {v}")
print(f"\nmachines our sound suite DECIDED: {len(decided)}")
for sp,w in decided[:20]: print(f"  {w}: {sp}")
