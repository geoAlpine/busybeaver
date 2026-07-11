#!/usr/bin/env python3
"""x2co_trace.py -- extract the DOUBLING-PHASE episode chain of M6(g)->M1(g+1).

Runs the certified executor from M1(g); the trace's milestones (after the first
m.step) are M2,M3,M4,M5,M6,M1(g+1) -- so the DOUBLING phase is between the 5th
milestone (=M6(g)) and the 6th (=M1(g+1)).  During that phase we log a COMPRESSED
signature stream: collapse consecutive identical shape-signatures (state + run-pattern
skeleton, counts abstracted), and annotate each macro-rule fired.  This reveals the
episode structure compactly and lets us compare across g for uniformity.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2cc_symb import Config, Machine, Split, Halted, E
from x2cc_faith import T
from x2cc_gencheck import m1_spec


def sig(cfg):
    def rr(runs):
        return tuple((p if (c.is_const() and c.c == 1) else p + '*') for p, c in runs)
    # only keep the head-local window: last 3 left runs, first 6 right runs
    L = rr(cfg.left)[-3:]
    R = rr(cfg.right)[:6]
    return (cfg.state, L, R)


def is_milestone(cfg):
    if cfg.state != 'E' or not cfg.right or cfg.right[0][0][0] != '0':
        return False
    return not any('1' in p and cn.ge(1) is not False for p, cn in cfg.left)


def trace_gen(g, max_ops=3_000_000):
    start = Config([], 'E', T(m1_spec(g)))
    m = Machine(start, guard_r=False)
    miles = 0
    m.step()
    op = 0
    in_doubling = False
    stream = []       # compressed (macrokind, sig) with run-length
    macrocount = {'R': 0, 'L': 0, 'D': 0, 'm': 0}
    while op < max_ops:
        op += 1
        c = m.cfg
        if is_milestone(c):
            miles += 1
            if miles == 5:
                in_doubling = True
                stream.append(('M6', str(c)[:100]))
            elif miles == 6:
                stream.append(('M1next', str(c)[:100]))
                break
            elif in_doubling:
                stream.append(('MILE', str(c)[:100]))
        which = None
        try:
            if m.try_R_cycle():
                which = 'R'
            elif m.try_L_cycle():
                which = 'L'
            elif m.try_D_loop():
                which = 'D'
            else:
                m.micro()
                which = 'm'
        except (Split, Halted) as e:
            stream.append(('STOP', f"{type(e).__name__}: {e}"[:90]))
            break
        if in_doubling:
            macrocount[which] += 1
            s = sig(m.cfg)
            if which != 'm':  # log every macro
                stream.append((which, s))
    return stream, m.events, macrocount


def compress(stream):
    """collapse consecutive equal (kind,sig) into (kind,sig,count)."""
    out = []
    for item in stream:
        if item[0] in ('M6', 'M1next', 'MILE', 'STOP'):
            out.append(item)
            continue
        if out and isinstance(out[-1], tuple) and len(out[-1]) == 3 and out[-1][0] == item[0] and out[-1][1] == item[1]:
            out[-1] = (item[0], item[1], out[-1][2] + 1)
        else:
            out.append((item[0], item[1], 1))
    return out


if __name__ == "__main__":
    g = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    stream, events, mc = trace_gen(g)
    cs = compress(stream)
    print(f"=== g={g} DOUBLING phase (M6 -> M1(g+1)) compressed episode stream ===")
    for item in cs:
        if item[0] in ('M6', 'M1next', 'MILE', 'STOP'):
            print(f"  [{item[0]}] {item[1]}")
        else:
            kind, s, cnt = item
            st, Lw, Rw = s
            print(f"    {kind}x{cnt:<5} [{st}] L={Lw} R={Rw}")
    gaps = sorted(ev[2].c for ev in events if ev[1] == 'gap' and ev[2].c >= 3)
    n2 = sum(1 for ev in events if ev[1] == 'gap' and ev[2].c == 2)
    print(f"  macro counts: {mc}")
    print(f"  gaps>=3: {gaps}  L2count: {n2}")
