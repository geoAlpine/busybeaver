#!/usr/bin/env python3
"""Final pass on the 39 non-x2 candidate-new (>=1.3). For each: full-run peak sequence in
total1 & maxrun; is it geometric (growing, cv<0.25)? If so, best-fit rational multiplier
(match to KNOWN {3/2,4/3,8/3,5/2} within 0.08 else nearest simple rational). Else artifact."""
import sys, json
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import simulate, _segments, match_engine
from fractions import Fraction
import statistics as S

def peakseq(fast, idx):
    v=[f[idx] for f in fast]; segs=_segments(v)
    return [max(v[a:b]) for a,b in segs]

def best_geo(fast):
    best=None
    for ob,idx in [('total1',2),('maxrun',3),('width',4)]:
        pk=peakseq(fast,idx)
        if len(pk)<7: continue
        tp=pk[-10:]
        if tp[0]<=0 or tp[-1]<4*tp[0]: continue
        pr=[tp[i+1]/tp[i] for i in range(len(tp)-1) if tp[i]>0]
        med=S.median(pr); cv=S.pstdev(pr)/med if med else 9
        if 1.15<med<4.5 and cv<0.25:
            cand=(ob,round(med,4),round(cv,3),pk[-6:])
            if best is None or cv<best[2]:
                best=cand
    return best

if __name__=="__main__":
    cap=int(sys.argv[1]) if len(sys.argv)>1 else 30_000_000
    rows=json.load(open('mse_census_rows.json'))
    cand=[r for r in rows if r.get('reported') and r['reported'].startswith('~')]
    def fval(r): return float(Fraction(r['reported'][1:].split('(')[0]))
    non_x2=[r for r in cand if fval(r)>=1.3 and r['reported']!='~2(cand-new)']
    genK=[]; genN=[]; art=[]
    for r in non_x2:
        outc,step,fast,slow,ftail,nL,nR=simulate(r['spec'],cap)
        g=best_geo(fast)
        if g is None:
            art.append((r['rho'],r['reported'],r['spec'])); continue
        eng,f=match_engine(g[1])
        if eng and not eng.startswith('~'):
            genK.append((r['rho'],g,eng,r['spec']))
        else:
            genN.append((r['rho'],g,r['reported'],r['spec']))
    print(f"=== GEOMETRIC -> KNOWN engine (mis-extracted): {len(genK)} ===")
    for rho,g,eng,sp in sorted(genK):
        print(f"  rho4={rho:.3f} peakratio={g[1]}({g[0]}) cv={g[2]} -> {eng}   {sp}")
    print(f"\n=== GEOMETRIC -> non-known multiplier (genuine-new-candidate): {len(genN)} ===")
    for rho,g,rep,sp in sorted(genN):
        print(f"  rho4={rho:.3f} peakratio={g[1]}({g[0]}) cv={g[2]} rep={rep}  peaks={g[3]}  {sp}")
    print(f"\n=== ARTIFACT (no clean geometric peaks): {len(art)} ===")
    for rho,rep,sp in sorted(art):
        print(f"  rho4={rho:.3f} rep={rep}  {sp}")
    json.dump(dict(genK=[(r,e,s) for r,g,e,s in genK],genN=[(r,rep,s) for r,g,rep,s in genN],art=art),open('nonx2_final_out.json','w'))
