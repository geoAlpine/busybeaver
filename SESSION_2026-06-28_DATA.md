# capstone 文書 + annealed/quenched gap データ取得（2026-06-28, 続）

④完全証明 capstone 文書統合 と ①annealed/quenched gap の徹底データ取得を並列実行。
**結果: capstone 文書完成（7節）＋ gap を数値で精密定量化（annealed 2^{-N} vs quenched 1/√N = 「kind」の差）。
データは「ほぼ全部 non-halt を指す（+0.16 margin, 1000× safety）が、証明は単一軌道 typicality 定理=Mahler/AEV を要する」。誤証明ゼロ。**

## ④ capstone 文書（`COMPLETE_PROOF_CAPSTONE.md`, 7節）
完全証明の現在地を投稿可能な形で1本に統合。全 label を source から verbatim（upgrade なし）、load-bearing 数値を再検証。
6行 executive summary：
1. 非停止 ⟺ even-density≥1/3 ⟺ mean D≥3/2（induced 3/2-Syracuse o₀=27）= [PROVEN 機械検証]（GAP Lemma・renewal 恒等式・valuation 公式）。
2. measure 側 [PROVEN] 完備: induced map exact・Haar 保存・Bernoulli（D i.i.d. geometric mean 2>3/2）。
3. example 側 [PROVEN arithmetic]: 周期排除 C3・Countdown・Dual-Repulsion・v₃(o_{j+1})=D_j−1。
4. 構造のみ証明不可 = 2 独立メタ定理 [PROVEN]（β(ψ)=+1/2 at o=1 / free 構造は o=1 共有）。
5. 残 [OPEN] = AEV Conj 1.6（floor mirror）の一方向・level-2・単一軌道 fragment（Mahler 1968 を含意、より弱い named home なし）。
6. 解析的 handle 文献に存在せず、唯一の missing link = annealed→quenched Fourier-decay gap（AEV 自身も跨げない）。

## ① annealed/quenched gap データ（K1/K2/K3）

### K1. quenched Weyl 和（`QUENCHED_DATA.md`）— gap を「kind」で定量化
- **[OBSERVED] quenched Weyl 和 |S_N(h)| は N^{1/2}-generic**（b=0.39–0.51 全 h）、sup|S_N(h)|/√N は [1.7,2.1] に有界、super-√N 累積なし。
- discrepancy D*_N({4(3/2)^n}) ~ N^{-0.525}（Koksma generic）。
- **数値での gap（決定的）**: quenched |S_N|/N は **多項式 N^{-1/2}** で減衰（−log₁₀ が log 的に増大 0.94→2.63, N=10²→10⁵）、
  annealed Φ(N) は **指数 2^{-N}** で減衰（−log₂Φ/N→1.000 bit/step, N≈1010 で underflow）。**両者は kind が違う**
  （多項式 1/√N vs 指数 2^{-N}）= 非Pisot/Rajchman の annealed decay が quenched bound を含意できないことを hard number で確認。
- **[OBSERVED] random を超える cancellation なし**: quenched |S_N(1)|/√N は i.i.d. surrogate の 95% 帯（Rayleigh mean ≈0.886）に
  squarely 内在。統計的に random と区別不能 ＝ annealed/quenched gap が lone [OPEN] である所以。

### K2. ν_{2/3} の effective Fourier rate（`NU_RATE_DATA.md`）
- **[OBSERVED] 経験的に power decay, a ≈ log2/log(3/2) = 1.7095**。generic-ξ は power-like envelope だが pointwise erratic
  （decade slope −1.6〜+3.9, |ν̂| が 10⁶→10⁷ で増えることも）、uniform power law でない。
- **subsequence ξ_N=(3/2)^N/8（carry-product channel）では clean power law** a≈1.7095, R²=0.99998, slope 一定 ≈log2, drift なし、
  logarithmic は decisively reject。Link B 恒等式 |ν̂(ξ_N)|=0.7748·Φ(N) を4桁で確認。
- **[PROVEN-lit] citable な rate は logarithmic のみ**: Kershner(rational λ)・Varjú-Yu(≥log, subsequence で sharp)。
  **power-rate 定理は 2/3 に適用不可**（Dai-Feng-Wang は Garsia=代数的整数 要、3/2 は代数的整数ですらない；Streck/Solomyak は
  special-algebraic/a.e. で 2/3 に特殊化不可）。
