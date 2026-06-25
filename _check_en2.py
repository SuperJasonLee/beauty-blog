# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

en = Path('E:/git_local/beauty-blog/content/en/posts/rhinoplasty-deep-analysis-2026-06.md')
data = en.read_bytes()
print(f'EN file size: {len(data)} bytes')
rrn = data.count(b'\r\r\n')
rn = data.count(b'\r\n')
print(f'\\r\\r\\n count: {rrn}')
print(f'\\r\\n count: {rn}')
print(f'description: | found: {b"description: |" in data}')

# Show first 450 bytes
print('\nFirst 450 bytes hex dump:')
for i in range(0, min(450, len(data)), 16):
    chunk = data[i:i+16]
    h = ' '.join(f'{b:02x}' for b in chunk)
    try:
        t = chunk.decode('utf-8').replace('\r', '\\r').replace('\n', '\\n')
    except:
        t = '???'
    print(f'  [{i:4d}] {h:<48} {t}')
