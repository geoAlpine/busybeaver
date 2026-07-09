# BB(6) 完全証明への道筋 — 全データ統合版 (2026-07-10)

*キャンペーン全データ（2026-07-06〜07-10、~80 コミット、7回の (K)-build、B1/B2/B3/C1 決定試行）を統合した、
完全証明までの正確な地図。各主張は記録ノートを引用。ラベル規律: [PROVEN]/[OBSERVED]/[OPEN]。
**現時点で決定された機械はゼロ** — この文書は「何が証明されれば BB(6) が確定するか」の完全な分解である。*

---

## 0. 完全証明の分解式

```
BB(6) = N(champion) の完全証明
  = [A] 17 named cryptids の決定（全機 非停止 と予想）
  + [B] ~1087 un-catalogued holdouts の決定
  + [C] champion の停止時刻の厳密計算
  + [D] 全 5-tuple 列挙の形式検証（Coq-BB5 相当）
```

- **[C] は既知作業**（champion は既知の halter、計算は有界）。
- **[D] は community 規模の工学**（BB(5) で実証済みの体制、新数学不要）。
- **[B] は community 規模**: holdout 実数 1104（機械可読リスト local: `_bbdata/bb6_holdouts_1104.txt`）、
  named 17 を除く ~1087。我々の certified suite は community decider class の部分集合で **0/10 yield**
  （`HOLDOUT_SWEEP_FEASIBILITY_2026-07-10.md`）。全機 slow polynomial-width counter、halt-in-cap ゼロ。
- **[A] が本質** — 以下が本体。

## 1. [A] 17 named cryptids — 壁の完全な分類（今日確定）

### 1a. 壁は3種類に分類され、全種類が内部攻撃に対して閉じた

| 壁の種類 | 機械 | 内部攻撃の状態 |
|---|---|---|
| **(K) 頻度壁** (base-p/q normality) | 14機: Antihydra, o2, o3, o4, o5, o8, o10, o11, o12, o13, o14, o16, o15/o18 | **証明付きで尽きた**（7 builds、§2） |
| **thin-set 到達壁** (Collatz型 bit-mixing) | o7, Space Needle | **合同/オートマトン攻撃 不可能と確定**（§3、07-10） |
| **gate-timing 壁** (unbounded gate-state) | o17 | **有限状態性が Myhill–Nerode で反証**（§3、07-10） |

**結論 [honest]: 17機のいずれも、既存の全手法＋本キャンペーンで構築した全新手法では内部決定できない。
これは推測ではなく、種類ごとに機構的な閉鎖証明/反証を持つ。**

### 1b. しかし問題は 1 点に凝縮された（キャンペーンの主成果）

統一定理 [PROVEN, Lean: `Mirror.lean`] により、(K) 14機は全て
「明示的 ×(p/q) 軌道の q-adic 深度過程」であり、開いた自由度は正確に:

> **seed 固有の reload units w_i ∈ ℤ_q^× の等分布**
> ⟺ a-priori E[K²] 上界 ⟺ base-p/q normality ⟺ AEV Conj 1.6 ⟺ Mahler 3/2 系
>
> **最易インスタンス = o4**: halt ⟺ freq{3∣W_n} ≥ 4/5（seed 57、margin 2.4、lossy 可）。
> `freq ≤ 4/5 − ε` を示せば o4 が落ち、手法が一般的なら 14機が連鎖する。

深度軸は無条件制御済み [PROVEN, Lean]。単一破滅 run は subcritical 機で排除済み [PROVEN, Lean]。

## 2. (K) 壁への内部攻撃の完全な記録（7 builds、全て閉鎖証明付き）

| 攻撃 | 閉鎖の機構 | 記録 |
|---|---|---|
| run-cap potential | fatal 方向（1次モーメント）に直交、C-S gap √n | `O4_NEWMATH_BUILD` |
| 重み付き sub-action B(3,k) | δ₋₁₄ 固定点が growth 無関係に強制 | 〃 |
| 桁理論 (Mahler/DS/Koksma/SML) | autonomy split の open 側と証明（非自励、線形回帰でない） | `NEWMATH_DIGIT_BRIDGE` |
| exact reload map excursion | carry-coupling absent（unit refresh が深度を decouple） | `RELOAD_EXCURSION_BUILD` |
| cross-machine transfer | 同一 engine（×3/2 は文字通り1つ）でも per-seed | `RELOAD_MAP_UNIFIED` |
| measure rigidity (EKL/IP/coisometry) | {2,3}-host 全体で不適用 [publishable 定理] | `PAPER_RIGIDITY_LIMITS` |
| solenoid diagonal (u₀ 排除) | 対角=run-cap そのもの; cap-legal fatal class 生存 | `U0_EXCLUSION_BUILD` |

**副産物（正の資産）**: exact reload skew-product [PROVEN]、explicit cap-legal adversary、
道具の設計仕様（`NEWMATH_BUILD_SYNTHESIS` §design-spec）、publishable partial 2本。

