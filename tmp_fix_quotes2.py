"""Fix zh post figure shortcode title quoting for Hugo."""
import re
from pathlib import Path

path = Path(r"E:\git_local\beauty-blog\content\zh-cn\posts\plastic-surgery-subfields-deep-analysis-2026-07.md")
lines = path.read_text(encoding="utf-8").splitlines(keepends=True)

fixed_lines = []
for line in lines:
    # Detect figure shortcode lines
    if "{{< figure" in line and "title=" in line:
        # Find the title= value between single quotes
        m = re.search(r"title='(.*?)' >\}\}", line)
        if m:
            inner = m.group(1)
            # Replace ASCII double quotes "..." with 「...」
            inner = re.sub(r'"([^"]*)"', r'「\1」', inner)
            line = line[:m.start(1)] + inner + line[m.end(1):]
    fixed_lines.append(line)

path.write_text("".join(fixed_lines), encoding="utf-8")
print("Fixed zh figure titles — replaced ASCII double quotes with 「」 brackets")

# Verify
for i, line in enumerate(fixed_lines):
    if "{{< figure" in line:
        print(f"  Line {i+1}: {line.rstrip()[:100]}")
