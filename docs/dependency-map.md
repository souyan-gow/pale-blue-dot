# PALE BLUE DOT — コード依存関係マップ

`src/pale_blue_dot_prototype.html` 内の JavaScript は、以下の**8層構造**で依存関係が成立している。
上位層ほど多くの下位層に依存し、下位層は上位層を知らない。

---

## 層構造図

```
┌─────────────────────────────────────────────────────────────┐
│  [8] メインループ層  animate()                               │
│       ↑ 全層に依存                                          │
├─────────────────────────────────────────────────────────────┤
│  [7] UI 層                                                  │
│       showInfoPanel / buildDestMenu / updateAlbum           │
│       takePhoto / updateNavInfo / updateCockpitHUD          │
│       ↑ データ層・永続化層・Three.js シーン層に依存          │
├──────────────────────────────┬──────────────────────────────┤
│  [6a] Three.js シーン層      │  [6b] 地表ビュー層（2D）     │
│       scene / renderer /     │       drawSurfaceView()      │
│       camera / planetMeshes  │       drawStormOverlay()     │
│       buildPlanetMesh()      │       startSurfaceLoop()     │
│       moonOrbitPivot         │       専用ノイズヘルパー      │
│       ↑ テクスチャ生成層 +   │       ↑ ユーティリティ層のみ │
│         Three.js に依存      │         に依存（Three.js 不使用）
├──────────────────────────────┴──────────────────────────────┤
│  [5] 音声層                                                 │
│       initAudio() / playSfx() / updateAudio()               │
│       ↑ Web Audio API に依存（ユーザー操作で初期化、R-45）  │
├─────────────────────────────────────────────────────────────┤
│  [4] 永続化層                                               │
│       openPhotoDB / dbSavePhoto / dbGetAllPhotos            │
│       dbUpdateSlot / dbDeletePhoto / dbRenamePhoto          │
│       ↑ IndexedDB + localStorage に依存                     │
├─────────────────────────────────────────────────────────────┤
│  [3] テクスチャ生成層                                       │
│       texMercury/Venus/Earth/Moon/Mars/Jupiter              │
│       texSaturn/Uranus/Neptune/Sun/Starfield (11 関数)      │
│       TEXTURES{} キャッシュ                                 │
│       ↑ ユーティリティ層に依存                              │
├─────────────────────────────────────────────────────────────┤
│  [2] ユーティリティ層                                       │
│       smoothNoise / fbm / warpFbm                           │
│       lerp / clamp / mix3 / mkCanvas                        │
│       ↑ 純粋関数、依存なし                                  │
├─────────────────────────────────────────────────────────────┤
│  [1] データ・定数層                                         │
│       PLANETS[] / PLANET_MAP{} / COLLECTION_SLOTS[]         │
│       SUN_R / EARTH_ORBIT / AU_KM                           │
│       ↑ 依存なし（定数・データのみ）                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 各層の詳細

### [1] データ・定数層

| 識別子 | 型 | 役割 |
|-------|----|------|
| `PLANETS[]` | Array | 13天体の定義（id / 半径 / 軌道半径 / 公転周期 / 傾き / facts） |
| `PLANET_MAP{}` | Object | `id → 天体データ` のルックアップテーブル |
| `COLLECTION_SLOTS[]` | Array | 12実績スロットの定義（撮影条件・ラベル） |
| `SUN_R` | Number | 太陽半径（109.3 = 地球半径=1 基準） |
| `EARTH_ORBIT` | Number | 地球軌道半径（409.3 scene units = 1 AU） |
| `AU_KM` | Number | 1 AU = 149,597,870.7 km |

### [2] ユーティリティ層

| 関数 | 用途 |
|------|------|
| `smoothNoise(x,y,seed)` | 格子ベースの滑らかなノイズ値（0〜1） |
| `fbm(x,y,octs,seed)` | フラクタルブラウン運動（多重ノイズ合成） |
| `warpFbm(x,y,octs,seed)` | ドメインワーピング付き fbm（複雑な地形用） |
| `lerp(a,b,t)` | 線形補間 |
| `clamp(v,lo,hi)` | 値域クランプ |
| `mix3(a,b,t)` | 3要素配列の線形補間 |
| `mkCanvas(w,h)` | オフスクリーン Canvas 生成 |

### [3] テクスチャ生成層

各関数は `THREE.CanvasTexture` を返す。呼び出しは `loadAllTextures()` が非同期で順次実行。

| 関数 | テクスチャキー | 特記事項 |
|------|--------------|---------|
| `texMercury()` | `'mercury'` | クレーター・高地・低地のマクロ/メソ/マイクロ構造 |
| `texVenus()` | `'venus'` | 酸性雲・硫黄色の大気 |
| `texEarth()` | `'earth'` | 大陸・海洋・極冠・山岳 |
| `texEarthCloud()` | `'earthcloud'` | 半透明雲レイヤー（Earth メッシュの子に追加） |
| `texMoon()` | `'moon'` | ハイランド/マーレ分布＋クレーター群（R-57追加） |
| `texMars()` | `'mars'` | 赤鉄鉱・オリンポス山・渓谷 |
| `texJupiter()` | `'jupiter'` | バンド・大赤斑 |
| `texSaturn()` | `'saturn'` | バンド・極嵐 |
| `texSaturnRing()` | `'saturn_ring'` | リング断面プロファイル（幅 512×4px） |
| `texUranus()` | `'uranus'` | 薄青・均一なヘイズ |
| `texNeptune()` | `'neptune'` | 深青・大暗斑・スクーター |
| `texSun()` | `'sun'` | 粒状対流・黒点・フレア |
| `texStarfield()` | `'stars'` | 6,000 星 + 輝星スパイク + 星雲光 |

### [4] 永続化層

```
IndexedDB: PaleBlueDotPhotos
  └─ photos ストア
       ├─ key: auto-increment
       ├─ index: timestamp (unique)
       └─ フィールド: {canvas, label, location, dist, slotId, timestamp}

