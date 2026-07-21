"""DELIVERABLE 1+2: phase decomposition of M6(g) -> M1(g+1).

The `regenIn k` occurrences NEST (level k's exit tree contains lower-level
calls), so coverage is the UNION of the maximal intervals [n, n+exitSteps k).
The complement is what `regenLaw_closed` does NOT cover: report each gap with
the config at its two ends.
"""
import sys
from x2t7_sim import A, B, C, D, E, F, SNAMES, Cfg, M1, M6, step
from x2t7_scan import scan
from x2t7_verify import exitSteps, raw, strip

PHASE = {1: 544291, 2: 2119015, 3: 8476791, 4: 33657275, 5: 134602955, 6: 537346575}


def maximal(hits):
    iv = sorted(((n, n + exitSteps(k), k) for (nm, k, n, p) in hits if nm == "regenIn"))
    out = []
    for (a, b, k) in iv:
        if out and a >= out[-1][0] and b <= out[-1][1]:
            continue                      # nested inside previous maximal
        out.append((a, b, k))
    return out


def analyse(g):
    N = PHASE[g]
    hits, ctrl, status = scan(g, 4, g + 12, N)
    mx = maximal(hits)
    covered = sum(b - a for (a, b, k) in mx)
    print(f"=== g={g}  K={g+8}  doubling phase = {N} steps ===")
    print(f"  regenIn occurrences: {len([h for h in hits if h[0]=='regenIn'])}"
          f"   corrupted-seam control: {ctrl}")
    per = {}
    for (nm, k, n, p) in hits:
        per[k] = per.get(k, 0) + 1
    print(f"  per level k: {dict(sorted(per.items()))}   "
          f"(2^(K-k) = {[2**(g+8-k) for k in sorted(per)]})")
    print(f"  MAXIMAL (non-nested) REGEN intervals: {len(mx)}")
    for (a, b, k) in mx:
        print(f"      k={k:<3} [{a:>10}, {b:>10})  len={b-a:>9} = exitSteps({k})")
    print(f"  covered by regenLaw_closed: {covered} / {N} = {100*covered/N:.2f}%")
    gaps = []
    prev = 0
    for (a, b, k) in mx:
        if a > prev:
            gaps.append((prev, a))
        prev = max(prev, b)
    if prev < N:
        gaps.append((prev, N))
    print(f"  GAPS (uncovered): {len(gaps)}, total {sum(b-a for a,b in gaps)}")
    for (a, b) in gaps:
        print(f"      [{a:>10}, {b:>10})  len={b-a:>9}")
    return N, mx, gaps


def dump(g, n, w=90):
    c = M6(g); raw(c, n)
    s = lambda xs: "".join("1" if b else "0" for b in xs)
    l = c.lean_left()
    return (f"{SNAMES[c.st]}@{c.pos:<6} |L|={len(strip(l)):<6} "
            f"L:{s(l[:w])[::-1]:>{w}}[{'1' if c.h else '0'}]"
            f"{s(c.lean_right()[:w])}")


if __name__ == "__main__":
    for g in [int(x) for x in sys.argv[1:]]:
        N, mx, gaps = analyse(g)
        print("  --- config at each gap boundary ---")
        for (a, b) in gaps:
            print(f"   gap start n={a}:  {dump(g, a)}")
            print(f"   gap end   n={b}:  {dump(g, b)}")
        print()
