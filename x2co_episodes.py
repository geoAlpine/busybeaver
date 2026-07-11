#!/usr/bin/env python3
"""x2co_episodes.py -- the DOUBLING-phase EPISODE CHAIN, boundaries only.

Print a line only when the local shape-signature CHANGES (an episode boundary),
with the running macro-op count and the full head-local config, so the episode
chain is compact.  Compare across g for uniformity."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2cc_symb import Config, Machine, Split, Halted, E
from x2cc_faith import T
from x2cc_gencheck import m1_spec


def sig(cfg):
    def rr(runs):
        return tuple((p if (c.is_const() and c.c == 1) else p + '*') for p, c in runs)
    return (cfg.state, rr(cfg.left)[-2:], rr(cfg.right)[:5])


def is_milestone(cfg):
    if cfg.state != 'E' or not cfg.right or cfg.right[0][0][0] != '0':
        return False
    return not any('1' in p and cn.ge(1) is not False for p, cn in cfg.left)


def loc(cfg, nl=2, nr=6):
    def rr(runs):
        return ' '.join(f"{p}^{c}" if not (c.is_const() and c.c == 1) else p for p, c in runs)
    return f"...{rr(cfg.left[-nl:])} [{cfg.state}] {rr(cfg.right[:nr])}..."


def run(g, max_ops=5_000_000):
    m = Machine(Config([], 'E', T(m1_spec(g))), guard_r=False)
    miles = 0
    m.step()
    indb = False
    prev = None
    op = 0
    boundaries = []
    nmacro = 0
    seg_start = 0
    while op < max_ops:
        op += 1
        c = m.cfg
        if is_milestone(c):
            miles += 1
            if miles == 5:
                indb = True
                boundaries.append(('=M6=', nmacro, loc(c, 1, 8)))
                prev = None
            elif miles == 6:
                boundaries.append(('=M1n=', nmacro, loc(c, 1, 8)))
                break
            elif indb:
                boundaries.append(('MILE', nmacro, loc(c, 1, 8)))
        try:
            fired = ('R' if m.try_R_cycle() else 'L' if m.try_L_cycle()
                     else 'D' if m.try_D_loop() else None)
            if fired is None:
                m.micro()
                fired = 'm'
        except (Split, Halted) as e:
            boundaries.append(('STOP', nmacro, f"{type(e).__name__}: {e}"[:90]))
            break
        if indb:
            if fired != 'm':
                nmacro += 1
            s = sig(m.cfg)
            if s != prev:
                boundaries.append((fired, nmacro - seg_start, loc(m.cfg)))
                seg_start = nmacro
                prev = s
    return boundaries


if __name__ == "__main__":
    for g in [int(x) for x in (sys.argv[1:] or ['3', '4'])]:
        print(f"\n===================== g={g} =====================")
        bs = run(g)
        print(f"  ({len(bs)} episode boundaries)")
        for kind, n, txt in bs:
            print(f"  [{kind:>5} +{n:<4}] {txt}")
