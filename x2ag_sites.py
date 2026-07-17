#!/usr/bin/env python3
"""x2ag_sites.py -- dump the REAL build(2) configs at REGEN(7)'s TI-confirmed
site boundaries, and check the 215 glue site against braid_topgrind's IN/OUT
pattern (N=6) cell-for-cell, solving for the concrete Lc / marker / casc.

REGEN(7) genuine window [12709,15239)  (x2ag_regen7.py, TI-filtered)
  offset    0        REGEN(7) IN
  offset  241  raw 12950   REGEN(4) IN   (TI-confirmed)
  offset  311  raw 13020   215 glue IN   == braid_topgrind N=6 IN ?
  offset  526  raw 13235   REGEN(5) IN   (TI-confirmed)
  offset  744  raw 13453   1089 glue IN  == descent_glue N=14 d+1=2 IN ?
  offset 1833  raw 14542   REGEN(4) IN   (TI-confirmed)
  offset 1903  raw 14612   627 glue IN
  offset 2530  raw 15239   REGEN(7) OUT
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

MARKS = [(12709, "REGEN(7) IN"), (12950, "REGEN(4) IN  [off 241]"),
         (13020, "215 glue IN  [off 311]"), (13235, "REGEN(5) IN  [off 526]"),
         (13453, "1089 glue IN [off 744]"), (14542, "REGEN(4) IN  [off 1833]"),
         (14612, "627 glue IN  [off 1903]"), (15239, "REGEN(7) OUT [off 2530]")]

def runs(bits, k=14):
    out = []; i = 0
    while i < len(bits) and len(out) < k:
        j = i
        while j < len(bits) and bits[j] == bits[i]: j += 1
        out.append("%d^%d" % (bits[i], j-i)); i = j
    return " ".join(out)

sim = build(2); sim.step()
snaps = {}
while sim.n <= 15239:
    if sim.n in dict(MARKS):
        snaps[sim.n] = (sim.st, sim.pos, sim.L[::-1], sim.h, sim.R[::-1])
    if not sim.step(): break

for n, label in MARKS:
    st, pos, L, h, R = snaps[n]
    print("--- %-26s raw n=%d  st=%s pos=%d head=%d" % (label, n, st, pos, h))
    print("      L (nearest-first) runs: %s" % runs(L))
    print("      R (nearest-first) runs: %s" % runs([h]+R))

# ---- the 215 site vs braid_topgrind N=6 ----
print("\n" + "="*72)
print("braid_topgrind N=6 IN  = E on 0, L = pow01(Lc+6) ++ marker,")
print("                         R = 0^3 ++ ones 13 ++ 0^2 ++ casc")
st, pos, L, h, R = snaps[13020]
seq = [h] + R
print("\nreal site 13020: st=%s head=%d" % (st, h))
print("   R = %s" % runs(seq, 8))
print("   R starts 0^3 1^13 0^2 ? ->",
      seq[:3] == [0,0,0] and seq[3:16] == [1]*13 and seq[16:18] == [0,0])
# solve Lc: L must start with pow01(Lc+6) = (0,1) repeated
i = 0
while i+1 < len(L) and L[i] == 0 and L[i+1] == 1: i += 2
print("   L begins (01)^%d then %s" % (i//2, runs(L[i:], 6)))
print("   -> Lc + 6 = %d  =>  Lc = %d" % (i//2, i//2 - 6))

# ---- braid_topgrind N=6 predicted OUT vs real 13235 ----
N, Lc = 6, i//2 - 6
st2, pos2, L2, h2, R2 = snaps[13235]
print("\nbraid_topgrind N=6 OUT = E at p+5+2N (= p+%d), L = ones %d ++ pow10 %d ++ 1::marker,"
      % (5+2*N, 4*N+4, Lc))
print("                          R = 0 :: casc")
print("real 13235: st=%s head=%d  head-shift = %d (predicted %d) -> %s"
      % (st2, h2, pos2-pos, 5+2*N, pos2-pos == 5+2*N))
print("   L = %s" % runs(L2, 8))
print("   L starts ones %d ++ pow10 %d ++ 1 ? -> %s"
      % (4*N+4, Lc, L2[:4*N+4] == [1]*(4*N+4) and L2[4*N+4:4*N+4+2*Lc] == [1,0]*Lc
         and L2[4*N+4+2*Lc] == 1))

# ---- the descent_glue OUT (raw 14542) vs the EXPLICIT deposit prediction ----
# descent_lower_fold_dep's existential dep is structurally determined:
#   D(0) = [1,0,1] ;  D(d+1) = D(d) ++ [0,0,1] ++ pow01(2^(d+3)-2)
# descent_glue's dep = D(d) ++ ones(4N+4) ++ pow10 Lc ++ [1] ++ marker
def pow01_(j): return [0,1]*j
def D(d):
    return [1,0,1] if d == 0 else D(d-1) + [0,0,1] + pow01_(2**(d+2)-2)
print("\n" + "="*72)
print("foldDep D(0) =", ''.join(map(str, D(0))))
print("foldDep D(1) =", ''.join(map(str, D(1))), "  (first 7 =",
      ''.join(map(str, D(1)[:7])), "; regen4_transport IN needs 1010010)")
st, pos, L, h, R = snaps[14542]
N, Lc = 14, 1
pred = [1]*12 + D(1) + [1]*(4*N+4) + [1,0]*Lc + [1]
print("\nreal L at 14542 (descent_glue OUT / REGEN(4) IN):")
print("   %s" % runs(L, 16))
print("predicted ones 12 ++ D(1) ++ ones 60 ++ pow10 1 ++ 1 ++ marker:")
print("   %s" % runs(pred, 16))
print("   PREFIX MATCH over %d cells -> %s" % (len(pred), L[:len(pred)] == pred))
