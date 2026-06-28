# 完全証明への道筋 — 全データ横断解析の結論（2026-06-28, 戦略）

15ラウンド/~56エージェントの全データ（数値・還元・barrier・文献）を横断解析（`DATA_REANALYSIS.md` fresh-eyes +
`LIMIT_THEOREM_AUDIT.md` gap audit）。**結論: 道筋は2つに分岐し、一方は閉じている（AEV/Mahler 待ち）、
もう一方は実質完成（consolidation のみ）。誤証明ゼロ。**

## 道筋の分岐（決定的）

### 道筋 (A) = 個別 cryptid の完全証明（Antihydra 非停止を無条件定理に）→ BLOCKED
**データが「近道なし」を証明**（`DATA_REANALYSIS.md`）:
- 構造のみ証明 = PROVEN 不可能（β>0 メタ定理・free 構造は o=1 共有）。
- **無条件 liminf even-density ≥ c > 0 は どの c でも到達不能**[PROVEN]: potential telescoping 恒等式 Σφ_new≈N が budget を固定するが、
  単一の長い D=1 run（φ_new=Ω(N)）が K を collapse させ得る。integrality は run を 1.17N でしか cap せず無用。
  壁は c=0 に座し、δ₁(o=1) に anchor、しかも **2-adic に（長い D=1 run で）接近**するので軌道の archimedean 増大は効かない。
- 全数値が noise floor（freq(D≥k)=Haar to 1e-4、conditional 独立 ~1σ、cross-prime corr≈0）。**未活用シグナルなし**。
- 唯一の live lead = quenched Weyl 和 Σe(h·4·(3/2)^n) の effective o(N) = **AEV/Mahler そのもの**（clean 再定式: D_j⊥D_{j-1} ⟺ m equidistributes、同じ壁）。
→ **(A) は名前付き研究 frontier 予想（AEV q=2 / Mahler 3/2）に終端。我々が自己完結的に閉じられない。**
  正直な stance: **Antihydra 非停止は AEV q=2 に CONDITIONAL**、還元自体が無条件貢献。

### 道筋 (B) = 構造的限界定理 + frontier カタログ（cryptid を解かない原貢献）→ 実質完成
**audit（`LIMIT_THEOREM_AUDIT.md`）: (B) は本質的に既に PROVEN**、残りは圧倒的に consolidation/writeup。4つの separable PROVEN unit：
1. **記述的 certification hierarchy**: 5本の予想非依存 strict 分離（star-free ⊊ REG ⊊ SLIN ⊊ 2-automatic ⊊ CF ⊊ CS）、
   各 explicit・sim 検証済 witness TM + Squeeze Lemma + 「REG は n=3 で十分」。**airtight・最も standalone**。
2. **subword-complexity floor**（cryptid parity 列）: eventually-periodic ⊊ Sturmian ⊊ p(ℓ)≥1.71ℓ。**PROVEN airtight**。
3. **厳密還元**（Antihydra density・o18/o15 existence・o10-inner、全 bb_sim 照合）: **全て PROVEN exact、analogy ゼロ**。
   o10-full は OUT（確率的停止）、o17 は kernel-less。
4. **density β>0 barrier**（Antihydra）: renewal 鎖・induced-map Bernoulli 定理・β(ψ)=+1/2 at o=1 **PROVEN**。

## (B) を airtight にする最小タスク（全て closable、研究 gap なし）
1. **[本セッションで CLOSE] ψ = D の関数を [PROVEN] に**: D=v₂(3o−1) の residue 同値（D=1⟺o≡1 mod4、D=2⟺o≡7 mod8、
   D≥3⟺o≡3 mod8、∵3⁻¹≡3 mod8）⟹ **ψ = +1/2 (D=1) / −1/2 (D=2) / −3/2 (D≥3) = min(D,3) の純関数**。初等的に [PROVEN]
   （旧 [verified] 数値を格上げ）。これで β=Σ_d ψ(d)·(atom 上の値) の ergodic-opt 評価が airtight。
2. **メタ claim を airtight core + LP で restate**: 「全軌道不等式は偽（o=1）ゆえ標的は orbit-specific」+ k=3..12 の機械検証 LP infeasibility
   を core とし、広い「no structure-only proof」は meta として label。
3. **all-k/REG barrier の IFF を one-direction + conjecture に降格**: brick-(d)（非有界 run ⟹ REG barrier）は PROVEN、逆は conjecture。
4. **scope を厳守**: β-barrier = **Antihydra のみ**、o18/o15 = existence barrier OPEN、o10-full OUT、o17 kernel-less。

## 防御可能な headline（(B) の最強 TRUE 主張）
> BB(6) の expanding-kernel Collatz cryptid 群 {Antihydra, o18, o15, o10-inner}（v_p(μ)=−1）は、**厳密・機械検証済の
> 還元**により AEV/Mahler 等分布予想の named fragment（q=2 density / q=3 existence）に帰着し、**density facet には
> proven ergodic-optimization barrier（Antihydra, β=+1/2、no structure-only proof）**を持ち、全体は**予想非依存の
> 5階層 certification-complexity hierarchy** に anchor される。（o17 と o10-full は除外。）

## (A) の無条件 fallback 定理（完全証明でなくとも standalone で記録価値）
1. **厳密還元定理**（raw 6-state TM → named 2-adic predicate）★最強 standalone
2. **induced-map Bernoulli/exactness 定理**（T_μ on ℤ_p は v_p(μ)=−1 で exact Haar 保存 Bernoulli）★最強 standalone
3. Haar-a.e. 非停止（annealed、SLLN/Borel-Cantelli I；o₀=27 は null 点で decide せず、と明記）
4. not eventually periodic（transience、予想非依存）
5. subword-complexity floor
6. β>0 no-structure-only メタ定理

## 戦略的結論（道筋）
**完全証明への道筋 = (B) を仕上げること**。個別 cryptid（A）は AEV/Mahler という名前付き open 予想に等価で、
データが「近道・部分結果・未活用シグナル全て無し」を証明済 ＝ 我々が無条件に閉じる道は無い。
**達成可能な「完全証明」は構造的限界定理 (B)**：4 PROVEN unit が揃い、残りは consolidation + 4 small fix（うち1つは本セッションで CLOSE）。
これは「cryptid を解く」のでなく「**BB6 Collatz core が何に等価で、なぜ構造的に解けないかを完全かつ厳密に特徴づける**」原貢献。
[[feedback_never_close_bb6]] と整合：(A) の攻撃面は AEV への解析的 input（effective equidistribution）として開き続ける一方、
**今 finalize できる完全な成果は (B)**。

## 次の具体手（(B) finalize の実行計画）
1. **fix #2–#4 を実行**（restate/scope、機械的）→ `UNIFIED_LIMIT_THEOREM.md` + `COMPLETE_PROOF_CAPSTONE.md` を audit 準拠に更新。
2. **(B) を1本の standalone 定理文書に consolidate**（hierarchy + floor + 還元群 + β barrier + カタログ + headline）。
   `docs/theory_certification_hierarchy.md` と統合、投稿可能形。
3. **(A) を「AEV q=2 conditional + 無条件 fallback 1,2」として明記**（誠実な現在地）。
4. 並行で (A) の唯一 live lead（effective quenched Weyl cancellation = AEV への解析 input）を攻撃面として維持。
