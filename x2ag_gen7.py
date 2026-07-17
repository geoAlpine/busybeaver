#!/usr/bin/env python3
"""x2ag_gen7.py -- emit the FACTORISED regen7:

  glue(241) . REGEN(4) . braid_topgrind(6,1) . REGEN(5) . descent_glue_expl(14,1,1)
            . REGEN(4) . glue(627)

Sub-call offsets 241/311/526/744/1833/1903 are TI-CONFIRMED (x2ag_regen7.py), not
inferred from step counts.  Uses x2r6_gen.py's fixed absolute tape cut so the chunks
compose under `steps_add`.

SIMULATOR EVIDENCE ONLY.  Lean's kernel is the final judge of every emitted theorem.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2r6_gen import window, cfg_at, lean_list

k = 7
s, e, LEN, loCut, hiCut = window(k)
PSHIFT = cfg_at(s, loCut, hiCut)[1] - 11      # re-anchor REGEN(7) IN pos to 11
print(f"REGEN(7) window [{s},{e}] len={LEN} cut lo={loCut} hi={hiCut} PSHIFT={PSHIFT}")

OFF = dict(R4a=241, TG=311, R5=526, DG=744, R4b=1833, TAIL=1903)
def P(off): return cfg_at(s+off, loCut, hiCut)[1] - PSHIFT   # re-anchored pos

def ones(n):  return [1]*n
def pow01(j): return [0,1]*j
def pow10(j): return [1,0]*j
def descCascade(d):
    return [1] if d == 0 else ones(2**(d+2)-3) + [0,0] + descCascade(d-1)
def foldDep(d):
    return [1,0,1] if d == 0 else foldDep(d-1) + [0,0,1] + pow01(2**(d+2)-2)
def braidRunSteps(r, n):
    return 0 if n == 0 else (8*r+10) + braidRunSteps(r+1, n-1)
def lowerFoldSteps(d):
    return 0 if d == 0 else (6*(2**(d+1)-2)+3) + lowerFoldSteps(d-1)
def lowerFoldShiftN(d):
    return 0 if d == 0 else (2*(2**(d+1)-2)+3) + lowerFoldShiftN(d-1)

OUT = []
def emit(t): OUT.append(t)

# ============ 1. verify + emit the two FORALL-FAMILY sites ============
# ---- braid_topgrind 6 1 at offset 311 (the 4->5 ASCENDING glue, 215 steps) ----
N_tg, Lc_tg = 6, 1
cin  = cfg_at(s+OFF['TG'], loCut, hiCut)
cout = cfg_at(s+OFF['TG']+215, loCut, hiCut)
assert cin[0] == 'E' and cin[3] == 0, "TG site state/head"
assert cin[2][:2*(Lc_tg+N_tg)] == pow01(Lc_tg+N_tg), "TG IN left != pow01 (Lc+N)"
marker_tg = cin[2][2*(Lc_tg+N_tg):]
assert cin[4][:3] == [0,0,0] and cin[4][3:3+2*N_tg+1] == ones(2*N_tg+1) \
   and cin[4][3+2*N_tg+1:3+2*N_tg+3] == [0,0], "TG IN right != 0^3 ones(2N+1) 0^2 casc"
casc_tg = cin[4][3+2*N_tg+3:]
pred_out_L = ones(4*N_tg+4) + pow10(Lc_tg) + [1] + marker_tg
pred_out_R = [0] + casc_tg
assert cout[0] == 'E' and cout[3] == 0, "TG OUT state/head"
assert cout[2] == pred_out_L, "TG OUT left != ones(4N+4) ++ pow10 Lc ++ 1 :: marker"
assert cout[4] == pred_out_R, "TG OUT right != 0 :: casc"
assert cout[1]-PSHIFT == P(OFF['TG']) + 5 + 2*N_tg, "TG head shift != 5+2N"
TG_STEPS = 7 + braidRunSteps(0, N_tg) + (4*N_tg+4)
assert TG_STEPS == 215
print(f"  braid_topgrind {N_tg} {Lc_tg} at off {OFF['TG']}: VERIFIED cell-for-cell, "
      f"{TG_STEPS} steps, marker={len(marker_tg)} casc={len(casc_tg)} cells")

emit(f"""set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- **THE `4 → 5` ASCENDING GLUE AT THE REAL `k=7` SITE IS `braid_topgrind 6 1`.**  The
`215` of `glueSegs 7` idx 1, at the TI-CONFIRMED offset `311` — between `REGEN(4)`'s end and
`REGEN(5)`'s start — discharged by INSTANTIATING §5af's `∀N Lc` transport at `N=6, Lc=1`, with
`marker`/`casc` bound to the site's remaining explicit cells.  NOT a kernel `rfl` run: the proof
term is `braid_topgrind`'s.  This is the whole point of §5ak — the "missing ascending
transport" is this instantiation.  `[propext, Quot.sound]`. -/
theorem r7f_topgrind_site (L R : List Bool) :
    steps {TG_STEPS} ⟨.E, {P(OFF['TG'])}, ⟨{lean_list(cin[2],'L')}, false, {lean_list(cin[4],'R')}⟩⟩
      = some ⟨.E, {cout[1]-PSHIFT}, ⟨{lean_list(cout[2],'L')}, false, {lean_list(cout[4],'R')}⟩⟩ := by
  rw [show (({cout[1]-PSHIFT} : Int)) = ({P(OFF['TG'])} : Int) + 5 + 2 * (({N_tg} : Nat) : Int) from by decide]
  exact braid_topgrind {N_tg} {Lc_tg} {P(OFF['TG'])} ({lean_list(marker_tg,'L')}) ({lean_list(casc_tg,'R')})
