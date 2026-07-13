#!/usr/bin/env python3
"""x2lm_extract.py -- extract the EXACT bounded-window transport of one forward tile
and confirm it is a translation-invariant tile with arbitrary L/R frames.

Strategy: run g=4 (even) to M3, then to M4. Locate the steady forward tiles
(consecutive len-14-anchored 29-step compounds at pos 23->30->37). For one tile:
- compute the exact head pos window [lo,hi] visited during the 29 steps
- dump the FULL zipper config at tile start and tile end
- express both as: fixed local window content + arbitrary far-left L / far-right R frame
Then verify tile(pos30) start config == tile(pos23) end config, and that the far
frames only ACCUMULATE (2 ones added to left comb) / shift.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def to_M3(g):
    sim = build(g)
    sim.step()
    mc = 0
    while True:
        if sim.is_milestone():
            mc += 1
            if mc == 2:
                return sim
        if not sim.step():
            return sim


def absbits(sim):
    """return dict offset->bit relative to head, plus pos."""
    d = {0: sim.h}
    for i, b in enumerate(reversed(sim.R)):  # reversed(R) = far..near? R stored reversed
        pass
    # R stored reversed so R[-1] nearest (offset+1). rebuild:
    for k in range(len(sim.R)):
        d[k + 1] = sim.R[len(sim.R) - 1 - k]
    for k in range(len(sim.L)):
        d[-(k + 1)] = sim.L[len(sim.L) - 1 - k]
    return d


def full(sim):
    return (sim.st, sim.pos, sim.h, list(sim.L), list(sim.R))


def main():
    g = 4
    sim = to_M3(g)
    # step to M4 collecting configs by n
    configs = {sim.n: full(sim)}
    poslog = {sim.n: sim.pos}
    while True:
        if not sim.step():
            break
        configs[sim.n] = full(sim)
        poslog[sim.n] = sim.pos
        if sim.is_milestone():
            break

    # steady tiles start at n=215, 244, 273 (pos 23,30,37) per x2lm_tile
    for n0 in (215, 244):
        n1 = n0 + 29
        lo = min(poslog[n] for n in range(n0, n1 + 1))
        hi = max(poslog[n] for n in range(n0, n1 + 1))
        st0, p0, h0, L0, R0 = configs[n0]
        st1, p1, h1, L1, R1 = configs[n1]
        print(f"\n--- tile n={n0}->{n1}: pos {p0}->{p1}, head window [{lo}..{hi}] ---")
        print(f"  start st={st0} pos={p0}  |L|={len(L0)} |R|={len(R0)}")
        print(f"  end   st={st1} pos={p1}  |L|={len(L1)} |R|={len(R1)}  dL={len(L1)-len(L0)} dR={len(R1)-len(R0)}")
        # local window content [lo..hi] at start & end
        def win(L, h, R, pos, lo, hi):
            # absolute bit at position q given head at pos
            d = {0: h}
            for k in range(len(R)):
                d[k + 1] = R[len(R) - 1 - k]
            for k in range(len(L)):
                d[-(k + 1)] = L[len(L) - 1 - k]
            return [d.get(q - pos, 0) for q in range(lo, hi + 1)]
        ws = win(L0, h0, R0, p0, lo, hi)
        we = win(L1, h1, R1, p1, lo, hi)
        print(f"  window[{lo}..{hi}] start: {ws}")
        print(f"  window[{lo}..{hi}] end  : {we}")

    # translation-invariance of the transport with frames:
    # compare tile@215 (start) shifted +7 vs tile@244 (start)
    st0, p0, h0, L0, R0 = configs[215]
    st2, p2, h2, L2, R2 = configs[244]
    print("\n--- frame check: does start@244 == start@215 with left comb +2 ones, shifted +7? ---")
    print(f"  215: pos={p0} |L|={len(L0)} |R|={len(R0)}")
    print(f"  244: pos={p2} |L|={len(L2)} |R|={len(R2)}  (pos +{p2-p0}, dL={len(L2)-len(L0)}, dR={len(R2)-len(R0)})")
    # near-head structure identical?
    print(f"  215 L top12: {L0[-12:]}")
    print(f"  244 L top12: {L2[-12:]}")
    print(f"  215 R near12: {R0[-12:]}")
    print(f"  244 R near12: {R2[-12:]}")


if __name__ == "__main__":
    main()
