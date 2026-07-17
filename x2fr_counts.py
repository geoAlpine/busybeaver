#!/usr/bin/env python3
"""x2fr_counts.py -- lightweight (no full-vector) exact counts of chew-starts and
carries for larger g (K).  Reuses the ripple_probe carry definition (=192/386 GT)
and the chew_start local-max definition (=3852/9729 GT)."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
from x2bd_outer import right_first_block, left_comb_pairs


def counts(g):
    sim = build(g); sim.step()
    miles = 0
    starts = []       # (blk, comb)
    while True:
        if sim.is_milestone():
            miles += 1
            if miles == 6: break
        if miles >= 5 and sim.st == 'E' and sim.h == 0:
            starts.append((right_first_block(sim), left_comb_pairs(sim)))
        if not sim.step():
            break
    # chew-starts = local maxima of blk with blk>=5
    cs = []
    for i in range(len(starts)):
        blk = starts[i][0]
        p = starts[i-1][0] if i > 0 else -1
        nx = starts[i+1][0] if i+1 < len(starts) else -1
        if blk >= 5 and blk > p and blk >= nx:
            cs.append(starts[i])
    # carries = up-regenerations (ripple), counting depth
    ncarry = 0
    depths = {}
    i = 0
    while i < len(cs):
        if i > 0 and cs[i][0] > cs[i-1][0]:
            d = 1; j = i
            while j+1 < len(cs) and cs[j+1][0] > cs[j][0]:
                d += 1; j += 1
            depths[d] = depths.get(d,0)+1
            ncarry += d
            i = j+1
        else:
            i += 1
    # comb profile over CHEW-STARTS (`cs`), NOT over carries -- the carries are the
    # separate depths/ncarry loop above.  MISLABELLED "comb-at-carry" until 2026-07-17.
    # NB the `c > 0` filter DROPS the comb=0 bucket (64 events at K=10).
    from collections import Counter
    combhist = Counter(c for b,c in cs if c > 0)
    return len(cs), ncarry, depths, dict(sorted(combhist.items()))


def blk_dist(g):
    sim = build(g); sim.step()
    miles = 0
    starts = []
    while True:
        if sim.is_milestone():
            miles += 1
            if miles == 6: break
        if miles >= 5 and sim.st == 'E' and sim.h == 0:
            starts.append((right_first_block(sim), left_comb_pairs(sim)))
        if not sim.step():
            break
    cs = []
    for i in range(len(starts)):
        blk = starts[i][0]
        p = starts[i-1][0] if i > 0 else -1
        nx = starts[i+1][0] if i+1 < len(starts) else -1
        if blk >= 5 and blk > p and blk >= nx:
            cs.append(starts[i])
    from collections import Counter
    return Counter(b for b,_ in cs), len(cs)


if __name__ == "__main__":
    g = int(sys.argv[1])
    if len(sys.argv) > 2 and sys.argv[2] == 'dist':
        import pickle
        dist, T = blk_dist(g)
        SP = '/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/8b7a3f39-ce4e-4044-afe8-60ce3b3aedcf/scratchpad'
        with open(f'{SP}/dist_g{g}.pkl','wb') as f:
            pickle.dump(dict(dist), f)
        print(f"g={g} K={g+8}: T={T}, dist saved ({len(dist)} distinct blocks)")
    else:
        T, C, depths, combhist = counts(g)
        print(f"g={g} K={g+8}: chew-starts T={T}  carries C={C}  ripple-depths={depths}")
        print(f"  comb-at-carry hist={combhist}")
