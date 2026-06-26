"""NEW MATH: the conditional-bias operator B_k (the meeting's decision -- NON-circular definition).
B_k f = E[ middle_digit_k | foothold data ] - E[middle_digit_k];  sigma(k) = ||B_k||.
Foothold data = the archimedean phase phi_n = frac(log2 c_n) (= {n log2 3 + const}; the TOP bits,
controlled by the foothold). middle/low bit = the injection target (a low/middle bit of c_n = the
moving-middle-digit). sigma(k) measures whether KNOWING the foothold lets you PREDICT the middle bit
-- this does NOT assume Mahler (it measures COUPLING), so it cannot smuggle the core (the meeting's
key worry). If sigma ~ 0: foothold does not predict the middle bit (fresh w.r.t. foothold, non-circular
evidence). If sigma > control: a real foothold->middle coupling = a genuine handle.
We measure for the REAL orbit (lambda=0) vs a SHUFFLE control (bit independent of phase).
"""
import numpy as np, math

N=400000
c=8; vals=[]
for _ in range(N):
    vals.append(c); c=(3*c)//2

# foothold phase phi_n = frac(log2 c_n) in [0,1)  (top-bit / archimedean control)
def phase(c):
    bl=c.bit_length(); sh=max(0,bl-60)
    mant=(c>>sh)/(1<<(min(bl,60)-1))
    return math.log2(mant)
phi=np.array([phase(c) for c in vals])

def low_bit(c,k):    # k-th low bit (k>=1); k small = injection / 2-adic low (= moving-middle-digit of 3^n)
    return (c>>(k-1))&1
def mid_bit(c,frac): # genuine middle digit at position frac*bitlen
    bl=c.bit_length(); p=int(frac*bl)
    return (c>>p)&1

def sigma_op(bits, phi, B):
    # bin n by phase into B bins; bias_b = E[bit|bin]-1/2; sigma_max = max|bias|, sigma_L2 = RMS bias
    idx=np.clip((phi*B).astype(int),0,B-1)
    biases=[]; weights=[]
    for b in range(B):
        sel=idx==b
        if sel.sum()>=200:
            biases.append(bits[sel].mean()-0.5); weights.append(sel.sum())
    biases=np.array(biases); weights=np.array(weights)
    smax=np.max(np.abs(biases)); sL2=math.sqrt(np.sum(weights*biases**2)/np.sum(weights))
    return smax, sL2

print("="*80)
print("B_k conditional-bias operator: sigma(k) = ||E[middle bit | foothold phase] - 1/2||")
print("(does the foothold predict the middle bit? sigma~control => NO => fresh, non-circular)")
print("="*80)
rng=np.random.default_rng(0)

print(f"\nN={N}.  Low bit k (=injection target = moving-middle-digit of 3^n), B phase-bins:")
print(f"{'k':>3} {'B bins':>7} {'orbit sigma_max':>15} {'ctrl sigma_max':>14} {'orbit sigma_L2':>14} {'ctrl sigma_L2':>13} {'coupling?':>10}")
for k in (1,2,3,5,8):
    bits=np.array([low_bit(c,k) for c in vals])
    ctrl=bits.copy(); rng.shuffle(ctrl)   # bit independent of phase
    for B in (64, 400):
        om,ol=sigma_op(bits,phi,B); cm,cl=sigma_op(ctrl,phi,B)
        coup = "NO (fresh)" if ol<cl*1.3+0.001 else "YES coupling"
        print(f"{k:>3} {B:>7} {om:15.5f} {cm:14.5f} {ol:14.5f} {cl:13.5f} {coup:>10}")

print(f"\nGenuine MIDDLE digit (position frac*bitlen), B=400 phase-bins:")
print(f"{'frac':>5} {'orbit sigma_L2':>14} {'ctrl sigma_L2':>13} {'coupling?':>12}")
for frac in (0.2,0.4,0.6,0.8):
    bits=np.array([mid_bit(c,frac) for c in vals])
    ctrl=bits.copy(); rng.shuffle(ctrl)
    ol=sigma_op(bits,phi,400)[1]; cl=sigma_op(ctrl,phi,400)[1]
    coup="NO (fresh)" if ol<cl*1.3+0.001 else "YES coupling"
    print(f"{frac:>5} {ol:14.5f} {cl:13.5f} {coup:>12}")

print("\n" + "="*80)
print("READING")
print("="*80)
print("If orbit sigma ~ control sigma at every k/position: the foothold phase does NOT predict the")
print("middle/low bit => B_k ~ 0 (non-circular: we did NOT assume equidistribution, we measured that")
print("the KNOWN foothold carries no info about the middle bit). This means the middle bit is 'fresh")
print("relative to the foothold' -- but sigma~0 is NECESSARY not sufficient (the bit could be biased")
print("in a way invisible to the phase). Still: B_k is well-defined, non-circular, and at the noise")
print("floor => the meeting's worry (smuggling Mahler) is AVOIDED, and the operator exists to build on.")
print("If orbit sigma > control somewhere: a real foothold->middle coupling = a genuine new HANDLE")
print("(the foothold would partially predict the middle bit -- the first crack toward the bridge).")
