# o18 CLEANUP task 1 (2026-07-08): resolve the 5 SPLIT adjudications left open by
# o18_r1_fuzz.py mode 'eq' (O18_R1_PINNING_2026-07-08.md sec 2).
#
# Background: mode_eq(seed=1, n=200000) found 60 base-vs-ext disagreements; 55 were
# adjudicated concretely (T_ext right, base wrong); 5 came back ('SPLIT', ...) from
# o18_r1_probe.probe_cell -- outcomes mixing 'UNSAFE-NONHALT' flags at small magnitudes.
# Suspected artifact (previously root-caused in O18_INVARIANT_SYNTHESIS L3): probe()
# free-runs up to maxF=24 F-entries, so the run-wide `unsafe` flag can be set by the
# CONTINUATION (later passes) halting, not by the pass under test; plus small-m boundary
# effects where 1^m is too short for the word template.
#
# This script:
#   phase 1 -- reproduce the disagreement set EXACTLY (same PRNG, seed 1, n 200000;
#              pure symbolic, no simulation), re-run probe_cell on each, and extract
#              the SPLIT cells (must be 5, matching the pinning note).
#   phase 2 -- for each SPLIT cell (r,w): fresh concrete probes at >=8 magnitudes of m
#              (m == r mod 3, up to ~10^4) with PER-PASS ISOLATION: run_cfg is stopped
#              at the FIRST ANCHORED F-entry (iterating maxF upward), so `unsafe` and
#              the outcome are attributed to THIS pass only.  Also a small-m scan
#              (every m == r mod 3 from 4 to ~90) to locate any template threshold.
#   verdicts -- per cell: {EXT-RIGHT / BASE-RIGHT / MAGNITUDE-DEPENDENT (CRITICAL:
#              breaks (m mod 3, w)-determinism) / SMALL-M-BOUNDARY (harmless,
#              threshold documented)}.
import sys, random, pickle, time
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from o18_md_rules import T, Unknown
from o18_md_rules_ext import T_ext
from o18_md_probe import word_blocks, parse_word, wstr
from o18_depth_map import run_cfg
from o18_r1_fuzz import rand_word
from o18_r1_probe import probe_cell

SCR = '/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/8b7a3f39-ce4e-4044-afe8-60ce3b3aedcf/scratchpad'


def reproduce_disagreements(seed=1, n=200000):
    """Symbolic-only replay of o18_r1_fuzz.mode_eq's word stream (identical PRNG use)."""
    rng = random.Random(seed)
    disags = []
    for i in range(n):
        w = rand_word(rng, deep_bias=(i % 2 == 0))
        for r in (0, 1, 2):
            try:
                a = T(r, w)
            except Unknown:
                a = None
            try:
                b = T_ext(r, w)
            except Unknown:
                b = None
            if a is not None and b != a:
                disags.append((r, w, a, b))
    return disags


def probe_isolated(m, w, kmax=60, budget=None):
    """One PASS of the machine on (m,w), stopped at the FIRST ANCHORED F-entry, so the
    unsafe flag is per-pass (no continuation attribution).  Iterates run_cfg's maxF
    upward: interior F-entries (hp>0) are not pass boundaries and are skipped, but each
    retry stops the run at exactly the k-th F-entry, so when the anchored entry is hit
    the run has executed NOTHING beyond it.  Returns (kind, out, unsafe)."""
    for k in range(1, kmax + 1):
        status, fents, steps, unsafe = run_cfg(word_blocks(m, w), maxF=k,
                                               budget=budget, lpadf=10)
        if fents and len(fents) == k:
            s, clean, land, R, hp = fents[-1]
            if clean:
                return ('LAND', land, unsafe)
            if hp <= 0:
                p = parse_word(R, hp)
                if p is not None:
                    return ('MOVE', p, unsafe)
                return ('UNPARSED', (R, hp), unsafe)
            continue  # interior entry: not a pass boundary; extend the run by one entry
        # run ended before reaching a k-th F-entry: HALT/OVERFLOW/BUDGET inside this pass
        if status == 'HALT':
            return ('HALT', None, unsafe)
        return (status, None, unsafe)
    return ('MAXK', None, None)


def outcome_key(m, res):
    """Normalize an isolated-probe result to the (kind, c, w') pass law for comparison."""
    kind, out, unsafe = res
    if kind == 'MOVE':
        m2, w2 = out
        return ('MOVE', 3 * m2 - 8 * m, w2), unsafe
    if kind == 'LAND':
        return ('LAND', 3 * out - 8 * m), unsafe
    return (kind,), unsafe


def mags_for(r, uptolarge=True):
    base = [13, 40, 100, 301, 601, 1000, 3001] + ([9999] if uptolarge else [])
    return sorted({m + ((r - m) % 3) for m in base})


