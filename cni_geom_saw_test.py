#!/usr/bin/env python3
"""CORRECTED discriminator: a genuine value-x(p/q) odometer shows a GROWING GEOMETRIC
SAWTOOTH in some observable -- segment peaks GROW geometrically (each ~p/q x prev) across
many macro-periods, spanning a large range (last_peak/early_peak >> 1). A linear counter
or bounded/bouncer shows NO such observable (peaks flat, or no resets, or erratic).

Test per observable: segments via _segments; take peaks; require
  (a) >=8 segments, (b) tail peaks strictly growing: last>3x the 8th-from-last,
  (c) median consecutive peak-ratio in (1.15,6), cv<0.20.
Validated to FIRE on o4/o5/o15/o18/o10/SN (sawtooth-caught known engines) and be silent
on non-growing observables. Antihydra/o7/o8 are transfer-caught (sawtooth-silent) -- expected.
"""
import sys, json
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import simulate, _segments, match_engine, est_transfer
from fractions import Fraction
import statistics as S

def geom_saw(fast):
    best=None
    for ob,idx in [('total1',2),('maxrun',3),('width',4)]:
        vals=[f[idx] for f in fast]
        segs=_segments(vals)
        if len(segs)<8: continue
        peaks=[max(vals[a:b]) for a,b in segs]
        tp=peaks[-10:]
        if tp[0]<=0 or tp[-1] < 3*tp[0]:   # must span a large geometric range at the tail
            continue
        pr=[tp[i+1]/tp[i] for i in range(len(tp)-1) if tp[i]>0]
        if len(pr)<5: continue
        med=S.median(pr); cv=S.pstdev(pr)/med if med else 99
        if 1.15<med<6 and cv<0.20:
            cand=(ob,round(med,4),round(cv,3),tp[-4:])
            if best is None or cv<best[2]:
                best=cand
    return best

def analyze(spec,cap):
    outc,step,fast,slow,ftail,nL,nR=simulate(spec,cap)
    gs=geom_saw(fast)
    tr,_=est_transfer(ftail)
    return dict(nfast=len(fast), geomsaw=gs, transfer=str(tr) if tr else None)

def work(a):
    sp,cap=a
    try: return dict(spec=sp,**analyze(sp,cap))
    except Exception as e: return dict(spec=sp,err=str(e))

if __name__=="__main__":
    import multiprocessing as mp
    from mse_extract import NAMED
    cap=12_000_000
    mode=sys.argv[1] if len(sys.argv)>1 else 'gate'
    if mode=='gate':
        print("=== GATE on known engines (must FIRE geomsaw on o4/o5/o15/o18/o10/SN) ===")
        for name in ['o4','o5','o15','o18','o10','o8','o7','SpaceNeedle','Antihydra','o16','o13','o14']:
            sp,true=NAMED[name]
            r=analyze(sp,cap)
            print(f"{name:11} true={str(float(true)) if true else None:5} geomsaw={r['geomsaw']} transfer={r['transfer']}")
    else:
        robust=json.load(open('robust_out.json'))
        specs=[r['spec'] for r in robust]
        rob={r['spec']:r for r in robust}
        ctx=mp.get_context('fork')
        with ctx.Pool(8) as pool:
            res=pool.map(work,[(s,cap) for s in specs],chunksize=2)
        out=[]
        for r in res:
            sp=r['spec']; rb=rob[sp]
            gs=r.get('geomsaw'); tr=r.get('transfer')
            rep12=rb['rep12']
            genuine = gs is not None
            drift_known = rep12 and not rep12.startswith('~')
            if genuine:
                eng,f=match_engine(gs[1])
                if eng and not eng.startswith('~'):
                    cls='MIS-EXTRACTED-KNOWN'; note=f'geomsaw {gs[1]}~{eng}'
                else:
                    cls='GENUINE-NEW-CANDIDATE'; note=f'geomsaw {gs[1]} cv={gs[2]}'
            elif tr:
                cls='HAS-TRANSFER'; note=f'transfer={tr}'
            elif drift_known:
                cls='MIS-EXTRACTED-KNOWN'; note=f'drift->{rep12} (no geomsaw)'
            else:
                cls='ARTIFACT'; note='no geomsaw; '+str(rb['rep4'])+'->'+str(rep12)
            out.append(dict(spec=sp,rep4=rb['rep4'],rep12=rep12,rho4=rb['rho4'],geomsaw=gs,transfer=tr,cls=cls,note=note))
        from collections import Counter
        for o in sorted(out,key=lambda o:(o['cls'],o['rho4'] or 0)):
            print(f"{o['cls']:22} rho4={(o['rho4'] or 0):.3f} {str(o['rep4']):>15}  {o['note']}")
        print("\nCLASS TALLY:",dict(Counter(o['cls'] for o in out)))
        json.dump(out,open('geom_saw_out.json','w'))
