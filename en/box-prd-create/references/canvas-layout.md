# Canvas layout (annotation layer)

> Split out of SKILL.md (2026-10-30). Read before placing cards, arranging screens, numbering, or attaching badges. Annotation-layer specs belong only to the PRD annotation layer and are not used for prototype screen content.

## Contents
- Where to work
- Page skeleton
- Prototype frames
- Numbering system
- Number badges
- Annotation cards
- Unnumbered cards (retired)


## Where to work

- Prototypes, annotation cards, annotations: work directly on the canvas of the target design file.
- **Technical flowcharts and the feature list: build them first on the FigJam whiteboard `<FigJam whiteboard fileKey>`, then copy and paste back into the prototype PRD** (the Plugin API disables TABLE / CONNECTOR / SHAPE_WITH_TEXT in design mode).

## Page skeleton

Zones are arranged top to bottom, with ≥1500px between zones on the y axis. **Basis: bottom edge of the lowest row of prototype frames in the upper zone → top edge of the next zone's level-1 title bar.** The annotation card column is not counted in this basis, but **the card column itself must not intersect the next zone's title bar**: annotation cards are HUG height and grow every time the body changes, so after any rearrangement the top-level AABB check must be run back to zero.

**Level-1 title bar** (one per zone)
- Layer name = the title text itself, no prefix
- FRAME height 92, width covering the whole zone (including the rightmost annotation card column), fill `#00C8B3` at 100% opacity, corner radius 0
- autolayout HORIZONTAL, padding 10/24, gap 10, counterAxisAlign CENTER
- Text Noto Sans SC Medium 48px / lineHeight 71.04 / `#FFFFFF`
- y = the zone's first row of frames y − 186
- Title text uses a short noun

**Level-2 title bar**: same spec, fill opacity 0.4, width covering only the sub-zone.

The purple `#674EFF` title bar is a legacy leftover; change it when seen. The annotation-layer `#00C8B3` is **not** brand color A1.

## Prototype frames

- Uniform size **402 × 872**. Dialogs are 390×356~546 by content; Alert types 300×162~216. 375×812 is a historical leftover
- Frame name: page name/state name; when roles or languages must be distinguished, write `<role or language>-<state>`; **frame names carry no number**
- **Frame names must be unique within one PRD page**
- Laid out in rows, left to right following the flow; different roles/branches start a new row
- x step: 781 for rows with side-attached annotation cards; 462 for pure end-state matrix rows
- **All interface content inside a frame follows the tokens and component instances of the "Design system" section**

**Connector span constraint**: the Euclidean distance between the centers of a connector's two end nodes ≤2000px. Beyond that, nodes must be rearranged, the flow split, or a relay node added.

**Connectors** (in the design file): `#00C3D0`, strokeWeight 4, ELBOWED, start NONE, end ARROW_LINES. Label Inter Medium 16px with no fill; the connector's name is changed to the label text.

## Numbering system

- Badge number = **in-screen sequence number, plain digits, reset per screen**, no zero padding, no zone letter
- Derived annotation cards use dotted second-level numbers `1.1`, `1.2`
- Each number appears exactly twice: once as a badge in the screen + once in the annotation card's label row
- **The feature list does not use F001-style numbers, and group titles do not carry number ranges**
- Cross-screen reference format: `FrameName-in-screen sequence number`

## Number badges

Remote component `Annotate it! – Badge nbl390kvg019lcd6`, key `<badge component key>`, fill `#18A0FB`, cornerRadius 24, height 24. Use the component instance and do not change its internal styles.

- **In-screen placement**: the badge is a child of the container inside the prototype frame, laid over the control being described
- **Card placement**: the badge is the 1st child of the annotation card's label row autolayout

Before attaching an in-screen badge, look up the real parent: coordinates of children inside an artboard are relative to their real parent (often an intermediate Frame rather than the artboard); convert using the `absoluteBoundingBox` difference.

