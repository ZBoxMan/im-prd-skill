#!/usr/bin/env python3
"""技能自身机检。改动本技能任何文件后运行，0 问题才算改完。

检查：引用文件存在；SKILL.md 体量与兄弟技能依赖的章节锚点；规范库三档门槛、ID 唯一、
指针条目与跨模块归属表一致、模块无品牌名、evidence 覆盖；校准样例与 lint 夹具回归。

用法：python3 lint_skill.py   （任意目录运行，自动定位技能根目录）
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

# 兄弟技能（box-figma-prd、box-prd-review、dual-panel-prd）按章节名引用本技能
ANCHORS = ["## 设计系统", "## 生成流程", "## 裁决记录", "## FigJam 流程图与功能清单",
           "## 说明卡正文不写视觉规格", "## 说明卡写作规范", "判断链形态", "## 竞品参照",
           "## 原型帧", "连线跨度约束", "## 写入闸门", "## 交付自检"]
SECTIONS = ["## 基线", "## 惯例", "## 分歧点", "## 必问状态", "## 反模式", "## 校准样例"]
ENTRY = re.compile(r"^- \*\*\[([A-Z]+-D?\d{1,3})\]")
POINTER = re.compile(r"见\s*([A-Z]+-D?\d{1,3})")
WEAK = re.compile(r"仅两家|仅一家|常识|未取证")
MAX_SKILL, MAX_MODULE = 300, 200
MAX_README = 200

problems = []
bad = problems.append
brand_re = brand_pattern(load_brands())
skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

# 1. 引用文件存在
for md in [ROOT / "SKILL.md", *sorted((ROOT / "references").rglob("*.md"))]:
    text = md.read_text(encoding="utf-8")
    for ref in set(re.findall(r"`((?:references/|im-norms/|scripts/)[^`\s]+\.(?:md|py|txt))", text)):
        if not any(c.exists() for c in (ROOT / ref, ROOT / "references" / ref, NORMS / ref)):
            bad(f"{md.relative_to(ROOT)}: 引用的 {ref} 不存在")
    for ref in set(re.findall(r"`(\d{2}-[a-z-]+\.md|anti-patterns\.md)`", text)):
        if not (NORMS / ref).exists():
            bad(f"{md.relative_to(ROOT)}: 引用的规范文件 {ref} 不存在")

# 2. SKILL.md、规范库 README 体量与锚点
rn = len((NORMS / "README.md").read_text(encoding="utf-8").splitlines())
if rn > MAX_README:
    bad(f"im-norms/README.md {rn} 行，超过 {MAX_README}")
n = len(skill.splitlines())
if n > MAX_SKILL:
    bad(f"SKILL.md {n} 行，超过 {MAX_SKILL}")
for a in ANCHORS:
    if a not in skill:
        bad(f"SKILL.md 缺少兄弟技能依赖的锚点「{a}」")

# 3. 规范库模块
entries = {}  # id -> (file, section, line)
for md in sorted(NORMS.glob("[0-9][0-9]-*.md")):
    lines = md.read_text(encoding="utf-8").splitlines()
    if len(lines) > MAX_MODULE:
        bad(f"{md.name}: {len(lines)} 行，超过 {MAX_MODULE}")
    text = "\n".join(lines)
    for s in SECTIONS:
        if s not in text:
            bad(f"{md.name}: 缺少章节 {s}")
    section = ""
    for no, line in enumerate(lines, 1):
        for m in brand_re.finditer(line):
            bad(f"{md.name}:{no}: 模块文件出现品牌名 {m.group(0)!r}")
        if line.startswith("## "):
            section = line
        m = ENTRY.match(line)
        if not m:
            continue
        i = m.group(1)
        if i in entries:
            bad(f"{md.name}:{no}: ID {i} 与 {entries[i][0]} 重复")
        entries[i] = (md.name, section, line)
        body = line.split("：", 1)[-1]
        is_pointer = bool(POINTER.match(body.strip()))
        if is_pointer and re.search(r"推荐|量级|选项", body):
            bad(f"{md.name}:{no}: 指针条目 {i} 不应再带选项、推荐或量级")
        if section.startswith("## 基线"):
            if not re.search(r"置信度[:：]\s*高", line):
                bad(f"{md.name}:{no}: 基线 {i} 置信度必须为高")
            if WEAK.search(line):
                bad(f"{md.name}:{no}: 基线 {i} 含弱证据措辞（仅两家/仅一家/常识/未取证）")
        elif section.startswith("## 惯例"):
            if "置信度" not in line and not is_pointer:
                bad(f"{md.name}:{no}: 惯例 {i} 缺置信度")
            if re.search(r"(?:仅|只有|只)一家|单家|无产品直接取证", line) and not re.search(r"规范|标准|移入必定义|[在已只]在?必定义|必定义里|只作参考", line):
                bad(f"{md.name}:{no}: 惯例 {i} 只有一家证据且无平台规范支撑")
        elif section.startswith("## 分歧点") and not is_pointer:
            if "推荐" not in line:
                bad(f"{md.name}:{no}: 分歧点 {i} 缺推荐项")
            if not re.search(r"级别[:：]\s*(必问|可默认)", line):
                bad(f"{md.name}:{no}: 分歧点 {i} 缺级别标（｜级别：必问 / 可默认）")
    sample = text.split("## 校准样例", 1)[-1]
    # 样例前的说明语是给技能读者的，不属于卡片正文；只检查「说明：」起的卡片部分
    sample = sample[sample.find("说明：") if "说明：" in sample else 0:]
    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as f:
        f.write(sample)
    for no, name, frag, _ in lint(f.name, brand_re):
        bad(f"{md.name}: 校准样例 [{name}] {frag!r}")
    Path(f.name).unlink()
    ev = NORMS / "evidence" / md.name
    if not (NORMS / "evidence").is_dir():
        pass  # 公开版不附 evidence/，跳过证据覆盖检查
    elif not ev.exists():
        bad(f"缺少证据文件 evidence/{md.name}")
    else:
        evtext = ev.read_text(encoding="utf-8")
        for i in re.findall(r"^- \*\*\[([A-Z]+-D?\d{1,3})\]", text, re.M):
            if not re.search(r"(?<![A-Z\d-])" + re.escape(i) + r"(?![\d])", evtext):
                bad(f"evidence/{md.name}: 缺 {i} 的证据行")

anti = NORMS / "anti-patterns.md"
for no, line in enumerate(anti.read_text(encoding="utf-8").splitlines(), 1):
    for m in brand_re.finditer(line):
        bad(f"anti-patterns.md:{no}: 品牌名 {m.group(0)!r}")

# 4. 跨模块概念归属表：非归属条目必须指向归属 ID
own_file = NORMS / "ownership.md"
own = own_file.read_text(encoding="utf-8") if own_file.exists() else \
    (NORMS / "README.md").read_text(encoding="utf-8").split("## 跨模块概念归属表", 1)[-1].split("\n## ", 1)[0]
for row in re.findall(r"^\|([^|\n]+)\|\s*([A-Z]+-D?\d{1,3})\s*\|([^|\n]+)\|", own, re.M):
    concept, owner, others = row[0].strip(), row[1], re.findall(r"[A-Z]+-D?\d{1,3}", row[2])
    if owner not in entries:
        bad(f"归属表「{concept}」: 归属 {owner} 不存在")
    for o in others:
        if o not in entries:
            bad(f"归属表「{concept}」: 条目 {o} 不存在")
        elif f"见 {owner}" not in entries[o][2] and f"见{owner}" not in entries[o][2]:
            bad(f"归属表「{concept}」: {o} 未写「见 {owner}」")

# 5. lint 夹具回归：must-pass 必须 0 命中；must-flag 每条正文行至少命中一次
if lint(FIX / "must-pass.md", brand_re):
    for no, name, frag, _ in lint(FIX / "must-pass.md", brand_re):
        bad(f"fixtures/must-pass.md:{no}: 误报 [{name}] {frag!r}")
flagged = {no for no, *_ in lint(FIX / "must-flag.md", brand_re)}
for no, line in enumerate((FIX / "must-flag.md").read_text(encoding="utf-8").splitlines(), 1):
    if line.strip() and not line.startswith("说明"):
        if no not in flagged:
            bad(f"fixtures/must-flag.md:{no}: 漏报 ← {line.strip()}")

for p in problems:
    print(p)
tiers = {}
for f, sec, _ in entries.values():
    k = sec[3:5]
    tiers[k] = tiers.get(k, 0) + 1
summary = "／".join(f"{k} {v}" for k, v in tiers.items())
print(f"问题 {len(problems)} 处；规范条目 {len(entries)} 条（{summary}）" if problems
      else f"通过；规范条目 {len(entries)} 条（{summary}）")
sys.exit(1 if problems else 0)
