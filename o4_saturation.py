# o4 boundary-graph SATURATION + 11-avoidance safety experiment (2026-07-06)
# Reuses the validated sound accelerator idea from o4_accel_sound.py.
# Machine o4: 1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---
# Non-halt <=> F never reads 1 <=> every 1 that B reads has right-neighbour 0
#            <=> B never created on the LEFT 1 of an "11".
# Goal: run to large step budget, and
#   (1) record every B-reads-1 event and its right-neighbour (must all be 0 = SAFE),
#   (2) build the boundary-event context set at windows w=4,6,8 and watch it SATURATE,
#   (3) track the milestone odometer G-sequence and max G reached,
#   (4) test closure: does any boundary context ever produce an UNSAFE branch?
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

def run(N, W=4):
    tape=defaultdict(int); pos=0; st='A'
    bctx=set()                 # boundary contexts (state, window)
    b_reads1=0; unsafe=0       # B reads 1; of those, right-neighbour 1 (=would halt)
    unsafe_examples=[]
    # milestone detection: form 0^G (10)^a 1001 with head at left end.
    milestones=[]              # (step, G, a)
    def window(p):
        return tuple(tape.get(p+o,0) for o in range(-W,W+1))
    # boundary event = a micro-step that is NOT inside a uniform period-p sweep.
    # Detect sweeps exactly as the validated accelerator: at each step try p in (2,3,4)
    # to find a returning restoring cycle; steps not part of such a jump are "boundary".
    def micro():
        nonlocal pos,st,b_reads1,unsafe
        r=tape[pos]; a=M[(st,r)]
        if a is None: return None
        if st=='B' and r==1:
            b_reads1+=1
            if tape.get(pos+1,0)==1:
                nonlocal_unsafe()
        w,d,ns=a
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns
        return True
    def nonlocal_unsafe():
        nonlocal unsafe
        unsafe+=1
        if len(unsafe_examples)<5: unsafe_examples.append((pos,window(pos)))
    done=0
    while done<N:
        r=tape[pos]; a=M[(st,r)]
        if a is None: return dict(halt=True, step=done, pos=pos)
        # try sound p-cycle jump
        found=False
        for p in (2,3,4):
            if done+p>N: continue
            orig={}; pos0=pos; st0=st; ok=True
            for _ in range(p):
                rr=tape[pos]
                if pos not in orig: orig[pos]=rr
                aa=M[(st,rr)]
                if aa is None: ok=False; break
                w,d,ns=aa
                if w==0: tape.pop(pos,None)
                else: tape[pos]=w
                pos+=d; st=ns
            # revert
            for k2,v in orig.items():
                if v==0: tape.pop(k2,None)
                else: tape[k2]=v
            pos=pos0; st=st0
            if not ok: continue
            # re-simulate to get delta/state
            delta=0; sT=st0
            # recompute delta by simulating again quickly
            p2={}; ps=pos0; s2=st0
            for _ in range(p):
                rr=tape[ps];
                if ps not in p2: p2[ps]=rr
                aa=M[(s2,rr)]; w,d,ns=aa
                if w==0: tape.pop(ps,None)
                else: tape[ps]=w
                ps+=d; s2=ns
            for k2,v in p2.items():
                if v==0: tape.pop(k2,None)
                else: tape[k2]=v
            ps_end=ps; delta=ps-pos0
            cells_restored=all(tape.get(k2,0)==p2[k2] for k2 in p2)
            if s2==st0 and delta!=0 and cells_restored:
                pat={k2-pos0:p2[k2] for k2 in p2}
                cyc=0; maxc=(N-done)//p
                while cyc<maxc:
                    base=pos0+delta*(cyc+1)
                    if all(tape.get(base+off,0)==val for off,val in pat.items()):
                        cyc+=1
                    else: break
                if cyc>=1:
                    pos=pos0+delta*cyc; done+=p*cyc; found=True; break
        if found: continue
        # boundary event: record context then micro-step
        bctx.add((st, window(pos)))
        if micro() is None: return dict(halt=True, step=done, pos=pos)
        done+=1
    return dict(halt=False, step=done, b_reads1=b_reads1, unsafe=unsafe,
                unsafe_examples=unsafe_examples, n_bctx=len(bctx), bctx=bctx, pos=pos)

if __name__=='__main__':
    import sys
    for W in (4,6,8):
        print(f"--- window W={W} ---")
        prev=None
        for N in (10**5, 10**6, 5*10**6, 2*10**7):
            r=run(N,W)
            newctx = len(r['bctx'] - prev) if prev is not None else r['n_bctx']
            print(f"N={N:>9}: B-reads-1={r['b_reads1']:>8}  UNSAFE(right=1)={r['unsafe']}  "
                  f"#bctx={r['n_bctx']:>4}  new-since-prev={newctx}")
            prev=r['bctx']
        print()
