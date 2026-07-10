"""
Christol / automatic-sequence test for the o4 residue sequence rho_n = W_n mod 3.

Christol's theorem: a sequence over F_p is p-automatic  <=>  its generating
function is algebraic over F_p(x)  <=>  its p-kernel is FINITE.

p-kernel of a sequence a:  K_p(a) = { n |-> a(p^k n + r) : k>=0, 0 <= r < p^k }.
Finite kernel  <=> automatic; growing kernel <=> non-automatic (transcendent GF).

We compute the 3-kernel and 2-kernel sizes at increasing depth for:
  - rho_n = W_n mod 3            (the residue sequence, over F_3)
  - the indicator 1{rho_n = 1}   (over F_2 -- genuine 2-automaticity target)
  - the run-length sequence (rho=1 runs) and reload-unit sequence.

Exact big-int arithmetic throughout.  No floats in the orbit.
"""
import sys

# ---------------------------------------------------------------------------
# 1. Exact orbit.  Self-contained W-orbit with rho = W mod 3.
#    Derivation (O4_RUN_STRUCTURE): G-orbit 3G' = 4G + e(G mod3),
#    e={0:9,1:14,2:1}; mirror W=G+14 => 3W' = 4W + (e-14).
#    Keyed by r = W mod 3:  r=0 -> +0, r=1 -> -13, r=2 -> -5.
#    So  W' = (4W - c(r))/3,  c = {0:0, 1:13, 2:5}.  Seed W_0 = 57 (G_0=43).
# ---------------------------------------------------------------------------
C = {0: 0, 1: 13, 2: 5}

def gen_orbit(N, W0=57):
    W = W0
    rho = []
    Ws = []
    for _ in range(N):
        r = W % 3
        rho.append(r)
        Ws.append(W)
        num = 4 * W - C[r]
        assert num % 3 == 0, "non-integer step -- orbit derivation wrong"
        W = num // 3
    return rho, Ws

# Cross-check against the raw G-orbit to be certain the derivation is exact.
def gen_G(N, G0=43):
    E = {0: 9, 1: 14, 2: 1}
    G = G0
    rhoG = []
    for _ in range(N):
        r = G % 3
        rhoG.append(r)
        num = 4 * G + E[r]
        assert num % 3 == 0
        G = num // 3
    return rhoG

# ---------------------------------------------------------------------------
# 2. p-kernel computation.
#    We measure kernel elements as functions by their first L values.
#    Two subsequences are identified iff their first L available values agree.
#    To avoid FALSE MERGES from truncation, every kernel element at depth<=K
#    must have >= L available terms: need original length >= p^K*(L-1)+r+1.
# ---------------------------------------------------------------------------
def kernel_sizes(seq, p, Kmax, L):
    """Return list of (k, cumulative distinct kernel elements using depths 0..k),
    comparing subsequences on their first L terms.  Auto-caps Kmax to the depth
    for which every residue class r<p^k still has a full window of L terms
    (last index p^k*(L-1)+r < len(seq)), so NO comparison is ever truncated."""
    n_total = len(seq)
    sizes = []
    seen = {}                 # signature tuple -> id
    for k in range(Kmax + 1):
        pk = p ** k
        # need p^k*(L-1) + (pk-1) < n_total  (worst residue r=pk-1)
        if pk * (L - 1) + (pk - 1) >= n_total:
            break
        for r in range(pk):
            sig = tuple(seq[pk * m + r] for m in range(L))
            if sig not in seen:
                seen[sig] = len(seen)
        sizes.append((k, len(seen)))
    return sizes, None

# ---------------------------------------------------------------------------
# 3. run-length + reload-unit sequences.
# ---------------------------------------------------------------------------
def run_lengths(rho):
    """Maximal-run structure. Returns list of (value, length) runs and the
    sequence of rho=1 run lengths (d_i) and non-1 block lengths (reload units)."""
    runs = []
    i = 0
    n = len(rho)
    while i < n:
        v = rho[i]
        j = i
        while j < n and rho[j] == v:
            j += 1
        runs.append((v, j - i))
        i = j
    return runs

