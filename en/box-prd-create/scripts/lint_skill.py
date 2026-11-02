#!/usr/bin/env python3
"""Self-check for this skill. Run after changing any file in it; done only at 0 problems.

Checks: referenced files exist; SKILL.md size and the section anchors sibling skills rely on; norms-library tier
requirements, unique IDs, pointer entries consistent with the ownership table, no brand names in modules,
calibration samples and lint fixture regression.

Usage: python3 lint_skill.py   (run from any directory; locates the skill root itself)
"""
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NORMS = ROOT / "references" / "im-norms"
FIX = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint_card_text import brand_pattern, lint, load_brands  # noqa: E402

# Sibling skills (box-figma-prd, box-prd-review, dual-panel-prd) reference this skill by section name
ANCHORS = ["## Design system", "## Generation flow", "## Rulings", "## FigJam flowcharts and feature list",
           "## No visual specs in card text", "## Card writing rules", "Decision-chain shape", "## Competitor reference",
           "## Prototype frames", "Connector span constraint", "## Write gate", "## Delivery self-check"]
SECTIONS = ["## Baseline", "## Conventions", "## Divergences", "## Must-ask states", "## Anti-patterns", "## Calibration sample"]
ENTRY = re.compile(r"^- \*\*\[([A-Z]+-D?\d{1,3})\]")
POINTER = re.compile(r"See\s*([A-Z]+-D?\d{1,3})")
WEAK = re.compile(r"(?i:only two products|only one product|common sense|not evidenced)")
MAX_SKILL, MAX_MODULE = 300, 200
MAX_README = 200

problems = []
bad = problems.append
brand_re = brand_pattern(load_brands())
skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

# 1. Referenced files exist
for md in [ROOT / "SKILL.md", *sorted((ROOT / "references").rglob("*.md"))]:
    text = md.read_text(encoding="utf-8")
    for ref in set(re.findall(r"`((?:references/|im-norms/|scripts/)[^`\s]+\.(?:md|py|txt))", text)):
        if not any(c.exists() for c in (ROOT / ref, ROOT / "references" / ref, NORMS / ref)):
            bad(f"{md.relative_to(ROOT)}: referenced {ref} does not exist")
    for ref in set(re.findall(r"`(\d{2}-[a-z-]+\.md|anti-patterns\.md)`", text)):
        if not (NORMS / ref).exists():
            bad(f"{md.relative_to(ROOT)}: referenced norms file {ref} does not exist")

# 2. SKILL.md and norms README size and anchors
rn = len((NORMS / "README.md").read_text(encoding="utf-8").splitlines())
if rn > MAX_README:
    bad(f"im-norms/README.md has {rn} lines, over {MAX_README}")
n = len(skill.splitlines())
if n > MAX_SKILL:
    bad(f"SKILL.md has {n} lines, over {MAX_SKILL}")
for a in ANCHORS:
    if a not in skill:
        bad(f"SKILL.md lacks the anchor \"{a}\" that sibling skills rely on")

