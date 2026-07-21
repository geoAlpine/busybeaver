"""Does the banked `regenIn k` / `cascadeReg k` family OCCUR on the M6(g) -> M1(g+1)
doubling-phase orbit?  If it does, `regenLaw_closed` discharges that segment outright.

Both families are built FROM THE LEAN DEFINITIONS (never lifted off the orbit).
`marker`, `R`, `z` are free tails, so we match PREFIXES of the two tape lists.
A control family (`regenIn` with a deliberately wrong seam) is scanned too and
MUST never fire.
"""
import sys
from x2t7_sim import A, B, C, D, E, F, SNAMES, Cfg, M1, M6, ones, zeros, pow01, pow10


def descCascade(d):
    out = []
    for i in range(d, 0, -1):
        out += ones(2 ** (i + 2) - 3) + [False, False]
    return out + ones(1)


# ---- the fixed (marker/R-independent) prefixes of the two Lean families ----
def regenIn_left_prefix(k):
    # ones(2^k-3) ++ [F,T,F,F,T] ++ pow01(2^(k-1)-2)   (nearest-first)
    return ones(2 ** k - 3) + [False, True, False, False, True] + pow01(2 ** (k - 1) - 2)


def regenIn_right_prefix(k):
    # [F] ++ descCascade(k-4)   (then zeros z ++ R, free)
    return [False] + descCascade(k - 4)


def cascadeReg_left_prefix(k, Lc=1):
    return pow01(Lc + (2 ** (k - 1) - 2))


def cascadeReg_right_prefix(k):
    return ([False, False, False] + ones(2 ** k - 3) + [False, False]
            + descCascade(k - 3) + [False, False] + zeros(7))


# CONTROL: same shape, seam corrupted (F,T,F,F,T -> F,T,F,T,T). Must never fire.
def control_left_prefix(k):
    return ones(2 ** k - 3) + [False, True, False, True, True] + pow01(2 ** (k - 1) - 2)


def endswith(lst, pref):
    """lst is the REVERSED store (nearest = last). pref is nearest-first."""
    n = len(pref)
    if len(lst) < n:
        return False
    seg = lst[len(lst) - n:]
    seg.reverse()
    return seg == pref


def scan(g, kmin, kmax, limit):
    RIL = {k: regenIn_left_prefix(k) for k in range(kmin, kmax + 1)}
    RIR = {k: regenIn_right_prefix(k) for k in range(kmin, kmax + 1)}
    CRL = {k: cascadeReg_left_prefix(k) for k in range(kmin, kmax + 1)}
    CRR = {k: cascadeReg_right_prefix(k) for k in range(kmin, kmax + 1)}
    CTL = {k: control_left_prefix(k) for k in range(kmin, kmax + 1)}
    onerun = {2 ** k - 3: k for k in range(kmin, kmax + 1)}

    c = M6(g)
    L, R = c.L, c.R
    st, h, pos = c.st, c.h, c.pos
    hits = []
    ctrl_hits = 0
    for i in range(1, limit + 1):
        if st == A:
            nh, ns, dp, right = (True, B, 1, True) if not h else (False, E, 1, True)
        elif st == B:
            if h: return hits, ctrl_hits, ("HALT", i)
            nh, ns, dp, right = True, C, 1, True
        elif st == C:
            nh, ns, dp, right = (False, D, -1, False) if not h else (True, E, -1, False)
        elif st == D:
            nh, ns, dp, right = (False, E, 1, True) if not h else (True, D, -1, False)
        elif st == E:
            nh, ns, dp, right = (True, F, 1, True) if not h else (False, C, -1, False)
        else:
            nh, ns, dp, right = (False, A, 1, True) if not h else (True, E, 1, True)
        if right:
            L.append(nh)
            h = R.pop() if R else False
        else:
            R.append(nh)
            h = L.pop() if L else False
        st = ns; pos += dp

        if st != E or h:
            continue
        # --- regenIn gate: >=13 ones immediately left, a 0 immediately right ---
        if len(L) >= 13 and L[-1] and L[-13] and all(L[-13:]) and R and not R[-1]:
            n1 = 0
            j = len(L) - 1
            while j >= 0 and L[j]:
                n1 += 1; j -= 1
            k = onerun.get(n1)
            if k is not None:
                if endswith(L, RIL[k]) and endswith(R, RIR[k]):
                    hits.append(("regenIn", k, i, pos))
                if endswith(L, CTL[k]):
                    ctrl_hits += 1
        # --- cascadeReg gate: 000 then a 1-run on the right, comb on the left ---
        if len(R) >= 4 and not R[-1] and not R[-2] and not R[-3] and R[-4] \
           and len(L) >= 2 and not L[-1] and L[-2]:
            n1 = 0
            j = len(R) - 4
            while j >= 0 and R[j]:
                n1 += 1; j -= 1
            k = onerun.get(n1)
            if k is not None and endswith(L, CRL[k]) and endswith(R, CRR[k]):
                hits.append(("cascadeReg", k, i, pos))
    return hits, ctrl_hits, ("RAN", limit)


if __name__ == "__main__":
    for g in [int(x) for x in sys.argv[1:]]:
        K = g + 8
        lim = {1: 544291, 2: 2119015, 3: 8476791, 4: 33657275, 5: 134602955}[g]
        hits, ctrl, status = scan(g, 4, K + 4, lim)
        print(f"=== g={g} (K={K}), doubling phase = {lim} steps, status={status} ===")
        print(f"  CONTROL (corrupted-seam regenIn) hits: {ctrl}  (MUST be 0)")
        if not hits:
            print("  NO regenIn/cascadeReg occurrence found.")
        for nm, k, i, p in hits:
            print(f"  {nm:>11} k={k:<3} at phase-step {i:>12}  pos={p}")
        sys.stdout.flush()
