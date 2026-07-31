"""Fix Hugo shortcode title quoting: replace smart/ASCII quotes in body with Chinese brackets."""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent

for lang in ["zh-cn", "en"]:
    path = REPO / "content" / lang / "posts" / "plastic-surgery-subfields-deep-analysis-2026-07.md"
    with open(path, "r", encoding="utf-8-sig") as f:
        raw = f.read()

    # Split at second '---' to isolate body
    parts = raw.split("\n---\n", 2)
    if len(parts) < 3:
        print(f"{lang}: only {len(parts)} parts, skipping body fix")
        continue
    fm_block = parts[0] + "\n---\n" + parts[1]
    body = parts[2]

    # In body: inside {{< figure ... title='...'>}} replace "..." → 「...」
    # Strategy: find figure shortcode blocks, then fix quotes inside title='...'
    def fix_figure_title(match):
        tag = match.group(0)
        # Replace Chinese/ASCII double-quote pairs inside the title value
        # U+201C U+201D → 「 」
        tag = tag.replace("\u201c", "\u300c").replace("\u201d", "\u300d")
        # Also replace ASCII " used as Chinese quotation marks
        tag = tag.replace('"', '\u300c').replace('"', '\u300d')
        return tag

    body = re.sub(
        r"\{\{< figure [^>]+>\}\}",
        fix_figure_title,
        body,
        flags=re.DOTALL,
    )

    new_content = fm_block + "\n---\n" + body

    with open(path, "w", encoding="utf-8-sig") as f:
        f.write(new_content)

    # Verify
    with open(path, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()
    print(f"{lang}: {len(lines)} lines, body figures:")
    for i, line in enumerate(lines, 1):
        if "{{< figure" in line:
            print(f"  L{i}: {line.rstrip()[:180]}")

print("Done")
