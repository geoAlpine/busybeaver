/-!
# The UNIFORM fixed-point run theorem — general-`q` mirror ladder (Lean 4)

Abstracts `RunStructure.lean` (the `q = 3`, `×4/3` odometer o4) to an **arbitrary
base `q ≥ 2`** with a general branch map, so that every Type-I BB(6) cryptid's run
law (`PAPER_MIRROR_LADDER.md` §1) becomes a corollary of one theorem.

Setup (all arithmetic over `ℤ`, base `q : ℕ`):
each branch is an affine map `b(v) = (p·v + e)/q` with `gcd(p, q) = 1`; it has the
fixed point `x = -e/(p-q)`; whenever `x ∈ ℤ` (`q·x = p·x + e`),
* `q·(b v - x) = p·(v - x)`  (`branch_conj`), and — because `p` is a **unit** in
  the `q`-adic integers (`gcd(p,q)=1`) —
* `v_q(b v - x) = v_q(v - x) - 1`  (`vq_step_down`).

Hence the **maximal run** of the branch from `v` is exactly `v_q(v - x)`
(`run_closed_form`), capped by `log_q |v - x|` (`run_cap`).

**The mathematical crux is `vqn_unit_mul`**: a `q`-adic *unit* `u` (`gcd(u,q)=1`)
does not move the valuation, `v_q(u·n) = v_q(n)`. It rests on Euclid's lemma
`gcd(u,q)=1 ∧ q ∣ u·n → q ∣ n`, proved from scratch (`vqn_euclid`) via
`gcd(u·n, q·n) = gcd(u,q)·n = n`.

Dependency-free: core Lean only (no mathlib); `Int`/`Nat` arithmetic, `omega`,
and a from-scratch `q`-adic valuation `vqn`/`vq`.  Corollaries (§5) instantiate the
single theorem for Antihydra, o11, o16, o4, o15/o18, and Space Needle's even branch.
-/

namespace Mirror

/-! ## §0 Strong induction (self-contained, no mathlib). -/

theorem strong_ind (P : Nat → Prop) (h : ∀ n, (∀ m, m < n → P m) → P n) :
    ∀ n, P n := by
  have key : ∀ N n, n < N → P n := by
    intro N
    induction N with
    | zero => intro n hn; exact absurd hn (Nat.not_lt_zero n)
    | succ N ihN => intro n hn; exact h n (fun m hm => ihN m (by omega))
  intro n; exact key (n + 1) n (by omega)

/-! ## §1 The `q`-adic valuation on `ℕ`, for arbitrary base `q ≥ 2`. -/

/-- `q`-adic valuation on `ℕ` (`vqn q 0 = 0` and `vqn q n = 0` when `q < 2`, by
convention).  The guard `2 ≤ q ∧ 0 < n` makes the recursion terminate for a
*variable* base. -/
def vqn (q n : Nat) : Nat :=
  if h : 2 ≤ q ∧ 0 < n ∧ n % q = 0 then vqn q (n / q) + 1 else 0
termination_by n
decreasing_by exact Nat.div_lt_self h.2.1 h.1

theorem vqn_zero (q : Nat) : vqn q 0 = 0 := by
  rw [vqn.eq_def, dif_neg]; rintro ⟨_, h, _⟩; exact absurd h (Nat.lt_irrefl 0)

theorem vqn_of_not_dvd {q n : Nat} (h : n % q ≠ 0) : vqn q n = 0 := by
  rw [vqn.eq_def, dif_neg]; rintro ⟨_, _, hc⟩; exact h hc

theorem vqn_of_dvd {q n : Nat} (hq : 2 ≤ q) (hn : 0 < n) (h : n % q = 0) :
    vqn q n = vqn q (n / q) + 1 := by
  rw [vqn.eq_def, dif_pos ⟨hq, hn, h⟩]

/-- `k < q·k` for `q ≥ 2`, `k ≠ 0` (Classical-free; `Nat.mul_lt_mul_right` is not). -/
theorem lt_mul_self {q k : Nat} (hq : 2 ≤ q) (hk : k ≠ 0) : k < q * k := by
  have h2k : 2 * k ≤ q * k := Nat.mul_le_mul hq (Nat.le_refl k)
  omega

