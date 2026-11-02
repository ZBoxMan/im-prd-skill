# Translation guide: zh-CN → en (box-prd-create)

Source: `zh-CN/box-prd-create/`. Target: `en/box-prd-create/` (same relative paths, same file names).

## Hard rules

1. **Translate faithfully and completely.** Every rule, number, option, condition, exception and example must survive. Do not summarize, merge, drop or add rules. Keep the same line structure: one source line → one target line (scripts count lines; module files must stay ≤ 200 lines, SKILL.md ≤ 300 lines).
2. **Keep all IDs, file names, paths, code, commands, Figma API names, placeholders' shape and Markdown structure unchanged** (e.g. `NOTI-20`, `references/im-norms/08-notifications.md`, `figma_execute`, `402 × 872`, tables, bold, `｜`-separated tails become ` | `).
3. **Module files must not contain product brand names** (no WhatsApp, Telegram, WeChat, Signal, QQ, LINE, etc.). Apple and Google may appear only where the source has them.
4. "Box" is the decision-maker's name. Keep "Box". "ZYMIX" is the product name. Keep "ZYMIX".
5. Write plain, precise product-spec English. No marketing tone. US spelling.
6. Chinese-typography rules (CJK/Latin spacing, full-width punctuation, 「」 corner quotes, Chinese list numbering words) are translated but marked "(Chinese copy only)", and the English-copy equivalent is stated right after where obvious: UI copy in English cards is wrapped in straight double quotes "…"; curly quotes and 【】 are banned in both.

## Fixed formats (scripts parse these — follow exactly)

Module section headings (im-norms/NN-*.md):

| zh | en |
|---|---|
| `## 目录` | `## Contents` |
| `## 基线（默认遵循，置信度高）` | `## Baseline (follow by default, high confidence)` |
| `## 惯例（可默认，标建议）` | `## Conventions (default-OK, mark as suggested)` |
| `## 分歧点（必问的问 Box，可默认的按推荐写并列清单）` | `## Divergences (ask Box on must-ask; write default-OK per recommendation and list it)` |
| `## 必问状态（…）` | `## Must-ask states (…)` |
| `## 反模式` | `## Anti-patterns` |
| `## 校准样例` | `## Calibration sample` |

Entry line: `- **[NOTI-01] 标题**：正文。必定义：…。｜量级：…｜置信度：高`
→ `- **[NOTI-01] Title**: body. Must define: …. | Magnitude: … | Confidence: High`

- `置信度：高/中/低` → `Confidence: High/Medium/Low` (keep any parenthetical reason after it, translated).
- Divergence: `选项 A：…／选项 B：…。推荐：A，理由：…。取舍背景：…。｜级别：必问` → `Option A: … / Option B: …. Recommended: A. Rationale: …. Background: …. | Level: Must-ask` (`可默认` → `Default-OK`).
- Pointer entry body starting `见 XXX-NN` → `See XXX-NN` (must be the first words after the colon). Inline `见 NOTI-23` → `see NOTI-23`.
- `按必问处理` → `treat as must-ask`.
- Weak-evidence words: `仅两家` → `only two products`, `仅一家` → `only one product`, `常识` → `common sense`, `未取证` → `not evidenced`. `两家/三家/五家` → `two/three/five products`. `一家` → `one product`.
- Calibration sample cards: `说明：` → `Description:`; sample text must contain no brand names, no hex colors, no px, no rule IDs.

## Delivery draft vocabulary (lint parses headings and placeholders)

