#!/usr/bin/env python3
"""Deep probe of the g=3 rung-11/rung-12 region to locate the +80 precisely.
List ALL regenIn 11/12 and cascadeReg 11/12 occurrences in the g=3 phase."""
import x2t7_lib
x2t7_lib.SPAN = 1 << 18
x2t7_lib.ORIGIN = x2t7_lib.SPAN
from x2t7_lib import run, rle_right, ones_run_left

def exitSteps(k): return 2**(2*k-3) + k*2**(k-1) + 2**(k-2) + 2
def descCascade_blocks(d):
    out = [ (1 << (j + 2)) - 3 for j in range(d, 0, -1) ]; out.append(1); return out
def match_descCascade(rle, start, dmax=11):
    for d in range(dmax, 0, -1):
        want = descCascade_blocks(d); ok, i = True, start
        for bi, blen in enumerate(want):
            if i >= len(rle) or rle[i][0] != 1 or rle[i][1] != blen: ok=False; break
            i += 1
            if bi < len(want) - 1:
                if i >= len(rle) or rle[i][0] != 0 or rle[i][1] != 2: ok=False; break
                i += 1
        if ok: return d
    return None
def classify_full(pos, tape):
    rle = rle_right(tape, pos, limit=40000)
    if not rle: return None
    if rle[0] == (0, 1):
        d = match_descCascade(rle, 1)
        if d is not None:
            k = d + 4
            if ones_run_left(tape, pos) == (1 << k) - 3: return ("regenIn", k)
    if rle[0][0]==0 and rle[0][1]==3 and len(rle)>2 and rle[1][0]==1:
        blk = rle[1][1]; k=(blk+3).bit_length()-1
        if (1<<k)-3==blk and k>=4 and rle[2]==(0,2):
            d = match_descCascade(rle,3)
            if d is not None and d==k-3: return ("cascadeReg", k)
    return None

M6_3, M1_4 = 2852510, 11329301
hits11 = []; hits12 = []
def hook(step, st, pos, tape):
    if st != 4 or tape[pos] != 0: return
    if tape[pos+1] != 0: return
    b2 = tape[pos+2]
    if not (b2==1 or (b2==0 and tape[pos+3]==0 and tape[pos+4]==1)): return
    r = classify_full(pos, tape)
    if r is None: return
    kind, k = r
    if k == 11: hits11.append((step, kind))
    if k == 12: hits12.append((step, kind))
run(M1_4 + 5, hook=hook, hook_from=M6_3)

print("=== g=3 level-11 events ===")
for step, kind in hits11:
    print(f"  {kind:11s} @ {step}")
print("=== g=3 level-12 events ===")
for step, kind in hits12:
    print(f"  {kind:11s} @ {step}")

# principal rung 11: first regenIn 11
reg11 = [s for s,k in hits11 if k=="regenIn"]
casc11 = [s for s,k in hits11 if k=="cascadeReg"]
reg12 = [s for s,k in hits12 if k=="regenIn"]
casc12 = [s for s,k in hits12 if k=="cascadeReg"]
print("\nregenIn11 first =", reg11[0] if reg11 else None,
      " cascadeReg11 first =", casc11[0] if casc11 else None)
if reg11 and casc11:
    print("  exit span rung11 =", casc11[0]-reg11[0], " vs exitSteps(11)=", exitSteps(11),
          " diff=", (casc11[0]-reg11[0])-exitSteps(11))
print("regenIn12 first =", reg12[0] if reg12 else None,
      " cascadeReg12 first =", casc12[0] if casc12 else None)
if reg12 and casc12:
    print("  exit span rung12 =", casc12[0]-reg12[0], " vs exitSteps(12)=", exitSteps(12),
          " diff=", (casc12[0]-reg12[0])-exitSteps(12))
# gap(11) two ways
if casc11 and reg12:
    print("gap(11) = regenIn12 - cascadeReg11 =", reg12[0]-casc11[0], " law=", 4**11-3*2**11+7)
