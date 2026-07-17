"""x2b5_shape.py -- dump B5's exact tape shape at chosen steps, to read off structure."""
import sys
from x2b5_sim import RULES, Tape

def dump(tape, pos, state):
    s = []
    for p in range(tape.lo, tape.hi + 1):
        c = '1' if tape.cells.get(p, 0) else '0'
        s.append(c)
    line = ''.join(s)
    hp = pos - tape.lo
    return line, hp

def run(max_steps, at):
    tape = Tape(); pos = 0; state = 'A'
    at = sorted(at); ai = 0
    for step in range(max_steps):
        if ai < len(at) and step == at[ai]:
            line, hp = dump(tape, pos, state)
            print(f"step={step} state={state} pos={pos} lo={tape.lo} hi={tape.hi} ones={tape.ones()} maxrun={tape.maxrun()}")
            print("  " + line)
            print("  " + " " * hp + "^")
            ai += 1
        sym = tape.read(pos)
        rule = RULES[state][sym]
        if rule is None:
            print("HALT at", step); return
        w, mv, nxt = rule
        tape.write(pos, w); pos += mv; state = nxt

if __name__ == '__main__':
    run(200000, [100, 500, 1000, 2000, 5000, 10000, 20000, 50000])
