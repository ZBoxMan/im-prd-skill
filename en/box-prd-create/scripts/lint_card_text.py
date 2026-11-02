#!/usr/bin/env python3
"""Delivery-draft lint for annotation cards: brand names, visual specs, symbols, leaked norms-library markers.

Usage: python3 lint_card_text.py [--gate] <delivery.md> [more files...]
--gate: run before the write gate; additionally requires no {TBD: …} left in cards (must-ask items decided).
        Each {TBC: …} is listed as a note and must be itemized in the write request.
Exit code: 0 = no hits; 1 = hits.
Code fences and blockquote lines are reported (they would let whole passages skip the checks); their content is still checked.
In the "Decisions for Box", "Defaulted to recommendation", "Open items" and "Suggested follow-ups" sections,
question numbers, tier words and {TBD} are not checked.
Section headings and the {TBD:}/{TBC:} placeholders must stay in English even when the draft body is in another language.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_brands():
    """brand_terms.txt: one per line. A leading = makes the term case-sensitive (avoids false hits on element, line…)."""
    terms = []
    for line in (HERE / "brand_terms.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            terms.append(line)
    return terms


def brand_pattern(terms):
    parts = []
    for t in terms:
        sensitive = t.startswith("=")
        t = t.lstrip("=")
        body = re.escape(t)
        if re.fullmatch(r"[A-Za-z ]+", t):
            body = r"(?<![A-Za-z])" + body + r"(?![A-Za-z])"
        parts.append(body if sensitive else "(?i:" + body + ")")
    return re.compile("|".join(parts))


# Palette tokens look like levels, iterations and priorities (G2, B1, S1, P1): only flag them in a color context
COLOR_TOKEN = r"(?:A[0-6]|B(?:10|[0-9])|C[1-5]|G[1-8]|M(?:1[0-2]|[1-9])|S[1-8]|P[1-4])"
TOKEN_AFTER = r"(?=\s*(?i:colou?r|background|fill|stroke|border|shadow|blur|#|token))"
FONT_TOKEN = r"(?:D_[LMS]_800|H[1-3]_700|Body_[LS]_[5-7]00|Caption_[MS]_[56]00|Micro_[LMS]_[56]00)"
NUM_WORD = r"(?:ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|twenty|thirty|forty|fifty|sixty)"
RULE_PREFIX = (r"ACC|REL|LIST|SEND|ACT|MEDIA|GRP|NOTI|SAFE|MISC|UI|UX|BOT|PAY|FEED|RICH|AI|DISC|WAL|INV|AGE|ENF|ADS|PTS|PRIV|SUP")

CHECKS = [
    ("hex color", re.compile(r"#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b")),
    ("color/font token", re.compile(
        r"(?<![A-Za-z0-9_])" + FONT_TOKEN + r"(?![A-Za-z0-9_])"
        r"|(?i:\b(?:use|uses|using|set to|changed? to|colou?r is|fill is|background is))\s*" + COLOR_TOKEN + r"(?![A-Za-z0-9_])"
        r"|(?<![A-Za-z0-9_])" + COLOR_TOKEN + r"(?![A-Za-z0-9_])" + TOKEN_AFTER)),
    ("font size/line height", re.compile(
        r"(?i:font size|line height|font|weight|style)\D{0,6}([89]|[1-5]\d|60)\s*/\s*(1\d|[2-7]\d|80)(?![\d./}])"
        r"|\(\s*([89]|[1-5]\d|60)\s*/\s*(1\d|[2-7]\d|80)\s*\)")),
    ("pixel size", re.compile(
        r"\d+\s*[×xX*]\s*\d+"
        r"|(?i:\b(?:width|height|size|corner radius|radius|spacing|padding|margin|line height|line spacing|font size|diameter))\s*[:：]?\s*"
        r"(?:\d+(?![\d.])(?!\s*(?i:MB|GB|KB|M\b|G\b|K\b|characters?|chars|items?|people|members|times|messages?|files?|images?|photos?|seconds?|minutes?|hours?|days?))|" + NUM_WORD + r"\b)"
        r"|\d+\s*(?:px|pt|dp)\b|\d+\s*(?i:logical pixels|pixels)")),
    ("aspect ratio", re.compile(r"(?<![\d:：.])(?:16\s*:\s*9|9\s*:\s*16|4\s*:\s*3|3\s*:\s*4|1\s*:\s*1|21\s*:\s*9|3\s*:\s*2|2\s*:\s*3)(?![\d:])")),
    ("opacity", re.compile(r"(?i:opacity|transparency)\s*[:：]?\s*\d+\s*%|\d+\s*%\s*(?i:opacity|transparency)")),
    ("animation duration/curve", re.compile(
        r"\d+\s*ms\b|\d+\s*(?i:milliseconds?)"
        r"|(?i:animation|transition|motion).{0,16}\d+(?:\.\d+)?\s*(?i:s|sec|secs|seconds?)\b"
        r"|(?i:ease-in-out|ease-in|ease-out|cubic-bezier|bezier)")),
    ("shadow/blur", re.compile(r"(?i:blur|shadow)\s*[:：]?\s*\d+")),
    ("hit area value", re.compile(
        r"(?i:hit area|touch target|tap target|tap area).{0,16}(?:\d+|\b" + NUM_WORD + r"[- ]?\w*\s*(?i:pt|dp|px|points?))")),
    ("coordinates", re.compile(r"(?<![A-Za-z])[xy]\s*=\s*-?\d+")),
    ("contrast ratio", re.compile(r"\d+\.\d+\s*:\s*1(?!\d)|(?i:contrast)\D{0,6}\d+(?:\.\d+)?\s*:\s*1(?!\d)")),
    ("font name/weight", re.compile(
        r"Noto Sans|Manrope|SF Pro|PingFang|Inter (?:Medium|Regular|Bold)|(?i:font weight)"
        r"|(?<![A-Za-z])(?i:extrabold|semibold)(?![A-Za-z])|(?<![A-Za-z])(?:Bold|Medium|Regular)(?![A-Za-z])"
        r"|(?i:font size)\s+" + NUM_WORD + r"\b")),
    ("color description", re.compile(
        r"(?i:\b(?:green|red(?!\s*(?:packets?|envelopes?|dots?)\b)|blue|yellow|orange|purple|gr[ae]y(?!(?:ed)?\s*out)|black|white)\b"
        r"|\b(?:primary|theme|brand|accent)\s+colou?r|\bbrightens?\b|\b(?:primary|secondary)\s+style)")),
    ("banned brackets/quotes", re.compile(r"[【】“”『』＂]")),
    ("full-width comparator", re.compile(r"[＞＜≧≦]")),
    ("comparator spacing", re.compile(r"(?<! )[≤≥]|[≤≥](?! )|(?<=\d)[<>]|[<>](?=\d)")),
    ("circled number or arrow", re.compile(r"[①-⓿❶-➓㉑-㉟㊱-㊿→]")),
    ("zero-width character", re.compile(r"[​‌‍﻿]")),
    ("| inside placeholder", re.compile(r"\{[^}]*\|[^}]*\}")),
    ("list marker", re.compile(r"^\s*(?:[b-h]|ii|iii|iv|v|vi|vii)\.\s|^\s*a\.\s*\d+-\s")),
    ("old check style", re.compile(r"(?i:\bcheck\s*\d+\s*[:：])|判断\s*\d+\s*[:：]")),
    ("\"Interaction:\" section", re.compile(r"^\s*(?:\d+\.\s*)?(?i:interactions?)\s*[:：]")),
    ("norms rule ID", re.compile(r"(?<![A-Za-z])(?i:(?:" + RULE_PREFIX + r")-?D?)\d{1,3}(?!\d)")),
    ("pending-ruling leftover", re.compile(r"(?i:pending\s+Box|awaiting\s+(?:Box|ruling)|to be decided by Box|fill in after (?:the )?ruling)")),
    ("split brand name", re.compile(r"(?i:We\s+Chat|Tele\s+gram|Whats\s+App)|微\s+信|电\s+报")),
    ("ruling question in card", re.compile(r"(?<![A-Za-z])Q\d{1,2}(?!\d)(?!\s*(?i:iteration|quarter|launch|release|roadmap|planning))")),
    ("sample wording", re.compile(r"(?i:\billustrative\b|for illustration only|\btentative\b|values? for reference only|no must-ask items in this example)")),
    ("norms wording in card", re.compile(r"(?i:deviat\w*\s+from\s+(?:the\s+)?(?:convention|baseline)|mainstream domestic products|domestic mainstream products|mainstream products in China|privacy-first products|\bone product\b)")),
    ("internal term", re.compile(r"(?i:norms library|\bevidenced\b|little evidence|surveyed products|norms magnitude|baseline rule|convention tier|\bdivergences?\b|\bevidence\b)")),
]

# Only the four template headings count as decision sections, so a card titled "### 3 Open items hint" is not mistaken for one
DECISION_HEADING = re.compile(r"^##\s*(Decisions for Box|Defaulted to recommendation|Open items|Suggested follow-ups)\s*$", re.I)
SKIP_IN_DECISION = {"ruling question in card", "norms wording in card", "must-ask undecided", "pending-ruling leftover"}

GATE_CHECKS = [("must-ask undecided", re.compile(r"\{TBD:[^}]*\}"))]
GATE_NOTE = re.compile(r"\{TBC:[^}]*\}")  # note only before the gate: itemize in the write request and get Box's consent

# Words in "Defaulted to recommendation" that often mean a privacy, data-handling or money must-ask got downgraded: note only
DEFAULT_SUSPECT = re.compile(
    r"(?i:\bother (?:party|person|user|side)|\bothers\b|\bvisible\b|can(?:not|'t) see|\bsees?\b|\bretain|\bdelet|\bclear|\brefund|\breissu|\bresend"
    r"|\bdiscard|on by default|off by default|default on|default off|claim record|\bamount)")
DEFAULT_HEADING = re.compile(r"^##\s*Defaulted to recommendation\s*$", re.I)


def default_warnings(path):
    out = []
    in_default = False
    for no, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("## "):
            in_default = bool(DEFAULT_HEADING.match(line))
            continue
        if in_default and line.strip().startswith("-"):
            m = DEFAULT_SUSPECT.search(line)
            if m:
                out.append((no, m.group(0), line))
    return out


def lint(path, brand_re, gate=False):
    hits = []
    in_decision = False
    for no, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("#"):
            in_decision = bool(DECISION_HEADING.match(line))
        fence = line.strip().startswith(("```", "~~~"))
        if fence or line.lstrip().startswith(">"):
            hits.append((no, "code fence or blockquote", line.strip()[:3], line))
            if fence:
                continue
        for m in brand_re.finditer(line):
            hits.append((no, "brand name", m.group(0), line))
        for name, rx in CHECKS + (GATE_CHECKS if gate else []):
            if in_decision and name in SKIP_IN_DECISION:
                continue
            for m in rx.finditer(line):
                if m.group(0):
                    hits.append((no, name, m.group(0), line))
    return hits


def section(text, heading):
    parts = re.split(r"^## " + heading + r"\s*$", text, maxsplit=1, flags=re.M | re.I)
    return parts[1].split("\n## ", 1)[0] if len(parts) > 1 else None


def main(argv):
    if len([a for a in argv[1:] if a != "--gate"]) < 1:
        print(__doc__)
        return 2
    gate = "--gate" in argv
    files = [a for a in argv[1:] if a != "--gate"]
    brand_re = brand_pattern(load_brands())
    total = 0
    for p in files:
        hits = lint(p, brand_re, gate)
        total += len(hits)
        for no, name, frag, line in hits:
            print(f"{p}:{no}: [{name}] {frag!r}  ← {line.strip()[:80]}")
        text = Path(p).read_text(encoding="utf-8")
        if gate:
            for no, line in enumerate(text.splitlines(), 1):
                for m in GATE_NOTE.finditer(line):
                    print(f"{p}:{no}: note (not a hit) [TBC open] {m.group(0)!r}; itemize it in the write request with who answers and which cards it affects")
        accept = section(text, "Acceptance checkpoints")
        n_accept = len(re.findall(r"^\s*- ", accept, re.M)) if accept else 0
        if n_accept > 12:
            print(f"{p}: note (not a hit) [{n_accept} acceptance checkpoints > 12] keep only cross-card, cross-role, timing/multi-device and privacy contrast assertions")
        body = re.split(r"^## (?:Defaulted to recommendation|Open items)\s*$", text, maxsplit=1, flags=re.M | re.I)[-1]
        topics = [x.strip() for x in re.findall(r"\{TBD:\s*([^,，}]+)", body)]
        for topic in sorted({x for x in topics if topics.count(x) > 1}):
            print(f"{p}: note (not a hit) [{{TBD}} repeated {topics.count(topic)} times] \"{topic}\" belongs only on its defining card; elsewhere write \"same as FrameName-N\"")
        flist = section(text, "Feature list")
        if flist and "{TBD" in flist:
            print(f"{p}: note (not a hit) [{{TBD}} in feature list] write \"per the card\" for undecided items")
        for no, frag, line in default_warnings(p):
            print(f"{p}:{no}: note (not a hit) [default list may hide a must-ask] {frag!r}  ← {line.strip()[:80]}; check the norms entry: Level: Must-ask or \"treat as must-ask\" moves to Decisions for Box, Default-OK stays")
    print(f"{total} hits" if total else "Pass: 0 hits")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
