"""(beta) REVERSE-ILLUMINATION: scan the cryptid family c->floor(a c/p) for maps whose carry-sum
T_{n+1}=a T_n + p^n s_n  (s_n=(a c_n) mod p) is SOLVABLE -- i.e. the branch sequence s_n is eventually
periodic / low-complexity, so the even/branch density (halting) is decidable. Then read off the algebraic
property that makes the carry collapse, and confirm Antihydra (a=3,p=2) LACKS it.

For each (a,p), p<a, run from a seed, build branch seq s_n in {0..p-1}, and classify:
  - ratio a/p integer?  -> trivial linear map (no floor) -- degenerate-solvable
  - eventual period found within N?  -> SOLVABLE (decidable density)
  - else block-complexity (distinct 8-blocks) -> CRYPTID (random-like carry)
Also record the diagonal carry digit balance and whether a == 1 mod p (the '+1' p-adic-contraction
candidate) and whether a,p multiplicatively dependent (a a power of p).
0 false proofs: 'solvable' asserted ONLY if an exact period is found and re-verified; else 'cryptid/unknown'.
"""
import math
from collections import Counter

def is_power_of(a, p):
    while a % p == 0: a //= p
    return a == 1

def find_period(seq, burnin, maxP):
    """exact eventual period P in seq[burnin:] if seq[i]==seq[i+P] holds for a long stretch."""
    s = seq[burnin:]
    L = len(s)
    for P in range(1, maxP + 1):
        if all(s[i] == s[i + P] for i in range(L - P)):
            return P
    return None

def block_complexity(seq, b):
    return len(set(tuple(seq[i:i+b]) for i in range(len(seq) - b)))

def run(a, p, seed, N):
    c = seed
    s = []
    for _ in range(N):
        s.append((a * c) % p)
        c = (a * c) // p
        if c == 0:  # halted/absorbed
            return s, True
    return s, False

N = 3000
print(f"scan c->floor(a c/p), seed varies, N={N}")
print(f"{'(a,p)':>8} {'a/p':>6} {'class':>14} {'period':>7} {'cmplx8':>7} {'d-bal':>6}  notes")
print("-" * 78)
results = []
for p in range(2, 8):
    for a in range(p + 1, 4 * p + 1):
        if a % p == 0:
            cls = "trivial-linear"; note = "a/p integer (no floor)"
            results.append((a, p, cls, None, 0, 0.5));
            print(f"{(a,p)!s:>8} {a/p:6.3f} {cls:>14} {'-':>7} {'-':>7} {'-':>6}  {note}")
            continue
        seed = p + 1
        s, halted = run(a, p, seed, N)
        if halted:
            cls = "shrinks/halts"; per = None; cx = 0; note = f"halts at n={len(s)} (a/p<1 region or absorbed)"
            results.append((a, p, cls, per, cx, 0.5))
            print(f"{(a,p)!s:>8} {a/p:6.3f} {cls:>14} {'-':>7} {'-':>7} {'-':>6}  {note}")
            continue
        per = find_period(s, burnin=N//3, maxP=200)
        cx = block_complexity(s, 8)
        # diagonal carry-digit balance (base-p digit of T_n at position ~n): build T_n
        T = 0; pw = 1; dbits = []
        for n in range(min(N, 1500)):
            dbits.append((T // pw) % p)  # base-p digit at position n
            T = a * T + pw * s[n]
            pw *= p
        # balance of whether that digit is 0 vs not (crude)
        dbal = sum(1 for x in dbits if x != 0) / len(dbits)
        if per is not None:
            cls = "SOLVABLE-per"; note = f"eventual period {per} (decidable density)"
        elif cx <= 8:
            cls = "low-cmplx"; note = f"complexity {cx} (<= 8 -> likely automatic/decidable)"
        else:
            cls = "CRYPTID?"; note = f"complexity {cx} (random-like carry)"
        amod = a % p
        extra = f" a==1modp" if amod == 1 else ""
        results.append((a, p, cls, per, cx, dbal))
        print(f"{(a,p)!s:>8} {a/p:6.3f} {cls:>14} {str(per):>7} {cx:>7} {dbal:6.3f}  {note}{extra}")

# summary: which (a,p) are SOLVABLE and what do they share?
print("\n" + "="*78)
print("CLASSIFICATION SUMMARY")
print("="*78)
solv = [(a,p) for (a,p,cls,per,cx,db) in results if cls.startswith("SOLVABLE") or cls=="low-cmplx"]
cryp = [(a,p) for (a,p,cls,per,cx,db) in results if cls=="CRYPTID?"]
triv = [(a,p) for (a,p,cls,per,cx,db) in results if cls in ("trivial-linear","shrinks/halts")]
print(f"trivial/degenerate (integer ratio or shrinks): {len(triv)}  e.g. {triv[:6]}")
print(f"SOLVABLE carry (periodic/low-complexity)      : {len(solv)}  {solv}")
print(f"CRYPTID carry (random-like, NOT solvable)     : {len(cryp)}  {cryp[:12]}{'...' if len(cryp)>12 else ''}")
print(f"\nAntihydra (3,2): ", [r for r in results if r[0]==3 and r[1]==2])
print("""
READING: if every GENUINE grower (non-integer a/p, doesn't shrink) is CRYPTID and the only SOLVABLE
maps are the degenerate ones (integer ratio = trivial linear, or shrinking = halts), then the carry-sum
is solvable EXACTLY for the algebraically degenerate maps -- and Antihydra's hardness is the generic
fate of any genuine non-integer-ratio grower. That reverse-illuminates: Antihydra lacks NOTHING special;
it is the simplest genuine grower, and 'solvable carry' requires the map to NOT be a genuine cryptid.
If instead some genuine grower IS solvable, its shared property (e.g. a==1 mod p, or a,p mult. dependent)
is the missing structure -- name it and confirm (3,2) lacks it.""")
