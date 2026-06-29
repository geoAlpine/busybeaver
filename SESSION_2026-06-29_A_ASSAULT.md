# (A) = (K) = Mahler 3/2 への総攻撃（4 新角度）（2026-06-29）

(B) 完成後、(A) に全力。これまで閉じた経路を避け、genuinely 新しい・非循環な4角度を同時投入。
**結果: breakthrough なし（予想どおり Mahler）。だが核を最鋭形 H₂ に圧縮 + 2つの新 [PROVEN] 構造的 negative
（resonance-strip / separation）+ 生き残る唯一の avenue を pinpoint。誤証明ゼロ。**

## A1【最重要】核の最鋭形 H₂（`WEAKEST_SUFFICIENT.md`）
- (K) は **単一 mod-2 character・一方向・full factor-2 slack** の形に圧縮：
  > **H₂: `liminf_N (1/N) Σ_{n<N} (−1)^{c_n} ≥ −1/3`**（Antihydra c-orbit, c₀=8）
  ∵ avg(−1)^{c_n}=2·even-density−1、even-density≥1/3 ⟺ avg≥−1/3。**核がこれ以上圧縮できない最小形**。
- **≥1/3 slack は full Mahler より厳密に弱い sufficient condition を買う**[PROVEN]: Vaaler 量子化で target 1/3 ⟺ 円周 **J=5 周波数**のみ
  （target→1/2=Haar ⟺ J→∞=full equidistribution）。strict-weakening 鎖: full AEV-q2(全 2^k, two-sided, exact) ⟹ level-2 ⟹ one-sided ⟹ +1/3 slack = (K)。
- 候補仮説の含意解析: (a) 正の下界密度 c>0 of {o≡3 mod4} は (K) を含意**せず**（深 cylinder が nested、c≥1/2 要）/(b) freq(1 mod4)≤2/3 も不足（4/3<3/2）/(c) pair-correlation は **strong すぎ**(u.d. を含意)/(d) 単一周波数 cancellation は 2-adic dual で YES(band-limited cylinder)、円周で J=5/(e) discrepancy o(N)=full u.d.。
- **verdict: 論理的には ≥1/3 slack が strictly weaker sufficient(1 character, factor-2 room)= 核の最 clean statement。だが proof 難度は壁を越えず**
  ——全 weakest 形が同じ kind（quenched 単一軌道 geometric (3/2)-phase character cancellation）、annealed mean=0(Wall II)・a.e.=√N(Wall I)、
  単一の one-sided single-orbit character cancellation すら無条件 tool 到達せず。**weaker target, same wall, no crack（だが statement は最鋭化）**。