/-- `v_q(q·n) = v_q(n) + 1`. -/
theorem vqn_q_mul {q n : Nat} (hq : 2 ≤ q) (hn : n ≠ 0) :
    vqn q (q * n) = vqn q n + 1 := by
  have h0 : 0 < q := by omega
  have hqn : 0 < q * n := Nat.mul_pos h0 (Nat.pos_of_ne_zero hn)
  have hmod : (q * n) % q = 0 := Nat.mul_mod_right q n
  have hdiv : (q * n) / q = n := Nat.mul_div_cancel_left n h0
  rw [vqn_of_dvd hq hqn hmod, hdiv]

theorem vqn_pos_of_dvd {q m : Nat} (hq : 2 ≤ q) (hm : m ≠ 0) (hd : m % q = 0) :
    1 ≤ vqn q m := by
  rw [vqn_of_dvd hq (Nat.pos_of_ne_zero hm) hd]; omega

theorem vqn_pos_dvd {q m : Nat} (h : 1 ≤ vqn q m) : q ∣ m := by
  by_cases hd : m % q = 0
  · exact Nat.dvd_of_mod_eq_zero hd
  · rw [vqn_of_not_dvd hd] at h; omega

/-- **Euclid's lemma (the coprimality hook).** If `gcd(u,q)=1` and `q ∣ u·n`,
then `q ∣ n`.  Proof: `q ∣ u·n` and `q ∣ q·n`, so `q ∣ gcd(u·n, q·n) = gcd(u,q)·n
= 1·n = n`. -/
theorem vqn_euclid {q u n : Nat} (hcop : Nat.gcd u q = 1) (hd : q ∣ u * n) :
    q ∣ n := by
  have h1 : q ∣ q * n := ⟨n, rfl⟩
  have h2 : q ∣ Nat.gcd (u * n) (q * n) := Nat.dvd_gcd hd h1
  rw [Nat.gcd_mul_right, hcop, Nat.one_mul] at h2
  exact h2

/-- **The crux: a `q`-adic unit preserves the valuation.**  If `gcd(u,q)=1` then
`v_q(u·n) = v_q(n)` for all `n`.  This is where coprimality enters the run law. -/
theorem vqn_unit_mul {q u : Nat} (hq : 2 ≤ q) (hu : Nat.gcd u q = 1) :
    ∀ n, vqn q (u * n) = vqn q n := by
  apply strong_ind (fun n => vqn q (u * n) = vqn q n)
  intro n ih
  by_cases h0 : n = 0
  · subst h0; rw [Nat.mul_zero]
  · by_cases hdvd : n % q = 0
    · -- `q ∣ n`: recurse.  `u·(q·k) = q·(u·k)`; unit preserved by IH on `k`.
      obtain ⟨k, hk⟩ := Nat.dvd_of_mod_eq_zero hdvd
      subst hk
      have hk0 : k ≠ 0 := by rintro rfl; rw [Nat.mul_zero] at h0; exact h0 rfl
      have hu0 : u ≠ 0 := by
        rintro rfl; rw [Nat.gcd_zero_left] at hu; omega
      have huk : u * k ≠ 0 := Nat.mul_ne_zero hu0 hk0
      have hlt : k < q * k := lt_mul_self hq hk0
      have hassoc : u * (q * k) = q * (u * k) := by
        rw [← Nat.mul_assoc, Nat.mul_comm u q, Nat.mul_assoc]
      rw [hassoc, vqn_q_mul hq huk, vqn_q_mul hq hk0, ih k hlt]
    · -- `q ∤ n`: by Euclid `q ∤ u·n`, so both valuations are `0`.
      have hun : (u * n) % q ≠ 0 := by
        intro hc
        obtain ⟨k, hk⟩ := vqn_euclid hu (Nat.dvd_of_mod_eq_zero hc)
        exact hdvd (by rw [hk]; exact Nat.mul_mod_right q k)
      rw [vqn_of_not_dvd hun, vqn_of_not_dvd hdvd]

/-! ## §5-cap: `q^(v_q n) ≤ n`. -/

theorem vqn_pow_le {q : Nat} (hq : 2 ≤ q) : ∀ n, n ≠ 0 → q ^ vqn q n ≤ n := by
  apply strong_ind (fun n => n ≠ 0 → q ^ vqn q n ≤ n)
  intro n ih h0
  by_cases h3 : n % q = 0
  · obtain ⟨k, hk⟩ := Nat.dvd_of_mod_eq_zero h3
    subst hk
    have hk0 : k ≠ 0 := by rintro rfl; rw [Nat.mul_zero] at h0; exact h0 rfl
    have hlt : k < q * k := lt_mul_self hq hk0
    have hle : q ^ vqn q k ≤ k := ih k hlt hk0
    rw [vqn_q_mul hq hk0, Nat.pow_succ, Nat.mul_comm q k]
    exact Nat.mul_le_mul hle (Nat.le_refl q)
  · rw [vqn_of_not_dvd h3, Nat.pow_zero]; omega

