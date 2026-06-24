# SCRUTINY: is the M1 fixed-point uniqueness circular? The fixed-point sims fed incoming bits from an RNG --
# i.e. INDEPENDENT of the chain state. But state-independence IS the hypothesis (H). Without it, is the
# fixed point still unique? Test: the ALL-ODD trap (state-correlated incoming) -- is it self-consistent?
k=10; K=1<<k
def step(s,h): return (3*(s+(h<<k)))//2 % K
# all-odd trap: keep c ≡ 1 mod 2^k. The incoming bit needed each step to STAY odd (c_{n+1} odd):
# choose h (state-correlated!) to keep state==1 mod 2^k if possible.
s=1; odd_count=0; T=200000; incoming=[]
for n in range(T):
    # try both incoming bits; pick one that keeps state odd (state-correlated adversary)
    cand=[(h, step(s,h)) for h in (0,1)]
    odd_opts=[(h,t) for h,t in cand if t&1==1]
    if odd_opts: h,t=odd_opts[0]
    else: h,t=cand[0]
    incoming.append(h)
    if t&1==1: odd_count+=1
    s=t
print("STATE-CORRELATED adversary (keeps state odd):")
print(f"  even-density of output = {1-odd_count/T:.4f}  (Bernoulli would be 0.5)")
inc=sum(incoming)/T
print(f"  incoming density of 1s = {inc:.4f};  output(parity) density of 1s = {odd_count/T:.4f}")
print(f"  self-consistent (incoming law ~ output law)? incoming-1s={inc:.3f} vs output-1s(odd)={odd_count/T:.3f}")
print("\n=> if a STATE-CORRELATED process is self-consistent with even-density != 1/2, then the fixed point is")
print("   NOT unique without assuming state-independence => M1/D2 PRESUPPOSES (H) => CIRCULAR.")
print("   The RNG-fed sims gave Bernoulli only because the RNG is state-independent = assumes (H).")
