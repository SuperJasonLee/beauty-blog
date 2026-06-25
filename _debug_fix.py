# -*- coding: utf-8 -*-
"""Debug fix script."""
import sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
repo = Path('E:/git_local/beauty-blog')
zh = repo / 'content/zh-cn/posts/rhinoplasty-deep-analysis-2026-06.md'
data = zh.read_bytes()

old_prefix = b'description: |\r\r\n  '
idx = data.index(old_prefix)
rest = data[idx + len(old_prefix):]

print(f'old_prefix at byte: {idx}')
print(f'rest starts at byte: {idx + len(old_prefix)}')
print(f'rest first 20 bytes hex: {rest[:20].hex()}')

# Find all \r\r\n positions
positions = [m.start() for m in re.finditer(rb'\r\r\n', rest)]
print(f'\\r\\r\\n positions in rest: {positions[:10]}')

# Find all \r\r\n followed by letter
for m in re.finditer(rb'\r\r\n([a-zA-Z])', rest):
    print(f'Match at rest[{m.start()}:{m.end()}]: {m.group()!r}  → desc content would be rest[:{m.start()}] = {rest[:m.start()][:30]}...')

# Also look for \r\r\n followed by quote
for m in re.finditer(rb'\r\r\n(["\'])', rest):
    print(f'Quote match at rest[{m.start()}:{m.end()}]: {m.group()!r}')
