# -*- coding: utf-8 -*-
"""Fix the description block scalar bug in rhinoplasty posts."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

repo = Path('E:/git_local/beauty-blog')

# ── Fix ZH post ──────────────────────────────────────────────────────────────
zh_file = repo / 'content/zh-cn/posts/rhinoplasty-deep-analysis-2026-06.md'
zh_bytes = zh_file.read_bytes()

# Locate 'description: |\r\n\r\n  '  (the broken block scalar)
# In bytes: b'description: |\r\n\r\n  '
old_zh = b'description: |\r\n\r\n  '
new_zh = b'description: "'

if old_zh in zh_bytes:
    # Find where the block scalar ends (next \r\n\r\n---\r\n or \r\n\r\ntags:)
    idx = zh_bytes.index(old_zh)
    rest = zh_bytes[idx + len(old_zh):]
    
    # Find end of description content: before \r\n\r\n followed by a non-space char
    # or before \r\n\r\n--- 
    # The description content runs until we hit a blank line followed by a top-level key
    import re
    # Find: \r\n\r\n followed by a non-space char (end of block scalar)
    m = re.search(rb'\r\n\r\n([a-zA-Z])', rest)
    if m:
        desc_end = m.start()
        desc_content = rest[:desc_end].decode('utf-8').rstrip()
        # Build new single-line description
        new_desc_line = f'description: "{desc_content}"\r\n'.encode('utf-8')
        # Replace: old pattern + desc_content + \r\n\r\n with just new line
        replace_end = desc_end + 2  # include the \r\n of the blank line
        new_bytes = zh_bytes[:idx] + new_desc_line + zh_bytes[idx + len(old_zh) + replace_end:]
        zh_file.write_bytes(new_bytes)
        print(f'ZH post: Fixed. Description: "{desc_content[:80]}..."')
    else:
        print('ZH post: Could not find end of block scalar')
else:
    print('ZH post: Pattern not found, showing actual bytes:')
    idx2 = zh_bytes.find(b'description: |')
    if idx2 >= 0:
        print('  ', zh_bytes[idx2:idx2+40].hex())

# ── Fix EN post ──────────────────────────────────────────────────────────────
en_file = repo / 'content/en/posts/rhinoplasty-deep-analysis-2026-06.md'
if en_file.exists():
    en_bytes = en_file.read_bytes()
    old_en = b'description: |\r\n\r\n  '
    if old_en in en_bytes:
        idx = en_bytes.index(old_en)
        rest = en_bytes[idx + len(old_en):]
        import re
        m = re.search(rb'\r\n\r\n([a-zA-Z])', rest)
        if m:
            desc_end = m.start()
            desc_content = rest[:desc_end].decode('utf-8').rstrip()
            new_desc_line = f'description: "{desc_content}"\r\n'.encode('utf-8')
            replace_end = desc_end + 2
            new_bytes = en_bytes[:idx] + new_desc_line + en_bytes[idx + len(old_en) + replace_end:]
            en_file.write_bytes(new_bytes)
            print(f'EN post: Fixed. Description: "{desc_content[:80]}..."')
        else:
            print('EN post: Could not find end of block scalar')
    else:
        print('EN post: Pattern not found')
else:
    print('EN post: File not found')
