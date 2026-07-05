# o4 SEAM-PARITY instrument (2026-07-06)
# o4: 1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---
#
# Non-halt <=> F never reads 1 <=> every B-reads-1 has tape[pos+1]=0
#          <=> B is NEVER created on the LEFT "1" of an "11".
#
# GOAL: isolate every "11" defect, record how state B interacts with it, and find the
# INVARIANT that forces B onto the RIGHT "1" (never the left).
#
# B is created ONLY by A:0->1RB or F:0->0RB (both step RIGHT from p-1 onto p).
# So for each B-reads-1 we log:
#   creator  : 'A' (wrote 1 at p-1) or 'F' (wrote 0 at p-1)
#   L=tape[p-1], H=tape[p]=1, R=tape[p+1], R2=tape[p+2]
#   side     : 'RIGHT-of-11' if L==1 (safe by construction), 'ISO/LEFT' if L==0
#   UNSAFE   : R==1  (B on LEFT of an 11 -> next step F reads 1 -> HALT)
# We also track the lifetime of every maximal 1-run of length>=2 (the "11" blocks):
#   when it is born (a step creates two adjacent 1s), and every head-visit to it.
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
    prev_st=None            # state that executed the previous transition (creator when it made B)
    b1=0; unsafe=0
    # classification of every B-reads-1
    cls=Counter()           # (creator, L, R, R2) -> count
    creator_of_B=None       # the state whose transition just created current-step's move-in
    # Track "11" births: a transition that writes a 1 at q while tape[q+-1]==1 creates an adjacent pair
    eleven_births=Counter() # (writer_state, side) -> count   side: pair formed to which direction
    # Track, whenever B reads a 1 that is the LEFT of an 11 (unsafe) OR right of an 11, the creator
    right_of_11_creator=Counter()
    left_of_11_creator=Counter()   # should stay empty
    # sample max run-of-1 length
    for s in range(N):
        r=tape[pos]; a=M[(st,r)]
        if a is None:
            return dict(halt=True, step=s, pos=pos)
        # ---- record B-reads-1 BEFORE mutating ----
        if st=='B' and r==1:
            b1+=1
            L=tape.get(pos-1,0); R=tape.get(pos+1,0); R2=tape.get(pos+2,0)
            cls[(prev_st,L,R,R2)]+=1
            if R==1: unsafe+=1
            if L==1:  # B sits on the right 1 of an 11
                right_of_11_creator[prev_st]+=1
            elif R==1:  # B sits on the left 1 of an 11 (UNSAFE)
                left_of_11_creator[prev_st]+=1
        # ---- detect 11-birth: this transition writes value w at pos ----
        w,d,ns=a
        if w==1:
            if tape.get(pos-1,0)==1: eleven_births[(st,'L')]+=1
            if tape.get(pos+1,0)==1: eleven_births[(st,'R')]+=1
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        prev_st=st
        pos+=d; st=ns
    return dict(halt=False, step=N, b1=b1, unsafe=unsafe,
               cls=dict(cls), right=dict(right_of_11_creator),
               left=dict(left_of_11_creator), births=dict(eleven_births))

if __name__=='__main__':
    r=run(30_000_000)
    print("halt:", r.get('halt'))
    print(f"B-reads-1 events : {r['b1']:,}")
    print(f"UNSAFE (R==1)    : {r['unsafe']}")
    print("\nB-reads-1 classified by (creator, L=tape[p-1], R=tape[p+1], R2=tape[p+2]):")
    for key,ct in sorted(r['cls'].items(), key=lambda kv:-kv[1]):
        cr,L,R,R2=key
        tag=""
        if L==1: tag="  RIGHT-of-11 (safe)"
        if R==1: tag="  *** UNSAFE: B on LEFT of 11 ***"
        print(f"  creator={cr}  L={L} H=1 R={R} R2={R2}  x{ct:,}{tag}")
    print("\nCreator of B when B is RIGHT-of-11 (L==1):", r['right'])
    print("Creator of B when B is LEFT-of-11 (UNSAFE):", r['left'])
    print("\n'11'-birth events (writer_state, side pair formed):", r['births'])
