"""
U0_EXCLUSION_BUILD 2026-07-10
=============================
Question (the single un-blocked target): does an A-PRIORI mechanism EXCLUDE the
explicit fatal adversary u0 constructed in RELOAD_EXCURSION_BUILD (a free Z_2^x
element realizing E[K^2]=inf)?

Reframe: u0 was built in Q_2 ALONE (solve disjoint-window congruences). The REAL
reload unit w_i = (v_i - x)/2^{d_i} is NOT free: v_i is an ACTUAL integer of the
orbit, of prescribed ARCHIMEDEAN magnitude v_i ~ 8*(3/2)^{n_i}. The orbit lives
on the (2,3)-SOLENOID: R x Q_2 x Q_3 simultaneously via Z[1/6] diagonal.

We TEST whether the solenoid diagonal (archimedean coupling) constrains u0:
  COMP 1: the naive Q_2-only fatal u0 -- is its depth sequence archimedean-legal?
          (run-cap K_i <= 0.585 * sum_{j<i} K_j from |v|_2 <= |v|_inf).  -> VIOLATES.
  COMP 2: build a run-cap-RESPECTING heavy-tail adversary (schedule deep excursions
          to respect the growing archimedean budget); verify map-faithful + E[K^2]=inf.
  COMP 3: first-moment product-formula identity on the REAL orbit (INTRATERM check):
          sum K_i * log2(3/2) =? log2 v_n  -- the diagonal's first-moment content.
          And show the 2nd moment sum K^2 is NOT an archimedean read-out.

STRICT big-int. No label upgraded.
"""
import random
from math import log2

LOG2_15 = log2(1.5)   # 0.5849625... archimedean run-cap slope for x3/2

def vq(n, q):
    if n == 0: return 10**9
    k = 0
    while n % q == 0:
        n //= q; k += 1
    return k

# ---------------------------------------------------------------------------
# The exact Antihydra reload map on Z_2^x (from RELOAD_EXCURSION_BUILD, verified).
#   K_{i+1} = v2(3^{K_i} u_i + s_i),  u_{i+1} = (3^{K_i} u_i + s_i) >> K_{i+1}
#   s alternates -1 (even->odd), +1 (odd->even).
# ---------------------------------------------------------------------------

def real_orbit_reloads(c0=8, NSTEP=200000):
    """Real integer orbit c->floor(3c/2). Return per-reload records:
       K_i (run length), n_i (orbit step at run entry), v_i (entry value, exact bigint)."""
    c = c0
    cur = c % 2; runlen = 0; entry = c; entry_step = 0
    recs = []   # (K, n_entry, v_entry)
    n = 0
    while n < NSTEP:
        par = c % 2
        if par == cur:
            runlen += 1
        else:
            recs.append((runlen, entry_step, entry))
            cur = par; runlen = 1; entry = c; entry_step = n
        c = (3*c)//2
        n += 1
    # drop truncated final run
    return recs[:-1]

# ---------------------------------------------------------------------------
# COMP 1. The naive Q_2-only fatal u0 (RELOAD_EXCURSION_BUILD PART C).
#   Build a 2-adic unit realizing a prescribed heavy K-tail, ignoring archimedean.
#   Then test archimedean legality: run-cap K_i <= 3 + 0.585 * sum_{j<i} K_j.
# ---------------------------------------------------------------------------

def build_adversary_antihydra(Kseq):
    """Solve forward in Z_2 for u realizing depths Kseq[1:] exactly (map-faithful).
       Returns realized depth sequence (== Kseq if solvable)."""
    seq_out = [Kseq[0]]
    s = -1
    K_cur = Kseq[0]
    u = 1
    for idx in range(1, len(Kseq)):
        Knext = Kseq[idx]
        mod = 1 << (Knext + 1)
        a = pow(3, K_cur, mod)
        ainv = pow(a, -1, mod)
        u_low = (ainv * ((-s) % (1 << Knext))) % (1 << Knext)
        if u_low % 2 == 0:
            u_low |= 1
        base = (pow(3, K_cur, mod) * u_low + s) % mod
        bit = (base >> Knext) & 1
        u_full = u_low + (1 << Knext) if bit == 0 else u_low
        val = pow(3, K_cur) * u_full + s
        got = vq(val, 2)
        seq_out.append(got)
        s = -s
        K_cur = got
        u = val >> got
    return seq_out

