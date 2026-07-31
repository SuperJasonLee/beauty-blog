"""Fix zh post: switch figure shortcode title= from single-quote to double-quote
for Hugo 0.161 CJK compatibility. Also fix line 19 broken {< → {{<."""
from pathlib import Path
import re

path = Path(r"E:\git_local\beauty-blog\content\zh-cn\posts\plastic-surgery-subfields-deep-analysis-2026-07.md")
text = path.read_text(encoding="utf-8")

# Fix 1: frontmatter figure opener {< → {{<
text = text.replace(
    "{< figure src=\"/images/posts/plastic-surgery-subfields-2026-07/image-2.jpg\"",
    "{{< figure src=\"/images/posts/plastic-surgery-subfields-2026-07/image-2.jpg\"",
    1,
)

# Fix 2: All figure shortcodes: title='...' → title="..." for CJK compatibility
# Pattern: title='anything' inside a figure shortcode
def fix_title(m):
    inner = m.group(1)
    # Escape any double-quotes inside (shouldn't be any after prior fixes)
    escaped = inner.replace('"', '\\"')
    return f'title="{escaped}"'

text = re.sub(r"title='(.+?)'", fix_title, text)

# Fix 3: Ensure every figure shortcode closes properly >}} not >
text = text.replace("' >}}", '" >}}')  # already fixed above, this is just safety
# Fix any remaining single-quote closes
text = re.sub(r"' >\}\}", '" >}}', text)

path.write_text(text, encoding="utf-8")

# Verify all figure lines
for i, line in enumerate(text.splitlines()):
    if "{{< figure" in line:
        print(f"  L{i+1}: {line[:130]}")

print("Fixed")
