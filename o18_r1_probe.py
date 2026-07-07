# o18 R1-PINNING step 2: resolve every adversarially-reachable Unknown cell of T by
# CONCRETE probing (fresh simulation of the actual machine), >=3 magnitudes of m per cell,
# with per-cell (m mod 3, w)-determinism check (kind, constant c, exact rewrite w' must
# agree at every magnitude).  Prediction-free: this script never consults T.
import sys, pickle
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_probe import probe, wstr

SCR = '/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/8b7a3f39-ce4e-4044-afe8-60ce3b3aedcf/scratchpad'
IN = sys.argv[1] if len(sys.argv) > 1 else SCR + '/o18_r1_unknowns.pkl'
OUT = sys.argv[2] if len(sys.argv) > 2 else SCR + '/o18_r1_probed.pkl'

# 4 magnitudes per residue class (m ~ 40 / 100 / 300 / 1000), m mod 3 = r
MAGS = {0: (42, 102, 303, 1002), 1: (40, 100, 301, 1000), 2: (41, 101, 302, 1001)}

def probe_cell(r, w, mags=None):
    """Concrete outcome of one pass on (m=r mod 3, w) at 4 magnitudes.
    Returns ('HALT',) | ('LAND', c) | ('MOVE', c, w2) if deterministic, else ('SPLIT', outs)."""
    outs = []
    for m in (mags or MAGS[r]):
        kind, out, s, unsafe = probe(m, w, maxF=24)
        if kind == 'HALT':
            outs.append(('HALT',))
        elif kind == 'LAND':
            outs.append(('LAND', 3 * out - 8 * m))
        elif kind == 'MOVE':
            m2, w2 = out
            outs.append(('MOVE', 3 * m2 - 8 * m, w2))
        else:
            outs.append((kind, out))
        # unsafe on a non-halting pass would be a gate violation: flag loudly
        if unsafe and kind != 'HALT':
            outs.append(('UNSAFE-NONHALT', m, kind))
    if all(o == outs[0] for o in outs[1:]):
        return outs[0]
    return ('SPLIT', tuple(outs))

if __name__ == '__main__':
    with open(IN, 'rb') as f:
        data = pickle.load(f)
    unks = data['unks']
    cells = sorted(set((r, w) for r, w, _ in unks))
    tag_of = {(r, w): (t if isinstance(t, str) else t[0]) for r, w, t in unks}
    print(f'{len(unks)} Unknown cell instances, {len(cells)} distinct (r,w) cells; '
          f'probing 4 magnitudes each', flush=True)
    res = {}
    splits, halts, moves, lands, other = [], [], 0, 0, []
    from multiprocessing import Pool
    with Pool(8) as pool:
        outs = pool.starmap(probe_cell, cells, chunksize=4)
    for i, ((r, w), out) in enumerate(zip(cells, outs)):
        res[(r, w)] = out
        if out[0] == 'SPLIT':
            splits.append((r, w, out))
        elif out[0] == 'HALT':
            halts.append((r, w))
        elif out[0] == 'MOVE':
            moves += 1
        elif out[0] == 'LAND':
            lands += 1
        else:
            other.append((r, w, out))
    print(f'\nRESULTS over {len(cells)} cells (each at 4 magnitudes, deterministic unless SPLIT):')
    print(f'  MOVE (deterministic rewrite): {moves}')
    print(f'  LAND: {lands}')
    print(f'  HALT (fatal cells!): {len(halts)}')
    for h in halts:
        print('    FATAL', h[0], wstr(h[1]))
    print(f'  SPLITs (determinism violations!): {len(splits)}')
    for s in splits[:10]:
        print('    SPLIT', s)
    print(f'  other/unparsed: {len(other)}')
    for o in other[:10]:
        print('    OTHER', o)
    # census by raise-site tag x outcome kind
    from collections import Counter
    cen = Counter()
    for (r, w), out in res.items():
        cen[(tag_of[(r, w)], out[0])] += 1
    print('\ncensus (raise-site, outcome):')
    for k, v in sorted(cen.items()):
        print(f'   {k}: {v}')
    # census of MOVE constants
    cc = Counter(out[1] for out in res.values() if out[0] == 'MOVE')
    print('MOVE constants c:', dict(sorted(cc.items())))
    with open(OUT, 'wb') as f:
        pickle.dump({'res': res, 'tag_of': tag_of}, f)
    print(f'dumped -> {OUT}')
