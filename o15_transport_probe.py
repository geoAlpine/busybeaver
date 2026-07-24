#!/usr/bin/env python
"""
o15 OUTER-LAYER TRANSPARENCY PROBE  (2026-07-25)

Decides whether o15's OUTER collision structure (the 11-abutment halt) is decided by a
TRANSPARENT bounded/predictable-carry outer layer (x2-style, forall-transportable WITHOUT
base-8/3 normality) or whether it inherits the INNER Mahler (base-8/3, base-3 digit) opacity.

Raw TM  o15 = 1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA  (halt = state A reads 1).
Reuses the GUARDED generation runner run_gen from o15_template_scan.py (doc-verified == bb_sim).
"""
from __future__ import annotations
import math
from o15_template_scan import run_gen, parse as parse15, M as M15

O15 = "1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA"

# raw-TM planting simulator (dict tape) for the halt-mechanic control
def parse(spec):
    m = {}
    for i, g in enumerate(spec.split("_")):
        st = chr(ord("A") + i); m[st] = {}
        for s in (0, 1):
            w, mv, nx = g[s*3:s*3+3]
            m[st][s] = (int(w) if w in "01" else 0, mv, nx)
    return m
TBL = parse(O15)
HALT = {"Z", "H", "-"}

def run_from(tape, head, state, budget):
    tape = dict(tape); steps = 0
    while steps < budget:
        sym = tape.get(head, 0)
        w, mv, nx = TBL[state][sym]
        tape[head] = w
        head += 1 if mv == "R" else -1
        steps += 1
        if nx in HALT:
            return True, steps
        state = nx
    return False, steps

# ============================================================================
print("=" * 78)
print("PART A.  o15 HALT GATE  =  11-abutment at the F->A right handoff  (raw TM)")
print("=" * 78)
# A entered only by F:1->1RA (writes 1, moves R). A:1->HALT, A:0->1RB.
# So HALT <=> F reads a 1 whose RIGHT neighbour is 1.  Positive/negative controls:
# Plant state F reading a 1 with right-neighbour 1  vs  right-neighbour 0.
print("  Plant F on ...1[1]1... (right nb 1): expect HALT in ~1 step")
tape = {-1: 1, 0: 1, 1: 1}          # head at 0 reads 1, right neighbour (pos1) is 1
h, st = run_from(tape, 0, "F", 100)
print(f"    halted={h} steps={st}  {'OK' if h else 'FAIL'}")
print("  Plant F on ...1[1]0... (separator present): expect NO halt")
tape = {-1: 1, 0: 1, 1: 0}          # right neighbour 0
h, st = run_from(tape, 0, "F", 100)
print(f"    halted={h} steps={st}  {'OK' if not h else 'FAIL'}")

# ============================================================================
print("\n" + "=" * 78)
print("PART B.  o15 blank-orbit widths  (raw TM run_gen chained)  vs  W' = floor(8W/3)+2")
print("=" * 78)
# Start from the first milestone block-vector and chain generations.
blocks = [39]   # first clean single block on the blank orbit (W=40)
print(f"  gen  block-vector (head)                    W       floor(8W/3)+2  match?")
W = sum(blocks) + len(blocks) - 1
prev_pred = None
for g in range(6):
    status, land, steps, unsafe, mg, toks, bad0 = run_gen(blocks, budget=60_000_000)
    if status != 'LAND':
        print(f"    gen{g}: {status} steps={steps} unsafe={unsafe}")
        break
    Wl = sum(land) + len(land) - 1
    pred = math.floor(8 * W / 3) + 2
    disp = str(land) if len(land) < 6 else f"[{land[0]},{land[1]},..+{len(land)-2}]"
    print(f"    {g:2d}  {disp:38s} W={W:<6d}  pred={pred:<6d}  d={Wl-pred:+d} unsafe={unsafe}")
    blocks = land
    W = Wl

# ============================================================================
print("\n" + "=" * 78)
print("PART C.  *** THE TRANSPARENCY TEST ***  (o15_FIXEDPOINT_2026-07-07 §6)")
print("  Does the OUTER generation map depend only on a BOUNDED window of the block")
print("  string, or on the UNBOUNDED queue DEPTH?  Family [1]^k + [V]:")
print("=" * 78)
# [1]^k, V : run ONE generation, read landing, report V' and V' mod 3 as a function of k.
# If V' mod 3 has period 3 in k, then two configs agreeing on V and on ANY bounded queue
# window but differing in depth land in DIFFERENT branches -> no bounded-window transducer
# state -> NOT carry-transparent (unlike x2's register-driven odometer).
for V in (51, 300):
    print(f"\n  V={V}:  k = number of leading 1-digits")
    print("   k  landing block-vector                    V'=head block   V' mod 3")
    vmods = []
    for k in range(0, 10):
        blocks = [1] * k + [V]
        status, land, steps, unsafe, mg, toks, bad0 = run_gen(blocks)
        if status != 'LAND':
            print(f"   {k:2d}  {status}")
            continue
        Vp = land[-1]         # active (head) block after the generation
        vmods.append(Vp % 3)
        disp = str(land) if len(land) < 7 else f"[..{len(land)}bl..,{land[-1]}]"
        print(f"   {k:2d}  {disp:38s} {Vp:<14d} {Vp % 3}")
    # period detection in the V' mod 3 string
    per = None
    for p in range(1, 5):
        if len(vmods) >= 2*p and all(vmods[i] == vmods[i+p] for i in range(len(vmods)-p)):
            per = p; break
    print(f"    -> V' mod 3 over k = {vmods}   period = {per}")
    print(f"       {'DEPTH-DEPENDENT (period 3): outer map NOT bounded-window' if per==3 else 'check'}")

# ============================================================================
print("\n" + "=" * 78)
print("PART D.  ORDER-DEPENDENCE OF THE HALT  (o15_FIXEDPOINT §4): same multiset, opposite fate")
print("=" * 78)
# A bounded/commutative summary (multiset of digits) cannot decide the halt if two configs
# with the SAME multiset have opposite halting fate.  Test [1,2,1,2,1,1] vs [1,1,2,1,2,1] + V.
for V in (51, 52, 100):
    for buf in ([1,2,1,2,1,1], [1,1,2,1,2,1]):
        blocks = [2,2] + buf + [V]   # fatal-set prefix per O15_TEMPLATE_PORT (leading [2,2])
        status, land, steps, unsafe, mg, toks, bad0 = run_gen(blocks, budget=8_000_000)
        tag = 'HALT' if status == 'HALT' else ('LAND' if status=='LAND' else status)
        print(f"    V={V:3d} buf={buf} multiset={sorted(buf)} -> {tag} (steps={steps})")

print("\nDONE o15.")
