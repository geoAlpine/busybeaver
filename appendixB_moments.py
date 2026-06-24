# Appendix B: cylinder-visit moments M_2, M_4 of the Antihydra renewal sequence vs random-iid model.
from collections import Counter
c=8; renew=[]; J=8000
while len(renew)<J:
    if c%2==0: renew.append(c//2)
    c=(3*c)//2
def rand_M2(k):
    m=2**k; return J + J*(J-1)/m
def rand_M4(k):
    m=2**k
    return J + 7*J*(J-1)/m + 6*J*(J-1)*(J-2)/m**2 + J*(J-1)*(J-2)*(J-3)/m**3
print(f"{'k':>2} {'M2_obs':>10} {'M2_rand':>10} {'r':>5}   {'M4_obs':>16} {'M4_rand':>16} {'r':>5}")
for k in (2,4,6,8,10,12,14):
    cnt=Counter(x%(2**k) for x in renew)
    M2=sum(v*v for v in cnt.values()); M4=sum(v**4 for v in cnt.values())
    print(f"{k:>2} {M2:>10d} {rand_M2(k):>10.0f} {M2/rand_M2(k):>5.3f}   {M4:>16d} {rand_M4(k):>16.0f} {M4/rand_M4(k):>5.3f}")
