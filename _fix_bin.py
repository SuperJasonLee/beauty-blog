# -*- coding: utf-8 -*-
"""Fix the description block scalar bug - binary-level precise fix."""
import sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

repo = Path('E:/git_local/beauty-blog')

def fix_file(filepath: Path):
    data = filepath.read_bytes()
    
    # The file uses CRLF: \r\n as line endings
    # 'description: |' is followed by \r (end of its line) then \r\n (blank line)
    # So pattern in bytes: b'description: |\r\r\n  '
    old_prefix = b'description: |\r\r\n  '
    
    if old_prefix not in data:
        # Try alternate: maybe it's b'description: |\r\n  '
        old_prefix2 = b'description: |\r\n  '
        if old_prefix2 in data:
            idx = data.index(old_prefix2)
            rest = data[idx + len(old_prefix2):]
            # Find the next \r\n\r\n or \r\n--- sequence that terminates block
            m = re.search(rb'\r\n\r\n([a-zA-Z"\'])', rest)
            if m:
                desc_end = m.start()
                desc_raw = rest[:desc_end]
                desc_text = desc_raw.decode('utf-8')
                # Replace the block scalar with single-line quoted description
                new_desc = f'description: "{desc_text}"\r\n'.encode('utf-8')
                # After desc_end+2 there's \r\n\r\n - we want to keep \r\n after description
                new_data = data[:idx] + new_desc + rest[desc_end + 4:]  # skip \r\n\r\n
                filepath.write_bytes(new_data)
                print(f'Fixed {filepath.name}: description = "{desc_text[:80]}..."')
                return
        print(f'NOT FOUND in {filepath.name}, showing bytes around description:')
        idx = data.find(b'description: |')
        if idx >= 0:
            print('  Hex:', data[idx:idx+40].hex())
        return
    
    idx = data.index(old_prefix)
    rest = data[idx + len(old_prefix):]
    
    # Find where block scalar ends: look for \r\n\r\n followed by ASCII letter or quote
    m = re.search(rb'\r\n\r\n([a-zA-Z"\'])', rest)
    if m:
        desc_end = m.start()
        desc_raw = rest[:desc_end]
        desc_text = desc_raw.decode('utf-8').rstrip()
        new_desc = f'description: "{desc_text}"\r\n'.encode('utf-8')
        # Replace old block scalar (prefix + content + \r\n\r\n) with single line
        new_data = data[:idx] + new_desc + rest[desc_end + 4:]  # skip the \r\n\r\n
        filepath.write_bytes(new_data)
        print(f'Fixed {filepath.name}: description = "{desc_text[:80]}..."')
    else:
        print(f'{filepath.name}: Could not find block scalar end')

fix_file(repo / 'content/zh-cn/posts/rhinoplasty-deep-analysis-2026-06.md')
fix_file(repo / 'content/en/posts/rhinoplasty-deep-analysis-2026-06.md')
