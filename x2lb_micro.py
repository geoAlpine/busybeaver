#!/usr/bin/env python3
"""x2lb_micro.py -- dump EVERY E-on-0 anchor in a window, with (comb, cascade
block vector), to read the exact odometer micro-rule for the pure Layer-B model."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2bd_sim import build
from x2bd_outer import right_first_block, left_comb_pairs


def right_block_vector(sim):
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
    return runs


if __name__ == "__main__":
    g = 2
    nlo = int(sys.argv[1]) if len(sys.argv) > 1 else 6484
    nhi = int(sys.argv[2]) if len(sys.argv) > 2 else 6760
    sim = build(g); sim.step()
    miles = 0
    while True:
        if sim.is_milestone():
            miles += 1
            if miles == 6: break
        if miles >= 5 and sim.st == 'E' and sim.h == 0 and nlo <= sim.n <= nhi:
            vec = right_block_vector(sim)
            # strip frozen big tail: keep blocks until we hit one >= 1000
            active = []
            for b in vec:
                if b >= 900: break
                active.append(b)
            print(f" n={sim.n:<7} comb={left_comb_pairs(sim):<4} blk={right_first_block(sim):<4} active={active}")
        if sim.n > nhi: break
        if not sim.step():
            break
