#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate PALE BLUE DOT test specification as a .docx file. v1.1"""

import zipfile, os

# ─── XML helpers ──────────────────────────────────────────────────────────────
def escape(t):
    return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def para(text, style="Normal", bold=False, size=None, color=None,
         spacing_before=0, spacing_after=0, align="left"):
    rpr = ("","")[0]
    if bold:   rpr += "<w:b/>"
    if size:   rpr += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    if color:  rpr += f'<w:color w:val="{color}"/>'
    ppr = f'<w:pStyle w:val="{style}"/>'
    if align != "left": ppr += f'<w:jc w:val="{align}"/>'
    if spacing_before or spacing_after:
        ppr += f'<w:spacing w:before="{spacing_before}" w:after="{spacing_after}"/>'
    rpr_blk = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
    return (f'<w:p><w:pPr>{ppr}</w:pPr>'
            f'<w:r>{rpr_blk}<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>')

def heading(text, level=1):
    s = {1:"Heading1", 2:"Heading2", 3:"Heading3"}.get(level,"Heading1")
    return f'<w:p><w:pPr><w:pStyle w:val="{s}"/></w:pPr><w:r><w:t>{escape(text)}</w:t></w:r></w:p>'

def page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

def cell(text, width, bold=False, shade=None, align="left", font_size=18):
    rpr = "<w:b/>" if bold else ""
    rpr += f'<w:sz w:val="{font_size}"/><w:szCs w:val="{font_size}"/>'
    if shade and shade.upper() != "2E75B6":
        rpr += '<w:color w:val="000000"/>'
    elif shade and shade.upper() == "2E75B6":
        rpr += '<w:color w:val="FFFFFF"/>'
    shade_xml = f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>' if shade else ""
    align_xml = f'<w:jc w:val="{align}"/>' if align != "left" else ""
    border = ('<w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
              '<w:left w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
              '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
              '<w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>')
    return (f'<w:tc><w:tcPr>'
            f'<w:tcW w:w="{width}" w:type="dxa"/>'
            f'<w:tcBorders>{border}</w:tcBorders>'
            f'{shade_xml}'
            f'<w:tcMar><w:top w:w="80" w:type="dxa"/><w:left w:w="120" w:type="dxa"/>'
            f'<w:bottom w:w="80" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tcMar>'
            f'</w:tcPr>'
            f'<w:p><w:pPr>{align_xml}</w:pPr>'
            f'<w:r><w:rPr>{rpr}</w:rPr>'
            f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p></w:tc>')

def tbl_row(cells_data, is_header=False):
    cells_xml = ""
    for args in cells_data:
        text, width = args[0], args[1]
        shade = "2E75B6" if is_header else args[2] if len(args)>2 else None
        align = args[3] if len(args)>3 else "left"
        cells_xml += cell(text, width, bold=is_header, shade=shade, align=align)
    trpr = "<w:trPr><w:tblHeader/></w:trPr>" if is_header else "<w:trPr/>"
    return f"<w:tr>{trpr}{cells_xml}</w:tr>"

def simple_table(rows, col_widths, header=True):
    total = sum(col_widths)
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in col_widths)
    tbl = (f'<w:tbl>'
           f'<w:tblPr><w:tblW w:w="{total}" w:type="dxa"/></w:tblPr>'
           f'<w:tblGrid>{grid}</w:tblGrid>')
    for i, row in enumerate(rows):
        is_hdr = (i == 0 and header)
        cells = [(row[j], col_widths[j]) for j in range(len(row))]
        tbl += tbl_row(cells, is_header=is_hdr)
    tbl += "</w:tbl>"
    return tbl

def info_table(rows):
    total = 9360
    tbl = (f'<w:tbl><w:tblPr><w:tblW w:w="{total}" w:type="dxa"/></w:tblPr>'
           f'<w:tblGrid><w:gridCol w:w="2400"/><w:gridCol w:w="6960"/></w:tblGrid>')
    for label, value in rows:
        tbl += (f'<w:tr><w:trPr/>'
                f'{cell(label, 2400, bold=True, shade="F2F2F2")}'
                f'{cell(value, 6960)}'
                f'</w:tr>')
    tbl += "</w:tbl>"
    return tbl

