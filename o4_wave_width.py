# o4 CASCADE-WIDTH / TRAVELING-WAVE experiment (2026-07-06)
# o4: 1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---
# Non-halt <=> every B-reads-1 has right-neighbour 0.
#
# GOAL: test the "bounded-cascade-width" lemma three ways:
#  (1) Does the FULL head-local window set (state, radius R) SATURATE as G grows to ~1e4?
#      -> bounded set  == bounded seam diversity  == the wave is a bounded-width object.
#  (2) Measure the "disturbance width": max contiguous non-alternating / non-uniform
#      region around the head, as a function of G.  Bounded? or Theta(G)?
#  (3) Deep-gap microstep trace for two different G: is the interior a FIXED periodic
#      pattern with a bounded seam, independent of G?
from collections import defaultdict

def parse(spec):
    M={}
    for k,blk in enumerate(spec.split('_')):
        st="ABCDEF"[k]
        for r in (0,1):
            c=blk[3*r:3*r+3]
            M[(st,r)]=None if c[0]=='-' else (int(c[0]),1 if c[1]=='R' else -1,c[2])
    return M
M=parse("1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---")

def step(tape,pos,st):
    r=tape[pos]; a=M[(st,r)]
    if a is None: return None
    w,d,ns=a
    if w==0: tape.pop(pos,None)
    else: tape[pos]=w
    return pos+d, ns, r

# ---------- (1) full head-window saturation vs G ----------
def window_saturation(N, R):
    tape=defaultdict(int); pos=0; st='A'
    seen=set(); maxpos=0; minpos=0
    checkpoints=[]; targets=[500,1000,2000,4000,6000]; ti=0
    for s in range(N):
        win=(st,)+tuple(tape.get(pos+o,0) for o in range(-R,R+1))
        seen.add(win)
        nx=step(tape,pos,st)
        if nx is None: return dict(halt=True,step=s)
        pos,st,_=nx
        if pos>maxpos: maxpos=pos
        if pos<minpos: minpos=pos
        G=maxpos-minpos
        if ti<len(targets) and G>=targets[ti]:
            checkpoints.append((targets[ti], s, len(seen)))
            ti+=1
    return dict(halt=False, seen=len(seen), gmax=maxpos-minpos, checkpoints=checkpoints)

# ---------- (2) disturbance width vs G ----------
# "clean" tape away from the head is: all-0 (gap) on the left of the head, and
# perfectly-alternating (10)* then cap on the right.  Define disturbance width as
# the size of the smallest interval [a,b] around the head outside which the tape is
# either constant-0 (on the deep-left side) or perfectly alternating (on the right side).
def disturbance_width_profile(N):
    tape=defaultdict(int); pos=0; st='A'
    widths=defaultdict(int)   # G-bucket -> max width seen
    maxpos=0; minpos=0
    sample_every=1
    for s in range(N):
        nx=step(tape,pos,st)
        if nx is None: return dict(halt=True,step=s)
        pos,st,_=nx
        if pos>maxpos: maxpos=pos
        if pos<minpos: minpos=pos
        if s % 4000 == 0 and s>0:
            # measure disturbance width around head
            ones=sorted(tape.keys())
            if not ones: continue
            lo=ones[0]; hi=ones[-1]
            # scan for the maximal run where pattern deviates from alternating,
            # measured as count of adjacent-equal pairs among 1-positions region.
            # Simpler robust proxy: number of positions p in [lo,hi] with tape[p]==tape[p+1]==1
            # (a "11") plus number of 0-gaps of length!=1 strictly inside [lo,hi] excluding the
            # single big gap.  This counts local defects of the alternating background.
            defects=0
            p=lo
            # find big gap = the longest 0-run; everything else should be unit gaps / unit blocks
            # compute run-length encoding of tape[lo..hi]
            rle=[]
            val=tape.get(lo,0); cnt=0
            for q in range(lo,hi+1):
                v=tape.get(q,0)
                if v==val: cnt+=1
                else: rle.append((val,cnt)); val=v; cnt=1
            rle.append((val,cnt))
            # ideal: alternating unit runs, with exactly one long 0-run (the gap) and the 1001 cap (0,2 gap).
            # disturbance width = total length of runs that are NOT unit, minus the single big gap.
            zero_runs=sorted([c for (v,c) in rle if v==0], reverse=True)
            biggap = zero_runs[0] if zero_runs else 0
            nonunit=0
            skipped_big=False
            for (v,c) in rle:
                if v==0 and c==biggap and not skipped_big:
                    skipped_big=True; continue
                if c!=1:
                    nonunit+=c
            G=maxpos-minpos
            bucket=(G//500)*500
            widths[bucket]=max(widths[bucket],nonunit)
    return dict(halt=False, widths=dict(widths), gmax=maxpos-minpos)

# ---------- (3) deep-gap microstep trace ----------
def deep_gap_trace(stop_G, span_probe=60):
    tape=defaultdict(int); pos=0; st='A'
    maxpos=0; minpos=0; s=0
    # run until gap ~ stop_G, then log a chunk of microsteps while head is deep-left
    while True:
        G=maxpos-minpos
        deep = (pos < minpos + 0.4*G) and (pos > minpos + 0.05*G) and G>stop_G
        nx=step(tape,pos,st)
        if nx is None: return dict(halt=True,step=s)
        pos,st,r=nx
        if pos>maxpos: maxpos=pos
        if pos<minpos: minpos=pos
        s+=1
        if G>stop_G and deep:
            # log the next span_probe microsteps
            trace=[]
            for _ in range(span_probe):
                rr=tape[pos]
                trace.append(f"{st}{rr}")
                nx=step(tape,pos,st)
                if nx is None: break
                pos,st,r=nx
            return dict(halt=False, G=G, trace=trace, pos=pos)
        if s>10**8: return dict(err="no deep gap")

if __name__=='__main__':
    print("=== (3) deep-gap microstep traces at two different G ===")
    for tg in (300, 1500):
        r=deep_gap_trace(tg)
        if r.get('trace'):
            print(f"G~{r['G']}: "+" ".join(r['trace']))
    print()

    print("=== (1) full head-window set saturation vs G  (col = |distinct (state,window)|) ===")
    for R in (6, 10, 14):
        r=window_saturation(6_000_000, R)
        cps=r.get('checkpoints',[])
        line=f"R={R:>2}: "+"  ".join(f"G>={g}:|W|={w}" for (g,_,w) in cps)
        print(line + f"   | final Gmax~{r['gmax']}, total distinct={r['seen']}")
    print()

    print("=== (2) disturbance (non-unit-run) width vs G bucket ===")
    r=disturbance_width_profile(6_000_000)
    for bucket in sorted(r['widths']):
        print(f"  G in [{bucket},{bucket+500}): max non-unit-run width = {r['widths'][bucket]}")
    print(f"  final Gmax~{r['gmax']}")
