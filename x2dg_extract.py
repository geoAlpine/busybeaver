#!/usr/bin/env python3
"""x2dg_extract.py -- extract exact Lean Cfgs for the STD descent tile and the
finalization, to build precise tail-parametric Lean lemma statements."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

def runs(bits):
    out=[];i=0
    while i<len(bits):
        b=bits[i];j=i
        while j<len(bits) and bits[j]==b:j+=1
        out.append((b,j-i));i=j
    return out

def sim_at(n):
    sim=build(2);sim.step()
    while sim.n<n:
        if not sim.step():break
    return sim

def show(sim,tag):
    print(f"  {tag}: st={sim.st} pos={sim.pos} h={sim.h}")
    print(f"       L(near,runs)={runs(sim.L[::-1])[:10]}")
    print(f"       R(from head,runs)={runs([sim.h]+sim.R[::-1])[:12]}")

# absolute window base:
BASE={5:13453,6:33830,7:114703}

print("=== STD tile: block 13 (a=5, relstep 935->974, 39 steps) ===")
show(sim_at(BASE[5]+935),"IN ")
show(sim_at(BASE[5]+974),"OUT")

print("\n=== STD tile: block 29-as-second (a=6, relstep 3911->3998, 87 steps) ===")
show(sim_at(BASE[6]+3911),"IN ")
show(sim_at(BASE[6]+3998),"OUT")

print("\n=== STD tile: block 5 (a=5, relstep 974->989, 15 steps) ===")
show(sim_at(BASE[5]+974),"IN ")
show(sim_at(BASE[5]+989),"OUT")

print("\n=== FINALIZATION (a=5, relstep 989->1089, 100 steps, register [1]->base) ===")
show(sim_at(BASE[5]+989),"IN ")
show(sim_at(BASE[5]+1089),"OUT")
print("\n=== FINALIZATION (a=6, relstep 4052->4152, 100 steps) ===")
show(sim_at(BASE[6]+4052),"IN ")
show(sim_at(BASE[6]+4152),"OUT")
