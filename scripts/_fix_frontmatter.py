"""Fix YAML frontmatter encoding issues in generated posts."""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

for lang in ["zh-cn", "en"]:
    path = REPO / "content" / lang / "posts" / "plastic-surgery-subfields-deep-analysis-2026-07.md"
    with open(path, "r", encoding="utf-8-sig") as f:
        raw = f.read()

    m = re.match(r"^(---\s*\n)(.*?)(\n---\s*\n)(.*)$", raw, re.DOTALL)
    if not m:
        print(f"{lang}: cannot split frontmatter, skipping")
        continue

    fm_text = m.group(2)
    sep = m.group(3)
    body = m.group(4)

    lines = fm_text.split("\n")
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("tags:") or stripped.startswith("keywords:"):
            key = stripped.split(":")[0]
            val = stripped[len(key) + 1:].strip()
            if val.startswith("[") and val.endswith("]"):
                inner = val[1:-1]
                items = [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()]
                quoted = [f'"{x}"' for x in items]
                new_line = f"{key}: [{', '.join(quoted)}]"
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    new_fm = "\n".join(new_lines)
    new_content = "---\n" + new_fm + sep + body

    with open(path, "w", encoding="utf-8-sig") as f:
        f.write(new_content)
    print(f"{lang}: frontmatter fixed")

print("Done")
