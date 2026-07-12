# -*- coding: utf-8 -*-
"""Validate frontmatter with Python yaml."""
import sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

try:
    import yaml
except ImportError:
    print("PyYAML not installed")
    sys.exit(1)

repo = Path('E:/git_local/beauty-blog')
zh = repo / 'content/zh-cn/posts/rhinoplasty-deep-analysis-2026-06.md'
raw = zh.read_bytes()

# Extract frontmatter: between first --- and second ---
fm_start = raw.index(b'---') + 3
# Find closing --- after a blank line
closing = re.search(rb'\r\r\n---\r\r\n', raw[fm_start:])
if not closing:
    print("No closing --- found")
    sys.exit(1)
fm_end = fm_start + closing.start()
fm_bytes = raw[fm_start:fm_end]

print(f"Frontmatter bytes: {fm_start} to {fm_end} ({len(fm_bytes)} bytes)")
print(f"Frontmatter (first 200 bytes): {fm_bytes[:200].hex()}")
print()

# Try to parse
try:
    fm = yaml.safe_load(fm_bytes)
    print("YAML parse OK!")
    for k, v in fm.items():
        print(f"  {k}: {repr(v)[:80]}")
except yaml.YAMLError as e:
    print(f"YAML parse error: {e}")
    # Show context around error
    if hasattr(e, 'problem_mark'):
        m = e.problem_mark
        print(f"  At line {m.line+1}, col {m.column+1}")

# Also show the actual decoded text of the frontmatter
print("\n=== Decoded frontmatter ===")
text = fm_bytes.decode('utf-8')
for i, line in enumerate(text.split('\r\r\n'), 1):
    print(f"  {i:2d}: {repr(line[:100])}")
