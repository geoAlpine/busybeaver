# o4 SOUND accelerate-then-concrete-probe (2026-07-06)
# Strategy that avoids the phase bug of the discarded o4_accel_windows.py:
#   (1) use the VALIDATED sound accelerator (o4_accel_sound.py logic) to advance to a large-G config,
#       jumping ONLY verified-uniform period-p cycles (cell-restoring + state-return + pattern-ahead);
#   (2) from that exact (state,pos,tape) run CONCRETE (no acceleration) for K steps, recording every
#       B-reads-1 window + right-neighbour. Window recording is thus 100% concrete => obviously sound.
# Validation: (A) accel(N) state/pos/tape == concrete(N); (B) accel-to-N + concrete-probe window-set
#   == pure-concrete window-set over the same region.
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

def accel_to(N):
    """Advance N steps by sound acceleration; return (state,pos,tape,leftmost)."""
    tape=defaultdict(int); pos=0; st='A'; done=0; leftmost=0
    while done<N:
        r=tape[pos]; a=M[(st,r)]
        if a is None: return ('HALT',pos,tape,leftmost,done)
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
            delta=pos-pos0
            cells_restored=all(tape.get(k2,0)==orig[k2] for k2 in orig)
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
                    if all(tape.get(base+off,0)==val for off,val in pat.items()): cyc+=1
                    else: break
                if cyc>=1:
                    pos=pos0+delta*cyc; done+=p*cyc; found=True
                    if pos<leftmost: leftmost=pos
                    break
        if found: continue
        # micro
        r=tape[pos]; a=M[(st,r)]
        if a is None: return ('HALT',pos,tape,leftmost,done)
        w,d,ns=a
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns; done+=1
        if pos<leftmost: leftmost=pos
    return (st,pos,tape,leftmost,done)

def concrete_probe(st,pos,tape,K,W=5,record=True):
    """Concrete (no accel) for K steps; record B-reads-1 windows. Returns (wins,unsafe,f1,halt,leftmost)."""
    tape=defaultdict(int,{k:v for k,v in tape.items() if v})
    wins=set(); unsafe=0; f1=0; leftmost=pos
    for _ in range(K):
        r=tape[pos]; a=M[(st,r)]
        if a is None: return dict(wins=wins,unsafe=unsafe,f1=f1,halt=True,leftmost=leftmost)
        if record and st=='B' and r==1:
            win=tuple(tape.get(pos+o,0) for o in range(-W,W+1))
            wins.add(win)
            if tape.get(pos+1,0)==1: unsafe+=1
        if record and st=='F' and r==1: f1+=1
        w,d,ns=a
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns
        if pos<leftmost: leftmost=pos
    return dict(wins=wins,unsafe=unsafe,f1=f1,halt=False,leftmost=leftmost)

def pure_concrete_wins(N0,N1,W=5):
    """Pure concrete: record B-reads-1 windows for steps in [N0,N1)."""
    tape=defaultdict(int); pos=0; st='A'; wins=set(); unsafe=0
    for s in range(N1):
        r=tape[pos]; a=M[(st,r)]
        if a is None: break
        if s>=N0 and st=='B' and r==1:
            win=tuple(tape.get(pos+o,0) for o in range(-W,W+1)); wins.add(win)
            if tape.get(pos+1,0)==1: unsafe+=1
        w,d,ns=a
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns
    return wins,unsafe

if __name__=='__main__':
    # VALIDATION A: accel(N) == concrete(N) up to N=10M (state,pos,tape)
    def concrete(N):
        tape=defaultdict(int); pos=0; st='A'
        for _ in range(N):
            r=tape[pos]; a=M[(st,r)]
            if a is None: return ('HALT',pos,tape)
            w,d,ns=a
            if w==0: tape.pop(pos,None)
            else: tape[pos]=w
            pos+=d; st=ns
        return (st,pos,tape)
    print("VALIDATION A (accel==concrete):")
    for N in (2_000_000, 10_000_000):
        ac=accel_to(N); co=concrete(N)
        ok=(ac[0],ac[1])==(co[0],co[1]) and dict(ac[2])==dict(co[2])
        print(f"  N={N:>10}: accel=({ac[0]},{ac[1]}) concrete=({co[0]},{co[1]}) tape-match={dict(ac[2])==dict(co[2])} OK={ok}")

    # VALIDATION B: accel-to-N + concrete-probe window-set == pure-concrete window-set over same region
    print("VALIDATION B (probe window-set == pure concrete window-set):")
    N=5_000_000; K=3_000_000
    st,pos,tape,lm,done=accel_to(N)
    pr=concrete_probe(st,pos,tape,K,5)
    # pure concrete needs step index of accel end == N (steps), then K more
    pc_wins,pc_unsafe=pure_concrete_wins(N, N+K, 5)
    print(f"  probe |S|={len(pr['wins'])} unsafe={pr['unsafe']}  pureconc |S|={len(pc_wins)} unsafe={pc_unsafe}")
    print(f"  SETS EQUAL: {pr['wins']==pc_wins}")
    if pr['wins']!=pc_wins:
        print("  probe-only:", pr['wins']-pc_wins)
        print("  pure-only :", pc_wins-pr['wins'])

    # Canonical saturated set at r=5 (from concrete 32M) for subset checking.
    canon,_=pure_concrete_wins(0, 32_000_000, 5)
    print(f"\nCanonical saturated B-reads-1 window set (r=5): |canon|={len(canon)}")

    # LARGE-G closure test: accelerate far, then concrete-probe >= a generation.
    print("LARGE-G SOUND closure test (accelerate, then concrete-probe 20M steps):")
    for N in (100_000_000, 1_000_000_000):
        st,pos,tape,lm,done=accel_to(N)
        if st=='HALT': print(f"  N={N}: HALT"); break
        pr=concrete_probe(st,pos,tape,20_000_000,5)
        Gproxy=-lm
        outside=pr['wins']-canon          # NEW windows never seen at small G (falsification if nonempty)
        bad=[w for w in pr['wins'] if w[6]==1]
        print(f"  accel N={N:>13} (G~{Gproxy:>9,}): probe|S|={len(pr['wins']):>3} unsafe={pr['unsafe']} "
              f"f1={pr['f1']} outside-canon={len(outside)} bad={len(bad)}  "
              f"CLOSED&SAFE={len(outside)==0 and pr['unsafe']==0 and pr['f1']==0}")
        if outside: print("    NEW windows outside canonical set:", outside)
