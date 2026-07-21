#!/usr/bin/env python3
"""Measure the full g=4 ladder over the phase M6(4)->M1(5) = [11329720, 44986995].
Detect regenIn k / cascadeReg k for k=5..13. Deep rungs (k>=11) need a wide window,
so verification uses rle_right(limit=40000) and an extended descCascade matcher.
Cheap O(1) pre-filter gates the expensive verification."""
import x2t7_lib
x2t7_lib.SPAN = 1 << 18
x2t7_lib.ORIGIN = x2t7_lib.SPAN
from x2t7_lib import run, rle_right, ones_run_left, E

M6_4 = 11329720
M1_5 = 44986995

def descCascade_blocks(d):
    out = [ (1 << (j + 2)) - 3 for j in range(d, 0, -1) ]
    out.append(1)
    return out

def match_descCascade(rle, start, dmax=11):
    for d in range(dmax, 0, -1):
        want = descCascade_blocks(d)
        ok, i = True, start
        for bi, blen in enumerate(want):
            if i >= len(rle) or rle[i][0] != 1 or rle[i][1] != blen:
                ok = False; break
            i += 1
            if bi < len(want) - 1:
                if i >= len(rle) or rle[i][0] != 0 or rle[i][1] != 2:
                    ok = False; break
                i += 1
        if ok:
            return d
    return None

def classify_full(pos, tape):
    """like x2t7_lib.classify but wide window + extended descCascade."""
    rle = rle_right(tape, pos, limit=40000)
    if not rle:
        return None
    # regenIn k: right = single 0, then descCascade(k-4); left ones = 2^k-3
    if rle[0] == (0, 1):
        d = match_descCascade(rle, 1)
        if d is not None:
            k = d + 4
            if ones_run_left(tape, pos) == (1 << k) - 3:
                return ("regenIn", k)
    # cascadeReg k: right = 0^3, ones(2^k-3), 0^2, descCascade(k-3)
    if rle[0][0] == 0 and rle[0][1] == 3 and len(rle) > 2 and rle[1][0] == 1:
        blk = rle[1][1]
        k = (blk + 3).bit_length() - 1
        if (1 << k) - 3 == blk and k >= 4:
            if rle[2] == (0, 2):
                d = match_descCascade(rle, 3)
                if d is not None and d == k - 3:
                    return ("cascadeReg", k)
    return None

hits = []
def hook(step, st, pos, tape):
    if st != 4 or tape[pos] != 0:
        return
    # cheap O(1) pre-filter
    b1 = tape[pos+1]
    if b1 != 0:
        return
    b2 = tape[pos+2]
    regen_cand = (b2 == 1)
    casc_cand  = (b2 == 0 and tape[pos+3] == 0 and tape[pos+4] == 1)
    if not (regen_cand or casc_cand):
        return
    r = classify_full(pos, tape)
    if r is not None:
        hits.append((step, r[0], r[1]))

print("scanning phase [%d, %d] (%d steps)..." % (M6_4, M1_5, M1_5 - M6_4))
run(M1_5 + 5, hook=hook, hook_from=M6_4)
print("raw hits:", len(hits))
for h in hits:
    print("   step=%d %s k=%d" % h)

# dedupe/organize: first regenIn k and first cascadeReg k per level
import collections
firstseen = {}
for step, kind, k in hits:
    key = (kind, k)
    if key not in firstseen:
        firstseen[key] = step
print("\n=== FIRST occurrence per (kind,k) ===")
for key in sorted(firstseen, key=lambda x: (x[1], x[0])):
    print("   %-11s k=%2d  step=%d" % (key[0], key[1], firstseen[key]))
