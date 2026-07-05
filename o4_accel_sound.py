# Turn 2: period-p SOUND acceleration (p up to 4). Detect a p-cycle that returns to the start state after p
# steps, advanced by delta, having written all crossed cells back UNCHANGED, with the next delta cells
# matching the same pattern -> jump whole cycles. VALIDATE by exact-step comparison to concrete.
def parse(spec):
    M={}
    for k,blk in enumerate(spec.split('_')):
        st="ABCDEF"[k]
        for r in (0,1):
            c=blk[3*r:3*r+3]
            M[(st,r)]=None if c[0]=='-' else (int(c[0]),1 if c[1]=='R' else -1,c[2])
    return M
M=parse("1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---")
from collections import defaultdict
def mk():
    return defaultdict(int)
def concrete(N):
    tape=mk(); pos=0; st='A'
    for s in range(N):
        r=tape[pos]; a=M[(st,r)]
        if a is None: return ('HALT',s,pos,tape)
        w,d,ns=a
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns
    return (st,N,pos,tape)

def accel(N, jumps_stat=None):
    tape=mk(); pos=0; st='A'; done=0
    def micro():
        nonlocal pos,st,done
        r=tape[pos]; a=M[(st,r)]
        if a is None: return None
        w,d,ns=a
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns; done+=1
        return True
    while done<N:
        r=tape[pos]; a=M[(st,r)]
        if a is None: return ('HALT',done,pos,tape)
        # try to detect a p-cycle by simulating p steps from a SNAPSHOT and checking cell restoration + state return
        found=False
        for p in (2,3,4):
            if done+p>N: continue
            # snapshot cells that will be touched: simulate p steps on a copy of the local region
            # We simulate p micro-steps but remember original values to test 'written back unchanged'
            orig={}; pos0=pos; st0=st
            touched=[]
            ok=True
            for _ in range(p):
                rr=tape[pos]
                if pos not in orig: orig[pos]=rr
                aa=M[(st,rr)]
                if aa is None: ok=False; break
                w,d,ns=aa
                if w==0: tape.pop(pos,None)
                else: tape[pos]=w
                pos+=d; st=ns
            if not ok:
                # revert
                for k2,v in orig.items():
                    if v==0: tape.pop(k2,None)
                    else: tape[k2]=v
                pos=pos0; st=st0; continue
            delta=pos-pos0
            cells_restored=all(tape.get(k2,0)==orig[k2] for k2 in orig)
            if st==st0 and delta!=0 and cells_restored:
                # this p-cycle is a candidate uniform sweep. revert, then jump full cycles while next-delta cells match.
                for k2,v in orig.items():
                    if v==0: tape.pop(k2,None)
                    else: tape[k2]=v
                pos=pos0; st=st0
                # pattern that the cycle expects at offsets: orig relative to pos0
                pat={k2-pos0:orig[k2] for k2 in orig}
                # count max cycles: keep jumping while the delta-shifted cells match pattern (sound: identical work)
                cyc=0; maxc=(N-done)//p
                while cyc<maxc:
                    base=pos0+delta*(cyc+1)
                    if all(tape.get(base+off,0)==val for off,val in pat.items()):
                        cyc+=1
                    else: break
                if cyc>=1:
                    # apply cyc cycles by SIMULATION (sound, no shortcut math) but that's O(cyc*p)... 
                    # instead: since verified identical, advance pos/done directly and leave tape unchanged (cells restored each cycle)
                    pos=pos0+delta*cyc; done+=p*cyc
                    if jumps_stat is not None: jumps_stat[0]+=1; jumps_stat[1]+=p*cyc
                    found=True
                    break
            else:
                for k2,v in orig.items():
                    if v==0: tape.pop(k2,None)
                    else: tape[k2]=v
                pos=pos0; st=st0
        if found: continue
        if micro() is None: return ('HALT',done,pos,tape)
    return (st,done,pos,tape)

allok=True
for N in (5000,50000,300000,2000000):
    c=concrete(N); js=[0,0]; ac=accel(N,js)
    ok=(c[0],c[1],c[2])==(ac[0],ac[1],ac[2]) and dict(c[3])==dict(ac[3])
    allok=allok and ok
    print(f"N={N}: concrete=({c[0]},{c[1]},{c[2]}) accel=({ac[0]},{ac[1]},{ac[2]}) tape-match={dict(c[3])==dict(ac[3])} MATCH={ok} jumps={js[0]} steps-jumped={js[1]}")
print("VALIDATED SOUND + accelerates" if allok else "MISMATCH -- NOT sound")