if __name__ == '__main__':
    print('phase 1: reproducing the mode_eq(seed=1, n=200000) disagreement set (symbolic)...',
          flush=True)
    disags = reproduce_disagreements()
    print(f'  disagreements: {len(disags)} (pinning note: 60)')
    # adjudicate exactly as the original did, to recover the 5 SPLITs
    splits, resolved = [], 0
    for r, w, a, b in disags[:60]:
        conc = probe_cell(r, w)
        if conc[0] == 'SPLIT' or any(isinstance(x, tuple) and x and x[0] == 'UNSAFE-NONHALT'
                                     for x in (conc[1] if conc[0] == 'SPLIT' else ())):
            splits.append((r, w, a, b, conc))
        else:
            ext_ok = (conc == b) or (conc[0] == 'HALT' and b[0] == 'HALT')
            base_ok = (conc == a) or (conc[0] == 'HALT' and a[0] == 'HALT')
            if ext_ok and not base_ok:
                resolved += 1
            else:
                splits.append((r, w, a, b, conc))   # anything not clean-ext-win
    print(f'  clean T_ext-right adjudications: {resolved}; unresolved (SPLIT/other): {len(splits)}')
    with open(SCR + '/o18_clean_splits.pkl', 'wb') as f:
        pickle.dump(splits, f)

    print('\nphase 2: per-pass-isolated deep probing of each unresolved cell', flush=True)
    verdicts = []
    for idx, (r, w, a, b, conc) in enumerate(splits):
        print(f'\n=== case {idx}: r={r}  w={wstr(w)}  ({w})')
        print(f'    base T   = {a}')
        print(f'    T_ext    = {b}')
        print(f'    original probe_cell (maxF=24, run-wide unsafe) = {conc}')
        # (a) small-m scan for the template threshold
        small = []
        m0 = r if r >= 4 else r + (3 if r > 0 else 6)
        m = m0
        while m <= 91:
            res = probe_isolated(m, w)
            key, unsafe = outcome_key(m, res)
            small.append((m, key, unsafe))
            m += 3
        # (b) large magnitudes
        large = []
        for m in mags_for(r):
            t0 = time.time()
            res = probe_isolated(m, w)
            key, unsafe = outcome_key(m, res)
            large.append((m, key, unsafe))
            print(f'    m={m:5d}: {key}  unsafe={unsafe}  ({time.time()-t0:.1f}s)', flush=True)
        # threshold analysis on the small scan: find where the outcome stabilizes to the
        # asymptotic (largest-m) outcome
        asym = large[-1][1]
        thr = None
        for m, key, u in small:
            if key != asym:
                thr = m  # last small-m deviation
        firsts = [(m, key) for m, key, u in small if key != asym]
        print(f'    small-m scan (m={m0}..91 step 3): '
              f'{len(firsts)} deviations from asymptotic outcome'
              + (f'; deviating m: {[m for m, _ in firsts]}' if firsts else ''))
        for m, key, u in small:
            mark = '   <-- differs' if key != asym else ''
            if key != asym or m <= m0 + 9:
                print(f'      m={m:3d}: {key} unsafe={u}{mark}')
        # verdict
        stable = [key for m, key, u in large if m >= 40]
        unsafe_iso = [u for m, key, u in large if m >= 40]
        ext_match = all(k == b or (k[0] == 'HALT' and b[0] == 'HALT') for k in stable)
        base_match = all(k == a or (k[0] == 'HALT' and a[0] == 'HALT') for k in stable)
        if len(set(stable)) > 1:
            v = 'MAGNITUDE-DEPENDENT  *** CRITICAL: breaks (m mod 3, w)-determinism ***'
        elif ext_match and not base_match:
            v = ('EXT-RIGHT (T_ext matches the isolated single-pass outcome at all '
                 f'magnitudes >= 40; base wrong)')
        elif base_match and not ext_match:
            v = 'BASE-RIGHT  *** unexpected: T_ext bug ***'
        elif ext_match and base_match:
            v = 'BOTH-RIGHT (a == b on the stable outcome?)'
        else:
            v = f'NEITHER matches: concrete stable outcome {stable[0]}'
        if thr is not None and len(set(stable)) == 1:
            v += f'; small-m deviations up to m={thr} (template threshold; harmless)'
        if any(unsafe_iso):
            v += '  [WARNING: isolated unsafe flag persists at m>=40]'
        else:
            v += '; per-pass isolated unsafe=0 at all m>=40 (original UNSAFE-NONHALT was continuation attribution)'
        print(f'    VERDICT: {v}')
        verdicts.append((r, w, v, small, large))
    with open(SCR + '/o18_clean_split_verdicts.pkl', 'wb') as f:
        pickle.dump(verdicts, f)
    print('\nsummary:')
    for r, w, v, _, _ in verdicts:
        print(f'  r={r} w={wstr(w)}: {v.splitlines()[0]}')
