#!/usr/bin/env python
# RED TEAM attack 1 (locality/composition) applied to the SUFFIX lemma -- the sharpest probe:
# For each g in {3,4,5}, over a (k,a) grid: record the full suffix trace Z(k,g,a) -> milestone.
#   (i)  compressed skeleton identical across the grid (thresholds 6/8/10/12);
#   (ii) sweep lengths exactly affine in (k,a):  L = c0 + c1*k + c2*a;
#   (iii) EVERY episode step's position sits at a (k,a)-INDEPENDENT offset from at least one
#         structural landmark (zone-left 0, cap 2k..2k+3, filler-left 2k+4+g,
#         filler-right 2k+4+g+2a+3, final-head/new-milestone position).
#        If some episode step has NO invariant landmark offset => the locality generalization
#        step is UNJUSTIFIED for that episode (a k- or a-dependent read).
from collections import defaultdict
from o4_redteam_suffix import TT, build_Z, parse_filler

def run_suffix_trace(k,g,a,maxsteps=10_000_000):
    tape0,pos,st=build_Z(k,g,a)
    tape=defaultdict(int)
    for kk,v in tape0.items(): tape[kk]=v
    sup=set(kk for kk,v in tape0.items() if v)
    trace=[]; poss=[]
    for s in range(maxsteps):
        if st=='E' and sup and pos<min(sup):
            mn=min(sup); mx=max(sup)
            f=''.join(str(tape[i]) for i in range(mn,mx+1))
            aa=parse_filler(f)
            if aa is not None and mn-pos>=6:
                return dict(trace=trace, poss=poss, G=mn-pos, a=aa, endpos=pos)
        r=tape[pos]; act=TT[(st,r)]
        if act is None: return dict(halt=True, steps=s)
        w,d,ns=act
        trace.append((st,r,w,d)); poss.append(pos)
        if w==0: tape.pop(pos,None); sup.discard(pos)
        else: tape[pos]=1; sup.add(pos)
        pos+=d; st=ns
    return dict(timeout=True)

def compress_idx(trace, thresh=8):
    """Return list of items: ('SWEEP', cyc, start_idx, length) or ('E', step, idx)."""
    out=[]; i=0; n=len(trace)
    while i<n:
        j=i
        while j+2<n and trace[j+2]==trace[j]: j+=1
        L=j+2-i
        if L>=thresh and trace[i]!=trace[i+1]:
            take=L-(L%2)
            out.append(('SWEEP',(trace[i],trace[i+1]),i,take)); i+=take
        else:
            out.append(('E',trace[i],i)); i+=1
    return out

def landmarks(k,g,a,endpos):
    return {'zoneL':0, 'capL':2*k, 'capR':2*k+3, 'filL':2*k+4+g, 'filR':2*k+4+g+2*a+3,
            'end':endpos}

if __name__=='__main__':
    ks=[19,21,23,41,101,251]; aas=[2,5,8,30]
    for g in (3,4,5):
        print(f"================ SUFFIX g={g} locality audit ================")
        data={}
        for k in ks:
            for a in aas:
                if g==3 and a<2: continue
                r=run_suffix_trace(k,g,a)
                assert 'trace' in r, (k,g,a,r)
                data[(k,a)]=r
        # (i) skeleton identity at multiple thresholds
        for th in (6,8,10,12):
            skels={}
            for key,r in data.items():
                comp=compress_idx(r['trace'],th)
                skels[key]=[(e[0],e[1]) for e in comp]
            keys=list(skels)
            same=all(skels[key]==skels[keys[0]] for key in keys)
            n_ep=sum(1 for e in skels[keys[0]] if e[0]=='E')
            n_sw=len(skels[keys[0]])-n_ep
            print(f"  thresh={th:>2}: skeleton identical over (k,a) grid: {same}  episodes={n_ep} sweeps={n_sw}")
        # find the largest a-floor sub-grid + threshold where the skeleton is identical
        keys=list(data)
        th_use=None; amin_use=None
        for amin in (0,5,8):
            for th in (8,6,10,12):
                sub=[key for key in keys if key[1]>=amin]
                sk={key:[(e[0],e[1]) for e in compress_idx(data[key]['trace'],th)] for key in sub}
                if all(sk[key]==sk[sub[0]] for key in sub):
                    th_use=th; amin_use=amin; break
            if th_use is not None: break
        print(f"  [i] largest stable sub-grid: a>={amin_use} at thresh={th_use}")
        keys=[key for key in keys if key[1]>=amin_use]
        comps={key:compress_idx(data[key]['trace'],th_use) for key in keys}
        sweeps={key:[e[3] for e in comps[key] if e[0]=='SWEEP'] for key in keys}
        n_s=len(sweeps[keys[0]])
        # fit with 3 grid points: (19,2/..),(21,same a),(19, other a)
        avail=sorted({key[1] for key in keys})
        a0=avail[0]; a1=avail[-2] if len(avail)>2 else avail[-1]
        k0,k1=ks[0],ks[1]
        aff_ok=True; coefs=[]
        for i in range(n_s):
            y00=dict(sweeps)[(k0,a0)][i]; y10=sweeps[(k1,a0)][i]; y01=sweeps[(k0,a1)][i]
            c1=(y10-y00)//(k1-k0); c2=(y01-y00)//(a1-a0); c0=y00-c1*k0-c2*a0
            bad=[key for key in keys if sweeps[key][i]!=c0+c1*key[0]+c2*key[1]]
            if bad: aff_ok=False; print(f"    sweep {i}: NOT affine at {bad[:4]}")
            coefs.append((c0,c1,c2))
        print(f"  sweep lengths exactly affine in (k,a): {aff_ok}")
        print(f"    coefficients (c0+c1*k+c2*a): {coefs}")
        # (iii) episode landmark pinning
        ep_off={}
        for key in keys:
            k,a=key; r=data[key]
            lms=landmarks(k,g,a,r['endpos'])
            offs=[]
            for e in comps[key]:
                if e[0]=='E':
                    p=r['poss'][e[2]]
                    offs.append({name:p-v for name,v in lms.items()})
            ep_off[key]=offs
        n_ep=len(ep_off[keys[0]])
        unpinned=[]
        for i in range(n_ep):
            pinned=[]
            for name in landmarks(1,g,1,0):
                vals={ep_off[key][i][name] for key in keys}
                if len(vals)==1: pinned.append((name,vals.pop()))
            if not pinned: unpinned.append(i)
        print(f"  episode steps: {n_ep}; steps with NO invariant landmark offset: {len(unpinned)} {unpinned[:10]}")
        if unpinned:
            i=unpinned[0]
            print(f"    example episode {i}: offsets per (k,a): "
                  f"{[(key, ep_off[key][i]) for key in keys[:3]]}")
        else:
            print(f"  => every episode step is pinned to a structural landmark at a (k,a)-independent offset: LOCALITY DATA CLEAN")
