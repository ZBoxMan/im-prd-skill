# Draft templates (delivery draft + working notes)

> Used in step 5. Both files go in the same directory as the current requirement's STATE or review dossier. Box reads only the delivery draft; the working notes are for review.

## Delivery draft: `<feature>-delivery.md`

```markdown
# <feature> delivery draft

## Decisions for Box
(At most 4 questions; must-ask level only: divergences the norms library marks "Must-ask", deviations from baseline, conflicts with existing ZYMIX rules; recommended option first. One line for the question stem, one line per option, no background paragraph)
Q1: <topic>
- A (recommended): <approach>. Rationale: <one sentence>
- B: <approach> (<cost, one sentence>)
Card location: <FrameName-N> (do not copy the card's placeholder text again)

## Defaulted to recommendation
(After writing, check line by line: does the norms library entry for this line carry `Level: Must-ask` or "treat as must-ask", or does it conflict with an existing ZYMIX rule? If so, move it to "Decisions for Box"; judge new topics the norms library does not cover by the five categories. Box's agreement at the write gate counts as adoption; one decision point per line, merge multiple parameters of the same decision point; at most 8 lines; never write "N more in the working notes")
- <topic>: <approach adopted> (<FrameName-N>)

## Open items
(Only questions that must be answered by the ZYMIX source of truth, engineering, compliance or a licensed institution, merged by answering party, at most 5 groups; anything that can be written per convention or recommendation does not go here. The matching spot in the card gets `{TBC: what is missing}`. May be empty, but keep the heading)
- <question>: <what information is missing, who can supply it> (<FrameName-N>)

## Role view summary
(Required when two or more roles are involved; otherwise delete this section)
| Scenario | <Role A> sees | <Role B> sees | <Other members> see |
|---|---|---|---|

## <FrameName>

### 1 <name of the UI element being described>
Description:
1. The button lights up after <input condition>
2. On tap, check in order:
   a. 1-<check name>: <what to check>
      i. <case 1>: <result, vehicle + "copy">
      i. <case 2>: proceed to the next check
   a. 2-<check name>: <what to check>
      i. <case>: <result>
      i. <case>: <result/destination>
3. Note: <risks, exceptions>

### 2 <next element>
…

## Feature list
| Feature name | Scope | Description | Platform |
|---|---|---|---|
| <object + behavior/state/rule> | <This release/Later> | <One sentence: trigger — result; details go as "see FrameName-N", do not restate card copy or values; where undecided write "per the card", no more {TBD}> | <iOS/Android/Server> |

## Acceptance checkpoints
(For testing, not placed on the canvas; write only assertions that cannot be read from a single card: cross-card or cross-role comparisons, timing and multi-device, and for privacy features the "the other party cannot tell the difference" comparison assertions (mandatory). Do not restate rules a single card already states; at most 12 items in total)
- <feature name>: precondition <…>; action <…>; expected <…>

## Suggested follow-ups
(Adjacent topics the user did not mention and this release writes no card for; one per line, may be empty. Topics the norms library marks must-ask for this feature, and supporting capabilities this feature requires, must not go here)
- <topic>: <one sentence on why it is worth doing>
```

**Delivery draft rules**

- Fixed order: Decisions for Box → Defaulted to recommendation → Open items → Role view summary (if needed) → annotation cards → Feature list → Acceptance checkpoints → Suggested follow-ups.
- Write the full decision chain only on the first card of a group of identical preconditions; other cards write "checks same as {FrameName-N}" instead of repeating it.
- For steps in a decision chain that need a server verdict (rate limit, dedup, object state, quota), note "returned by server" and state whether a blocked submission counts toward the attempt limit; checks that can be decided on the device (network, required fields, local state) go first.
- Divergences adjacent to this feature that the norms library recommends as "not provided" (e.g. mentions, visibility time window, group lists) merge into one "Not in this release: …" line under "Defaulted to recommendation", so readers can tell deliberate omission from oversight.
- When a default goes beyond the original requirement (widening operation permissions, adding a capability the requirement did not mention), put it in "Decisions for Box" or add a one-sentence rationale on its line in the defaults list; new capabilities outside the requirement go in "Suggested follow-ups", not on a card.
- Write the same value (time limit, count, copy) on one card only; the decisions section, defaults list and feature list carry only the topic and card number.
- The `{TBD}` for one topic appears once in the whole draft, in the card that defines it; other cards write "same as FrameName-N". One item must not contain both the body text of the recommended conclusion and a `{TBD}` for the same topic.
- When another card's rule depends on an undecided question, write the recommended option as definite body text; do not write conditionals like "if Q1 picks A then…" or "once item 2 is settled…"; revise when the ruling changes.
- Each cell of the role view summary states what that role actually sees; do not write "displayed per some card's rule" or "see some card"; for cells that depend on an undecided question, end the sentence with "(per Q2 recommendation)".
- When a card already has a `{TBD}`, do not add a separate "Note: … TBD" line restating it.
- When writing "consistent with current rules" or "carried over from production", cite the source (Wiki page name or Figma node); if no source can be found, write the recommended value plus `{TBC: production value}`; leave no reference without a source.
- After writing the scope words of confirmation dialogs and toasts, check them against every group chat, one-on-one chat and multi-device card; do not over-promise (e.g. "no longer receive messages from this person" while they remain visible in groups).

- Card title = name of the UI element being described; numbers reset per screen and are plain digits; cross-screen references are written `FrameName-N`.
- Cards do not contain topic numbers, norms library IDs, or norms library wording such as "deviates from convention" or "mainstream domestic products"; what needs Box's decision is written `{TBD: topic, recommended: approach}`, missing source of truth is written `{TBC: what is missing}`; both must be cleared before the write gate.
- Runtime variables use placeholders such as `{nickname}` without a "TBD" prefix.
- Write only the topics the user touched and their required states; adjacent features go in "Suggested follow-ups", not on a card.
- After writing, check cross-card consistency card by card: one topic is defined on one card only; scope words (no longer, all, every) in confirmation dialogs and toasts must agree with the rules on each scenario card.
- After writing, run `python3 <skill directory>/scripts/lint_card_text.py <delivery.md>`; run it again with `--gate` before the write gate.
- When explaining background to Box in the decisions section, "mainstream products differ" may be used; do not use skill-internal terms such as norms library, evidence or divergence.

## Working notes: `<feature>-notes.md`

The working notes are a review record, not a second delivery draft: the norms comparison lists only entries this requirement actually used, and the matrix lists only relevant dimensions.

```markdown
# <feature> working notes

## 0 Product framing
Chat form: / Modules hit: / Platforms: / End-to-end encryption: / Strangers reachable:
Dimensions not applicable and why:

## 1 Source of truth
fileKey / nodeId / zone / protected scope
| Requirement item | Defined/To confirm/Suggested | Source |

## 2 Norms comparison
| Norm entry ID | Tier (baseline/convention/divergence) | Handling in this requirement (follow/default per recommendation/must-ask/deviate + reason/not involved) |

## 3 State coverage matrix
| Dimension | Covered/N/A/Undefined | Which card |

## 4 Self-check log
lint results / veto items one by one / anti-patterns one by one
```
