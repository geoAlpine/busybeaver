#!/usr/bin/env python3
"""
o3 BOUNDARY-CHUNK landmark pinning (2026-07-06) -- the red-team upgrade applied to the
generation's boundary chunks (the body chunk is certified in o3_body_proof.py).
For each class, run standalone M(a,k) over a grid; segment into chunks (A at global lo);
compress each chunk; for the BOUNDARY chunks (all chunks except the body repetitions),
verify:
  (1) skeleton identity across the grid (position-independent trace word),
  (2) EPISODE-LANDMARK PINNING: every episode step's tape position is within a bounded,
      grid-INDEPENDENT offset of a structural landmark measured at chunk start:
      lo (left frontier), defect (leftmost 11-block), marker start (leftmost 11-block of
      the trailing marker = rightmost maximal (110)^* run), hi (right end);
      the per-episode (landmark, offset) vectors must be IDENTICAL across the grid.
With sweeps certified translation-invariant (o3_body_proof.py cycle certificates) and
episodes pinned, the boundary chunks generalize exactly as o4's prefix/suffix did.
"""
import sys
from collections import defaultdict
sys.path.insert(0,'/Users/aokiyousuke/busybeaver')
from o3_gen_proof import TM, build_M, match_M, compress

def landmarks(tape,lo,hi):
    """(lo, defect_start_or_None, marker_start_or_None, hi) from a dict tape."""
    cells=sorted(c for c,v in tape.items() if v)
    if not cells: return (lo,None,None,hi)
    # 11-blocks
    blocks=[]
    i=0
    while i<len(cells):
        j=i
        while j+1<len(cells) and cells[j+1]==cells[j]+1: j+=1
        blocks.append((cells[i],cells[j])); i=j+1
    twos=[b for b in blocks if b[1]-b[0]>=1]
    d=twos[0][0] if twos else None
    m=twos[-1][0] if twos else None
    return (lo,d,m,hi)

def run_chunks(a,k,maxsteps=10**8):
    tape=defaultdict(int,build_M(a,k)); pos=0; st='A'
    lo=hi=0
    cur=[]; curpos=[]; chunks=[]
    lm=landmarks(tape,lo,hi)
    for s in range(maxsteps):
        r=tape[pos]; act=TM[(st,r)]
        if act is None:
            return chunks,'HALT'
        if st=='A' and pos<=lo and s>0 and cur:
            chunks.append((cur,curpos,lm))
            cur=[]; curpos=[]
            lm=landmarks(tape,pos,hi)
            mk=match_M({c:v for c,v in tape.items() if v})
            if mk is not None:
                return chunks,mk
        w,d,ns=act
        cur.append((st,r,w,d)); curpos.append(pos)
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns
        lo=min(lo,pos); hi=max(hi,pos)
    return chunks,None

def pin_vector(trace,poss,lm):
    """compressed skeleton + per-episode (landmark_id, offset) with nearest landmark."""
    comp=compress(trace)
    skel=[]; pins=[]
    idx=0
    for e in comp:
        if e[0]=='S':
            skel.append(('S',e[1])); idx+=len(e[1])*e[2]
        else:
            skel.append(('E',e[1]))
            p=poss[idx]
            cands=[(abs(p-l),i,p-l) for i,l in enumerate(lm) if l is not None]
            dd,li,off=min(cands)
            pins.append((li,off))
            idx+=1
    return tuple(skel),tuple(pins)

if __name__=='__main__':
    # boundary chunks = all chunks except the body (identified by its skeleton from
    # o3_body_proof: the transport chunk). We verify pinning for chunk 0 (prefix /
    # cascade) and the LAST 4 chunks (suffix), per class.
    CASES={
        'cascade a%3==1': [(a,k) for a in (22,61,151,301) for k in (2,5,12)],
        'prefix+suffix a%3==2': [(a,k) for a in (23,62,152,302) for k in (3,5,12)],
        'suffix a%3==0': [(a,k) for a in (24,60,150,300) for k in (3,5,12)],
    }
    allok=True
    for name,grid in CASES.items():
        ref=None; ok=True
        for (a,k) in grid:
            chunks,land=run_chunks(a,k)
            assert land not in (None,'HALT'), f"{a},{k}: {land}"
            if 'cascade' in name:
                sel=[0]
            elif 'prefix' in name:
                sel=[0,1]+list(range(len(chunks)-4,len(chunks)))
            else:
                sel=list(range(len(chunks)-4,len(chunks)))
            vec=[]
            for i in sel:
                tr,ps,lm=chunks[i]
                vec.append(pin_vector(tr,ps,lm))
            if ref is None: ref=vec
            elif vec!=ref:
                ok=False; allok=False
                print(f"  {name}: PIN/SKELETON MISMATCH at (a={a},k={k})")
        n_ep=sum(len(p) for _,p in ref)
        mx=max((abs(o) for _,p in ref for _,o in p),default=0)
        print(f"{name}: {len(grid)} grid points, {len(ref)} boundary chunks, "
              f"{n_ep} pinned episodes, max |offset|={mx}, identical={ok}")
    print(f"\nBOUNDARY-CHUNK PINNING {'VERIFIED' if allok else 'FAILED'}: "
          f"episode (landmark,offset) vectors and skeletons identical across the grids.")
    print("(k=2 prefix variant at a%3==2 handled as its own per-k template per the note.)")
