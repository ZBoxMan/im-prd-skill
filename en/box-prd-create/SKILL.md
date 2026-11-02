---
name: "box-prd-create"
description: "Use when creating or continuing a PRD for an IM/social feature in ZYMIX Figma: prototype screens, annotation cards, number badges, state coverage matrix, notification template cards, flowcharts and feature lists. Also use when adding a feature to any ZYMIX page (settings, chat, group, wallet, etc.) and a PRD, prototype or requirement card is requested, or when asking how to set an IM rule (time limit, cap, default value) that must go into a PRD. Ships a norms library of feature rules, page structures and interaction conventions from mainstream instant-messaging products (loaded by module route), so generated features follow IM conventions by default and convention divergences go to Box for a ruling. It is also the single place that defines the ZYMIX annotation-card writing style, design system and brand-name ban (rules shared across the skills). Not for: full audit and acceptance (box-prd-review), canvas read/write, evidence and verification scripts (box-figma-prd), the HTML dual-panel carrier (dual-panel-prd), generic PRDs unrelated to ZYMIX (product-management:write-spec). Works for users in any language: rules are in English; write the delivery draft in the user's language."
---

# box-prd-create | ZYMIX IM product PRD generation

**What this skill covers**: what to generate (the IM norms library), how to generate it (flow and gates), how to write it (annotation-card style), and what it looks like (layout and design system, see references). `box-figma-prd` covers canvas read/write, evidence and verification; `box-prd-review` covers audit and acceptance. When generating or continuing, load it together with box-figma-prd; on conflict, red lines win.

**Shared rules are defined once, in this skill**: state coverage matrix, IM norms library, Box's six writing rules, copy and symbols, brand-name ban, design-system tokens and component table, no visual specs in annotation-card text. Other skills hold pointers only; on any inconsistency this skill wins, and the difference is logged to the matching skill's to-sync list. Other skills cite this skill by **section name** ("Write gate", "Delivery self-check", etc.), not by step number; the legacy pointer "six steps, step 5 write gate" means the "Write gate" step of this version.

**Figma channel**: always go through the figma-console MCP (Desktop Bridge): reads and writes via `figma_execute`, screenshots via `figma_capture_screenshot`; do not use the official Figma MCP's `use_figma` or similar tools. For connection and read-only discipline see `box-figma-prd`.

**Keep the three layers apart**:

| Layer | Content | Spec source |
|---|---|---|
| Prototype-screen content layer | The UI inside the 402×872 frame | Design-system library → `references/design-system.md`; page-structure conventions → `im-norms/11-ui-structure.md` |
| PRD annotation layer | Title bar, annotation-card shell, badges, connectors | This skill's layout colors (`#00C8B3` / `#18A0FB` / `#F6F8FD` / `#00C3D0`) → `references/canvas-layout.md` |
| Annotation-card text | Requirement text | **No visual specs of any kind**, see below |

## File map (read on demand, never load the whole package)

| When | Read |
|---|---|
| After step 0 framing, per matched feature module | The matching module file under `references/im-norms/` (routes in "IM norms") |
| Drawing prototype-screen content | `references/design-system.md` + `im-norms/11-ui-structure.md` + `im-norms/12-ui-interaction.md` |
| Placing cards, ordering screens, numbering, attaching badges | `references/canvas-layout.md` |
| Making flowcharts and feature lists | `references/figjam.md` |
| After each batch is written, before wrapping up | `references/self-check.md` |
| Rule conflict, or a suspected legacy layout | `references/rulings.md` |
| Needing each product's specific values, original evidence, or explaining competitor practice to Box | Your own research material (the author's Wiki and evidence details are not shipped with the public version; see `references/im-norms/README.md`, "External research material") |
| Writing the draft | `references/draft-template.md` |
| Machine-checking the annotation-card delivery draft | `python3 <skill-dir>/scripts/lint_card_text.py <delivery-draft.md>` (add `--gate` before the write gate) |

`<skill-dir>` is the directory containing this SKILL.md; the agent's working directory is usually not it, so always call scripts by absolute path.

## Generation flow

Nine steps from requirement to canvas (steps 0-8); skipping a step causes rework. Steps 0-6 do not write to the canvas; step 7 is the write gate.

