# Lisa's PPT

<p align="left">
  <img src="assets/tedandlisa-cover.jpg" alt="Hi Ted, Meet Lisa" style="width: 100%; max-width: 100%;">
</p>

[English](README.md) · [한국어](README_KO.md) · **繁體中文**

> **[Hi Ted, Meet Lisa](https://github.com/monomind-ai-lab/hi-ted-meet-lisa) 的原生可編輯 PowerPoint。**
> 一份 `.pptx`，每個圖形、文字方塊與圖表都是 PowerPoint 物件。
> 以技能（skill）安裝；沒有網頁模式。

Hi Ted, Meet Lisa 產出的是一個獨立的 HTML 檔。但有些場合要的是 `.pptx`：文字點一下就能改、圖表有「編輯資料」按鈕、在 PowerPoint 裡直接開啟，不必再裝任何東西。Lisa's PPT 做的就是這個檔案。

它是一個硬分叉（hard fork）。引擎是 Hugo He 的 [PPT Master](https://github.com/hugohe3/ppt-master) v6.1.0（MIT），只匯入一次。上面疊的是 byungjunjang 的 [slide-master](https://github.com/byungjunjang/slide-master)（MIT）所做的改良：透過 Codex 自己的影像工具產生圖片、帶版本號的匯出、七套韓國場域版型、一條「一種字型家族」的規則、韓文的引導介面。從那一刻起，這個儲存庫就獨立了。不再從任一來源拉取任何東西；日後若有回移的修正，也是手工完成，並連同來源 commit 記錄在 [`NOTICE`](NOTICE)。

引導介面說英文、韓文與繁體中文。這份 README 也是。

---

## 從這裡開始

Python 3.10 到 3.14，然後安裝相依套件。不需要 Node：負責作圖的 Codex CLI 是選配的 Node 工具，匯出檢查則是 Python。

```sh
pip install -r requirements.txt
```

外掛裝一次，`/lisa-ppt` 就永遠是你的指令。

```sh
/plugin marketplace add monomind-ai-lab/lisa-ppt
/plugin install lisa-ppt@monomind-ppt
```

在 Codex 裡，兩步併成一步：

```sh
codex plugin marketplace add monomind-ai-lab/lisa-ppt
```

任何遵循 Agent Skills 慣例的代理程式：

```sh
npx skills add monomind-ai-lab/lisa-ppt
```

或者把儲存庫 clone 下來，用你的代理程式開啟那個資料夾。技能放在 `skills/`，另有自動產生的 stub 放在 `.codex/skills/`，讓 Codex 找到同樣的三個技能。

**圖片是選配，而且不需要 API 金鑰。** 裝好 Codex CLI，登入一次。Lisa's PPT 之後就透過 Codex 自己的 `image_gen` 作圖；`IMAGE_BACKEND` 留空，這就是預設。也可以改用環境變數設定 API 金鑰的後端。

```sh
npm install -g @openai/codex
codex login
```

**`.pptx` 不會內嵌字型。** 每一台會開啟這份簡報的機器，都要裝好該語言的家族字型：韓文用 Pretendard，繁體中文用 Noto Sans TC，英文用 Plus Jakarta Sans，id 與程式碼用 JetBrains Mono。字型檔連同 SIL OFL 授權全文一起放在這個儲存庫裡；一道指令就能在 macOS、Windows 與 Linux 上以使用者層級安裝。

```sh
python3 skills/lisa-ppt/scripts/install_fonts.py            # --dry-run 只列計畫，--check 只回報狀態
```

**之後，需要什麼就下指令：**

```text
/lisa-ppt projects/q3/sources/report.pdf，給董事會看，10 頁左右，語氣收斂
```

讀取來源、在瀏覽器開啟引導介面、每頁寫一張 SVG 並即時預覽、檢查幾何，然後匯出 `projects/q3/exports/<標題>_ver1.pptx`。

```text
/lisa-ppt 一份向非工程師解釋 RAG 的簡報；資料你自己查
```

沒有來源？代理程式先做研究，再跑同一條流程。

```text
/lisa-ppt deck.html
```

已經有一份做好的 Lisa 簡報？它的每一頁會成為專案的來源 Markdown，它自己的顏色 token 會成為預先填好的 `design_spec.md`，讓 `.pptx` 從這份簡報自己的樣子開始。

其他的用白話說就好，路由器會挑路線：

```text
用 sources/company-template.pptx 的設計，填入 sources/plan.md 的內容
```

```text
把講者備忘稿和旁白加進 exports/deck_ver2.pptx
```

兩者都走 Edit Native PPTX 路線。前者保留範本的設計並逐頁填入內容，沒有改動的頁面逐位元組照抄。後者把備忘稿與旁白寫進檔案，並匯出一份 `_narrated` 的副本。

**你會拿到什麼**

- **一份 `.pptx`**，全是原生 DrawingML 圖形、文字方塊與圖表。在 PowerPoint 裡點任何元素都能改。
- **需要時，原生圖表與表格。** 匯出時加上 `--native-charts-and-tables`，符合條件的群組會變成 PowerPoint 的圖表與表格物件，附「編輯資料」，放在 `_native_charts_tables` 副本裡。預設則維持為可編輯的圖形，在每個應用程式裡都長得一樣。
- **帶版本號的匯出。** `<標題>_ver1.pptx`，接著是 `_ver2`，不會覆蓋上一版。
- **七套版型**，來自 slide-master：`academic_defense`、`government_blue`、`government_red`、`medical_university`、`psychology_attachment`、`ai_ops`、`pixel_retro`，與上游自帶的七套並列。再加上以 Lisa 自己的 token 建立的 `monomind` 品牌，以及兩套自家風格：`evidence-deck` 與 `paper-brief`。
- **16:9 以外的畫布**：4:3、A4、橫幅、限時動態、上游提供的社群格式，以及 1080×1350 的 `instagram`。
- **每種語言一種家族字型。** 層次靠字重與字級，不靠換字型。

---

## 一份簡報怎麼做出來

1. **你交出來源。** 一份 PDF、一份 DOCX、Markdown、一個網址、一張試算表，或一段文字。代理程式建立 `projects/<名稱>/` 並讀取它。
2. **引導介面在你的瀏覽器裡開啟**，英文、韓文或繁體中文（上游的簡體中文與日文也保留）。兩個階段：先是溝通契約，然後是最終方案與製作。畫布、頁數、版型或品牌、字型、圖片政策；每個問題都有預設值。每個選項都是型錄裡的 id，所以你讀題目用的語言不會滲進簡報。
3. **圖片**，如果你要的話，透過 Codex 的 `image_gen`。
4. **每頁一張 SVG**，依確認過的設計系統寫成，附即時預覽。在預覽裡點一個位置加上註記，代理程式就修那一頁。
5. **幾何關卡。** 重疊的文字、跑出畫布的圖形、彆扭的斷行，由字寬計算找出並修正；被標記的頁面會再渲染成像素看一次。開口要求，就逐頁做視覺檢查。
6. **匯出。** 轉換器把每張 SVG 變成 DrawingML，寫出 `projects/<名稱>/exports/<標題>_ver<N>.pptx`。交付檢查會把檔案讀回來，確認封裝完整與可攜性。

---

## 字型

每種語言一種家族。韓文用 Pretendard，繁體中文用 Noto Sans TC，英文用 Plus Jakarta Sans；id 與程式碼用 JetBrains Mono。層次來自字重、字級、字距與顏色，從不靠換字型家族。轉換器會把 CJK 家族同時登記到拉丁與東亞兩個字型槽，中英混排時 PowerPoint 就不會替換掉其中一個。

提示詞只會點名已隨附的字重：Pretendard 與 Plus Jakarta Sans 各六種（Light 到 ExtraBold）、Noto Sans TC 四種（Light、Regular、Medium、Bold）、JetBrains Mono 三種（Regular、Medium、SemiBold）。`.pptx` 一個字型都不內嵌：每台開啟簡報的機器都要裝好該家族，否則簡報會以那台機器替代的字型開啟。完整政策見 [`AGENTS.md`](AGENTS.md) 與 [`skills/lisa-ppt/assets/fonts/README.md`](skills/lisa-ppt/assets/fonts/README.md)。

---

## 通往 Lisa 的兩條路（進行中）

兩條都在各自的分支上進行，目前都還不在這棵樹裡。

- **從 Lisa 到這裡。** `/lisa` 的引導介面將會把 Lisa's PPT 列為一張外部卡片，掛著 `PPTX` 標籤。選它，你給 Lisa 的簡報摘要與答案會成為第一階段的契約，並預先選好 `monomind` 品牌。前提是這個外掛已安裝。
- **從 Lisa 的檔案到這裡。** `/lisa-ppt deck.html` 將會讀取一份做好的 Lisa 簡報：檔案裡的 `LISA:CONTENT-START/END` 區塊成為專案的來源 Markdown，token 區塊成為預先填好的 `design_spec.md`，讓 `.pptx` 與 HTML 一致。

---

## `projects/` 資料夾

每份簡報就是一個資料夾。不會在它之外寫任何東西。

| 路徑 | 裡面是什麼 |
| --- | --- |
| `projects/<名稱>/sources/` | 你交出來的東西，以及它的 Markdown 轉換 |
| `projects/<名稱>/design_spec.md` | 這份簡報確認過的設計系統與內容大綱 |
| `projects/<名稱>/notes/` | 每頁一份 Markdown 筆記，以及 `total.md` |
| `projects/<名稱>/images/` | 生成、取得與你提供的圖片 |
| `projects/<名稱>/svg_output/` | 每頁一張 SVG，寫成的原樣 |
| `projects/<名稱>/svg_final/` | 自足的預覽 SVG |
| `projects/<名稱>/exports/` | `<標題>_ver<N>.pptx` 與它的 `_native_charts_tables`、`_narrated` 副本 |

`analysis/`、`templates/` 與 `validation/` 放的是擷取出來的事實、專案層級的範本與工作流程記錄。`projects/` 是你的，不會被 commit。換機器時把它搬走就好。

---

## 它做不到的事

- **一次到位。** 模型決定上限；建議用大脈絡（large-context）的 Claude。留一段修飾的時間，在預覽裡或在 PowerPoint 裡。
- **內嵌字型。** 見上文。
- **保證 PowerPoint 以外的公式。** 公式以 OMML 匯出，在 PowerPoint 裡可編輯；Keynote、WPS 與 LibreOffice 不在契約之內。
- **SmartArt。** 刻意不做。
- **接續快速模式。** 快速模式一次跑完，沒有確認階段，也沒有可接續的設計紀錄。
- **gpt-image-2 的透明圖片。** 要求透明背景時，模型會畫出棋盤格。`codex-image` 技能會改寫提示詞並告訴你；能用單色背景就用單色背景。
- **保持小巧——但要知道這裡的「小」是什麼意思。** 完整 clone 是 210 MB，`--depth 1` 是 131 MB，實測明細見下方[它有多大](#它有多大)。光是 `templates/icons/` 就有 12,027 個 SVG——內容只約 13 MB，但 12,027 個小檔案在檔案系統上進位成區塊後約佔 48 MB——留在樹裡而不是改成 release 下載，好讓外掛安裝一次到齊；隨附的字型佔 32 MB。
- **在每個 Python 上都能跑。** 3.10 是底線，3.14 已驗證：`skia-pathops` 與 `uharfbuzz` 提供 abi3 wheel，流程本身在 3.11 上跑。

---

<p align="left">
  <img src="assets/ted-and-lisa.jpg" alt="Ted and Lisa" width="460">
</p>

---

## 包含哪些東西

- **`lisa-ppt`**：主流程。引導、SVG 頁面、品質關卡、匯出，以及 Edit Native PPTX 路線——填入範本，或替做好的檔案加上備忘稿、旁白與轉場。
- **`codex-image`**：透過 Codex CLI 產生圖片，內含透明背景的因應做法。基於 wjb127/codex-image。
- **`diagram-design`**：圖解構圖規則，vendor 自 cathrynlavery/diagram-design。它的獨立流程已關閉，被停用的原文逐字保留作為紀錄。
- **確認介面**、附即時預覽的 SVG 編輯器、DrawingML 轉換器、品質檢查器，以及 `.codex/skills` 的 stub 同步。
- **範本**：十四套版型、`monomind` 品牌、與上游十二套並列的 `evidence-deck` 與 `paper-brief` 風格、圖表與表格範本，以及圖示庫。

---

## 它有多大

在 `main` 上實測，2026-09-03：

| | |
|---|---|
| `git clone` | **210 MB** — 94 MB 的工作目錄，加上 116 MB 的歷史 |
| `git clone --depth 1` | **131 MB** — 同樣的工作目錄，歷史只有 37 MB |
| 只算工作目錄 | 12,869 個檔案、55 MB 的內容，在磁碟上約 94 MB |

這 94 MB 裡有 80 MB 來自兩個目錄，而且兩個都是刻意留下的：

- **`skills/lisa-ppt/templates/icons/`** — 12,027 個 SVG。內容只有 13 MB，
  在磁碟上卻約 48 MB：每個檔案不到 1 KB，但每個檔案仍要佔一個檔案系統區塊。
  以檔案形式保留，因為一份得停下來去下載圖示的簡報，就是一份會停下來的簡報。
- **`skills/lisa-ppt/assets/fonts/`** — 32 MB，四個字型家族共 19 個字重。
  PPTX 不會內嵌字型，所以頁面指名的家族必須存在於開啟它的那台機器上，
  由 `install_fonts.py` 負責安裝。

歷史比工作目錄重，是因為 v6.1.0 匯入時帶進了上游的 `docs/assets/`（33 MB，
一支主視覺 GIF）與 AI 影像對照圖庫（43 MB 的 PNG），兩者又在同一批 commit 中
被移除。它們已經不在檔案樹裡，卻仍留在歷史中；現在各自只剩一個 README 指出去向。
`--depth 1` 會跳過它們，而流程本身也不需要它們。

---

## 從哪裡來

匯入兩次，之後獨立。

1. **PPT Master v6.1.0**（`hugohe3/ppt-master`，commit `c40bca58`，2026-08-31），以一個 commit 帶入：每頁一張 SVG 的流程、DrawingML 轉換器、OMML 公式子系統、超連結保留、`svg_quality` 檢查器、圖形合併與文字排版（shaping）。
2. **slide-master**（`byungjunjang/slide-master`，commit `166472b`，2026-08-04），逐檔移植、各自成為一個 commit：Codex 影像後端與它的透明背景規則、`_ver<N>` 匯出、七套版型、`instagram` 畫布、韓文引導介面字串與 README、家族字型規則、stub 同步、`diagram-design` 的 vendor 做法。

沒有上游 remote、沒有更新腳本、沒有執行期的署名檢查。`NOTICE` 是帳本：兩個匯入點、每一個移植的檔案，以及日後任何回移的修正與其上游 commit。

---

## 授權

[MIT](LICENSE)。完整的授權鏈在 [`NOTICE`](NOTICE)：

- PPT Master，Copyright (c) 2025-2026 Hugo He，MIT
- slide-master，byungjunjang，MIT；以名稱、URL 與匯入的 commit 署名
- `codex-image`，Copyright (c) 2026 wjb127，MIT；授權隨技能附上
- `diagram-design`，Copyright (c) 2025 Cathryn Lavery，MIT；授權隨技能附上
- Pretendard、Noto Sans TC、Plus Jakarta Sans 與 JetBrains Mono，SIL Open Font License 1.1；授權全文放在字型檔旁
- Lisa's PPT，Copyright (c) 2026 MonoMind AI Lab，MIT

Lisa's PPT 將會在 [html.monomind.one](https://html.monomind.one) 上，與 HTML 範本並列展示。
