"""Final fix for zh post — line 19 broken figure shortcode."""
import re
from pathlib import Path

path = Path(r"E:\git_local\beauty-blog\content\zh-cn\posts\plastic-surgery-subfields-deep-analysis-2026-07.md")
lines = path.read_text(encoding="utf-8").splitlines(keepends=True)

# L19 (idx 18): broken {< figure with title=\' (escaped single quote)
# Need to replace {< with {{< and title=\' with title='
# Also the title content spans line 19-20 with broken quoting

# Fix line 18 (idx 18): replace {< with {{<
# Fix line 18 (idx 18): replace title=\' with title='
for i, line in enumerate(lines):
    if i == 18:
        # Line 19 in 1-indexed: broken {< figure ... title=\'...
        line = line.replace("{< figure", "{{< figure")
        line = line.replace(r"title=\'", "title='")
        lines[i] = line

# Now check if the title is still broken (spans multiple lines)
# Read the full file text and do a targeted replacement
text = "".join(lines)

# The broken pattern: title='2026 年... (split across lines)
# Fix: find the {{< figure on line 19 and make sure title is properly closed
text = text.replace(
    "{{< figure src=\"/images/posts/plastic-surgery-subfields-2026-07/image-2.jpg\" title='2026 年整形美容八大细分领域全景：技术前沿、安全动态与消费趋势深度分",
    "{{< figure src=\"/images/posts/plastic-surgery-subfields-2026-07/image-2.jpg\" title='2026 年整形美容八大细分领域全景：技术前沿、安全动态与消费趋势深度分析'"
)

path.write_text(text, encoding="utf-8")

# Verify L19
new_lines = text.splitlines(keepends=True)
for i in [17, 18, 19]:
    print(f"  L{i+1}: {repr(new_lines[i][:120])}")

print("Done")
