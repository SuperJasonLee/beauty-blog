"""Fix Hugo shortcode title quoting issues in zh-cn plastic-surgery post.
Hugo cannot handle single-quoted shortcode params that contain apostrophes/quotes.
Replace smart quotes with plain ASCII or Chinese brackets to avoid parser errors.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
path = REPO / "content" / "zh-cn" / "posts" / "plastic-surgery-subfields-deep-analysis-2026-07.md"

with open(path, "r", encoding="utf-8-sig") as f:
    content = f.read()

# Count figures before
figures_before = len(re.findall(r"\{\{< figure", content))
print(f"Found {figures_before} figure shortcodes")

# Replace Chinese curly quotes inside single-quoted titles
# U+201C = "  U+201D = "  U+2018 = '  U+2019 = '
# Also regular ASCII " inside single-quoted titles
content = content.replace("\u201c", "\u300c").replace("\u201d", "\u300d")  # "..."  → 「...」
content = content.replace("\u2018", "\u300e").replace("\u2019", "\u300f")  # '...'  → 『...』

# Also replace regular ASCII double quotes used as Chinese-style quotes
# Pattern: "word" → 「word」when used as Chinese quotation marks
# But be careful not to break YAML frontmatter
# Split into frontmatter and body
parts = content.split("\n---\n", 2)
if len(parts) >= 3:
    fm = parts[0] + "\n---\n" + parts[1]
    body = parts[2]
    # Only fix body (not frontmatter)
    body = body.replace('"', '\u300c').replace('"', '\u300d')  # ASCII " → 「」
    content = fm + "\n---\n" + body

# Verify figures still exist
figures_after = len(re.findall(r"\{\{< figure", content))
print(f"After fix: {figures_after} figure shortcodes")

with open(path, "w", encoding="utf-8-sig") as f:
    f.write(content)

print("Fixed and saved")

# Show the figure lines
with open(path, "r", encoding="utf-8-sig") as f:
    lines = f.readlines()
print("\nFigure shortcode lines:")
for i, line in enumerate(lines, 1):
    if "{{< figure" in line:
        print(f"  {i}: {line.rstrip()[:180]}")
