#!/usr/bin/env python3
"""M4 control for lean/T7Tail.lean `tailLaw`: is its IN register the one the ORBIT presents?
Checks  left = 0 :: (1 0 1 0 1 0 0)^j ++ turnWord ++ endWord ++ 0^11  and  right[0:4] = 0000
at the tail odometer's entry, every measured generation, with j = g-1."""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, check_anchors
assert check_anchors(verbose=False), "instrument check failed"
turnWord=[1,0,1,0,1,1,1,1,1,1,1,1,1,0,0]; endWord=[1,0,1,0,1,0,1,0,1]
def predL(j): return [0]+([1,0,1,0,1,0,0]*j)+turnWord+endWord+[0]*11
PTS={732623:('g=1',0), 2851954:('g=2',1), 11329137:('g=3',2), 11329164:('g=3 mid',1),
     44986804:('g=4',3)}
snap={}
def hook(step,st,pos,tape,origin):
    if step in PTS: snap[step]=(st,pos-origin,bytes(tape[pos-70:pos]),tape[pos],bytes(tape[pos+1:pos+10]))
run(max(PTS)+1,hook=hook,hook_from=min(PTS))
allok=True
for s,(tag,j) in sorted(PTS.items()):
    st,pos,l,h,r=snap[s]
    left=list(l[::-1]); P=predL(j)
    ok = left[:len(P)]==P and list(r[:4])==[0,0,0,0] and st==E and h==0
    allok &= ok
    print(f"  {tag:<9} step={s:>9} j={j}  {'MATCH' if ok else '*** MISMATCH ***'}")
print("ALL MATCH" if allok else "FAILED")
