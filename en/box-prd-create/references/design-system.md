# Design system (for drawing screens, public-version template)

> Read only when **drawing prototype-screen content**; do not read when writing annotation cards, whose body text carries no visual specs. The public version contains no design-system values of the author's team; fill in your own library following the structure below.

## Contents
- Source of truth and jurisdiction
- How to use components
- Color tokens
- Font tokens
- Dark tones
- Overlay specs (for drawing screens)

## Source of truth and jurisdiction

**Source of truth**: `<design system library name>` (libraryKey `<libraryKey>`). State whether it is a standalone published library or pages inside the PRD file, and whether the library has Figma variables and styles; without variables, draw with literal color values and do not write `setBoundVariable`.

**Jurisdiction**: only the UI content inside prototype frames. The annotation layer is not constrained, and annotation-card text follows "No visual specs in card text" in SKILL.md.

## How to use components

In a `figma_execute` script, import by key with `importComponentSetByKeyAsync(key)` / `importComponentByKeyAsync(key)`, then `createInstance()`. **Importing components needs separate authorization from the decision-maker**, which is a different matter from Figma write authorization. When the library holds several component sets of the same name, identify the current version by width and variant count, not by timestamp.

| Component | componentKey | Spec |
|---|---|---|
| Chat-list row | `<key>` | `<width×height, variants>` |
| Tab bar (light) | `<key>` | `<width×height, variants>` |
| Tab bar (dark) | `<key>` | `<width×height, variants>` |

When the library has no component of a matching width, draw it yourself and register it here.

## Color tokens

Choose tokens by semantics, not by reverse lookup from color values; tokens with the same value but different semantics are registered separately.

| Token | Color value | Where used |
|---|---|---|
| `<A1>` | `<#RRGGBB>` | `<brand primary color, primary button, selected state>` |

Register known contrast defects (e.g. insufficient text contrast on the primary button) below the table; the PRD side keeps them unchanged but must say so.

## Font tokens

| Token | Font / size / line height / weight | Where used |
|---|---|---|
| `<Body_S_500>` | `<font 14/20 500>` | `<body text>` |

## Dark tones

State where dark-mode values come from (separate tokens, or dark values of same-named tokens); do not derive new tokens for anything undefined.

## Overlay specs (for drawing screens)

One line each for overlays such as toast, inline error, dialog and bottom sheet: which color and font tokens, position and layering. When it conflicts with the token tables, the token tables win, and log it in `rulings.md`.
