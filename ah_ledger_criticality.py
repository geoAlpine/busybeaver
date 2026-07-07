#!/usr/bin/env python
"""ah_ledger_criticality.py — the family criticality table.

Criterion: a maximal drain run entered at generation n0 has length = v_p(orbit - fixed point)
<= log_p(orbit magnitude at entry) ~ rho * n0, while the ledger at entry is ~ beta * n0.
Single-run fatality (one run exhausting the whole ledger) is excluded at scale iff
    ratio := rho / beta < 1.
rho = (orbit log-growth per generation)/log p ("run-cap slope"); beta = ledger drift
("budget slope"). NOTE the run length is fixed by the valuation AT ENTRY, so the naive
ratio criterion is the sharp one (no end-of-run correction needed).

Verifies:  Antihydra ratio = log2(3/2)/(1/2) = log2(9/4) = 1.1699  ( > 1, NOT excluded —
critical), identical to PROOF_TOOL_ATTEMPT's independently derived 0.585/0.5 = 1.17x;
o4 ratio = log3(4/3)/3 = 0.0873; o3 measured from its exact (a,k) map (200k generations,
re-verifying O3_TEMPLATE_PORT's orbit statistics + the v3(a+9) drain-run law);
o15/o18 run-cap slope log3(8/3) = 0.8928 (budget: string / reset — no scalar slope).

Interpreter: /Users/aokiyousuke/quantum-ecc/.venv/bin/python
"""
import math

ok = True
def check(name, cond, detail=""):
    global ok
    print(("PASS  " if cond else "FAIL  ") + name + ("" if not detail else "  | " + detail))
    if not cond: ok = False

log2_32 = math.log2(1.5)          # Antihydra run-cap slope (v2 depth of a x3/2 orbit)
log3_43 = math.log(4/3, 3)        # o4 run-cap slope (v3 depth of a x4/3 orbit)
log3_83 = math.log(8/3, 3)        # o15 / o18-depth run-cap slope (v3 of x8/3)

# --------------------------------------------------------- Antihydra
rho_AH, beta_AH = log2_32, 0.5
check("Antihydra ratio = log2(3/2)/(1/2) = log2(9/4)",
      abs(rho_AH/beta_AH - math.log2(2.25)) < 1e-15,
      f"= {rho_AH/beta_AH:.6f} > 1  -> single-run fatality NOT excluded (critical)")
check("identity with PROOF_TOOL_ATTEMPT's '1.17x improvement needed'",
      abs(rho_AH/beta_AH - 0.585/0.5) < 2e-4,
      f"needed <0.5n vs proven ceiling 0.585n: 0.585/0.5 = {0.585/0.5:.4f} — the SAME number, (K) itself")

# --------------------------------------------------------- o4
rho_o4, beta_o4 = log3_43, 3.0    # growth x4/3 exactly per generation [PROVEN given template]; drift (−1+4+6)/3
check("o4 ratio = log3(4/3)/3", abs(rho_o4/beta_o4 - 0.087287) < 1e-5,
      f"= {rho_o4/beta_o4:.6f} < 1  -> single-run fatality excluded")

# --------------------------------------------------------- o3: exact (a,k) map, 200k generations
# map (O3_TEMPLATE_PORT_2026-07-06.md §3, [PROVEN on grid]):
#   a=1 (mod 3): (a,k) -> (a-1,  k+2)
#   a=2 (mod 3): (a,k) -> ((4a+4)/3, k+1)
#   a=0 (mod 3), k>=2: (a,k) -> (4a/3+3, k-1)     (drain; fixed point a=-9 -> run = v3(a+9))
#   (k=1/k=0 floor rules never fire on this orbit: k stays >= 2)
def v3(m):
    r = 0
    while m % 3 == 0: m //= 3; r += 1
    return r

