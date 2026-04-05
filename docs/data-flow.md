# PALE BLUE DOT — データフロー概要

ユーザー操作・ゲーム進行に伴うデータの生成・変換・保存・表示の流れを整理する。

---

## 起動時フロー

```
ブラウザがindex.htmlをロード
        │
        ▼
loadAllTextures()  [非同期・1テクスチャ/フレーム]
        │  texMercury() / texVenus() / ... / texMoon() 等11関数を実行
        ▼
TEXTURES{} に THREE.CanvasTexture を格納
        │
        ▼
buildScene()  [同期]
  ├─ scene / renderer / camera / lights を初期化
  ├─ buildPlanetMesh(pd) × 13天体
  │     → planetMeshes{} / orbitAngles{} に登録
  ├─ moonOrbitPivot を scene に追加
  ├─ openPhotoDB()
  │     → dbGetAllPhotos()
  │           → photos[] / collectionMap{} を復元
  ├─ buildDestMenu()  → DOM にボタン生成
  └─ animate() 開始（requestAnimationFrame ループ）
```

---

## メインループフロー（60 FPS）

```
animate()
  │
  ├─ [公転・自転更新]
  │    PLANETS.forEach:
  │      orbitAngles[id] += orbitSpeed * dt * simSpeed
  │      m.position = f(orbitAngles, orbitR)         ← 通常惑星
  │      m.position = earthPos + f(orbitAngles, 60.3) ← 月（R-57）
  │      m.rotation.y = Math.PI - a                  ← 月（潮汐固定）
  │      moonOrbitPivot.position.copy(earthMesh.position)
  │
  ├─ [カメラ更新]
  │    cockpitMode ON → camera.rotation.set(pitch, yaw, 0, 'YXZ')
  │    reentryShake > 0 → camera.position にランダム揺れ
  │
  ├─ [イベント検出]  checkSpecialEvents()
  │    カメラが heliopause.orbitR に近い → triggerHeliopause()
  │    カメラが alpha_centauri.orbitR に近い → triggerAlphaCentauri()
  │
  ├─ [UI 更新]
  │    updateNavInfo() → 目的地・距離・光速換算を DOM に反映
  │    updateCockpitHUD() → ALT / VEL / LOC / HDG を更新
  │
  ├─ [音声更新]  updateAudio()
  │    近傍惑星 → proxGain を上げ、freqMap から惑星固有音程を設定
  │    地表モード → noiseGain を上げ（風音）
  │    アルバム表示中 → droneGain を下げる
  │
  └─ renderer.render(scene, camera)
```

---

## ユーザー操作フロー

### カメラ操作

```
マウスドラッグ
  → spherical.theta / phi 更新
  → updateCamera()
  → camera.position = spherical座標からデカルト変換

マウスホイール / タッチピンチ
  → spherical.r 更新（ズーム）
  → updateCamera()
```

### 惑星クリック → 情報パネル表示

```
クリック(mx, my)
  → Raycaster.setFromCamera()
  → intersects = raycaster.intersectObjects(planetMeshes)
  → intersects[0].object.userData.planetId を取得
  → navigateTo(planetId) or showInfoPanel(planetId)
        │
        └─ PLANET_MAP[planetId] からデータ取得
           TEXTURES[planetId] からテクスチャ取得
           drawIconFrame() で128x128 Canvas アイコンをアニメーション
           facts[] を DOM に描画
```

### 目的地選択 → カメラ飛行

```
buildDestMenu() でボタン生成
  ↓
ボタンクリック → navigateTo(planetId)
  ├─ travelFrom = orbitTarget.clone()
  ├─ travelTo = planetMeshes[id].getWorldPosition() or 固定位置
  ├─ t=0 からイージングで orbitTarget.lerpVectors(from, to, e)
  └─ t=1 到達時 → showInfoPanel(planetId)
```

### 着陸シーケンス → 地表モード

