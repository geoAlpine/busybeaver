#!/usr/bin/env python3
"""x2dg_boundary.py -- measure the TRUE per-depth tile costs inside descent(a).
For each descent, record the step (relative to window start) at which the machine is
E on a boundary 0 with the right register EXACTLY a descending cascade
  0^2 1^{2^d-3} 0^2 1^{2^{d-1}-3} 0^2 ... 0^2 1^1   (head on the leading 0)
i.e. the register has descended to depth d (top block consumed).  This reveals whether
descent(a) = TILE(a) then descent restricted to depth a-1 with matching step counts.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

DESC = {5: (13453, 14542), 6: (33830, 37982), 7: (114703, 131134)}

def cascade_blocks(reg_runs):
    """given run list of [h]+R, if it is 0^k 1^b1 0^2 1^b2 0^2 ... return [b1,b2,...] else None.
    tolerate trailing."""
    # expect leading zeros then alternating 1-block,0^2
    i = 0
    if not reg_runs or reg_runs[0][0] != 0: return None
    i = 1
    blocks = []
    while i < len(reg_runs):
        if reg_runs[i][0] != 1: break
        blocks.append(reg_runs[i][1])
        i += 1
        if i < len(reg_runs) and reg_runs[i][0] == 0:
            if reg_runs[i][1] == 2:
                i += 1; continue
            else:
                break
        else:
            break
    return blocks

def runs(bits):
    out = []; i = 0
    while i < len(bits):
        b = bits[i]; j = i
        while j < len(bits) and bits[j] == b: j += 1
        out.append((b, j - i)); i = j
    return out

def descent_boundaries(a):
    s, e = DESC[a]
    sim = build(2); sim.step()
    while sim.n < s:
        if not sim.step(): break
    n0 = sim.n
    seen = []
    while sim.n <= e:
        if sim.st == 'E' and sim.h == 0 and (1 not in sim.L):
            pass  # never (comb on left)
        # detect E on leading 0 of a clean descending cascade
        if sim.st == 'E' and sim.h == 0:
            rr = runs([sim.h] + sim.R[::-1])
            blocks = cascade_blocks(rr)
            if blocks and len(blocks) >= 1 and blocks[-1] == 1 and all(
                    blocks[k] == 2**(len(blocks)+1-k) - 3 for k in range(len(blocks))):
                seen.append((sim.n - n0, tuple(blocks)))
        if sim.n >= e: break
        if not sim.step(): break
    return seen

for a in (5, 6, 7):
    print(f"\n=== descent a={a} : clean descending-cascade E-boundary crossings (relstep, blocks) ===")
    b = descent_boundaries(a)
    # dedup consecutive
    prev = None
    for (rs, blk) in b:
        if blk != prev:
            print(f"   relstep {rs:6d}  blocks={list(blk)}  depth={len(blk)}")
            prev = blk
