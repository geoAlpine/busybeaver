"""DELIVERABLE 2: classify EVERY segment of the doubling phase against the
banked forall-lemma inventory.

  exitSteps k      = 2^(2k-3) + k*2^(k-1) + 2^(k-2) + 2   -> regenLaw_closed  (5bk)
  topGrindSteps k  = 2^(2k) + 7 - 3*2^k                   -> braid_topgrind   (5af/5ak)
  descentSteps k   = 2^(2k) + 110 - 9k                    -> descent_glue     (5ag)
anything else      -> UNCOVERED.
"""
import sys
from x2t7_sim import M6, M1, SNAMES
from x2t7_scan import scan
from x2t7_verify import exitSteps, raw, strip, eqb
from x2t7_cover import maximal, PHASE


def topGrindSteps(a): return 2 ** (2 * a) + 7 - 3 * 2 ** a
def descentSteps(a): return 2 ** (2 * a) + 110 - 9 * a


def classify(n, kmax):
    for k in range(3, kmax + 2):
        if topGrindSteps(k) == n: return f"topGrindSteps({k})  [braid_topgrind, banked forall]"
        if descentSteps(k) == n:  return f"descentSteps({k})   [descent_glue, banked forall]"
    return None


if __name__ == "__main__":
    for g in [int(x) for x in sys.argv[1:]]:
        K = g + 8
        N = PHASE[g]
        hits, ctrl, status = scan(g, 4, g + 12, N)
        mx = maximal(hits)
        segs = []
        prev = 0
        for (a, b, k) in mx:
            if a > prev: segs.append((prev, a, None))
            segs.append((a, b, k)); prev = max(prev, b)
        if prev < N: segs.append((prev, N, None))

        cov_regen = cov_tg = cov_dg = unc = 0
        unknown = []
        for (a, b, k) in segs:
            L = b - a
            if k is not None:
                cov_regen += L; continue
            c = classify(L, K + 2)
            if c is None:
                unc += L; unknown.append((a, b, L))
            elif c.startswith("topGrind"): cov_tg += L
            else: cov_dg += L
        print(f"=== g={g} K={K}  phase = {N} steps, {len(segs)} segments ===")
        print(f"  regenLaw_closed (exitSteps)     : {cov_regen:>11}  {100*cov_regen/N:6.2f}%")
        print(f"  braid_topgrind  (topGrindSteps) : {cov_tg:>11}  {100*cov_tg/N:6.2f}%")
        print(f"  descent_glue    (descentSteps)  : {cov_dg:>11}  {100*cov_dg/N:6.2f}%")
        print(f"  ---- covered by banked forall   : "
              f"{cov_regen+cov_tg+cov_dg:>11}  {100*(cov_regen+cov_tg+cov_dg)/N:6.2f}%")
        print(f"  UNCOVERED                       : {unc:>11}  {100*unc/N:6.2f}%"
              f"   in {len(unknown)} segment(s)")
        for (a, b, L) in unknown:
            role = ("ENTRY" if a == 0 else "EXIT" if b == N else "MIDGAP")
            print(f"      {role:<7} [{a:>10},{b:>10})  len={L}")
        sys.stdout.flush()
