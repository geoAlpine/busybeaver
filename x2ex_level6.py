#!/usr/bin/env python3
"""x2ex_level6.py -- locate the level-6 EXIT (CORE = sweepEF62) and extract its
terminal glue for a 4th data point on TERM(k)=2^{k+1}+k+5.  Also verify the two
identical 144-step S-blocks in EXIT(5) diverge only at the terminal.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def left_solid(sim):
    L = sim.L; i = 0
    while i < len(L) and L[-1 - i] == 1:
        i += 1
    return i


def scan_anchors(cap):
    sim = build(2); sim.step()
    A = []
    while sim.n < cap:
        if sim.st == 'E' and sim.h == 0:
            A.append((sim.n, left_solid(sim), sim.left_ones()))
        if not sim.step():
            break
    return A


def find_cores(A):
    """maximal gap==2 lsolid+2 chains -> (m, start_n, end_n)."""
    chains = []
    i = 0; N = len(A)
    while i < N-1:
        if A[i+1][0]-A[i][0] == 2 and A[i+1][1] == A[i][1]+2:
            k = i
            while k < N-1 and A[k+1][0]-A[k][0] == 2 and A[k+1][1] == A[k][1]+2:
                k += 1
            m = (A[k][0]-A[i][0])//2
            chains.append((m, A[i][0], A[k][0]))
            i = k
        else:
            i += 1
    return chains


def carry_end_after(core_end, A):
    """the level's carry ends at the next milestone-like anchor with lsolid==0
    following a big lones drop; heuristically the next anchor whose lones drops
    by >= the block laid.  We just return the next anchor where the following
    gap is 'large' then lsolid resets deep -- simpler: return the anchor whose
    lones is a local min after a big terminal gap.  We instead find the biggest
    gap after core_end up to the next CORE and treat its end as carry end."""
    # find anchors after core_end
    idx = next(i for i, a in enumerate(A) if a[0] == core_end)
    # walk until next big-core start; the carry end = last anchor before lsolid
    # jumps to a big value again (next level's fold peak).  Return the anchor
    # right after the maximal terminal gap.
    best_gap = 0; best_end = None
    i = idx
    while i < len(A)-1:
        g = A[i+1][0]-A[i][0]
        if g > 300:   # next-level structure; stop
            break
        if g > best_gap:
            best_gap = g; best_end = A[i+1][0]
        i += 1
    return best_end, best_gap


def main():
    A = scan_anchors(20000)
    chains = find_cores(A)
    print("cores (m, start, end) with m in [4,70]:")
    seen = {}
    for m, s, e in chains:
        if 4 <= m <= 70:
            seen.setdefault(m, (s, e))
    for m in sorted(seen):
        print(f"   sweepEF{m:<3} core ends n={seen[m][1]}")
    # level j core m = 2^j-2 : j=3->6, 4->14, 5->30, 6->62
    print("\nEXIT terminals (block-final gap) per level:")
    TERM = lambda k: 2**(k+1)+k+5
    for j in (3, 4, 5, 6):
        m = 2**j - 2
        if m not in seen:
            print(f"   j={j} sweepEF{m}: NOT reached in scan window")
            continue
        core_end = seen[m][1]
        cend, gap = carry_end_after(core_end, A)
        print(f"   j={j}: CORE sweepEF{m} ends {core_end}, EXIT=[{core_end},{cend}] "
              f"len={cend-core_end if cend else '?'}, terminal gap={gap}, "
              f"predicted TERM(k={j+1})={TERM(j+1)}  match={gap==TERM(j+1)}")


if __name__ == "__main__":
    main()