localStorage:
  └─ pbd_session: "1"  ← 起動済みフラグ（Ctrl+Shift+R でクリア）
```

| 関数 | 操作 |
|------|------|
| `openPhotoDB()` | DB 接続（バージョン 1） |
| `dbSavePhoto(data)` | 写真追加 |
| `dbGetAllPhotos()` | 全写真取得（起動時ロード） |
| `dbUpdateSlot(id, updates)` | スロット情報更新 |
| `dbDeletePhoto(timestamp)` | 写真削除（R-50） |
| `dbRenamePhoto(timestamp, newLabel)` | 写真名称変更（R-50） |

### [5] 音声層

- **初期化タイミング**: 最初のミュートボタンクリック時（R-45、ゲーム起動時は無音）
- **AudioContext 構成**:

```
AudioContext
├─ droneA/B/C (Oscillator) → droneFilter → droneGain → master
├─ proxOsc (Oscillator)   → proxFilter → proxGain → master
└─ noiseSrc (Buffer)      → noiseFilter → noiseGain → master
                                                         ↓
                                                  audioCtx.destination
```

### [6a] Three.js シーン層

| 識別子 | 型 | 役割 |
|-------|----|------|
| `scene` | THREE.Scene | 全3Dオブジェクトのルート |
| `renderer` | THREE.WebGLRenderer | `<canvas id="c">` への描画 |
| `camera` | THREE.PerspectiveCamera | 視点（FOV 65°） |
| `planetMeshes{}` | Object | `id → THREE.Mesh` |
| `orbitAngles{}` | Object | `id → 公転角度（ラジアン）` |
| `moonOrbitPivot` | THREE.Object3D | 月軌道リングの位置追従ピボット |
| `buildPlanetMesh(pd)` | Function | メッシュ・リング・大気・雲の生成 |

**月の特殊処理（R-57）**:
- `isMoon: true` の天体は `planetMeshes[parentId].position` を基準に公転位置計算
- `rotation.y = Math.PI - a` で潮汐固定（常に同じ面を地球へ向ける）

### [6b] 地表ビュー層（2D Canvas）

Three.js を使わない独立した描画エンジン。`<canvas id="surface-canvas">` に描画。

| 関数 | 役割 |
|------|------|
| `drawSurfaceView(planetId, yaw, pitch)` | 全惑星・月の地表を 6 レイヤーパララックスで描画 |
| `drawStormOverlay(ctx, W, H)` | 土星専用：嵐パーティクルをオーバーレイ |
| `startSurfaceLoop(pd)` | RAF ループ開始（土星は嵐も同時起動） |
| `stopSurfaceLoop()` | RAF 停止 |
| `surfHash(n)` / `fbm1d(x,seed)` | 地表専用の決定論的ノイズ（フレーム間でちらつかない） |
| `cellRng(cellIdx, seed)` | セル単位の LCG 乱数（岩・クレーターの位置を固定） |
| `pxCtx(ctx, off, fn)` | コンテキストをパララックスオフセット分だけ translate して描画 |

### [7] UI 層

| 関数 | 依存先 |
|------|--------|
| `showInfoPanel(planetId)` | PLANET_MAP / TEXTURES / drawIconFrame() |
| `buildDestMenu()` | PLANETS[] |
| `navigateTo(planetId)` | planetMeshes / orbitTarget |
| `startLanding(planetId)` | planetMeshes / camState / playSfx |
| `takePhoto()` | renderer / detectSlotId / dbSavePhoto / updateAlbum |
| `updateAlbum()` / `makePhotoCard()` | photos[] / collectionMap / dbDeletePhoto / dbRenamePhoto |
| `updateNavInfo()` | planetMeshes / camState / 単位変換関数群 |
| `updateCockpitHUD()` | camera / simSpeed / planetMeshes |

### [8] メインループ層

```javascript
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.05);
  const s  = simSpeed;

  // [6a] 公転・自転更新（月は地球基準）
  PLANETS.forEach((pd, i) => { ... });
  // 月軌道リングが地球を追随
  moonOrbitPivot.position.copy(planetMeshes['earth'].position);

  // [カメラ] cockpitMode 時のカメラ姿勢適用
  // [FX] reentryShake カメラ揺れ

  // [7] 毎フレーム UI 更新
  checkSpecialEvents();
  updateNavInfo();
  updateCockpitHUD();
  updateAudio();       // [5] 音声

  renderer.render(scene, camera);  // [6a] 描画
}
```

---

## camState ごとの処理分岐

| camState | 主な処理 | 次の状態 |
|---------|---------|---------|
| `'orbit'` | 惑星公転・カメラ操作・クリック判定 | `'landing'` |
| `'landing'` | zoom→speedlines→flash アニメ | `'surface'` |
| `'surface'` | 地表ビュー描画（6b） | `'returning'` |
| `'returning'` | 宇宙への帰還飛行 | `'reentry'` |
| `'reentry'` | カメラシェイク・大気圏突入 | `'ending'` |
| `'ending'` | エンディングスライドショー | （終了） |
