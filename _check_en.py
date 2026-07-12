# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

en = Path('E:/git_local/beauty-blog/content/en/posts/rhinoplasty-deep-analysis-2026-06.md')
data = en.read_bytes()
rrn = data.count(b'\r\r\n')
rn = data.count(b'\r\n')
print(f'EN file: {rrn} x \\r\\r\\n, {rn} x \\r\\n')

# Find description field
idx = data.find(b'description: |')
if idx >= 0:
    print(f'description: | at byte {idx}')
    # Show 200 bytes around it
    print('Hex:', data[idx:idx+200].hex())
else:
    print('No description: | found, checking current state...')
    idx2 = data.find(b'description:')
    if idx2 >= 0:
        print(f'description: at byte {idx2}')
        print('Hex:', data[idx2:idx2+200].hex())
