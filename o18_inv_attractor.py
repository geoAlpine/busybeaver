# o18 INVARIANT SYNTHESIS step 2a: EXACT adversarial BAD-attractor on a bounded universe.
# BAD(w)  :=  the adversary (free choice of residue r in {0,1,2} each pass) can force a
#             HALT from word w using only words inside the universe.   (least fixpoint:
#             only finite forcing paths count; escapes outside the universe count SAFE,
#             so BAD is an UNDER-approximation of the true adversarial attractor.)
# The structure of BAD is the ground-truth feature set for any inductive invariant:
# any sound invariant I (exit-cone in I, T-closed, fatal-free) must satisfy I /\ BAD = 0.
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown
from itertools import product

def in_universe(w, maxlen, maxb, maxs):
    return len(w) <= maxlen and all(b <= maxb and s <= maxs for s, b in w)

def compute_bad(universe_words, maxlen, maxb, maxs):
    status = {}   # word -> True (BAD) / False (not forced within universe)
    onstack = set()
    sys.setrecursionlimit(100000)
    def bad(w):
        if w in status:
            return status[w]
        if w in onstack:          # lfp: cycles are not winning for the adversary
            return False
        onstack.add(w)
        res_bad = False
        for r in (0, 1, 2):
            try:
                res = T(r, w)
            except Unknown:
                continue          # unknown cells: not counted as a win (under-approx)
            if res[0] == 'HALT':
                res_bad = True
                break
            if res[0] == 'LAND':
                continue
            w2 = res[2]
            if not in_universe(w2, maxlen, maxb, maxs):
                continue          # escape: counts SAFE (under-approx of BAD)
            if bad(w2):
                res_bad = True
                break
        onstack.discard(w)
        status[w] = res_bad
        return res_bad
    for w in universe_words:
        bad(w)
    return status

# ---------------- pattern features ----------------
def units_split(w):
    """word -> list of ('U', n) / block items, collapsing unit runs."""
    out, i = [], 0
    while i < len(w):
        if w[i] == (1, 1):
            j = i
            while j < len(w) and w[j] == (1, 1):
                j += 1
            out.append(('U', j - i)); i = j
        else:
            out.append(w[i]); i += 1
    return out

def nonunit_blocks(w):
    return [x for x in units_split(w) if x[0] != 'U']

def has_pair_pattern(w, first_pred, second_pred):
    """exists blocks i<i' separated ONLY by unit blocks, first_pred(b_i), second_pred(b_i')."""
    seq = units_split(w)
    idx = [k for k, x in enumerate(seq) if x[0] != 'U']
    for a in range(len(idx)):
        for b in range(a + 1, len(idx)):
            if all(seq[k][0] == 'U' for k in range(idx[a] + 1, idx[b])):
                if first_pred(seq[idx[a]]) and second_pred(seq[idx[b]]):
                    return True
            else:
                break
    return False

if __name__ == '__main__':
    # universe: exhaustive small + wider shells
    words = set()
    B4, S4 = range(1, 10), range(1, 4)
    for L in range(1, 5):
        for w in product([(s, b) for s in S4 for b in B4], repeat=L):
            words.add(w)
    for w in product([(s, b) for s in (1, 2) for b in range(1, 7)], repeat=5):
        words.add(w)
    print(f'universe: {len(words)} words', flush=True)
    maxlen, maxb, maxs = 5, 9, 3
    status = compute_bad(words, maxlen, maxb, maxs)
    bad = [w for w in words if status.get(w)]
    print(f'BAD (adversary forces halt in-universe): {len(bad)} / {len(words)}')

    # ---- mine: minimal BAD words (by total size) ----
    def size(w):
        return sum(s + b for s, b in w)
    bad.sort(key=lambda w: (len(w), size(w)))
    print('\n30 smallest BAD words:')
    for w in bad[:30]:
        print('   ', w)

    # ---- test candidate pattern predicates against BAD ----
    # P0: two exact-(sep1,2) blocks separated only by units
    # P1: (any sep, v==2mod3, v>=2) then units* then (1,2)
    # P2: (any sep, v==2mod3, v>=2) then units* then (any sep, 2)
    # P3: (any sep>=2 OR v==2mod3) then units* then (any sep, 2)
    is2mod3 = lambda x: x[1] % 3 == 2 and x[1] >= 2
    P0 = lambda w: has_pair_pattern(w, lambda x: x == (1, 2), lambda x: x == (1, 2))
    P1 = lambda w: has_pair_pattern(w, is2mod3, lambda x: x == (1, 2))
    P2 = lambda w: has_pair_pattern(w, is2mod3, lambda x: x[1] == 2)
    P3 = lambda w: has_pair_pattern(w, lambda x: x[0] >= 2 or is2mod3(x), lambda x: x[1] == 2)
    for name, P in (('P0', P0), ('P1', P1), ('P2', P2), ('P3', P3)):
        miss = [w for w in bad if not P(w)]                 # BAD but pattern-free: pattern too weak
        safe_with = sum(1 for w in words if not status.get(w) and P(w))  # pattern-positive but not (in-universe-)forced
        print(f'\n{name}: BAD missed by pattern: {len(miss)};  pattern-positive non-BAD: {safe_with}')
        for w in miss[:15]:
            print('    missed:', w)
