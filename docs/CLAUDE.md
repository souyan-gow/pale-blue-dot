# PALE BLUE DOT — CLAUDE.md

## プロジェクト概要
カール・セーガンの「ペイル・ブルー・ドット」にインスパイアされたアンビエント探索ゲーム。
単一HTMLファイル（Three.js r128）で動作。インストール不要。

## ディレクトリ構成
```
pale_blue_dot_delivery/
├── docs/
│   ├── requirements.md               ← 全仕様
│   └── pale_blue_dot_gdd_v3.docx     ← ゲームデザインドキュメント
├── src/
│   ├── pale_blue_dot_prototype.html  ← メイン（ここを編集する）
│   └── solar_system_visualizer.html  ← 高品質テクスチャの参照元
└── concept_art/
```

## スケール定数（変更禁止）
```javascript
const SUN_R = 109.3;        // 太陽半径（地球=1）
const EARTH_ORBIT = 409.3;  // 地球軌道半径（scene units）= 1 AU
// 各惑星の軌道半径 = EARTH_ORBIT * realAU
```

## 惑星データ構造
```javascript
{
  id: 'earth',
  nameJa: '地球', nameEn: 'EARTH',
  color: 0x2a6fd4, colorHex: '#2a6fd4',
  r: 1.000,           // 半径（地球=1）
  orbitR: 409.3,      // 軌道半径（scene units）
  period: 10,         // 公転周期（ゲーム内時間）
  tilt: 23.4,         // 自転軸の傾き（度）
  ring: true,         // リングの有無（土星のみ）
  facts: [...],
  noTravel: true,     // trueなら「旅する」ボタン非表示
  isBoundary: true,   // ヘリオポーズ等
  isStar: true,       // 恒星
}
```

## カメラ制御
```javascript
// 通常時（軌道視点）
let spherical = {theta, phi, r};
let orbitTarget = new THREE.Vector3();
updateCamera();  // spherical → camera.position に変換

// 地表視点
cockpitMode = true;
cockpitYaw = 0;    // 左右
cockpitPitch = 0;  // 上下
// camera.rotation.set(cockpitPitch, cockpitYaw, 0, 'YXZ') をループ内で適用
```

## ゲーム状態
```javascript
let camState = 'orbit';
// 'orbit'     - 通常の太陽系ビュー
// 'landing'   - 着陸シーケンス中
// 'surface'   - 地表ビュー中
// 'returning' - 帰還旅行中
// 'reentry'   - 大気圏突入中
// 'ending'    - エンディング表示中
```

## 地表ビューシステム
- `<canvas id="surface-canvas">` と `<div id="surface-ui">` が着陸時に表示される
- コックピット（`#cockpit`）は廃止済み。`showSurfaceView(planetId)` / `hideSurfaceView()` で管理
- 各惑星の地表パラメータは `drawSurfaceView(planetId)` 内の `configs` で定義

```javascript
// 土星の嵐システム
let saturnStormCalmed = false;
startSaturnStorm()  // 嵐パーティクル開始（80個+稲妻）
// 「嵐を収める」ボタン → saturnStormCalmed=true → drawSurfaceView('saturn')再描画

// アルバム（9枠固定グリッド）
// 保存: canvas.toBlob() → URL.createObjectURL() → <a download>
// キャッシュ連動: localStorage 'pbd_session' フラグで起動時にDBをチェック
```

## ゲームデザインの原則
1. **失敗させない** — 燃料切れ・敵・ゲームオーバーは存在しない
2. **強制しない** — すべてプレイヤーが決める
3. **静寂を大切に** — 余白が感動を生む
4. **数字より体感** — 「8億km」より「光で44分」で表現する
5. **偶然の美を残す** — 計算された演出でない美しさを守る

## 実装状況
詳細は `docs/requirements.md` を参照。
現在はPhase 1（テクスチャ高解像度化・宇宙船表現など）に着手するフェーズ。

## 要件定義書修正時のワークフロー
要件定義書（`docs/requirements.md`）の修正依頼を受けたとき、必ず以下を実行すること：
1. `docs/requirements.md` を修正する
2. CLAUDE.md（このファイル）に反映すべき変更がないか確認し、あれば修正する
3. `docs/pale_blue_dot_gdd_v3.docx` に影響がないか確認し、あれば修正内容を報告する

## アーキテクチャドキュメント

以下の3ファイルはプロジェクトの構造を詳述している。作業開始前に必要なものを参照すること。

| ファイル | パス | 参照すべきタイミング |
|---------|------|-------------------|
| アーキテクチャ構造 | `docs/architecture.md` | ・新しいファイルを追加・削除するとき<br>・ライブラリ・CDN依存を変更するとき<br>・コードのどのセクションに手を入れるか見当をつけるとき |
| 依存関係マップ | `docs/dependency-map.md` | ・新しい機能・関数を追加するとき（どの層に属するか判断する）<br>・既存の関数を修正するとき（影響範囲を把握する）<br>・バグの原因が複数層にまたがると疑われるとき |
| データフロー概要 | `docs/data-flow.md` | ・ユーザー操作に関わるバグを調査するとき<br>・写真・IndexedDB・collectionMap に関わる処理を変更するとき<br>・camState のフェーズ遷移を変更・追加するとき |

## 参照スキル
- テクスチャ移植手順 → `.claude/skills/texture-migration.md`
- 演出実装メモ（演出・デプロイ・Q&A） → `.claude/skills/scene-effects.md`