# ─── Test cases ────────────────────────────────────────────────────────────────
# (no, category, item, operation, expected, env)
# env: "pc" | "mob" | "both"
TEST_CASES = [
    (1,  "ローディング", "プログレスバー表示",        "ページにアクセスする",                              "黒背景にプログレスバーと「初期化中...」メッセージが表示される",           "both"),
    (2,  "ローディング", "テクスチャ生成メッセージ",   "ローディング中に待機する",                          "「太陽を生成中...」等のメッセージが順番に切り替わる",                    "both"),
    (3,  "ローディング", "キーボードヒント表示",        "ローディング画面を確認する",                        "「P:撮影 N:目的地 A:アルバム M:ミュート ESC:閉じる」が表示される",        "pc"),
    (4,  "ローディング", "ロード完了・非表示",          "ロード完了後を確認する",                            "ローディング画面がフェードアウトし、3D宇宙が表示される",                  "both"),
    (5,  "3D描画",      "太陽系全体表示",              "ロード完了直後を確認する",                          "太陽・惑星・軌道ラインが表示され、惑星が公転している",                    "both"),
    (6,  "3D描画",      "軌道ドラッグ（PC）",          "マウスドラッグで画面を動かす",                      "カメラが回転し、視点が変わる",                                           "pc"),
    (7,  "3D描画",      "ズーム（PC）",                "マウスホイールを操作する",                          "カメラが前後に滑らかに移動する",                                         "pc"),
    (8,  "3D描画",      "星空背景",                    "カメラを任意の方向に向ける",                        "星空（スターフィールド）が全周に表示されている",                          "both"),
    (9,  "3D描画",      "土星リング",                  "土星に近づいてズームする",                          "リング・パーティクル・カッシーニの隙間が確認できる",                      "both"),
    (10, "3D描画",      "時間加速スライダー",           "スライダーを右に動かす",                            "惑星の公転速度が加速する。左に戻すと減速・停止する",                      "both"),
    (11, "タッチ操作",  "1本指ドラッグ",               "1本指でスワイプする",                               "カメラが回転し、視点が変わる",                                           "mob"),
    (12, "タッチ操作",  "ピンチズームイン",             "2本指を広げるピンチ操作をする",                     "カメラが近づく（ズームイン）",                                           "mob"),
    (13, "タッチ操作",  "ピンチズームアウト",           "2本指を縮めるピンチ操作をする",                     "カメラが遠ざかる（ズームアウト）",                                       "mob"),
    (14, "タッチ操作",  "タップで惑星選択",             "惑星を1本指でタップする",                           "惑星の情報パネルが表示される",                                           "mob"),
    (15, "タッチ操作",  "iOS ラバーバンド防止",         "画面端でスワイプする",                              "ブラウザの「戻る」動作が発生しない",                                     "mob"),
    (16, "惑星情報",    "クリックで情報パネル表示",     "惑星をクリック（またはタップ）する",                "右側に惑星名・事実・「この惑星を旅する」ボタンが表示される",              "both"),
    (17, "惑星情報",    "✕ボタンで閉じる",             "情報パネル右上の✕をクリックする",                   "パネルが閉じる",                                                         "both"),
    (18, "惑星情報",    "太陽は旅できない",             "太陽をクリックして情報パネルを確認する",            "「この惑星を旅する」ボタンが表示されない",                                "both"),
    (19, "着陸",        "ワープエフェクト",             "「この惑星を旅する」をクリックする",                "スピードライン→フラッシュ→着陸メッセージが表示される",                    "both"),
    (20, "着陸",        "ワープ音",                    "着陸ボタンを押した直後（音声ON時）",                "ワープ音（上昇するサウンド）が再生される",                                "both"),
    (21, "着陸",        "コックピットHUD表示",          "着陸完了後の画面を確認する",                        "コックピットフレーム・ALT/VEL/LOC/HDGが画面に表示される",                "both"),
    (22, "着陸",        "地表ドラッグ",                "地表モードでドラッグする",                          "コックピット視点が動く（全周見渡せる）",                                  "both"),
    (23, "着陸",        "「宇宙へ戻る」ボタン",         "地表で「宇宙へ戻る」をクリックする",                "コックピットが消え、軌道上に戻る",                                       "both"),
    (24, "撮影",        "📷ボタンで撮影",               "📷撮影ボタンをクリックする",                        "フラッシュ・シャッター音・撮影完了メッセージが表示される",                "both"),
    (25, "撮影",        "Pキーで撮影",                 "Pキーを押す",                                       "撮影と同じ動作が発生する",                                               "pc"),
    (26, "撮影",        "写真カウント増加",             "撮影後に写真カウントを確認する",                    "「📸 N枚」の数字が増える",                                               "both"),
    (27, "アルバム",    "アルバムを開く",               "🖼アルバムボタンをクリックする",                    "コレクション12スロット＋フォトログが表示される",                          "both"),
    (28, "アルバム",    "Aキーでアルバム開閉",          "Aキーを押す",                                       "アルバムが開閉する",                                                     "pc"),
    (29, "アルバム",    "フォトログに写真が並ぶ",       "撮影後にアルバムを開く",                            "撮影した写真が「PHOTO LOG」欄にサムネイルで表示される",                   "both"),
    (30, "コレクション","旅立ちの日スロット獲得",       "最初の撮影を行う",                                  "旅立ちの日スロットが金色枠になり、チャイム音が鳴る",                      "both"),
    (31, "コレクション","惑星付近スロット獲得",         "各惑星付近で撮影する",                              "対応スロットが獲得済みになる",                                           "both"),
    (32, "コレクション","進捗カウント更新",             "スロット獲得後にアルバムを開く",                    "「N / 12」の数字が増える",                                               "both"),
    (33, "ナビ",        "目的地メニュー表示",           "目的地ボタンをクリックする",                        "全11天体のリストが左側に表示される（プロキシマbまで）",                   "both"),
    (34, "ナビ",        "Nキーでメニュー開閉",          "Nキーを押す",                                       "目的地メニューが開閉する",                                               "pc"),
    (35, "ナビ",        "HUD 近傍距離表示",             "任意の惑星に近づく",                                "「近傍: ○○ (N AU)」のように近傍天体と距離が表示される",                  "both"),
    (36, "ナビ",        "単位切替 AU→km",              "AUボタンを1回クリックする",                         "表示が「十億km」形式に変わる",                                           "both"),
    (37, "ナビ",        "単位切替 km→光年",             "kmボタンをもう1回クリックする",                     "表示が「光年」形式に変わる（近距離時はAUにフォールバック）",              "both"),
    (38, "ナビ",        "Uキーで単位切替",              "Uキーを押す",                                       "単位が切り替わる",                                                       "pc"),
    (39, "サウンド",    "初回クリックで音声開始",        "ページ表示後、最初にクリックする",                  "宇宙アンビエントドローンが聞こえ始める",                                  "both"),
    (40, "サウンド",    "ミュートボタン",               "🔊ボタンをクリックする",                            "音声がOFFになり、🔇アイコンに変わる",                                    "both"),
    (41, "サウンド",    "ミュート解除",                 "🔇ボタンを再クリックする",                          "音声が再開し、🔊アイコンに戻る",                                         "both"),
    (42, "サウンド",    "Mキーでミュート切替",           "Mキーを押す",                                       "ミュートが切り替わる",                                                   "pc"),
    (43, "サウンド",    "惑星共鳴音",                   "任意の惑星に非常に近づく",                          "惑星固有の共鳴音（音程）が微かに聞こえる",                               "both"),
    (44, "キーボード",  "ESCで全パネル閉じる",          "パネルを開いてESCを押す",                           "開いているパネルがすべて閉じる",                                         "pc"),
    (45, "星系",        "ヘリオポーズ通過メッセージ",   "太陽から遠く離れる（120AU付近）",                   "「ヘリオポーズを越えた」メッセージが表示される",                          "both"),
    (46, "星系",        "α星系3つの恒星表示",           "ケンタウルス座α付近まで移動する",                   "黄白（A）・橙（B）・赤（プロキシマ）3つの恒星が見える",                   "both"),
    (47, "星系",        "到達時の選択肢表示",            "α星系に接近する",                                   "「地球へ帰還する」「先へ進む」の選択肢が表示される",                      "both"),
    (48, "星系",        "プロキシマbへ着陸",            "目的地でプロキシマbを選択し旅する",                 "異星の地表にコックピットで着陸できる",                                    "both"),
    (49, "帰還",        "帰還シーケンス開始",            "「地球へ帰還する」を選択する",                      "帰還メッセージと惑星モンタージュが表示される",                            "both"),
    (50, "帰還",        "訪問惑星モンタージュ",          "帰還中の画面を確認する",                            "着陸した惑星を逆順に通過するメッセージが表示される",                      "both"),
    (51, "大気圏突入",  "突入メッセージ・速度表示",     "帰還後の大気圏突入開始を確認する",                  "「高度400km 速度7.8km/s」等のメッセージが表示される",                    "both"),
    (52, "大気圏突入",  "プラズマ火炎エフェクト",        "突入シーケンス中の画面を確認する",                  "画面周囲にオレンジ色の炎エフェクトが表示される",                          "both"),
    (53, "大気圏突入",  "カメラシェイク",               "プラズマ加熱フェーズを確認する",                    "カメラが小刻みに揺れる",                                                 "both"),
    (54, "大気圏突入",  "高度計表示",                   "突入中の画面下を確認する",                          "「ALT Nkm | VEL N.Nkm/s | NNNN°C」が画面下に表示される",               "both"),
    (55, "エンディング","エンディング画面表示",          "突入完了後を確認する",                              "カール・セーガンの引用文と旅の写真が表示される",                          "both"),
    (56, "エンディング","リスタートボタン",              "「もう一度旅をする」をクリックする",                "ページがリロードされ最初から始まる",                                      "both"),
    (57, "永続化",      "写真がリロード後も残る",        "撮影後にページをリロードする",                      "アルバムの写真カウントと写真が保持されている",                            "both"),
    (58, "永続化",      "コレクションがリロード後も残る","コレクション獲得後にリロードする",                   "獲得済みスロットが金色枠のまま保持される",                               "both"),
    (59, "モバイル",    "ボタンサイズ",                 "スマートフォンでHUDを確認する",                     "ボタンが指でタップしやすいサイズで表示される",                            "mob"),
    (60, "モバイル",    "レイアウト崩れなし",            "スマートフォンで全体レイアウトを確認する",           "テキストや要素がはみ出したり重なったりしない",                            "mob"),
    (61, "モバイル",    "アルバム3カラム表示",           "スマートフォンでアルバムを開く",                    "コレクショングリッドが3カラムで表示される",                               "mob"),
]

