# 4ルート同時監査 — 収縮「迂回」の検証と標的の精密化（2026-06-28）

「全パターンを試す」→ 収縮ルートの4つの next-move を独立エージェントで並列に攻めた。
4本が **同じ結論** に収束。誤証明ゼロ（過剰主張1件を請求前に捕捉・撤回）。

## 1. 検証した主張
自己無撞着写像 `S: ν → L_ν ν` は収縮（定数 ≈ λ₂(L)+‖F‖ ≈ 0.048 < 1）で不動点一意 = Haar、
これが変分原理の障害（正エントロピー ⇒ 非UE）を **迂回** する（self-consistency ⊋ invariance）。

## 2. 結論：sidestep は UNSOUND（`AUDIT_CONTRACTION.md`）
- **[REFUTED]** 「Haar だけが self-consistent」は偽。`mckean_contraction.py` の sidestep は
  間違った作用素 `L_Haar` で δ₁ を測定。正しく `L_{δ₁}δ₁` で測ると **δ₀, δ₁ も self-consistent**
  （= T の整数不動点 {0,1}）。変分多重性は **再生産** され、迂回されない。
- **[REFUTED]** 収縮定数 `λ₂+‖F‖` は無効な評価。スペクトル半径は劣加法的でない。`L|_V` は
  極端に非正規（ρ=0 冪零だが ‖L|_V‖=1）。擬スペクトル試験で真の `ρ(L+F)≈0.4–0.55`、
  分解能 k とともに 1 へ増大。

## 3. 3本が同一の open core に収束
- **追従ブリッジ（`TRACKING_BRIDGE.md`）**: 収縮は測度レベル、軌道は Haar-null 点 → 収縮だけでは
  単一軌道収束を与えない。数値では軌道は Haar を追うが **ergodic ~N^{−0.4}（≈1/√N）率**で、
  収縮率 0.04 は軌道の収束に一切現れない。ブリッジは既知 open core（Mahler/AEV）に **還元**。
- **コサイクル（`COCYCLE_ERGODICITY.md`）**: Furstenberg/Anzai/Conze-Krygin/Schmidt は等長・
  零エントロピー専用 → 拡大・正エントロピーファイバーに **不適用**。非コバウンダリ（commit 794b450）が
  買うのは off-target な ℤ-シリンダーのエルゴード性のみ、単一軌道 c₀=8 の Birkhoff 収束は与えない。
  a.e.-vs-specific gap = Tao 2019 gap。**この avenue は撤退推奨**。

→ 残る open kernel は **還元不能** = 単一軌道の有効等分布（Mahler 3/2 / AEV normality）。
   収縮枠組みはそれを mean-field 言語に移し替えただけ。

## 4. 監査が生んだ資産（攻撃面は広がった）
- **[PROVEN・citable]** 非Pisot 3/2 ⇒ ν_{2/3} Rajchman ⇒ **annealed carry balance**。
  レート = **対数**（Varjú–Yu; commit 984f70f の多項式 slope −1.6 は定理でなく数値観察と訂正）。
  **新しい厳密恒等式**（数値確認）: `|ν̂_{2/3}((3/2)^N/8)| = Φ(N)·tail`、Φ = exp_sum の annealed
  carry 積、定数比 0.7748（N=5..80）。`NONPISOT_FOURIER_CHAIN.md`。
- **真の解析対象を特定**: quenched ‖F‖ を支配するのは
  `d log Φ/dp |_{1/2} = Σ_j 2i·tan(π{(3/2)^j/4})` = **(3/2)^j tan-和 = Korobov/Mahler 量**。
  → **annealed[PROVEN] / quenched[OPEN]=Mahler** の二層分離が clean に。
- **構造**: self-consistent 不動点 {δ₀, δ₁, Haar} ↔ T の整数不動点 {0,1} + SRB。

## 5. 次の生きた一手（攻撃面を狭めない）
1. **quenched (3/2)^j tan-和の cancellation を直接攻める** — いま精密に同定された解析対象。
   Theorem E / Korobov 和の有効 cancellation（PROOF_STATUS §3.6, ROUTE_RENEWAL_CLT §7 と整合）。
2. **annealed→quenched ギャップ**を renewal 構造（軌道の再生）× PROVEN annealed バランスで詰める。
   独立性が壊れる箇所＝相関の有効減衰＝core そのもの、だが部分 quenched 限界が取れるか。
3. **新恒等式 Φ(N)·tail をブリッジに**: annealed Fourier 減衰（厳密・対数）から quenched 量への
   橋を、定数比 0.7748 の構造（なぜ定数か）から建てられるか。
4. **annealed 結果を partial result として banking** — citable な厳密成果（非Pisot⇒バランス）。

## 6. 健全性メモ
収縮ルートは「迂回」としては死んだが、**標的を quenched (3/2)^j tan-和に鋭く絞り**、**citable な
annealed 厳密結果**＋**新恒等式**を残した。INCIDENT の教訓（本物の敵で gate、null だけで安心するな）を
自分の枠組みに向け、請求前に過剰主張を撤回 = 偽証明ゼロ維持。`mckean_contraction.py` 冒頭に撤回記録。
