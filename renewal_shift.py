# Verify: induced map F advances the renewal sequence (c'_{i+1}=F(c'_i)), so
# additive energy E_2(k) = #{(i,j): v2(c'_i-c'_j)>=k} = renewal self-correlation.
def v2(x):
    x=abs(int(x))
    if x==0: return 99
    r=0
    while x%2==0: x//=2; r+=1
    return r
c=8; renew=[]
while len(renew)<2000:
    if c%2==0: renew.append(c//2)
    c=(3*c)//2
def F(cp):
    D=v2(3*cp-1); num=3**(D+1)*cp-3**D+2**D; den=2**(D+1)
    assert num%den==0; return num//den
ok=sum(1 for i in range(len(renew)-1) if F(renew[i])==renew[i+1])
print(f"c'_(i+1)==F(c'_i): {ok}/{len(renew)-1}")
J=400
for k in (4,6,8,10):
    d=sum(1 for i in range(J) for j in range(J) if (renew[i]-renew[j])%(2**k)==0)
    print(f"k={k:2d} collisions(ordered)={d:6d}  ~ J + J^2/2^k = {J + J*J/2**k:.0f}")