- **正直な verdict**: 経験的に多項式(a≈1.71)・**証明可能には logarithmic のみ**。clean な power law それ自体が「{(3/2)^k} 等分布」
  ＝ Mahler/AEV [OPEN]。NONPISOT Link C と AEV reading を覆さず再確認。

### K3. annealed→quenched 転送データ（`ANNEALED_QUENCHED_DATA.md`）— 「ほぼ全部転送済」
- annealed Φ は super-exponential collapse（1.1e-90 at N=300, float-0 by N≈3000）= [PROVEN] 非Pisot⇒Rajchman⇒annealed balance。
  **quenched 軌道はその vanishing mean に乗らず**、1/√N scale で 1/2 周りに揺れる（|E_q−½|·2√N = O(1), 0.06–1.5, N=5×10⁶ で 0.85）
  ＝ CLT-typical single draw の signature。
- **[OBSERVED] 相関減衰（転送の鍵）**: 自己生成重みに検出可能な相関なし。parity autocorr は i.i.d. noise floor（lag 1024 まで |ac|/noise≤1.6）、
  gap D mean 1.9992≈2.0, autocorr≈0。**weights は経験的に ≈i.i.d.**。target を破るに必要な lag-1 相関 |ρ*|≈0.74 vs 実測 |ρ|≈0.0006
  ＝ **~1000× safety factor**。
- **[OBSERVED] 1/3 threshold への worst dip**: 累積 even-density worst dip 0.4934, **margin +0.16 over 1/3**, 長くしても深まらず。
  counter min は halt 境界(−1)に決して近づかず（+2,497,141 at N=5×10⁶）。
- **assessment（正直）**: "almost there", visible block なし。転送可能な統計は全て転送済（even-density は annealed 1/2 を O(1/√N) で追う、
  区別特徴の weight 相関は ≈0, gap 則は annealed 一致, 一方向 target は +0.16 margin で成立）。残る gap は既知壁
  （annealed mean Φ は quenched single realization を bound せず、finite-N typicality は o(1) arithmetic correlation を排除できない）。
  missing = 単一軌道 typicality 定理そのもの（effective {(3/2)^n} 等分布 = Mahler/AEV core）、annealed ν_{2/3} 制御は構造的に供給不可。

## このセッションの bankable な結論（誤証明ゼロ）
1. **capstone 文書完成**（`COMPLETE_PROOF_CAPSTONE.md`, 7節, 投稿可能, label verbatim）。
2. **[OBSERVED] gap を「kind」で定量化**: annealed 指数 2^{-N} vs quenched 多項式 1/√N。quenched は random と統計的に区別不能、
   cancellation beyond random なし。
3. **[OBSERVED/PROVEN-lit] ν_{2/3} rate**: 経験的 power a≈log2/log(3/2)≈1.71（subsequence で clean）だが証明可能には logarithmic のみ、
   power-rate 定理は 2/3 に適用不可。clean power law それ自体が Mahler。
4. **[OBSERVED] 転送はほぼ完了**: weights ≈i.i.d.（autocorr≈0, 1000× safety）、even-density ≥1/3 を +0.16 margin で N=5×10⁶ まで維持、
   counter は halt 境界に近づかず。残るのは単一軌道 typicality 定理（Mahler/AEV）のみ＝既知壁、新 obstruction なし。

## 完全証明の最終状態（今日の到達点）
**「1つの brand-new 名前付き予想（AEV Conj 1.6, floor mirror）の最弱 fragment を除いて全 PROVEN」**。
- 全 PROVEN 還元鎖 + measure 側 + example 側 + 2 メタ定理 = `COMPLETE_PROOF_CAPSTONE.md` に統合（投稿可能）。
- 残 [OPEN] = annealed/quenched gap = 単一軌道 typicality（Mahler/AEV）、データは non-halt を圧倒的 margin で支持するが
  証明には typicality 定理が不可欠（annealed 制御では構造的に届かない、新 obstruction はない）。

## 次の生きた一手（候補）
1. **single-orbit typicality 定理への解析的 input を絞る**（唯一の真 frontier）: quenched Weyl 和 Σe(h·4·(3/2)^n) の N^{1/2} を
   N^{1-ε} に改善する effective cancellation（van der Corput/Vinogradov の (3/2)^n 版、lacunary 障害は既知）。
2. **AEV 著者に floor-mirror 一方向 single-orbit fragment を connect**（記録・協働）。
3. **capstone 文書を投稿形式に磨く**（arXiv/notes、BB6 frontier の現在地として）。
4. BB6 本体に戻り、他の cryptid / open core の構造を本 capstone の枠組みで再点検。