""")

# ---- descent_glue_expl 14 1 1 at offset 744 (the 5->4 glue, 1089 steps) ----
N_dg, d_dg, Lc_dg = 14, 1, 1
cin  = cfg_at(s+OFF['DG'], loCut, hiCut)
cout = cfg_at(s+OFF['DG']+1089, loCut, hiCut)
assert cin[0] == 'E' and cin[3] == 0, "DG site state/head"
assert cin[2][:2*(Lc_dg+N_dg)] == pow01(Lc_dg+N_dg), "DG IN left != pow01 (Lc+N)"
marker_dg = cin[2][2*(Lc_dg+N_dg):]
pref = [0,0,0] + ones(2*N_dg+1) + [0,0] + descCascade(d_dg+1) + [0,0] + [0]*7
assert cin[4][:len(pref)] == pref, "DG IN right != 0^3 ones(2N+1) 0^2 descCascade 0^2 0^7 R"
R_dg = cin[4][len(pref):]
pred_out_L = ones(12) + foldDep(d_dg) + ones(4*N_dg+4) + pow10(Lc_dg) + [1] + marker_dg
pred_out_R = [0,1,0] + R_dg
assert cout[0] == 'E' and cout[3] == 0, "DG OUT state/head"
assert cout[2] == pred_out_L, "DG OUT left != ones 12 ++ foldDep d ++ ones(4N+4) ++ pow10 Lc ++ 1::marker"
assert cout[4] == pred_out_R, "DG OUT right != 0::1::0::R"
SHIFT_dg = 13 + 2*N_dg + lowerFoldShiftN(d_dg+1)
assert cout[1]-PSHIFT == P(OFF['DG']) + SHIFT_dg, "DG head shift != 13+2N+lowerFoldShiftN"
DG_STEPS = (7 + braidRunSteps(0, N_dg) + (4*N_dg+4)) + lowerFoldSteps(d_dg+1) + 100
assert DG_STEPS == 1089
print(f"  descent_glue_expl {N_dg} {d_dg} {Lc_dg} at off {OFF['DG']}: VERIFIED cell-for-cell, "
      f"{DG_STEPS} steps, shift +{SHIFT_dg}, marker={len(marker_dg)} R={len(R_dg)} cells")

emit(f"""set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- **THE `5 → 4` GLUE AT THE REAL `k=7` SITE IS `descent_glue_expl 14 1 1`.**  The `1089`
of `glueSegs 7` idx 2, at the TI-CONFIRMED offset `744`, discharged by INSTANTIATING §5ak's
EXPLICIT-`OUT` descent glue at `N=14, d+1=2, Lc=1` (`= descentSteps 5`, the a=5 descent).  The
`∃`-free `OUT` is what lets the next chunk (`r7f_regen4_site_2`) fire on it: its left is
`ones 12 ++ foldDep 1 ++ …`, and `foldDep 1` begins `1,0,1,0,0,1,0` = `regen4_transport`'s IN.
NOT a kernel `rfl` run.  `[propext, Quot.sound]`. -/
theorem r7f_descent_site (L R : List Bool) :
    steps {DG_STEPS} ⟨.E, {P(OFF['DG'])}, ⟨{lean_list(cin[2],'L')}, false, {lean_list(cin[4],'R')}⟩⟩
      = some ⟨.E, {cout[1]-PSHIFT}, ⟨{lean_list(cout[2],'L')}, false, {lean_list(cout[4],'R')}⟩⟩ := by
  rw [show (({cout[1]-PSHIFT} : Int)) = ({P(OFF['DG'])} : Int) + 13 + 2 * (({N_dg} : Nat) : Int)
        + ((lowerFoldShiftN {d_dg+1} : Nat) : Int) from by decide]
  exact descent_glue_expl {N_dg} {d_dg} {Lc_dg} {P(OFF['DG'])} ({lean_list(marker_dg,'L')}) ({lean_list(R_dg,'R')})
