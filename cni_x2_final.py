#!/usr/bin/env python3
"""Rigorous final classification of the 21 near-x2 machines.
Criterion for GENUINE geometric x2: in total1 OR maxrun, the segment-peak sequence is
(a) growing (last peak > 4x an early tail peak), (b) consistent (cv of consecutive peak
ratios < 0.22), (c) ratio in [1.8,2.2], (d) >=6 peaks.  Also test the STRONG signature:
consecutive peaks fit v'=2v+c (affine doubling) -> report c and residual.
"""
import sys, json
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import simulate, _segments
import statistics as S

def peakseq(fast, idx):
    v=[f[idx] for f in fast]; segs=_segments(v)
    return [max(v[a:b]) for a,b in segs]

def affine_double_fit(pk):
    """fit pk[k+1] = 2*pk[k] + c via median c; return (c, max_resid_rel) on last 8."""
    tail=pk[-9:]
    if len(tail)<5: return None
    cs=[tail[i+1]-2*tail[i] for i in range(len(tail)-1)]
    c=S.median(cs)
    resid=max(abs((tail[i+1]-2*tail[i])-c) for i in range(len(tail)-1))
    scale=tail[-1] or 1
    return (c, round(resid/scale,4))

def classify(spec, cap):
    outc,step,fast,slow,ftail,nL,nR=simulate(spec,cap)
    best=None
    for ob,idx in [('total1',2),('maxrun',3)]:
        pk=peakseq(fast,idx)
        if len(pk)<6: continue
        tp=pk[-9:]
        if tp[0]<=0 or tp[-1] < 4*tp[0]: continue
        pr=[tp[i+1]/tp[i] for i in range(len(tp)-1) if tp[i]>0]
        med=S.median(pr); cv=S.pstdev(pr)/med if med else 9
        if 1.8<med<2.2 and cv<0.22:
            af=affine_double_fit(pk)
            cand=(ob,round(med,4),round(cv,3),af,pk[-6:])
            if best is None or cv<best[2]:
                best=cand
    return best

if __name__=="__main__":
    cap=int(sys.argv[1]) if len(sys.argv)>1 else 30_000_000
    rows=json.load(open('mse_census_rows.json'))
    x2=[r for r in rows if r.get('reported')=='~2(cand-new)']
    genuine=[]; artifact=[]
    for r in x2:
        c=classify(r['spec'],cap)
        if c: genuine.append((r['spec'],r['rho'],c))
        else: artifact.append((r['spec'],r['rho']))
    print(f"=== GENUINE geometric x2 (clean doubling): {len(genuine)} ===")
    for sp,rho,c in sorted(genuine,key=lambda x:x[2][2]):
        ob,med,cv,af,pk=c
        print(f"  cv={cv} {ob} ratio={med} affine(v'=2v+c): c={af[0]} resid={af[1]}  peaks={pk}")
        print(f"      {sp}")
    print(f"\n=== ARTIFACT (no clean doubling): {len(artifact)} ===")
    for sp,rho in artifact:
        print(f"  rho={rho:.3f}  {sp}")
    json.dump(dict(genuine=[(s,r) for s,r,c in genuine],artifact=artifact),open('x2_final_out.json','w'))