/-! ## §2 The `q`-adic valuation on `ℤ`, and the unit / step lemmas. -/

/-- `q`-adic valuation on `ℤ` (`vq q 0 = 0` by convention). -/
def vq (q : Nat) (n : Int) : Nat := vqn q n.natAbs

theorem vq_zero (q : Nat) : vq q 0 = 0 := by
  unfold vq; rw [Int.natAbs_zero, vqn_zero]

/-- `v_q(q·m) = v_q(m) + 1`. -/
theorem vq_q_mul {q : Nat} (hq : 2 ≤ q) {m : Int} (hm : m ≠ 0) :
    vq q ((q : Int) * m) = vq q m + 1 := by
  unfold vq
  rw [Int.natAbs_mul, Int.natAbs_natCast]
  exact vqn_q_mul hq (Int.natAbs_ne_zero.mpr hm)

/-- `v_q(p·m) = v_q(m)` when `gcd(p,q)=1` — the `ℤ` form of the crux. -/
theorem vq_unit_mul {q : Nat} (hq : 2 ≤ q) {p : Int}
    (hcop : Nat.gcd p.natAbs q = 1) (m : Int) : vq q (p * m) = vq q m := by
  unfold vq
  rw [Int.natAbs_mul]
  exact vqn_unit_mul hq hcop m.natAbs

theorem vq_pos_dvd {q : Nat} {n : Int} (h : 1 ≤ vq q n) : (q : Int) ∣ n := by
  have hd : q ∣ n.natAbs := vqn_pos_dvd h
  rw [← Int.dvd_natAbs]; exact_mod_cast hd

theorem vq_eq_zero_not_dvd {q : Nat} (hq : 2 ≤ q) {n : Int} (hn : n ≠ 0)
    (h : vq q n = 0) : n % (q : Int) ≠ 0 := by
  intro hmod
  have hd : (q : Int) ∣ n := Int.dvd_of_emod_eq_zero hmod
  have hd2 : q ∣ n.natAbs := by
    have := Int.dvd_natAbs.mpr hd
    exact_mod_cast this
  obtain ⟨k, hk⟩ := hd2
  have hm0 : n.natAbs % q = 0 := by rw [hk]; exact Nat.mul_mod_right q k
  have hpos := vqn_pos_of_dvd hq (Int.natAbs_ne_zero.mpr hn) hm0
  unfold vq at h; omega

theorem p_ne_zero {p : Int} {q : Nat} (hq : 2 ≤ q)
    (hcop : Nat.gcd p.natAbs q = 1) : p ≠ 0 := by
  intro h; subst h
  simp only [Int.natAbs_zero, Nat.gcd_zero_left] at hcop
  omega

/-- **Valuation drop.**  `q·a = p·b`, `q ∣ b`, `b ≠ 0`, `gcd(p,q)=1` force
`v_q(a) + 1 = v_q(b)`: multiplying by the unit `p` fixes `v_q`, dividing by `q`
drops it by one. -/
theorem vq_step_down {p a b : Int} {q : Nat} (hq : 2 ≤ q)
    (hcop : Nat.gcd p.natAbs q = 1) (h : (q : Int) * a = p * b)
    (hb : b ≠ 0) (hdvd : (q : Int) ∣ b) : vq q a + 1 = vq q b := by
  obtain ⟨c, hc⟩ := hdvd
  have hc0 : c ≠ 0 := by rintro rfl; rw [Int.mul_zero] at hc; exact hb hc
  have hpb : p * b = (q : Int) * (p * c) := by
    rw [hc, ← Int.mul_assoc, Int.mul_comm p (q : Int), Int.mul_assoc]
  have hqa : (q : Int) * a = (q : Int) * (p * c) := by rw [h, hpb]
  have hqne : (q : Int) ≠ 0 := by exact_mod_cast (show q ≠ 0 by omega)
  have ha : a = p * c := Int.eq_of_mul_eq_mul_left hqne hqa
  rw [ha, hc, vq_unit_mul hq hcop c, vq_q_mul hq hc0]

/-! ## §3 The abstract branch map, its orbit, and the conjugation identity. -/

/-- The affine branch map `b(v) = (p·v + e)/q`. -/
def bmap (p e : Int) (q : Nat) (v : Int) : Int := (p * v + e) / (q : Int)