0. **Product framing**: confirm the chat forms the requirement touches (one-on-one chat / group / channel / community), the IM modules, the platforms (iOS / Android / desktop), whether end-to-end encryption applies, and whether strangers can reach the user; also the form-type divergences marked "framing: yes" in matched modules (e.g. whether live location is one-way or multi-person on one map, whether bill splitting goes through bookkeeping or real payment, the group-type system). Do not ask what the PRD and source of truth already state; ask what is missing in one round of multiple-choice questions (one dimension per question, ≤ 4 questions; if there are more than 4 framing dimensions, first ask Box whether to split), and framing questions do not count against the 4 questions of the "Question budget". Also check **feasibility prerequisites** (e.g. wallet and payment qualification, licensed-institution capability, whether third-party services are integrated); unconfirmed ones go to the top as blocking open items, written as `{TBC}`. Based on this, decide which `im-norms` modules to read and which dimensions to mark "not applicable" with a one-line reason.
1. **Lock the source of truth**: record fileKey, normalized nodeId (`123-456` → `123:456`), target zone, protected scope. Tag each requirement `defined` / `to-confirm` / `suggested`. `to-confirm` never lands in card text: if the source of truth is missing (production rules, dev or compliance answers) write `{TBC: what is missing}` and list it under "Open items"; if Box must decide, write `{TBD: topic, recommended: approach}` and list it under "Decisions for Box". Only two kinds of `suggested` may land on a card: norms-library conventions and trade-offs defaulted per recommendation, and they must be listed in "Defaulted to recommendation"; Box's agreement at the write gate counts as adoption. Any other `suggested` does not land on a card.
2. **IM norms check**: read the matched module files. **Baseline** is followed by default; a PRD that deviates must write `Note:` and list it under "Decisions for Box". **Conventions** are adopted per recommendation and listed under "Defaulted to recommendation". **Divergences**: take only those the annotation cards of this requirement will touch, and handle them by the level pre-marked on the entry: `Must-ask` ones are bundled into multiple-choice questions asked to Box once (recommendation first); `Default-OK` ones are written into the card per recommendation and listed. **Must-ask states**: take only the rows relevant to this requirement's objects and merge them into the next step's matrix. Box's rulings for this feature go into the current requirement's STATE or audit file; only rulings on writing style that apply to all PRDs are logged in `references/rulings.md`.
3. **Decide whether external competitor reference is needed**: only when the norms library does not cover it, it is a "new user capability or new main flow", and there is still a factual gap in interaction or state architecture; see "Competitor reference".
4. **List the state coverage matrix**: general dimensions: entry, default, input/selection, client-side validation, server wait, success, post-action failure (main action succeeded but an attached reward, notification or sync failed), recoverable failure, blocked, cancel, back, retry; when relevant add permission, offline, timeout, unknown result, review, freeze; then add the must-ask states of the matched modules (other party blocked / deleted / left the group, multi-device sync, offline recipient, weak network, already forwarded/quoted, group vs one-on-one differences, etc.). Mark each `covered` / `not applicable` / `undefined`; for `undefined`, first judge whether it can be written as body text by convention or recommendation; only what must be answered by the ZYMIX source of truth, dev or compliance goes into the delivery draft's "Open items" (counted merged by answering party, at most 5 groups, e.g. "licensed institution: limits, fees, settlement time" is one group; beyond that the requirement is not ready, so tell Box first). Do not invent requirements just to fill the matrix.
5. **Write the draft before the canvas**: write annotation-card text and the feature list first as a Markdown draft (in the same directory as the STATE or audit file; structure in "Draft structure" below), run `lint_card_text.py` to zero, then walk the matched modules' "Anti-patterns" one by one. With ≥ 6 cards or ≥ 3 matched modules, also run one **reader test**: dispatch a subagent without this session's context to read only the annotation cards of the delivery draft and list the questions a developer would ask while implementing; cross out those the card answers, and add the unanswerable ones to the card or to "Open items" (without subagent capability, read only the delivery draft yourself and list questions card by card from a developer's view). The delivery draft is the only source of canvas text.
6. **Plan screen order and numbering**: fix screen order, row grouping, x step, annotation cards per screen and their numbers, all in one pass (`references/canvas-layout.md`).
7. **Write gate**: the delivery draft must first pass `lint_card_text.py --gate` (`{TBD:}` cleared; `{TBC:}` cleared, or listed one by one in the request block and taken to the canvas with Box's agreement). Submit one write request to Box: target file and zone, list of nodes to create, batch split, whether existing nodes are overwritten, expected further confirmation points. Touch the canvas only after Box explicitly agrees; do not interrupt in batches. When continuing existing work, attach the protected scope.
8. **Place cards and self-check**: after each batch, run the "Delivery self-check" section; proceed to the next batch only when it passes; at the end give the acceptance receipt.

### Question budget

Box's attention is the most expensive resource. Divergences, conventions, undefined states and default values are handled at three levels, and **one round asks at most 4 multiple-choice questions** (the single-call limit of the multiple-choice tool):

| Level | Criterion | Handling |
|---|---|---|
| Must-ask | **The norms-library label governs**: divergences marked `Level: Must-ask`, and clauses in an entry that say "treat as must-ask". At runtime, escalate additionally only in two cases: ④ conflicts with an existing ZYMIX rule or deviates from the baseline; a new topic not covered by the norms library that falls in the five classes below. Definitions of the five classes (for maintaining the norms library and judging new topics): ① privacy defaults, reciprocity rules, what the other party can perceive; ② scope of irreversible handling or data deletion (including whether history is kept/cleared, whether messages are re-delivered after block or unsend, whether local or cloud content is deleted, whether unreported state is discarded); ③ a binary choice that sends the main flow in different directions, without which the card cannot be written, or whose mainstream values differ enormously and directly determine product positioning (e.g. the unsend time limit); ④ conflicts with an existing ZYMIX rule or deviates from the baseline; ⑤ reversibility of regulated fund flows: whether a payment can be undone and funds recovered (return path and timing depend on licensed-institution capability, write `{TBC}`). Values that depend on the licensed institution, regulation or dev capability (limits, launch regions, whether in-transit funds can be frozen) are not for Box to decide: write `{TBC}` into open items, and they do not take a question slot | Ask Box as multiple choice, recommendation first; write `{TBD: topic, recommended: approach}` in the card |
| Default to recommendation | Defaults outside the norms library's "Conventions" and baseline; divergences marked `Level: Default-OK` (even if the content touches visibility or return paths, the label has already passed the five-class judgment, so follow the label); new trade-offs derived from the conflict-ruling gradient that do not fall in the five classes above | Write the recommended option as card body text (no `{TBD}` left); list one line in the delivery draft's "Defaulted to recommendation" (topic: chosen option); it takes effect unless Box changes it; the list counts decision points, at most 8 (several parameters of one decision point merge into one line); beyond that the scope has spread, so move the extra topics to "Suggested follow-ups" and do not let them overflow into the notes |
| Not in this release | Topics the user did not touch and that are not required states of this feature (e.g. backup/restore and old-version compatibility when building a toggle; inviting into groups and blocklist management page when building block) | Do not ask, do not write a card; if needed, list one line under "Suggested follow-ups" at the end of the delivery draft. Topics the norms library marks must-ask for this feature, and required companions of this feature (e.g. cooldown and frequency of an export, renewal reminder of a subscription), must not be put under "Suggested follow-ups" |

**Scope**: cover only topics the user touched, the required states of those topics, and required companion entries (e.g. the blocklist management a block must have, the settings entry a toggle must have); do not expand to adjacent features. Order: privacy and irreversibility > changes to the main flow > the rest. **Labels first**: anything marked or clause-marked "treat as must-ask" is must-ask; the rest follow the entry's level, with no re-judgment against the five classes at runtime (so the same topic gets the same treatment across runs). When the recommendation departs from mainstream practice (e.g. not showing red-packet amounts publicly for privacy), the question text must say "opposite to mainstream practice, a ×× trade-off", not merely "practice varies". More than 4 must-ask questions means the requirement scope is too large: first ask Box whether to split; if Box does not split, ask in rounds of ≤ 4. **Adoption time is uniformly the write gate**: Box agreeing to the write request counts as adopting that round's "Defaulted to recommendation" list. A must-ask must not be rewritten as `{TBC}` or stuffed into "Open items" to get around the question cap. When Box is offline or the run is non-interactive (evals, scheduled tasks), do not wait: write `{TBD: topic, recommended: approach}` placeholders for must-ask items in the card, produce the delivery draft as usual, and stop before the write gate.

### Draft structure

The draft is two files; Box only needs to read the delivery draft. Template in `references/draft-template.md`. **Language**: write card text, copy and the working notes in the user's language; keep the template's `## ` section headings and the `{TBD: …}` / `{TBC: …}` placeholder prefixes in English, because `lint_card_text.py` parses them.

- **Delivery draft** (`<feature>-delivery.md`): annotation cards (by screen, by number), feature list, "Decisions for Box" (≤ 4 multiple-choice questions), "Defaulted to recommendation" list. Cards must be self-sufficient: a developer can implement from the cards alone, and **cards must not contain topic numbers like "Q1", norms-library IDs, or norms-library phrasing like "deviates from convention" or "mainstream products in China"**. Must-ask values not yet ruled are written `{TBD: topic, recommended: approach}` (with the recommendation, so dev and review can see the direction first; distinguish from runtime variables like `{nickname}`); one topic is flagged only once in the whole draft, other cards write "same as FrameName-N"; recommended defaults are written directly as body text. The delivery draft order is fixed: Decisions for Box → Defaulted to recommendation → Open items → Role view summary (if needed) → annotation cards → Feature list → Acceptance checkpoints → Suggested follow-ups, so Box sees what needs a decision first. **Write each value in only one card**: the decisions section, defaults list and feature list state only the topic and cite the card number, without repeating values and copy. When the same group of pre-checks appears on several cards, write the full decision chain only on the first card; the others write "checks same as {FrameName-N}".
- **Size**: a single feature is usually 6-10 cards; when the delivery draft is clearly longer, first check for scope spread and for the same rule expanded across several cards (it should be defined on one card and cited by the others), and do not cut required states to save length.
- **Acceptance checkpoints**: at the end of the delivery draft, write executable acceptance assertions (for testing, not placed on the canvas), only those that cannot be read from a single card: cross-card or cross-role comparisons, timing and multi-device; privacy features must include one "the other party cannot tell the difference" comparison assertion (e.g. the UI is identical when the blocked party sends and when the other party is offline). Do not restate rules a single card already states; at most 12 in total. Feature-list descriptions are a single "trigger - result" sentence plus card number, not restating card copy and values. For features with two or more roles, put a "Role view summary" table before the annotation cards (rows are behavior scenarios, columns are what each role sees).
- **Working notes** (`<feature>-notes.md`): product framing, source-of-truth tagging, norms check, state coverage matrix, self-check log. For review, not for Box to read item by item.

## IM norms

The norms library is at `references/im-norms/` (usage and entry format in its `README.md`). Collected from the clients, open-source code, official docs and protocol specs of mainstream instant-messaging products, version of 2026-10-30.

**Routing**: read the file matching the features the requirement touches; a requirement usually matches 2-4.

| The requirement involves | Read |
|---|---|
| Sign-up, login, verification code, two-step verification, multi-device, account deletion | `01-account-devices.md` |
| Adding friends, stranger messages, block, remove contact, privacy settings | `02-relations-privacy.md` |
| Chat list, pin, mute, archive, unread, delete chat | `03-chat-list.md` |
| Sending, send status, failure retry, read receipts, typing, online status | `04-send-receipts-presence.md` |
| Reply/quote, forward, unsend/delete, edit, multi-select, reactions, pinned messages, favorites | `05-message-actions.md` |
| Images, video, files, voice messages, auto-download | `06-media-files.md` |
| Group itself: roles and permissions, invite to join, @, mute, leave/dissolve; whether to introduce channels/communities/topics (group-type system) | `07-groups-channels.md` |
| Push, mute pass-through, badge count | `08-notifications.md` |
| Encryption, security code, disappearing messages, screenshots, report, risk control | `09-safety-security.md` |
| Search, audio/video calls, storage sync, backup, whether link previews are generated by default, drafts | `10-search-calls-storage.md` |
| Service accounts, bots, card messages, mini-program cards, official verification and system chats | `13-service-bots.md` |
| In-chat transfers, red packets, collecting payment, group collection and bill splitting, in-person verification and limits at payment (the wallet account itself is in 19) | `14-wallet-payments.md` |
| Feed posts, stories; publishing and operating rules of channels, communities, topics | `15-feeds-channels-community.md` |
| Location, live location sharing, contact cards, polls, sticker packs and custom emoji, GIFs, file preview, text formatting (bold, spoiler, etc.), composition of link cards and who fetches them | `16-rich-messages.md` |
| Message translation, auto-translation, translation languages, in-chat AI (summarize, ask AI, rewrite/polish), AI labeling and privacy, AI in groups | `17-translate-ai.md` |
| QR code cards and scanning, face-to-face group creation, people nearby, contact matching, Apple / Google login and binding, system permission guidance | `18-discovery-login-permissions.md` |
| Wallet account opening and identity verification, top-up, withdrawal, card binding/unbinding, transaction details and statements, payment-collection and payment codes, wallet freeze and restriction, closing the wallet | `19-wallet-account.md` |
| Inviting friends to register, invite codes and code entry on the sign-up page, issuing invite rewards (points), anti-abuse and clawback, inviting unregistered contacts, sharing externally and landing pages | `20-invite-growth.md` |
| Minimum age, birthday, age confirmation (age estimation, ID), restrictions on accounts without completed age confirmation, age-restricted content, detecting underage accounts, minor mode and guardians | `21-age-minors.md` |
| Account restriction and ban notices and lift times (wallet freeze is in 19), groups disabled by the platform, appeal entry and result notification, disclosure of penalty reasons, data during a penalty and after a wrongful-ban recovery | `22-enforcement-appeals.md` |
| Ad slots in the chat list, feed ads, channel ads, ad labels, frequency and cooldown, closing and reporting ads, personalized-recommendation toggle, scope of targeting data, ads for minors | `23-ads-personalization.md` |
| Earning points, check-in and behavior tasks, points validity and ledger, points mall redemption, lottery mechanics such as a wheel, points tied to cash, membership activation and benefit display, paywall prompts, auto-renewal and cancellation, downgrade on expiry, membership badges | `24-points-membership.md` |
| Re-consent after terms and privacy-policy updates, consent management and withdrawal, download my data, relation between delete-my-data and account deletion, personal-information access and correction, data-rights request channels, collection list and third-party sharing list, privacy center page | `25-privacy-center.md` |
| Help and contact-support entry, submitting feedback, "My feedback" and support-ticket status, supplementary materials needed, reopening, handling-time commitments, satisfaction, bot-to-human handoff and handler identity; progress display for reports, appeals and wallet disputes | `26-support-tickets.md` |
| Any requirement that draws screens | `11-ui-structure.md`, `12-ui-interaction.md` |
| Closing self-check | `anti-patterns.md` |

**Conflict-ruling gradient** (when rules clash and no ruling record exists, take from top to bottom): Box's ruling this round > existing rulings in `rulings.md` > privacy and data integrity > accessibility and recoverability > the user can understand the current state > consistency with existing ZYMIX features > IM baseline > implementation convenience. A conclusion reached by the gradient is classified by the "Question budget": ask Box if it falls in the five must-ask classes, otherwise list it under "Defaulted to recommendation".

**Three disciplines**:

- The norms library says only "how mainstream does it" and does not decide for ZYMIX. Baselines are followed by default; conventions and default-OK divergences are written per recommendation with a parallel list so Box can change them at a glance; must-ask divergences must be asked; magnitudes only judge whether a value is off the charts, and values are not copied.
- Calibration samples only demonstrate the writing style: values in samples are illustrative, so values are re-set for ZYMIX's business and the norm magnitudes; the lead-in lines before a sample ("this sample has no must-ask items", "values are illustrative") do not enter the delivery draft.
- Norms-library module files contain no brand names, so their wording can be borrowed directly; the brand comparisons under `evidence/` are for review only and none of it enters the canvas.
- When the norms conflict with the ZYMIX source of truth (production measurements, Box's rulings), the source of truth wins, and the difference is recorded under open items for the next review of the norms library.

## No visual specs in card text

**Core rule (Box ruling 2026-09-17): annotation cards describe only behavior and rules; visuals always follow the design file.**

The body text **must not contain**:

- Pixel sizes and coordinates: `width 370`, `height 72`, `40 × 40`, `corner radius 12`, `x = 12`, `y = 220`
- Color values and color tokens: `#F5F6F7`, `B7`, `S7 #0E0E0F 80%`, `A1`
- Font tokens and sizes/line heights: `Noto Sans SC Bold 14/20`, `Body_S_700`, `Caption_S_500（12/16）`
- Contrast values: `9.69:1`, `below 4.5:1`
- Specific aspect ratios and hit-area values of assets: `16:9`, `no less than 44 × 44`

When a visual difference must be expressed, **write the qualitative relation** instead of numbers:

| Do not write | Rewrite as |
|---|---|
| Card slot 370 × 72, corner radius 12, B7 #F5F6F7 background | The card slot is inset from the left and right edges, has rounded corners, and has its own background color |
| Thumbnail 40 × 40, corner radius 8 | The thumbnail is a rounded square, not a circular avatar |
| Badge width: Chinese 32, English 25, Vietnamese 63, Filipino 62 | The badge copy has a different length in each of the four languages; from shortest to longest: English, Simplified Chinese, Filipino, Vietnamese |
| Available title width 226 / 233 / 195 / 196 | The wider the badge, the narrower the available title width; the same ad fits clearly fewer characters in Vietnamese than in English |
| Tap hit area no less than 44 × 44 | The tap hit area must meet the platform accessibility standard |
| Measured contrast 2.28:1, below 4.5:1 | The design system's existing primary-button colors do not meet accessibility contrast |
| Asset uploaded at 16:9 | The asset is uploaded at the aspect ratio specified in the design file |

**Numbers to keep**: these are not visual specs but product constraints, and are written as usual:

- Truncation line counts: e.g. "summary at most 2 lines", "collapse beyond 5 lines" (Box ruling 2026-10-31: line counts are content rules)

- Time: cooldown 24 hours, exposure dwell at least 1 second, animated image 1 to 4 seconds
- Counts: daily exposure cap, minimum interval between two exposures, frame count 5 to 20 frames
- Content: character limits: **those that vary by locale or layout** are written "configured per locale" without a number; **global hard limits** (e.g. nickname at most 32 characters, group name at most 64 characters) are product constraints and are written as usual
- Business thresholds: group-member-count tiers, error-count limits

**Test**: if this number changes, is it a requirement change or a design-file change? If a design-file change, do not write it.

When exact specs are needed, the annotation card says "see design file" or "per the asset spec", and the numbers stay in the design file and the handoff spec. Tokens and color values are used only for **drawing screens** themselves and for verbal handoff to design/dev, and do not go into annotation-card body text.

The same rule applies to the **description column of the FigJam feature list**, which is also explanatory text.

## Card writing rules

For each annotation point, first run the semantic checklist to decide **what to ask**: display/trigger, default, user action, client-side validation, server-side judgment, success result, exceptions and recovery, exact copy, side effects, platform/permission/data/async differences.

**Sentence patterns**

1. The backbone is a key-value short sentence of "condition/object + colon + result" (Chinese copy uses a full-width colon `：`; English copy uses a half-width colon `:`)
2. Decision branches are **exhaustive in pairs**, both positive and negative, none omitted; the last branch states where it goes
3. Button-type cards fix the first two lines: `1. Button becomes enabled once <input condition> is met`, `2. On tap, check in order:`
4. Fallback/degradation gets its own line in the fixed pattern "When no match is found, …"
5. Risk control/rate limiting is written in four segments: `within <time window> <comparator> <count>: <action>, <cooldown duration>, show "<original copy>"`. **Comparators use half-width `>` `<` and U+2264 `≤` / U+2265 `≥`, with one half-width space on each side**
6. Counting rules state the **scope dimension and the conditions that do not reset it**; time-boundary rules (in transit, time limit, effective time) state the **judgment basis**: which timestamp and which side governs (e.g. "messages whose server receipt time ≤ the block effective time are delivered as usual")
7. Reusing an existing rule is not expanded again; write "consistent with … / see …"
8. Supplementary risks, exceptions and design trade-offs go on their own line starting with `Note:`
9. This-release scope and later plans are set side by side on the same card
10. A server-side chain can be compressed to one line with ➡️; but **decision exits must be one per line**
11. Common entry prefixes: `Trigger:` `Entry:` `Exit:` `Default:` `Rule:` `Scope:` `Tap behavior:`. Do not use `Interaction:`
12. **Visual matters get only qualitative relations and constraints, no spec numbers**, see "No visual specs in card text"

**Cross-card rule boundaries must be bounded**: when the same quantity appears on different cards, only one card defines it and the others cite it. Absolute statements ("always a single line", "width adapts") may be written only when they hold in **all forms**; if any form is an exception, either add a qualifier or turn it into a citation. This kind of contradiction is the most frequent in reviews.

**Box's six writing rules** (when they conflict with the sentence patterns above, this section wins)

1. **Define each state's meaning one by one**: for every state in a state machine, first state its meaning in one line, then write the rules.
2. **Tiered rules merge into a single card**: when one feature is tiered by headcount/condition, list the tiers line by line on the same card.
3. **Icon encoding uses a legend strip**: express the shape and color of status icons with a legend strip, not text description lines like "single check = sent".
4. **Fixed skeleton for interaction cards**: `Scope:` → counting basis → `On-demand data fetch:` → `Loading:` → `Load failure:` → data detail → tap destination.
5. **Signaling rules in four segments**: `Trigger` → `Refresh` → `Stop` (list all stop conditions) → `Restart`.
6. **Colloquial short sentences are allowed**: a colloquial short sentence with a single meaning is legitimate. The test is whether a developer can implement it uniquely.

**Decision-chain shape (the only compliant form)**

Only multiple pre-checks escalate into a decision chain: checks are expanded one by one at the `a.` level with an `N-` step prefix, and **each exit takes its own line, including the next step on pass**:

```
Description:
1. Button becomes enabled after a phone number is entered
2. On tap, check in order:
   a. 1-Format check: whether the phone number matches the numbering rules of the selected country
      i. Invalid: inline error "Invalid phone number"
      i. Valid: go to the next check
   a. 2-Validate request legitimacy: whether the number is already registered
      i. Registered: dialog prompting login
      i. Not registered: go to the next step
```

With fewer than 3 checks, no decision chain is needed. **There is no third form**: no `①②③`, no `→`, no merging exits onto the check line.

**A decision chain must include the filter step**: for any feature with a front filter such as cooldown, rate limit, lock or blocklist, the filter must appear explicitly as the first step of the chain; checks that do not depend on the server (permission, local lock, network) come first; filters that need a server decision (rate limit, cooldown, server-side lock state) follow right after network; the remaining server-side checks (object state, balance, eligibility) come last. Otherwise a question like "does the filtered-out one yield to the next-priority one" cannot be implemented uniquely.

**Copy and symbols**

- UI copy, buttons and prompts are always **given verbatim**. In English cards wrap them in straight double quotes "…" (Chinese copy: corner quotes `「」`); `【】` and curly quotes are banned in both
- **No other brand names**, including competitors' product-line names. Exception: Apple and Google may appear as the names of the login methods ZYMIX supports; "consistent with mainstream instant-messaging products" is the approved rewording
- Name the prompt vehicle explicitly: `toast:` `dialog:` `button shows loading state`
- (Chinese copy only) put a half-width space between digits, Latin letters and Chinese characters
- Variable placeholders use half-width `{}`
- Multiple parallel values are separated with `/`
- Cross-zone references use straight double quotes "…" (Chinese copy: `「」`), not `【】`

**Notification template cards** (finished SMS/email copy): no `Description:` prefix, give the finished copy directly. SMS is one line; email uses the three-part skeleton `Email subject:` / `Email body:` / `Foot:`.

## Competitor reference

The norms library is the first reference. Only when the **norms library does not cover** it, the task is a **new user capability or new main flow**, and there is still a factual gap in interaction or state architecture, do external competitor research (2-4 directly comparable mainstream instant-messaging products; research defaults to `product-management:competitive-brief`). Filling in states, fixing copy, deriving tables/flows, and visual cleanup never trigger it.

- **Tag external conclusions `suggested` first**; they upgrade to `defined` only when Box or the current source of truth explicitly adopts them.
- **Do not copy competitors' specific values**: a competitor's character limits, sizes and durations were set under its own layout and business; use them only to judge magnitude.
- Record new research conclusions in the current requirement's STATE or audit file, and in the acceptance receipt remind Box whether to add them to the norms library; updating the norms library is a separate maintenance task (run `lint_skill.py` after changes), not done in passing during generation.

**PRD body text must never contain other brand names**, including competitors' **product-line names**, not just company and app names:

| Do not write | Rewrite as |
|---|---|
| Consistent with Telegram and WhatsApp | Consistent with mainstream instant-messaging products |
| Not adopting the approach of iMessage / Signal | Directly describe the excluded approach itself |
| Following WeChat's handling | Consistent with how mainstream instant-messaging products handle it |

Sources, comparison tables and difference conclusions of competitor research go in the norms library's `evidence/` or a standalone research document, **not onto the PRD canvas**.

## Plugin collaboration

**Plugin output never goes onto the canvas; it is design input only.**

| Stage | Plugin skill |
|---|---|
| Writing up requirements | `product-management:write-spec` |
| Competitor reference (when the norms library does not cover it) | `product-management:competitive-brief` |
| Research synthesis | `product-management:synthesize-research` |
| Option trade-offs | `product-management:product-brainstorming` |
| UI copy | `design:ux-copy` |
| Design-system consistency | `design:design-system` |
| Dev handoff | `design:design-handoff` |

Enable as needed; there is no need to run all of them every time. **Exact visual specs go into the handoff spec produced by design-handoff, not into annotation cards.**

## Design system (for drawing screens)

**Source of truth**: the standalone published library **`<design system library name>`** (libraryKey `<libraryKey>`). It governs only the UI content inside prototype frames; the annotation layer is not constrained, and annotation-card text carries no visual specs. **Before drawing screens, read `references/design-system.md`**: component keys and how to tell the current version, color and font tokens, dark tones, overlay specs. The library has no Figma variables or styles, so draw with literal color values; importing components needs Box's separate authorization. Page-structure conventions (chat-list row composition, chat-page grouping, input-bar show/hide) are in `im-norms/11-ui-structure.md`.

## Prototype frames

Frame 402 × 872, frame names unique and without numbers, laid out in a horizontal row following the flow. **Connector span constraint**: the center-to-center distance between a connector's two end nodes ≤ 2000px; beyond that, re-lay out, split, or add a relay node. The full layout (page skeleton, numbering system, number badges, annotation-card shell and positioning, re-layout after text changes) is in `references/canvas-layout.md`.

## FigJam flowcharts and feature list

Technical flowcharts and the feature list are first built on the FigJam board `<FigJam board fileKey>`, then copied back into the prototype PRD. Shape semantics, colors, connectors, TABLE specs and the three API limits are in `references/figjam.md`. Feature-list descriptions follow "trigger - handling - result - exception", likewise carry no visual specs, and align one by one with the annotation cards.

## Write gate

The full checklist of step 7, submitted to Box in one go; touch the canvas only after explicit agreement:

1. Target file and zone, protected scope (when continuing)
2. List of nodes to create and batch split; whether existing nodes are overwritten
3. The delivery draft has passed `lint_card_text.py --gate`: 0 hits. `{TBD:}` must be cleared; if an external answer for `{TBC:}` has not arrived, list them one by one in the request block (answering party, which card is affected), and after Box agrees they go to the canvas as-is as `{TBC}`, to be filled in when the answer arrives
4. The "Defaulted to recommendation" list is given along with the request, and Box can change it here at the same time
5. Whether component import is needed (needs separate authorization); expected further confirmation points

The reply to Box contains only three things: the decision multiple-choice questions, the key points of the defaults list, and the write-request block; lint results, batch details and self-check go into the working notes; the reply must not contain internal process words such as lint, script names, fileKey or norms-library IDs. The request block must **appear verbatim in the reply** (not only in the working notes), and screen and card counts in it are counted from the delivery draft with commands like `grep -c`, not written from memory. While `{TBD}` remains, the reply gives the decision questions first, and the request block is marked "submit after rulings" and still listed in full. When the decision questions have already been asked with the multiple-choice tool, the reply body does not list them again; without the tool, one line per question (topic + recommendation). In the reply the defaults list gives topic names only, with approaches in the delivery draft; the reply does not restate rules and copy from the delivery draft.

## Delivery self-check

**Veto items** (any hit means do not deliver, fix first):

1. A state machine lacks a terminal state, or a state has an entry but no exit
2. A broken chain: created but cannot be undone, viewed or exited (no unsend/delete note after sending, no leave after joining a group, no way to turn off after turning on)
3. A feature involving messages or chats does not define multi-device consistency, or a feature involving groups does not define the difference from one-on-one chat (when unrelated to this feature, one line of reason in the working notes suffices)
4. Privacy-related defaults undefined (who can see, who can reach, default on or off)
5. Any of offline, retry, timeout undefined and not marked "not applicable"
6. Deviates from the IM baseline without a `Note:`, or a must-ask divergence lands on a card without Box's ruling (conventions and recommendation defaults are not in this category)
7. An annotation card or the feature list contains a brand name or visual specs
8. The same topic is handled contradictorily on two cards; scope words ("no longer", "all", "every") in confirmation dialogs and toasts do not match the actual rules on the scenario cards

The remaining items one by one (structure and layout, design-system compliance, annotation-card text, feature list, IM compliance) are in `references/self-check.md`. The eight items frame size, card width, unique frame names, default layer names, banned symbols, brand names, hand-typed numbering, paired numbering run through box-figma-prd's layout self-check script; the delivery draft runs `lint_card_text.py` (add `--gate` before the write gate); the rest is by hand.

## Rulings

All rulings and deprecated layouts are in `references/rulings.md`, and the skill change log is in `references/HISTORY.md`. On a rule conflict, check rulings first; new writing-style rulings from Box are appended to the end of the table, and the body is updated in the related files. Feature-level rulings (e.g. a feature's time-limit value) do not go into rulings; write them into that requirement's STATE or audit file.
