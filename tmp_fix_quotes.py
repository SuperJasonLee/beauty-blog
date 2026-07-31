"""Fix Chinese double-quote issues in zh post figure shortcodes."""
import re
from pathlib import Path

path = Path(r"E:\git_local\beauty-blog\content\zh-cn\posts\plastic-surgery-subfields-deep-analysis-2026-07.md")
text = path.read_text(encoding="utf-8")

# Fix 1: Replace all figure shortcode title= inner Chinese curly quotes "
# The shortcode titles already use single quotes, so we just need to escape inner "
# Hugo shortcode parser: title='...' is fine as long as no inner single quotes
# Problem is Chinese " (U+201C/U+201D) — Hugo may misparse these as YAML delimiters
# Solution: replace them with 「 and 」

text = text.replace("\u201c", "\u300c").replace("\u201d", "\u300d")

# Fix 2: The line 43 mangled title had a broken pattern — fix it
# Broken: title='眼部整形正从单一"双眼皮手术「向眼综合...
# Should be: title='眼部整形正从单一「双眼皮手术」向眼综合...
text = text.replace(
    "title='眼部整形正从单一\u300c双眼皮手术\u300c向眼综合",
    "title='眼部整形正从单一\u300c双眼皮手术\u300d向眼综合",
)

# Fix 3: Also fix body text quotes that were affected
text = text.replace(
    "「金标准\u201d材料",
    "\u201c金标准\u201d材料",
)

path.write_text(text, encoding="utf-8")
print("Fixed zh post figure titles")
