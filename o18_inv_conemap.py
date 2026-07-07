# o18 INVARIANT SYNTHESIS step 2b: status of the EXIT CONE in the exact adversarial
# attractor + sharper mining of what separates BAD from non-BAD.
import sys, pickle, os
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown
from o18_inv_attractor import compute_bad, in_universe, units_split
from itertools import product

CACHE = '/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/8b7a3f39-ce4e-4044-afe8-60ce3b3aedcf/scratchpad/attractor_status.pkl'

def universe():
    words = set()
    for L in range(1, 5):
        for w in product([(s, b) for s in range(1, 4) for b in range(1, 10)], repeat=L):
            words.add(w)
    for w in product([(s, b) for s in (1, 2) for b in range(1, 7)], repeat=5):
        words.add(w)
    return words

if __name__ == '__main__':
    words = universe()
    if os.path.exists(CACHE):
        status = pickle.load(open(CACHE, 'rb'))
    else:
        status = compute_bad(words, 5, 9, 3)
        pickle.dump(status, open(CACHE, 'wb'))
    # -------- exit cone + D family --------
    print('EXIT-CONE / D-FAMILY STATUS in the exact adversarial attractor (in-universe):')
    tests = []
    for t in (1, 2, 3):
        tests.append((f'[2t+2,6] t={t}', ((1, 2 * t + 2), (1, 6))))
    tests.append(('[4,1,1,1]', ((1, 4), (1, 1), (1, 1), (1, 1))))
    for t in range(0, 4):
        for e in (1, 2, 3, 4, 5, 6, 8, 9):
            tests.append((f'D t={t} e={e}', ((1, 1),) * t + ((1, e),)))
    nbad = 0
    for name, w in tests:
        if not in_universe(w, 5, 9, 3):
            print(f'  {name}: OUT OF UNIVERSE')
            continue
        st = status.get(w)
        if st:
            nbad += 1
        print(f'  {name}: {"BAD" if st else "not-forced (in-universe)"}')
    print(f'  -> exit-cone/D words BAD: {nbad}')

    # -------- sharper mining --------
    # hypothesis H: BAD  <=>  exists a NON-FIRST block with value exactly 2
    #               (i.e. a "waiting 2" that something can be pushed onto)
    #               ... possibly minus escort/censoring effects.
    def waiting2(w):
        seq = units_split(w)
        blocks = [x for x in seq if x[0] != 'U']
        return any(b == 2 for s, b in blocks[1:])
    def first2(w):
        seq = units_split(w)
        blocks = [x for x in seq if x[0] != 'U']
        return bool(blocks) and blocks[0][1] == 2
    fp = fn = 0
    fn_ex, fp_ex = [], []
    for w in words:
        st = bool(status.get(w))
        h = waiting2(w)
        if h and not st:
            fp += 1
            if len(fp_ex) < 12: fp_ex.append(w)
        if st and not h:
            fn += 1
            if len(fn_ex) < 12: fn_ex.append(w)
    print(f'\nH = "some non-first block has value exactly 2":')
    print(f'  BAD without H (H too weak): {fn}')
    for w in fn_ex: print('    BAD, no waiting-2:', w)
    print(f'  H without BAD (censoring or genuine safety): {fp}')
    for w in fp_ex: print('    waiting-2, not forced:', w)

    # refine: H2 = waiting2 OR (first block value 2 and some other block value ==2)... subsumed.
    # look at BAD words with NO value-2 block at all:
    def any2(w):
        return any(b == 2 for s, b in w)
    no2 = [w for w in words if status.get(w) and not any2(w)]
    print(f'\nBAD with NO value-2 block anywhere: {len(no2)}')
    for w in sorted(no2, key=lambda w: (len(w), sum(s + b for s, b in w)))[:20]:
        print('   ', w)
