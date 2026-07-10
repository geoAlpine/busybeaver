#!/usr/bin/env python3
"""Carry-dichotomy structural probes (2026-07-11).
Part 1: the 7 x2-species machines -- register-law rigidity probes:
  (a) exact peak recurrence v' = 2v + d_k : is d_k constant / arithmetic drift / erratic?
  (b) reset values (segment minima after each peak): bounded small set vs growing?
  (c) final-milestone 1-run cascade: successive block-length ratios ~2 (rigid shift cascade)?
  (d) halt gate location (state/read with ---).
Part 2: the 5 unpinned candidate-new -- geometric peak ratio at cap, d_k drift under best
  rational, block-transfer signal (q>1 residue engine?).
Part 3: sample of the 105 robust collapsed holdouts -- confirm engine ratio, note q.
All outputs [OBSERVED, exact simulation]. Decides NO halting.
"""
import sys, json, statistics as S
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import simulate, _segments, parse
from fractions import Fraction

CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 12_000_000

X2 = [
 '1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE',  # primary (the mapped one)
 '1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD',  # peak-twin of primary
 '1RB0RE_1RC1LF_0LD0RE_---1LE_1RA0LB_1LB0LC',  # total1 pair A
 '1RB0RC_1LC1RA_0RF0LD_1LE0RB_1LB0LD_---1RD',  # total1 pair B
 '1RB0LD_1LC0RA_1RA1LB_1LA1LE_1RF0LC_---0RE',  # clean total1
 '1RB0LB_1LC1LB_1RD1LA_0RE0RE_0RA1RF_---1RD',  # noisy maxrun
 '1RB0RB_1LC0LF_1RD0LB_1RE1RC_0RA---_1LA1RE',  # noisy total1
]
UNPINNED = [
 ('~11/7', '1RB1RE_1LC1RE_---1LD_1LE0LB_0RF0LD_1RD1RA'),
 ('~7/5',  '1RB0RC_1RC---_1LD1RE_1LE0LD_1RA0LF_0RC0RB'),
 ('~13/7', '1RB0LE_1RC0RF_0RD0RB_1RE0RC_1LA0LA_1RA---'),
 ('~8/5',  '1RB1RE_1LC0RA_1RD0LB_1LB1RC_1LF0RD_---0LE'),
 ('~23/7', '1RB1RE_1LC0LE_1RD0LB_0RA1RC_0RC0RF_1RA---'),
]

def haltgate(spec):
    out=[]
    for si,st in enumerate(spec.split('_')):
        for r,t in enumerate((st[0:3],st[3:6])):
            if t[0]=='-' or t[2]=='-': out.append(f"{chr(65+si)}:{r}")
    return out

def peak_reset(fast, idx):
    v=[f[idx] for f in fast]; segs=_segments(v)
    pk=[max(v[a:b]) for a,b in segs]
    rs=[min(v[a:b]) for a,b in segs]
    return pk, rs

def probe_x2(spec):
    outc, step, fast, slow, ftail, nL, nR = simulate(spec, CAP)
    res = {'spec': spec, 'outc': outc, 'gate': haltgate(spec)}
    best=None
    for ob,idx in [('maxrun',3),('total1',2)]:
        pk,rs = peak_reset(fast, idx)
        if len(pk)<7: continue
        tp=pk[-9:]
        if tp[0]<=0 or tp[-1]<3*tp[0]: continue
        d=[tp[i+1]-2*tp[i] for i in range(len(tp)-1)]
        # classify d_k: constant / arithmetic (constant 2nd diff) / erratic
        if len(set(d))==1: law=f"EXACT v'=2v{d[0]:+d}"
        else:
            dd=[d[i+1]-d[i] for i in range(len(d)-1)]
            if len(set(dd))==1: law=f"ARITH-DRIFT v'=2v+d_k, d_k={d}, step {dd[0]:+d}"
            elif max(dd)-min(dd)<=2: law=f"NEAR-ARITH d_k={d}"
            else: law=f"ERRATIC d_k={d}"
        scale=max(abs(x) for x in d) / (tp[-1] or 1)
        cand=(ob, tp, law, rs[-8:], scale)
        if best is None or ('EXACT' in law and 'EXACT' not in best[2]): best=cand
        if best[2].startswith('ERRATIC') and not law.startswith('ERRATIC'): best=cand
    res['peaks']=best
    # cascade check: final milestone RLE 1-runs
    if ftail:
        r=ftail[-1][1]
        ones=[n for c,n in r if c==1 and n>=3]
        top=sorted(ones)[-8:]
        rat=[round(top[i+1]/top[i],3) for i in range(len(top)-1)] if len(top)>2 else []
        res['cascade']=(top, rat)
    return res

