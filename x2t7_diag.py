"""Diagnostic: where does the orbit from M6(g) actually go? No target assumed."""
import sys
from x2t7_sim import A, B, C, D, E, F, SNAMES, Cfg, M1, M6
from x2t7_measure import canon, strip


def probe(g, limit):
    c = M6(g)
    L, R = c.L, c.R
    st, h, pos = c.st, c.h, c.pos
    nl = sum(1 for b in L if b)
    minnl = nl
    minnl_at = 0
    minpos, maxpos = pos, pos
    nl0_events = 0
    for i in range(1, limit + 1):
        if st == A:
            nh, ns, dp, right = (True, B, 1, True) if not h else (False, E, 1, True)
        elif st == B:
            if h:
                return dict(halt=i)
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
        if nl < minnl:
            minnl, minnl_at = nl, i
        if nl == 0:
            nl0_events += 1
        if pos < minpos: minpos = pos
        if pos > maxpos: maxpos = pos
    c.st, c.h, c.pos = st, h, pos
    return dict(halt=None, ran=limit, minnl=minnl, minnl_at=minnl_at,
                nl0=nl0_events, minpos=minpos, maxpos=maxpos,
                final_pos=pos, final_st=SNAMES[st], final_nl=nl,
                len_R=len(R), len_L=len(L))


if __name__ == "__main__":
    g = int(sys.argv[1]); lim = int(float(sys.argv[2]))
    print(f"g={g} limit={lim}")
    for k, v in probe(g, lim).items():
        print(f"  {k}: {v}")
    # what does M1(g+1) look like at its left edge?
    t = M1(g + 1)
    print(f"  M1({g+1}): pos={t.pos} left={t.lean_left()[:8]} head={t.h} "
          f"right[:30]={''.join('1' if b else '0' for b in t.lean_right()[:30])}")
    s = M6(g)
    print(f"  M6({g}):   pos={s.pos} left={s.lean_left()[:8]} head={s.h} "
          f"right[:30]={''.join('1' if b else '0' for b in s.lean_right()[:30])}")
