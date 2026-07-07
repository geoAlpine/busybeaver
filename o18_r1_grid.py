# o18 R1-PINNING step 3a: SYSTEMATIC concrete grids over the unpinned deep-R1 template
# families (beyond the ad-hoc 517 cells), to fit general closed-form templates:
#   H : w = 1^j (1,2) 1^p (1,2) 1^q                        (h_p general p; rho = 2q+6)
#   H': w = 1^j (1,2) 1^p (1,2) (2,zv) W                   (h_p with rho = zv+6)
#   G : w = 1^j (1,2) 1^p (1,2) (zs>=3,zv) W               ('gap s>=3' site)
#   B1: w = 1^j (1,2) 1^p (1,2) 1^{q>=1} (2,zv) W          ('deep', gapped tail)
#   B2: w = 1^j (1,2) 1^p (1,2) 1^q (1,2) W                ('deep', nested third 2)
# All at r=1 (the R1 branch), j=0 primary + j=1,2 wrapper checks; 4 magnitudes each,
# per-cell determinism enforced.  Prediction-free (never consults T).
import sys, pickle
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_r1_probe import probe_cell
from o18_md_probe import wstr

SCR = '/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/8b7a3f39-ce4e-4044-afe8-60ce3b3aedcf/scratchpad'
OUT = sys.argv[1] if len(sys.argv) > 1 else SCR + '/o18_r1_grid.pkl'

U = lambda n: ((1, 1),) * n

def famH():
    for j in (0, 1, 2):
        for p in range(1, 13):
            for q in range(0, 7):
                yield ('H', (j, p, q)), U(j) + ((1, 2),) + U(p) + ((1, 2),) + U(q)

def famHp():
    for j in (0, 1):
        for p in range(1, 11):
            for zv in range(1, 9):
                for W in ((), ((1, 3),), ((1, 1), (1, 6))):
                    yield ('Hp', (j, p, zv, W)), U(j) + ((1, 2),) + U(p) + ((1, 2), (2, zv)) + W

def famG():
    for j in (0, 1):
        for p in range(1, 7):
            for zs in (3, 4, 5):
                for zv in (1, 2, 3, 4, 6):
                    for W in ((), ((1, 4),)):
                        yield ('G', (j, p, zs, zv, W)), U(j) + ((1, 2),) + U(p) + ((1, 2), (zs, zv)) + W

def famB1():
    for j in (0, 1):
        for p in range(1, 9):
            for q in range(1, 5):
                for zs in (2, 3, 4):
                    for zv in (1, 2, 3, 4, 6):
                        if zs > 2 and (zv in (4, 6) or q > 2):
                            continue  # keep the zs>=3 shell lighter
                        for W in ((), ((1, 4),)):
                            yield ('B1', (j, p, q, zs, zv, W)), U(j) + ((1, 2),) + U(p) + ((1, 2),) + U(q) + ((zs, zv),) + W

def famB2():
    Ws = ((), U(1), U(3), ((1, 5),), ((1, 3),), ((2, 3),), ((1, 2),), U(2) + ((1, 2),), ((1, 1), (1, 6)))
    for j in (0, 1, 2):
        for p in range(1, 9):
            for q in range(0, 5):
                for W in Ws:
                    yield ('B2', (j, p, q, W)), U(j) + ((1, 2),) + U(p) + ((1, 2),) + U(q) + ((1, 2),) + W

if __name__ == '__main__':
    which = sys.argv[2] if len(sys.argv) > 2 else 'all'
    fams = {'H': famH, 'Hp': famHp, 'G': famG, 'B1': famB1, 'B2': famB2}
    res = {}
    nsplit = nhalt = 0
    from multiprocessing import Pool
    for name, gen in fams.items():
        if which not in ('all', name):
            continue
        items = list(gen())
        with Pool(8) as pool:
            outs = pool.starmap(probe_cell, [(1, w) for _, w in items], chunksize=8)
        for (key, w), out in zip(items, outs):
            res[key] = (w, out)
            if out[0] == 'SPLIT':
                nsplit += 1
                print('SPLIT!', key, w, out, flush=True)
            if out[0] == 'HALT':
                nhalt += 1
        print(f'family {name}: {len(items)} cells probed', flush=True)
    print(f'TOTAL {len(res)} cells; SPLITs {nsplit}; HALTs {nhalt}')
    with open(OUT, 'wb') as f:
        pickle.dump(res, f)
    print(f'dumped -> {OUT}')
