"""M4 main line P2 (pure algebra): does the integrality congruence T_n == 8*3^n mod 2^n FORBID a
biased parity? Forbidden structure = {biased parity} + {dual carry congruence} + {integer output}.
First experiment (per the meeting): feed ARTIFICIAL biased parity sequences r_i, build the carry
T_n = sum_{i<n} 3^{n-1-i} 2^i r_i, and test how long T_n == 8*3^n mod 2^n can hold. The region of
bias that CANNOT satisfy it = the forbidden-address candidate.

KEY hand-derivation (verified below): T_n = 3 T_{n-1} + 2^{n-1} r_{n-1}, and with T_{n-1} == 8*3^{n-1}
mod 2^{n-1}, the congruence T_n == 8*3^n mod 2^n forces  r_{n-1} == s mod 2,  where
s = (T_{n-1} - 8*3^{n-1})/2^{n-1} mod 2. So each parity bit is UNIQUELY FORCED by the congruence
(given the history). => the integrality-compatible parity sequence is UNIQUE (= the real orbit).
We test what this means for 'biased => non-integer'.
"""
import numpy as np
def real_orbit_parity(N):
    c=8; r=[]
    for _ in range(N): r.append(c&1); c=(3*c)//2
    return r

N=2000
# (1) the congruence forces each bit: given history T_{n-1}, the unique r_{n-1}.
def forced_bit(Tprev, n):
    # s = (T_{n-1} - 8*3^{n-1})/2^{n-1} mod 2 ; forced r_{n-1} = s mod 2
    if n==1:
        # T_1 = 8*3 mod 2 ... base: r_0 forced so that T_1 == 8*3 mod 2; T_1 = 2^0 r_0 = r_0; 8*3=24 even -> r_0=0
        return (24 - Tprev)  # handled below generically
    diff = Tprev - 8*pow(3,n-1)
    s = (diff // (1<<(n-1))) & 1
    return s & 1

# reconstruct the unique integrality-compatible parity by forcing each bit, compare to real orbit
T=0; rec=[]
for n in range(1,N+1):
    # need r_{n-1} so that T_n = 3T + 2^{n-1} r == 8*3^n mod 2^n
    base = 3*T  # mod 2^n
    target = 8*pow(3,n)
    # 2^{n-1} r == target - base mod 2^n  => r == ((target-base)/2^{n-1}) mod 2
    need = (target - base) % (1<<n)
    r = (need // (1<<(n-1))) & 1
    rec.append(r)
    T = 3*T + (1<<(n-1))*r
real = real_orbit_parity(N)
match = sum(1 for a,b in zip(rec,real) if a==b)
print("="*78)
print("M4-P2: the integrality congruence T_n == 8*3^n mod 2^n FORCES each parity bit uniquely")
print("="*78)
print(f"\n(1) reconstructed unique integrality-compatible parity vs the real orbit's parity:")
print(f"    match = {match}/{N}  ({'IDENTICAL => unique solution = the real orbit' if match==N else 'differ'})")
# verify the real orbit satisfies the congruence
T=0; ok=True
for n in range(1,N+1):
    T=3*T+(1<<(n-1))*real[n-1]
    if T % (1<<n) != (8*pow(3,n)) % (1<<n): ok=False
print(f"    real orbit satisfies T_n==8*3^n mod 2^n for all n<= {N}: {ok} (automatic = integrality)")

# (2) feed ARTIFICIAL biased parity: when does it first VIOLATE the congruence?
print(f"\n(2) artificial biased parity sequences -> first n where T_n != 8*3^n mod 2^n (violation):")
print(f"{'bias model':>22} {'first violation n':>18}")
rng=np.random.default_rng(0)
def first_violation(rseq):
    T=0
    for n in range(1,len(rseq)+1):
        T=3*T+(1<<(n-1))*int(rseq[n-1])   # Python big-int
        if T % (1<<n) != (8*pow(3,n)) % (1<<n): return n
    return None
models={
 'Bernoulli p=0.5': (rng.random(N)<0.5).astype(int),
 'Bernoulli p=0.4 (biased)': (rng.random(N)<0.4).astype(int),
 'Bernoulli p=0.3 (halt-like)': (rng.random(N)<0.3).astype(int),
 'all-0 (max even)': np.zeros(N,int),
 'all-1 (max odd=halt)': np.ones(N,int),
 'real orbit': np.array(real),
}
for name,seq in models.items():
    fv=first_violation(list(seq))
    print(f"{name:>22} {str(fv):>18}")

print("\n" + "="*78)
print("READING (honest)")
print("="*78)
print("The congruence FORCES each parity bit uniquely => exactly ONE integrality-compatible parity")
print("sequence exists, and it IS the real orbit. So ANY artificial biased sequence (!= orbit) VIOLATES")
print("the congruence almost immediately (n=O(1)). This is genuine RIGIDITY: 'arbitrary biased parity")
print("+ integer output' is IMPOSSIBLE -- the integer constraint pins the whole sequence.")
print("BUT the honest limit: the REAL orbit's parity (whatever its even-density) DOES satisfy the")
print("congruence (automatically). So integrality forces THE orbit but does NOT bound ITS bias --")
print("'biased => non-integer' is FALSE for the orbit's own bias (the orbit is an integer; whether its")
print("even-density >= 1/3 is exactly the open question, not decided by integrality). P2 gives RIGIDITY")
print("(unique orbit), not a bias bound. The forbidden structure forbids OTHER sequences, not the orbit's.")
print("=> P2's value: it converts 'bound the orbit's bias' into 'the orbit is the unique integer solution")
print("of the congruence' -- a purely arithmetic re-encoding. The next question (P3): does the unique")
print("solution's growth/run-length structure FORCE even-density >= 1/3? (integrality + valuation budget).")
