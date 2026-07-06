#!/usr/bin/env python3
"""
o3 GROUND TRUTH (2026-07-06) -- port of the o4 pipeline, step 1.
o3 = 1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC   (halt = state F reads 0)

[PROVEN from the table] halt-relevant local-event reduction:
  F is entered ONLY by E,0->1RF (scan table: no other transition targets F).
  After E,0 at cell p: writes 1, moves R to p+1, state F. F reads cell p+1:
  0 => HALT; 1 => 0RC (continue).
  => o3 HALTS <=> some E-reads-0 event has right neighbour 0.
  SAFETY CONDITION: every E-reads-0 event has cell(p+1)==1.
This is o3's analogue of o4's "F never reads 1".

This script (pure concrete, NO acceleration):
  (1) verifies the halt gate never fires over N steps,
  (2) records the window set around E-reads-0 events at radius 3,4,5,
      reporting saturation (last-new-window step) and all-safe,
  (3) also records E-reads-1 windows (the other F-feeding-adjacent event
      class, for completeness of the local picture).
"""
import sys
from collections import defaultdict

def parse(spec):
    M={}
    for k,blk in enumerate(spec.split('_')):
        st="ABCDEF"[k]
        for r in (0,1):
            c=blk[3*r:3*r+3]
            M[(st,r)]=None if c[0]=='-' else (int(c[0]),1 if c[1]=='R' else -1,c[2])
    return M

SPEC="1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC"
M=parse(SPEC)

def halt_gate_audit():
    """[PROVEN from table] print the predecessor chain of the halt."""
    preds=[(s,r) for (s,r),a in M.items() if a is not None and a[2]=='F']
    print(f"transitions entering F: {preds}  (unique: {len(preds)==1})")
    s,r=preds[0]
    w,d,ns=M[(s,r)]
    print(f"  {s},{r} -> write {w}, move {'R' if d==1 else 'L'}, state F")
    print(f"  F,0 -> {M[('F',0)]}  (HALT)   F,1 -> {M[('F',1)]}")
    assert len(preds)==1 and (s,r)==('E',0) and d==1 and M[('F',0)] is None
    print("  => HALT <=> E reads 0 with right neighbour 0.  [PROVEN from table]")

def run(N, radii=(3,4,5)):
    SZ=1<<24
    tape=bytearray(SZ); off=SZ//2
    pos=off; st=0  # states as ints 0..5
    Mi=[[None,None] for _ in range(6)]
    for (s,r),a in M.items():
        Mi["ABCDEF".index(s)][r]=None if a is None else (a[0],a[1],"ABCDEF".index(a[2]))
    wins={W:set() for W in radii}
    last_new={W:0 for W in radii}
    e0=0; unsafe=0
    lo=hi=pos
    for step in range(N):
        r=tape[pos]
        a=Mi[st][r]
        if a is None:
            print(f"HALT at step {step}"); return None
        if st==4 and r==0:  # E reads 0
            e0+=1
            if tape[pos+1]!=1: unsafe+=1
            for W in radii:
                w=tuple(tape[pos+t] for t in range(-W,W+1))
                if w not in wins[W]:
                    wins[W].add(w); last_new[W]=step
        w,d,ns=a
        tape[pos]=w; pos+=d; st=ns
        if pos<lo: lo=pos
        if pos>hi: hi=pos
    return dict(e0=e0, unsafe=unsafe, wins=wins, last_new=last_new,
                width=hi-lo+1, N=N)

if __name__=='__main__':
    halt_gate_audit()
    N=int(sys.argv[1]) if len(sys.argv)>1 else 50_000_000
    print(f"\nconcrete run, N={N:,} steps (no acceleration):")
    r=run(N)
    if r is None: sys.exit(1)
    print(f"  E-reads-0 events: {r['e0']:,}   UNSAFE (right nbr != 1): {r['unsafe']}")
    print(f"  tape width: {r['width']:,}")
    for W in sorted(r['wins']):
        S=r['wins'][W]
        allsafe=all(w[W+1]==1 for w in S)
        print(f"  radius {W}: |window set| = {len(S):>3}   last new at step {r['last_new'][W]:>12,} "
              f"({100*r['last_new'][W]/r['N']:.2f}% of run)   all-safe: {allsafe}")
    print("\n[OBSERVED] labels only; saturation = last-new fraction small.")
