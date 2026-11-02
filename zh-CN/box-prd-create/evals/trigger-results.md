# 触发评测记录

| 日期 | 方法 | 结果 | 备注 |
|---|---|---|---|
| 2026-10-30 | `skill-creator/scripts/run_eval.py`（`claude -p`） | 无效 | 本机 Claude Code CLI 未登录（输出「Not logged in」），两次运行全部 0 触发均为假结果，不采信。Box 在终端执行 `claude /login` 后可重跑 |
| 2026-10-30 | 代理选择测试：无上下文子 agent（sonnet）只看 19 个相邻技能的名称与描述，对 22 条请求选择要加载的技能 | 22/22 | 正例 12 条全部首选 box-prd-create；负例 10 条无一选中，分别分流到 box-prd-review、box-figma-prd、dual-panel-prd、write-spec、market-research 等。局限：非真实运行时，不含账号同名旧版的竞争 |
| 2026-10-31 | 代理选择测试扩大版：全量 31 条（正 18／负 13）；候选为本机运行时实际技能清单 114 项（本地 72 + 账号与插件，含同名账号版 box-prd-create 的旧描述）；3 个无上下文子 agent（sonnet ×2、haiku ×1）独立作答 | 30/31、31/31、30/31 → 修复后 31/31、31/31 | 两次失分同为「续写 figma 链接里的原型」被 box-figma-prd 抢走（其本地描述含「生成、续写原型 PRD」）。已把 box-figma-prd 描述改为画布读写／取证／验证，新建与续写交 box-prd-create 主导；复跑 sonnet、haiku 各一次均 31/31，验证脚本与节点定点检查两条负例仍落在 box-figma-prd。haiku 17 次选中同名账号版（内容已同步为 v5，不影响结果）。真实 `claude -p` 评测仍待 CLI 登录 |

# 同题盲评记录（对外部同类 skill）

方法：对手按其 SKILL.md 方法论产出同一需求；opus 评审在不知来源、A/B 顺序轮换的情况下按 IM 正确性、边界覆盖、决策处理、可实现性、可读性五维打分。原始结果未随公开版发布。

| 轮次 | 本技能版本 | 对手 | 用例 | 结果 |
|---|---|---|---|---|
| iteration-5 | v2.4 | heyimjames chat-and-messaging、product-on-purpose deliver-prd、phuryn create-prd | 撤回、拉黑、编辑 | 9/9 胜 |
| iteration-6 | v2.5 | heyimjames、deliver-prd | 同上 | 6/6 胜 |
| iteration-7 | v2.6 | heyimjames、deliver-prd | 同上 | 6/6 胜 |
| iteration-8 | v2.6 | 996pm interaction-prd、heyimjames nikita-bier-consumer-apps、SpaceZephyr pm-prd-writer、本机 ada-prd | 撤回、拉黑、编辑 | 11/12（负 1：拉黑 vs interaction-prd，已据此出 v2.7）|
| iteration-9 | v2.7 | interaction-prd、pm-prd-writer | 同上 | 6/6 |
| iteration-10 | v2.8 | deliver-prd、interaction-prd | 群红包、实时位置 | 4/4 |
| iteration-11 | v2.9 | deliver-prd、interaction-prd | 会话列表广告位、受限申诉 | 4/4 |
| iteration-12 | v3.0 | deliver-prd、interaction-prd | 会员订阅、下载我的数据 | 4/4 |
| iteration-14 | v3.0 | 全网普查最强未测 3 个：PANGKAIFENG prd-architect、Uxcel product-spec、82030615 EARS PRD | 撤回、拉黑、会员订阅 | 9/9 |