def make_test_table(rows):
    # Columns: No(380) Cat(900) Item(1700) Op(1800) Expected(1900) Env(560) PC結果(560) SP結果(560)
    # Total = 380+900+1700+1800+1900+560+560+560 = 8360 → use 9360 total
    # Adjust: No(400) Cat(1000) Item(1780) Op(1780) Expected(2000) Env(600) PC(600) SP(600) = 8760
    # Final: No(400) Cat(1000) Item(1820) Op(1820) Expected(2100) Env(500) PC(560) SP(560) = 8760
    # Use 9360: No(440) Cat(1100) Item(1900) Op(1900) Expected(2080) Env(540) PC(600) SP(600) - wait let me just make it fit
    # 440+1100+1900+1900+2080+540+600+600 = 9160... close enough, use 9360
    # Let me just pick: 440+1100+1920+1920+2100+540+620+620 = 9260 hmm
    # Simple: 7 cols fitting into 9360:
    # No:480, Cat:1000, Item:1800, Op:1800, Exp:2200, Env:480, PC:600, SP:600 = 8960... close
    # No:480, Cat:1000, Item:1800, Op:1800, Exp:2200, Env:480, PC:800, SP:800 = 9360 ✓
    cols = [
        ("No.",    480),
        ("カテゴリ", 1000),
        ("テスト項目", 1800),
        ("操作手順",  1800),
        ("期待結果",  2200),
        ("環境",     480),
        ("PC結果",   800),
        ("SP結果",   800),
    ]
    total = sum(w for _, w in cols)
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for _, w in cols)
    tbl = (f'<w:tbl>'
           f'<w:tblPr><w:tblW w:w="{total}" w:type="dxa"/></w:tblPr>'
           f'<w:tblGrid>{grid}</w:tblGrid>')

    # Header row
    hdr_cells = ""
    for label, w in cols:
        hdr_cells += cell(label, w, bold=True, shade="2E75B6", align="center", font_size=16)
    tbl += f"<w:tr><w:trPr><w:tblHeader/></w:trPr>{hdr_cells}</w:tr>"

    for no, cat, item, op, exp, env in rows:
        pc_val  = "" if env in ("pc",  "both") else "ー"
        sp_val  = "" if env in ("mob", "both") else "ー"
        row_cells = [
            (str(no), 480,  None, "center"),
            (cat,     1000, None, "left"),
            (item,    1800, None, "left"),
            (op,      1800, None, "left"),
            (exp,     2200, None, "left"),
            (env.upper() if env=="pc" else ("SP" if env=="mob" else "両方"), 480, None, "center"),
            (pc_val,  800,  None, "center"),
            (sp_val,  800,  None, "center"),
        ]
        row_xml = ""
        for text, w, shade, align in row_cells:
            row_xml += cell(text, w, shade=shade, align=align, font_size=16)
        tbl += f"<w:tr><w:trPr/>{row_xml}</w:tr>"

    tbl += "</w:tbl>"
    return tbl

