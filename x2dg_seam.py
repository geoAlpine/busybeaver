#!/usr/bin/env python3
"""x2dg_seam.py -- MEASURE the descentGlue seams bit-for-bit on the faithful build(2) orbit.

Checks, for a = 5,6,7:
  (1) the descent IN config (raw step DESC[a][0]) has the braid_topgrind IN shape
        E on 0, right = 0^3 1^{2^a-3} 0^2 descCascade(a-3), left = (01)^{Lc+N} ++ marker
  (2) the seam at IN + topGrindSteps(a): does braid_topgrind's OUT
        right = 0 :: descCascade(a-3) ++ 0^2 R,  left = 1^{4N+4} ++ (10)^Lc ++ 1 :: marker
      literally match descent_lower_fold's IN?
  (3) the post-lower-fold point at IN + topGrindSteps(a) + lowerFoldSteps(a-3):
        right = 0 :: 1^1 :: 0^2 R   (the residue -> the FINAL 100)
  (4) the FINAL 100 window's IN/OUT.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

DESC = {5: (13453, 14542), 6: (33830, 37982), 7: (114703, 131134)}


def topGrindSteps(a):
    return 2 ** (2 * a) + 7 - 3 * 2 ** a


def lowerFoldSteps(d):
    return 0 if d == 0 else (6 * (2 ** (d + 1) - 2) + 3) + lowerFoldSteps(d - 1)


def descentSteps(a):
    return 2 ** (2 * a) + 110 - 9 * a


def descCascade(d):
    """1^{2^{d+2}-3} 0^2 ... 0^2 1^1 as a bit list (head-first order)."""
    if d == 0:
        return [1]
    return [1] * (2 ** (d + 2) - 3) + [0, 0] + descCascade(d - 1)


def runs(bits, k=None):
    out = []
    i = 0
    while i < len(bits):
        b = bits[i]
        j = i
        while j < len(bits) and bits[j] == b:
            j += 1
        out.append((b, j - i))
        i = j
        if k and len(out) >= k:
            break
    return out


def snap(sim, kL=8, kR=10):
    return (sim.st, runs(sim.right_bits(), kR), sim.left_runs_top(kL), sim.pos)


def goto(sim, n):
    while sim.n < n:
        if not sim.step():
            raise SystemExit(f"HALT at {sim.n}")


for a in (5, 6, 7):
    s, e = DESC[a]
    N = 2 ** (a - 1) - 2
    d = a - 3
    tg = topGrindSteps(a)
    lf = lowerFoldSteps(d)
    print(f"\n=== a={a}  N={N} d={d}  window [{s},{e}] len={e-s} "
          f"descentSteps={descentSteps(a)} topGrind={tg} lowerFold={lf} "
          f"rest={descentSteps(a)-tg-lf}")

    sim = build(2)
    sim.step()
    goto(sim, s)
    p0 = sim.pos
    print(f" IN   @{sim.n:>7} st={sim.st} pos=+0")
    print(f"   right runs = {runs(sim.right_bits(), 10)}")
    print(f"   left  runs = {sim.left_runs_top(8)}")
    # EXPECTED IN right (braid_topgrind): 0^3 1^{2N+1} 0^2 descCascade(d)
    exp_in = [0, 0, 0, 0] + [1] * (2 * N + 1) + [0, 0] + descCascade(d)
    got_in = sim.right_bits()
    print(f"   IN right prefix match vs 0^3 1^{2*N+1} 0^2 descCascade({d})"
          f" [{len(exp_in)} cells]: {got_in[:len(exp_in)] == exp_in}")

    # (2) the TOPGRIND -> lower-fold seam
    goto(sim, s + tg)
    print(f" SEAM @{sim.n:>7} (IN+{tg}) st={sim.st} head={sim.h} dpos={sim.pos-p0}")
    print(f"   right runs = {runs(sim.right_bits(), 8)}")
    print(f"   left  runs = {sim.left_runs_top(6)}")
    exp_seam = [0, 0] + descCascade(d)
    print(f"   SEAM right prefix == 0 :: descCascade({d}) [{len(exp_seam)} cells]: "
          f"{sim.right_bits()[:len(exp_seam)] == exp_seam}")
    print(f"   expected dpos = 5+2N = {5+2*N}: {sim.pos-p0 == 5+2*N}")

    # (3) after the lower fold: the residue
    goto(sim, s + tg + lf)
    print(f" RESID@{sim.n:>7} (IN+{tg+lf}) st={sim.st} head={sim.h} dpos={sim.pos-p0}")
    print(f"   right runs = {runs(sim.right_bits(), 8)}")
    print(f"   left  runs = {sim.left_runs_top(6)}")
    print(f"   RESID right prefix == [0,0,1,0,0]: {sim.right_bits()[:5] == [0,0,1,0,0]}")

    # (4) the FINAL
    goto(sim, s + descentSteps(a))
    print(f" OUT  @{sim.n:>7} (IN+{descentSteps(a)}) st={sim.st} head={sim.h} dpos={sim.pos-p0}")
    print(f"   right runs = {runs(sim.right_bits(), 8)}")
    print(f"   left  runs = {sim.left_runs_top(6)}")
