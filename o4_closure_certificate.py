# o4 HEAD-WINDOW CLOSURE CERTIFICATE test (2026-07-06)  -- the decisive soundness test.
# o4: 1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---
#
# A head-window of radius R is (state, c_{-R},...,c_{R}) with head reading c_0.
# Collect the OBSERVED set W of head-windows from a long concrete run.
# Then test SOUND CLOSURE (an over-approximation valid for ALL tapes):
#   for every w in W and every possible value (0/1) of the single NEW cell that
#   enters at the far edge when the head moves, compute the successor head-window w'.
#   * if the move HALTS (F reads 1) -> would refute non-halt (should never happen from W).
#   * if w' NOT in W -> "escape": w needs non-local (counter) info to stay closed.
#   * if the step is B reading 1 with right-neighbour 1 -> "unsafe".
# If (escapes==0 AND unsafe==0 AND no halt) for some R, then W is a SOUND inductive
# certificate => o4 provably never halts.  Otherwise, the escaping windows pin EXACTLY
# where the counter (base-4/3 odometer) information is required.
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

def collect(N,R):
    tape=defaultdict(int); pos=0; st='A'
    W=set()
    for s in range(N):
        r=tape[pos]; a=M[(st,r)]
        if a is None: return None
        W.add((st,)+tuple(tape.get(pos+o,0) for o in range(-R,R+1)))
        w,d,ns=a
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns
    return W

def successor(w,R,incoming):
    # w=(st, c_{-R..R}); returns list of events for the microstep.
    st=w[0]; cells={o:w[1+i] for i,o in enumerate(range(-R,R+1))}
    r=cells[0]; a=M[(st,r)]
    if a is None: return ('HALT',None,False,False)
    wr,d,ns=a
    unsafe = (st=='B' and r==1 and cells.get(1,None)==1)
    bread1_rightunknown = (st=='B' and r==1 and (1 not in cells))  # can't happen, R>=1
    # write
    cells[0]=wr
    # shift to new head at offset d: new cell coords o' = o-d ; new window offsets -R..R
    newcells={}
    for o in range(-R,R+1):
        oldo=o+d
        if oldo in cells:
            newcells[o]=cells[oldo]
        else:
            # the single incoming cell at the far edge
            newcells[o]=incoming
    wp=(ns,)+tuple(newcells[o] for o in range(-R,R+1))
    return ('OK',wp,unsafe,bread1_rightunknown)

def test_closure(W,R):
    escapes=0; unsafe=0; halts=0; escape_ex=[]; unsafe_ex=[]
    for w in W:
        for incoming in (0,1):
            kind,wp,uns,_=successor(w,R,incoming)
            if kind=='HALT':
                halts+=1
                continue
            if uns:
                unsafe+=1
                if len(unsafe_ex)<6: unsafe_ex.append(w)
            if wp not in W:
                escapes+=1
                if len(escape_ex)<12: escape_ex.append((w,incoming,wp))
    return dict(escapes=escapes,unsafe=unsafe,halts=halts,
               escape_ex=escape_ex,unsafe_ex=unsafe_ex,size=len(W))

if __name__=='__main__':
    for R in (3,4,5,6,7):
        W=collect(3_000_000,R)
        res=test_closure(W,R)
        print(f"R={R}: |W|={res['size']:>5}  escapes={res['escapes']:>5}  "
              f"unsafe={res['unsafe']}  halts={res['halts']}  "
              f"=> {'SOUND CLOSURE (PROOF)' if res['escapes']==0 and res['unsafe']==0 and res['halts']==0 else 'NOT closed'}")
        if res['escapes'] and R==5:
            print("   sample escapes (window, incoming-bit, escaping successor):")
            for (w,inc,wp) in res['escape_ex'][:8]:
                print(f"     w={w}")
                print(f"       incoming={inc} -> w'={wp}")
