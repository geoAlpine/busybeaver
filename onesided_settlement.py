# Settlement of #2: the factor-2 margin in 'avg jump <= 2' translates to a one-sided 2x-anti-concentration
# target (N_k/J <= 2*2^-k), STRICTLY weaker than equidistribution -- but the upper bound on each specific small
# cylinder IS a specified-orbit cylinder-frequency statement (= the additive energy), same class as equidist.
# So the margin relaxes the constant (2x vs 1x), not the KIND of control. Equi-difficult vs current tools.
def v2(x):
    x=abs(int(x)); r=0
    if x==0: return 10**9
    while x%2==0: x//=2; r+=1
    return r
c=8; renew=[]
while len(renew)<50000:
    if c%2==0: renew.append(c//2)
    c=(3*c)//2
J=len(renew)
print("k  N_k/J   2^-k   obs/Haar   2x-budget")
for k in range(1,9):
    Nk=sum(1 for cp in renew if v2(3*cp-1)>=k)/J
    print(f"{k}  {Nk:.4f}  {2.0**-k:.4f}  {Nk/2.0**-k:.3f}   {2*2.0**-k:.4f}")
print("avg jump<=2  <=  N_k/J <= 2*2^-k for all k (sum=2). One-sided 2x-anti-concentration = strictly weaker")
print("than equidist, but the per-cylinder upper bound = the additive energy = specified-orbit frequency control,")
print("same class. Margin relaxes the constant, not the kind => weaker TARGET, not easier PROOF. #2 settled.")
