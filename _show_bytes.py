# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

zh = Path('E:/git_local/beauty-blog/content/zh-cn/posts/rhinoplasty-deep-analysis-2026-06.md')
data = zh.read_bytes()
print('description: | found:', b'description: |' in data)
print('description: " found:', b'description: "' in data)

print('\nBytes 128-420 hex:')
for i in range(128, min(420, len(data)), 16):
    chunk = data[i:i+16]
    h = ' '.join(f'{b:02x}' for b in chunk)
    try:
        t = chunk.decode('utf-8').replace('\r', '\\r').replace('\n', '\\n')
    except:
        t = '???'
    print(f'  [{i:4d}] {h:<48} {t}')
