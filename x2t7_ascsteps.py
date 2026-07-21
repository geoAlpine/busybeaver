"""RE-MEASUREMENT of the `ascSteps b n` claim (coordinator asked for this explicitly).

CLAIM UNDER TEST (X2.lean line 8734):
    ascSteps b 0     = 0
    ascSteps b (n+1) = (exitSteps b + topGrindSteps b) + ascSteps (b+1) n
and `ascSpine`: from `regenIn b`, `ascSteps b n` steps land on `regenIn (b+n)`.

TEST: take a REAL on-orbit `regenIn b` occurrence, run exactly `ascSteps b n`
steps, and check the config is the `regenIn (b+n)` family shape.

CONTROLS (must all fail):
  - off-by-one step counts (ascSteps +/- 1)
  - a corrupted-seam regenIn family (never matches at all)
  - landing on the WRONG level regenIn (b+n+1) / (b+n-1)
"""
import sys
from x2t7_sim import M6, M1, SNAMES, E
from x2t7_scan import (regenIn_left_prefix, regenIn_right_prefix,
                       control_left_prefix, endswith, scan)
from x2t7_verify import exitSteps, raw, strip


def topGrindSteps(a): return 2 ** (2 * a) + 7 - 3 * 2 ** a
def descentSteps(a): return 2 ** (2 * a) + 110 - 9 * a


def ascSteps(b, n):
    """X2.lean's def, transcribed recursively (NOT a closed form)."""
    return 0 if n == 0 else (exitSteps(b) + topGrindSteps(b)) + ascSteps(b + 1, n - 1)


def is_regenIn(c, k):
    return (c.st == E and not c.h
            and endswith(c.L, regenIn_left_prefix(k))
            and endswith(c.R, regenIn_right_prefix(k)))


def is_control_family(c, k):
    """corrupted seam -- must NEVER match"""
    return (c.st == E and not c.h and endswith(c.L, control_left_prefix(k)))


if __name__ == "__main__":
    g = 1
    N = 544291
    hits, ctrl, status = scan(g, 4, g + 12, N)
    first = {}
    for nm, k, i, p in hits:
        if nm == "regenIn":
            first.setdefault(k, i)
    print(f"on-orbit regenIn occurrences (g={g}): "
          f"{ {k: sum(1 for h in hits if h[1]==k) for k in sorted(first)} }")
    print(f"corrupted-seam control hits over the whole phase: {ctrl}  (must be 0)\n")

    b = 4
    start = first[4]
    print(f"=== ascSpine test: from the on-orbit regenIn(4) at phase-step {start} ===")
    print(f"{'n':>2} {'ascSteps(4,n)':>14}  lands on regenIn(4+n)?   "
          f"CONTROLS: +1   -1   wrong-level   corrupted")
    allok = True
    for n in range(0, 5):
        S = ascSteps(b, n)
        c = M6(g); raw(c, start); raw(c, S)
        ok = is_regenIn(c, b + n)
        c1 = M6(g); raw(c1, start); raw(c1, S + 1)
        c2 = M6(g); raw(c2, start); raw(c2, S - 1) if S >= 1 else None
        ctl_p1 = is_regenIn(c1, b + n)
        ctl_m1 = is_regenIn(c2, b + n) if S >= 1 else False
        ctl_wrong = is_regenIn(c, b + n + 1) or (n > 0 and is_regenIn(c, b + n - 1))
        ctl_corrupt = is_control_family(c, b + n)
        allok &= ok and not (ctl_p1 or ctl_m1 or ctl_wrong or ctl_corrupt)
        print(f"{n:>2} {S:>14}  {str(ok):>20}   "
              f"{str(ctl_p1):>5} {str(ctl_m1):>5} {str(ctl_wrong):>12} {str(ctl_corrupt):>10}")
    print(f"\n  ascSpine step-count claim SURVIVES re-measurement: {allok}")

    print(f"\n=== rampDescend test: ascSteps(4,n) + exitSteps(4+n) + descentSteps(4+n) ===")
    print(f"     should land back on the FLOOR family regenIn(4)")
    allok2 = True
    for n in range(1, 5):
        S = ascSteps(b, n) + exitSteps(b + n) + descentSteps(b + n)
        c = M6(g); raw(c, start); raw(c, S)
        ok = is_regenIn(c, 4)
        c1 = M6(g); raw(c1, start); raw(c1, S + 1)
        c2 = M6(g); raw(c2, start); raw(c2, S - 1)
        allok2 &= ok and not is_regenIn(c1, 4) and not is_regenIn(c2, 4)
        print(f"  n={n} total={S:>9}  lands on regenIn(4): {ok}    "
              f"CONTROL +1: {is_regenIn(c1,4)}  -1: {is_regenIn(c2,4)}")
    print(f"\n  rampDescend step-count claim SURVIVES re-measurement: {allok2}")

    print(f"\n=== the measured LADDER as a chain of rampDescend rungs ===")
    def rung(n): return ascSteps(4, n) + exitSteps(4 + n) + descentSteps(4 + n)
    def ladder(m): return exitSteps(4) if m == 0 else ladder(m - 1) + rung(m)
    meas = {4: 132470, 5: 528510, 6: 2108038, 7: 8414862, 8: 33615510,
            9: 134356638, 10: 537181862}
    for m, v in meas.items():
        print(f"  ladderSteps {m} = {ladder(m):>12}   measured LADDER({m+4}) = {v:>12}   "
              f"{'EXACT' if ladder(m) == v else 'MISMATCH'}")
    # CONTROL: a deliberately wrong rung (drop the descent) must NOT reproduce
    def rung_bad(n): return ascSteps(4, n) + exitSteps(4 + n)
    def ladder_bad(m): return exitSteps(4) if m == 0 else ladder_bad(m - 1) + rung_bad(m)
    print(f"  CONTROL (rung without descentSteps): ladder_bad 4 = {ladder_bad(4)} "
          f"vs measured 132470 -> {'MATCHES (BAD!)' if ladder_bad(4)==132470 else 'differs, as required'}")
