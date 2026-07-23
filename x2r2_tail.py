#!/usr/bin/env python3
"""R2 (2026-07-23): the TAIL episode (cascadeReg(g+9) -> M1(g+1)) and the g=3 regenEntry.

Single pass to ~2.87M steps with three windows:
  A. tail(2)      [2 851 000, 2 852 091]  -- dump E-on-0 configs, find cascadeReg 11
  B. g=3 head     [2 852 510, 2 861 000]  -- M6(3) = M1(3) + 419 (h_low odd: 305+38g)
                                             measure descIn rungs + regenEntry at g=3
Raw dumps, no narrow detector (METHODS M1: my first R2 detector was broken).
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2t7_lib import run, E, SPAN, ORIGIN

M1_3 = 2852091
M6_3 = M1_3 + 419
WA = (2851000, M1_3)
WB = (M6_3, M6_3 + 120000)


def rle(tape, pos, limit=60000, maxruns=40):
    out, i = [], pos + 1
    end = min(pos + 1 + limit, 2 * SPAN)
    while i < end and len(out) < maxruns:
        b = tape[i]
        j = i
        while j < end and tape[j] == b:
            j += 1
        out.append((b, j - i))
        i = j
    return out


def comb_left(tape, pos):
    i, n = pos - 1, 0
    while i - 1 >= 0 and tape[i] == 0 and tape[i - 1] == 1:
        n += 1
        i -= 2
    return n


def ones_left(tape, pos):
    i, c = pos - 1, 0
    while i >= 0 and tape[i] == 1:
        c += 1
        i -= 1
    return c


def casc(d):
    return [(1 << (j + 2)) - 3 for j in range(d, 0, -1)] + [1]


def cascade_at(r, start):
    for d in range(10, 0, -1):
        want, ok, i = casc(d), True, start
        for bi, bl in enumerate(want):
            if i >= len(r) or r[i][0] != 1 or r[i][1] != bl:
                ok = False
                break
            i += 1
            if bi < len(want) - 1:
                if i >= len(r) or r[i][0] != 0 or r[i][1] != 2:
                    ok = False
                    break
                i += 1
        if ok:
            return d
    return None


def label(r, comb, onesl):
    """descIn k / regenIn k / cascadeReg k, all with the FULL signature checked."""
    # descIn k : right = 0^1 1^{2^k-3} 0^2 descCascade(k-2)... ; left comb (01)^{2^{k-1}}
    if len(r) >= 3 and r[0] == (0, 1) and r[1][0] == 1 and r[2] == (0, 2):
        blk = r[1][1]
        k = (blk + 3).bit_length() - 1
        if (1 << k) - 3 == blk and cascade_at(r, 3) == k - 2 and comb >= (1 << (k - 1)):
            return f"descIn {k}"
    # regenIn k : right = 0^1 descCascade(k-4)... ; left ones(2^k-3)
    if len(r) >= 2 and r[0] == (0, 1):
        d = cascade_at(r, 1)
        if d is not None and onesl == (1 << (d + 4)) - 3:
            return f"regenIn {d + 4}"
    # cascadeReg k : right = 0^3 1^{2^k-3} 0^2 descCascade(k-3)...
    if len(r) >= 4 and r[0] == (0, 3) and r[1][0] == 1 and r[2] == (0, 2):
        blk = r[1][1]
        k = (blk + 3).bit_length() - 1
        if (1 << k) - 3 == blk and cascade_at(r, 3) == k - 3:
            return f"cascadeReg {k}"
    return None


rowsA, rowsB = [], []


def hook(step, st, pos, tape):
    if st != E or tape[pos] != 0:
        return
    if WA[0] <= step <= WA[1]:
        r = rle(tape, pos)
        rowsA.append((step, pos - ORIGIN, comb_left(tape, pos), ones_left(tape, pos), r))
    elif WB[0] <= step <= WB[1]:
        r = rle(tape, pos)
        lb = label(r, comb_left(tape, pos), ones_left(tape, pos))
        if lb:
            rowsB.append((step, pos - ORIGIN, lb, r))


run(WB[1] + 1, hook=hook, hook_from=WA[0])

print(f"== A. tail(2) window [{WA[0]}, {WA[1]}]:  {len(rowsA)} E-on-0 configs ==")
prev = None
for step, pos, comb, onesl, r in rowsA:
    lb = label(r, comb, onesl)
    gap = f"(+{step - prev})" if prev is not None else ""
    prev = step
    body = ' '.join(f"{b}^{l}" for b, l in r[:10])
    print(f"{step:>8} {gap:>7} pos={pos:>6} comb={comb:<4} ones_l={onesl:<5} | {body}"
          f"{'   <<< ' + lb if lb else ''}")

print(f"\n== B. g=3 head window [{WB[0]}, {WB[1]}] (M6(3) = M1(3)+419) ==")
prev = None
for step, pos, lb, r in rowsB:
    gap = f"(+{step - prev})" if prev is not None else ""
    prev = step
    body = ' '.join(f"{b}^{l}" for b, l in r[:10])
    print(f"{step:>8} {gap:>8} pos={pos:>6} {lb:<14} | {body}")
