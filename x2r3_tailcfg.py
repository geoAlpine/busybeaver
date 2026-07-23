#!/usr/bin/env python3
"""tail Lean-ification: cell-exact configs of the frameDigit stage and fixedEnd, at g=4
(3 stages -- the cleanest case) and g=2 (1 stage), for diffing."""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, check_anchors
assert check_anchors(verbose=False)
G4=[44986804,44986831,44986858,44986885,44986920,44986926,44986932,44986938,44986944,44986995]
G2=[2851954,2851981,2852016,2852022,2852028,2852034,2852040,2852091]
PTS=set(G4)|set(G2)
snap={}
def hook(step,st,pos,tape,origin):
    if step in PTS: snap[step]=(st,pos-origin,bytes(tape[max(0,pos-70):pos]),bytes(tape[pos:pos+70]))
run(max(PTS)+1, hook=hook, hook_from=min(PTS))
def show(tag,steps):
    print(f"\n===== {tag} =====")
    prev=None
    for s in steps:
        st,pos,l,r=snap[s]
        left=l[::-1]
        gap=f"(+{s-prev})" if prev is not None else ""
        prev=s
        print(f"{s:>10} {gap:>6} st={'ABCDEF'[st]} pos={pos:>5}")
        print(f"    L: {''.join(map(str,left[:56]))}")
        print(f"    R: {''.join(map(str,r[:56]))}")
show("g=4  (3 frameDigit stages then fixedEnd)",G4)
show("g=2  (1 frameDigit stage then fixedEnd)",G2)
print("\n===== fixedEnd alignment: g=4 last 6 vs g=2 last 6 =====")
for a,b in zip(G4[4:],G2[2:]):
    la,ra=snap[a][2][::-1],snap[a][3]; lb,rb=snap[b][2][::-1],snap[b][3]
    nl=next((i for i in range(56) if la[i]!=lb[i]),56)
    nr=next((i for i in range(56) if ra[i]!=rb[i]),56)
    print(f"  {a} vs {b}: left agrees {nl}/56, right agrees {nr}/56, pos {snap[a][1]} / {snap[b][1]}")
