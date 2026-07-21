#!/usr/bin/env python3
"""Is the g=3 rung-11 +80 genuine dynamics or a detector shift?
Inspect configs at the exitSteps-predicted landing (5018116) and observed (5018196).
Also compare to g=4 rung-11 landing (predicted==observed 13466968)."""
import x2t7_lib
x2t7_lib.SPAN = 1 << 18
x2t7_lib.ORIGIN = x2t7_lib.SPAN
from x2t7_lib import run, rle_right, ones_run_left

def show(label, step):
    _, st, pos, tape, _ = run(step)
    rle = rle_right(tape, pos, limit=40000)
    print(f"{label} step={step} state={st} head={tape[pos]} left_ones={ones_run_left(tape,pos)}")
    print("   rle head:", rle[:8])

# g=3 rung 11: regenIn @4482050, exitSteps(11)=536066 -> predicted 5018116; observed cascadeReg @5018196
print("### g=3 rung 11 ###")
show("regenIn11(g3)      ", 4482050)
show("predicted+exit     ", 4482050 + 536066)   # 5018116
show("observed cascadeReg", 5018196)
# g=4 rung 11: regenIn @12930902, predicted==observed 13466968
print("\n### g=4 rung 11 ###")
show("regenIn11(g4)      ", 12930902)
show("predicted+exit     ", 12930902 + 536066)   # 13466968
