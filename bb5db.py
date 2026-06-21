"""Read the bbchallenge 5-state seed DB (30-byte header + 30 bytes/machine) -> standard format."""
import os
DB = os.path.join(os.path.dirname(__file__), "_bbdata", "all_5_states_undecided_machines_with_global_header")
SC = "ABCDE"
def machine(buf, i):
    off = 30 + i * 30
    rec = buf[off:off + 30]
    toks = []
    for t in range(10):                       # A0,A1,B0,B1,...,E0,E1
        w, m, g = rec[3*t], rec[3*t+1], rec[3*t+2]
        if g == 0:                            # undefined -> halt
            toks.append("---")
        else:
            toks.append(f"{w}{'R' if m==0 else 'L'}{SC[g-1]}")
    return "_".join(toks[2*s] + toks[2*s+1] for s in range(5))
def load():
    with open(DB, "rb") as f:
        return f.read()