# 3. Norms modules
entries = {}  # id -> (file, section, line)
for md in sorted(NORMS.glob("[0-9][0-9]-*.md")):
    lines = md.read_text(encoding="utf-8").splitlines()
    if len(lines) > MAX_MODULE:
        bad(f"{md.name}: {len(lines)} lines, over {MAX_MODULE}")
    text = "\n".join(lines)
    for s in SECTIONS:
        if s not in text:
            bad(f"{md.name}: missing section {s}")
    section = ""
    for no, line in enumerate(lines, 1):
        for m in brand_re.finditer(line):
            bad(f"{md.name}:{no}: brand name in module file {m.group(0)!r}")
        if line.startswith("## "):
            section = line
        m = ENTRY.match(line)
        if not m:
            continue
        i = m.group(1)
        if i in entries:
            bad(f"{md.name}:{no}: ID {i} duplicates {entries[i][0]}")
        entries[i] = (md.name, section, line)
        body = line.split("**:", 1)[-1] if "**:" in line else line.split(":", 1)[-1]
        is_pointer = bool(POINTER.match(body.strip()))
        if is_pointer and re.search(r"Recommended|Magnitude|Option [A-D]", body):
            bad(f"{md.name}:{no}: pointer entry {i} must not carry options, a recommendation or magnitude")
        if section.startswith("## Baseline"):
            if not re.search(r"Confidence:\s*High", line):
                bad(f"{md.name}:{no}: baseline {i} must have Confidence: High")
            if WEAK.search(line):
                bad(f"{md.name}:{no}: baseline {i} uses weak-evidence wording")
        elif section.startswith("## Conventions"):
            if "Confidence" not in line and not is_pointer:
                bad(f"{md.name}:{no}: convention {i} lacks Confidence")
            if re.search(r"(?i:only one product|a single product|no direct product evidence)", line) and \
                    not re.search(r"(?i:guideline|standard|spec|must define|reference only)", line):
                bad(f"{md.name}:{no}: convention {i} rests on one product without platform-guideline support")
        elif section.startswith("## Divergences") and not is_pointer:
            if "Recommended" not in line:
                bad(f"{md.name}:{no}: divergence {i} lacks a recommendation")
            if not re.search(r"Level:\s*(Must-ask|Default-OK)", line):
                bad(f"{md.name}:{no}: divergence {i} lacks a level tag (| Level: Must-ask / Default-OK)")
    sample = text.split("## Calibration sample", 1)[-1]
    # The lead-in before the sample is for skill readers, not card text; only check from "Description:" on
    sample = sample[sample.find("Description:") if "Description:" in sample else 0:]
    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as f:
        f.write(sample)
    for no, name, frag, _ in lint(f.name, brand_re):
        bad(f"{md.name}: calibration sample [{name}] {frag!r}")
    Path(f.name).unlink()

anti = NORMS / "anti-patterns.md"
for no, line in enumerate(anti.read_text(encoding="utf-8").splitlines(), 1):
    for m in brand_re.finditer(line):
        bad(f"anti-patterns.md:{no}: brand name {m.group(0)!r}")

# 4. Cross-module ownership table: non-owner entries must point to the owner ID
own = (NORMS / "ownership.md").read_text(encoding="utf-8")
for row in re.findall(r"^\|([^|\n]+)\|\s*([A-Z]+-D?\d{1,3})\s*\|([^|\n]+)\|", own, re.M):
    concept, owner, others = row[0].strip(), row[1], re.findall(r"[A-Z]+-D?\d{1,3}", row[2])
    if owner not in entries:
        bad(f"ownership \"{concept}\": owner {owner} does not exist")
    for o in others:
        if o not in entries:
            bad(f"ownership \"{concept}\": entry {o} does not exist")
        elif not re.search(r"(?i:see)\s*" + re.escape(owner) + r"(?!\d)", entries[o][2]):
            bad(f"ownership \"{concept}\": {o} does not say \"see {owner}\"")

# 5. Lint fixture regression: must-pass has 0 hits; every body line of must-flag hits at least once
for no, name, frag, _ in lint(FIX / "must-pass.md", brand_re):
    bad(f"fixtures/must-pass.md:{no}: false positive [{name}] {frag!r}")
flagged = {no for no, *_ in lint(FIX / "must-flag.md", brand_re)}
for no, line in enumerate((FIX / "must-flag.md").read_text(encoding="utf-8").splitlines(), 1):
    if line.strip() and not line.startswith("Description"):
        if no not in flagged:
            bad(f"fixtures/must-flag.md:{no}: missed ← {line.strip()}")

for p in problems:
    print(p)
tiers = {}
for f, sec, _ in entries.values():
    k = sec[3:].split(" ", 1)[0]
    tiers[k] = tiers.get(k, 0) + 1
summary = " / ".join(f"{k} {v}" for k, v in tiers.items())
print(f"{len(problems)} problems; {len(entries)} norms entries ({summary})" if problems
      else f"Pass; {len(entries)} norms entries ({summary})")
sys.exit(1 if problems else 0)
