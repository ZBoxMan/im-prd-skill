# im-prd-skill

[English](README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Português](README.pt.md) | [Français](README.fr.md)

一個用來撰寫即時通訊（IM）與社群產品 PRD 的 Claude Agent Skill（技能包）。內建涵蓋 26 個模組的規則庫，整理主流即時通訊應用處理各項功能的方式，讓產出的規格預設符合 IM 慣例。只有主流應用做法確實不同的地方，才會以選擇題交由決策者裁決。可以只產出 Markdown 交付稿，也可以把說明卡寫到 Figma 畫布上。

本技能原為 ZYMIX 團隊打造。公開版移除了團隊的 Figma 檔案 key、設計系統取值、內部裁決與原始佐證資料；工作流程、規則庫、範本、腳本與評測案例皆完整保留。

## 版本

| 版本 | 路徑 | 說明 |
|---|---|---|
| English | [`en/box-prd-create/`](en/box-prd-create/) | 中文以外的語言請使用此版本。規則以英文撰寫；交付稿以使用者的語言撰寫。 |
| 简体中文 | [`zh-CN/box-prd-create/`](zh-CN/box-prd-create/) | 原始版本。包含評測案例（`evals/`）與完整變更紀錄。繁體中文使用者可任選其中一個版本。 |

兩個版本都使用技能名稱 `box-prd-create`；請擇一安裝。

## 解決什麼問題

直接請 AI 撰寫 IM 功能規格，通常會出現三種問題：把不確定的規則寫得像已定案；只涵蓋正常流程，漏掉封鎖、帳號註銷、離線、多裝置，以及群組與一對一聊天的差異等狀態；業界慣例與團隊真正需要拍板的少數決策混在一起，決策者必須通讀全文才能找出來。

本技能的處理方式：

- **三層規則庫**：基線（主流應用一致；預設遵循）、慣例（多數應用如此；預設採用建議做法）、分歧（各應用不同；標示為 Must-ask（必問）或 Default-OK（可預設））。
- **只問必問的問題**：每輪最多 4 道選擇題，建議選項排在最前面。其餘一律依建議撰寫，並逐行列在「Defaulted to recommendation」（已依建議預設）之下供審閱。
- **狀態覆蓋矩陣**：逐項檢查成功、失敗、逾時、離線、權限、多裝置同步，以及「對方已封鎖你／已註銷帳號／已退出群組」等狀態。
- **不確定之處保持可見**：需要決策的項目寫成 `{TBD: topic, recommended: approach}`，缺少的事實寫成 `{TBC: what is missing}`。不會把未定案的內容當成定案。
- **寫入關卡**：動到 Figma 之前，技能會列出將要建立的所有節點與批次；決策者核准後才會寫入畫布。

## 工作流程

| 步驟 | 內容 |
|---|---|
| 0 產品定位 | 確認對話類型（一對一／群組／頻道／社群）、平台、是否端對端加密、陌生人是否可以聯繫使用者，以及可行性前提 |
| 1 鎖定事實來源 | 記錄 Figma 檔案與節點；將每項需求標示為已定義／待確認／建議 |
| 2 IM 規範檢查 | 讀取對應的模組：遵循基線、預設採用慣例、依等級處理分歧 |
| 3 競品參考 | 僅針對規則庫未涵蓋的能力進行外部研究 |
| 4 狀態覆蓋矩陣 | 通用維度加上模組的必問狀態，各自標示為已涵蓋／不適用／未定義 |
| 5 先寫草稿 | 撰寫 Markdown 交付稿並執行 `lint_card_text.py`；篇幅較大的草稿再加上讀者測試 |
| 6 版面與編號 | 一次規劃好畫面順序、列與編號 |
| 7 寫入關卡 | `lint_card_text.py --gate` 通過且決策者核准後，才寫入任何內容 |
| 8 寫入卡片並自我檢查 | 每批寫入後自我檢查；最後附上驗收回條 |

交付稿順序：Decisions for Box（交由 Box 裁決）→ Defaulted to recommendation → Open items（未決項目）→ Role view summary（角色視角摘要）→ Cards（說明卡）→ Feature list（功能清單）→ Acceptance checkpoints（驗收要點，≤ 12）→ Suggested follow-ups（建議後續）。

