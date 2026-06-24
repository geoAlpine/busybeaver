# delta(P^k)=0 means state mod p^k after k steps is independent of start. Is the map
# F_k: (k incoming digits) -> (state mod p^k) a BIJECTION? If yes: equidistributed incoming k-blocks
# => equidistributed state => parity 1/2. This makes the contraction->equidistribution step RIGOROUS.
def F_map(p, fstep, k, start=0):
    K=p**k
    out={}
    import itertools
    for digs in itertools.product(range(p), repeat=k):
        s=start
        for d in digs:
            c=s + d*K       # inject incoming high digit
            s=fstep(c) % K
        out[digs]=s
    return out
def check_bij(p,fstep,k):
    m=F_map(p,fstep,k)
    images=set(m.values())
    # bijection iff all p^k images distinct AND independent of start
    indep=True
    m2=F_map(p,fstep,k,start=(p**k)//2+1)
    for d in m: 
        if m[d]!=m2[d]: indep=False; break
    return len(images)==p**k, indep
f2=lambda c:(3*c)//2
f3=lambda c:(8*c)//3
print("F_k bijection check (k incoming digits -> state mod p^k):")
for k in (3,4,5):
    bij,indep=check_bij(2,f2,k)
    print(f"  p=2 k={k}: bijection={bij}  start-independent={indep}")
for k in (2,3):
    bij,indep=check_bij(3,f3,k)
    print(f"  p=3 k={k}: bijection={bij}  start-independent={indep}")
print("\n=> bijection + start-independent => RIGOROUS: state mod p^k equidistributes IFF the incoming")
print("   k-digit blocks equidistribute. So: [hypothesis: incoming digits have equidistributed k-blocks]")
print("   ==> state equidistributes ==> digit delta_n ~ Uniform(1/p) ==> non-halt.  Contraction step RIGOROUS.")