/-- Orbit under the branch map. -/
def orb (p e : Int) (q : Nat) (v : Int) : Nat → Int
  | 0 => v
  | (n + 1) => bmap p e q (orb p e q v n)

/-- **Conjugation identity.**  At the integer fixed point `x` (`q·x = p·x + e`),
on the branch (`q ∣ v - x`), `q·(b v - x) = p·(v - x)`.  In particular `b v` is
an integer there. -/
theorem branch_conj {p e x : Int} {q : Nat} (hx : (q : Int) * x = p * x + e)
    (v : Int) (hdvd : (q : Int) ∣ (v - x)) :
    (q : Int) * (bmap p e q v - x) = p * (v - x) := by
  obtain ⟨c, hc⟩ := hdvd
  have hv : v = x + (q : Int) * c := by omega
  have e1 : p * v = p * x + p * ((q : Int) * c) := by rw [hv, Int.mul_add]
  have e2 : p * ((q : Int) * c) = (q : Int) * (p * c) := by
    rw [← Int.mul_assoc, Int.mul_comm p (q : Int), Int.mul_assoc]
  have e3 : (q : Int) * (x + p * c) = (q : Int) * x + (q : Int) * (p * c) :=
    Int.mul_add (q : Int) x (p * c)
  have hint : p * v + e = (q : Int) * (x + p * c) := by omega
  have hdvd2 : (q : Int) ∣ (p * v + e) := ⟨x + p * c, hint⟩
  have hbmap : (q : Int) * bmap p e q v = p * v + e := by
    unfold bmap; exact Int.mul_ediv_cancel' hdvd2
  have hms : (q : Int) * (bmap p e q v - x)
      = (q : Int) * bmap p e q v - (q : Int) * x := Int.mul_sub (q : Int) _ x
  have hpvx : p * (v - x) = p * v - p * x := Int.mul_sub p v x
  omega

/-! ## §4 The uniform run theorem. -/

/-- **Run invariant.**  Inside the run, `v_q(orb i - x) = v_q(v - x) - i`, and
`orb i - x ≠ 0`.  Each step conjugates by `p/q`, dropping `v_q` by exactly one. -/
theorem run_invariant {p e x : Int} {q : Nat}
    (hq : 2 ≤ q) (hcop : Nat.gcd p.natAbs q = 1) (hx : (q : Int) * x = p * x + e)
    (v : Int) (hv : v ≠ x) :
    ∀ i, i ≤ vq q (v - x) →
      vq q (orb p e q v i - x) = vq q (v - x) - i ∧ orb p e q v i - x ≠ 0 := by
  intro i
  induction i with
  | zero =>
    intro _
    refine ⟨?_, ?_⟩
    · show vq q (v - x) = vq q (v - x) - 0; rw [Nat.sub_zero]
    · show v - x ≠ 0
      intro h; exact hv (by omega)
  | succ i ih =>
    intro hi
    obtain ⟨hval, hne⟩ := ih (by omega)
    have hpos : 1 ≤ vq q (orb p e q v i - x) := by omega
    have hdvd : (q : Int) ∣ (orb p e q v i - x) := vq_pos_dvd hpos
    have hstep : (q : Int) * (orb p e q v (i + 1) - x) = p * (orb p e q v i - x) := by
      show (q : Int) * (bmap p e q (orb p e q v i) - x) = p * (orb p e q v i - x)
      exact branch_conj hx (orb p e q v i) hdvd
    have hdrop : vq q (orb p e q v (i + 1) - x) + 1 = vq q (orb p e q v i - x) :=
      vq_step_down hq hcop hstep hne hdvd
    refine ⟨by omega, ?_⟩
    have hp0 : p ≠ 0 := p_ne_zero hq hcop
    have hrhs : p * (orb p e q v i - x) ≠ 0 := Int.mul_ne_zero hp0 hne
    intro h0
    rw [h0, Int.mul_zero] at hstep
    exact hrhs hstep.symm