def main():
    N = 250_000
    print(f"Generating exact orbit, N={N} ...", flush=True)
    rho, Ws = gen_orbit(N)
    # cross check with G-orbit residues: G mod 3 vs W mod 3 relation
    rhoG = gen_G(200000)
    # G = W-14 ; G mod3 = (W-14)mod3 = (W+1)mod3.  So rhoG = (rho+1)%3
    ok = all(rhoG[i] == (rho[i] + 1) % 3 for i in range(len(rhoG)))
    print(f"G/W residue cross-check (rhoG == (rhoW+1)%3): {ok}")

    from collections import Counter
    c = Counter(rho[:200000])
    print(f"residue counts (first 2e5): {dict(c)}  freq(W==0 i.e. rho=1 in G)= {c[0]/200000:.5f}")

    print("\n================ 3-KERNEL of rho_n = W_n mod 3 (over F_3) ================")
    for L in (100, 200, 400):
        sizes, err = kernel_sizes(rho, 3, 8, L)
        if err:
            print(f"L={L}: {err}")
            continue
        pretty = "  ".join(f"k<={k}:{s}" for k, s in sizes)
        print(f"window L={L}:  {pretty}")

    print("\n================ 2-KERNEL of rho_n = W_n mod 3 =====================")
    for L in (100, 200, 400):
        sizes, err = kernel_sizes(rho, 2, 14, L)
        if err:
            print(f"L={L}: {err}")
            continue
        pretty = "  ".join(f"k<={k}:{s}" for k, s in sizes)
        print(f"window L={L}:  {pretty}")

    print("\n============ 2-KERNEL of indicator 1{rho_n=1(G)} == 1{W_n==0} (over F_2) ============")
    ind = [1 if r == 0 else 0 for r in rho]   # W==0  <=> G==1 <=> rho_G=1 (the ledger-drain letter)
    for L in (100, 200, 400):
        sizes, err = kernel_sizes(ind, 2, 14, L)
        if err:
            print(f"L={L}: {err}"); continue
        pretty = "  ".join(f"k<={k}:{s}" for k, s in sizes)
        print(f"window L={L}:  {pretty}")

    print("\n============ 3-KERNEL of same indicator (over F_3, as 0/1 seq) ============")
    for L in (100, 200, 400):
        sizes, err = kernel_sizes(ind, 3, 8, L)
        if err:
            print(f"L={L}: {err}"); continue
        pretty = "  ".join(f"k<={k}:{s}" for k, s in sizes)
        print(f"window L={L}:  {pretty}")

    # ------- run-length / reload structure -------
    print("\n================ run-length / reload-unit sequences ================")
    runs = run_lengths(rho)
    d_run1 = [ln for (v, ln) in runs if v == 0]     # rho_G=1 runs == W==0 runs
    reload = [ln for (v, ln) in runs if v != 0]     # non-drain blocks
    print(f"total runs={len(runs)}, #(W==0 runs)={len(d_run1)}, max run len={max(d_run1)}, "
          f"mean={sum(d_run1)/len(d_run1):.4f}")
    # run-length alphabet is unbounded -> cannot be automatic as-is over finite alphabet.
    from collections import Counter as Ct
    print(f"run-length value distribution (W==0 runs): {dict(sorted(Ct(d_run1).items()))}")
    # Test automaticity of run-length seq REDUCED mod 2 and mod 3 (finite alphabet):
    for mod, pp in ((2, 2), (3, 3)):
        dm = [x % mod for x in d_run1]
        L = 100
        sizes, err = kernel_sizes(dm, pp, 30, L)
        pretty = "  ".join(f"k<={k}:{s}" for k, s in sizes)
        print(f"run-len (W==0) mod {mod}, {pp}-kernel L={L}:  {pretty}")
    # reload-unit sequence too
    for mod, pp in ((2, 2),):
        rm = [x % mod for x in reload]
        L = 100
        sizes, err = kernel_sizes(rm, pp, 30, L)
        pretty = "  ".join(f"k<={k}:{s}" for k, s in sizes)
        print(f"reload-unit mod {mod}, {pp}-kernel L={L}:  {pretty}")

    print("\nDONE.")

if __name__ == "__main__":
    main()
