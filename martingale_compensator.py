"""Wall (B) martingale / compensator numerics  (v2, correct low-bit tracking).

W_N = sum_{n<N} (-1)^{r_n},  r_n = c_n mod 2,  c_0=8, c_{n+1}=floor(3 c_n/2).
r_n = bit_{n+3}(3^n) = the moving-MIDDLE diagonal bit.

ANY filtration (F_n) gives  W_N = C_N + M_N,
   C_N = sum E[(-1)^{r_n}|F_{n-1}]  (predictable COMPENSATOR),
   M_N = martingale residual (|incr|<=2 -> Azuma O(sqrt(N log N)) IN A PROBABILITY MODEL).
For one deterministic orbit there is no measure, so we measure a GENUINE causal predictor:
learn kernel g(s)=E[f|state] on FIRST half, apply OUT-OF-SAMPLE on SECOND half.

Decisive honest metric = out-of-sample R^2:
   R2 = 1 - sum_held (sign - g(s))^2 / sum_held (sign - mean)^2.
   R2 <= 0  <=>  filtration has NO predictive power over the parity  <=>  compensator is noise,
   residual = full sum, the hard cancellation is NOT removed (stays = Mahler middle digit).

Filtrations:
  (i)   state = TRUE c_n mod 2^k  (low bits of orbit; literally contains r_n=bit0)  -> vacuous.
  (ii)  state = T_n mod 2^k       (low bits of carry; old history)                  -> the genuine test.
  (iii) state = (top m bits of c_n, bits 1..m of c_n) = BOTH proven footholds combined.
Exact arithmetic. 0 false proofs: every number is a finite-sample statistic with its sqrt(N) band.
"""
import math, sys
from collections import defaultdict

N = int(sys.argv[1]) if len(sys.argv) > 1 else 200000

f = bytearray(N)           # parity r_n
clow = [0]*N               # TRUE c_n mod 2^12  (from big-int)
Tlow = [0]*N               # T_n mod 2^12  (exact: mult-by-3, no division)
topbot = [0]*N
M3 = 6
KT = 12; MT=(1<<KT)-1
c = 8; T = 0
for n in range(N):
    r = c & 1
    f[n] = r
    clow[n] = c & MT
    Tlow[n] = T & MT
    bl = c.bit_length()
    top = (c >> (bl - M3)) if bl >= M3 else c
    low = (c >> 1) & ((1<<M3)-1)
    topbot[n] = (top << M3) | low
    T = (3*T + ((1 << n) & MT) * r) & MT     # exact low bits, no division
    c = c + (c >> 1)                          # floor(3c/2), full big-int

sign = [1 - 2*int(b) for b in f]
W = sum(sign); sq = math.sqrt(N)
print(f"N={N}  W_N={W}  W/N={W/N:+.5f}  sqrt(N)={sq:.1f}  W/sqrt(N)={W/sq:+.2f}  odd-density={sum(f)/N:.5f}\n")

half = N//2; nh = N-half; sqh = math.sqrt(nh)
Wsh = sum(sign[half:]); meanh = Wsh/nh
sstot = sum((s-meanh)**2 for s in sign[half:])   # held-out total SS (baseline: predict mean)

def test(name, state, desc):
    s1=defaultdict(int); n1=defaultdict(int)
    for n in range(half):
        st=state[n]; s1[st]+=sign[n]; n1[st]+=1
    g={st:s1[st]/n1[st] for st in n1}
    C=0.0; ssres=0.0; covered=0
    for n in range(half,N):
        st=state[n]; gh=g.get(st,0.0)
        if st in g: covered+=1
        C+=gh; ssres+=(sign[n]-gh)**2
    R=Wsh-C
    R2 = 1 - ssres/sstot if sstot>0 else 0.0
    print(f"[{name}] {desc}  #states={len(n1)}  avg_cnt={half/max(len(n1),1):.0f}")
    print(f"   OOS compensator C={C:+.1f}  residual R={R:+.1f}   (baseline |W'|={abs(Wsh):.0f}, sqrt(N/2)={sqh:.0f})")
    print(f"   |C|/sqrt={abs(C)/sqh:.2f}  |R|/sqrt={abs(R)/sqh:.2f}  OUT-OF-SAMPLE R^2={R2:+.5f}   ({'PREDICTIVE' if R2>0.001 else 'NO predictive power'})\n")

print("="*80)
print("(i) state = TRUE c_n mod 2^k  (low bits of ORBIT; contains bit0 = r_n exactly)")
print("="*80)
for k in (4,8,12):
    test(f"i:c%2^{k}", [v&((1<<k)-1) for v in clow], f"k={k}")

print("="*80)
print("(ii) state = T_n mod 2^k  (low bits of CARRY = old history; r_n is a HIGH bit of T)")
print("="*80)
for k in (4,8,12):
    test(f"ii:T%2^{k}", [v&((1<<k)-1) for v in Tlow], f"k={k}")

print("="*80)
print(f"(iii) state = (top {M3} bits, bits 1..{M3}) of c_n = BOTH proven footholds together")
print("="*80)
test(f"iii:top{M3}+bot{M3}", topbot, f"2*{M3}={2*M3} foothold bits")

print("="*80)
print("STRUCTURAL: is T_n mod 2^k a deterministic x3-rotation (no live orbit info)?")
print("="*80)
for k in (8,12):
    M=(1<<k)-1; st=[v&M for v in Tlow]
    viol=sum(1 for n in range(k,N-1) if (3*st[n])&M != st[n+1])
    seen={}; per=None
    for n in range(k,N):
        if st[n] in seen: per=n-seen[st[n]]; break
        seen[st[n]]=n
    print(f"  k={k}: T_{{n+1}}==3T_n mod 2^k for n>=k -> violations={viol}/{N-1-k};  eventual period={per}")
print("  => low carry bits are a FIXED rotation (function of n only): conditioning on them")
print("     carries NO information about the live middle parity bit.")
