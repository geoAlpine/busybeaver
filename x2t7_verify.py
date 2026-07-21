"""DELIVERABLE 3: does `regenLaw_closed` fire on the real doubling-phase orbit?

At each on-orbit `regenIn k` occurrence, run exactly `exitSteps k` further steps
and check the result IS `cascadeReg k 1 (p - 2^k) marker R`.

Off-list tape cells are BLANK, so all tape comparisons are modulo trailing
`false` padding (`eqb` below).  Controls: a corrupted-seam IN family (must never
fire) and an off-by-one step count (must never land).
"""
import sys
from x2t7_sim import A, B, C, D, E, F, SNAMES, Cfg, M1, M6, ones, zeros, pow01, step
from x2t7_scan import (descCascade, regenIn_left_prefix, regenIn_right_prefix,
                       cascadeReg_left_prefix, cascadeReg_right_prefix, endswith, scan)


def exitSteps(k):
    return 2 ** (2 * k - 3) + k * 2 ** (k - 1) + 2 ** (k - 2) + 2


def strip(xs):
    i = len(xs)
    while i > 0 and not xs[i - 1]:
        i -= 1
    return xs[:i]


def eqb(a, b):
    """tape-list equality modulo trailing blanks (off-list cells are blank)"""
    return strip(list(a)) == strip(list(b))


def at(xs, i, n):
    """xs[i:i+n], blank-extended"""
    seg = list(xs[i:i + n])
    return seg + [False] * (n - len(seg))


def raw(c, n):
    for _ in range(n):
        if not step(c):
            return None
    return c


def verify(g, k, n, extra=0):
    c = M6(g)
    if raw(c, n) is None:
        return None
    okin = (c.st == E and not c.h
            and endswith(c.L, regenIn_left_prefix(k))
            and endswith(c.R, regenIn_right_prefix(k)))
    z = 2 ** (k - 1) + 9
    pref = len(regenIn_right_prefix(k))
    padok = not any(at(c.lean_right(), pref, z))
    pin = c.pos
    marker = c.lean_left()[len(regenIn_left_prefix(k)):]
    Rtail = c.lean_right()[pref + z:]
    if raw(c, exitSteps(k) + extra) is None:
        return None
    exp_left = cascadeReg_left_prefix(k, 1) + marker
    exp_right = cascadeReg_right_prefix(k) + Rtail
    okout = (c.st == E and c.pos == pin - 2 ** k and not c.h
             and eqb(c.lean_left(), exp_left) and eqb(c.lean_right(), exp_right))
    return okin, padok, okout, pin, len(strip(marker)), len(strip(Rtail))


if __name__ == "__main__":
    g = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    lim = {1: 544291, 2: 2119015, 3: 8476791}[g]
    hits, ctrl, status = scan(g, 4, g + 12, lim)
    print(f"g={g}: {len(hits)} `regenIn` occurrences on the doubling orbit; "
          f"corrupted-seam CONTROL hits={ctrl} (must be 0)")
    seen = {}
    for nm, k, i, p in hits:
        if nm == "regenIn":
            seen.setdefault(k, []).append((i, p))
    print(f"  occurrences per level: "
          f"{ {k: len(v) for k, v in sorted(seen.items())} }")
    print("\n=== regenLaw_closed applied at the FIRST occurrence of each level ===")
    allok = True
    for k in sorted(seen):
        n, p = seen[k][0]
        r = verify(g, k, n)
        okin, padok, okout, pin, ml, rl = r
        allok &= (okin and padok and okout)
        print(f"  k={k:<2} @{n:<9} pos={pin:<6} exitSteps={exitSteps(k):<8} "
              f"IN={okin} pad(z={2**(k-1)+9})={padok} "
              f"OUT=cascadeReg k 1 (p-2^{k}) : {okout}   |marker|={ml} |R|={rl}")
    print(f"  ALL GREEN: {allok}")

    print("\n=== CONTROL: exitSteps k +1 / -1 must NOT land (all False) ===")
    for k in sorted(seen):
        n, p = seen[k][0]
        a = verify(g, k, n, +1); b = verify(g, k, n, -1)
        print(f"  k={k:<2}  +1 lands: {a[2] if a else 'halt'}   "
              f"-1 lands: {b[2] if b else 'halt'}")

    print("\n=== EVERY occurrence at every level (full sweep) ===")
    bad = []
    for k in sorted(seen):
        for (n, p) in seen[k]:
            r = verify(g, k, n)
            if not (r and r[0] and r[1] and r[2]):
                bad.append((k, n, r))
    print(f"  occurrences checked: {sum(len(v) for v in seen.values())}, "
          f"FAILURES: {len(bad)}")
    for x in bad[:10]:
        print("   ", x)
