"""Final clean fix for zh-cn post — targeted line edits only."""
from pathlib import Path

path = Path(r"E:\git_local\beauty-blog\content\zh-cn\posts\plastic-surgery-subfields-deep-analysis-2026-07.md")
lines = path.read_text(encoding="utf-8").splitlines(keepends=True)

# Line 19 (idx 18): broken {{< figure with title=\'...\'析\'
# Replace entire broken line with correct version
lines[18] = "{{< figure src=\"/images/posts/plastic-surgery-subfields-2026-07/image-2.jpg\" title='2026 年整形美容八大细分领域全景：技术前沿、安全动态与消费趋势深度分析' >}}\n"

path.write_text("".join(lines), encoding="utf-8")

# Verify all 6 figure lines
for i, line in enumerate(lines):
    if "{{< figure" in line:
        print(f"  L{i+1}: {line.rstrip()[:120]}")

print("Fixed line 19")
