#!/usr/bin/env python3
"""x2rc_regen_lands.py -- does the ALREADY-PROVEN REGEN(k) transport's OUT register
literally EQUAL descent_glue's IN (= cascadeReg(k))?  k=4,5.

lean/X2.lean's `regen4_transport` / `regen5_transport` are stated `forall L R`.  This
probe checks, as pure LIST DATA, that instantiating those two universally-quantified
tails makes the OUT match `cascadeReg(k)` cell-for-cell -- i.e. the seam needs NO
connector, exactly as §5ag's seam 1 did not.

This is a LIST-ALGEBRA check (the Lean proof is `descent_reach_4/5` in §5ah); it is not
simulator evidence.  The on-path evidence is x2rc_regen_shape.py.
"""

def ones(n):    return [1] * n
def zeros(n):   return [0] * n
def pow01(k):   return [0, 1] * k


def descCascade(d):
    if d == 0:
        return [1]
    return ones(2 ** (d + 2) - 3) + [0, 0] + descCascade(d - 1)


def cascadeReg(k, Lc, marker, R):
    """descent_glue's IN, k-indexed: left, head, right."""
    N = 2 ** (k - 1) - 2
    left = pow01(Lc + N) + marker
    right = ([0, 0, 0] + ones(2 * N + 1) + [0, 0]
             + descCascade(k - 3) + [0, 0] + zeros(7) + R)
    return left, 0, right


# --- regen4_transport's OUT, transcribed from lean/X2.lean (forall L R) ---
def regen4_out(L, R):
    left = [0, 1, 0] + L
    right = ([0, 0, 0] + ones(13) + [0, 0] + ones(5) + [0, 0] + ones(1) + [0, 0, 0] + R)
    return left, 0, right


# --- regen5_transport's OUT, transcribed from lean/X2.lean (forall L R) ---
def regen5_out(L, R):
    left = [0] + L
    right = ([0, 0, 0] + ones(29) + [0, 0] + ones(13) + [0, 0] + ones(5) + [0, 0]
             + ones(1) + [0] + R)
    return left, 0, right


if __name__ == "__main__":
    marker = ['M1', 'M2', 'M3']      # opaque symbols: stands for the forall-quantified marker
    Rp = ['R1', 'R2', 'R3']          # stands for the forall-quantified R

    print("=== k=4: regen4_transport OUT  vs  cascadeReg(4, Lc=1) ===")
    got = regen4_out(L=[1] + pow01(5) + marker, R=zeros(6) + Rp)
    want = cascadeReg(4, 1, marker, Rp)
    print(f"  instantiate L := 1 :: (01)^5 ++ marker,  R := 0^6 ++ R")
    print(f"  left  match: {got[0] == want[0]}")
    print(f"  right match: {got[2] == want[2]}")
    print(f"  FULL match : {got == want}")

    print("\n=== k=5: regen5_transport OUT  vs  cascadeReg(5, Lc=1) ===")
    got = regen5_out(L=[1] + pow01(14) + marker, R=zeros(8) + Rp)
    want = cascadeReg(5, 1, marker, Rp)
    print(f"  instantiate L := 1 :: (01)^14 ++ marker, R := 0^8 ++ R")
    print(f"  left  match: {got[0] == want[0]}")
    print(f"  right match: {got[2] == want[2]}")
    print(f"  FULL match : {got == want}")

    print("\n=== the COLLAPSE identity 1^{2^k-3} 0^2 descCascade(k-3) == descCascade(k-2) ===")
    for k in range(4, 12):
        lhs = ones(2 ** k - 3) + [0, 0] + descCascade(k - 3)
        print(f"  k={k:2d}: {lhs == descCascade(k - 2)}")
