#!/usr/bin/env python3
"""R3: the descent-ENTRY configs, cell-exact, at g=2 / g=3 / g=4 — is the even family uniform?"""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, comb_left, check_anchors
assert check_anchors(verbose=False)
PTS = {734759:'g2 descIn 9', 2900995:'g3 descIn 9', 11336041:'g4 descIn 11'}
snap={}
def hook(step,st,pos,tape,origin):
    if step in PTS: snap[step]=(st,pos-origin,bytes(tape[max(0,pos-4000):pos]), bytes(tape[pos:pos+80]))
run(max(PTS)+1, hook=hook, hook_from=min(PTS))
for s in sorted(PTS):
    st,pos,l,r = snap[s]
    left = l[::-1]                      # head-adjacent first
    # count the leading (01) comb, then show the marker head
    i=n=0
    while i+1 < len(left) and left[i]==0 and left[i+1]==1:
        n+=1; i+=2
    print(f"\n{PTS[s]} step={s} pos={pos}")
    print(f"  left comb (01)^{n}, then marker head: {''.join(map(str,left[i:i+48]))}")
    print(f"  right(from head, 40): {''.join(map(str,r[:40]))}")
print("\n== marker-head comparison (the 40 cells after the comb) ==")
def mh(s):
    l=snap[s][2][::-1]; i=0
    while i+1<len(l) and l[i]==0 and l[i+1]==1: i+=2
    return ''.join(map(str,l[i:i+60]))
a,b,c = mh(734759), mh(2900995), mh(11336041)
print(f"  g2: {a}\n  g3: {b}\n  g4: {c}")
print(f"  g2==g4 ? {a==c}    g2==g3 ? {a==b}")