# ─── Build document ────────────────────────────────────────────────────────────
def build_document():
    body = []

    # ── Title ──
    body.append(para("PALE BLUE DOT", bold=True, size=40, color="1F4E79", align="center", spacing_after=120))
    body.append(para("テスト仕様書", bold=True, size=28, color="2E75B6", align="center", spacing_after=240))

    # ── 0. 修正履歴 ──
    body.append(heading("0. 修正履歴", 1))
    rev_rows = [
        ["バージョン", "日付",         "修正者",      "修正内容"],
        ["1.0",        "2026/03/28",   "souyan-gow",  "初版作成"],
        ["1.1",        "2026/03/28",   "souyan-gow",  "修正履歴表を追加。PC/SP別の結果列を追加。凡例から□を削除。"],
    ]
    body.append(simple_table(rev_rows, [900, 1200, 1500, 5760]))
    body.append(para("", spacing_before=120, spacing_after=0))

    # ── 1. テスト概要 ──
    body.append(heading("1. テスト概要", 1))
    body.append(info_table([
        ("テスト対象URL", "https://souyan-gow.github.io/pale-blue-dot/"),
        ("作成日",        "2026年3月28日"),
        ("最終更新",      "2026年3月28日（v1.1）"),
        ("テストケース数", f"{len(TEST_CASES)}件"),
        ("対象ブラウザ",  "Chrome / Firefox / Edge / Safari"),
        ("対象端末",      "PC（デスクトップ/ノート）/ スマートフォン（iOS・Android）"),
        ("テスト実施者",  "（記入）"),
        ("テスト実施日",  "（記入）"),
    ]))
    body.append(para("", spacing_before=120, spacing_after=0))

    # ── 2. テスト環境 ──
    body.append(heading("2. テスト環境", 1))
    body.append(heading("2.1 PC（ブラウザ）", 2))
    body.append(info_table([
        ("必須",   "Google Chrome（最新版）"),
        ("推奨追加", "Firefox / Microsoft Edge / Safari（Mac）"),
        ("確認事項", "WebGL・Web Audio API・IndexedDB が有効であること"),
    ]))
    body.append(para("", spacing_before=80, spacing_after=0))
    body.append(heading("2.2 スマートフォン", 2))
    body.append(info_table([
        ("iOS",    "Safari（iPhone / iPad）"),
        ("Android", "Google Chrome"),
        ("確認事項", "WebGLサポート端末であること。音声はタップ後に有効化される"),
    ]))
    body.append(para("", spacing_before=120, spacing_after=0))

    # ── 3. 凡例（□を削除） ──
    body.append(heading("3. 凡例", 1))
    body.append(info_table([
        ("環境列 PC",  "PCブラウザのみで確認"),
        ("環境列 SP",  "スマートフォンのみで確認"),
        ("環境列 両方", "PCとスマートフォン両方で確認"),
        ("PC結果 / SP結果", "それぞれの環境でテストした結果を記入する"),
        ("○",          "期待結果通りに動作した"),
        ("×",          "期待結果と異なる動作をした（バグ）"),
        ("△",          "おおむね動作するが確認事項あり"),
        ("ー",          "その環境では対象外（N/A）"),
    ]))

    body.append(page_break())

    # ── 4. テストケース一覧 ──
    body.append(heading("4. テストケース一覧", 1))
    body.append(para(f"全{len(TEST_CASES)}件。PC結果・SP結果欄に ○ / × / △ を記入してください（対象外は「ー」）。",
                     size=18, color="595959", spacing_before=0, spacing_after=160))
    body.append(make_test_table(TEST_CASES))

    body.append(page_break())

    # ── 5. バグ記録シート ──
    body.append(heading("5. バグ記録シート", 1))
    body.append(para("テスト中に発見したバグをここに記録してください。", size=20, spacing_before=0, spacing_after=160))
    bug_cols = [("No.", 360),("TC番号",600),("バグ内容",3200),("環境",600),("優先度",600),("状態",600),("備考",3400)]
    bug_total = sum(w for _,w in bug_cols)
    bug_grid  = "".join(f'<w:gridCol w:w="{w}"/>' for _,w in bug_cols)
    bug_tbl   = (f'<w:tbl><w:tblPr><w:tblW w:w="{bug_total}" w:type="dxa"/></w:tblPr>'
                 f'<w:tblGrid>{bug_grid}</w:tblGrid>')
    hdr = "".join(cell(label, w, bold=True, shade="2E75B6", align="center", font_size=16) for label,w in bug_cols)
    bug_tbl += f"<w:tr><w:trPr><w:tblHeader/></w:trPr>{hdr}</w:tr>"
    for i in range(1, 12):
        r = cell(str(i), 360, align="center", font_size=16)
        r += "".join(cell("", w, font_size=16) for _,w in bug_cols[1:])
        bug_tbl += f"<w:tr><w:trPr/>{r}</w:tr>"
    bug_tbl += "</w:tbl>"
    body.append(bug_tbl)

    body.append(para("", spacing_before=120, spacing_after=0))

    # ── 6. テスト結果サマリー ──
    body.append(heading("6. テスト結果サマリー", 1))
    body.append(info_table([
        ("テスト実施日",  ""),
        ("実施者",        ""),
        ("総テスト数",    f"{len(TEST_CASES)}件"),
        ("PC ○ 合格",    ""),
        ("PC × 不合格",  ""),
        ("SP ○ 合格",    ""),
        ("SP × 不合格",  ""),
        ("△ 要確認",     ""),
        ("総合判定",      "合格 / 条件付き合格 / 不合格"),
        ("コメント",      ""),
    ]))

    body_xml = "\n".join(body)
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
  xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
  xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
  mc:Ignorable="">
