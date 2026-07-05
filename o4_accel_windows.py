# *** UNSOUND -- DISCARDED (2026-07-06). DO NOT USE. ***
# Validation against concrete simulation FAILED: 9 windows missing at r=5 (phase bug --
# B-reads-1 events inside jumped sweeps are recorded at the wrong phase near block edges).
# Kept only as a record of the failure mode. See O4_WINDOW_SATURATION_2026-07-06.md "Soundness note".
#
# o4 accelerator that tracks B-reads-1 windows across jumps (ORIGINAL, OVERCLAIMED header below)
# Builds on the VALIDATED o4_accel_sound.py: a jumped p-cycle restores all cells and
# returns to the same state, so it is UNIFORM -> every B-reads-1 inside its `cyc` repeats
# shares the representative cycle's window. Recording the representative once (x cyc) is SOUND.
# This lets us reach G ~ 10^7 and test window-set closure far beyond concrete sim.
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

def run(N, W=5):
    tape=defaultdict(int); pos=0; st='A'
    wins=defaultdict(int); unsafe=0; halt=False
    leftmost=0
    def win_at(p):
        return tuple(tape.get(p+o,0) for o in range(-W,W+1))
    def record_B_reads_1():
        # call when about to execute (st='B', read=1)
        nonlocal unsafe
        w=win_at(pos); wins[w]+=1
        if tape.get(pos+1,0)==1: unsafe+=1
    done=0
    while done<N:
        r=tape[pos]; a=M[(st,r)]
        if a is None: return dict(halt=True, step=done)
        found=False
        for p in (2,3,4):
            if done+p>N: continue
            # simulate p steps recording original cells + any B-reads-1 windows in this cycle
            orig={}; pos0=pos; st0=st; ok=True
            cyc_b1=[]  # (relative offset structure) B-reads-1 events within one representative cycle
            for _ in range(p):
                rr=tape[pos]
                if pos not in orig: orig[pos]=rr
                if st=='B' and rr==1:
                    cyc_b1.append((win_at(pos), tape.get(pos+1,0)))
                aa=M[(st,rr)]
                if aa is None: ok=False; break
                w,d,ns=aa
                if w==0: tape.pop(pos,None)
                else: tape[pos]=w
                pos+=d; st=ns
            delta=pos-pos0
            cells_restored=all(tape.get(k2,0)==orig[k2] for k2 in orig)
            # revert
            for k2,v in orig.items():
                if v==0: tape.pop(k2,None)
                else: tape[k2]=v
            pos=pos0; st=st0
            if not ok: continue
            if st==st0 and delta!=0 and cells_restored:
                pat={k2-pos0:orig[k2] for k2 in orig}
                cyc=0; maxc=(N-done)//p
                while cyc<maxc:
                    base=pos0+delta*(cyc+1)
                    if all(tape.get(base+off,0)==val for off,val in pat.items()):
                        cyc+=1
                    else: break
                if cyc>=1:
                    # SOUND: each of the cyc repetitions is identical uniform work.
                    # Record the representative cycle's B-reads-1 windows x cyc.
                    for (w,rn) in cyc_b1:
                        wins[w]+=cyc
                        if rn==1: unsafe+=cyc
                    pos=pos0+delta*cyc; done+=p*cyc; found=True
                    if pos<leftmost: leftmost=pos
                    break
        if found: continue
        # micro-step (boundary event)
        r=tape[pos]; a=M[(st,r)]
        if a is None: return dict(halt=True, step=done)
        if st=='B' and r==1: record_B_reads_1()
        w,d,ns=a
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns; done+=1
        if pos<leftmost: leftmost=pos
    return dict(halt=False, wins=dict(wins), unsafe=unsafe, leftmost=leftmost)

if __name__=='__main__':
    W=5
    print(f"SAFETY-SOUND accelerated window closure test, radius W={W}")
    prev=set()
    for N in (2_000_000, 20_000_000, 200_000_000, 1_000_000_000):
        r=run(N,W)
        if r['halt']:
            print(f"N={N}: HALT at step {r['step']}"); break
        cur=set(r['wins'].keys()); new=cur-prev
        bad=[w for w in cur if w[W+1]==1]
        print(f"N={N:>12}: |leftmost|~{-r['leftmost']:>9} (~G reached)  |S|={len(cur):>3}  new={len(new):>3}  UNSAFE={r['unsafe']}  bad={len(bad)}")
        prev=cur
