#!/usr/bin/env python
"""
Confirm the EXACT k-window floor m=8 for the o17 A01^k barrier, and the binding missing gram.
Binding gram at window m is the o=1 marker window of canon('0 A 0 1^k') = ('0','A','0','1'*(m-3)).
Present iff reachable has A-reads-0 with a 0 immediately left and >=(m-3) ones right.
"""
import sys
sys.path.insert(0, "/Users/aokiyousuke/quantum-ecc/busybeaver")
from far_dfa import FAR, reachable_configs, canon

O17 = "1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"
configs, halted = reachable_configs(O17, 300_000)
assert not halted
print(f"reachable configs: {len(configs)}")
for m in range(6, 13):
    far = FAR(O17, configs, m)
    g_o1 = ('0', 'A', '0') + ('1',) * (m - 3)      # o=1 marker window "0 A 0 1^(m-3)"
    g_o0 = ('A', '0') + ('1',) * (m - 2)           # o=0 marker window "A 0 1^(m-2)"
    halter_k = next(k for k in range(m, m + 20) if k % 3 in (1, 2))
    acc = far.accepts(canon(['A', '0'] + ['1'] * halter_k))
    print(f"  m={m:2d}: '0 A 0 1^{m-3}' in G = {g_o1 in far.G:5}   "
          f"'A 0 1^{m-2}' in G = {g_o0 in far.G:5}   "
          f"halter A01^{halter_k} accepted = {acc}")
print()
print("=> floor is the largest m with the o=1 gram '0 A 0 1^(m-3)' present.")
print("   (i.e. reachable A-reads-0-with-0-left has right-1-run capped; barrier stops above it.)")
