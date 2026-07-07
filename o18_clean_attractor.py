# o18 CLEANUP task 2a (2026-07-08): re-run the exact adversarial BAD-attractor of
# o18_inv_attractor.py with the CORRECTED transducer T_ext (o18_md_rules_ext.py).
# Base-T count on the same universe: 65,669 / 800,712 (O18_INVARIANT_SYNTHESIS sec 2).
# The base transducer's unsoundness is exclusively false-HALT (O18_R1_PINNING sec 2),
# so the base BAD set is an OVER-count of the T_ext BAD set restricted to shared cells
# -- but T_ext also DEFINES cells base T raised Unknown on (which mode 'unknown cells
# are not counted as a win' made SAFE), so the count can move both ways a priori;
# this run measures it.  Also reports: the exit-cone/D-family status under T_ext, the
# value-2 feature census on the new BAD set, and the exact base-vs-ext BAD diff.
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown
from o18_md_rules_ext import T_ext
from o18_inv_attractor import in_universe, units_split, nonunit_blocks
from itertools import product

def compute_bad(universe_words, maxlen, maxb, maxs, TT):
    status = {}
    onstack = set()
    sys.setrecursionlimit(100000)
    def bad(w):
        if w in status:
            return status[w]
        if w in onstack:
            return False
        onstack.add(w)
        res_bad = False
        for r in (0, 1, 2):
            try:
                res = TT(r, w)
            except Unknown:
                continue
            if res[0] == 'HALT':
                res_bad = True
                break
            if res[0] == 'LAND':
                continue
            w2 = res[2]
            if not in_universe(w2, maxlen, maxb, maxs):
                continue
            if bad(w2):
                res_bad = True
                break
        onstack.discard(w)
        status[w] = res_bad
        return res_bad
    for w in universe_words:
        bad(w)
    return status

if __name__ == '__main__':
    words = set()
    B4, S4 = range(1, 10), range(1, 4)
    for L in range(1, 5):
        for w in product([(s, b) for s in S4 for b in B4], repeat=L):
            words.add(w)
    for w in product([(s, b) for s in (1, 2) for b in range(1, 7)], repeat=5):
        words.add(w)
    print(f'universe: {len(words)} words', flush=True)
    maxlen, maxb, maxs = 5, 9, 3

    st_ext = compute_bad(words, maxlen, maxb, maxs, T_ext)
    bad_ext = {w for w in words if st_ext.get(w)}
    print(f'BAD under T_ext: {len(bad_ext)} / {len(words)}   (base-T reference: 65,669)',
          flush=True)

    st_base = compute_bad(words, maxlen, maxb, maxs, T)
    bad_base = {w for w in words if st_base.get(w)}
    print(f'BAD under base T (re-run cross-check): {len(bad_base)}')

    only_base = bad_base - bad_ext
    only_ext = bad_ext - bad_base
    print(f'BAD in base only (false-fatal candidates removed by the correction): {len(only_base)}')
    print(f'BAD in T_ext only (newly-defined cells opening real forcing paths): {len(only_ext)}')
    for w in sorted(only_base, key=lambda w: (len(w), sum(s + b for s, b in w)))[:10]:
        print('   base-only BAD:', w)
    for w in sorted(only_ext, key=lambda w: (len(w), sum(s + b for s, b in w)))[:10]:
        print('   ext-only  BAD:', w)

    # feature checks that O18_INVARIANT_SYNTHESIS sec 2 committed to (on the base set):
    # every BAD word contains a value-2 block; tail-2-free BAD words all start (3,2)
    no2 = [w for w in bad_ext if all(b != 2 for s, b in nonunit_blocks(w))]
    ntail2 = [w for w in bad_ext
              if all(b != 2 for s, b in nonunit_blocks(w)[1:])]
    bad_first32 = [w for w in ntail2 if not (nonunit_blocks(w) and nonunit_blocks(w)[0] == (3, 2))]
    print(f'T_ext BAD words with NO value-2 block: {len(no2)} (base: 0)')
    print(f'T_ext BAD words with no TAIL 2: {len(ntail2)} (base: 55, all first-block (3,2))')
    print(f'   ...of those, first block != (3,2): {len(bad_first32)}')

    # exit cone + D-family status
    cone = [((1, 2 * t + 2), (1, 6)) for t in range(1, 12)] + [((1, 4), (1, 1), (1, 1), (1, 1))]
    dfam = [((1, 1),) * t + ((1, e),) for t in range(0, 4) for e in range(1, 7)]
    nc = sum(1 for w in cone if w in words and st_ext.get(w))
    nd = sum(1 for w in dfam if w in words and st_ext.get(w))
    print(f'exit cone BAD under T_ext: {nc}/{sum(1 for w in cone if w in words)}; '
          f'D-family BAD: {nd}/{sum(1 for w in dfam if w in words)}  (base: 0/36 combined)')
