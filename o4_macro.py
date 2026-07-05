# o4 run-length (RLE) macro-machine (2026-07-06)
# Tape as runs [sym,len]; implicit 0s beyond both ends. Head = (ri, off); state st.
# Sweep steps (write==read) never split runs; only genuine changes (0<->1) at seams do.
# Goal: faithful micro-sim on RLE (validated vs concrete), then O(1) jumps of uniform sweeps
#       to reach big-int G (steps ~ G^2 concretely => need macro jumps).
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

def normalize(runs, ri, off):
    """Merge adjacent equal-sym runs; drop zero-length; return (runs, ri, off) with head preserved."""
    # compute absolute offset of head from left edge of runs
    abshead = sum(runs[i][1] for i in range(ri)) + off
    # drop zero-length
    merged=[]
    for s,L in runs:
        if L<=0: continue
        if merged and merged[-1][0]==s: merged[-1][1]+=L
        else: merged.append([s,L])
    if not merged: merged=[[0,1]]
    # relocate head by abshead
    ri2=0; rem=abshead
    while ri2<len(merged) and rem>=merged[ri2][1]:
        rem-=merged[ri2][1]; ri2+=1
    if ri2>=len(merged): ri2=len(merged)-1; rem=merged[ri2][1]-1
    return merged, ri2, rem

class Cfg:
    __slots__=('runs','ri','off','st')
    def __init__(self,runs,ri,off,st):
        self.runs=runs; self.ri=ri; self.off=off; self.st=st

def start():
    return Cfg([[0,1]],0,0,'A')

def micro(cfg):
    """One faithful micro-step on RLE. Returns False if HALT, else True (cfg mutated)."""
    runs=cfg.runs; ri=cfg.ri; off=cfg.off; st=cfg.st
    sym=runs[ri][0]
    tr=M[(st,sym)]
    if tr is None: return False
    w,d,ns=tr
    # write
    if w!=sym:
        s,L=runs[ri]
        left=off; right=L-off-1
        newpieces=[]
        if left>0: newpieces.append([s,left])
        newpieces.append([w,1])
        if right>0: newpieces.append([s,right])
        runs[ri:ri+1]=newpieces
        # head now on the [w,1] piece
        ri = ri + (1 if left>0 else 0)
        off = 0
        runs,ri,off=normalize(runs,ri,off)
    # move
    if d==1:  # right
        off+=1
        if off>=runs[ri][1]:
            ri+=1; off=0
            if ri>=len(runs):
                # into implicit right 0s
                if runs[-1][0]==0: runs[-1][1]+=1; ri=len(runs)-1; off=runs[-1][1]-1
                else: runs.append([0,1]); ri=len(runs)-1; off=0
    else:  # left
        off-=1
        if off<0:
            ri-=1
            if ri<0:
                if runs[0][0]==0: runs[0][1]+=1; ri=0; off=0
                else: runs.insert(0,[0,1]); ri=0; off=0
            else:
                off=runs[ri][1]-1
    cfg.runs=runs; cfg.ri=ri; cfg.off=off; cfg.st=ns
    return True

def flatten(cfg):
    """Return (dict tape, abs head pos) with head-left-edge of runs[0] at coordinate 0."""
    tape={}; p=0
    for i,(s,L) in enumerate(cfg.runs):
        if s!=0:
            for j in range(L): tape[p+j]=s
        if i==cfg.ri: head=p+cfg.off
        p+=L
    return tape, head

# ---------- validation vs concrete ----------
def concrete_trace(N):
    tape=defaultdict(int); pos=0; st='A'; hist=[]
    for _ in range(N):
        r=tape[pos]; a=M[(st,r)]
        if a is None: return hist, True
        w,d,ns=a
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns
        hist.append((st,pos,dict(tape)))
    return hist, False

if __name__=='__main__':
    # VALIDATE: RLE micro-sim matches concrete step-for-step (state, head cell value, whole tape) for N steps.
    N=200000
    cfg=start()
    tape=defaultdict(int); pos=0; st='A'
    ok=True; firstbad=None
    for s in range(N):
        # concrete step
        r=tape[pos]; a=M[(st,r)]
        if a is None: break
        w,d,ns=a
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        pos+=d; st=ns
        # macro step
        alive=micro(cfg)
        if not alive:
            firstbad=('macro halted, concrete did not',s); ok=False; break
        # compare tapes RELATIVE TO HEAD (origins differ) + state
        mtape,mhead=flatten(cfg)
        mrel={k-mhead:v for k,v in mtape.items() if v}
        crel={k-pos:v for k,v in tape.items() if v}
        if cfg.st!=st or crel!=mrel:
            firstbad=(s, 'state',cfg.st,st,'tape-eq',crel==mrel,'crel',crel,'mrel',mrel); ok=False; break
    print(f"RLE micro-sim vs concrete over {N} steps: MATCH={ok}")
    if not ok: print("  first divergence:", firstbad)
    else: print(f"  final: state={cfg.st}, #runs={len(cfg.runs)}")
