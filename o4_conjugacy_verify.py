# Verify idea A's central claim: the o4 residue itinerary is a bijection
# Z/3^k -> {0,1,2}^k (T conjugate to the one-sided full 3-shift). 2026-07-10.
e = {0: 9, 1: 14, 2: 1}
def T(G, mod):
    r = G % 3
    return ((4 * G + e[r]) // 3) % mod   # step on Z/3^m; caller supplies mod
def itinerary(G0, k):
    # itinerary of G0 read on Z/3^{k} (enough precision): rho_j = (T^j G0) mod 3
    G = G0; out = []
    for _ in range(k):
        out.append(G % 3)
        G = (4 * G + e[G % 3]) // 3   # exact integer step (representative)
    return tuple(out)
for k in range(1, 9):
    seen = {}
    ok = True
    for G0 in range(3**k):
        w = itinerary(G0, k)
        if w in seen:
            ok = False; break
        seen[w] = G0
    nwords = len(seen)
    print(f"k={k}: distinct itineraries = {nwords} / 3^{k} = {3**k}  bijection={ok and nwords==3**k}")
    assert ok and nwords == 3**k, f"NOT a bijection at k={k}"
print("VERIFIED: itinerary is a bijection Z/3^k -> {0,1,2}^k for k=1..8")
print("=> T conjugate to the one-sided full 3-shift; phi = symbol-1 frequency; phi=1/3 Haar-a.e.")
print("No machine decided. No label upgraded.")
