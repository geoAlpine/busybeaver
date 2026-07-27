"""Zero-cost falsification test: do any of the NAMED cryptids -- classified '(K), all of them'
by simulation -- satisfy the exact comb-doubler interface?  A single hit would be a
counterexample to a load-bearing claim.  Also report the gradient, which is a finer probe than
a yes/no."""
from atoms_flex_scan import flex_scan, NAMES, span_coeffs
from atoms_island_scan import SC
NAMED = [
 ("Antihydra","1RB1RA_0LC1LE_1LD1LC_1LA0LB_1LF1RE_---0RA"),
 ("o2","1RB1RC_1LC1LE_1RA1RD_0RF0RE_1LA0LB_---1RA"),
 ("o3","1RB1LD_1RC1RE_0LA1LB_0LD1LC_1RF0RA_---0RC"),
 ("o4","1RB0LD_1RC1RF_1LA0RA_0LA0LE_1LD1LA_0RB---"),
 ("o5","1RB0LB_1LC0RE_1LA1LD_0LC---_0RB0RF_1RE1RB"),
 ("o7","1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC"),
 ("o8","1RB1LA_0LC0RC_1LE1RD_1RE1RC_1LF0LA_---1LE"),
 ("o10","1RB1RA_0RC1RC_1LD0LF_0LE1LE_1RA0LB_---0LC"),
 ("o11","1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF"),
 ("o12","1RB0RE_1LC1LD_0RA0LD_1LB0LA_1RF1RA_---1LB"),
 ("o13","1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA"),
 ("o14","1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE"),
 ("o15","1RB---_0RC0RE_1RD1RF_1LE0LB_1RC0LD_1RC1RA"),
 ("o16","1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE"),
 ("o17","1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"),
 ("o18","1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---"),
 ("SpaceNeedle","1RB1LA_0LC0RE_1LD1LB_1RE1LF_1RC0RA_0RC---"),
]
print("named cryptid : best atoms held (out of 6) under the EXACT comb-doubler interface")
hits=[]
for nm, sp in NAMED:
    try:
        best, res = flex_scan(sp)
    except Exception as e:
        print(f"  {nm:12s} : error {e}"); continue
    miss = sorted(set(NAMES) - res[0][3])
    tag = "  <== FULL INTERFACE" if best==6 else ""
    if best==6: hits.append(nm)
    print(f"  {nm:12s} : {best}/6   missing {miss}{tag}")
print()
print(f"=> named cryptids matching the comb-doubler interface: {len(hits)}  {hits}")
print("   (a hit would contradict 'the named 19 are all (K)'; no hit leaves that claim standing")
print("    for THIS interface only -- it says nothing about other mechanisms.)")