""")

# ============ 2. the three REGEN sub-call sites (steps_pos_shift reuse) ============
R4_IN_L  = ones(12) + [1,0,1,0,0,1,0]; R4_IN_R = [0,1,0] + [0]*10
R4_OUT_L = [0,1,0]
R4_OUT_R = [0,0,0]+ones(13)+[0,0]+ones(5)+[0,0]+[1,0,0,0]
R5_IN_L  = ones(28) + [1,0,1,0,0]; R5_IN_R = [0,1,1,1,1,1,0,0,1,0] + [0]*16
R5_OUT_L = [0]
R5_OUT_R = ([0,0,0]+ones(29)+[0,0]+ones(13)+[0,0]+ones(5)+[0,0]+[1,0])

def emit_regen_site(name, off, kk, steps_n, inL, inR, outL, outR, inP, outP, doc):
    ca = cfg_at(s+off, loCut, hiCut); cb = cfg_at(s+off+steps_n, loCut, hiCut)
    assert ca[0]=='E' and ca[3]==0 and cb[0]=='E' and cb[3]==0, name+" state/head"
    assert ca[2][:len(inL)] == inL,  name+" IN left"
    assert ca[4][:len(inR)] == inR,  name+" IN right"
    assert cb[2][:len(outL)] == outL, name+" OUT left"
    assert cb[4][:len(outR)] == outR, name+" OUT right"
    d1 = (ca[1]-PSHIFT) - inP; d2 = (cb[1]-PSHIFT) - outP
    assert d1 == d2, f"{name}: pos shift not constant ({d1} vs {d2})"
    print(f"  REGEN({kk}) at off {off}: VERIFIED, constant pos shift d={d1}")
    emit(f"""set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
{doc}
theorem {name} (L R : List Bool) :
    steps (exitSteps {kk}) ⟨.E, {ca[1]-PSHIFT}, ⟨{lean_list(ca[2],'L')}, false, {lean_list(ca[4],'R')}⟩⟩
      = some ⟨.E, {cb[1]-PSHIFT}, ⟨{lean_list(cb[2],'L')}, false, {lean_list(cb[4],'R')}⟩⟩ := by
  rw [show (({ca[1]-PSHIFT} : Int)) = ({inP} : Int) + {d1} from by decide,
      show (({cb[1]-PSHIFT} : Int)) = ({outP} : Int) + {d1} from by decide]
  exact steps_pos_shift (regen{kk}_transport ({lean_list(ca[2][len(inL):],'L')}) ({lean_list(ca[4][len(inR):],'R')}))
