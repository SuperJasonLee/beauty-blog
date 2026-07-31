"""Comprehensive fix for zh post figure shortcode quoting."""
import re
from pathlib import Path

path = Path(r"E:\git_local\beauty-blog\content\zh-cn\posts\plastic-surgery-subfields-deep-analysis-2026-07.md")
text = path.read_text(encoding="utf-8")

# Fix 1: frontmatter opener `{< figure` → `{{< figure` (missing {)
text = text.replace(
    "{< figure src=\"/images/posts/plastic-surgery-subfields-2026-07/image-2.jpg\"",
    "{{< figure src=\"/images/posts/plastic-surgery-subfields-2026-07/image-2.jpg\"",
)

# Fix 2: Fix any broken `title=` patterns with escaped quotes
# Replace title=\x27 (literal \x27 in the file) with title='
text = text.replace(r"title=\x27", "title='")
text = text.replace(r"'\x27 >\}\}", "' >}}")

# Fix 3: Now properly fix all figure shortcode titles - replace ASCII " with 「」
# Pattern: {{< figure ... title='SOME "CHINESE" TEXT' >}}
def fix_figure(m):
    full = m.group(0)
    # Find the title='...' portion
    tm = re.search(r"title='(.+?)'", full)
    if tm:
        inner = tm.group(1)
        # Replace ASCII " with 「」 bracket quotes
        inner = re.sub(r'"', '\u300c', inner)
        # Every other unmatched becomes 」 — actually simpler:
        # just replace all " pairs with 「」
        inner_fixed = inner.replace('\u300c\u300c', '\u300c').replace('\u300c', '\u300c')
        # Replace each remaining " with 」
        inner_fixed = inner_fixed.replace('"', '\u300d')
        # Now fix alternating patterns: 「text」 should be 「text」
        # Undo double replacements
        inner_fixed = inner_fixed.replace('\u300c\u300d', '\u300c')
        return full[:tm.start(1)] + inner_fixed + full[tm.end(1):]
    return full

# Re-apply more carefully: just replace all ASCII " inside title='...' with 「」
lines = text.splitlines(keepends=True)
fixed = []
for line in lines:
    if "{{< figure" in line and "title='" in line:
        # Find title='...'
        m = re.search(r"(title=')(.+?)(')", line)
        if m:
            inner = m.group(2)
            # Replace " with 「 and 」 alternately
            # Simplest: replace all " with 「
            inner_new = inner.replace('"', '「')
            # Close with 」 at end (before the closing ')
            # Actually just replace all " with 」 — simple approach
            inner_new = inner.replace('"', '「')
            # Wait, I need closing brackets too
            # Let me count pairs
            parts = inner.split('"')
            if len(parts) > 1:
                result_parts = []
                for i, part in enumerate(parts):
                    result_parts.append(part)
                    if i < len(parts) - 1:
                        if i % 2 == 0:
                            result_parts.append('「')
                        else:
                            result_parts.append('」')
                inner_new = ''.join(result_parts)
            line = line[:m.start(2)] + inner_new + line[m.end(2):]
    fixed.append(line)

text = ''.join(fixed)
path.write_text(text, encoding="utf-8")
print("Done")

# Verify all figure lines
for i, line in enumerate(text.splitlines()):
    if "{{< figure" in line:
        print(f"  L{i+1}: {line[:120]}")