def probe_unpinned(name, spec):
    outc, step, fast, slow, ftail, nL, nR = simulate(spec, CAP)
    out={'name':name,'spec':spec,'outc':outc,'gate':haltgate(spec)}
    found=[]
    for ob,idx in [('total1',2),('maxrun',3),('width',4)]:
        pk,rs = peak_reset(fast, idx)
        if len(pk)<7: continue
        tp=pk[-10:]
        if tp[0]<=0 or tp[-1]<3*tp[0]: continue
        pr=[tp[i+1]/tp[i] for i in range(len(tp)-1)]
        med=S.median(pr); cv=S.pstdev(pr)/med if med else 9
        found.append((ob, round(med,4), round(cv,3), tp[-6:], rs[-6:]))
    out['geo']=found
    return out

def probe_holdout(spec, reported):
    outc, step, fast, slow, ftail, nL, nR = simulate(spec, CAP)
    best=None
    for ob,idx in [('total1',2),('maxrun',3),('width',4)]:
        v=[f[idx] for f in fast]; segs=_segments(v)
        pk=[max(v[a:b]) for a,b in segs]
        if len(pk)<6: continue
        tp=pk[-9:]
        if tp[0]<=0 or tp[-1]<2*tp[0]: continue
        pr=[tp[i+1]/tp[i] for i in range(len(tp)-1)]
        med=S.median(pr); cv=S.pstdev(pr)/med if med else 9
        if best is None or cv<best[2]: best=(ob,round(med,4),round(cv,3))
    return {'spec':spec,'reported':reported,'outc':outc,'geo':best}

if __name__=='__main__':
    print(f"=== PART 1: the 7 x2-species (cap {CAP}) ===")
    for sp in X2:
        r=probe_x2(sp)
        print(f"\n{sp}  outc={r['outc']} gate={r['gate']}")
        if r.get('peaks'):
            ob,tp,law,rs,scale=r['peaks']
            print(f"  [{ob}] peak law: {law}  (rel scale {scale:.4f})")
            print(f"  peaks tail: {tp}")
            print(f"  resets tail: {rs}")
        else: print("  no clean peak sequence")
        if r.get('cascade'):
            print(f"  cascade 1-runs {r['cascade'][0]} ratios {r['cascade'][1]}")
    print(f"\n=== PART 2: the 5 unpinned candidate-new (cap {CAP}) ===")
    for name,sp in UNPINNED:
        r=probe_unpinned(name,sp)
        print(f"\n{name}  {sp}  outc={r['outc']} gate={r['gate']}")
        for ob,med,cv,tp,rs in r['geo']:
            print(f"  [{ob}] ratio={med} cv={cv} peaks={tp} resets={rs}")
        if not r['geo']: print("  no geometric peaks at this cap")
    print(f"\n=== PART 3: sample of the 105 robust collapsed holdouts ===")
    rows=json.load(open('/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/8b7a3f39-ce4e-4044-afe8-60ce3b3aedcf/scratchpad/mse_census_rows.json'))
    robust=[x for x in rows if x.get('reported') and x['reported'].startswith('x')
            and x['conf'] and ('high' in x['conf'] or 'med' in x['conf'])]
    print(f"(robust count = {len(robust)})")
    import random; random.seed(7)
    sample=random.sample(robust,8)
    for x in sample:
        r=probe_holdout(x['spec'], x['reported'])
        print(f"  {x['spec']}  reported={x['reported']} src={x['src']}  re-probe geo={r['geo']}")
