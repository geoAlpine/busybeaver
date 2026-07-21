"""Ground truth: run x2 from `init` and locate every M1(g) / M6(g) milestone.

Detection is by CANONICAL config equality (strip far-side blank padding from
both tape lists, ignore absolute pos) -- the pos+boundary-blank normalisation
that the §5am CAVEAT says the canonical families need.  We RECORD the actual
pos and blank padding at each hit, so nothing is assumed.
"""
import sys, time
from x2t7_sim import A, B, C, D, E, F, SNAMES, Cfg, M1, M6


def strip(xs):
    i = len(xs)
    while i > 0 and not xs[i - 1]:
        i -= 1
    return xs[:i]


def chain(maxg, limit):
    # canonical right-tapes of the milestones we hunt (left is blank at both)
    tgt = {}
    for g in range(1, maxg + 1):
        m = M1(g)
        tgt[("M1", g)] = (m.st, tuple(strip(m.lean_right())))
        m = M6(g)
        # M6 has left=[False] -> strips to (); pos -5
        tgt[("M6", g)] = (m.st, tuple(strip(m.lean_right())))
    rev = {}
    for k, v in tgt.items():
        rev.setdefault(v, []).append(k)

    c = Cfg(A, 0, [], False, [])
    L, R = c.L, c.R
    st, h, pos = c.st, c.h, c.pos
    nl = 0
    found = []
    t0 = time.time()
    for i in range(1, limit + 1):
        if st == A:
            nh, ns, dp, right = (True, B, 1, True) if not h else (False, E, 1, True)
        elif st == B:
            if h:
                print(f"HALT at {i}"); return found
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
        # cheap necessary condition: E, head 0, left side entirely blank
        if nl == 0 and st == E and not h:
            key = (st, tuple(strip(R[::-1])))
            names = rev.get(key)
            if names:
                found.append((names, i, pos, len(L), len(R)))
                print(f"  {names}  n={i:>12}  pos={pos:>7}  |leftpad|={len(L):>7} "
                      f" [{time.time()-t0:.0f}s]")
                sys.stdout.flush()
    print(f"  ... ran {limit} steps, {time.time()-t0:.0f}s")
    return found


if __name__ == "__main__":
    maxg = int(sys.argv[1]); lim = int(float(sys.argv[2]))
    print(f"hunting M1(1..{maxg}) and M6(1..{maxg}) from init, limit={lim}")
    f = chain(maxg, lim)
    print("\n=== milestone table ===")
    prev = 0
    for names, n, pos, lp, lr in f:
        print(f"{str(names):>16}  n={n:>12}  delta={n-prev:>12}  pos={pos:>7}  leftpad={lp}")
        prev = n
