# -*- coding: utf-8 -*-
"""Debug: show exact binary around description field."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

repo = Path('E:/git_local/beauty-blog')
zh_file = repo / 'content/zh-cn/posts/rhinoplasty-deep-analysis-2026-06.md'

data = zh_file.read_bytes()
idx = data.find(b'description: |')
print(f'Found at byte: {idx}')
print(f'Bytes around it (hex):')
for i in range(max(0, idx-5), min(len(data), idx+80)):
    print(f'  [{i:4d}] 0x{i:02x} {data[i:i+1].hex()} {repr(chr(data[i]) if 32 <= data[i] < 127 else "?")}')

print()
print(f'Searching for b"description: |\\r\\r\\n  ": ...')
target = b'description: |\r\r\n  '
print(f'  Target bytes: {target.hex()}')
print(f'  Found: {target in data}')

# Also check if it's actually \r\n\r\n
target2 = b'description: |\r\n\r\n  '
print(f'Searching for b"description: |\\r\\n\\r\\n  ": ...')
print(f'  Found: {target2 in data}')

# Show the first 20 bytes after 'description: |'
if idx >= 0:
    after = data[idx:idx+50]
    print(f'\nActual bytes after "description: |": {after.hex()}')
    print(f'Decoded as raw: {after}')
    
    # Try different splits
    print('\nTrying to find where tags: appears...')
    tags_idx = data.find(b'\r\ntags:', idx)
    print(f'  \\r\\ntags: at {tags_idx}')
    tags_idx2 = data.find(b'\r\r\ntags:', idx)
    print(f'  \\r\\r\\ntags: at {tags_idx2}')
    tags_idx3 = data.find(b'\n\n', idx)
    print(f'  \\n\\n at {tags_idx3}')
    # Find the sequence of \r\n\r\n or just \n\n after description
    print(f'\n  Raw bytes from idx to idx+100:')
    chunk = data[idx:idx+100]
    print(f'  {chunk.hex()}')
