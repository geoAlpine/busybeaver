#!/usr/bin/env python3
"""R2 (2026-07-23): wide-tape simulator for the x2 machine, with EXPLICIT bounds checking.

x2t7_lib.run uses SPAN = 2^14 and silently relies on the tape never leaving it; past ~14M steps
it raises IndexError (measured), and a NEGATIVE excursion would silently wrap (Python negative
indexing) -- the documented instrument hazard in METHODS M1.  This module fixes both:
SPAN is a parameter and both ends are asserted every step.

METHODS M1: `check_anchors()` must pass before any result from this module is trusted.
"""
import sys

A, B, C, D, E, F = 0, 1, 2, 3, 4, 5
TT = [
    [(1,  1, B), (0,  1, E)],
    [(1,  1, C), None       ],
    [(0, -1, D), (1, -1, E)],
    [(0,  1, E), (1, -1, D)],
    [(1,  1, F), (0, -1, C)],
    [(0,  1, A), (1,  1, E)],
]

ANCHORS = {1: 188099, 2: 732733, 3: 2852091}


def run(nsteps, hook=None, hook_from=0, span=1 << 17):
    tape = bytearray(2 * span)
    origin = span
    pos, st = origin, A
    lo = hi = origin
    for step in range(nsteps):
        e = TT[st][tape[pos]]
        if e is None:
            return step, st, pos, tape, True, origin, (lo, hi)
        w, d, st = e
        tape[pos] = w
        pos += d
        if pos < 0 or pos >= 2 * span:
            raise RuntimeError(f"TAPE OVERFLOW at step {step+1}: pos={pos-origin} span={span}")
        if pos < lo:
            lo = pos
        elif pos > hi:
            hi = pos
        if hook is not None and step + 1 >= hook_from:
            hook(step + 1, st, pos, tape, origin)
    return nsteps, st, pos, tape, False, origin, (lo, hi)


def check_anchors(verbose=True):
    """METHODS M1: the recorded milestones must be reproduced exactly."""
    seen = []
    z40 = bytearray(40)

    def hook(step, st, pos, tape, origin):
        if st != E or tape[pos] != 0:
            return
        if tape[pos - 40:pos] == z40 and 1 not in tape[:pos]:
            seen.append(step)

    run(ANCHORS[3] + 1, hook=hook)
    ok = all(a in seen for a in ANCHORS.values())
    if verbose:
        for g, a in ANCHORS.items():
            print(f"  M1({g}) @ {a:>9}  {'HIT' if a in seen else '*** MISS ***'}")
        print(f"  instrument {'OK' if ok else 'FAILED'} (span-parameterised, bounds-checked)")
    return ok


def casc_blocks(d):
    return [(1 << (j + 2)) - 3 for j in range(d, 0, -1)] + [1]


def rle(tape, pos, maxruns=16):
    out, i, end = [], pos + 1, len(tape)
    while i < end and len(out) < maxruns:
        b = tape[i]
        j = i
        while j < end and tape[j] == b:
            j += 1
        out.append((b, j - i))
        i = j
    return out


def cascade_at(r, s, dmax=13):
    for d in range(dmax, 0, -1):
        want, ok, i = casc_blocks(d), True, s
        for bi, bl in enumerate(want):
            if i >= len(r) or r[i][0] != 1 or r[i][1] != bl:
                ok = False
                break
            i += 1
            if bi < len(want) - 1:
                if i >= len(r) or r[i] != (0, 2):
                    ok = False
                    break
                i += 1
        if ok:
            return d
    return None


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


def label(tape, pos, r=None):
    """FULL-signature label: descIn k / regenIn k / cascadeReg k, or None."""
    if r is None:
        r = rle(tape, pos)
    if len(r) >= 3 and r[0] == (0, 1) and r[1][0] == 1 and r[2] == (0, 2):
        blk = r[1][1]
        k = (blk + 3).bit_length() - 1
        if (1 << k) - 3 == blk and cascade_at(r, 3) == k - 2 and comb_left(tape, pos) >= (1 << (k - 1)):
            return f"descIn {k}"
    if len(r) >= 2 and r[0] == (0, 1):
        d = cascade_at(r, 1)
        if d is not None and ones_left(tape, pos) == (1 << (d + 4)) - 3:
            return f"regenIn {d + 4}"
    if len(r) >= 4 and r[0] == (0, 3) and r[1][0] == 1 and r[2] == (0, 2):
        blk = r[1][1]
        k = (blk + 3).bit_length() - 1
        if (1 << k) - 3 == blk and cascade_at(r, 3) == k - 3:
            return f"cascadeReg {k}"
    return None


if __name__ == '__main__':
    print("== METHODS M1 -- INSTRUMENT CHECK (wide tape) ==")
    sys.exit(0 if check_anchors() else 1)
