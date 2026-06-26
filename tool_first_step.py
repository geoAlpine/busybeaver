# First step of the one-sided anti-concentration TOOL: map structural ingredients, find the binding content.
# Finding: avg jump=sum_k N_k/J is SMALL-k dominated; the trivial per-frequency bound gives sum_{k<=3}<=3>2,
# so the proof needs small-k freqs ~Haar (= equidistribution). Large-k is negligible for the sum (Baker-attackable
# but USELESS for the complete proof). So the tool's first brick IS the small-k equidistribution = the wall.
def v2(x):
    x=abs(int(x)); r=0
    if x==0: return 10**9
    while x%2==0: x//=2; r+=1
    return r
c=8; renew=[]
while len(renew)<50000:
    if c%2==0: renew.append(c//2)
    c=(3*c)//2
J=len(renew); 
Nk=[sum(1 for cp in renew if cp%2**k==pow(3,-1,2**k))/J for k in range(1,30)]
print(f"avg jump = sum N_k/J = {sum(Nk):.4f}")
print(f"  small-k (k=1,2,3) contributes {sum(Nk[:3]):.3f} of {sum(Nk):.3f}; large-k tail (k>=10) = {sum(Nk[9:]):.4f} (negligible)")
print(f"  trivial bound: N_k/J<=1 each => sum_(k<=3) <= 3 > 2, so small-k MUST be ~Haar (= equidistribution).")
print(f"  amortized sparsity: ~{J/(renew[-1].bit_length()-renew[0].bit_length()):.3f} points/octave (growth>2, structural).")
print("VERDICT: the tool's binding content is small-k equidistribution; large-k is negligible for avg jump.")
print("No tractable first brick -- the first brick IS the wall. (Large-k Baker = a separate partial, useless here.)")
