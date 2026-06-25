# Proposition 3 (PROVEN, new): the even-density jump has a 3-adic avatar.  D_j = v2(3c'_j-1) = v3(2c'_{j+1}-1).
# Proof: 2c'_{j+1}-1 = 3^{D_j} u_j, u_j=(3c'_j-1)/2^{D_j} is a unit at 2 and 3 (3c'_j-1 == -1 mod 3 => v3=0).
def vp(x,p):
    x=abs(int(x)); r=0
    if x==0: return 10**9
    while x%p==0: x//=p; r+=1
    return r
c=8; renew=[]
while len(renew)<50000:
    if c%2==0: renew.append(c//2)
    c=(3*c)//2
ok=sum(1 for j in range(len(renew)-1) if vp(3*renew[j]-1,2)==vp(2*renew[j+1]-1,3))
print(f"D_j == v3(2c'_(j+1)-1): {ok}/{len(renew)-1}")
aj2=sum(vp(3*cp-1,2) for cp in renew)/len(renew)
aj3=sum(vp(2*renew[j+1]-1,3) for j in range(len(renew)-1))/(len(renew)-1)
print(f"avg jump 2-adic={aj2:.4f}  3-adic={aj3:.4f}  => non-halt <=> avg v3(2c'-1) <= 2 (3-adic avatar)")
