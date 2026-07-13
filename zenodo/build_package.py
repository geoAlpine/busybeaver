#!/usr/bin/env python3
# Zenodo package builder (2026-07-08).
# Assembles the curated artifact: papers + verification battery (self-contained) + Lean layer + supporting notes.
# Then SELF-TESTS: extracts to a temp dir and runs verify_all.py --quick inside it.
import os, re, shutil, zipfile, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def _ver():
    if "--version" in sys.argv:
        return sys.argv[sys.argv.index("--version")+1]
    return "1.0"
VERSION = None  # set in main()

PAPERS = ["PAPER_RUN_STRUCTURE.md", "PAPER_TEMPLATE_METHOD.md", "PAPER_SPECIES_SURVEY.md",
          "PAPER_MIRROR_LADDER.md", "PAPER_CENSUS.md", "PAPER_RIGIDITY_LIMITS.md",
          "MINIMAL_OPEN_KERNEL.md", "PAPER_X2_INTEGER_DOUBLER.md"]

# verification battery: verify_all.py + its 11 items + their imports (import-closure, hand-audited)
VERIFICATION = [
    "verify_all.py",
    "o4_body_proof.py", "o4_growing_certify.py", "o4_wander_certify.py",
    "o4_ledger_bijection.py", "o4_closure_fixpoint.py", "o4_seam_lemma_verify.py",
    "o3_body_proof.py", "o18_depth_map.py", "o15_fp_vmap.py",
    "o17_gate_map_2026-07-07.py", "o4_bouncer_macro.py",
    # import closure:
    "o18_md_rules.py", "o18_md_probe.py", "o18_md_rules_ext.py",  # ext incl. for the documented correction
    "o4_coboundary_lp.py", "ah_ledger_criticality.py", "mirror_census.py", "freq_rundepth_whiteness.py",  # bonus exact certificates
]

LEAN = ["lean/RunStructure.lean", "lean/Template.lean", "lean/Suffix.lean", "lean/Mirror.lean",
        "lean/lakefile.toml", "lean/lean-toolchain", "lean/lake-manifest.json",
        "lean/O3.lean", "lean/O18.lean", "lean/O2.lean", "lean/O17.lean", "lean/Completion.lean",
        "lean/X2.lean",
        "lean/crosscheck.py", "lean/template_crosscheck.py",
        "lean/suffix_crosscheck.py", "lean/o3_crosscheck.py", "lean/o18_crosscheck.py",
        "LEAN_STATUS_2026-07-07.md"]

