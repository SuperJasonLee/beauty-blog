"""Final comprehensive fix for zh post before Hugo build."""
import re
from pathlib import Path

path = Path(r"E:\git_local\beauty-blog\content\zh-cn\posts\plastic-surgery-subfields-deep-analysis-2026-07.md")
text = path.read_text(encoding="utf-8")

# L19 issue: title=\' (literal backslash-quote) — caused by double-escaping
# The line shows: title=\'2026 年...分析\'析\' >}\n
# There's also a broken '析' at the end of the title

# Fix 1: Replace {{{{< with {{{<
text = text.replace("{{{{<", "{{{<")

# Fix 2: Replace {{{{ with {{
text = text.replace("{{{{< figure", "{{< figure")

# Fix 3: Fix the broken title on line 19
# Pattern: title=\'2026 年...分析\'析\' >}
# Should be: title='2026 年...深度分析' >}}
text = re.sub(
    r"title=\\'(.+?)' >\}",
    lambda m: "title='" + m.group(1).rstrip("析") + "' >}}",
    text
)

# Fix 4: Also fix any literal \x27 patterns
text = text.replace(r"title=\x27", "title='")

path.write_text(text, encoding="utf-8")

lines = text.splitlines(keepends=True)
for i in [17, 18, 19]:
    print(f"  L{i+1}: {repr(lines[i][:120])}")
print("Done")