""")

emit_regen_site("r7f_regen4_site_1", OFF['R4a'], 4, 70, R4_IN_L, R4_IN_R, R4_OUT_L, R4_OUT_R, 9, -7,
  """/-- **THE FIRST `REGEN(4)` SUB-CALL**, TI-confirmed at offset `241`.  `regen4_transport`'s
proof term, translated to this site's absolute head position by `steps_pos_shift` (§5aj).  No
kernel re-run.  `[propext, Quot.sound]`. -/""")
emit_regen_site("r7f_regen5_site", OFF['R5'], 5, 218, R5_IN_L, R5_IN_R, R5_OUT_L, R5_OUT_R, 10, -22,
  """/-- **THE `REGEN(5)` SUB-CALL**, TI-confirmed at offset `526` — the FIRST time a `REGEN(k')`
with `k' > 4` is reused inside a larger `REGEN` at the transport level.  `regen5_transport`'s
proof term via `steps_pos_shift`.  `[propext, Quot.sound]`. -/""")
emit_regen_site("r7f_regen4_site_2", OFF['R4b'], 4, 70, R4_IN_L, R4_IN_R, R4_OUT_L, R4_OUT_R, 9, -7,
  """/-- **THE SECOND `REGEN(4)` SUB-CALL**, TI-confirmed at offset `1833` — fed DIRECTLY by
`r7f_descent_site`'s explicit `OUT` (this is the composition `descent_glue`'s `∃` blocked).
`regen4_transport`'s proof term via `steps_pos_shift`.  `[propext, Quot.sound]`. -/""")

# ============ 3. the two BRUTE glue runs (lead 241, trailing 627) ============
def emit_chunks(name, lo, hi, ch=38):
    bounds = list(range(lo, hi, ch)) + [hi]
    for i in range(len(bounds)-1):
        x, y = bounds[i], bounds[i+1]
        ca = cfg_at(x, loCut, hiCut); cb = cfg_at(y, loCut, hiCut)
        emit(f"""theorem {name}{i+1} (L R : List Bool) :
    steps {y-x} ⟨.{ca[0]}, {ca[1]-PSHIFT}, ⟨{lean_list(ca[2],'L')}, {'true' if ca[3] else 'false'}, {lean_list(ca[4],'R')}⟩⟩
      = some ⟨.{cb[0]}, {cb[1]-PSHIFT}, ⟨{lean_list(cb[2],'L')}, {'true' if cb[3] else 'false'}, {lean_list(cb[4],'R')}⟩⟩ :=
  rfl
""")
    return len(bounds)-1

n1 = emit_chunks("r7f_G1_", s, s+OFF['R4a'])
emit(f"""set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- **THE LEAD GLUE** (`glueSegs 7` idx 0, `241` steps): `REGEN(7)`'s IN to the first
`REGEN(4)` sub-call site.  Per-level kernel `rfl` — NO `∀` law covers it (see §5ak's scope note).
`[propext, Quot.sound]`. -/
theorem r7f_glue1 (L R : List Bool) :
    steps {OFF['R4a']} ⟨.E, 11, ⟨{lean_list(cfg_at(s,loCut,hiCut)[2],'L')}, false, {lean_list(cfg_at(s,loCut,hiCut)[4],'R')}⟩⟩
      = some ⟨.E, {cfg_at(s+OFF['R4a'],loCut,hiCut)[1]-PSHIFT}, ⟨{lean_list(cfg_at(s+OFF['R4a'],loCut,hiCut)[2],'L')}, false, {lean_list(cfg_at(s+OFF['R4a'],loCut,hiCut)[4],'R')}⟩⟩ := by
{chr(10).join(f'  rw [show ({b} : Nat) = 38 + {b-38} from by decide, steps_add, r7f_G1_{i+1}, someBind]' for i, b in enumerate(range(OFF['R4a'], 0, -38)) if b > 38)}
  exact r7f_G1_{n1} L R
""")