def runcap_audit(Kseq, tag, slope=LOG2_15, base_bits=3.0):
    """Check the archimedean run-cap K_i <= base_bits + slope * sum_{j<i} K_j.
       Returns (#violations, first_violation_index, worst_excess)."""
    S = 0.0
    viol = 0; first = None; worst = 0.0
    details = []
    for i, K in enumerate(Kseq):
        cap = base_bits + slope * S     # log2(8*(3/2)^{n_i}) with n_i = sum_{j<i}K_j
        excess = K - cap
        if excess > 0:
            viol += 1
            if first is None: first = i
            worst = max(worst, excess)
            if len(details) < 8:
                details.append((i, K, round(cap,2), round(excess,2), int(S)))
        S += K
    print(f"  [{tag}] run-cap audit: {viol}/{len(Kseq)} excursions VIOLATE "
          f"K_i <= 3 + 0.585*sum_prev_K")
    if viol:
        print(f"     first violation at reload i={first}; worst excess = {worst:.2f} bits")
        print(f"     (i, K_i, cap, excess, n_i=sum_prev):")
        for d in details:
            print(f"        {d}")
    return viol, first, worst

# ---------------------------------------------------------------------------
# COMP 2. A run-cap-RESPECTING heavy-tail adversary.
#   At reload i maintain budget cap_i = 3 + 0.585 * S_i, S_i = sum_{j<i}K_j.
#   Draw K_i from a heavy tail but CAP at floor(cap_i). Occasionally SATURATE the
#   cap (deep excursion scheduled only when the archimedean budget permits it).
#   Then confirm (a) map-faithful via the congruence solver, (b) E[K^2] diverges.
# ---------------------------------------------------------------------------

def build_solenoid_legal_heavy(M=4000, seed=11, saturate_at_powers=True):
    """Return a run-cap-legal depth sequence with heavy 2nd moment.
       Typical depths ~geometric(1/2); at sparse indices i=2^m saturate to the cap."""
    random.seed(seed)
    Kseq = [2]
    S = 2.0
    m_next = 2
    for i in range(1, M):
        cap = 3.0 + LOG2_15 * S
        cap_floor = int(cap)
        if saturate_at_powers and i == m_next:
            K = cap_floor                      # saturate the archimedean budget
            m_next *= 2
        else:
            # geometric(1/2) draw, truncated to the cap
            K = 1
            while random.random() < 0.5:
                K += 1
            if K > cap_floor:
                K = cap_floor
        if K < 1: K = 1
        Kseq.append(K)
        S += K
    return Kseq

def moment_growth(Kseq, tag):
    """Report the running excursion-average (1/M) sum K_i^2 -- diverges iff E[K^2]=inf."""
    print(f"  [{tag}] running E[K^2] (excursion average) at M = 250,1000,4000:")
    for M in (250, 1000, min(4000, len(Kseq))):
        sub = Kseq[:M]
        eK = sum(sub)/M
        eK2 = sum(k*k for k in sub)/M
        print(f"     M={M:5d}: E[K]={eK:.3f}  E[K^2]={eK2:8.2f}  maxK={max(sub)}  "
              f"sumK(=n)={sum(sub)}")
    # is the growth super-linear in M? compare E[K^2] at M and 4M
    Ms = [250, 1000, 4000]
    vals = [sum(k*k for k in Kseq[:m])/m for m in Ms if m <= len(Kseq)]
    if len(vals) >= 2:
        print(f"     ratio E[K^2](4M)/E[K^2](M): "
              + ", ".join(f"{vals[i+1]/vals[i]:.2f}" for i in range(len(vals)-1))
              + "   (>1 growing => E[K^2] -> inf)")

