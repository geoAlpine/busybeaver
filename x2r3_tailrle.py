#!/usr/bin/env python3
"""tail structure: RLE of BOTH sides at every tail config, g=2 and g=4, aligned."""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, check_anchors
assert check_anchors(verbose=False)
G4=[44986775,44986804,44986831,44986858,44986885,44986920,44986926,44986932,44986938,44986944,44986995]
G2=[2851925,2851954,2851981,2852016,2852022,2852028,2852034,2852040,2852091]
PTS=set(G4)|set(G2); snap={}
def rl(bits):
    out=[];i=0
    while i<len(bits) and len(out)<14:
        b=bits[i];j=i
        while j<len(bits) and bits[j]==b: j+=1
        out.append(f"{b}^{j-i}"); i=j
    return ' '.join(out)
def hook(step,st,pos,tape,origin):
    if step in PTS: snap[step]=(st,pos-origin,bytes(tape[max(0,pos-120):pos]),bytes(tape[pos:pos+120]))
run(max(PTS)+1, hook=hook, hook_from=min(PTS))
for tag,steps in (("g=4",G4),("g=2",G2)):
    print(f"\n===== {tag} =====")
    prev=None
    for s in steps:
        st,pos,l,r=snap[s]
        gap=f"(+{s-prev})" if prev is not None else ""
        prev=s
        print(f"{s:>10} {gap:>6} {'ABCDEF'[st]} pos={pos:>5}")
        print(f"     L(head-adj first): {rl(l[::-1])}")
        print(f"     R(head first)    : {rl(r)}")
