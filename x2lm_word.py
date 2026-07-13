#!/usr/bin/env python3
"""x2lm_word.py -- extract the register word at the first steady forward tile (pos 23)
and confirm the forward pass is (period-7 unit)^u ++ suffix, so the run induction is clean.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

def to_M3(g):
    s=build(g); s.step(); mc=0
    while True:
        if s.is_milestone():
            mc+=1
            if mc==2: return s
        if not s.step(): return s

for g in (2,4,6):
    s=to_M3(g)
    while not (s.st=='E' and s.h==0 and s.pos==23):
        if not s.step(): break
    # register nearest-first from head: head then reversed(R)
    right = [s.h] + s.R[::-1]
    print(f"\ng={g} (u={g-1}) register at pos23 head, first 40 cells (nearest-first incl head):")
    print("  ", right[:40])
    # left comb nearest-first
    left = s.L[::-1]
    print(f"  left comb (nearest-first), first 30: {left[:30]}")

# period-7 check: input ctx [1,0,1,0,0,1,0,0,0,0,0]; hypothesize register right of head =
# unit^u ++ tail. Determine unit by diffing g=4 and g=6 register words.
def reg_at23(g):
    s=to_M3(g)
    while not (s.st=='E' and s.h==0 and s.pos==23):
        if not s.step(): break
    return [s.h]+s.R[::-1]
r4=reg_at23(4); r6=reg_at23(6)
# find longest common prefix then the periodic insert
i=0
while i<len(r4) and i<len(r6) and r4[i]==r6[i]:
    i+=1
print(f"\ng4 vs g6 register: common prefix length {i}")
print(f"  g4[{i}:{i+20}] = {r4[i:i+20]}")
print(f"  g6[{i}:{i+20}] = {r6[i:i+20]}")
# g6 has 2 more units than g4; the extra 14 cells (2*7) should be an insert
print(f"  |r6|-|r4| (in the tail region) diff: g4 len {len(r4)}, g6 len {len(r6)}")