**Do not confuse badges with round numeric badge counts in the UI**: an unread-message badge count is also a blue-fill white-text circle, and appearing on the same screen creates numbering ambiguity.

The badge's `#18A0FB` belongs to the annotation layer and is not counted in the in-screen token compliance scan.

## Annotation cards

**Structure and visuals**

```
Root FRAME  name: <title>  (named by the title alone; scripts identify cards by width 349 + card-body structure)
  VERTICAL, padding 0, itemSpacing 8, width FIXED 349 / height HUG
├─ Label row FRAME  HORIZONTAL, padding 0, itemSpacing 4, HUG/HUG, align CENTER
│    ├─ Badge INSTANCE
│    └─ TEXT title  Noto Sans SC Regular 14px / #18A0FB
└─ Card body FRAME  HORIZONTAL, padding 12, itemSpacing 10, width FIXED 349 / height HUG
     fill #F6F8FD, stroke #DDE4F2 1px INSIDE, cornerRadius 6
     └─ TEXT body  width FILL(325) / height HUG
```

(The above is the spec of the annotation card **shell**, which belongs to the annotation layer. **What to write** inside a card is in "no visual specs in annotation card body".)

Card title = name of the UI element being described, not a sentence.

**One state has only one annotation card.** When the same state appears elsewhere again, move and reuse the card; do not create a second one.

**Body typeface**: the `Description:` section Noto Sans SC Bold 14 / `#666666` (followed immediately by a line break; Chinese copy uses a full-width colon); items Noto Sans SC Regular 14 / `#666666`. `Description:` is the only section heading.

**Lists**
- Use Figma **native ordered lists** (`setRangeListOptions ORDERED` + `setRangeIndentation`), levels fixed as `1.` → `a.` → `i.`
- List numbers are generated automatically by the native list; except for the check-step prefix of decision chains, **hand-typing list numbers is forbidden**

| | Numbering style |
|---|---|
| Correct | The body contains only content; numbering is left to the native list |
| Correct | For multi-step check chains add a hand-typed step prefix at the `a.` level: `1-Format check: …` |
| Wrong | Hand-typing `1.` `2.` `(1)` `①` in the body as list numbers |
| Wrong | Adding a `1-` step prefix at the `1.` or `i.` level (only the `a.` level uses it) |
| Wrong | **Adding an `N-` prefix to parallel enumerations**; the prefix is only for check chains with a fixed order |
| Wrong | Separating items with blank lines or zero-width spaces |

**Card positioning**

```
Side-attached (default)      card.x = frame.x + 417   card.y = frame.y   multiple cards on one screen stack downward, 24 apart
Bottom-attached (end-state matrix)   card.x = frame.x         card.y = frame.y + 900
```

## Unnumbered cards (retired)

**The three kinds of unnumbered cards, "global notes", "scope of this release" and "solution premises", are no longer used.** Their content must be folded into the annotation cards of specific features:

- Technical rules shared across screens (config fetching, caching, offline, rate limiting) → merge into the most relevant scheduling-type feature card
- Out-of-scope items for this release → written as negative sentences in the matching feature card; "not doing X" goes on the card of the feature X belongs to
- Compliance premises and risk arguments → written as `Note:` items on the matching feature card
- Standalone features such as tracking and data reporting → **one separate numbered annotation card**

**Test**: every rule must be traceable to a specific control or a specific check. What cannot be traced is background, not a requirement, and does not go on a card.

This change also cancels the layout object "leftmost unnumbered card column" and its column spacing of 20. **The zone spacing basis is unchanged** (see "Page skeleton"); numbered annotation card columns are still bound by "must not intersect the next zone's title bar", and the delivery self-check's AABB check still runs.

**Always rearrange after a change**: annotation cards are vertically HUG, so changing body text cascades card heights and collides with cards below. After each change, recompute the y of every card in that column (24 spacing within a column) and rerun the top-level AABB intersection check. Treat "edit text → rearrange → AABB back to zero" as one inseparable action.
