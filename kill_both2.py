import math, numpy as np
a=math.log2(3/2)
N=120000
fr=[(n*a)%1.0 for n in range(1,N+1)]
mant=[2**f for f in fr]
print("PROVABLE (Weyl/Benford via mult. independence of 2,3): top-K bits of (3/2)^n equidistribute:")
for K in (1,2,5,10):
    bits=[int(m*2**K)&1 for m in mant]
    print(f"  bit at FIXED depth K={K:2d} from top: density {sum(bits)/N:.4f} (->0.5 PROVABLE)")
def diag(n):
    r=pow(3,n,1<<n); return (r>>(n-1))&1
db=[diag(n) for n in range(2,N)]
print(f"\nKERNEL target: diagonal bit at MOVING depth ~0.585n: density {sum(db)/len(db):.4f} (UNPROVABLE)")
print("\nGAP (exact): PROVABLE = bit at any FIXED depth-from-top; OPEN = bit at depth GROWING with n.")
print("  Mult. independence gives the TOP (fixed) bits free; stops exactly at the moving diagonal.")
# joint probe (fast modular)
def dtrit2(n):  # is n-th base-3 digit of 8^n equal to 2?
    return 1 if (pow(8,n,3**(n+1))//3**n)%3==2 else 0
M=20000
m1=np.array([diag(n) for n in range(2,M)])
m2=np.array([dtrit2(n) for n in range(2,M)])
print(f"\nKILL-BOTH joint probe: corr(monster1 bit, monster2 digit=2) = {np.corrcoef(m1,m2)[0,1]:+.4f}")
print("  (~0 => the two diagonals are statistically INDEPENDENT: no joint sum-rule linking them.")
print("   So 'one relation kills both' has no handle; but both have the SAME obstruction type")
print("   (moving diagonal of a multiplicative orbit) => one METHOD for that type kills both.)")
