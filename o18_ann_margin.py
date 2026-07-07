# o18 ANNEALED MODEL — orbit-margin arm.  Re-runs the TRUE orbit (exact big ints,
# grid-proven transducer T; validity at astronomical m [OBSERVED/exact-fit] as in
# o18_md_orbit.py) with full margin instrumentation:
#   - every pass whose word contains a (1,2) block: escort margin (units immediately
#     left), gap (units) between consecutive 2-blocks, 2-train length;
#   - protected margin of every v=2 (mod 3) block: escort + 2(v-2)/3 (the push-margin
#     credit it would carry if pushed down to an exact 2);
#   - residue histogram of dirty passes (true residues vs the i.i.d.-uniform model);
#   - the orbit margin M = min over the whole run of any 2-block's escort margin.
# EXACT ingredients; the i.i.d. comparison is [MODEL].
import sys
from collections import Counter
sys.set_int_max_str_digits(2_000_000)
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown


def scan(w):
    """(list of (escort, idx) for (1,2) blocks, min protected margin of v=2mod3 blocks,
    min gap between consecutive 2-blocks, max 2-train)."""
    twos = []
    prot = None
    for i, (s, b) in enumerate(w):
        if s == 1 and b == 2:
            m = 0
            k = i - 1
            while k >= 0 and w[k] == (1, 1):
                m += 1
                k -= 1
            twos.append((m, i))
        if s == 1 and b > 2 and b % 3 == 2:
            m = 0
            k = i - 1
            while k >= 0 and w[k] == (1, 1):
                m += 1
                k -= 1
            pm = m + 2 * (b - 2) // 3
            prot = pm if prot is None else min(prot, pm)
    mingap = None
    train = 1 if twos else 0
    for (m1, i1), (m2, i2) in zip(twos, twos[1:]):
        if all(w[k] == (1, 1) for k in range(i1 + 1, i2)):
            gap = i2 - i1 - 1
            mingap = gap if mingap is None else min(mingap, gap)
            if gap == 0:
                train += 1
    return twos, prot, mingap, train


def run(N0=10, budget=200000, report_every=50000):
    state = ('C', N0)
    res_hist = Counter()
    twopass = 0
    minescort = None
    minprot = None
    mingap = None
    maxtrain = 0
    escort_dist = Counter()
    gens = 0
    dirty = 0
    for step in range(budget):
        if state[0] == 'C':
            N = state[1]
            gens += 1
            if N % 3 == 2:
                state = ('D', (8 * N - 25) // 3, ((1, 6),))
            else:
                state = ('C', (8 * N) // 3 + 2)
        else:
            _, m, w = state
            dirty += 1
            r = m % 3
            res_hist[r] += 1
            twos, prot, gap, train = scan(w)
            if twos:
                twopass += 1
                e = min(t[0] for t in twos)
                escort_dist[e] += 1
                minescort = e if minescort is None else min(minescort, e)
            if prot is not None:
                minprot = prot if minprot is None else min(minprot, prot)
            if gap is not None:
                mingap = gap if mingap is None else min(mingap, gap)
            maxtrain = max(maxtrain, train)
            res = T(r, w)
            if res[0] == 'HALT':
                print(f'HALT at step {step} m~1e{len(str(m)) - 1} w={w}')
                return
            if res[0] == 'LAND':
                state = ('C', (8 * m + res[1]) // 3)
            else:
                state = ('D', (8 * m + res[1]) // 3, res[2])
        if (step + 1) % report_every == 0:
            mm = state[1]
            print(f'  step {step + 1}: m~1e{len(str(mm)) - 1}  gens={gens} dirty={dirty} '
                  f'2-passes={twopass} minescort={minescort} minprot={minprot} '
                  f'mingap={mingap} maxtrain={maxtrain}', flush=True)
    tot = sum(res_hist.values())
    print(f'DONE {budget} tower-steps: m ~ 1e{len(str(state[1])) - 1}, '
          f'generations={gens}, dirty passes={dirty}')
    print(f'  dirty-pass residues (true): ' +
          ', '.join(f'{r}: {res_hist[r]} ({res_hist[r]/tot:.4f})' for r in (0, 1, 2)))
    print(f'  passes with a (1,2) block: {twopass}'
          f'  escort-margin dist: {dict(sorted(escort_dist.items()))}')
    print(f'  ORBIT MARGIN M (min escort of any 2-block ever): {minescort}')
    print(f'  min PROTECTED margin of any v=2mod3 block: {minprot}')
    print(f'  min units-gap between consecutive 2-blocks: {mingap}'
          f'   max 2-train: {maxtrain}   (fatality needs gap=0, train>=2, escort<=1)')


if __name__ == '__main__':
    budget = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    run(10, budget)
