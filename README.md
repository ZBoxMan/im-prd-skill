# im-prd-skill

[English](README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Português](README.pt.md) | [Français](README.fr.md)

A Claude Agent Skill for writing PRDs for messaging (IM) and social products. It ships a 26-module library of how mainstream messaging apps handle each feature, so generated specs follow IM conventions by default. Only the points where mainstream apps genuinely differ are put to the decision-maker, as multiple-choice questions. It can produce a Markdown delivery draft only, or also write the annotation cards onto a Figma canvas.

The skill was built for the ZYMIX team. This public edition removes the team's Figma file keys, design-system values, internal rulings and raw evidence; the workflow, rule library, templates, scripts and eval cases are intact.

## Editions

| Edition | Path | Notes |
|---|---|---|
| English | [`en/box-prd-create/`](en/box-prd-create/) | Use this for any language other than Chinese. Rules are in English; the delivery draft is written in the user's language. |
| 简体中文 | [`zh-CN/box-prd-create/`](zh-CN/box-prd-create/) | Original edition. Includes the eval cases (`evals/`) and full change history. |

Both editions use the skill name `box-prd-create`; install one of them.

## What it solves

Asking an AI to write an IM feature spec directly tends to go wrong in three ways: uncertain rules are written as if settled; only the happy path is covered, missing states such as blocked, deleted account, offline, multi-device, and group-vs-one-on-one differences; and industry conventions get mixed with the few calls the team really needs to make, so the decision-maker has to read everything to find them.

How this skill handles it:

- **Three-tier rule library**: baseline (mainstream apps agree; follow by default), convention (most apps do it; default to the recommendation), divergence (apps differ; tagged Must-ask or Default-OK).
- **Only must-ask questions are asked**: at most 4 multiple-choice questions per round, recommended option first. Everything else is written per recommendation and listed line by line under "Defaulted to recommendation" for review.
- **State coverage matrix**: success, failure, timeout, offline, permissions, multi-device sync, and "the other party has blocked you / deleted the account / left the group" are checked one by one.
- **Uncertainty stays visible**: items needing a decision are written as `{TBD: topic, recommended: approach}`, missing facts as `{TBC: what is missing}`. Nothing is passed off as settled.
- **Write gate**: before touching Figma, the skill lists every node it will create and the batches; it writes the canvas only after the decision-maker approves.

## Workflow

| Step | What happens |
|---|---|
| 0 Product framing | Confirm the conversation type (one-on-one / group / channel / community), platforms, end-to-end encryption, whether strangers can reach users, and feasibility prerequisites |
| 1 Lock the source of truth | Record the Figma file and nodes; tag each requirement as defined / to-confirm / suggested |
| 2 IM norms check | Read the matching modules: follow baselines, default conventions, handle divergences by level |
| 3 Competitor reference | External research only for capabilities the library does not cover |
| 4 State coverage matrix | General dimensions plus module must-ask states, each marked covered / not applicable / undefined |
| 5 Draft first | Write the Markdown delivery draft and run `lint_card_text.py`; add a reader test for larger drafts |
| 6 Layout and numbering | Plan screen order, rows and numbering in one pass |
| 7 Write gate | `lint_card_text.py --gate` passes and the decision-maker approves before anything is written |
| 8 Write cards and self-check | Self-check after each batch; finish with an acceptance receipt |

Delivery draft order: Decisions for Box → Defaulted to recommendation → Open items → Role view summary → Cards → Feature list → Acceptance checkpoints (≤ 12) → Suggested follow-ups.

## Layout

```
en/box-prd-create/              # English edition (same layout in zh-CN/)
├── SKILL.md                    # Workflow and routing (entry point)
├── references/
│   ├── im-norms/               # 26 IM modules + anti-patterns + ownership table
│   ├── draft-template.md       # Delivery draft and working notes template
│   ├── self-check.md           # Delivery self-check
│   ├── canvas-layout.md        # Figma canvas layout
│   ├── figjam.md               # Flowcharts and feature list
│   ├── design-system.md        # Design system (template, fill in your own)
│   ├── rulings.md              # Rulings (template, fill in your own)
│   └── HISTORY.md              # Change history
└── scripts/
    ├── lint_card_text.py       # Card text lint (--gate for the write gate)
    ├── lint_skill.py           # Rule library structure self-check
    └── brand_terms.txt         # Banned brand names
```

Modules: accounts and devices, contacts and privacy, chat list, sending and receipts, message actions, media and files, groups and channels, notifications, safety and security, search/calls/storage, page structure, interaction patterns, service accounts and bots, in-chat payments, feeds/channels/communities, rich messages, translation and AI, discovery/sign-in/permissions, wallet account, invites and growth, age and minors, enforcement and appeals, ads and personalization, points and membership, privacy center, support tickets.

## Install

Claude Code (English edition shown; use `zh-CN/box-prd-create` for Chinese):

```bash
git clone https://github.com/ZBoxMan/im-prd-skill.git
```

```bash
cp -R im-prd-skill/en/box-prd-create ~/.claude/skills/
```

claude.ai: zip the `box-prd-create` folder and upload it under Settings → Capabilities → Skills.

## Usage

Just describe the feature, for example:

- "Add group announcements to group chats. Write the PRD, delivery draft only for now."
- "Add 'Download my data' to Settings. Write the PRD onto Figma: figma.com/design/<fileKey>, in the Settings zone."
- "How long should the unsend window be? I need it in the PRD."

## Adapting it to your team

- `references/design-system.md`: your design library, component keys, color and type tokens (used only when drawing prototype screens).
- `references/rulings.md`: your team's writing rulings and retired layouts.
- `scripts/brand_terms.txt`: brand names that must not appear in card text.
- "ZYMIX" and "Box" in SKILL.md are the product name and the decision-maker; replace them as needed.
- Writing to Figma needs the Desktop Bridge of [figma-console MCP](https://github.com/southleft/figma-console-mcp). Markdown-only drafts need nothing extra.
- `box-figma-prd` and `box-prd-review`, mentioned in SKILL.md, are the author's private companion skills (canvas inspection and full review). The generation flow works without them.

## Evaluation

Run on the Chinese edition:

- Blind comparison: 8 scenarios (multi-device, group management, red packets, reporting, group polls, friend feed, new-user onboarding, unsend/edit) against 21 similar skills on the same brief. An Opus judge, blind to the source, scored IM correctness, edge coverage, decision handling, implementability and readability: 94 rounds, 90 wins, 4 losses.
- Real triggering: 31 positive and negative prompts × 3 runs with `claude -p`: 31/31 correct, no false triggers on negatives.

Records: `zh-CN/box-prd-create/evals/trigger-results.md`. The English edition has not been evaluated separately.

## Sources and freshness

Collected in October 2026 from the public behavior of mainstream messaging clients, open-source client code, official help centers and developer docs, and protocol specs. Module files contain no brand names; per-product details are not published. Most values are client defaults that servers may override; review every 90 days.

## License

MIT
