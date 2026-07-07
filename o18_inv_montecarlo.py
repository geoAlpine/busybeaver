# o18 INVARIANT SYNTHESIS step 4: QUANTIFICATION under the null model.
# The witness (o18_inv_witness_verify.py) shows fatality is adversarially reachable from
# the exit cone; safety of the true orbit can therefore only be an ARITHMETIC property of
# its 3-adic itinerary.  The community's "probviously halting" heuristic models the
# itinerary as uniform random residues.  Here we measure that null model exactly on the
# word dynamics: from each exit product, run passes with i.i.d. uniform residues r in
# {0,1,2} until LAND (excursion ends, clean reset) or HALT; estimate
#     p_halt = P[an exit excursion ends in HALT rather than LAND].
# The true orbit performs one such excursion per generation (~122k so far); under the
# null model the orbit halts a.s. with expected ~1/p_halt generations between hits.
import sys, random
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown

def excursion(w, rng, maxpass=100000):
    n = 0
    while True:
        r = rng.randrange(3)
        try:
            res = T(r, w)
        except Unknown:
            return ('UNK', n)
        n += 1
        if res[0] == 'LAND':
            return ('LAND', n)
        if res[0] == 'HALT':
            return ('HALT', n)
        w = res[2]
        if n >= maxpass:
            return ('OVER', n)

if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 2026
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
    rng = random.Random(seed)
    starts = [((1, 2 * t + 2), (1, 6)) for t in (1, 2, 3, 4, 7, 10, 25, 100)]
    starts.append(((1, 4), (1, 1), (1, 1), (1, 1)))
    from collections import Counter
    tot = Counter()
    lens = []
    halt_lens = []
    for i in range(N):
        w = starts[i % len(starts)]
        kind, n = excursion(w, rng)
        tot[kind] += 1
        lens.append(n)
        if kind == 'HALT':
            halt_lens.append(n)
    print(f'excursions: {N}  outcomes: {dict(tot)}')
    p = tot['HALT'] / N
    print(f'p_halt per excursion (uniform-residue null model): {p:.6f}'
          + (f'  (~1 in {round(1/p)})' if p else ''))
    lens.sort()
    print(f'excursion length quartiles: {lens[N//4]}, {lens[N//2]}, {lens[3*N//4]}, max {lens[-1]}')
    if halt_lens:
        halt_lens.sort()
        print(f'halting-excursion lengths: min {halt_lens[0]}, median {halt_lens[len(halt_lens)//2]}, max {halt_lens[-1]}')
    if tot['UNK']:
        print(f'NOTE: {tot["UNK"]} excursions hit Unknown transducer cells (unpinned deep R1) -- excluded from p.')
    # under the null model: orbit halts a.s.; expected generations to halt ~ 1/p
    if p:
        print(f'null-model expectation: halt after ~{round(1/p)} generations; the true orbit has '
              f'done 122,015 clean generations (evidence the true itinerary is NOT null / or luck '
              f'p={ (1-p)**122015 :.3g}).')
