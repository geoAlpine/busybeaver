# Direct attack on (alpha) = "force the single seed-6 orbit's empirical measure to Haar".
# Two EXACT verified identities + a verified circularity result.
import math
def v2(x):
    x=abs(int(x))
    if x==0: return 10**9
    r=0
    while x%2==0: x//=2; r+=1
    return r
def log_big(x):
    bl=x.bit_length()
    return math.log(x) if bl<=60 else math.log(x>>(bl-60))+(bl-60)*math.log(2)
# (I) sum_j v2(3 c'_j-1) == #odd  =>  avg jump = #odd/#even  exactly
c=8; n=200000; ne=no=sumD=0; cur=c
for _ in range(n):
    if cur%2==0: ne+=1; sumD+=v2(3*(cur//2)-1)
    else: no+=1
    cur=(3*cur)//2
print(f"(I) sum D_j == #odd : {sumD==no} (sumD={sumD},#odd={no}) => avg jump = #odd/#even = {sumD/ne:.5f}")
# (II) telescoping 2c'_{j+1}-1 == (3/2)^{D_j}(3c'_j-1);  (III) growth is an identity (circular)
c=8; renew=[]
while len(renew)<4000:
    if c%2==0: renew.append(c//2)
    c=(3*c)//2
b=[2*cp-1 for cp in renew]; D=[v2(3*cp-1) for cp in renew]
tele=all(2*renew[j+1]-1 == 3**D[j]*((3*renew[j]-1)//2**D[j]) for j in range(len(renew)-1))
print(f"(II) telescoping 2c'_(j+1)-1==3^D u_j : {tele}")
eps=sum(math.log1p(1.0/(3*b[j]) if b[j].bit_length()<1000 else 0.0) for j in range(3999))
J=3999; lhs=log_big(b[J]); rhs=math.log(1.5)*(J+sum(D[:J]))+eps+log_big(b[0])
print(f"(III) log b_J == log(3/2)(J+sumD)+eps+const (eps->{eps:.4f} bounded): {abs(lhs-rhs)<0.01}")
print("     => n=J+sumD reappears; growth gives NO bound on sumD. Counting/growth CIRCULAR for (alpha).")
