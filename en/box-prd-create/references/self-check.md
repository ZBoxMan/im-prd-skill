# Delivery self-check (item by item)

> Split out of SKILL.md (2026-10-30). Run item by item after each batch is written and before wrapping up; veto items are in SKILL.md "Delivery self-check".

## Structure, design system, body text and feature list

The eight items frame size, card width, unique frame names, default layer names, banned symbols, brand names, hand-typed numbering and paired numbers run the layout self-check script of box-figma-prd; design-system compliance inside screens runs the token compliance scan; **everything else is manual**.

**Structure and layout**

- All prototype frames are 402×872, all annotation cards are 349 wide
- Frame names are unique within one PRD page
- Each number inside a screen appears exactly twice
- Each state has only one annotation card
- No default layer names remain on self-built nodes (**default names inside component instances do not count**; when judging, walk up the parent chain to check whether the node is inside an INSTANCE)
- Distance between the centers of a connector's two end nodes ≤2000px
- Top-level AABB intersections are 0, including the annotation card column and the next zone's title bar

**Design-system compliance (content inside prototype frames only)**

- All fills / strokes inside screens fall within the color token table; annotation-layer nodes and badges do not count
- All fontSize / lineHeight / font weights inside screens fall within the font token table
- English and digits use Manrope, Chinese uses Noto Sans SC
- Chat list rows and the tab bar use component instances from the design system library, not hand-drawn
- S-series tokens with "background blur" are given together with the blur value
- M-series tokens are chosen by the "self/other party" perspective
- Dark-background screens use light text, verified by reading the actual fill up the parent chain

**Annotation card body** (run regexes over all annotation cards and the feature list description column)

- No color values `#RRGGBB`
- No color/font token IDs (such as `A1` `B7` `S7` `Body_S_700`)
- No font-size/line-height combinations (such as `14/20`)
- No pixel dimensions (`width 370`, `40 × 40`, `corner radius 12`)
- No coordinates (`x = 12`)
- No contrast values (`9.69:1`)
- No font names (`Noto Sans SC` / `Manrope`)
- Chinese copy uses only `「」`, with no `【】` or curly quotes; English copy uses only straight double quotes "…" and no `【】` or curly quotes
- No other brand names anywhere in the text
- Each card has only one section, `Description:`, and the body is entirely native ordered lists
- The `N-` prefix appears only on check chains with a fixed order
- Decision branches come in pairs and the last branch has a destination; exits one per line
- Prompt copy is verbatim and the vehicle is explicit
- (Chinese copy only) a half-width space between digits/English and Chinese
- Each quantity is defined in one place only, the rest are references

**Feature list**

- No F numbers, no number ranges, no related-screen-number column
- No fully empty rows; write "To confirm" for unknown and "N/A" for irrelevant
- Every independent feature block has a matching row, aligned item by item with the annotation cards

## IM compliance (added 2026-10-30)

- The step 0 framing conclusion is written into the draft or review dossier: chat form, modules hit, platforms, whether encrypted, whether strangers can reach
- Every `im-norms` module that was hit has been read; baseline items checked one by one, and each deviation has a `Note:` and is listed in "Decisions for Box"
- Every must-ask divergence has a Box ruling, or is a `{TBD: topic}` in the card and listed in "Decisions for Box" (≤ 4 questions); conventions and items defaulted to recommendation are listed in "Defaulted to recommendation"; feature-level rulings go into the requirement dossier, not `rulings.md`
- The rows of the module's "Must-ask states" that relate to this requirement's object are each marked `Covered` / `N/A` / `Undefined`; unrelated rows need no reasons
- Every item marked `Covered` in the state matrix can be found under a card number in the delivery draft (the working notes matrix states the card number); after merging or deleting cards to save space, redo this check, and change items marked `Covered` that only say "to be written in the corresponding feature" back to `Undefined` and add the card
- The module's "Anti-patterns" and `im-norms/anti-patterns.md` have been gone through item by item, and hits fixed
- Involved values were compared against the norms library magnitude; values clearly out of range have the business reason explained in a `Note:`
- The delivery draft has been run through `lint_card_text.py` with 0 hits; `--gate` was run before the write gate with 0 hits; each "default list suspected must-ask" hint in the lint output has been confirmed (those in the five must-ask categories move to Decisions for Box)
- Delivery draft and working notes are separate; annotation cards are self-sufficient and contain no topic numbers, norms library IDs or norms library wording
- The "Defaulted to recommendation" list contains no topic the norms library marks must-ask or "treat as must-ask", and no trade-off that conflicts with existing ZYMIX rules; the delivery draft has an "Open items" section
- With ≥ 6 cards or ≥ 3 modules hit, the reader test was done, and questions it could not answer were added as cards or put in Open items
- One topic is defined on one card only; the scope words in confirmation dialogs and toasts agree with each scenario card
- For each question under "Decisions for Box", the recommended option, and for each line of "Defaulted to recommendation", match the corresponding `{TBD: …, recommended: …}` or body value in the card word for word (e.g. the decisions section says "read-only or hidden" while the card says only "read-only" is a mismatch); "cannot tell the difference" style assertions in the recommendation rationale do not contradict the card's actual behavior
- Time-boundary rules state the judging basis; the delivery draft has "Acceptance checkpoints", privacy features include the "the other party cannot tell the difference" comparison assertion; multi-role features have a "Role view summary"
- Whether the step order and defaults given in the original requirement cause downstream problems (e.g. send a friend request first, set the nickname after); if so they have gone to a ruling and are not written as the original says
- After changing this skill, run `scripts/lint_skill.py` and it passes
