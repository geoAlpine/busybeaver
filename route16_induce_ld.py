"""
Route #16 part 3.
Finding from part 2: rho_{n+1} = (G_n // 3) mod 3  EXACTLY (an exact finite read-out
transport). Verify it, then test the two routes that could still help:
  (E) first-return / induced system on cylinder [rho=1]: is it simpler (computable freq)?
  (F) large-deviation rate for {freq(rho=1) >= 4/5}: how thin is the 'bad set',
      and where does seed 43 sit?
"""
import sys, math
sys.set_int_max_str_digits(1000000)
from collections import Counter, defaultdict

E = {0: 9, 1: 14, 2: 1}
def T(G): return (4 * G + E[G % 3]) // 3

# ---- verify exact identity rho_{n+1} = (G//3) mod 3 ----
G = 43; ok = True
for _ in range(5000):
    predicted = (G // 3) % 3
    G2 = T(G)
    if G2 % 3 != predicted:
        ok = False; break
    G = G2
print(f"(verify) rho_{{n+1}} == (G_n//3) mod 3  for 5000 steps: {ok}")
# also T(G) = 4*(G//3) + s_r, s_0=3,s_1=6,s_2=3
G = 43; ok2 = True
S = {0:3,1:6,2:3}
for _ in range(5000):
    if T(G) != 4*(G//3) + S[G%3]:
        ok2 = False; break
    G = T(G)
print(f"(verify) T(G) == 4*(G//3) + s_(G mod3), s=(3,6,3): {ok2}")

# ---- build long itinerary ----
N = int(sys.argv[1]) if len(sys.argv) > 1 else 300000
G = 43; res = []
for _ in range(N):
    res.append(G % 3); G = T(G)

# ---- (E) first-return induced system on [rho=1] ----
pos = [i for i,r in enumerate(res) if r==1]
rets = [pos[i+1]-pos[i] for i in range(len(pos)-1)]
print(f"\n(E) induced first-return times on [rho=1]: {len(rets)} returns")
# is the return-time SEQUENCE itself structured? entropy of return-time symbol stream
rc = Counter(rets)
tot = len(rets)
Hret = -sum((c/tot)*math.log2(c/tot) for c in rc.values())
# geometric(1/3) entropy for comparison: H = H(p)/p with p=1/3
p = 1/3
Hgeo = (-(p*math.log2(p) + (1-p)*math.log2(1-p)))/p
print(f"    entropy of return-time distribution: {Hret:.4f} bits   geometric(1/3) ref: {Hgeo:.4f}")
# memory in the return-time sequence: H(r_{k+1}|r_k)
ctx = defaultdict(Counter)
for i in range(len(rets)-1): ctx[rets[i]][rets[i+1]] += 1
tt = sum(sum(c.values()) for c in ctx.values())
Hc = sum(sum(c.values())/tt*(-sum((x/sum(c.values()))*math.log2(x/sum(c.values())) for x in c.values())) for c in ctx.values())
print(f"    H(r_{{k+1}} | r_k) = {Hc:.4f}  (>= Hret means memoryless => no extra structure)")

# ---- (F) large deviations: sliding-window freq of rho=1, and Cramer rate for >=4/5 ----
print(f"\n(F) sliding-window freq(rho=1) statistics over seed-43 orbit (N={N}):")
for W in (50, 200, 1000):
    fr = []
    run = sum(1 for r in res[:W] if r==1)
    fr.append(run/W)
    for i in range(W, len(res)):
        run += (res[i]==1) - (res[i-W]==1)
        fr.append(run/W)
    mx = max(fr); mn = min(fr); above = sum(1 for x in fr if x>=0.8)/len(fr)
    print(f"    window W={W:4d}: mean={sum(fr)/len(fr):.4f}  min={mn:.3f} max={mx:.3f}  frac(window>=4/5)={above:.2e}")
# Cramer rate: for iid uniform(1/3), P(freq>=q) ~ exp(-N I(q)), I(q)=q log(3q)+(1-q)log(3(1-q)/2)
def rate(q):
    return q*math.log(3*q) + (1-q)*math.log(3*(1-q)/2)
q=0.8
print(f"    Cramer rate I(4/5) for iid-uniform base3 = {rate(q):.4f} nats/symbol")
print(f"    => 'bad set' {{freq>=4/5}} has box-dim deficit ~ I/log3 = {rate(q)/math.log(3):.4f} below full;")
print(f"       measure(bad set) ~ 3^-N * e^{{N*0}}... i.e. Lebesgue-null but positive Hausdorff dim.")
