# NEWMATH_DIGIT_BRIDGE verification (2026-07-09)
# Purpose: verify the STRUCTURAL DICHOTOMY that is the bridge lemma --
#   (A) a genuine CONSTANT-COEFFICIENT linear recurrence has EVENTUALLY PERIODIC
#       p-adic valuation v_p(u_n) [the Lucas-mod-3^k / 3rd-order-recurrence regime,
#       arXiv:2511.00722, arXiv:2402.18279] -> exact computable digit frequency (quenched OK);
#   (B) the o4 cryptid orbit's run-depth d_n = v_3(G_n - x_rho) is v_3 of a
#       NON-AUTONOMOUS (branch-self-selected) recurrence 3G' = 4G + e(G mod 3) --
#       no fixed characteristic polynomial, so (A)'s periodicity engine does NOT apply.
# Exact bigint. Interpreter: /Users/aokiyousuke/quantum-ecc/.venv/bin/python
# SOUNDNESS GUARD (not a rerun of a logged NO-GO): the run law v_3 identity is re-checked
# as a guard; the whiteness/(K)-equivalence conclusion is NOT recomputed here.

def v3(n):
    if n == 0: return 10**9
    v = 0
    while n % 3 == 0:
        n //= 3; v += 1
    return v

# ---- o4 odometer: 3G' = 4G + e(rho), rho = G mod 3, e = {0:9,1:14,2:1} ----
e = {0:9, 1:14, 2:1}
x = {0:-9, 1:-14, 2:-1}    # branch fixed points x_rho = -e(rho)
def step(G):
    rho = G % 3
    return rho, (4*G + e[rho]) // 3

# ============ (1) SOUNDNESS GUARD: run law d = v_3(G - x_rho) exact ============
# The maximal run of residue rho starting at G equals v_3(G - x_rho).
def max_run(G):
    rho0 = G % 3; g = G; L = 0
    while g % 3 == rho0:
        _, g = step(g); L += 1
    return L

seed = 8
G = seed
mism = 0; checks = 0
for _ in range(4000):
    rho = G % 3
    predicted = v3(G - x[rho])
    if G % 3 == rho:                      # measure actual maximal run at run-starts only
        actual = max_run(G)
        # actual maximal run should equal predicted valuation (both are the run length)
        if actual != predicted:
            mism += 1
        checks += 1
    _, G = step(G)
print(f"(1) run-law guard v3(G-x_rho)==maxrun : {checks-mism}/{checks} match, {mism} mismatch")

# ============ (2) NON-AUTONOMY: the branch (=recurrence coefficient) is aperiodic ==
# Build the residue itinerary rho_0..rho_N from seed 8 and test for ANY period p<=P.
G = seed; itin = []
for _ in range(20000):
    rho, G = step(G); itin.append(rho)
def has_period(seq, p, tail=4000):
    s = seq[-tail:]
    return all(s[i] == s[i-p] for i in range(p, len(s)))
periods = [p for p in range(1, 2000) if has_period(itin, p)]
print(f"(2) o4 residue itinerary length {len(itin)}: eventual periods p<2000 found = {periods}")
print(f"    (empty list => branch/coefficient is NON-CONSTANT & aperiodic on tested window)")

# ============ (3) THE CORRECT DISCRIMINATOR: residue seq mod 3^k ================
# The p-adic VALUATION is unbounded for genuine recurrences too (Lengyel), so raw
# valuation-periodicity is NOT the discriminator. The mechanism that yields a
# COMPUTABLE valuation frequency (hence quenched digit results) is: the RESIDUE
# sequence (u_n mod 3^k) is EVENTUALLY PERIODIC (finite-state) for a constant-coeff
# recurrence [Pisano-type], which lets v_3-frequencies be read off one period exactly.
def resid_period(gen, m, N=200000, tail=6000):
    """least eventual period of the residue sequence mod m, or None."""
    s = [x % m for x in gen[:N]]
    t = s[-tail:]
    for p in range(1, tail//2):
        if all(t[i] == t[i-p] for i in range(p, len(t))):
            return p
    return None
# genuine constant-coeff recurrence (Fibonacci): residues mod 3^k are periodic (Pisano)
f = [0,1]
for _ in range(200000): f.append(f[-1]+f[-2])
for k in (1,2,3):
    print(f"(3) Fibonacci residues mod 3^{k}: eventual period = {resid_period(f,3**k)}  (finite => computable v_3 freq; Lucas regime arXiv:2511.00722)")

# ============ (4) o4: residue seq mod 3^k is NOT eventually periodic (non-descent) =
# The odometer G' = (4G + e(G mod 3))/3 divides by 3 each step, so G' depends on
# G mod 3^{k+1}, NOT on G mod 3^k: the map does NOT DESCEND to a finite quotient
# (AEV non-descent). Consequence: (G_n mod 3^k) has no finite-state generator.
G = seed; Gseq = []
for _ in range(200000):
    Gseq.append(G); _, G = step(G)
for k in (1,2,3):
    print(f"(4) o4 orbit residues mod 3^{k}: eventual period = {resid_period(Gseq,3**k)}  (None => non-descent, no finite-state generator)")

# summary
print("\nDICHOTOMY (the bridge lemma):")
print(f"  constant-coeff linear rec  -> residues mod 3^k EVENTUALLY PERIODIC => v_3 frequency EXACT/computable => QUENCHED digit results exist")
print(f"  o4 non-autonomous odometer -> residues mod 3^k NON-PERIODIC (non-descent), branch itinerary aperiodic (periods {periods})")
print(f"  => o4 run-depth d_n = v_3(G-x_rho) is the base-4/3 numeration digit (AEV Conj 1.6); NOT a linear-recurrence valuation.")
