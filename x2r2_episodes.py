#!/usr/bin/env python3
"""R2 (2026-07-23): cell-exact extraction of the TWO FIXED EPISODES of the doubling phase.

  regenEntry : descIn 5        -> regenIn 5      (~615 steps, claimed level-free)
  tail(g)    : cascadeReg(g+9) -> M1(g+1)        (claimed 211 / 184 / 265 at g=2/3/4)

METHODS M1 (instrument check) runs FIRST and gates everything: the recorded anchors are
  M1(1) @ 188 099, M1(2) @ 732 733, M1(3) @ 2 852 091   (h_low g=2 costs 343: M6(2)=733 076)
If any anchor misses, the script refuses to report episode data.

METHODS M0 (measure first): this script MEASURES; it asserts nothing about the proof shape.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2t7_lib import run, classify, E, SPAN, ORIGIN, rle_right, ones_run_left

ANCHORS = {1: 188099, 2: 732733, 3: 2852091}


def is_M1_like(st, pos, tape):
    """E, head on 0, and no 1 anywhere to the left -- the milestone signature (x2bd_sim.is_milestone)."""
    if st != E or tape[pos] != 0:
        return False
    return 1 not in tape[:pos]


def descIn_level(st, pos, tape):
    """descIn k = <E, ., <pow01(2^{k-1}) ++ M, false, false :: ones(2^k-3) ++ 0 0 descCascade(k-2) ++ T>>.
    Detect by the RIGHT signature 0 , 1^{2^k-3} , 0^2 and confirm the left comb (01)^{2^{k-1}}."""
    if st != E or tape[pos] != 0:
        return None
    if tape[pos + 1] != 0 or tape[pos + 2] != 1:
        return None
    r = rle_right(tape, pos, limit=6000)
    if len(r) < 3 or r[0] != (0, 1) or r[1][0] != 1 or r[2][0] != 0 or r[2][1] != 2:
        return None
    blk = r[1][1]
    k = (blk + 3).bit_length() - 1
    if (1 << k) - 3 != blk or k < 5:
        return None
    # left comb (01)^{2^{k-1}}: reading leftwards from pos-1 must be 0,1,0,1,...
    want = 1 << (k - 1)
    i, pairs = pos - 1, 0
    while pairs < want and i - 1 >= 0 and tape[i] == 0 and tape[i - 1] == 1:
        pairs += 1
        i -= 2
    if pairs < want:
        return ('descIn?', k, pairs, want)      # right matches, comb short -- report honestly
    return ('descIn', k, pairs, want)


def window(tape, pos, back, fwd):
    lo, hi = max(0, pos - back), min(2 * SPAN, pos + fwd + 1)
    return ''.join(str(tape[i]) for i in range(lo, hi)), pos - lo


def rle_str(r, n=14):
    return ' '.join(f"{b}^{l}" for b, l in r[:n])


def main():
    LIMIT = 2_900_000
    hits = {}          # step -> label
    milestones = []
    snapshots = {}     # step -> (st, pos, bytes(tape))
    WANT_SNAP = set()

    def hook(step, st, pos, tape):
        if st != E or tape[pos] != 0:
            return
        d = descIn_level(st, pos, tape)
        if d is not None:
            hits[step] = d
        c = classify(st, pos, tape)
        if c is not None:
            hits[step] = c
        if step in WANT_SNAP:
            snapshots[step] = (st, pos, bytes(tape))

    # ---- pass 1: milestones only (cheap check of the anchors) ----
    ms = []

    def hook_ms(step, st, pos, tape):
        if st == E and tape[pos] == 0 and 1 not in tape[:pos]:
            ms.append(step)

    print("== METHODS M1 -- INSTRUMENT CHECK ==")
    run(LIMIT, hook=hook_ms)
    print(f"milestone-signature steps found: {ms[:8]}{' ...' if len(ms) > 8 else ''}")
    ok = all(a in ms for a in ANCHORS.values())
    for g, a in ANCHORS.items():
        print(f"  M1({g}) @ {a:>9}  {'HIT' if a in ms else '*** MISS ***'}")
    if not ok:
        print("\nINSTRUMENT CHECK FAILED -- refusing to report episode data (METHODS M1).")
        return 1
    print("instrument OK\n")

    # ---- pass 2: classify E-on-0 configs across the g=2 doubling phase ----
    M6_2 = ANCHORS[2] + 343          # h_low g=2 = 343 steps (hlow_g2)
    M1_3 = ANCHORS[3]
    print(f"== g=2 doubling phase: M6(2)@{M6_2} -> M1(3)@{M1_3}  ({M1_3 - M6_2} steps) ==")

    found = {}

    def hook2(step, st, pos, tape):
        if step < M6_2 or step > M1_3:
            return
        if st != E or tape[pos] != 0:
            return
        d = descIn_level(st, pos, tape)
        if d is not None and d[0] == 'descIn':
            found.setdefault(('descIn', d[1]), step)
        c = classify(st, pos, tape)
        if c is not None:
            found.setdefault(c, step)

    run(M1_3 + 1, hook=hook2, hook_from=M6_2)
    for key in sorted(found, key=lambda k: found[k]):
        print(f"  {found[key]:>9}  {key[0]} {key[1]}   (+{found[key] - M6_2} into the phase)")

    d5 = found.get(('descIn', 5))
    r5 = found.get(('regenIn', 5))
    print()
    if d5 and r5:
        print(f"** regenEntry measured: descIn 5 @{d5} -> regenIn 5 @{r5}  = {r5 - d5} steps **")
    else:
        print(f"** regenEntry NOT bracketed: descIn 5={d5}, regenIn 5={r5} **")

    creg = [(k, s) for (lbl, k), s in found.items() if lbl == 'cascadeReg']
    creg.sort(key=lambda t: t[1])
    if creg:
        ktop, stop_ = creg[-1]
        print(f"** tail(2) measured: cascadeReg {ktop} @{stop_} -> M1(3) @{M1_3} = {M1_3 - stop_} steps **")

    # ---- pass 3: cell-exact snapshots at the four episode endpoints ----
    ends = [s for s in (d5, r5, (creg[-1][1] if creg else None), M1_3) if s]
    WANT_SNAP.update(ends)
    snaps = {}

    def hook3(step, st, pos, tape):
        if step in WANT_SNAP:
            snaps[step] = (st, pos, bytes(tape))

    run(max(ends) + 1, hook=hook3, hook_from=min(ends))
    print("\n== cell-exact endpoints ==")
    for s in sorted(snaps):
        st, pos, tape = snaps[s]
        r = rle_right(tape, pos, limit=6000)
        lo = ones_run_left(tape, pos)
        print(f"\nstep {s}: state={'ABCDEF'[st]} pos={pos - ORIGIN} head={tape[pos]} ones-run-left={lo}")
        print(f"  right RLE: {rle_str(r)}")
        w, off = window(tape, pos, 40, 40)
        print(f"  window+-40 (head at ^): {w}")
        print(f"                          {' ' * off}^")
    return 0


if __name__ == '__main__':
    sys.exit(main())
