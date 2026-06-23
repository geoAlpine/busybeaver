import math, cmath
# Object: r_n = 3^n mod 2^n. Study bit statistics + the "decoupling" idea (diagonal a=b is the only hard case).
N=4000

# 1) bit-density of r_n (fraction of 1-bits among the n bits) -> 1/2 ?
def bits_ones(n):
    r=pow(3,n,1<<n)
    return bin(r).count('1')
samp=[2**k for k in range(4,12)]  # n=16..2048
print("bit-density of r_n=3^n mod 2^n (ones/n -> 0.5?):")
for n in samp:
    o=bits_ones(n)
    print(f"  n={n:5d}: ones={o:5d} density={o/n:.4f}")

# 2) TOP bit b_{n-1} of r_n decides {(3/2)^n} in [0,1/2) vs [1/2,1). Is the sequence balanced & decorrelated?
top=[]
for n in range(2,N+2):
    r=pow(3,n,1<<n)
    top.append((r>>(n-1))&1)
ones=sum(top); 
print(f"\ntop-bit balance: {ones}/{len(top)} = {ones/len(top):.4f} (->0.5)")
# lag-1..4 autocorrelation of top-bit (centered)
import statistics
m=ones/len(top)
c=[t-m for t in top]
for lag in (1,2,3,4):
    num=sum(c[i]*c[i+lag] for i in range(len(c)-lag))
    den=sum(x*x for x in c)
    print(f"  autocorr lag {lag}: {num/den:+.4f}")

# 3) DECOUPLING test: fixed modulus 2^M, sum over n of e(3^n/2^M). For M fixed, n up to ord=2^(M-2):
#    complete-group sum should be tiny. Compare to DIAGONAL.
print("\ndecoupled sum |Σ_{n<L} e(3^n/2^M)| for fixed M (complete group => small):")
for M in (10,14,18):
    L=min(2**(M-2), 100000)
    S=0j
    x=1
    for n in range(L):
        x=(x*3)&((1<<M)-1)
        S+=cmath.exp(2j*math.pi*x/(1<<M))
    print(f"  M={M:2d} L={L:7d}: |S|={abs(S):8.2f} |S|/sqrt(L)={abs(S)/math.sqrt(L):.3f} |S|/L={abs(S)/L:.5f}")

# 4) SECOND MOMENT over a window of moduli (large-sieve flavor): average of |diagonal phase| structure.
#    Q: is the diagonal 'on average over nearby scales' tame? Compute for n in [N0,N0+W] the phases
#    3^n/2^(n+s) for small shifts s, see if shifting modulus decorrelates (=> diagonal is not special).
print("\nmodulus-shift decorrelation: corr of top-bit(3^n mod 2^n) vs bit(3^n mod 2^(n+s)):")
base=[ (pow(3,n,1<<n)>>(n-1))&1 for n in range(2,1000)]
for s in (1,2,4,8):
    shifted=[ (pow(3,n,1<<(n+s))>>(n+s-1))&1 for n in range(2,1000)]
    mb=sum(base)/len(base); ms=sum(shifted)/len(shifted)
    num=sum((base[i]-mb)*(shifted[i]-ms) for i in range(len(base)))
    den=math.sqrt(sum((b-mb)**2 for b in base)*sum((x-ms)**2 for x in shifted))
    print(f"  s={s}: corr(top bit, top bit at modulus 2^(n+{s}))={num/den:+.4f}")
