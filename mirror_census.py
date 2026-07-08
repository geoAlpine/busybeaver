# Unified fixed-point / mirror-ladder census verifier (2026-07-08).
#
# UNIFORM THEOREM. Every Type-I BB(6) cryptid runs, on its milestone variable v, a value map
#   T(v) = floor((p/q) v) + c_par(v)      (p/q in lowest terms, gcd(p,q)=1)
# whose per-branch affine pieces b(v) = (p v + e)/q have integer fixed points x = -e/(p-q),
# and since p is a UNIT in Z_q (gcd(p,q)=1), v_q(v - x) drops by exactly 1 per same-branch
# step. Hence the maximal run of a branch from v equals  v_q(v - x_branch).
#
# For the x3/2 family (q=2), with T(even v)=3v/2+c_e and T(odd v)=(3v-1)/2+c_o, the fixed
# points close in the corrections:  x_even = -2 c_e,  x_odd = 1 - 2 c_o.
# This script recomputes x for every machine's (c_e, c_o) and verifies run = v2(v - x)
# by direct simulation -- one uniform check across the whole (2,3) ladder, plus the x5/2
# (Space Needle) even branch.  The (3,4)/(3,8) machines (v3) are verified in their own
# notes and in the Lean layer; their fixed points are stated for the record.

def vq(n, q):
    n = abs(int(n))
    if n == 0: return 10**9
    k = 0
    while n % q == 0: n //= q; k += 1
    return k

def check_x32(c_e, c_o, N=200000):
    """T(even v)=3v/2+c_e, T(odd v)=(3v-1)/2+c_o.  x_e=-2c_e, x_o=1-2c_o.  run=v2(v-x)."""
    def T(v): return (3*v)//2 + c_e if v % 2 == 0 else (3*v-1)//2 + c_o
    x_e, x_o = -2*c_e, 1 - 2*c_o
    bad = 0
    for v in range(2, N):
        par = v % 2; x = x_e if par == 0 else x_o
        run = 0; w = v
        while w % 2 == par and run < 80:
            run += 1; w = T(w)
        if run != vq(v - x, 2): bad += 1
    return bad, (x_e, x_o)

def check_x52_even(N=200000):
    """Space Needle even branch f(m)=5m/2 (5 a 2-adic unit).  run = v2(m)."""
    bad = 0
    for m in range(2, N, 2):
        run = 0; w = m
        while w % 2 == 0 and run < 80:
            run += 1; w = (5*w)//2
        if run != vq(m, 2): bad += 1
    return bad

X32 = [("Antihydra", 0, 0), ("o11", 4, 4), ("o13", 7, 4), ("o14", 6, 6), ("o16", 2, 2)]

if __name__ == "__main__":
    print("UNIFIED MIRROR-LADDER CENSUS  (run = v_q(v - x_branch); p a q-adic unit)")
    print("=" * 72)
    allok = True
    for name, ce, co in X32:
        b, x = check_x32(ce, co)
        allok = allok and b == 0
        print(f"  {name:<11} x3/2 (q=2)  c=({ce},{co}) -> x={x}  run=v2(v-x): "
              f"{'OK' if b == 0 else str(b) + ' MISMATCH'}")
    bsn = check_x52_even()
    allok = allok and bsn == 0
    print(f"  {'SpaceNeedle':<11} x5/2 (q=2)  even x=0        run=v2(m):   "
          f"{'OK' if bsn == 0 else 'MISMATCH'}  (odd branch: NO single fixed point)")
    print(f"  {'o4':<11} x4/3 (q=3)  x=(-9,-14,-1)  run=v3(G-x): [PROVEN: O4_RUN_STRUCTURE + Lean]")
    print(f"  {'o15/o18':<11} x8/3 (q=3)  x=1            run=v3(V-1): [PROVEN: O15_FIXEDPOINT + Lean]")
    print("=" * 72)
    print("x_even = -2 c_e, x_odd = 1 - 2 c_o closes the x3/2 fixed points in the corrections.")
    print("ALL x3/2 + x5/2-even RUN LAWS VERIFIED." if allok else "MISMATCH -- investigate.")
    print("No machine decided. No label upgraded.")
