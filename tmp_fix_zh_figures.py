"""Clean fix for zh post figure shortcodes — rewrite broken lines directly."""
import re
from pathlib import Path

path = Path(r"E:\git_local\beauty-blog\content\zh-cn\posts\plastic-surgery-subfields-deep-analysis-2026-07.md")
lines = path.read_text(encoding="utf-8").splitlines(keepends=True)

# The post_generator.py already used 「...」 bracket quotes in most titles.
# Three lines got mangled. Fix them by index (0-based):
# L42 (idx 42): title='眼部整形正从单一"双眼皮手术「向眼综合...  → fix quotes
# L50 (idx 50): title=」\x27鼻综合手术正从"单一垫高"向...    → rewrite entirely
# L68 (idx 68): title='隆胸手术正进入「数据驱动「时代...  → fix quotes
# L88 (idx 88): title=」\x27私密部位整形正从美学需求...    → rewrite entirely

fixes = {
    42: lambda l: l.replace(
        "title='眼部整形正从单一\u300c双眼皮手术\u300c向眼综合（去皮去脂+提肌+开眼角联合方案）演进",
        "title='眼部整形正从单一\u300c双眼皮手术\u300d向眼综合（去皮去脂+提肌+开眼角联合方案）演进"
    ),
    50: lambda l: "{{< figure src=\"/images/posts/plastic-surgery-subfields-2026-07/image-3.jpg\" title='鼻综合手术正从「单一垫高」向全鼻结构重塑演进，3D导航与术前模拟是三甲医院标配' >}}\n",
    68: lambda l: l.replace(
        "title='隆胸手术正进入\u300c数据驱动\u300c时代：AI 辅助选择、微生物组学与干细胞脂肪移植构成三大技术前沿'",
        "title='隆胸手术正进入「数据驱动」时代：AI 辅助选择、微生物组学与干细胞脂肪移植构成三大技术前沿'"
    ),
    88: lambda l: "{{< figure src=\"/images/posts/plastic-surgery-subfields-2026-07/image-5.jpg\" title='私密部位整形正从美学需求扩展至功能性诉求，知情同意与适应症规范化是关键' >}}\n",
}

new_lines = []
for i, line in enumerate(lines):
    if i in fixes:
        line = fixes[i](line)
    new_lines.append(line)

path.write_text("".join(new_lines), encoding="utf-8")

# Verify all figure lines
for i, line in enumerate(new_lines):
    if "{{< figure" in line:
        print(f"  L{i+1}: {line.rstrip()[:130]}")

print("Fixed")
