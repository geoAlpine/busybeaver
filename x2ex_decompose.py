#!/usr/bin/env python3
"""x2ex_decompose.py -- THE DECISIVE EXIT decomposition.

Extract the carry EXIT at three levels cell-for-cell from the faithful build(2)
orbit and decompose EACH at its E-on-0 anchors into proven-piece instances
(sweepEF m / fold / ntick / glue).  Then answer the crux:

  Is EXIT(j) a forall-j PARAMETRIC straight-line composite (same piece-type
  sequence, lengths a closed formula in j), or does the piece-SEQUENCE itself
  grow/nest with j (non-parametric, a well-founded recursion)?

Windows (CORE = the biggest sweepEF; EXIT = [core_end, carry_end]):
  EXIT(3) = [6638, 6708]  (70 steps)   CORE sweepEF 6  ended 6638
  EXIT(4) = [6923, 7141]  (218 steps)  CORE sweepEF 14 ended 6923
  EXIT(5) = [8076, 8798]  (722 steps)  CORE sweepEF 30 ended 8076
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build

EXITS = {3: (6638, 6708), 4: (6923, 7141), 5: (8076, 8798)}


def left_solid(sim):
    L = sim.L; i = 0
    while i < len(L) and L[-1 - i] == 1:
        i += 1
    return i


def snap(sim):
    return dict(n=sim.n, st=sim.st, pos=sim.pos, h=sim.h, lsolid=left_solid(sim))


def anchors(n0, n1):
    sim = build(2); sim.step()
    while sim.n < n0:
        assert sim.step()
    A = []
    while sim.n <= n1:
        if sim.st == 'E' and sim.h == 0:
            A.append(snap(sim))
        if not sim.step():
            break
    return A


def classify(A):
    """Return list of (kind, info, a_n, b_n)."""
    segs = []
    i = 0; N = len(A)
    while i < N - 1:
        a = A[i]; b = A[i + 1]
        gap = b['n'] - a['n']
        # CORE: maximal gap==2 chain, lsolid grows by 2 each (builds 1^{2m})
        if gap == 2 and b['lsolid'] == a['lsolid'] + 2:
            j = i
            while j < N - 1 and A[j + 1]['n'] - A[j]['n'] == 2 \
                    and A[j + 1]['lsolid'] == A[j]['lsolid'] + 2:
                j += 1
            m = (A[j]['n'] - A[i]['n']) // 2
            segs.append(('CORE', f'sweepEF{m}', A[i]['n'], A[j]['n'])); i = j; continue
        # NTICK run: gaps of form 4t+10
        if gap >= 14 and (gap - 10) % 4 == 0:
            j = i; cnt = 0
            while j < N - 1:
                g = A[j + 1]['n'] - A[j]['n']
                if g >= 14 and (g - 10) % 4 == 0:
                    j += 1; cnt += 1
                else:
                    break
            if cnt >= 1:
                ts = [(A[k + 1]['n'] - A[k]['n'] - 10) // 4 for k in range(i, j)]
                segs.append(('NTICK', f't={ts}', A[i]['n'], A[j]['n'])); i = j; continue
        # FOLD run: gap==6
        if gap == 6:
            j = i
            while j < N - 1 and A[j + 1]['n'] - A[j]['n'] == 6:
                j += 1
            segs.append(('FOLD', f'{j - i}folds', A[i]['n'], A[j]['n'])); i = j; continue
        segs.append(('GLUE', f'g{gap}', a['n'], b['n'])); i += 1
    return segs


def token_seq(segs):
    """compact piece-type token sequence for comparison."""
    out = []
    for k, info, a, b in segs:
        if k == 'CORE':
            out.append(info)          # sweepEFm
        elif k == 'FOLD':
            out.append(info)          # Nfolds
        elif k == 'NTICK':
            out.append(f'NTICK{info}')
        else:
            out.append(info)          # gN
    return out


def verbatim_trace(n0, n1):
    """(state, head, delta-pos) trace over the window -- the self-embedding fingerprint."""
    sim = build(2); sim.step()
    while sim.n < n0:
        assert sim.step()
    base = sim.pos
    tr = []
    while sim.n < n1:
        tr.append((sim.st, sim.h, sim.pos - base))
        assert sim.step()
    return tr


def occurs(needle, hay):
    """does needle (list) occur as contiguous sublist of hay?"""
    n, h = len(needle), len(hay)
    for s in range(h - n + 1):
        if hay[s:s + n] == needle:
            return s
    return -1


def main():
    print("=" * 78)
    print("PER-LEVEL EXIT PIECE DECOMPOSITION (at E-on-0 anchors)")
    print("=" * 78)
    decomps = {}
    for j, (a, b) in EXITS.items():
        A = anchors(a, b)
        segs = classify(A)
        decomps[j] = segs
        print(f"\n--- EXIT({j}) = [{a},{b}]  {b - a} steps  ({len(segs)} pieces) ---")
        for k, info, s, e in segs:
            print(f"   {s:<6}->{e:<6} ({e - s:>4}s)  {k:<6} {info}")

    print("\n" + "=" * 78)
    print("TOKEN SEQUENCES (piece-type, side by side)")
    print("=" * 78)
    for j in (3, 4, 5):
        print(f"\nEXIT({j}): " + "  ".join(token_seq(decomps[j])))

    print("\n" + "=" * 78)
    print("HYPOTHESIS 1: is EXIT(j) a VERBATIM copy embedded in EXIT(j+1)?")
    print("  (main-loop claim: NO).  (state,head,dpos) trace containment test:")
    print("=" * 78)
    t3 = verbatim_trace(*EXITS[3])
    t4 = verbatim_trace(*EXITS[4])
    t5 = verbatim_trace(*EXITS[5])
    print(f"  EXIT(3) trace ({len(t3)}) in EXIT(4) ({len(t4)})? idx={occurs(t3, t4)}")
    print(f"  EXIT(4) trace ({len(t4)}) in EXIT(5) ({len(t5)})? idx={occurs(t4, t5)}")
    print(f"  EXIT(3) trace ({len(t3)}) in EXIT(5) ({len(t5)})? idx={occurs(t3, t5)}")

    print("\n" + "=" * 78)
    print("HYPOTHESIS 2: is EXIT(j) piece-token-sequence PARAMETRIC in j?")
    print("  compare token sequences across levels (prefix / suffix / nesting)")
    print("=" * 78)
    tk3, tk4, tk5 = (token_seq(decomps[j]) for j in (3, 4, 5))
    # longest common prefix
    def lcp(x, y):
        i = 0
        while i < min(len(x), len(y)) and x[i] == y[i]:
            i += 1
        return i
    print(f"  |EXIT3|={len(tk3)} |EXIT4|={len(tk4)} |EXIT5|={len(tk5)} tokens")
    print(f"  lcp(EXIT3,EXIT4)={lcp(tk3, tk4)}  lcp(EXIT4,EXIT5)={lcp(tk4, tk5)}")
    # does EXIT4 token seq contain EXIT3 token seq?
    print(f"  EXIT3 tokens sublist of EXIT4? idx={occurs(tk3, tk4)}")
    print(f"  EXIT4 tokens sublist of EXIT5? idx={occurs(tk4, tk5)}")


if __name__ == "__main__":
    main()
