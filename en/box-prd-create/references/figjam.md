# FigJam flowcharts and feature list

> Split out of SKILL.md (2026-10-30). Read before making technical flowcharts or the feature list. The description column likewise carries no visual specs.


Build on the whiteboard `<FigJam whiteboard fileKey>`:

- **One SECTION per flowchart**, fill `#FFFFFF`, stroke `#E6E6E6`, named `<module>-<sub-flow>`. The feature list TABLE and the source-of-truth statement TEXT sit at page level
- **Page-level TEXT source-of-truth statement** (Inter Medium 24px), four lines: `Sole source of truth` / `Scope` / `Boundary` / `Derived artifacts`
- Shape semantics: ordinary step ROUNDED_RECTANGLE 320×96 white fill + stroke `#757575` 4px; decision DIAMOND 360×160; failure/blocked `#FFCDC2`; success end state `#CDF4D3`; **degraded end state (collapse, not delivered, silent failure) `#FFE0C2`**; rule/boundary block `#EDEDED`. Text Inter Medium 16px
- Flowchart colors are FigJam working colors, not bound by design system tokens
- Connectors: `#757575`, strokeWeight 4, ELBOWED, NONE→ARROW_LINES, **branch conditions go on the connector's own text**
- **A connector's text.fontName is empty by default; assign fontName before writing characters**, otherwise it errors `Font family "" is not available`
- **Each connection point of each node takes at most one connector**: when several connectors enter the same node use different connection points, or add an explicit merge node
- **Every non-end node must have an outgoing connector**: a white-fill step node with only incoming connectors is a dangling end point. Loop-backs must connect explicitly back to the decision node and be labeled "re-evaluate"
- Rule blocks (`#EDEDED`) without connectors are allowed and do not count as isolated nodes
- STICKY notes are not used
- **The feature list uses a native TABLE**: header row fill `#1E1E1E` white text Inter Medium 16px; group rows fully colored with white text (`#874FFF` `#3DADFF` `#66D575` `#FF9E42`, cycling by group); content rows white fill black text. Columns are generally Feature name / Scope / Description / Platform. **No "number" column and no "related screen number" column**. Feature name is written as "object + behavior/state/rule", description as "trigger — handling — result — exception". No fully empty rows; write "To confirm" for unknown and "N/A" for irrelevant
- **The description column likewise carries no visual specs**: it is explanatory text, and all the rules of "no visual specs in annotation card body" apply
- **The feature list must align item by item with the annotation cards**: every independent feature block in the cards needs a matching row. In practice the four most often missed are asset specs, disclosure-type components, server-side validation, and rate limiting with config fetching
- When done, copy and paste the whole thing back into the matching zone of the prototype PRD

**Three API limitations**
- TABLE column widths are read-only, and TABLE **has no `resize` method**. `createTable` defaults to 4 columns at 768 total width, which stretches the description column very tall; it can only be widened by hand in the UI. Plan the column count once, up front
- TABLE, CONNECTOR and SHAPE_WITH_TEXT are disabled in design mode; copying back into the prototype PRD can only be done manually in the UI with Cmd+C / Cmd+V
- To read FigJam structure use a read-only `figma_execute` script (the bridge plugin runs on the FigJam side), or `figjam_get_board_contents` / `figjam_get_connections`