/-- **The uniform fixed-point run law.**  For `gcd(p,q)=1`, integer fixed point
`x` (`q·x = p·x + e`), and any seed `v ≠ x`: the branch residue (`≡ x (mod q)`)
persists for exactly the first `v_q(v - x)` steps of the orbit and breaks at step
`v_q(v - x)`.  I.e. **the maximal run equals `v_q(v - x)`.**  Every Type-I cryptid's
run law (§5) is an instance. -/
theorem run_closed_form {p e x : Int} {q : Nat}
    (hq : 2 ≤ q) (hcop : Nat.gcd p.natAbs q = 1) (hx : (q : Int) * x = p * x + e)
    (v : Int) (hv : v ≠ x) :
    (∀ i, i < vq q (v - x) → (orb p e q v i - x) % (q : Int) = 0) ∧
      (orb p e q v (vq q (v - x)) - x) % (q : Int) ≠ 0 := by
  refine ⟨?_, ?_⟩
  · intro i hi
    obtain ⟨hval, _⟩ := run_invariant hq hcop hx v hv i (by omega)
    have hpos : 1 ≤ vq q (orb p e q v i - x) := by omega
    exact Int.emod_eq_zero_of_dvd (vq_pos_dvd hpos)
  · obtain ⟨hval, hne⟩ := run_invariant hq hcop hx v hv (vq q (v - x)) (Nat.le_refl _)
    have hz : vq q (orb p e q v (vq q (v - x)) - x) = 0 := by omega
    exact vq_eq_zero_not_dvd hq hne hz

/-- **Run cap.**  `q^(v_q n) ≤ |n|`, hence the run `≤ log_q |v - x|`. -/
theorem run_cap {q : Nat} (hq : 2 ≤ q) {n : Int} (h : n ≠ 0) :
    q ^ vq q n ≤ n.natAbs := by
  unfold vq
  exact vqn_pow_le hq n.natAbs (Int.natAbs_ne_zero.mpr h)

/-! ## §5 Corollaries: the whole census is one theorem.

Each machine's per-branch run law `run = v_q(v - x_branch)` is `run_closed_form`
specialized to its `(p, q, e, x)`.  The only obligations are `gcd(p,q)=1` and the
fixed-point identity `q·x = p·x + e`, both discharged by `decide`/`omega`.  The
`x`-values match `PAPER_MIRROR_LADDER.md` §2 and `mirror_census.py`. -/

section Census

/-- Antihydra, even branch: `×3/2`, `c_e = 0`, fixed point `x = 0`; `run = v₂(v)`. -/
theorem antihydra_even (v : Int) (hv : v ≠ 0) :
    (∀ i, i < vq 2 (v - 0) → (orb 3 0 2 v i - 0) % (2 : Int) = 0) ∧
      (orb 3 0 2 v (vq 2 (v - 0)) - 0) % (2 : Int) ≠ 0 :=
  run_closed_form (by decide) (by decide) (by omega) v hv

/-- Antihydra, odd branch: `×3/2`, `c_o = 0`, `e = -1`, fixed point `x = 1`;
`run = v₂(v - 1)`. -/
theorem antihydra_odd (v : Int) (hv : v ≠ 1) :
    (∀ i, i < vq 2 (v - 1) → (orb 3 (-1) 2 v i - 1) % (2 : Int) = 0) ∧
      (orb 3 (-1) 2 v (vq 2 (v - 1)) - 1) % (2 : Int) ≠ 0 :=
  run_closed_form (by decide) (by decide) (by omega) v hv

/-- o16, even branch: `c_e = 2`, `e = 4`, fixed point `x = -4`; `run = v₂(s + 4)`. -/
theorem o16_even (v : Int) (hv : v ≠ -4) :
    (∀ i, i < vq 2 (v - (-4)) → (orb 3 4 2 v i - (-4)) % (2 : Int) = 0) ∧
      (orb 3 4 2 v (vq 2 (v - (-4))) - (-4)) % (2 : Int) ≠ 0 :=
  run_closed_form (by decide) (by decide) (by omega) v hv

/-- o16, odd branch: `c_o = 2`, `e = 3`, fixed point `x = -3`; `run = v₂(s + 3)`. -/
theorem o16_odd (v : Int) (hv : v ≠ -3) :
    (∀ i, i < vq 2 (v - (-3)) → (orb 3 3 2 v i - (-3)) % (2 : Int) = 0) ∧
      (orb 3 3 2 v (vq 2 (v - (-3))) - (-3)) % (2 : Int) ≠ 0 :=
  run_closed_form (by decide) (by decide) (by omega) v hv

/-- o11, even branch: `c_e = 4`, `e = 8`, fixed point `x = -8`; `run = v₂(m + 8)`. -/
theorem o11_even (v : Int) (hv : v ≠ -8) :
    (∀ i, i < vq 2 (v - (-8)) → (orb 3 8 2 v i - (-8)) % (2 : Int) = 0) ∧
      (orb 3 8 2 v (vq 2 (v - (-8))) - (-8)) % (2 : Int) ≠ 0 :=
  run_closed_form (by decide) (by decide) (by omega) v hv

