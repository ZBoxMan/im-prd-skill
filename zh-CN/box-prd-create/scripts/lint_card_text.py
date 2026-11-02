#!/usr/bin/env python3
"""说明卡交付稿机检：品牌名、视觉规格、符号与空格、规范库内部标记泄漏。

用法：python3 lint_card_text.py [--gate] <交付稿.md> [更多文件...]
--gate：写入闸门前使用，额外要求卡内不存在 {待定：…}（必问已裁决）；{待查：…} 逐条提示，须在写入申请块列出。
退出码：0 = 无命中；1 = 有命中。
交付稿里不该有代码块与引用行，出现即报（避免整段绕过检查），其内容照常检查。
「待 Box 裁决」「已按推荐默认」「未决」「建议后续」小节里不查议题编号、分类词与 {待定}。
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CJK = r"一-鿿"


def load_brands():
    """brand_terms.txt：一行一个。前缀 = 表示大小写敏感（防止 element、line 一类普通词误报）。"""
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


# 色板 token 与等级名、迭代号、优先级同形（G2、B1、S1、P1），只在用色语境下报：前接「使用/采用/改为/颜色为」等或后接颜色词
COLOR_TOKEN = r"(?:A[0-6]|B(?:10|[0-9])|C[1-5]|G[1-8]|M(?:1[0-2]|[1-9])|S[1-8]|P[1-4])"
TOKEN_AFTER = r"(?=\s*(?:色|底|填充|描边|阴影|投影|模糊|#|token))"
FONT_TOKEN = r"(?:D_[LMS]_800|H[1-3]_700|Body_[LS]_[5-7]00|Caption_[MS]_[56]00|Micro_[LMS]_[56]00)"
UNIT_AFTER = r"(?!\s*[页起次天日月年号人条个张份届期])"

CHECKS = [
    ("色值", re.compile(r"#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b")),
    ("颜色/字体 token", re.compile(
        r"(?<![A-Za-z0-9_])" + FONT_TOKEN + r"(?![A-Za-z0-9_])"
        r"|(?:使用|采用|改为|色值为|颜色为|填充为|底色为)\s*" + COLOR_TOKEN + r"(?![A-Za-z0-9_])"
        r"|(?<![A-Za-z0-9_])" + COLOR_TOKEN + r"(?![A-Za-z0-9_])" + TOKEN_AFTER)),
    ("字号行高", re.compile(
        r"(?:字号|行高|字体|字重|样式)\D{0,6}([89]|[1-5]\d|60)\s*/\s*(1\d|[2-7]\d|80)(?![\d./}])"
        r"|[（(]\s*([89]|[1-5]\d|60)\s*/\s*(1\d|[2-7]\d|80)\s*[）)]")),
    ("像素尺寸", re.compile(
        r"\d+\s*[×xX*]\s*\d+"
        r"|(?<![最提升增加较])(?:宽度?|高度?|尺寸|大小|圆角|间距|边距|内边距|外边距|行高|行距|字号|直径)\s*[:：]?\s*(?:\d+(?![\d.])(?!\s*(?:MB|GB|KB|M\b|G\b|K\b|兆|字|个|人|条|次))|[一二三四五六七八九十]+)"
        r"|\d+\s*(?:px|pt|dp)\b|\d+\s*(?:逻辑像素|像素)")),
    ("宽高比", re.compile(r"(?<![\d:：.])(?:16\s*[:：]\s*9|9\s*[:：]\s*16|4\s*[:：]\s*3|3\s*[:：]\s*4|1\s*[:：]\s*1|21\s*[:：]\s*9|3\s*[:：]\s*2|2\s*[:：]\s*3)(?![\d:：])")),
    ("透明度", re.compile(r"透明度\s*[:：]?\s*\d+\s*%")),
    ("动效时长/曲线", re.compile(r"\d+\s*(?:ms|毫秒)\b|\d+\s*毫秒|(?:动画|动效|过渡|转场).{0,8}\d+(?:\.\d+)?\s*秒|(?i:ease-in-out|ease-in|ease-out|cubic-bezier|贝塞尔)")),
    ("阴影模糊", re.compile(r"(?i:blur|阴影|投影)\s*[:：]?\s*\d+")),
    ("热区数值", re.compile(r"(?:热区|触控区|点击区域).{0,6}(?:\d+|[一二三四五六七八九十百]+\s*(?:pt|dp|px|点))")),
    ("坐标", re.compile(r"(?<![A-Za-z])[xy]\s*=\s*-?\d+")),
    ("对比度数值", re.compile(r"\d+\.\d+\s*:\s*1(?!\d)|对比度\D{0,4}\d+(?:\.\d+)?\s*:\s*1(?!\d)")),
    ("字体名/字重", re.compile(
        r"Noto Sans|Manrope|SF Pro|PingFang|Inter (?:Medium|Regular|Bold)|字重"
        r"|(?<![A-Za-z])(?i:extrabold|semibold)(?![A-Za-z])|(?<![A-Za-z])(?:Bold|Medium|Regular)(?![A-Za-z])|字号\s*[一二三四五六七八九十]")),
    ("颜色描述", re.compile(r"(?:绿|红|蓝|黄|橙|紫|灰|黑|白)色|主色|主题色|品牌色|品牌[红蓝绿黄紫]|变亮|(?i:primary|secondary)\s*样式")),
    ("禁用括号/引号", re.compile(r"[【】“”‘’『』\"＂]")),
    ("全角比较符", re.compile(r"[＞＜≧≦]")),
    ("比较符两侧缺空格", re.compile(r"(?<! )[≤≥]|[≤≥](?! )|(?<=[\d" + CJK + r"])[<>]|[<>](?=[\d" + CJK + r"])")),
    ("圈号或箭头", re.compile(r"[①-⓿❶-➓㉑-㉟㊱-㊿→]")),
    ("零宽字符", re.compile(r"[​‌‍﻿]")),
    ("占位多值用 |", re.compile(r"\{[^}]*\|[^}]*\}")),
    ("中文与数字/英文/占位间缺空格", re.compile(
        r"[" + CJK + r"][A-Za-z0-9{]|[A-Za-z0-9}][" + CJK + r"]")),
    ("列表标记", re.compile(r"^\s*(?:[b-h]|ii|iii|iv|v|vi|vii)\.\s|^\s*a\.\s*\d+-\s")),
    ("旧判断写法", re.compile(r"判断\s*\d+\s*[:：]")),
    ("「交互：」分节", re.compile(r"^\s*(?:\d+\.\s*)?交互\s*[:：]")),
    ("规范库 ID", re.compile(r"(?<![A-Za-z])(?i:(?:ACC|REL|LIST|SEND|ACT|MEDIA|GRP|NOTI|SAFE|MISC|UI|UX)-?D?)\d{1,3}(?!\d)")),
    ("卡内待裁决残留", re.compile(r"待\s*Box|待裁决|裁决后补")),
    ("品牌名拆写", re.compile(r"微\s+信|电\s+报")),
    ("卡内裁决占位", re.compile(r"(?<![A-Za-z])Q\d{1,2}(?!\d)(?!\s*(?:迭代|季度|上线|版本|发布|规划))|待\s*Box\s*裁决\s*Q")),
    ("样例说明语", re.compile(r"数值为示意|本例没有必问项|示意值|暂定值|为暂定|仅供示意|数值仅供参考")),
    ("规范库措辞进卡", re.compile(r"偏离.{0,12}(?:惯例|基线)|国内主流产品|隐私优先类产品|一家产品")),
    ("内部术语", re.compile(r"规范库|已取证|有取证|未取证|取证较少|已调研产品|规范量级|基线规则|惯例档|分歧点|evidence")),
]

# 只认模板里的四个二级标题，避免「### 3 未决消息提示」这类卡标题被误当成决策区
DECISION_HEADING = re.compile(r"^##\s*(待\s*Box\s*裁决|已按推荐默认|未决项|建议后续)\s*$")
SKIP_IN_DECISION = {"卡内裁决占位", "规范库措辞进卡", "必问未裁决", "卡内待裁决残留", "待查未补"}


GATE_CHECKS = [("必问未裁决", re.compile(r"\{待定[:：][^}]*\}"))]
GATE_NOTE = re.compile(r"\{待查[:：][^}]*\}")  # 闸门前只提示：须在写入申请块逐条列出并经 Box 同意


# 「已按推荐默认」里出现这些词时，很可能是隐私、数据处置或资金类必问被降级：只提示，不计入命中
DEFAULT_SUSPECT = re.compile(r"对方|他人|可见|看不到|看到|保留|删除|清除|退回|补发|不补|丢弃|默认开|默认关|默认开启|默认关闭|领取记录|金额")
DEFAULT_HEADING = re.compile(r"^##\s*已按推荐默认\s*$")


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
            hits.append((no, "代码块或引用行", line.strip()[:3], line))
            if fence:
                continue
        for m in brand_re.finditer(line):
            hits.append((no, "品牌名", m.group(0), line))
        for name, rx in CHECKS + (GATE_CHECKS if gate else []):
            if in_decision and name in SKIP_IN_DECISION:
                continue
            for m in rx.finditer(line):
                if m.group(0):
                    hits.append((no, name, m.group(0), line))
    return hits


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
        if gate:
            for no, line in enumerate(Path(p).read_text(encoding="utf-8").splitlines(), 1):
                for m in GATE_NOTE.finditer(line):
                    print(f"{p}:{no}: 提示（不计命中）[待查未补] {m.group(0)!r}；写入申请块须逐条列出答复方与影响的卡")
        sec = re.split(r"^## 验收要点\s*$", Path(p).read_text(encoding="utf-8"), maxsplit=1, flags=re.M)
        n_accept = len(re.findall(r"^\s*- ", sec[1].split("\n## ", 1)[0], re.M)) if len(sec) > 1 else 0
        if n_accept > 12:
            print(f"{p}: 提示（不计命中）[验收要点 {n_accept} 条 > 12] 只留单卡读不出来的跨卡、跨角色、时序与多端、隐私对照断言")
        text = Path(p).read_text(encoding="utf-8")
        body = re.split(r"^## (?:已按推荐默认|未决项)\s*$", text, maxsplit=1, flags=re.M)[-1]
        topics = re.findall(r"\{待定[:：]\s*([^，,}]+)", body)
        for topic in sorted({x.strip() for x in topics if topics.count(x) > 1}):
            print(f"{p}: 提示（不计命中）[{{待定}} 重复挂 {topics.count(topic)} 次] 「{topic}」只在定义卡挂一次，其他卡写「同 帧名-编号」")
        flist = re.split(r"^## 功能清单\s*$", text, maxsplit=1, flags=re.M)
        if len(flist) > 1 and "{待定" in flist[1].split("\n## ", 1)[0]:
            print(f"{p}: 提示（不计命中）[功能清单含 {{待定}}] 未裁决处写「以卡内为准」")
        for no, frag, line in default_warnings(p):
            print(f"{p}:{no}: 提示（不计命中）[默认清单疑似必问] {frag!r}  ← {line.strip()[:80]}；核对对应规范库条目：标 级别：必问 或「按必问处理」的移到待 Box 裁决，标可默认的照常保留")
    print(f"命中 {total} 处" if total else "通过：0 命中")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
