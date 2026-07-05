# o4 SEAM predecessor analysis (2026-07-06)
# For every seam-creating A (A reads 0 at q, tape[q+1]==1 -> B lands on right-1 of an 11),
# record the PREDECESSOR transition (the state that moved the head into A at q).
# A is entered only by: C:1->1LA, D:0->0LA, E:1->1LA  (all move LEFT into q from q+1).
#   - D:0->0LA writes 0 at q+1 => tape[q+1]=0, cannot be a seam.
#   - E:1->1LA: E was at q+1 reading 1; E is entered ONLY by D:1->0LE (from q+2), which
#     WROTE 0 at q+2 => tape[q+2]=0 GUARANTEED => B safe.
#   - C:1->1LA: need to check tape[q+2].
# If every seam-creating A is entered from E, the safety proof CLOSES.
from collections import defaultdict, Counter

def parse(spec):
    M={}
    for k,blk in enumerate(spec.split('_')):
        st="ABCDEF"[k]
        for r in (0,1):
            c=blk[3*r:3*r+3]
            M[(st,r)]=None if c[0]=='-' else (int(c[0]),1 if c[1]=='R' else -1,c[2])
    return M
M=parse("1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---")

def run(N):
    tape=defaultdict(int); pos=0; st='A'
    prev_st=None
    seam_pred=Counter()          # predecessor state -> count (for seam-creating A)
    seam_pred_R2=Counter()       # (predecessor, tape[q+2]) -> count
    allA0_pred=Counter()         # predecessor of every A-reads-0 -> count
    c_seam_ctx=Counter()         # if predecessor is C, dump window
    for s in range(N):
        r=tape[pos]; a=M[(st,r)]
        if a is None:
            return dict(halt=True, step=s)
        if st=='A' and r==0:
            allA0_pred[prev_st]+=1
            if tape.get(pos+1,0)==1:     # seam-creating
                R2=tape.get(pos+2,0)
                seam_pred[prev_st]+=1
                seam_pred_R2[(prev_st,R2)]+=1
                if prev_st=='C':
                    w=''.join(str(tape.get(pos+o,0)) for o in range(-6,7))
                    c_seam_ctx[w]+=1
        w,d,ns=a
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        prev_st=st
        pos+=d; st=ns
    return dict(halt=False, step=N, seam_pred=dict(seam_pred),
               seam_pred_R2=dict(seam_pred_R2), allA0_pred=dict(allA0_pred),
               c_ctx=dict(c_seam_ctx))

if __name__=='__main__':
    r=run(50_000_000)
    print("halt:", r.get('halt'))
    print("\nPredecessor state of EVERY A-reads-0:", r['allA0_pred'])
    print("\nPredecessor state of SEAM-creating A (A reads0, tape[q+1]=1):")
    for k,ct in sorted(r['seam_pred'].items(), key=lambda kv:-kv[1]):
        print(f"   from {k}: x{ct:,}")
    print("\n(predecessor, tape[q+2]) for seam-creating A  [tape[q+2]=1 would be UNSAFE]:")
    for k,ct in sorted(r['seam_pred_R2'].items(), key=lambda kv:-kv[1]):
        pred,R2=k
        tag = "  *** UNSAFE (R2=1) ***" if R2==1 else ""
        print(f"   from {pred}, tape[q+2]={R2}: x{ct:,}{tag}")
    if r['c_ctx']:
        print("\nC-predecessor seam windows [-6..+6] (head=idx6):")
        for w,ct in sorted(r['c_ctx'].items(), key=lambda kv:-kv[1]):
            print(f"   {w}  x{ct:,}")
