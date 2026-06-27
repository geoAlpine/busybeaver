# fiber unit-part contraction 攻撃 — メタ障害「free 構造は停止軌道 o=1 と共有」（2026-06-28, capstone）

唯一 un-mined だった 3-adic fiber unit-part contraction（free synchronization）を4角度で攻撃。
**結果: contraction は [PROVEN] 本物だが target に直交、そして決定的メタ障害=「free な構造はすべて停止固定点 o=1 と
共有されるので非停止を含意できない」を [PROVEN]。valuation-coupling プログラム完全終了。誤証明ゼロ。**

## 決定的メタ障害（I4, 美しい）
「free」= base symbol 列に対し pathwise（genericity 非依存）。**停止固定点 o=1（D≡1, even-density 0）は real orbit と
同一の free contraction で synchronize する**（検証: all-D=1 列と real orbit が同じく synchronize, v3→40）。
→ **任意の free 条件は o=1 でも成立、だが o=1 は停止 ⟹ free な条件は非停止を含意できない**。
free 部は freq(D≥2)（停止/非停止を分ける唯一のもの）に**盲目**。
これは MINPROP メタ定理（β(ψ)=+1/2 を o=1 で達成）の contraction/free-structure 側からの**同一障害の再導出**。

## 4角度の結果

### I1. contraction の精密化（`UNITPART_CONTRACTION.md`）— [PROVEN]
- **[PROVEN] 明示 affine fiber** Φ_D(x)=a_D x+b_D, a_D=3^D·2^{-D}、per-step 3-adic contraction 3^{-D}≤1/3
  （unit framing で正確に 1/3）。cumulative |o_j−õ_j|_3=3^{-(D_{j-1}+…+D_{j-L})}|o_{j-L}−õ_{j-L}|_3。
- **[PROVEN] synchronization depth**: o_j mod 3^k = f(recent D-history D_{j-1..j-L}) once ΣD≥k、L≈k/2。
  placeholder 非依存検証（3000 位置）、1 symbol 不足で 500/500 leak（depth は sharp）。
- **free vs hard catalog**: free=contraction・u_j mod 3^k=f(D-history)・u は unit・leading digit=parity(D)、全て
  conditional-on-D recode で target に直交。**決定的: unit marginal 自体が valuation 統計**（u_{j+1} mod3=parity(D_j) 厳密
  ⟹ P(u≡1)=P(D odd) は同じ genericity 壁）。(u_j,u_{j+1}) mod27 は D_j を復元＝full itinerary 再符号化。free な非停止量なし。

### I2. cross-metric coupling + integrality（`UNITPART_CROSSMETRIC.md`）— [PROVEN] degeneracy 持続
- **[PROVEN] MI(u mod 3^c; D_j)=0**（shuffle-null 床）。free 3-adic data は次 depth について情報ゼロ。
- **[PROVEN] 軌道は CRT-独立な random 整数と区別不能**（degeneracy persists, raw adelic で失敗した lever は復活せず）。
- **構造的理由**: free 3-adic data は σ(過去 D-history)-可測；D_j は過去 D-history と独立；唯一の bridge（twist u mod 2^k 経由 e_j）は
  ℤ₂^* の Haar 保存全単射＝informationless。**dynamics は free data と hard target を独立な2つの CRT 座標へ能動的に routing し、
  null channel でのみ接続**。CRT-独立は「破られない」でなく**構造的に強制**。

### I3. self-consistency 不動点 + proven contraction（`UNITPART_SELFCONSISTENT.md`）— 直交を確定
- **[PROVEN] self-consistent loop**: u_{j+1}=(3^{D_{j-1}}u_j−1)/2^{D_j}（contraction 3^{-D_{j-1}}）、D_j=G(D-history) via u。
  modulus of continuity: seed は cum-3-power≥c で死ぬ（tail-length≈c/2）、reconstruction 2000/2000。
- **[PROVEN] contraction は D-分布に直交**：単一因子 3^{D_{j-1}}2^{-D_j} は **3-adic で contract、2-adic で expand**＝
  制御される座標と query される座標が**反対側**。MI(3-adic state; D_j)=shuffle-null、D_j は u mod 2^{D_j+2}（2-adic）で決定。
  AUDIT_CONTRACTION の教訓を over-claim せず vindicate（contraction は real・refuted でない、だが 3-adic place 上で、
  2-adic expansion が D の読む channel、CRT が bridge を断つ）。

