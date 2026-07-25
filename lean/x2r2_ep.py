#!/usr/bin/env python3
"""R2: cell-exact endpoints of the two FIXED episodes, at g=2 AND g=3, for diffing.
  E1 : descIn 3     -> cascadeReg 4   (200 steps, measured identical at g=2,3)
  E2 : cascadeReg 4 -> regenIn 5      (215 steps, measured identical at g=2,3)
"""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import run, E, rle, label, comb_left, ones_left, check_anchors
assert check_anchors(verbose=False)
PTS = {739241:'g2 descIn 3', 739441:'g2 cascadeReg 4', 739656:'g2 regenIn 5',
       2905477:'g3 descIn 3', 2905677:'g3 cascadeReg 4', 2905892:'g3 regenIn 5'}
snap={}
def hook(step,st,pos,tape,origin):
    if step in PTS: snap[step]=(st,pos,origin,bytes(tape[pos-64:pos+64]))
run(max(PTS)+1, hook=hook, hook_from=min(PTS))
for s in sorted(PTS):
    st,pos,origin,w = snap[s]
    left = w[:64][::-1]           # head-adjacent first, reading leftwards
    right = w[65:]                # strictly right, nearest first
    print(f"\n{PTS[s]}  step={s} pos={pos-origin} state={'ABCDEF'[st]} head={w[64]}")
    print(f"  left  (head-adjacent first, 64): {''.join(map(str,left))}")
    print(f"  right (nearest first, 63)      : {''.join(map(str,right))}")
print("\n== DIFF g2 vs g3 ==")
for a,b,name in ((739241,2905477,'descIn 3'),(739441,2905677,'cascadeReg 4'),(739656,2905892,'regenIn 5')):
    wa, wb = snap[a][3], snap[b][3]
    la = wa[:64][::-1]; lb = wb[:64][::-1]
    ra = wa[65:]; rb = wb[65:]
    pl = next((i for i in range(64) if la[i]!=lb[i]), None)
    pr = next((i for i in range(len(ra)) if ra[i]!=rb[i]), None)
    print(f"  {name:<14} left agrees for {pl if pl is not None else 64} cells; "
          f"right agrees for {pr if pr is not None else len(ra)} cells; "
          f"pos g2={snap[a][1]-snap[a][2]} g3={snap[b][1]-snap[b][2]}")