/-- o11, odd branch: `c_o = 4`, `e = 7`, fixed point `x = -7`; `run = v₂(m + 7)`. -/
theorem o11_odd (v : Int) (hv : v ≠ -7) :
    (∀ i, i < vq 2 (v - (-7)) → (orb 3 7 2 v i - (-7)) % (2 : Int) = 0) ∧
      (orb 3 7 2 v (vq 2 (v - (-7))) - (-7)) % (2 : Int) ≠ 0 :=
  run_closed_form (by decide) (by decide) (by omega) v hv

/-- o4 (`×4/3`, `q = 3`), branch `ρ=0`: `e = 9`, fixed point `x = -9`;
`run = v₃(G + 9)`.  (The whole `RunStructure.lean` o4 run law is this instance.) -/
theorem o4_r0 (v : Int) (hv : v ≠ -9) :
    (∀ i, i < vq 3 (v - (-9)) → (orb 4 9 3 v i - (-9)) % (3 : Int) = 0) ∧
      (orb 4 9 3 v (vq 3 (v - (-9))) - (-9)) % (3 : Int) ≠ 0 :=
  run_closed_form (by decide) (by decide) (by omega) v hv

/-- o4, branch `ρ=1`: `e = 14`, fixed point `x = -14`; `run = v₃(G + 14)`. -/
theorem o4_r1 (v : Int) (hv : v ≠ -14) :
    (∀ i, i < vq 3 (v - (-14)) → (orb 4 14 3 v i - (-14)) % (3 : Int) = 0) ∧
      (orb 4 14 3 v (vq 3 (v - (-14))) - (-14)) % (3 : Int) ≠ 0 :=
  run_closed_form (by decide) (by decide) (by omega) v hv

/-- o4, branch `ρ=2`: `e = 1`, fixed point `x = -1`; `run = v₃(G + 1)`. -/
theorem o4_r2 (v : Int) (hv : v ≠ -1) :
    (∀ i, i < vq 3 (v - (-1)) → (orb 4 1 3 v i - (-1)) % (3 : Int) = 0) ∧
      (orb 4 1 3 v (vq 3 (v - (-1))) - (-1)) % (3 : Int) ≠ 0 :=
  run_closed_form (by decide) (by decide) (by omega) v hv

/-- o15 / o18 (`×8/3`, `q = 3`), queued branch: `e = -5`, fixed point `x = 1`;
`run = v₃(V - 1)` (o18's depth-push law). -/
theorem o15_queued (v : Int) (hv : v ≠ 1) :
    (∀ i, i < vq 3 (v - 1) → (orb 8 (-5) 3 v i - 1) % (3 : Int) = 0) ∧
      (orb 8 (-5) 3 v (vq 3 (v - 1)) - 1) % (3 : Int) ≠ 0 :=
  run_closed_form (by decide) (by decide) (by omega) v hv

/-- Space Needle, even branch: `×5/2`, `e = 0`, fixed point `x = 0`; `run = v₂(m)`.
(The odd branch has NO single fixed point — out of scope, per the paper §3.) -/
theorem space_needle_even (v : Int) (hv : v ≠ 0) :
    (∀ i, i < vq 2 (v - 0) → (orb 5 0 2 v i - 0) % (2 : Int) = 0) ∧
      (orb 5 0 2 v (vq 2 (v - 0)) - 0) % (2 : Int) ≠ 0 :=
  run_closed_form (by decide) (by decide) (by omega) v hv

end Census

/-! ## §6 Numeric sanity + axiom audit. -/

-- Concrete run values, `vq` computed by the kernel (cross-checked in `mirror_census.py`).
#eval [vq 2 (12 - 0), vq 2 (7 - 1), vq 3 (43 + 14), vq 3 (30 + 9)]
  -- v₂(12), v₂(6), v₃(57), v₃(39)  = [2, 1, 1, 1]

/-- `vq` self-consistency check across a range (expect `true`). -/
def vqCheck : Bool :=
  (List.range 40).all (fun k => vq 2 (Int.ofNat (k + 2)) == vqn 2 (k + 2))

#eval vqCheck  -- expect true

#print axioms vqn_unit_mul
#print axioms branch_conj
#print axioms vq_step_down
#print axioms run_closed_form
#print axioms run_cap
#print axioms antihydra_odd
#print axioms o4_r1
#print axioms space_needle_even

end Mirror