<w:body>
{body_xml}
<w:sectPr>
  <w:pgSz w:w="12240" w:h="15840"/>
  <w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" w:header="720" w:footer="720" w:gutter="0"/>
</w:sectPr>
</w:body>
</w:document>"""

# ─── Static XML parts ─────────────────────────────────────────────────────────
STYLES_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault><w:rPr>
      <w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/>
      <w:sz w:val="20"/><w:szCs w:val="20"/>
      <w:lang w:val="ja-JP" w:eastAsia="ja-JP"/>
    </w:rPr></w:rPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>
    <w:pPr><w:outlineLvl w:val="0"/><w:spacing w:before="240" w:after="120"/><w:keepNext/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:b/>
      <w:color w:val="1F4E79"/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>
    <w:pPr><w:outlineLvl w:val="1"/><w:spacing w:before="200" w:after="80"/><w:keepNext/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:b/>
      <w:color w:val="2E75B6"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
  </w:style>
</w:styles>"""

SETTINGS_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:defaultTabStop w:val="720"/>
</w:settings>"""

RELS_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

DOC_RELS_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
</Relationships>"""

CONTENT_TYPES_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
</Types>"""

# ─── Write ────────────────────────────────────────────────────────────────────
out = os.path.join(os.path.dirname(__file__), "PALE_BLUE_DOT_テスト仕様書.docx")
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("[Content_Types].xml", CONTENT_TYPES_XML)
    zf.writestr("_rels/.rels", RELS_XML)
    zf.writestr("word/document.xml", build_document())
    zf.writestr("word/styles.xml", STYLES_XML)
    zf.writestr("word/settings.xml", SETTINGS_XML)
    zf.writestr("word/_rels/document.xml.rels", DOC_RELS_XML)

print(f"DOCX generated: {out}")
print(f"Test cases: {len(TEST_CASES)}")