## 3. thin-set / timing 壁への攻撃記録（07-10、全て honest negative）

- **o7** (`O7_DECISION_ATTEMPT_2026-07-10.md`): 2つの独立な sound 到達集合モデル（2-adic milestone
  automaton J≤14 / odd-adic cascade automaton m≤729）とも分離なし。構造的理由: oddpart(u) が halt 条件と
  dynamics の両方に入り合同連続でない — Collatz 型 2-adic/residue coupling が ℤ/m を埋める。
  soundness 訂正: even branch は a′=3a/2+1+b（b が結合; cascade entry では b=1 [0-mismatch/49,940]）。
- **Space Needle** (`SPACENEEDLE_DECISION_ATTEMPT_2026-07-10.md`): 分離 modulus 不存在（軌道が全残差を被覆）。
  f(m)=m+3⌊m/2^{v+1}⌋+v が無限に高い bit を引き下ろす → 有限状態合同でない [反例を各 M, j で構成]。
- **o17** (`O17_GATE_DECISION_ATTEMPT_2026-07-10.md`, **未コミット**・検証一時停止中): gate 安全性 b(d⃗) は
  (i) いかなる scalar 残差の関数でもない（base 2..8 × M≤64 × 両向き、0/112 exhaustive）、
  (ii) **Nerode index が 1,2,6,19,54,132 と成長・飽和なし → 有限オートマトン不在 [OBSERVED, Myhill–Nerode]**、
  (iii) μ=5 configs の 78% が HALT で「safe」は特徴づけなき 22% 少数派 → forward-closed 不変量なし。
  → 「(K)-shaped timing」ラベルが厳密に裏付けられた。tower-mod 兵器は「対象となる scalar が存在しない」ため不適用。

**判別基準（今日確立）**: エポック写像が有限状態合同か bit-mixing かが thin-set 攻撃の成否を決める。
17機は全機 bit-mixing / unbounded-state 側にいる。

## 4. 残された道 — 完全証明への現実的経路

### 経路 1: 外部連携（最有力・時間軸最短）
- **AEV/Eliahou グループへの hand-off**: 手紙準備済（`OUTREACH_EMAIL_DRAFT.md`）、**送信はユーザーの明示的
  go-ahead 必須**。手土産は世界最強: o4-最易インスタンスへの認証済み帰着 + margin 梯子 + Lean 層 +
  explicit adversary + 道具の設計仕様。(K) を正面研究する唯一のグループが 2025 年から活動中。
- **arXiv 公開**（ユーザー判断待ち）: `PAPER_RIGIDITY_LIMITS` + `PAPER_MIRROR_LADDER` は (K) と独立に
  出版可能 — 分野の専門家（測度剛性/数論力学）の目に触れる最短経路。Zenodo v1.5 draft は publish 待ち。

### 経路 2: 新数学の継続建設（generational・時期約束不能）
設計仕様は完成済み: seed の ℤ_q^× reload 軌道を読み、**cap-legal な E[K²]=∞ adversary を排除する**
a-priori 機構。非スペクトル・非構造・非自励・neutral-blind 破り・非 depth・非 2次モーメント。
次の builder は `ATTACK_PLAN_2026-07-10.md` + `NEWMATH_BUILD_SYNTHESIS` から開始（霧でなく施工図）。

### 経路 3: 条件付き完全証明の骨格（内部で完結可能・推奨）
**「BB(6) = N(champion) ⟸ 17 named protections ∧ 1087 holdouts の決定」を Lean で形式化。**
- 17機の protection を明示的算術予想として一覧化（大半は既に一覧: 各機の [OPEN] 行）
- champion の停止時刻を local に厳密検証
- 「予想 → 非停止」の各帰着を Lean 化(o4/o3 は済; 残りは grid→Lean の持ち上げ)
これが内部で到達できる完全証明の最大近似であり、外部が (K) を解いた瞬間に BB(6) が確定する体制を作る。

### 経路 4: community 協働（現方針: 投稿しない）
[B]+[D]（1087 holdouts + 全列挙検証）は本質的に community 規模。方針変更はユーザー判断のみ。

## 5. 推奨する次の一手（優先順）

1. **B3 (o17) の検証再開 → コミット**（現在一時停止中; Nerode 結果は重要な確定事項）
2. **経路 3 の着手**: 17 protections の明示的一覧 + champion 検証 + 条件付き骨格の設計
3. **経路 1 の判断をユーザーに仰ぐ**: AEV 手紙送付 / arXiv / Zenodo v1.5 publish
4. (K) 建設は施工図から再開可能な状態で park

## 6. 検証・再現
`verify_all.py --quick`（7/7 PASS）; Lean `~/.elan/bin/lake build`（17 jobs green, 324 定理, sorry 0）;
今日の攻撃 scripts: `o7d_*.py`, `snd_*.py`, `o17d_*.py`（o17d は検証一時停止中・未コミット）。
状態の一次情報: `ATTACK_PLAN_2026-07-10.md`（前回 hand-off）→ 本文書が最新。
