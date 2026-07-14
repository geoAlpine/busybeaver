#!/usr/bin/env python3
"""x2ck_regen_ti.py -- THE DECISIVE closure experiment.

Is the full REGEN(k) sub-block (lay 1^{2^k-3} top block + regenerate the descending
cascade below, ending in TERM(k)) a TRANSLATION-INVARIANT transport -- i.e. the same
(state,head,dpos) trace at every occurrence, differing only in the L/R padding?

If YES: carryExit closes as a structural recursion of reusable ∀L∀R transports.
If NO : REGEN's body depends on level context -> stays [DESIGN].

REGEN(k) = EXIT(k-1) lays block k.  Occurrences of a k=5 REGEN: EXIT(4)=[6923,7141]
(standalone) and inside EXIT(6) (the k=5 sub-regeneration, terminal g74 @13379).
We compare the (state,head,dpos) relative traces.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build


def rel_trace(n0, n1):
    """(state, head-bit, pos-pos0) trace over [n0,n1)."""
    sim = build(2); sim.step()
    while sim.n < n0: sim.step()
    p0 = sim.pos
    tr = []
    while sim.n < n1:
        tr.append((sim.st, sim.h, sim.pos - p0))
        if not sim.step(): break
    return tr


def find_terminal_starts(k_term_gap, cap=60000):
    """find all anchor pairs whose gap == k_term_gap (a TERM(k) terminal)."""
    sim = build(2); sim.step()
    A=[]
    while sim.n < cap:
        if sim.st=='E' and sim.h==0: A.append(sim.n)
        if not sim.step(): break
    out=[]
    for i in range(len(A)-1):
        if A[i+1]-A[i]==k_term_gap:
            out.append((A[i],A[i+1]))
    return out

# TERM(5)=74. Its occurrences (end-of-REGEN(5)).
t5 = find_terminal_starts(74)
print("TERM(5)=74 occurrences (anchor n -> n):", t5)
# TERM(4)=41
t4 = find_terminal_starts(41)
print("TERM(4)=41 occurrences:", t4)
# TERM(6)=139
t6 = find_terminal_starts(139)
print("TERM(6)=139 occurrences:", t6)

# REGEN(k) starts at the anchor right after the FOLD that opens EXIT(k-1). Its length
# is exitSteps(k). REGEN(5) length=218. So window ends at the TERM(5) terminal-end.
# For each TERM(5) occurrence (ending at e), REGEN(5) window = [e-218, e].
print("\n=== REGEN(5) full-window translation-invariance test (len 218) ===")
regen5_windows = [(e-218, e) for (s,e) in t5]
print("windows:", regen5_windows)
traces = [rel_trace(a,b) for (a,b) in regen5_windows]
if len(traces) >= 2:
    print("lengths:", [len(t) for t in traces])
    same = all(t == traces[0] for t in traces)
    print("ALL REGEN(5) rel-traces IDENTICAL:", same)
    if not same:
        # find first divergence
        for idx in range(min(len(x) for x in traces)):
            col = set(t[idx] for t in traces)
            if len(col) > 1:
                print(f"  first divergence at step {idx}: {[t[idx] for t in traces]}")
                break

print("\n=== REGEN(4) full-window test (len 70) ===")
regen4_windows = [(e-70, e) for (s,e) in t4]
print("windows:", regen4_windows)
tr4 = [rel_trace(a,b) for (a,b) in regen4_windows]
if len(tr4) >= 2:
    print("lengths:", [len(t) for t in tr4])
    print("ALL REGEN(4) rel-traces IDENTICAL:", all(t==tr4[0] for t in tr4))
    for idx in range(min(len(x) for x in tr4)):
        col=set(t[idx] for t in tr4)
        if len(col)>1:
            print(f"  first divergence at step {idx}: {[t[idx] for t in tr4]}"); break