累计：10 个对手（含普查覆盖的 IM 唯一专项 skill 与通用 PRD 类最强者）59 局 58 胜 1 负。普查记录未随公开版发布。
| iteration-15 | v3.0.2 | 普查备选：hieubui2409 product-spec、rastian interaction-design-skills、deanpeters prd-development | 拉黑、会员订阅 | 6/6（累计 13 个对手 65 局 64 胜 1 负）|
| iteration-16 | v3.0.5 | 同 iteration-15 三个对手（复用其产出） | 拉黑、会员订阅 | 6/6（累计 13 个对手 71 局 70 胜 1 负）|
| iteration-17/18 | v3.0.6/v3.0.7 | 新旧版本同评审盲比（对照 v3.0.4） | 拉黑、会员订阅 | 两题新版可读性、完整性、正确性三维均高于 v3.0.4 |
| iteration-19 | v3.0.7 / v3.0.8 | 996pm interaction-prd（历史唯一负局的对手）；新旧版本同评审盲比 | 多设备登录 | 对手 1/1 胜（累计 13 个对手 72 局 71 胜 1 负）；v3.0.8b 与 v3.0.7 同分 22，评审判新版胜（防钓鱼、加密会话裁决更完整）|
| iteration-20 | v3.0.8 | 996pm interaction-prd | 群管理 | 1/1 胜（累计 13 个对手 73 局 72 胜 1 负）；多设备 v3.0.8 复测确认修正落卡 |
| iteration-21/22 | v3.0.9 / v3.0.10 | 996pm interaction-prd；82030615 write-ears-prd（非社交通用需求技能） | 红包 | 两轮均第一（累计 14 个对手 76 局 75 胜 1 负）；群管理 v3.0.9 复测确认落卡 |
| iteration-23/24 | v3.0.10 / v3.0.11 | 996pm interaction-prd；hieubui2409 product-spec（非社交通用规格技能） | 举报 | 两轮均第一（累计 15 个对手 79 局 78 胜 1 负）；红包 v3.0.10 复测确认落卡 |
| iteration-25/26 | v3.0.11 / v3.0.12 | 996pm interaction-prd；phuryn create-prd（非社交通用 PRD 技能） | 群投票 | 两轮均第一（累计 16 个对手 82 局 81 胜 1 负）；举报 v3.0.11 复测确认落卡 |
| iteration-27/28 | v3.0.12 / v3.0.13 | 996pm interaction-prd；deanpeters prd-development（非社交通用 PRD 技能） | 好友动态 | 首轮第二（负 interaction-prd）；修订后第一（累计 17 个对手 85 局 83 胜 2 负）；群投票 v3.0.12 复测确认落卡 |
| iteration-29/30 | v3.0.13 / v3.0.14 | 996pm interaction-prd；product-on-purpose deliver-prd；SpaceZephyr pm-prd-writer（后两者为非社交通用 PRD 技能） | 新用户引导 | 首轮第三（负 interaction-prd、pm-prd-writer）；修订后第一（累计 19 个对手 91 局 87 胜 4 负）；好友动态 v3.0.13 复测确认落卡 |
| iteration-31 | v3.0.14 | （复测，无对手） | 新用户引导 | v3.0.14 末批修正（加盐与限流、号码设备 IP 计数与人机校验、超时计数以服务端为准、「暂不」后首条消息再引导、现行规则注明出处）全部落卡 |
| iteration-32 | v3.0.14 | pmYangKun create-prd-skill；mohitagw15856 prd-template；996pm interaction-prd | 撤回与编辑 | 第一（累计 21 个对手 94 局 90 胜 4 负） |
| iteration-33 | v3.0.15 | （复测，无对手） | 撤回与编辑 | v3.0.15 修正落卡：看图、语音、文件预览中被撤回即关闭或停止；文案不承诺对方一定看不到；编辑时限进默认并注明可配置；本期不做写理由；撤回前已进入举报页的照常提交原内容 |
| 2026-11-01 | 真实 `claude -p`（本机 CLI 已登录；31 条 × 3 次，禁写文件与命令，命中 box-prd-create 或账号同名版即计触发，≥2/3 判触发） | v3.0.15：29/31（负例 13/13 全对，零误触发；漏：「撤回时限怎么定写进 PRD」1/3、「设置页加下载我的数据写 PRD」1/3）→ v3.0.16 描述补两类说法后 31/31（两条均 3/3） | 首次有效真实评测；runner 与原始结果在会话 scratchpad/realeval（full-v3015.json、full2.json） |
