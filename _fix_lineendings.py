# -*- coding: utf-8 -*-
"""Fix all \r\r\n line endings to \r\n in rhinoplasty posts."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
repo = Path('E:/git_local/beauty-blog')

files = [
    repo / 'content/zh-cn/posts/rhinoplasty-deep-analysis-2026-06.md',
    repo / 'content/en/posts/rhinoplasty-deep-analysis-2026-06.md',
]

for f in files:
    if not f.exists():
        print(f'{f.name}: NOT FOUND')
        continue
    data = f.read_bytes()
    rrn = data.count(b'\r\r\n')
    rn = data.count(b'\r\n')
    print(f'{f.name}: {rrn} x \\r\\r\\n, {rn} x \\r\\n')
    
    if rrn > 0:
        fixed = data.replace(b'\r\r\n', b'\r\n')
        f.write_bytes(fixed)
        print(f'  -> Fixed! Now {fixed.count(b"\\r\\n")} x \\r\\n')
    else:
        print(f'  -> Already OK')
