#!/usr/bin/env python
"""
Space-time diagrams of Busy Beaver machines — SEE the machine think (no math, just look).

Each row = one time step (top = start, going down = later). Each column = a tape cell.
Black = 1, white = 0, red dot = the head. Champions and 'monsters' draw startlingly
intricate patterns — this is the visual soul of the machines we've been chasing.
"""
from __future__ import annotations

import sys, os, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HALT = {"Z", "H", "-"}


def parse(spec):
    M = {}
    for i, g in enumerate(spec.split("_")):
        st = chr(ord("A") + i); M[st] = {}
        for s in (0, 1):
            t = g[s*3:s*3+3]
            M[st][s] = None if t[2] in HALT else (int(t[0]), t[1], t[2])
    return M


def spacetime(spec, steps, max_rows=1400):
    M = parse(spec)
    # pass 1: span + actual length
    tape = {}; head = 0; st = "A"; lo = hi = 0; n = 0
    for _ in range(steps):
        lo, hi = min(lo, head), max(hi, head)
        t = M[st][tape.get(head, 0)]
        if t is None:
            break
        w, mv, nxt = t; tape[head] = w; head += 1 if mv == "R" else -1; st = nxt; n += 1
    width = hi - lo + 1
    stride = max(1, n // max_rows)
    rows = n // stride + 1
    grid = np.zeros((rows, width), dtype=float)
    headcol = np.full(rows, -1)
    # pass 2: fill
    tape = {}; head = 0; st = "A"; r = 0
    for step in range(n):
        if step % stride == 0 and r < rows:
            for c in range(lo, hi + 1):
                grid[r, c - lo] = tape.get(c, 0)
            hc = head - lo
            if 0 <= hc < width:
                headcol[r] = hc
            r += 1
        t = M[st][tape.get(head, 0)]
        if t is None:
            break
        w, mv, nxt = t; tape[head] = w; head += 1 if mv == "R" else -1; st = nxt
    return grid, headcol, n, width


def plot(spec, steps, title, fname):
    grid, headcol, n, width = spacetime(spec, steps)
    h = grid.shape[0]
    fig, ax = plt.subplots(figsize=(min(12, max(4, width / 60)), min(14, max(4, h / 110))))
    ax.imshow(grid, cmap="binary", aspect="auto", interpolation="nearest")
    ys = np.arange(h)
    ok = headcol >= 0
    ax.scatter(headcol[ok], ys[ok], s=1.2, c="red", linewidths=0)
    ax.set_title(f"{title}\n{spec}\n{n:,} steps shown, tape width {width}", fontsize=9)
    ax.set_xlabel("tape position"); ax.set_ylabel("time (down)")
    out = os.path.join(os.path.dirname(__file__), "figures", fname)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    plt.tight_layout(); plt.savefig(out, dpi=130); plt.close(fig)
    print(f"saved {out}  ({n:,} steps, width {width})")


def main():
    plot("1RB1LB_1LA0LC_1RZ1LD_1RD0RA", 200, "BB(4) champion (halts at 107)", "bb_st_bb4.png")
    plot("1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA", 12_000, "BB(5) champion (first steps of its 47M)", "bb_st_bb5.png")
    plot("1RB1RC_1LC0LZ_0RA0LB", 6_000, "a BOUNCER monster (two-sided growth)", "bb_st_bouncer.png")
    plot("1RB1LA_0LA0RB_0LA0LZ", 40_000, "a COUNTER monster (logarithmic creep)", "bb_st_counter.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
