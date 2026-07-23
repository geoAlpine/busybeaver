#!/usr/bin/env python3
"""R3 + tail (2026-07-23): measure the two remaining transports of the doubling phase.

  A. topEntry(g) : M1(g) -> ... -> the FIRST descIn hit of generation g's head.
     Reports the level and the actual left-comb count (the earlier probe REQUIRED
     comb >= 2^{k-1} and so may have silently skipped the true entry level).
  B. tail(g)     : the LAST cascadeReg k (k >= 9) before M1(g+1), and the gap.

Anchors (all measured): M1(1..5) = 188099 / 732733 / 2852091 / 11329301 / 44986995.
METHODS M1: check_anchors() gates the run.
"""
import sys, time
sys.path.insert(0, '/Users/aokiyousuke/busybeaver/.claude/worktrees/roadmap-post-closure-sync')
from x2r2_sim import (run, E, rle, cascade_at, comb_left, ones_left, check_anchors)

M1 = {1: 188099, 2: 732733, 3: 2852091, 4: 11329301, 5: 44986995}


def descIn_raw(tape, pos, r):
    """descIn signature WITHOUT the comb requirement; returns (k, comb, want) or None."""
    if len(r) >= 3 and r[0] == (0, 1) and r[1][0] == 1 and r[2] == (0, 2):
        blk = r[1][1]
        k = (blk + 3).bit_length() - 1
        if (1 << k) - 3 == blk and cascade_at(r, 3) == k - 2:
            return k, comb_left(tape, pos), 1 << (k - 1)
    return None


def cascadeReg_raw(tape, pos, r):
    if len(r) >= 4 and r[0] == (0, 3) and r[1][0] == 1 and r[2] == (0, 2):
        blk = r[1][1]
        k = (blk + 3).bit_length() - 1
        if (1 << k) - 3 == blk and cascade_at(r, 3) == k - 3:
            return k
    return None


def head_scan(g, span=250_000):
    """First descIn configs after M1(g)."""
    lo, hi = M1[g] + 1, M1[g] + span
    out = []

    def hook(step, st, pos, tape, origin):
        if st != E or tape[pos] != 0:
            return
        r = rle(tape, pos, maxruns=48)
        d = descIn_raw(tape, pos, r)
        if d is not None:
            out.append((step, pos - origin, d))
    run(hi, hook=hook, hook_from=lo)
    return out


def tail_scan(g, span=400_000):
    """Last cascadeReg k (k>=9) before M1(g+1), plus every E-on-0 config in the final 400."""
    target = M1[g + 1]
    lo = target - span
    best = None
    finals = []

    def hook(step, st, pos, tape, origin):
        nonlocal best
        if st != E or tape[pos] != 0:
            return
        r = rle(tape, pos, maxruns=48)
        k = cascadeReg_raw(tape, pos, r)
        if k is not None and k >= 9:
            best = (step, pos - origin, k)
        if step >= target - 400:
            finals.append((step, pos - origin,
                           ' '.join(f"{b}^{l}" for b, l in r[:8]), comb_left(tape, pos)))
    run(target + 1, hook=hook, hook_from=lo)
    return best, finals


assert check_anchors(verbose=False), "instrument check FAILED"
print("instrument OK\n")

print("=" * 72)
print("A.  topEntry(g) — the head's ENTRY level  (K(g) = g+8, so entry should be descIn K-1)")
print("=" * 72)
for g in (2, 3, 4):
    t0 = time.time()
    hits = head_scan(g)
    print(f"\ng={g}  M1({g}) @ {M1[g]}   K(g)={g+8}, expected entry descIn {g+7}")
    if not hits:
        print("  no descIn config found in the window")
    for step, pos, (k, comb, want) in hits[:6]:
        flag = 'COMB-OK' if comb >= want else f'comb SHORT ({comb} < {want})'
        print(f"  {step:>10} (+{step-M1[g]:>7} after M1)  descIn {k:<3} pos={pos:<7} {flag}")
    print(f"  [{round(time.time()-t0,1)}s]")

print("\n" + "=" * 72)
print("B.  tail(g) — last cascadeReg (k>=9) before M1(g+1)")
print("=" * 72)
for g in (2, 3):
    best, finals = tail_scan(g)
    print(f"\ng={g}  M1({g+1}) @ {M1[g+1]}   ladder top should be cascadeReg {g+9}")
    if best:
        print(f"  last cascadeReg: {best[2]} @ {best[0]} pos={best[1]}"
              f"   ->  tail({g}) = {M1[g+1]-best[0]} steps")
    else:
        print("  NO cascadeReg k>=9 found in the window")
    print("  final E-on-0 configs:")
    prev = None
    for step, pos, body, comb in finals:
        gap = f"(+{step-prev})" if prev is not None else ""
        prev = step
        print(f"    {step:>10} {gap:>7} pos={pos:>6} comb={comb:<4} | {body}")