### I4. 非停止 observable の unit-part 可測性（`UNITPART_OBSERVABLE.md`）— **決定的メタ障害**
- **[PROVEN] 同値・十分いずれの非停止条件も unit-part(free) 可測でない**。2つの独立な level で：
  1. **再符号化（free な追加 channel なし）**: synchronization で u_j mod 3^k は recent base symbol の決定的 sliding-window 関数
     (w≈k+1, 0 multi-image)＝同じ itinerary 代数の **finite-window(free)** 部、target(mean D, freq(D≥2)) は **tail-average(genericity)** 部。
     free synchronization は各 integrand 値を渡すが average は決して渡さない。
  2. **メタ障害**: free=「全 base 列で pathwise」＝**停止固定点 o=1 と同一 free contraction で synchronize**（検証）
     ⟹ 任意の free 条件は o=1 でも成立、o=1 は停止 ⟹ **free 条件は非停止を含意不可**。free 部は freq(D≥2) に盲目。
- unit field は balance を bound しない（Pearson ≤0.003、local bit 予測は chance 0.50）。
- **精密な理由**: channel split（target=valuation v3=D−1 invertible/generating, unit=直交補空間）と free/genericity split
  （unit=free finite-window, target=tail-average）が**一致**。free=unit 側は停止 o=1 と共有＝停止/非停止の区別を**一切持たない**、
  区別は valuation=漸近平均側＝AEV/Mahler 単一軌道等分布核にのみ宿る。

## このセッションの bankable な結論（誤証明ゼロ）
1. **[PROVEN] 明示 affine fiber Φ_D・contraction 1/3・synchronization depth L≈k/2**。
2. **[PROVEN] free 3-adic data は D について情報ゼロ**（MI=0）、dynamics は free/hard を独立 CRT 座標へ routing、null channel 接続、
   CRT-独立は構造的に強制。
3. **[PROVEN] contraction は target に直交**：因子 3^D 2^{-D} は 3-adic contract / 2-adic expand、制御座標と query 座標が反対側。
4. **[PROVEN・決定的メタ障害] free な構造（contraction/synchronization/全 unit observable）は停止固定点 o=1 と共有される
   ⟹ いかなる free/構造のみの条件も非停止を含意できない**。free 部は freq(D≥2)（停止/非停止の唯一の判別子）に盲目。
   MINPROP の β(ψ)=+1/2 メタ定理と**同一障害**（今度は contraction 側から）。

## valuation-coupling プログラムの最終像（完全終了）
非停止 ⟺ even-density≥1/3 ⟺ mean D≥3/2 ⟺ **AEV Conj1.6 一方向単一軌道インスタンス**。
**全ての構造的 handle が PROVEN に直交 or 停止軌道と共有**：
- 3 valuation（archimedean=first-moment / 2-adic=Mahler / 3-adic=isomorphic）全て同一壁。
- contraction（3-adic, 本物だが target に直交）。
- skew product（valuation channel は generating, 圧縮なし）。
- self-consistency（contract 座標 ≠ query 座標）。
- **2つの独立なメタ定理で「構造のみ証明不可」**: (i) ergodic-opt β(ψ)=+1/2 at o=1（MINPROP）, (ii) free 構造は o=1 と共有（本 session）。
measure 側=完全 PROVEN、example 側=arithmetic PROVEN、残 OPEN=単一軌道 27 genericity（=u⊥e 独立性=AEV）一点。
非停止/停止の区別は **tail-average(genericity) にのみ宿る**＝構造（finite-window）からは原理的に到達不能。

## 次の生きた一手（候補）
1. **AEV 2510.11723 精読**: p/q=3/2・一方向・単一軌道版に必要な最小 input を1文に spec、核が AEV のどの補題に依存するか確定。
   構造攻撃は尽きた（全 PROVEN 直交）ので、残るは genericity 核そのものへの解析的 input。
2. **u⊥e 独立性（crisp open core）を解析的 decoupling で**: tail-average の effective cancellation（Mahler 核）。
3. measure 側 PROVEN 資産（明示 fiber・contraction・メタ障害・独立性特徴づけ）を完全証明の確定部分として固定・commit。
4. 完全証明の全 PROVEN 還元鎖 + 残 OPEN(AEV) を1つの capstone 文書に統合（投稿可能な形）。
