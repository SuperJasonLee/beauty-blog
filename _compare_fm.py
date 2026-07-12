# -*- coding: utf-8 -*-
"""Compare frontmatter structures between working and broken posts."""
import sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
repo = Path('E:/git_local/beauty-blog')

# Working post
eye = repo / 'content/zh-cn/posts/eye-surgery-deep-analysis-2026-06.md'
# Broken post
rhino = repo / 'content/zh-cn/posts/rhinoplasty-deep-analysis-2026-06.md'

for name, f in [('eye-surgery', eye), ('rhinoplasty', rhino)]:
    data = f.read_bytes()
    # Find first ---\r\n (opening fm)
    fm_open = data.index(b'---')
    # Find second ---\r\n (closing fm) 
    rest = data[fm_open+3:]
    fm_close_match = re.search(rb'[\r\n]---[\r\n]', rest)
    if fm_close_match:
        fm_close = fm_close_match.start() + 3
        fm = data[fm_open+3:fm_close]
        print(f'\n=== {name} frontmatter ({len(fm)} bytes) ===')
        # Show first 100 bytes
        print(f'  First 100 hex: {fm[:100].hex()}')
        # Count \r\n vs \r\r\n
        rn = fm.count(b'\r\n')
        rrn = fm.count(b'\r\r\n')
        print(f'  \\r\\n count: {rn}')
        print(f'  \\r\\r\\n count: {rrn}')
        # Show lines
        lines = fm.split(b'\r\n')
        print(f'  Lines (split by \\r\\n): {len(lines)}')
        for i, line in enumerate(lines[:16], 1):
            print(f'    L{i}: {repr(line[:80])}')
