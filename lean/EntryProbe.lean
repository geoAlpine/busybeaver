import X2
open X2
set_option maxRecDepth 4000000
set_option maxHeartbeats 4000000
theorem p1 : (steps 100000 init).isSome = true := by rfl
