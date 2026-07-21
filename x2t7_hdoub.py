"""Is `h_doub` TRUE as literally stated on the §5am canonical families?

Runs from the CANONICAL M6(g) (pos -5, left=[False]) and reports the exact
config reached at the M1(g+1) shape: pos, left padding, and whether full Cfg
equality with `M1 (g+1)` holds.
"""
import sys
from x2t7_sim import A, B, C, D, E, F, SNAMES, Cfg, M1, M6
from x2t7_chain import strip


def run_to_shape(g, limit):
    tgt = M1(g + 1)
    tshape = (tgt.st, tuple(strip(tgt.lean_right())))
    c = M6(g)
    L, R = c.L, c.R
    st, h, pos = c.st, c.h, c.pos
    nl = sum(1 for b in L if b)
    for i in range(1, limit + 1):
        if st == A:
            nh, ns, dp, right = (True, B, 1, True) if not h else (False, E, 1, True)
        elif st == B:
            if h: return ("HALT", i, None)
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
            if nh: nl += 1
            h = R.pop() if R else False
        else:
            R.append(nh)
            if L:
                h = L.pop()
                if h: nl -= 1
            else:
                h = False
        st = ns; pos += dp
        if nl == 0 and st == E and not h and (st, tuple(strip(R[::-1]))) == tshape:
            c.st, c.h, c.pos = st, h, pos
            return ("HIT", i, c)
    return ("MISS", limit, None)


if __name__ == "__main__":
    for g in [int(x) for x in sys.argv[1:]]:
        K = g + 8
        st, n, c = run_to_shape(g, 1 << (2 * K + 2))
        if st != "HIT":
            print(f"g={g}: {st} after {n}")
            continue
        t = M1(g + 1)
        exact = (c.st == t.st and c.pos == t.pos
                 and c.lean_left() == t.lean_left()
                 and c.h == t.h and c.lean_right() == t.lean_right())
        print(f"g={g} K={K}: shape reached at n={n}")
        print(f"    reached : pos={c.pos:>4}  left={c.lean_left()[:6]}  "
              f"|right|={len(c.R)}")
        print(f"    M1({g+1}) : pos={t.pos:>4}  left={t.lean_left()[:6]}  "
              f"|right|={len(t.R)}")
        print(f"    EXACT Cfg equality (h_doub as literally stated): {exact}")
        print(f"    equality after pos-shift {t.pos - c.pos:+d} and blank-trim: "
              f"{strip(c.lean_left()) == strip(t.lean_left()) and strip(c.lean_right()) == strip(t.lean_right()) and c.st == t.st and c.h == t.h}")
        sys.stdout.flush()
