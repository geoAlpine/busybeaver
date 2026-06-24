import itertools, numpy as np
# NEW FRAMING: parity_n = G(incoming bits over a k-window), where G is the sliding-block code from F_k.
# The orbit's parity law is a FIXED POINT of G (as a CA factor map). Extract G, study its fixed points.
# Build F_k exactly: state mod 2^k after k steps from start s0, given k incoming bits.
def stepf(c): return (3*c)//2
def Gfunc(k, s0=0):
    # returns dict: (k incoming bits) -> parity (bit0) of state after k steps
    K=1<<k; G={}
    for digs in itertools.product((0,1),repeat=k):
        s=s0
        for d in digs:
            s=stepf(s + (d<<k)) % K
        G[digs]=s&1
    return G
# Extract G for k=3,4; check it's start-independent on parity (since delta(P^k)=0 on the whole state)
for k in (3,4):
    G0=Gfunc(k,0); G1=Gfunc(k,(1<<k)//2+1)
    same=all(G0[d]==G1[d] for d in G0)
    ones=sum(G0.values())
    print(f"k={k}: G is start-independent={same};  G outputs 1 on {ones}/{2**k} inputs (balanced if {2**(k-1)})")
    if k==3:
        print("   truth table G(b0..b{k-1})->parity:")
        for d in sorted(G0): print(f"     {d} -> {G0[d]}")