## A2 binary digits of 3^n（`DIGITS_OF_3N.md`）— 対角に one-sided 断片なし
- a_n=bit_n(8·3^n)=bit_{n−3}(3^n)＝3^n のビット格子の**主対角**（位置が n と動く）。全 unconditional handle は wrong place に着地。
- 最新: Ren-Roettger 2025(2511.03861) base-3 digit u.d. は **CONJECTURE**/Pegg「半分が 1」は **CONJECTURE**(finiteness のみ PROVEN)/Senge-Straus-Stewart-Bugeaud-Kaneko nonzero count→∞ rate log n/log log n=**sublinear**/**新 2501.00850: run-length L(3^K)=o(K) PROVEN(8·3^n に適用)だが horizontal run で diagonal density でない**。
- **新 [PROVEN 構造]: Rowland column-periodicity(period 2^{k−2})は対角を provably miss**（対角は column k を row k で sample、k≪2^{k−2}(k≥5)で各 column 1回・period 未満→density 転送ゼロ）。
- (K)＝対角 marginal＝Mahler/AEV Conj1.6、digit-community 問題(Ren/AEV normality)はその strict superset、**対角に attackable one-sided 断片なし**。

## A3 resonance-free strip（`RESONANCE_STRIP.md`）— affine⇒NLI 失敗（新 PROVEN 理由）
- 正しい対象: β=3/2 β-変換の transfer operator（holomorphic/Mayer-Ruelle, nuclear）。twisted `L_ξ f=(2/3)Σ_b e(ξφ_b)f∘φ_b` の高周波 leading-eigenvalue modulus = |ν̂_{2/3}(ξ)|(Link B)。
- **[PROVEN 新] Naud の resonance-free-strip 機構は適用不可、NLI が同一的に失敗**: ×(3/2) は **affine constant slope** → roof τ=log(3/2) 定数 → temporal distance Δ≡0 → non-local-integrability `∂φ/∂u≠0` 失敗（数値確認: affine [0,0,0] / nonlinear 摂動 [2.15,1.14,2.52]）。Bandtlow-Just-Slipantschuk: linear map の analytic-transfer spectrum は厳密 {0,1}、nontrivial Ruelle 共鳴は **nonlinearity(Blaschke 曲率)現象**＝affine map に欠如。
- 非soficity は red herring（operator は affine 分枝で定義可、難所は affine 幾何）。非Pisot は contracting→expanding に transfer(同一 operator の inverse 分枝)だが **annealed tier のみ**(contracting-vs-expanding gap = annealed-vs-quenched gap)。
- **verdict: Mahler in disguise**(新 well-posed strip 問題なし、affine⇒NLI 失敗が sharp な理由)。flagged 2 pivot(open): (i) frequency を scramble せず non-constant roof を作る analytic conjugacy(risky) (ii) a.e.→specific **selector** を独立攻撃。

## A4 Diophantine separation→density（`DIOPHANTINE_DENSITY.md`）— separation は density を制御不能（新 PROVEN）
- μ(log3)≤5.1163(Wu), μ(log2)≤3.8914。log₂3 の有効 irrationality measure 有限。LMN interpolation determinant が powers of 2,3 の sharp separation。**genuine archimedean anti-clustering 事実**。
- **[PROVEN 新] separation-based counting(cancellation でなく)は one-sided density を与えない**: covering bound `#{x_n∈[0,½)}≤(½)/δ_N+1` は spacing のみ使い vacuous でない（δ_N≈1/N で target 到達）。だが軌道点は **分母 2^{n−2} の dyadic 有理数**(gap ~2^{−n})、真の min-gap は **Poisson-scale N^{−2} ≪ 1/N**。covering bound ≈N²/2、N 倍 off。
- 決定的: 軌道は **separation budget 内で自由に clustering**（N=1600 で [0,½) に ≈N/2≈824 点、budget は ≈8.8×10⁵ 許容）＝density は clustering が決め、spacing は見えない。large-sieve/Turán も同じ δ⁻¹≲N で死ぬ。
- **verdict: separation-cannot-control-density、新 failure mode(cancellation 壁と別)。separation 経路 CLOSED(定量理由付)、cancellation 経路は依然 OPEN**。

## このセッションの bankable な結論（誤証明ゼロ・decision なし）
1. **[最鋭化] 核 = H₂: liminf(1/N)Σ(−1)^{c_n} ≥ −1/3**（単一 mod-2 character・一方向・factor-2 slack = 円周 J=5 周波数）。核がこれ以上圧縮不能な最小形。≥1/3 slack は full Mahler より strictly weaker な sufficient だが同 kind の quenched cancellation で壁を越えず。
2. **[PROVEN 新 negative ×2]**: resonance-strip（affine⇒NLI 失敗、Ruelle 共鳴は曲率現象で affine に欠如）/ separation（軌道が budget 内で自由 clustering、min-gap N^{−2}≪avg 1/N）。両経路を定量理由付で CLOSE。
3. **[文献]** digits-of-3^n は (K)=対角 marginal=Mahler、Rowland regularity は対角を miss、one-sided 断片なし。
4. **生き残る唯一の avenue = quenched 単一軌道 Weyl 和 cancellation**（Erdős-Turán の hard 側）。+ A3 の 2 pivot(non-constant-roof conjugacy / a.e.→specific selector 独立攻撃)が flagged-open。

## (A) の現在地（assault 後）
- 核は **H₂（最鋭・単一 character・一方向・factor-2 slack）**。全周辺 PROVEN、これ1点が Mahler 3/2。
- **閉じた経路（定量理由付）**: 構造のみ(β>0)・無条件 c>0・vdC・MR・Bernoulli/有限 twisted-RPF・decoupling-mean・sum-product-measure・L²-flattening・**resonance-strip(affine⇒NLI)**・**separation(clustering)**・nilsequences・×2×3-rigidity。
- **OPEN な attack surface（維持）**: ①quenched Weyl 和の有効 cancellation（cancellation 経路、唯一未閉）②a.e.→specific selector の独立攻撃（A3 pivot ii）③frequency 保存の non-constant-roof analytic conjugacy（A3 pivot i, risky）。
- 距離: 依然 Mahler 3/2（research frontier）。だが核の statement は最鋭、closed routes は network 化、surviving avenue は2-3本に pinpoint。

## 次の生きた一手（候補・[[feedback_never_close_bb6]]）
1. **a.e.→specific selector を独立に攻める**（A3 pivot ii）: cancellation を諦めず、「計算可能点 c₀=8 を a.e. 集合に入れる」機構（effective Tao / 計算可能点の equidistribution の最新）を Weyl 和と切り離して。これは2つ目の壁を単独で叩く未踏角度。
2. **H₂(単一 character one-sided)に特化した新 cancellation 道具**: full equidistribution でなく1 character の一方向だけを狙う Korobov/Vinogradov 変種。
3. **non-constant-roof analytic conjugacy**（A3 pivot i）: ×(3/2) を曲率付き共役で Naud 適用可能化（frequency scramble の risk を精密評価）。
4. annealed tier の effective log rate を partial result として固める（既 PROVEN, banking）。