```
🚀 ボタンクリック → startLanding(planetId)
  │
  ├─ Phase 1: zoom in（2秒）
  │    spherical.r → pd.r*3 にイージング
  │
  ├─ Phase 2: speed lines（1.2秒）
  │    slCtx.drawSpeedLines() でモーションブラー演出
  │
  ├─ Phase 3: flash + message
  │    flash div opacity 1→0
  │    showMsg('${nameJa}\n着陸しました', 2200)
  │
  └─ camState = 'surface' → enterSurfaceMode(pd)
        ├─ Three.js canvas を非表示
        ├─ surface-canvas / surface-ui を表示
        ├─ startSurfaceLoop(pd) → drawSurfaceView() RAF ループ
        └─ 土星の場合: drawStormOverlay() も毎フレーム呼び出し

地表ドラッグ（surface-ui でキャプチャ）
  → cockpitYaw / cockpitPitch 更新
  → drawSurfaceView(planetId, yaw, pitch) に反映（パララックス）
```

### 写真撮影フロー

```
P キー / 📸ボタン → takePhoto()
  │
  ├─ [1] renderer.domElement から PNG 取得
  │       canvas.toBlob() → Blob URL
  │
  ├─ [2] メタデータ生成
  │       location = camState / 近傍惑星名 等から決定
  │       dist = camera.position.length()
  │       au = dist / EARTH_ORBIT
  │
  ├─ [3] detectSlotId(location, au, nearestId, camState)
  │       → COLLECTION_SLOTS[] と照合
  │       → 条件一致すれば slotId を返す（例: 'earth', 'heliopause'）
  │
  ├─ [4] generateTitle(location, au, nearest, gamePhase)
  │       → 詩的な写真キャプションを生成
  │
  ├─ [5] photos[] に push
  │       collectionMap[slotId] = photo（スロット達成）
  │
  ├─ [6] dbSavePhoto(photoData)
  │       → IndexedDB: PaleBlueDotPhotos / photos ストアに保存
  │
  └─ [7] updateAlbum() / showMsg()
```

### アルバム操作フロー

```
A キー / 📁ボタン → openAlbum()
  → updateAlbum()
        ├─ COLLECTION_SLOTS[] × 12 → collectionGrid に描画
        │     埋まっているスロット: photos[].canvas をサムネ表示
        │     未撮影スロット: "No Photo" プレースホルダー
        └─ photos[] 全件 → photoLog に makePhotoCard() で描画
                ├─ canvas サムネイル
                ├─ タイトル / タイムスタンプ
                ├─ ダウンロードボタン
                │     → (ph.label||'photo').replace(特殊文字,'_') + '.png'（R-55）
                ├─ 名前変更ボタン → prompt() → dbRenamePhoto()（R-50）
                └─ 削除ボタン → confirm() → photos.splice() → dbDeletePhoto()（R-50）
```

### 帰還・エンディングフロー

```
🚀 宇宙へ戻るボタン → leaveSurfaceMode()
  → camState = 'returning'
  → startReturnJourney()
        │
        ├─ 帰還飛行アニメーション
        ├─ startReentry() → カメラシェイク（reentryShake）
        │
        └─ triggerEnding()
              ├─ ending 画面表示（z-index: 60）
              └─ photos[] からスライドショー表示
```

---

## 状態変数とデータの対応表

| 状態変数 | 型 | 更新タイミング | 参照元 |
|---------|-----|-------------|--------|
| `camState` | string | 各フェーズ移行時 | ほぼ全域 |
| `simSpeed` | number | スライダー操作 | animate / audio |
| `orbitAngles{}` | Object | 毎フレーム | animate |
| `focusedPlanetId` | string | クリック / navigateTo | showInfoPanel |
| `currentSurfacePlanet` | object | enterSurfaceMode | drawSurfaceView |
| `cockpitYaw / Pitch` | number | ドラッグ | drawSurfaceView |
| `photos[]` | Array | takePhoto / delete | updateAlbum / dbSave |
| `collectionMap{}` | Object | takePhoto | updateAlbum / collection表示 |
| `visitedPlanets[]` | Array | enterSurfaceMode | checkSpecialEvents |
| `saturnStormCalmed` | boolean | 嵐ボタンクリック | drawSurfaceLoop |
| `hpTriggered / acTriggered` | boolean | checkSpecialEvents | 一度だけ発火 |
| `audioMuted` | boolean | ミュートボタン | updateAudio |