GEN = 200_000
a, k = 6, 2
freq = [0, 0, 0]; dk_sum = 0; min_k_at_drain = None
drain_run = 0; longest_drain = 0; run_law_ok = True; pred = None
for n in range(GEN):
    r = a % 3
    freq[r] += 1
    if r == 1:
        a, dk = a - 1, +2
    elif r == 2:
        a, dk = (4*a + 4)//3, +1
    else:
        assert k >= 2, f"k floor hit at gen {n}"
        if drain_run == 0:
            pred = v3(a + 9)              # predicted maximal drain-run length
        if min_k_at_drain is None or k < min_k_at_drain: min_k_at_drain = k
        a, dk = (4*a)//3 + 3, -1
    if r == 0:
        drain_run += 1
    else:
        if drain_run:
            if drain_run != pred: run_law_ok = False
            longest_drain = max(longest_drain, drain_run)
        drain_run = 0
    dk_sum += dk; k += dk
f0, f1, f2 = (f/GEN for f in freq)
gamma = math.log(a) / GEN                 # orbit log-growth per generation
rho_o3 = gamma / math.log(3)
beta_o3 = dk_sum / GEN
check("o3 orbit statistics match O3_TEMPLATE_PORT (freqs ~ 1/2,1/4,1/4; drift ~ +0.248)",
      abs(f0 - 0.5009) < 2e-3 and abs(beta_o3 - 0.24828) < 2e-3,
      f"freq(a=0,1,2 mod 3) = ({f0:.4f},{f1:.4f},{f2:.4f}); drift = {beta_o3:.5f}/gen; "
      f"k = {k} at gen {GEN} (min k at a drain = {min_k_at_drain})")
check("o3 drain-run closed form: every maximal a=0(mod 3) run = v3(a+9) at entry", run_law_ok,
      f"longest drain run = {longest_drain} (note says 10)")
check("o3 longest drain run = 10 (O3_TEMPLATE_PORT)", longest_drain == 10)
gamma_ideal = 0.75 * math.log(4/3)        # idealized (1/2,1/4,1/4) frequencies
print(f"      o3 growth: gamma = {gamma:.6f}/gen  (idealized 0.75*ln(4/3) = {gamma_ideal:.6f}) "
      f"-> rho = {rho_o3:.4f} (idealized {gamma_ideal/math.log(3):.4f})")
print(f"      o3 ratio = rho/beta = {rho_o3/beta_o3:.4f}  [OBSERVED ingredients]")
print(f"      o3 ratio under the UNCONDITIONAL magnitude cap (a <= (4/3)^n a0): "
      f"{log3_43/beta_o3:.4f}  — above 1! o3's single-run exclusion genuinely needs the orbit's growth statistics")

# --------------------------------------------------------- table
print()
print("CRITICALITY TABLE  (ratio = run-cap slope / budget slope; single-run fatality excluded iff < 1)")
rows = [
    ("Antihydra", "x3/2, v2", f"{log2_32:.5f} [PROVEN]", "1/2  cumulative [OBS=annealed]",
     f"{log2_32/0.5:.4f}", "> 1: NOT excluded — THE critical rung"),
    ("o4",        "x4/3, v3", f"{log3_43:.5f} [PROVEN|template]", "3    cumulative [OBS=annealed]",
     f"{log3_43/3:.4f}", "< 1: excluded (also unconditionally via banked a40=124)"),
    ("o3",        "x4/3 mix, v3", f"{rho_o3:.5f} [OBSERVED growth]", f"{beta_o3:.3f} cumulative [OBSERVED]",
     f"{rho_o3/beta_o3:.4f}", "< 1: excluded GIVEN orbit stats (1.05 under unconditional cap)"),
    ("o15",       "x8/3, v3", f"{log3_83:.5f} [PROVEN|grid]", "string-valued (queue)  — no scalar slope",
     "n/a", "criterion inapplicable; single-run kill gated on v3(V-1)>=3 [grid]"),
    ("o18",       "x8/3, v3", f"{log3_83:.5f} [PROVEN|grid]", "RESET each generation (renewal)  beta_cum = 0",
     "inf", "formally supercritical: no cumulative budget; annealed model halts"),
]
hdr = ("machine", "depth process", "run-cap slope rho", "budget slope beta", "ratio", "verdict")
w = (10, 14, 26, 44, 7, 62)
print("  " + " | ".join(h.ljust(x) for h, x in zip(hdr, w)))
for row in rows:
    print("  " + " | ".join(str(v).ljust(x) for v, x in zip(row, w)))
print()
print("ALL CHECKS PASSED" if ok else "*** SOME CHECKS FAILED ***")
