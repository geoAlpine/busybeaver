#!/usr/bin/env python3
# verify_all.py -- one-command re-verification of the campaign's banked certificates (2026-07-07)
#
# Runs every assertion-checked verifier from the 2026-07-06/07 template/ledger campaign and
# reports PASS/FAIL per item. Each item is a standalone script that raises/asserts on failure.
# Heavy evidence runs (G=10^7 etc.) are NOT included -- this is the PROOF-PATH battery only.
#
#   usage: python3 verify_all.py [--quick]
#     --quick : skip items marked SLOW (> ~2 min)
#
# Item list (what each certifies):
#   o4_body_proof.py        o4 body lemma B(k)->B(k+2), k to 251           [PROVEN]
#   o4_growing_certify.py   3 growing configs = body iteration, non-halt    [PROVEN]
#   o4_wander_certify.py    4 configs translated-cycler certificates        [PROVEN]
#   o4_ledger_bijection.py  itinerary bijection L=1..8 + ruin constant      [PROVEN]
#   o4_closure_fixpoint.py  HALT-in-closure impossibility (no local cert)   [PROVEN]
#   o4_seam_lemma_verify.py seam decomposition census (assertions)          [PROVEN]
#   o3_body_proof.py        o3 body lemma, cycle certs p=10/20/6, j to 501  [PROVEN]
#   o18_depth_map.py        o18 pushdown-odometer transition table census   [PROVEN on grid]
#   o15_fp_vmap.py          o15 branch maps + fixed-point run laws          [PROVEN]
#   o17_gate_map_2026-07-07.py  o17 gate-to-gate map F islands              [exact map]
#   o4_bouncer_macro.py     macro-machine validation battery V1+V2 (SLOW)   [validated tool]
#
# Success criterion per item: exit code 0 AND no "FAIL"/"MISMATCH"/"NOT ESTABLISHED" in output.
# (Scripts with known benign non-assertion output are whitelisted below.)
import subprocess, sys, time, os

PY = sys.executable
HERE = os.path.dirname(os.path.abspath(__file__))

ITEMS = [
    # (script, slow?, forbidden-substrings, required-substrings)
    ("o4_body_proof.py",       False, ["NOT ESTABLISHED"], ["BODY LEMMA VERIFIED"]),
    ("o4_growing_certify.py",  False, ["FAIL"],            ["NON-HALTING"]),
    ("o4_wander_certify.py",   False, ["FAIL"],            ["all four NON-HALTING [PROVEN]"]),
    ("o4_ledger_bijection.py", False, ["NOT"],             ["bijection over 3^8 seeds: OK"]),
    ("o4_closure_fixpoint.py", False, [],                  ["certificate FAILS"]),  # the IMPOSSIBILITY result: closure must contain HALT
    ("o4_seam_lemma_verify.py",True,  ["AssertionError"],  ["ALL ASSERTIONS PASSED"]),
    ("o3_body_proof.py",       False, ["NOT ESTABLISHED"], ["BODY LEMMA VERIFIED"]),
    ("o18_depth_map.py",       True,  [],                  ["bad/unparsed/unsafe: NONE"]),
    ("o15_fp_vmap.py",         True,  ["MISMATCH"],        []),
    ("o17_gate_map_2026-07-07.py", True, [],               []),
    ("o4_bouncer_macro.py",    True,  ["FAILED", "MISMATCH -- NOT sound"], ["ALL VALIDATIONS PASSED"]),
]

def run(script, forbidden, required):
    t0 = time.time()
    try:
        p = subprocess.run([PY, os.path.join(HERE, script)], capture_output=True,
                           text=True, timeout=1800)
    except subprocess.TimeoutExpired:
        return ("TIMEOUT", time.time()-t0, "")
    out = p.stdout + p.stderr
    if p.returncode != 0:
        return ("ERROR(exit %d)" % p.returncode, time.time()-t0, out[-400:])
    for f in forbidden:
        if f in out:
            return ("FAIL(found %r)" % f, time.time()-t0, out[-400:])
    for r in required:
        if r not in out:
            return ("FAIL(missing %r)" % r, time.time()-t0, out[-400:])
    return ("PASS", time.time()-t0, "")

if __name__ == "__main__":
    quick = "--quick" in sys.argv
    results = []
    print("BB(6) campaign proof-path verification battery")
    print("=" * 64)
    for script, slow, forb, req in ITEMS:
        if quick and slow:
            print(f"  SKIP (slow)  {script}")
            continue
        if not os.path.exists(os.path.join(HERE, script)):
            print(f"  MISSING      {script}")
            results.append((script, "MISSING"))
            continue
        status, dt, tail = run(script, forb, req)
        print(f"  {status:<12} {script}  ({dt:.0f}s)")
        if status != "PASS" and tail:
            print("    --- tail ---")
            for line in tail.splitlines()[-6:]:
                print("    " + line)
        results.append((script, status))
    print("=" * 64)
    npass = sum(1 for _, s in results if s == "PASS")
    print(f"{npass}/{len(results)} PASS")
    sys.exit(0 if npass == len(results) else 1)