NOTES = [
    # the papers' "References to the record" + audit/corrections trail
    "O4_TEMPLATE_CLOSURE_2026-07-06.md", "O4_LEDGER_ANALYSIS_2026-07-06.md",
    "O4_RUN_STRUCTURE_2026-07-07.md", "O4_WINDOW_SATURATION_2026-07-06.md",
    "O4_SEAM_PARITY_LEMMA_2026-07-06.md", "O4_CSEAM_LOCALIZATION_2026-07-06.md",
    "O4_GROWING_REGIME_2026-07-07.md", "O4_GROWING_BUDGET_ASSESSMENT_2026-07-07.md",
    "O4_COBOUNDARY_LP_2026-07-08.md",
    "O3_TEMPLATE_PORT_2026-07-06.md",
    "O15_TEMPLATE_PORT_2026-07-07.md", "O15_FIXEDPOINT_2026-07-07.md",
    "O17_HALT_FLAVOR_2026-07-06.md", "O17_GATE_LAW_2026-07-07.md",
    "O18_TEMPLATE_PORT_2026-07-07.md", "O18_DEPTH_UNIFORM_2026-07-07.md",
    "O18_MULTIDEFECT_2026-07-07.md", "O18_INVARIANT_SYNTHESIS_2026-07-07.md",
    "O18_ANNEALED_STANDOFF_2026-07-07.md", "O18_R1_PINNING_2026-07-08.md",
    "O15_O18_IDENTITY_2026-07-07.md", "NOVELTY_AUDIT_2026-07-07.md",
    "O18_CLEANUP_2026-07-08.md", "X32_CLEANUP_2026-07-08.md",
    "BB6_CRYPTID_SPECIES_2026-07-07.md", "ANTIHYDRA_LEDGER_UNIFICATION_2026-07-07.md",
    "X32_FAMILY_REDUCTIONS_2026-07-07.md", "O2_LINK0_CERTIFIED_2026-07-08.md",
    "MAHLER_SEA_CLASSIFICATION_2026-07-07.md", "O11_REFILL_LAW_2026-07-08.md",
    "O13_O14_FIXEDPOINT_2026-07-08.md", "O16_SPACENEEDLE_FIXEDPOINT_2026-07-08.md",
    "FREQUENCY_AXIS_PROBE_2026-07-08.md", "O7_AND_CENSUS_COMPLETENESS_2026-07-09.md",
    "CAMPAIGN_2026-07-06_TEMPLATE_LEDGER.md", "BB6_FRAMEWORK_PACKAGE.md",
    # --- the (K)-wall program: synthesis + the complete-proof frame (2026-07-09/10) ---
    "ROADMAP_COMPLETE_PROOF_2026-07-10.md", "COMPLETION_SKELETON_2026-07-10.md",
    "OPEN_PROBLEM_2026-07-10.md", "ATTACK_PLAN_2026-07-10.md",
    "NEWMATH_BUILD_SYNTHESIS_2026-07-09.md", "NEWMATH_SOLENOID_BUILD_2026-07-09.md",
    "NEWMATH_DIGIT_BRIDGE_2026-07-09.md", "O4_NEWMATH_BUILD_2026-07-09.md",
    "RELOAD_EXCURSION_BUILD_2026-07-09.md", "RELOAD_MAP_UNIFIED_2026-07-09.md",
    "RIGIDITY_LIMITS_HOST_2026-07-09.md", "U0_EXCLUSION_BUILD_2026-07-10.md",
    "JOINT_ADELIC_BUILD_2026-07-10.md", "O4_CERTIFIED_FREQUENCY_BUILD_2026-07-10.md",
    # --- the (K)-wall tool sweep (2026-07-10): all honest negatives, each a sharp characterization ---
    "O4_EXPSUM_FREQUENCY_BUILD_2026-07-10.md", "O4_TRANSFER_OPERATOR_BUILD_2026-07-10.md",
    "O4_CHRISTOL_TEST_2026-07-10.md", "O4_GOWERS_TEST_2026-07-10.md",
    "O4_OSTROWSKI_TEST_2026-07-10.md", "O4_FREQUENCY_RIGIDITY_2026-07-10.md",
    "O4_PADIC_DYNAMICS_2026-07-10.md", "O4_EQUIVALENTS_SEARCH_2026-07-10.md",
    # --- Category B decision attempts (2026-07-10): the thin-set / timing walls ---
    "O7_DECISION_ATTEMPT_2026-07-10.md", "SPACENEEDLE_DECISION_ATTEMPT_2026-07-10.md",
    "O17_GATE_DECISION_ATTEMPT_2026-07-10.md", "O7_TRANSCENDENCE_ATTEMPT_2026-07-10.md",
    "SPACENEEDLE_TRANSCENDENCE_ATTEMPT_2026-07-10.md", "HOLDOUT_SWEEP_FEASIBILITY_2026-07-10.md",
    # --- the integer-doubler (x2) machine: the carry-transparent decision candidate (2026-07-11..13) ---
    "X2_FRONTIER_MAP_2026-07-11.md", "X2_STATUS_2026-07-12.md",
    "X2_WELLFOUNDED_DESIGN_2026-07-12.md",
]

META = ["zenodo/README_ZENODO.md", "zenodo/CITATION.cff",
        "zenodo/LICENSE-DOCS", "zenodo/LICENSE-CODE", "zenodo/metadata.json"]

def main():
    global VERSION
    VERSION = _ver()
    out = os.path.join(ROOT, "zenodo", f"bb6-cryptid-frontier-v{VERSION}.zip")
    missing = [f for group in (PAPERS, VERIFICATION, LEAN, NOTES, META) for f in group
               if not os.path.exists(os.path.join(ROOT, f))]
    if missing:
        print("MISSING FILES:"); [print("  ", m) for m in missing]; sys.exit(1)

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        readme = open(os.path.join(ROOT, "zenodo/README_ZENODO.md")).read()
        readme = re.sub(r"version \d+\.\d+(\.\d+)? \(", f"version {VERSION} (", readme)
        readme = re.sub(r"\(Version \d+\.\d+(\.\d+)?\)", f"(Version {VERSION})", readme)
        z.writestr("README.md", readme)
        for f in ["zenodo/CITATION.cff", "zenodo/LICENSE-DOCS", "zenodo/LICENSE-CODE", "zenodo/metadata.json"]:
            z.write(os.path.join(ROOT, f), os.path.basename(f))
        for f in PAPERS:        z.write(os.path.join(ROOT, f), f"papers/{f}")
        for f in VERIFICATION:  z.write(os.path.join(ROOT, f), f"verification/{f}")
        for f in LEAN:          z.write(os.path.join(ROOT, f), f.replace("lean/", "lean/", 1) if f.startswith("lean/") else f"lean/{os.path.basename(f)}")
        for f in NOTES:         z.write(os.path.join(ROOT, f), f"notes/{f}")
    size = os.path.getsize(out)
    print(f"built {out}  ({size/1e6:.2f} MB)")

    # SELF-TEST: extract + run verify_all --quick inside
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(out) as z: z.extractall(td)
        r = subprocess.run([sys.executable, "verify_all.py", "--quick"],
                           cwd=os.path.join(td, "verification"),
                           capture_output=True, text=True, timeout=600)
        tail = "\n".join((r.stdout + r.stderr).splitlines()[-4:])
        print("self-test (verify_all --quick) tail:\n" + tail)
        ok = r.returncode == 0
        print("SELF-CONTAINMENT:", "PASS" if ok else "FAIL")
        sys.exit(0 if ok else 2)

if __name__ == "__main__":
    main()
