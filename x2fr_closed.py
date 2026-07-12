#!/usr/bin/env python3
"""x2fr_closed.py -- derive & verify the closed form T(K), C(K) from the exact
band-count structure and the cached distributions."""
import sys, pickle
from collections import Counter
SP = '/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/8b7a3f39-ce4e-4044-afe8-60ce3b3aedcf/scratchpad'

GT_T = {10: 3852, 11: 9729, 12: 19470}
GT_C = {10: 192, 11: 386, 12: 768}


def dist_from_cache(g):
    with open(f'{SP}/css_g{g}.pkl', 'rb') as f:
        css = pickle.load(f)
    blks = [c[1] for c in css]
    return Counter(blks), len(css)


def analyze(g):
    K = g + 8
    dist, T = dist_from_cache(g)
    print(f"=== g={g} K={K}: T={T} (GT {GT_T[K]}) ===")
    # verify band law: count(b)=2^{K-j+1}-1 for b in (2^{j-1}-3, 2^j-3) non-milestone
    def band_of(b):
        # smallest j with 2^j-3 >= b
        j = 2
        while 2**j - 3 < b:
            j += 1
        return j
    bad = 0
    for b, cnt in sorted(dist.items()):
        if b < 5: continue
        j = band_of(b)
        if b == 2**j - 3:
            pred = 2**(K - j + 2) - 1  # milestone
            tag = 'MILE'
        else:
            pred = 2**(K - j + 1) - 1  # band
            tag = 'band'
        if cnt != pred:
            bad += 1
            if bad <= 12:
                print(f"  b={b} ({tag} j={j}): got {cnt} pred {pred}  diff {cnt-pred}")
    print(f"  band-law mismatches: {bad} of {len(dist)} block-values")


if __name__ == "__main__":
    for g in (2, 3):
        analyze(g)
