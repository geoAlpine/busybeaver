"""T7 measurement: the M6(g) -> M1(g+1) doubling phase.

Fast loop with an incremental `nl` = #True on the left tape, so the milestone
filter (state E, head 0, ENTIRE left side blank -- exactly M1's shape) is O(1).
"""
import sys
from x2t7_sim import (A, B, C, D, E, F, SNAMES, Cfg, M1, M6, zeros, ones,
                      pow10, pow01, uUnits, rUnits, m1casc)


def strip(xs):
    i = len(xs)
    while i > 0 and not xs[i - 1]:
        i -= 1
    return xs[:i]


def canon(c):
    return (c.st, tuple(strip(c.lean_left())), c.h, tuple(strip(c.lean_right())))


def fast_run(c, limit, hit_pred, report_every=None):
    """Run, maintaining nl. hit_pred(step, c, nl) -> truthy to record.
    Returns (list of hits, halted_at_or_None, steps_run)."""
    L, R = c.L, c.R
    st, h, pos = c.st, c.h, c.pos
    nl = sum(1 for b in L if b)
    hits = []
    for i in range(1, limit + 1):
        # --- inlined step ---
        if st == A:
            if not h:
                nh, ns, dp = True, B, 1
            else:
                nh, ns, dp = False, E, 1
            right = True
        elif st == B:
            if h:
                c.st, c.h, c.pos = st, h, pos
                return hits, i, i
            nh, ns, dp, right = True, C, 1, True
        elif st == C:
            if not h:
                nh, ns, dp, right = False, D, -1, False
            else:
                nh, ns, dp, right = True, E, -1, False
        elif st == D:
            if not h:
                nh, ns, dp, right = False, E, 1, True
            else:
                nh, ns, dp, right = True, D, -1, False
        elif st == E:
            if not h:
                nh, ns, dp, right = True, F, 1, True
            else:
                nh, ns, dp, right = False, C, -1, False
        else:  # F
            if not h:
                nh, ns, dp, right = False, A, 1, True
            else:
                nh, ns, dp, right = True, E, 1, True
        if right:
            L.append(nh)
            if nh:
                nl += 1
            h = R.pop() if R else False
        else:
            R.append(nh)
            if L:
                h = L.pop()
                if h:
                    nl -= 1
            else:
                h = False
        st = ns
        pos += dp
        # --- filter ---
        if st == E and not h and nl == 0:
            c.st, c.h, c.pos = st, h, pos
            hits.append((i, pos, len(L), canon(c)))
    c.st, c.h, c.pos = st, h, pos
    return hits, None, limit


def measure(g, limit):
    src = M6(g)
    tgt = M1(g + 1)
    tcanon = canon(tgt)
    c = src
    hits, halted, ran = fast_run(c, limit, None)
    if halted:
        return ("HALT", halted, None)
    match = [(n, pos, nlft) for (n, pos, nlft, k) in hits if k == tcanon]
    return ("OK", hits, match)


if __name__ == "__main__":
    gs = [int(x) for x in sys.argv[1:]] or [2, 3]
    for g in gs:
        K = g + 8
        limit = 1 << (2 * K - 1)
        st, hits, match = measure(g, limit)
        if st == "HALT":
            print(f"g={g}: HALTED at {hits}")
            continue
        print(f"g={g} K={K}: E/head0/left-blank events = {len(hits)}")
        for (n, pos, nl, k) in hits[:12]:
            print(f"    n={n:>12}  pos={pos:>8}  |left|={nl:>8}  "
                  f"{'*** = M1(g+1) canon ***' if k == canon(M1(g+1)) else ''}")
        print(f"  MATCHES to canon(M1({g+1})): {match}")
        sys.stdout.flush()
