#!/usr/bin/env python3
"""x2fr_state.py -- reconstruct the FULL register state at each chew-start and
test whether the odometer is a PURE (tape-free) register.

At every E-on-0 anchor we decode the complete tape into an abstract state:
  right cascade  = full list of 1-run lengths to the right of head (big->small
                   as encountered), the "todo/built cascade"
  comb           = number of leading (01)-comb pairs on the left
We then keep only chew-starts, and CHECK: is (state_{i+1}) a deterministic
function of (state_i) alone?  If a repeated state_i ever maps to two different
state_{i+1}, the register is NOT pure (tape-determined).  If the map is single-
valued on the whole orbit, the register is a candidate faithful pure model.
"""
import sys, pickle
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
from x2bd_outer import right_first_block, left_comb_pairs


def right_run_vector(sim):
    """full list of 1-run lengths to the right (head-first)."""
    bits = [sim.h] + sim.R[::-1]
    runs = []
    i = 0
    while i < len(bits):
        b = bits[i]; j = i
        while j < len(bits) and bits[j] == b:
            j += 1
        if b == 1:
            runs.append(j - i)
        i = j
    return tuple(runs)


def left_full(sim):
    """full left stack, nearest-first, as run tokens (bit,len)."""
    L = sim.L
    runs = []
    i = 0
    n = len(L)
    while i < n:
        b = L[-1-i]; j = i
        while j < n and L[-1-j] == b:
            j += 1
        runs.append((b, j-i))
        i = j
    return tuple(runs)


def collect(g, cap=200_000_000):
    sim = build(g); sim.step()
    miles = 0
    states = []   # (n, blk, comb, rightvec, leftruns)
    while True:
        if sim.is_milestone():
            miles += 1
            if miles == 6:
                states.append((sim.n, right_first_block(sim), left_comb_pairs(sim),
                               right_run_vector(sim), left_full(sim)))
                break
        if miles >= 5 and sim.st == 'E' and sim.h == 0:
            states.append((sim.n, right_first_block(sim), left_comb_pairs(sim),
                           right_run_vector(sim), left_full(sim)))
        if not sim.step():
            break
    return states


def chew_start_states(states):
    # local maxima of blk among the E-on-0 states
    out = []
    for i in range(len(states)):
        blk = states[i][1]
        prev = states[i-1][1] if i > 0 else -1
        nxt = states[i+1][1] if i+1 < len(states) else -1
        if blk >= 5 and blk > prev and blk >= nxt:
            out.append(states[i])
    return out


if __name__ == "__main__":
    g = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    states = collect(g)
    css = chew_start_states(states)
    print(f"g={g} K={g+8}: {len(css)} chew-starts, {len(states)} anchors")
    # Build the pure register state = (rightvec, comb).  Test determinism of the
    # transition (rightvec_i, comb_i) -> (rightvec_{i+1}, comb_{i+1}).
    reg = [(c[3], c[2]) for c in css]     # (rightvec, comb)
    trans = {}
    violations = 0
    for i in range(len(reg)-1):
        k = reg[i]; v = reg[i+1]
        if k in trans and trans[k] != v:
            violations += 1
            if violations <= 5:
                print("NONDET at state", k, "->", trans[k], "AND", v)
        trans[k] = v
    print(f"distinct chew-start register states: {len(set(reg))}")
    print(f"PURE-REGISTER determinism violations: {violations}")
    if violations == 0:
        print("  => the (rightvec,comb) register is a PURE deterministic function of itself.")
    # save
    sp='/private/tmp/claude-502/-Users-aokiyousuke-busybeaver/8b7a3f39-ce4e-4044-afe8-60ce3b3aedcf/scratchpad'
    with open(f'{sp}/reg_g{g}.pkl','wb') as f:
        pickle.dump(reg, f)