n2 = emit_chunks("r7f_G2_", s+OFF['TAIL'], e)
emit(f"""set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- **THE TRAILING GLUE** (`glueSegs 7` idx 3, `627` steps): the last `REGEN(4)` sub-call's
OUT to `REGEN(7)`'s OUT, incl. the `TERM(7)=268` terminal (§5y).  Per-level kernel `rfl`.
`[propext, Quot.sound]`. -/
theorem r7f_glue2 (L R : List Bool) :
    steps {e-(s+OFF['TAIL'])} ⟨.E, {cfg_at(s+OFF['TAIL'],loCut,hiCut)[1]-PSHIFT}, ⟨{lean_list(cfg_at(s+OFF['TAIL'],loCut,hiCut)[2],'L')}, false, {lean_list(cfg_at(s+OFF['TAIL'],loCut,hiCut)[4],'R')}⟩⟩
      = some ⟨.E, {cfg_at(e,loCut,hiCut)[1]-PSHIFT}, ⟨{lean_list(cfg_at(e,loCut,hiCut)[2],'L')}, false, {lean_list(cfg_at(e,loCut,hiCut)[4],'R')}⟩⟩ := by
{chr(10).join(f'  rw [show ({b} : Nat) = 38 + {b-38} from by decide, steps_add, r7f_G2_{i+1}, someBind]' for i, b in enumerate(range(e-(s+OFF['TAIL']), 0, -38)) if b > 38)}
  exact r7f_G2_{n2} L R
""")

# ============ 4. the factorisation ============
c0 = cfg_at(s, loCut, hiCut); c1 = cfg_at(e, loCut, hiCut)
emit(f"""set_option maxRecDepth 8000 in
set_option maxHeartbeats 2000000 in
/-- **`REGEN(7)` FACTORED — `glue ∘ REGEN(4) ∘ TOPGRIND(4) ∘ REGEN(5) ∘ DESCENT(5) ∘
REGEN(4) ∘ glue`.**  The `2530` steps of `exitSteps 7` at the TI-genuine window, assembled from
seven pieces at the TI-CONFIRMED offsets `241/311/526/744/1833/1903` (`exitSteps_7_split` is the
matching arithmetic).  FOUR of the seven are DISCHARGED BY REUSE, not by kernel runs: two
`regen4_transport`s and one `regen5_transport` (via `steps_pos_shift`), plus — new here — the
two `∀`-FAMILY glues `braid_topgrind 6 1` (§5af) and `descent_glue_expl 14 1 1` (§5ak).  That is
`70+215+218+1089+70 = 1662` of `2530` (66%) carried by `∀`-quantified lemmas; only the lead
`241` and trailing `627` are per-level `rfl`.

**HONEST SCOPE.**  `k=7` is the first level where the `∀`-covered families appear at all, and
this does NOT give `∀k`: the lead/trailing glue still has no law, and the IN config is a
HYPOTHESIS — reachability (`RegenLaw`, §5ai) is untouched.  `[propext, Quot.sound]`. -/
theorem regen7_factored (L R : List Bool) :
    steps (exitSteps 7) ⟨.E, 11, ⟨{lean_list(c0[2],'L')}, false, {lean_list(c0[4],'R')}⟩⟩
      = some ⟨.E, {c1[1]-PSHIFT}, ⟨{lean_list(c1[2],'L')}, false, {lean_list(c1[4],'R')}⟩⟩ := by
  rw [show exitSteps 7 = {OFF['R4a']} + (exitSteps 4 + ({TG_STEPS} + (exitSteps 5
        + ({DG_STEPS} + (exitSteps 4 + {e-(s+OFF['TAIL'])}))))) from by decide,
      steps_add, r7f_glue1, someBind,
      steps_add, r7f_regen4_site_1, someBind,
      steps_add, r7f_topgrind_site, someBind,
      steps_add, r7f_regen5_site, someBind,
      steps_add, r7f_descent_site, someBind,
      steps_add, r7f_regen4_site_2, someBind,
      r7f_glue2]
""")

open('/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/2d8c1f9f-0e02-4aa5-a7fc-fa27256534ce/scratchpad/r7f.lean','w').write("\n".join(OUT))
print(f"\nemitted {len(OUT)} theorems, G1 chunks={n1}, G2 chunks={n2}")
