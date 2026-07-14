#!/usr/bin/env python3
"""x2cu_decompose.py -- THE DECISIVE EXPERIMENT.

For each block-doubling carry (5->13, 13->29, 29->61) decompose the interior at
E-on-0 anchors and CLASSIFY every inter-anchor gap as one of the ==parametric==
families (matched to a proven Lean lemma) or as residual GLUE:

  * 'fold'   gap=6, block->comb (blk-=2, comb+=1): the descent block->comb fold.
  * 'ntick'  gap=4t+10 (t = left solid block, ODD): outer_tick_noCarry (PROVEN forall t).
             A maximal arithmetic run of these = outer_tick_noCarry_run (PROVEN forall n).
  * 'core'   a maximal gap=2 E-on-0 chain that builds 1^{2m} on the left: sweepEF m (CORE).
  * 'carry'  a recognized embedded lower carry sub-window (5->13 or 13->29).
  * 'glue'   anything else (gap 3, 7, 15, 24, ...): candidate CONSTANT connector.

Then we print, per carry, the GLUE events with their local cell context (state
sequence + left/right run tokens at the boundary), so the glue cell-patterns can be
compared cell-for-cell across levels.  The head EXCURSION (bounded window) confirms
tail-parametricity.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def right_first_block(sim):
    seq = [sim.h] + sim.R[::-1]
    i = 0
    while i < len(seq) and seq[i] == 0:
        i += 1
    j = i
    while j < len(seq) and seq[j] == 1:
        j += 1
    return j - i


def left_comb_pairs(sim):
    L = sim.L
    n = len(L)
    pairs = 0
    i = 0
    while i + 1 < n and L[-1 - i] != L[-1 - (i + 1)]:
        pairs += 1
        i += 2
    return pairs


def left_solid(sim):
    # length of leading 1-run on the left stack (nearest-first)
    L = sim.L
    i = 0
    while i < len(L) and L[-1 - i] == 1:
        i += 1
    return i


def runs(seq, k):
    out = []
    i = 0
    while i < len(seq) and len(out) < k:
        b = seq[i]
        j = i
        while j < len(seq) and seq[j] == b:
            j += 1
        out.append((b, j - i))
        i = j
    return out


def snap(sim):
    return dict(n=sim.n, st=sim.st, pos=sim.pos, h=sim.h,
                blk=right_first_block(sim), comb=left_comb_pairs(sim),
                lsolid=left_solid(sim),
                lt=runs([sim.L[-1 - i] for i in range(len(sim.L))], 6),
                rt=runs([sim.h] + sim.R[::-1], 6))


def collect_anchors(n0, n1):
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


def classify(A, sub_carries):
    """Return a segment list. sub_carries = list of (start_n, end_n, label)."""
    segs = []
    i = 0
    N = len(A)
    def in_subcarry(n):
        for (s, e, lab) in sub_carries:
            if s <= n < e:
                return (s, e, lab)
        return None
    while i < N - 1:
        a = A[i]; b = A[i + 1]
        sc = in_subcarry(a['n'])
        if sc and a['n'] == sc[0]:
            # jump to the anchor at/after sc end
            j = i
            while j < N and A[j]['n'] < sc[1]:
                j += 1
            segs.append(('CARRY', sc[2], a['n'], A[min(j, N-1)]['n']))
            i = j
            continue
        gap = b['n'] - a['n']
        # core: a maximal run of gap==2 with comb building 1^{2m} (lsolid grows by 2)
        if gap == 2 and b['lsolid'] == a['lsolid'] + 2:
            j = i
            while j < N - 1 and A[j+1]['n'] - A[j]['n'] == 2 \
                    and A[j+1]['lsolid'] == A[j]['lsolid'] + 2:
                j += 1
            m = (A[j]['n'] - A[i]['n']) // 2
            segs.append(('CORE', f'sweepEF {m}', A[i]['n'], A[j]['n']))
            i = j
            continue
        # ntick run: consecutive gaps of form 4t+10 (t odd), arithmetic
        if gap >= 14 and (gap - 10) % 4 == 0:
            j = i
            cnt = 0
            while j < N - 1:
                g = A[j+1]['n'] - A[j]['n']
                if g >= 14 and (g - 10) % 4 == 0:
                    j += 1; cnt += 1
                else:
                    break
            if cnt >= 1:
                ts = [(A[k+1]['n'] - A[k]['n'] - 10)//4 for k in range(i, j)]
                segs.append(('NTICK_RUN', f'{cnt} ticks t={ts}', A[i]['n'], A[j]['n']))
                i = j
                continue
        # fold run: consecutive gap==6, blk-=2 comb+=1
        if gap == 6:
            j = i
            while j < N - 1 and A[j+1]['n'] - A[j]['n'] == 6:
                j += 1
            segs.append(('FOLD_RUN', f'{j-i} folds', A[i]['n'], A[j]['n']))
            i = j
            continue
        # else glue
        segs.append(('GLUE', f'gap{gap}', a['n'], b['n']))
        i += 1
    return segs


def excursion(n0, n1):
    sim = build(2); sim.step()
    while sim.n < n0:
        assert sim.step()
    base = sim.pos
    lo = hi = sim.pos
    while sim.n < n1:
        assert sim.step()
        lo = min(lo, sim.pos); hi = max(hi, sim.pos)
    return lo - base, hi - base, base


CARRIES = {
    'C3(5->13)':  (6591, 6708, []),
    'C4(13->29)': (6484, 7141, [(6591, 6708, 'C3')]),
    'C5(29->61)': (6397, 8798, [(6484, 7141, 'C4')]),
}


def main():
    for name, (n0, n1, subs) in CARRIES.items():
        A = collect_anchors(n0, n1)
        segs = classify(A, subs)
        lo, hi, base = excursion(n0, n1)
        print(f"\n===== {name}  n=[{n0},{n1}]  {n1-n0} steps  "
              f"excursion rel[{lo},{hi}] (base pos {base}) =====")
        for kind, info, a, bb in segs:
            print(f"   {a:<6}->{bb:<6} ({bb-a:>4}s)  {kind:<10} {info}")
        # summarize glue
        glue = [(a, bb, info) for (k, info, a, bb) in segs if k == 'GLUE']
        gtot = sum(bb - a for (a, bb, i) in glue)
        print(f"   -- GLUE total = {gtot} steps in {len(glue)} events; "
              f"glue gaps = {[bb-a for (a,bb,i) in glue]}")


if __name__ == "__main__":
    main()
