# o4 CONCRETE (no acceleration) direct safety measurement (2026-07-06)
# o4: 1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---
# Non-halt <=> F never reads 1 <=> every B-reads-1 has right-neighbour 0.
# Directly count B-reads-1, F-reads, and any UNSAFE (right-neighbour 1) event.
# Also record the DISTINCT local windows of B-reads-1 events (should be a small fixed set).
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

def run(N, W=3):
    tape=defaultdict(int); pos=0; st='A'
    b1=0; f1=0; unsafe=0
    b1_windows=defaultdict(int); f_windows=defaultdict(int)
    maxpos=0; minpos=0
    for s in range(N):
        r=tape[pos]; a=M[(st,r)]
        if a is None:
            return dict(halt=True, step=s, pos=pos)
        if st=='B' and r==1:
            b1+=1
            win=tuple(tape.get(pos+o,0) for o in range(-W,W+1))
            b1_windows[win]+=1
            if tape.get(pos+1,0)==1: unsafe+=1
        if st=='F':
            f1 += (1 if r==1 else 0)
            win=tuple(tape.get(pos+o,0) for o in range(-W,W+1))
            f_windows[win]+=1
        w,d,ns=a
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns
        if pos>maxpos: maxpos=pos
        if pos<minpos: minpos=pos
    return dict(halt=False, step=N, b1=b1, f1=f1, unsafe=unsafe,
               b1_windows=dict(b1_windows), f_windows=dict(f_windows),
               span=(minpos,maxpos))

if __name__=='__main__':
    r=run(20_000_000, W=3)
    print("halt:", r['halt'])
    print(f"B-reads-1 events: {r['b1']:,}")
    print(f"F-reads total   : {sum(r['f_windows'].values()):,}")
    print(f"F-reads-1 (HALT if >0): {r['f1']}")
    print(f"UNSAFE B-reads-1 (right-neighbour=1): {r['unsafe']}")
    print(f"tape span: {r['span']}")
    print("\nDistinct B-reads-1 local windows (-3..+3), count:")
    for win,ct in sorted(r['b1_windows'].items(), key=lambda kv:-kv[1]):
        mark = "  <-- UNSAFE" if win[4]==1 else ""   # offset +1 is index 4 in -3..+3
        print(f"  {win}  x{ct:,}{mark}")
    print("\nDistinct F-read local windows (-3..+3), count:")
    for win,ct in sorted(r['f_windows'].items(), key=lambda kv:-kv[1]):
        mark = "  <-- F READS 1 = HALT" if win[3]==1 else ""  # head is index 3
        print(f"  {win}  x{ct:,}{mark}")