# ---------------------------------------------------------------------------
# COMP 3. First-moment product-formula (INTRATERM) identity on the REAL orbit.
#   sum_{j<i} K_j = n_i (steps); log2 v_{n_i} ~ 3 + 0.585 n_i.  The archimedean
#   place READS OUT exactly the SUM of depths (first moment), never the sum of
#   squares.  Verify the renewal ratio and show the 2nd-moment is not archimedean.
# ---------------------------------------------------------------------------

def product_formula_check(recs):
    print("  first-moment renewal (product formula = INTRATERM tautology):")
    print("     i        n_i    sum_{j<i}K_j   log2(v_ni)   0.585*n_i(+3)")
    S = 0
    checks = []
    for idx, (K, n_entry, v_entry) in enumerate(recs):
        if idx in (100, 1000, 10000, 50000) and idx < len(recs):
            log2v = log2(abs(v_entry)) if v_entry not in (0,1) else 0.0
            pred = 3.0 + LOG2_15 * n_entry
            print(f"     {idx:6d}  {n_entry:7d}   {S:9d}     {log2v:10.2f}   {pred:10.2f}")
            checks.append((log2v, pred, n_entry, S))
        S += K
    # verify n_i == sum_{j<i} K_j exactly (definition of the reload partition)
    S2 = 0; ok = True
    for (K, n_entry, v_entry) in recs:
        if n_entry != S2: ok = False
        S2 += K
    print(f"     [identity] n_i == sum_{{j<i}} K_j exactly: {ok}   (steps = drained depth)")
    # run-cap holds on the REAL orbit (necessary condition, always true):
    viol,_,_ = runcap_audit([K for (K,_,_) in recs], "REAL orbit", base_bits=3.0)
    return checks

def main():
    print("="*74)
    print("COMP 1  The naive Q_2-only fatal u0 -- is it archimedean (solenoid) legal?")
    print("="*74)
    # reproduce the two RELOAD_EXCURSION_BUILD fatal constructions
    target = [2] + list(range(1, 20))         # linear-growing depths, sum K^2 ~ M^3
    got = build_adversary_antihydra(target)
    print(f"  construction A (linear-growth depths [1..19]) realized map-faithfully: "
          f"{got[1:]==target[1:]}")
    runcap_audit(got, "naive u0 / linear-growth")
    print()
    random.seed(7)
    ht = [max(1, int(1.0/(1.0-random.random()))) for _ in range(40)]   # P(K>=k)~1/k
    got2 = build_adversary_antihydra([2] + ht)
    print(f"  construction B (heavy-tail P(K>=k)~1/k, E[K^2]=inf) realized: "
          f"{got2[1:]==ht}   maxK={max(got2)}")
    runcap_audit(got2, "naive u0 / heavy-tail")

    print("\n" + "="*74)
    print("COMP 2  A run-cap-RESPECTING (solenoid-legal) heavy-tail adversary")
    print("="*74)
    Kleg = build_solenoid_legal_heavy(M=4000)
    # verify map-faithful: the congruence solver realizes it exactly
    realized = build_adversary_antihydra(Kleg)
    faithful = realized[1:] == Kleg[1:]
    print(f"  map-faithful (reload congruences solvable for this K-seq): {faithful}")
    runcap_audit(Kleg, "solenoid-legal heavy")
    moment_growth(Kleg, "solenoid-legal heavy")

    print("\n" + "="*74)
    print("COMP 3  Real orbit: the diagonal's first-moment content (product formula)")
    print("="*74)
    recs = real_orbit_reloads(8, 200000)
    print(f"  real orbit seed 8: {len(recs)} reloads over 200000 steps")
    product_formula_check(recs)
    # real-orbit E[K^2] (finite, but that is the CONCLUSION not forced by archimedean)
    Kr = [K for (K,_,_) in recs]
    print(f"  real orbit  E[K]={sum(Kr)/len(Kr):.4f}  E[K^2]={sum(k*k for k in Kr)/len(Kr):.4f}"
          f"  maxK={max(Kr)}  (finite = the OPEN conclusion, not archimedean-forced)")

if __name__ == "__main__":
    main()
