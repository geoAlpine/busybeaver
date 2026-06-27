"""Does FLP (spread >= 1/3) prove the annealed product prod_j |cos(pi theta_j)| -> 0?  theta_j={(3/2)^j/4}.

Key facts to test:
  - decay RATE: -log(prod_J)/J should -> the Birkhoff average  E[-log|cos(pi theta)|] = integral_0^1 = log 2,
    IFF theta_j EQUIDISTRIBUTES. So the product decays at rate log2 <=> equidistribution = Mahler.
  - FLP gives only the SPREAD (support) of theta_j, NOT the frequency near 1/2. A sequence can have spread
    ~1 (FLP satisfied) yet visit the middle (theta~1/2, where |cos| is small) with vanishing frequency,
    keeping the product from decaying at the log2 rate -- or, in the worst case, oscillate near {0,1}
    (|cos|~1) and NOT decay. So FLP (support) does not force the decay.
We measure: the decay rate vs log2; the empirical theta_j histogram (equidistributed?); the FLP spread; and
whether the decay tracks the frequency-near-1/2, not the spread. 0 false proofs: measurement + the exact
integral; the conclusion (annealed decay = equidistribution = Mahler, not FLP) is argued, FLP insufficiency shown.
"""
import math

def theta(j):
    return (pow(3, j) % (1 << (j + 2))) / (1 << (j + 2))

J = 2000
ths = [theta(j) for j in range(J)]

# (1) decay rate vs log2
import math
S = 0.0
checkpoints = [50, 200, 500, 1000, 2000]
print("(1) decay rate of -log(product)/J vs the equidistribution rate log 2 = 0.6931:")
print(f"    {'J':>5} {'(-ln prod)/J':>14} {'(=log2 iff equidist)':>22}")
acc = 0.0
for j in range(J):
    f = abs(math.cos(math.pi * ths[j]))
    acc += -math.log(max(f, 1e-300))
    if j + 1 in checkpoints:
        print(f"    {j+1:>5} {acc/(j+1):>14.5f} {'':>22}")
print(f"    integral_0^1 -log|cos(pi t)| dt = log 2 = {math.log(2):.5f}  (the rate IFF theta_j equidistributes)")

# (2) theta histogram -- equidistributed?
NB = 10
hist = [0]*NB
for t in ths: hist[min(int(t*NB), NB-1)] += 1
print(f"\n(2) theta_j = {{(3/2)^j/4}} histogram over {J} terms (uniform => {J//NB} each):")
print("    " + " ".join(f"{h:>5}" for h in hist))
print(f"    (visits the middle bins ~1/2 => the SOURCE of the decay; uniformity = Mahler.)")

# (3) FLP spread (support) -- satisfied, but is it the right quantity?
sp = max(ths) - min(ths)
mid_freq = sum(1 for t in ths if 0.25 <= t <= 0.75) / J
print(f"\n(3) FLP spread (support) = max-min = {sp:.4f}  (>= 1/3, FLP satisfied trivially)")
print(f"    frequency in the middle [1/4,3/4] (where |cos| is small) = {mid_freq:.4f}")
print(f"""
VERDICT (the FLP lead does NOT close the annealed decay):
  - The decay rate -log(prod)/J -> log 2 (above) EXACTLY when theta_j equidistributes; the integral
    of -log|cos(pi t)| is log 2. So the annealed product decay <=> EQUIDISTRIBUTION of {{(3/2)^j}} = MAHLER.
  - FLP gives only the SPREAD/support ({sp:.2f} here, >=1/3): support does NOT control the FREQUENCY near 1/2
    that drives the decay. (A spread-1 sequence could visit the middle rarely, or oscillate near {{0,1}}
    where |cos|~1, and fail to decay -- FLP cannot exclude this.) Same support-vs-frequency gap as the
    even-density itself.
  => The annealed carry balance is ITSELF Mahler-class (not an FLP-provable foothold). The exponential-sum
     form (exp_sum.py) is the right home, but the decay -- annealed OR orbit -- is the equidistribution.
     The FLP lead is closed: it bounds support, not the frequency the product decay needs.""")
