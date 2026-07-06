# o4 C-seam detailed trace (2026-07-06)
# Dump the full micro-history and tape RLE around each C-entered seam (A reads0, tape[q+1]=1,
# predecessor = C:1->1LA). These occur at the 1001 cap. Goal: understand why tape[q+2]=0
# (i.e. C never stops at the left 1 of a pre-existing 11) and whether it's finitely bounded.
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

def snap(tape,pos,lo=-10,hi=10):
    return ''.join(('['+str(tape.get(pos+o,0))+']' if o==0 else str(tape.get(pos+o,0)))
                   for o in range(lo,hi+1))

def run(N, want=3):
    tape=defaultdict(int); pos=0; st='A'
    prev_st=None
    log=[]  # (step, st, r, pos, tape-snapshot-string)
    got=0
    for s in range(N):
        r=tape[pos]; a=M[(st,r)]
        if a is None:
            return
        if st=='A' and r==0 and tape.get(pos+1,0)==1 and prev_st=='C':
            got+=1
            print(f"\n=== C-SEAM #{got} at step {s}, head q={pos}  (tape[q+1]=1, tape[q+2]={tape.get(pos+2,0)}) ===")
            print("  window[q-10..q+10]:", snap(tape,pos))
            print("  last 25 microsteps (step: state read @pos  ->  snapshot[head-8..head+8]):")
            for (hs2,hst,hr,hp) in log[-25:]:
                print(f"    {hs2:>9}: {hst} r{hr} @{hp}")
            if got>=want:
                return
        w,d,ns=a
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        log.append((s,st,r,pos))
        if len(log)>60: log.pop(0)
        prev_st=st
        pos+=d; st=ns

if __name__=='__main__':
    run(2_000_000, want=3)
