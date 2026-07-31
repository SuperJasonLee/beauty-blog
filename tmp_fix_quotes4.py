"""Fix zh post figure shortcode titles for Hugo build."""
import re
from pathlib import Path

path = Path(r"E:\git_local\beauty-blog\content\zh-cn\posts\plastic-surgery-subfields-deep-analysis-2026-07.md")
text = path.read_text(encoding="utf-8")

# Fix 1: frontmatter {< figure -> {{< figure
text = text.replace(
    "{< figure src=\"/images/posts/plastic-surgery-subfields-2026-07/image-2.jpg\"",
    "{{< figure src=\"/images/posts/plastic-surgery-subfields-2026-07/image-2.jpg\"",
    1
)

# Fix 2: triple braces
text = text.replace("{{{< figure", "{{< figure")

# Fix 3: any escaped quotes
text = text.replace(r"title=\x27", "title='")
text = text.replace(r"\x27 >}}", "' >}}")

# Fix 4: For each figure shortcode, ensure title uses double-quote delimiter
# when the value contains ASCII double quotes, or use single quotes without ASCII "
lines = text.splitlines(keepends=True)
fixed = []

for line in lines:
    if "{{< figure" in line and "title=" in line:
        m = re.search(r"title='(.+?)'", line)
        if m:
            inner = m.group(1)
            if '"' in inner:
                # Switch to double-quote delimiter, escape inner "
                escaped = inner.replace('"', '&quot;')
                new_title = '"' + escaped + '"'
                line = line[:m.start(1)] + new_title + line[m.end(1):]
    fixed.append(line)

path.write_text("".join(fixed), encoding="utf-8")

# Verify
for i, line in enumerate(fixed):
    if "{{< figure" in line:
        print(f"  L{i+1}: {line.rstrip()[:130]}")

print("Done")
