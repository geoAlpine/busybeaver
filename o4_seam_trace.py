# o4 SEAM-CREATION trace (2026-07-06)
# The "11" seam is created ONLY by A:0->1RB (A writes 1 at p-1, B lands on pre-existing 1 at p).
# UNSAFE would require tape[p+1]=1 too (A steps onto the LEFT 1 of a pre-existing 11).
# INVARIANT TO PROVE:  when A reads 0 at q=p-1 and tape[q+1]==1, then tape[q+2]==0.
#
# Here we DUMP the exact local configuration at every seam-creating A:0->1RB, plus the
# short microstep history that placed A there, to expose the phase/parity invariant.
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

def win(tape,pos,lo=-6,hi=6):
    return ''.join(str(tape.get(pos+o,0)) for o in range(lo,hi+1))

def run(N, dump=40):
    tape=defaultdict(int); pos=0; st='A'
    hist=[]  # rolling (st,r,pos)
    seam_ctx=Counter()   # window at the A-step that creates a seam -> count
    a_reads0_onto1=Counter()  # (tape[q+1],tape[q+2]) distribution when A reads0 -> classifies
    dumped=0
    for s in range(N):
        r=tape[pos]; a=M[(st,r)]
        if a is None:
            return dict(halt=True, step=s)
        # A reads 0: about to create B at p=pos+1
        if st=='A' and r==0:
            R1=tape.get(pos+1,0); R2=tape.get(pos+2,0)
            a_reads0_onto1[(R1,R2)]+=1
            if R1==1:   # B will land on a 1 -> seam; safe iff R2==0
                w=win(tape,pos)
                seam_ctx[('A@'+w)]+=1
                if dumped<dump:
                    dumped+=1
                    print(f"step {s:>10}  SEAM create: A reads0 at pos, window[-6..+6]={w}  (R1={R1},R2={R2})")
                    print("      recent microsteps (state,read,pos):")
                    for (hs,hr,hp) in hist[-12:]:
                        print(f"         {hs} r{hr} @{hp}")
        w,d,ns=a
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        hist.append((st,r,pos))
        if len(hist)>40: hist.pop(0)
        pos+=d; st=ns
    return dict(halt=False, step=N, seam_ctx=dict(seam_ctx),
               a0=dict(a_reads0_onto1))

if __name__=='__main__':
    r=run(3_000_000, dump=6)
    print("\nhalt:", r.get('halt'))
    print("\nDistribution of (tape[q+1],tape[q+2]) when A reads 0 (q=head):")
    for key,ct in sorted(r['a0'].items(), key=lambda kv:-kv[1]):
        R1,R2=key
        tag=""
        if R1==1 and R2==0: tag="  seam (safe, B lands right-of-11)"
        if R1==1 and R2==1: tag="  *** UNSAFE would-be ***"
        print(f"  R1={R1} R2={R2}  x{ct:,}{tag}")
    print("\nDistinct seam-creation windows (A@ window[-6..+6], head at index 6):")
    for key,ct in sorted(r['seam_ctx'].items(), key=lambda kv:-kv[1]):
        print(f"  {key}  x{ct:,}")
