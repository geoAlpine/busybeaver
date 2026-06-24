import itertools, numpy as np
def stepf(c): return (3*c)//2
def Gfunc(k, s0=0):
    K=1<<k; G={}
    for digs in itertools.product((0,1),repeat=k):
        s=s0
        for d in digs: s=stepf(s+(d<<k))%K
        G[digs]=s&1
    return G
# extract exact affine form: parity = c0 XOR (sum_{i in S} b_i) over GF(2)
def affine_form(k):
    G=Gfunc(k,0)
    # G affine => G(b) = c0 + sum ci bi. ci = G(e_i) - G(0); c0 = G(0).
    c0=G[(0,)*k]
    coeffs=[]
    for i in range(k):
        e=[0]*k; e[i]=1
        coeffs.append((G[tuple(e)]-c0)&1)
    # verify it's truly affine
    ok=all( (c0 ^ sum(coeffs[i]&b[i] for i in range(k)))&1 == G[b] for b in G)
    return c0, coeffs, ok
print("exact affine form of parity code: parity_n = c0 XOR (XOR over set S of incoming bits)")
for k in (3,4,5,6,7):
    c0,co,ok=affine_form(k)
    S=[i for i in range(k) if co[i]]
    print(f"  k={k}: parity = {c0} XOR (bits at positions {S} of the k-incoming-window)  [affine-verified={ok}]")
    print(f"        |S|={len(S)} terms")
print("\nINTERPRETATION:")
print(" - position i in the window = incoming bit from (k-i) steps ago = bit_k(c_{n-(k-i)}).")
print(" - if |S|=1 (single position): parity is a pure DELAY of bit_k => circular (the wall).")
print(" - if |S|>1 (genuine XOR of several delayed bit_k's): the even-density of parity becomes a")
print("   LINEAR (XOR) exponential sum over the orbit -- potentially tractable where full equidist is not.")
