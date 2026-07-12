#!/usr/bin/env python3
"""x2fr_verdict.py -- derive & verify the exact closed forms T(K), C(K).

Main sum from band law:  T_main(K) = (2K-5)*2^(K-2) + 1
Even g:  T(K) = (2K-5)*2^(K-2) + K + 2       [verified K=10,12]
Odd g:   T(K) = (2K-5)*2^(K-2) + 2^(K-1) + ? [K=11]
Here we load the exact block distributions and pin the edge corrections exactly,
band-by-band, for both parities.
"""
import pickle
from collections import Counter
SP = '/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/8b7a3f39-ce4e-4044-afe8-60ce3b3aedcf/scratchpad'
GT_T = {10: 3852, 11: 9729, 12: 19470}


def load_dist(g):
    # prefer full css cache, else the light dist pkl
    try:
        with open(f'{SP}/css_g{g}.pkl','rb') as f:
            css = pickle.load(f)
        return Counter(c[1] for c in css)
    except FileNotFoundError:
        with open(f'{SP}/dist_g{g}.pkl','rb') as f:
            return Counter(pickle.load(f))


def band_of(b):
    j = 2
    while 2**j - 3 < b:
        j += 1
    return j


def check(g):
    K = g + 8
    dist = load_dist(g)
    T = sum(dist.values())
    # predicted per-block by band law
    pred_total = 0
    corr = 0
    corrections = []
    for b, cnt in dist.items():
        j = band_of(b)
        if b == 2**j - 3:
            pred = 2**(K - j + 2) - 1
        else:
            pred = 2**(K - j + 1) - 1
        pred_total += pred
        if cnt != pred:
            corrections.append((b, cnt, pred, cnt - pred))
        corr += cnt - pred
    # closed form main term
    Tmain = (2*K - 5) * 2**(K - 2) + 1
    even = (2*K - 5) * 2**(K - 2) + K + 2
    print(f"=== g={g} K={K} parity={'even' if K%2==0 else 'odd'} ===")
    print(f"  T (measured)      = {T}   (GT {GT_T[K]})  match={T==GT_T[K]}")
    print(f"  band-law pred sum = {pred_total}   edge-corr total = {corr}")
    print(f"  T_main=(2K-5)2^(K-2)+1 = {Tmain}   T - T_main = {T - Tmain}")
    print(f"  even-formula (2K-5)2^(K-2)+K+2 = {even}   T-even = {T - even}")
    print(f"  edge corrections (b, got, pred, diff):")
    for c in sorted(corrections):
        print(f"      {c}")


if __name__ == "__main__":
    for g in (2, 3, 4):
        try:
            check(g)
        except FileNotFoundError as e:
            print(f"g={g}: no dist cached ({e})")