| zh | en |
|---|---|
| 交付稿 | delivery draft (`<feature>-delivery.md`) |
| 工作底稿 / 底稿 | working notes (`<feature>-notes.md`) |
| `## 待 Box 裁决` | `## Decisions for Box` |
| `## 已按推荐默认` | `## Defaulted to recommendation` |
| `## 未决项` | `## Open items` |
| `## 角色视角速览` | `## Role view summary` |
| `## 功能清单` | `## Feature list` |
| `## 验收要点` | `## Acceptance checkpoints` |
| `## 建议后续` | `## Suggested follow-ups` |
| `{待定：议题，推荐：做法}` | `{TBD: topic, recommended: approach}` |
| `{待查：缺什么}` | `{TBC: what is missing}` |
| runtime variable `{昵称}` | `{nickname}` (no TBD/TBC prefix) |
| 说明： | Description: |
| 点击后进行以下判断： | On tap, check in order: |
| `a. 1-<判断名>：` | `a. 1-<check name>:` |
| 注： | Note: |
| 本期 / 后续 | This release / Later |
| 本期不做：… | Not in this release: … |
| 以卡内为准 | per the card |
| 同 帧名-编号 | same as FrameName-N |
| 校验同 {帧名-编号} | checks same as {FrameName-N} |
| （按 Q2 推荐） | (per Q2 recommendation) |
| 服务端返回 | returned by server |

## Core terms

| zh | en |
|---|---|
| 规范库 | norms library |
| 基线 / 惯例 / 分歧点 | baseline / convention / divergence |
| 必问 / 可默认 | must-ask / default-OK |
| 必问状态 | must-ask states |
| 必定义 | must define |
| 量级 | magnitude |
| 置信度 | confidence |
| 反模式 | anti-pattern |
| 校准样例 | calibration sample |
| 现档 | current tier |
| 取证 / 证据 | evidence |
| 说明卡 | annotation card |
| 卡标题 | card title |
| 编号徽标 | number badge |
| 原型帧 / 屏 | prototype frame / screen |
| 帧名-编号 | FrameName-N |
| 大区 | zone |
| 标注层 | annotation layer |
| 判断链 | decision chain |
| 判断链形态（唯一合规写法） | Decision-chain shape (the only compliant form) |
| 连线跨度约束 | Connector span constraint |
| 状态覆盖矩阵 | state coverage matrix |
| 功能清单 | feature list |
| 事实源 | source of truth |
| 保护范围 | protected scope |
| 写入闸门 | write gate |
| 写入申请 | write request |
| 交付自检 | delivery self-check |
| 验收回执 | acceptance receipt |
| 读者测试 | reader test |
| 提问预算 | question budget |
| 产品定型 | product framing |
| 定型：是 | framing: yes |
| 锁事实源 | lock the source of truth |
| 竞品参照 | competitor reference |
| 裁决 / 裁决记录 | ruling / rulings |
| 未决项 | open items |
| 现网 | production (current live behavior) |
| 设计系统 | design system |
| 品牌名禁用 | brand-name ban |
| 视觉规格 | visual specs |
| 文案 | copy |
| Toast / 弹窗 / 底部面板 / 行内错误 | toast / dialog / bottom sheet / inline error |
| 角标 | badge count |
| 会话 / 会话列表 | chat / chat list |
| 单聊 / 私聊 | one-on-one chat |
| 群 / 群聊 / 频道 / 社区 | group / group chat / channel / community |
| 群主 / 管理员 / 成员 | group owner / admin / member |
| 免打扰 | mute |
| @提及 / @全体 | @mention / @all |
| 撤回 | unsend |
| 编辑 | edit |
| 转发 / 引用 / 回复 | forward / quote / reply |
| 已读回执 / 送达 | read receipt / delivered |
| 拉黑 | block |
| 删除好友 | remove contact |
| 消息请求 | message request |
| 注销 | account deletion |
| 冻结 / 封禁 / 禁言 | freeze / ban / mute (member) |
| 多端 / 主设备 / 辅助端 | multi-device / primary device / linked device |
| 端到端加密 | end-to-end encryption |
| 红包 | red packet |
| 转账 / 收款 | transfer / collect payment |
| 钱包 | wallet |
| 动态 / 故事 | feed post / story |
| 服务号 / 机器人 | service account / bot |
| 举报 | report |
| 风控 / 频控 | risk control / rate limit |
| 持牌机构 | licensed institution |
| 上架地区 | launch region |
| 积分 / 会员 | points / membership |
| 工单 | support ticket |
| 隐私中心 | privacy center |
| 主流产品做法不一 | mainstream products differ |
