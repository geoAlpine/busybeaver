#!/usr/bin/env python3
"""T7 RECON (2026-07-22): is the `⊕` in `h_doub = RegenLaw ∀k ⊕ (doubling assembly)` wirable?

The roadmap books T7 as RegenLaw ∀k ⊕ the Θ(2^{2K}) doubling-phase assembly, but §5g/§5h
reference no regenIn/cascadeReg/RegenLaw/exitSteps at all (measured 2026-07-22, source-level).
So the ⊕ is bookkeeping, not a demonstrated reduction.

DECISIVE QUESTION: does the REAL doubling-phase orbit M6(g) -> M1(g+1) pass through configs
of the shape `regenIn k` / `cascadeReg k`?  If YES, RegenLaw's transport covers a chunk of the
phase and T7 shrinks a lot.  If NO, T7 is fully independent of the crux closure.

Machine: x2 = 1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE  (blank tape)

INSTRUMENT CHECK (must pass before any verdict is trusted; this repo has a documented
broken-instrument incident, commit 6b6d739): the recorded milestones are
  M1(1) @ step 188 099   tape carries a block 1^503
  M1(2) @ step 732 733   tape carries a block 1^1021
  M1(3) @ step 2 852 091 tape carries a block 1^2039
and `lean/HInit.lean` proves `steps 188099 init = some c189` (state E).
"""
import sys

# ---------------------------------------------------------------- machine
# A:1RB0RE  B:1RC---  C:0LD1LE  D:0RE1LD  E:1RF0LC  F:0RA1RE
# entry [state][read] = (write, dir(+1=R,-1=L), next) ; None = HALT
A, B, C, D, E, F = 0, 1, 2, 3, 4, 5
TT = [
    [(1,  1, B), (0,  1, E)],   # A
    [(1,  1, C), None       ],   # B  <- the ONLY halt transition
    [(0, -1, D), (1, -1, E)],   # C   (1LE = write 1, move LEFT, -> E)
    [(0,  1, E), (1, -1, D)],   # D
    [(1,  1, F), (0, -1, C)],   # E
    [(0,  1, A), (1,  1, E)],   # F
]

SPAN = 1 << 14           # tape half-width (plenty: |tape| ~ 4*2^K, K<=11)
ORIGIN = SPAN


def run(nsteps, hook=None, hook_from=0):
    """Simulate from blank. hook(step, st, pos, tape) called on steps >= hook_from."""
    tape = bytearray(2 * SPAN)
    pos, st = ORIGIN, A
    for step in range(nsteps):
        e = TT[st][tape[pos]]
        if e is None:
            return step, st, pos, tape, True
        w, d, st = e
        tape[pos] = w
        pos += d
        if hook is not None and step + 1 >= hook_from:
            hook(step + 1, st, pos, tape)
    return nsteps, st, pos, tape, False


# ---------------------------------------------------------------- shape tools
def rle_right(tape, pos, limit=4000):
    """Run-length encoding of the tape strictly right of `pos`, as [(bit,len),...]."""
    out, i, n = [], pos + 1, 0
    end = min(pos + 1 + limit, 2 * SPAN)
    while i < end:
        b = tape[i]
        j = i
        while j < end and tape[j] == b:
            j += 1
        out.append((b, j - i))
        i = j
        n += 1
        if n > 200:
            break
    return out


def ones_run_left(tape, pos):
    """Length of the run of 1s immediately left of `pos` (0 if tape[pos-1] != 1)."""
    i, c = pos - 1, 0
    while i >= 0 and tape[i] == 1:
        c += 1
        i -= 1
    return c


def descCascade_blocks(d):
    """descCascade d as the list of 1-block lengths, left to right.
    descCascade 0 = [1];  descCascade (d+1) = 2^(d+3)-3 :: descCascade d."""
    out = []
    for j in range(d, 0, -1):
        out.append((1 << (j + 2)) - 3)
    out.append(1)
    return out


def match_descCascade(rle, start):
    """If rle[start:] begins with descCascade d (blocks of 1s separated by exactly '00'),
    return d, else None.  Requires d >= 1 to be a meaningful hit."""
    for d in range(8, 0, -1):
        want = descCascade_blocks(d)
        ok, i = True, start
        for bi, blen in enumerate(want):
            if i >= len(rle) or rle[i][0] != 1 or rle[i][1] != blen:
                ok = False
                break
            i += 1
            if bi < len(want) - 1:
                if i >= len(rle) or rle[i][0] != 0 or rle[i][1] != 2:
                    ok = False
                    break
                i += 1
        if ok:
            return d
    return None


# regenIn k : state E, head 0, LEFT starts ones(2^k-3); RIGHT = 0 :: descCascade(k-4) :: 0^z :: R
# cascadeReg k: state E, head 0, RIGHT = 0^3 :: ones(2^k-3) :: 0^2 :: descCascade(k-3) :: 0^2 :: 0^7 :: R
def classify(st, pos, tape):
    if st != E or tape[pos] != 0:
        return None
    rle = rle_right(tape, pos)
    if not rle:
        return None

    # --- regenIn k ---  right: a single 0 (the `false ::`), then descCascade (k-4)
    if rle[0][0] == 0 and rle[0][1] == 1:
        d = match_descCascade(rle, 1)
        if d is not None:
            k = d + 4
            if ones_run_left(tape, pos) == (1 << k) - 3:
                return ("regenIn", k)
    # regenIn with z>=1 absorbed: `false :: descCascade ...` needs exactly one 0 first;
    # when k-4 == 0 descCascade is [1] -- too weak a signature, skip (needs d>=1).

    # --- cascadeReg k --- right: 0^3, ones(2^k-3), 0^2, descCascade(k-3)
    if rle[0][0] == 0 and rle[0][1] == 3 and len(rle) > 2 and rle[1][0] == 1:
        blk = rle[1][1]
        k = (blk + 3).bit_length() - 1
        if (1 << k) - 3 == blk and k >= 4:
            if rle[2][0] == 0 and rle[2][1] == 2:
                d = match_descCascade(rle, 3)
                if d is not None and d == k - 3:
                    return ("cascadeReg", k)
    return None


