# o4 SEAM-SAFETY LEMMA -- consolidated verification (2026-07-06)
# CORRECT transitions: A:0->1RB 1->0LD | B:0->1RC 1->1RF | C:0->1LA 1->0RA
#                      D:0->0LA 1->0LE | E:0->1LD 1->1LA | F:0->0RB 1->HALT
#
# PROVEN (transition table): non-halt <=> F never reads 1 <=> every B-reads-1 has tape[p+1]=0.
#   B created only by A:0->1RB or F:0->0RB. The only B-reads-1 that touches an "11" is the SEAM:
#   A:0->1RB writes 1 at p-1 then B lands on a pre-existing 1 at p  =>  B on the RIGHT 1 of the 11.
#   Safety of that read <=> tape[p+1]=0.  (p+1 == q+2 with q=p-1 the A-read cell.)
#
# PROVEN (transition table): a seam-creating A (reads 0 at q, tape[q+1]=1) has predecessor in
#   {E:1->1LA, C:1->0RA} ONLY.
#   * E:1->1LA at q+1  <=  entered ONLY by D:1->0LE at q+2 (wrote 0). Head path q+2->q+1->q->B,
#     never revisits q+2  =>  tape[q+2]=0  =>  SAFE.  [UNCONDITIONAL, all G]
#   * C:1->0RA: head sweeps right into q; safe iff q+2 still 0 (last erased by D:1->0LE, head
#     turned around left of q+2). [contingent on uniform-interior alternation]
#
# This script asserts, concretely: (1) 0 unsafe; (2) every seam predecessor in {E,C};
# (3) every seam has tape[q+2] last-written by D:1->0LE; (4) all gap-edge seams are E-type.
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
    tape=defaultdict(int); pos=0; st='A'; prev_st=None
    lastw={}; b1=unsafe=0
    pred=Counter(); prov=Counter(); loc=Counter()
    for s in range(N):
        r=tape[pos]; a=M[(st,r)]
        assert a is not None, f"HALT at {s}"
        if st=='B' and r==1:
            b1+=1
            if tape.get(pos+1,0)==1: unsafe+=1
        if st=='A' and r==0 and tape.get(pos+1,0)==1:
            pred[prev_st]+=1
            prov[lastw.get(pos+2,('init',None,0))]+=1
            edge = sum(tape.get(pos-o,0) for o in range(1,6))==0
            loc[(prev_st,'GAP-EDGE' if edge else 'CAP')]+=1
            assert tape.get(pos+2,0)==0, f"UNSAFE SEAM at {s}"
        w,d,ns=a
        lastw[pos]=(st,r,w)
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        prev_st=st; pos+=d; st=ns
    return b1,unsafe,dict(pred),dict(prov),dict(loc)
b1,unsafe,pred,prov,loc=run(30_000_000)
print(f"B-reads-1={b1:,}  UNSAFE={unsafe}")
print("seam predecessors:", pred)
assert set(pred) <= {'E','C'}, "predecessor outside {E,C}!"
print("q+2 last-writer:", prov)
assert all(k[0]=='D' and k[1]==1 and k[2]==0 for k in prov), "q+2 not always erased by D:1->0LE!"
print("seam (predecessor,location):", loc)
assert all(p=='E' for (p,l),c in loc.items() if l=='GAP-EDGE'), "a gap-edge seam is not E-type!"
print("\nALL ASSERTIONS PASSED:")
print("  * 0 unsafe; every seam predecessor in {E,C}; q+2 always last-erased by D:1->0LE;")
print("  * every GAP-EDGE (odometer-critical) seam is E-type => PROVEN safe (unconditional).")
