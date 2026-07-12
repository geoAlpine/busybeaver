#!/usr/bin/env python3
"""x2la_extract.py -- emit the EXACT tail-parametric window for a non-carry tick,
and SELF-VERIFY tail-independence by re-running with two different tail paddings.

For a tick [n0,n1] with head excursion [lo,hi]:
  untouched-left  tail = cells at pos < lo   (never visited)
  untouched-right tail = cells at pos > hi   (never visited)
The theorem is translation-fixed to head pos 0 at the start.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import Sim, build, TT


def sim_to(g, n0):
    sim = build(g)
    sim.step()
    while sim.n < n0:
        assert sim.step()
    return sim


def excursion(g, n0, n1):
    sim = sim_to(g, n0)
    lo = hi = sim.pos
    while sim.n < n1:
        assert sim.step()
        lo = min(lo, sim.pos); hi = max(hi, sim.pos)
    return lo, hi


def abs_tape(sim):
    """dict pos->bit over the whole current tape, plus (minpos,maxpos)."""
    d = {}
    d[sim.pos] = sim.h
    for i, b in enumerate(sim.L):        # L[-1] nearest = pos-1
        d[sim.pos - 1 - i] = b
    # careful: sim.L nearest is L[-1]; L[-1-k] at pos-1-k
    d = {sim.pos: sim.h}
    for k in range(len(sim.L)):
        d[sim.pos - 1 - k] = sim.L[-1 - k]
    for k in range(len(sim.R)):
        d[sim.pos + 1 + k] = sim.R[-1 - k]
    return d


def lean_list(bits):
    return ''.join(('true :: ' if b else 'false :: ') for b in bits)


def extract(g, n0, n1, verbose=True):
    lo, hi = excursion(g, n0, n1)
    s0 = sim_to(g, n0)
    p0, st0 = s0.pos, s0.st
    t0 = abs_tape(s0)
    s1 = sim_to(g, n1)
    p1, st1 = s1.pos, s1.st
    t1 = abs_tape(s1)
    # touched left prefix: pos from p0-1 down to lo (nearest-first)
    # untouched left tail: pos < lo  -> parametric L
    left_prefix = [t0[p0 - 1 - k] for k in range(p0 - lo)]  # pos p0-1 .. lo
    # touched right: pos p0+1 .. hi ; untouched right tail pos>hi -> parametric R
    right_prefix = [t0[p0 + 1 + k] for k in range(hi - p0)]  # pos p0+1 .. hi
    head0 = t0[p0]
    # END expressed with SAME parametric tails (pos<lo, pos>hi identical in t0,t1)
    end_left_prefix = [t1[p1 - 1 - k] for k in range(p1 - lo)]
    end_right_prefix = [t1[p1 + 1 + k] for k in range(hi - p1)]
    head1 = t1[p1]
    # verify untouched tails identical
    for pos in range(lo - 10, lo):
        if t0.get(pos) != t1.get(pos):
            print(f"  !! left tail differs at pos {pos}: {t0.get(pos)} vs {t1.get(pos)}")
    for pos in range(hi + 1, hi + 11):
        if t0.get(pos) != t1.get(pos):
            print(f"  !! right tail differs at pos {pos}: {t0.get(pos)} vs {t1.get(pos)}")
    if verbose:
        print(f"=== tick n={n0}->{n1}  ({n1-n0} steps)  st {st0}->{st1}  "
              f"pos {p0}->{p1} (shift {p1-p0})  excursion [{lo},{hi}] rel [{lo-p0},{hi-p0}] ===")
        print(f"  START: st {st0}, pos 0")
        print(f"    left  = {lean_list(left_prefix)}L")
        print(f"    head  = {'true' if head0 else 'false'}")
        print(f"    right = {lean_list(right_prefix)}R")
        print(f"  END:   st {st1}, pos {p1-p0}")
        print(f"    left  = {lean_list(end_left_prefix)}L")
        print(f"    head  = {'true' if head1 else 'false'}")
        print(f"    right = {lean_list(end_right_prefix)}R")
    return (st0, left_prefix, head0, right_prefix), (st1, end_left_prefix, head1, end_right_prefix, p1 - p0)


def verify_tailparam(g, n0, n1, pad_variants=(([], []), ([0, 0, 0], [0, 0, 0]),
                                              ([1, 0, 1], [1, 1, 1, 0]))):
    """Run the extracted window with different parametric tails; confirm the
    touched-window transform is IDENTICAL (proves tail-independence empirically)."""
    (st0, lp, h0, rp), (st1, elp, h1, erp, shift) = extract(g, n0, n1, verbose=False)
    nsteps = n1 - n0
    results = []
    for (Lpad, Rpad) in pad_variants:
        # build a Sim directly from the window + pads, head at pos 0
        # right string: head then right_prefix then Rpad
        rstr = ''.join('1' if b else '0' for b in ([h0] + rp + Rpad))
        sim = Sim(rstr, state=st0, pos=0)
        # set left = lp (nearest-first) + Lpad, but Sim.L is nearest at end
        Lfull = (lp + Lpad)          # nearest-first
        sim.L = Lfull[::-1]          # store so L[-1] = nearest
        for _ in range(nsteps):
            if not sim.step():
                results.append(('HALT', sim.n)); break
        else:
            # read back ONLY the touched-window transform (strictly inside [lo,hi],
            # excluding parametric tail cells that merely pass padding through)
            lo, hi = excursion(g, n0, n1)
            p0 = sim_to(g, n0).pos
            d = abs_tape(sim)
            win = tuple((pos, d.get(pos, 0)) for pos in range(lo - p0, hi - p0 + 1))
            results.append((sim.st, sim.pos, win))
    ok = all(r == results[0] for r in results)
    print(f"  tail-independence over {len(pad_variants)} paddings: "
          f"{'CONSISTENT' if ok else 'INCONSISTENT'}")
    if not ok:
        for r in results:
            print("    ", r)
    return ok


if __name__ == "__main__":
    g = 2
    ticks = [(6717, 6731), (6731, 6753), (6753, 6783), (6821, 6923)]
    if len(sys.argv) >= 3:
        ticks = [(int(sys.argv[1]), int(sys.argv[2]))]
    for n0, n1 in ticks:
        extract(g, n0, n1)
        verify_tailparam(g, n0, n1)
        print()
