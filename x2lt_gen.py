#!/usr/bin/env python3
"""x2lt_gen.py -- emit the FACTORISED regen6: glue(154) . regen4_transport . glue(498).

Uses the SAME fixed absolute tape cut as x2r6_gen.py so the chunks compose under
`steps_add`, but the chunk boundaries are aligned to the REGEN(4) SUB-TRANSPORT
(TI-confirmed at offset 154, x2lt_ti.py) instead of a blind 38-step grid.

SIMULATOR EVIDENCE ONLY.  Lean's kernel `rfl` is the final judge of every chunk.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2r6_gen import window, cfg_at, lean_list

k = 6
s, e, LEN, loCut, hiCut = window(k)
PSHIFT = cfg_at(s, loCut, hiCut)[1] - 11     # re-anchor REGEN(6) IN pos to 11
OFF4 = 154                                   # TI-confirmed REGEN(4) site
LEN4 = 70                                    # exitSteps 4

print(f"REGEN(6) window [{s},{e}] len={LEN}, cut lo={loCut} hi={hiCut}, PSHIFT={PSHIFT}")
a4, b4 = s + OFF4, s + OFF4 + LEN4
print(f"REGEN(4) sub-window raw [{a4},{b4}]  offsets [{OFF4},{OFF4+LEN4}]")

# ---- sanity: the site config IS regen4_transport's IN shape (Lean-cut view) ----
c1 = cfg_at(a4, loCut, hiCut); c2 = cfg_at(b4, loCut, hiCut)
R4_IN_L = [1]*12 + [1,0,1,0,0,1,0]
R4_IN_R = [0,1,0] + [0]*10
R4_OUT_L = [0,1,0]
R4_OUT_R = [0,0,0]+[1]*13+[0,0]+[1]*5+[0,0]+[1,0,0,0]
assert c1[0]=='E' and c1[3]==0, "site IN state/head"
assert c1[2][:19] == R4_IN_L, "site IN left != regen4 IN left"
assert c1[4][:13] == R4_IN_R, "site IN right != regen4 IN right"
assert c2[0]=='E' and c2[3]==0, "site OUT state/head"
assert c2[2][:3] == R4_OUT_L, "site OUT left"
assert c2[4][:29] == R4_OUT_R, "site OUT right"
D = (c1[1]-PSHIFT) - 9
print(f"  site IN  pos(re-anchored) = {c1[1]-PSHIFT}   regen4 IN pos = 9   => d = {D}")
print(f"  site OUT pos(re-anchored) = {c2[1]-PSHIFT}   regen4 OUT pos = -7 => d = {(c2[1]-PSHIFT)-(-7)}")
assert D == (c2[1]-PSHIFT)-(-7), "pos shift not constant across the sub-transport!"
print(f"  *** regen4_transport applies at this site with a CONSTANT pos shift d = {D} ***")
print(f"  regen4 L-tail  = {len(c1[2])-19} explicit cells ++ L")
print(f"  regen4 R-tail  = {len(c1[4])-13} explicit cells ++ R")

def emit_chunks(name, lo, hi, ch=38):
    """chunks covering raw [lo,hi] in <=ch steps, as `rfl` theorems."""
    bounds = list(range(lo, hi, ch)) + [hi]
    out=[]
    for i in range(len(bounds)-1):
        x,y = bounds[i], bounds[i+1]
        ca=cfg_at(x,loCut,hiCut); cb=cfg_at(y,loCut,hiCut)
        out.append((f"{name}{i+1}", y-x, ca, cb))
    return out

def thm(nm, n, ca, cb):
    return (f"theorem {nm} (L R : List Bool) :\n"
            f"    steps {n} ⟨.{ca[0]}, {ca[1]-PSHIFT}, ⟨{lean_list(ca[2],'L')}, "
            f"{'true' if ca[3] else 'false'}, {lean_list(ca[4],'R')}⟩⟩\n"
            f"      = some ⟨.{cb[0]}, {cb[1]-PSHIFT}, ⟨{lean_list(cb[2],'L')}, "
            f"{'true' if cb[3] else 'false'}, {lean_list(cb[4],'R')}⟩⟩ :=\n  rfl\n")

g1 = emit_chunks("r6f_G1_", s, a4)
g2 = emit_chunks("r6f_G2_", b4, e)
print(f"\nglue1: {len(g1)} chunks {[n for _,n,_,_ in g1]} sum={sum(n for _,n,_,_ in g1)} (=154?)")
print(f"glue2: {len(g2)} chunks {[n for _,n,_,_ in g2]} sum={sum(n for _,n,_,_ in g2)} (=498?)")

def nest(ns):
    r = str(ns[-1])
    for n in reversed(ns[:-1]): r = f"{n}+({r})"
    return r

def compose(nm, chunks, total):
    ns=[n for _,n,_,_ in chunks]
    ca=chunks[0][2]; cb=chunks[-1][3]
    rw = "".join(f"steps_add, {c[0]}, someBind,\n      " for c in chunks[:-1]) + chunks[-1][0]
    body = (f"theorem {nm} (L R : List Bool) :\n"
            f"    steps {total} ⟨.{ca[0]}, {ca[1]-PSHIFT}, ⟨{lean_list(ca[2],'L')}, "
            f"{'true' if ca[3] else 'false'}, {lean_list(ca[4],'R')}⟩⟩\n"
            f"      = some ⟨.{cb[0]}, {cb[1]-PSHIFT}, ⟨{lean_list(cb[2],'L')}, "
            f"{'true' if cb[3] else 'false'}, {lean_list(cb[4],'R')}⟩⟩ := by\n")
    if len(ns)==1:
        body += f"  exact {chunks[0][0]} L R\n"
    else:
        body += f"  rw [show ({total} : Nat) = {nest(ns)} from by decide,\n      {rw}]\n"
    return body

# ---- the REGEN(4) site lemma, proved FROM regen4_transport (no kernel re-run) ----
Ltail = lean_list(c1[2][19:], 'L')
Rtail = lean_list(c1[4][13:], 'R')
site = (f"theorem r6f_regen4_site (L R : List Bool) :\n"
        f"    steps (exitSteps 4) ⟨.{c1[0]}, {c1[1]-PSHIFT}, ⟨{lean_list(c1[2],'L')}, "
        f"{'true' if c1[3] else 'false'}, {lean_list(c1[4],'R')}⟩⟩\n"
        f"      = some ⟨.{c2[0]}, {c2[1]-PSHIFT}, ⟨{lean_list(c2[2],'L')}, "
        f"{'true' if c2[3] else 'false'}, {lean_list(c2[4],'R')}⟩⟩ := by\n"
        f"  rw [show (({c1[1]-PSHIFT} : Int)) = 9 + {D} from by decide,\n"
        f"      show (({c2[1]-PSHIFT} : Int)) = -7 + {D} from by decide]\n"
        f"  exact steps_pos_shift (regen4_transport ({Ltail}) ({Rtail}))\n")

ci = cfg_at(s, loCut, hiCut); co = cfg_at(e, loCut, hiCut)
final = (f"theorem regen6_factored (L R : List Bool) :\n"
         f"    steps (exitSteps 6) ⟨.{ci[0]}, {ci[1]-PSHIFT}, ⟨{lean_list(ci[2],'L')}, "
         f"{'true' if ci[3] else 'false'}, {lean_list(ci[4],'R')}⟩⟩\n"
         f"      = some ⟨.{co[0]}, {co[1]-PSHIFT}, ⟨{lean_list(co[2],'L')}, "
         f"{'true' if co[3] else 'false'}, {lean_list(co[4],'R')}⟩⟩ := by\n"
         f"  rw [show exitSteps 6 = 154 + (exitSteps 4 + 498) from by decide,\n"
         f"      steps_add, r6f_glue1, someBind,\n"
         f"      steps_add, r6f_regen4_site, someBind,\n"
         f"      r6f_glue2]\n")

parts = ([thm(*c) for c in g1] + [compose("r6f_glue1", g1, 154)]
         + [site] + [thm(*c) for c in g2] + [compose("r6f_glue2", g2, 498)] + [final])
OUT='/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/2d8c1f9f-0e02-4aa5-a7fc-fa27256534ce/scratchpad/r6f.lean'
open(OUT,'w').write("\n".join(parts))
print(f"\nwritten {OUT}")