## 目錄結構

```
en/box-prd-create/              # 英文版（zh-CN/ 結構相同）
├── SKILL.md                    # 工作流程與路由（入口）
├── references/
│   ├── im-norms/               # 26 個 IM 模組 + 反模式 + 歸屬表
│   ├── draft-template.md       # 交付稿與工作筆記範本
│   ├── self-check.md           # 交付自我檢查
│   ├── canvas-layout.md        # Figma 畫布版面
│   ├── figjam.md               # 流程圖與功能清單
│   ├── design-system.md        # 設計系統（範本，請填入自己的內容）
│   ├── rulings.md              # 裁決紀錄（範本，請填入自己的內容）
│   └── HISTORY.md              # 變更紀錄
└── scripts/
    ├── lint_card_text.py       # 卡片文字檢查（--gate 用於寫入關卡）
    ├── lint_skill.py           # 規則庫結構自我檢查
    └── brand_terms.txt         # 禁用品牌名稱
```

模組：帳號與裝置、聯絡人與隱私、聊天列表、傳送與回執、訊息操作、媒體與檔案、群組與頻道、通知、安全與資安、搜尋／通話／儲存空間、頁面結構、互動模式、服務帳號與機器人、聊天內付款、動態／頻道／社群、豐富訊息、翻譯與 AI、探索／登入／權限、錢包帳戶、邀請與成長、年齡與未成年人、處置與申訴、廣告與個人化、點數與會員、隱私中心、客服工單。

## 安裝

Claude Code（以下為英文版；中文請改用 `zh-CN/box-prd-create`）：

```bash
git clone https://github.com/ZBoxMan/im-prd-skill.git
```

```bash
cp -R im-prd-skill/en/box-prd-create ~/.claude/skills/
```

claude.ai：將 `box-prd-create` 資料夾壓縮成 zip，到「設定 → 功能 → Skills」上傳。

## 使用方式

直接描述功能即可，例如：

- 「幫群組聊天加上群組公告。撰寫 PRD，目前只要交付稿。」
- 「在設定頁加上『下載我的資料』。把 PRD 寫到 Figma：figma.com/design/<fileKey>，放在『設定』區。」
- 「撤回訊息的時限應該設多久？我要寫進 PRD。」

## 調整成適合你的團隊

- `references/design-system.md`：你的設計庫、元件 key、色彩與字型 token（僅在繪製原型畫面時使用）。
- `references/rulings.md`：團隊的寫作裁決與已停用的版面。
- `scripts/brand_terms.txt`：不得出現在卡片文字中的品牌名稱。
- SKILL.md 中的「ZYMIX」與「Box」分別是產品名稱與決策者；可依需要替換。
- 寫入 Figma 需要 [figma-console MCP](https://github.com/southleft/figma-console-mcp) 的 Desktop Bridge。只產出 Markdown 草稿則不需要額外設定。
- SKILL.md 中提到的 `box-figma-prd` 與 `box-prd-review` 是作者私有的搭配技能（畫布檢查與完整審查）。沒有它們，生成流程仍可運作。

## 評測

在中文版上進行：

- 盲測比較：8 個情境（多裝置、群組管理、紅包、檢舉、群組投票、好友動態、新使用者引導、收回／編輯訊息），以同一份需求與 21 個類似技能比較。由不知道來源的 Opus 評審就 IM 正確性、邊界涵蓋、決策處理、可實作性與可讀性評分：94 輪，90 勝，4 敗。
- 真實觸發：31 個正反向提示 × 3 次，以 `claude -p` 執行：31/31 判斷正確，反向提示無誤觸發。

紀錄：`zh-CN/box-prd-create/evals/trigger-results.md`。英文版尚未單獨評測。

## 來源與時效

於 2026 年 10 月，從主流即時通訊用戶端的公開行為、開源用戶端程式碼、官方說明中心與開發者文件，以及協定規格蒐集而成。模組檔案不含品牌名稱；不公開各產品的細節。多數數值是用戶端預設值，伺服器可能覆寫；請每 90 天複查一次。

## 授權

MIT
