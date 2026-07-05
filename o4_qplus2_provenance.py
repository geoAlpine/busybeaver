# o4 q+2 provenance (2026-07-06) -- CORRECT transitions:
# A:0->1RB 1->0LD | B:0->1RC 1->1RF | C:0->1LA 1->0RA | D:0->0LA 1->0LE | E:0->1LD 1->1LA | F:0->0RB 1->HALT
#
# Seam-creating A: A reads 0 at q, tape[q+1]=1 (B will land on right-1 of an 11). Safe iff tape[q+2]=0.
# For each seam, find WHICH transition (state,read->write) LAST WROTE cell q+2, and its written value.
# Claim to test:
#   E-seam (pred E:1->1LA): q+2 last written by D:1->0LE (value 0) -> PROVEN safe, odometer-independent.
#   C-seam (pred C:1->0RA): q+2 last written by an alternating leftward sweep (value 0) -> contingent on (10)* alternation.
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
    last_writer=dict()   # cell -> (state,read,write) of last transition that wrote it
    # provenance histograms
    prov=defaultdict(Counter)   # pred_state -> Counter of (writer_state,writer_read,writer_write) for q+2
    unsafe=0
    for s in range(N):
        r=tape[pos]; a=M[(st,r)]
        if a is None: return dict(halt=True,step=s)
        if st=='A' and r==0 and tape.get(pos+1,0)==1:
            q2=pos+2
            wr=last_writer.get(q2,('init',None,tape.get(q2,0)))
            prov[prev_st][wr]+=1
            if tape.get(q2,0)==1: unsafe+=1
        w,d,ns=a
        # record write
        last_writer[pos]=(st,r,w)
        if w==0: tape.pop(pos,None)
        else: tape[pos]=w
        prev_st=st
        pos+=d; st=ns
    return dict(halt=False,step=N,prov={k:dict(v) for k,v in prov.items()},unsafe=unsafe)

if __name__=='__main__':
    r=run(50_000_000)
    print("halt:",r.get('halt'),"  UNSAFE(tape[q+2]=1):",r['unsafe'])
    for pred in sorted(r['prov']):
        print(f"\nSeam predecessor = {pred}:  last-writer of q+2 (writer_state, read, WROTE):")
        for wr,ct in sorted(r['prov'][pred].items(), key=lambda kv:-kv[1]):
            ws,wrd,wv=wr
            print(f"    {ws}: read {wrd} -> wrote {wv}    x{ct:,}")
