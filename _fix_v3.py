# -*- coding: utf-8 -*-
"""Fix description block scalar - using actual \r\r\n line endings."""
import sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

repo = Path('E:/git_local/beauty-blog')

def fix_post(filepath: Path):
    data = filepath.read_bytes()
    
    # Actual file line ending is \r\r\n (CR CR LF)
    # Pattern: 'description: |' + \r\r\n + '  ' (2-space indent)
    old_prefix = b'description: |\r\r\n  '
    
    if old_prefix not in data:
        print(f'{filepath.name}: old_prefix NOT found')
        return False
    
    idx = data.index(old_prefix)
    rest = data[idx + len(old_prefix):]
    
    # Find end of block scalar: \r\r\n followed by a non-space ASCII char (new top-level key)
    # \r\r\n = bytes 0d 0d 0a
    # The next line starting at col 0 has a letter like 't' (tags), 'c' (categories), 'k' (keywords), etc.
    m = re.search(rb'\r\r\n([a-zA-Z])', rest)
    if not m:
        print(f'{filepath.name}: could not find block scalar end')
        return False
    
    desc_end = m.start()          # position of \r in \r\r\n before next key
    desc_raw = rest[:desc_end]    # the raw description content bytes
    desc_text = desc_raw.decode('utf-8').rstrip()
    
    # Build new single-line quoted description
    # Line ending is \r\r\n
    new_desc_line = f'description: "{desc_text}"\r\r\n'.encode('utf-8')
    
    # Replace: old_prefix + desc_raw + \r\r\n → new_desc_line
    new_data = data[:idx] + new_desc_line + rest[desc_end + 3:]  # skip \r\r\n (3 bytes)
    
    filepath.write_bytes(new_data)
    print(f'{filepath.name}: Fixed ✓')
    print(f'  Description ({len(desc_text)} chars): "{desc_text[:100]}..."')
    return True

ok_zh = fix_post(repo / 'content/zh-cn/posts/rhinoplasty-deep-analysis-2026-06.md')
ok_en = fix_post(repo / 'content/en/posts/rhinoplasty-deep-analysis-2026-06.md')
