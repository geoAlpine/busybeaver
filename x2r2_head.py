#!/usr/bin/env python3
"""R2 (2026-07-23): DUMP every E-on-0 config across the g=2 HEAD window, with full RLE.

Written after my first R2 detector fired on a partial signature (leading block only, no
descCascade check) and produced rung costs 768/384/192/96 that contradict the recorded
9(2^{k-1}-1).  METHODS M1: when the instrument and the record disagree, DOUBT THE INSTRUMENT.
So: no detector at all here -- just dump the raw configs and let the shapes speak.

Window: M6(2) @ 733 076  ->  regenIn 5 @ 739 656 (the 6 580-step head, per the design doc).
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2t7_lib import run, E, SPAN, ORIGIN

LO, HI = 733076, 739700


def rle_right_big(tape, pos, limit=40000, maxruns=40):
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
    """number of (01) pairs immediately left of pos, reading leftwards: tape[pos-1]=0, tape[pos-2]=1,..."""
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


def descCascade_blocks(d):
    return [(1 << (j + 2)) - 3 for j in range(d, 0, -1)] + [1]


def cascade_after(r, start):
    """largest d such that r[start:] begins with descCascade d (1-blocks separated by 0^2)."""
    best = None
    for d in range(9, 0, -1):
        want, ok, i = descCascade_blocks(d), True, start
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
            best = d
            break
    return best


rows = []


def hook(step, st, pos, tape):
    if step < LO or step > HI:
        return
    if st != E or tape[pos] != 0:
        return
    r = rle_right_big(tape, pos)
    rows.append((step, pos - ORIGIN, comb_left(tape, pos), ones_left(tape, pos), r))


run(HI + 1, hook=hook, hook_from=LO)

print(f"E-on-0 configs in [{LO}, {HI}]: {len(rows)}\n")
prev = None
for step, pos, comb, onesl, r in rows:
    # descIn k signature: right = 0^1 , 1^{2^k-3} , 0^2 , descCascade(k-2) ...
    tag = ''
    if len(r) >= 3 and r[0] == (0, 1) and r[1][0] == 1 and r[2] == (0, 2):
        blk = r[1][1]
        k = (blk + 3).bit_length() - 1
        if (1 << k) - 3 == blk:
            d = cascade_after(r, 3)
            want_comb = 1 << (k - 1)
            tag = (f"  <<< blk=2^{k}-3 cascade={d} (descIn needs {k-2})"
                   f" comb={comb}/{want_comb}{' COMB-OK' if comb >= want_comb else ''}"
                   f"{'  ** descIn %d **' % k if d == k - 2 and comb >= want_comb else ''}")
    gap = f" (+{step - prev})" if prev is not None else ""
    prev = step
    body = ' '.join(f"{b}^{l}" for b, l in r[:12])
    print(f"{step:>7}{gap:>9} pos={pos:>6} comb_l={comb:<5} ones_l={onesl:<5} | {body}{tag}")
