# BFLM grind: the action A=x(3/2) is SELF-DUAL (A-hat=x(3/2)), so BFLM's Fourier-decay-via-dual-orbit-spreading
# is circular for our rank-1 cyclic action. Empirically the Fourier coeffs decay ~1/sqrt(N) (the Mahler sum)
# but BFLM cannot force it (no random walk; self-dual). Positive residue: short-time spreading = Theta(log N) foothold.
import cmath, math
N=8000
def frac32(n): return (pow(3,n,2**n))/(2**n)   # exact frac((3/2)^n)
def nuhat(xi): return abs(sum(cmath.exp(2j*math.pi*(xi*frac32(n)%1.0)) for n in range(1,N+1)))/N
print("A-hat = x(3/2) (self-dual, exact). Empirical Fourier coeff |nu_N(xi)| vs 1/sqrt(N)=%.5f:"%(1/math.sqrt(N)))
for xi in (1,2,3,5):
    print(f"  xi={xi}: |nu_N(xi)|={nuhat(xi):.5f} (ratio {nuhat(xi)*math.sqrt(N):.2f})")
print("=> coeffs decay ~1/sqrt(N) (equidist holds) but it IS the Mahler sum; BFLM can't prove it (self-dual,")
print("   no random walk). Adaptation fails because A is self-dual; BFLM needs a rank-2 non-abelian (larger) dual.")
