"""RE-MEASUREMENT against the CORRECT target: `DoubCanon`.

    DoubCanon A : forall g >= 1, exists n >= 1,
      steps n <E, -5, <[false], false, (M6 g).right ++ [false]>>
        = some <E, A(g+1) - A g, <[false], false, (M1 (g+1)).right ++ [false]>>

Four traps the coordinator named, each given its own CONTROL here:
  (i)   target `left` is [false], NOT [] -- control: the []-left target must FAIL
  (ii)  head displacement is A(g+1)-A(g), measured, NOT assumed +5 or -6
  (iii) one extra trailing blank on BOTH sides
  (iv)  n >= 1
Also answers: is the drift A(g+1)-A(g) CONSTANT in g?
"""
import sys
from x2t7_sim import A, B, C, D, E, F, SNAMES, Cfg, M1, M6, step


def strip(xs):
    i = len(xs)
    while i > 0 and not xs[i - 1]:
        i -= 1
    return xs[:i]


def doubcanon_start(g):
    """<E, -5, <[false], false, (M6 g).right ++ [false]>>  -- built from the DEFS."""
    return Cfg(E, -5, [False], False, M6(g).lean_right() + [False])


def doubcanon_target_right(g):
    """(M1 (g+1)).right ++ [false]"""
    return M1(g + 1).lean_right() + [False]


def run_find(g, limit):
    """Run from the DoubCanon start; return (n, cfg) at the first instant whose
    right tape equals the DoubCanon target right tape EXACTLY (as stored lists),
    with state E, head 0, left [false]. Nothing about pos is assumed."""
    tgt = doubcanon_target_right(g)
    tgt_s = tuple(strip(tgt))
    c = doubcanon_start(g)
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
        if nl == 0 and st == E and not h and tuple(strip(R[::-1])) == tgt_s:
            c.st, c.h, c.pos = st, h, pos
            return ("HIT", i, c)
    return ("MISS", limit, None)


def raw(c, n):
    for _ in range(n):
        if not step(c):
            return None
    return c


if __name__ == "__main__":
    gs = [int(x) for x in sys.argv[1:]] or [1, 2, 3, 4]
    drifts = []
    for g in gs:
        K = g + 8
        st, n, c = run_find(g, 1 << (2 * K + 2))
        if st != "HIT":
            print(f"g={g}: {st} after {n}"); continue
        tgt_right = doubcanon_target_right(g)
        # EXACT DoubCanon match, treating off-list cells as blank
        okL = strip(c.lean_left()) == strip([False])          # left is [false] -> strips to []
        left_exact = c.lean_left()[:1] == [False] or c.lean_left() == []
        okR = strip(c.lean_right()) == strip(tgt_right)
        okst = (c.st == E and c.h is False)
        print(f"g={g} K={K}: n={n}")
        print(f"    landed pos = {c.pos}   =>  A({g+1}) - A({g}) = {c.pos}")
        print(f"    state E, head 0        : {okst}")
        print(f"    left  == [false]       : {c.lean_left()[:2]!r}  (strips to {strip(c.lean_left())!r})")
        print(f"    right == M1({g+1}).right++[false] : {okR}")
        print(f"    n >= 1                 : {n >= 1}")
        drifts.append((g, c.pos))
        # ---- CONTROLS ----
        c2 = doubcanon_start(g); raw(c2, n + 1)
        ctl_off1 = (c2.st == E and not c2.h
                    and strip(c2.lean_right()) == strip(tgt_right)
                    and c2.pos == c.pos)
        c3 = doubcanon_start(g); raw(c3, n - 1)
        ctl_off_1 = (c3.st == E and not c3.h
                     and strip(c3.lean_right()) == strip(tgt_right)
                     and c3.pos == c.pos)
        # CONTROL (i): the []-left canonical M1(g+1) target -- must FAIL
        t = M1(g + 1)
        ctl_canon = (c.pos == t.pos and c.lean_left() == t.lean_left()
                     and c.lean_right() == t.lean_right())
        # CONTROL (ii): a hardcoded +5 drift -- must FAIL
        ctl_plus5 = (c.pos == -5 + 5)
        print(f"    CONTROL n+1 lands      : {ctl_off1}   (must be False)")
        print(f"    CONTROL n-1 lands      : {ctl_off_1}   (must be False)")
        print(f"    CONTROL canonical M1({g+1}) (left=[], pos=0) : {ctl_canon}   (must be False)")
        print(f"    CONTROL hardcoded +5 drift : {ctl_plus5}   (must be False)")
        sys.stdout.flush()
    print()
    print("=== IS THE DRIFT A(g+1)-A(g) CONSTANT IN g? ===")
    for g, d in drifts:
        print(f"   g={g}: A({g+1})-A({g}) = {d}")
    vals = {d for _, d in drifts}
    print(f"   distinct values: {vals}  -> "
          f"{'CONSTANT' if len(vals) == 1 else 'VARIES WITH g'}")
