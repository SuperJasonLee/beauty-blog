# -*- coding: utf-8 -*-
"""Fix EN post - rewrite the entire frontmatter cleanly."""
import sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
repo = Path('E:/git_local/beauty-blog')

# ── Fix ZH post (already partially fixed, need to clean up) ──────────────────
zh = repo / 'content/zh-cn/posts/rhinoplasty-deep-analysis-2026-06.md'
zh_data = zh.read_bytes()

# The ZH file has: after `description: "...", there's a double \r\n\r\n then tags:
# Show the area around description
idx = zh_data.find(b'description: "')
if idx >= 0:
    # Find the closing quote of description
    desc_start = idx + len(b'description: "')
    # Find the next " after desc_start
    q2 = zh_data.index(b'"', desc_start)
    desc_text = zh_data[desc_start:q2].decode('utf-8')
    print(f'ZH description ({len(desc_text)} chars): {desc_text[:80]}...')
    # Show what's after the closing quote
    after = zh_data[q2:q2+20]
    print(f'  After closing quote: {after.hex()}')
    
    # The issue: after `"` there's `\r\n\r\n` then more content
    # Need to ensure: `"...",\r\n` (single CRLF, no extra blank line)
    # Check current state
    if zh_data[q2:q2+4] == b'"0d0a0d0a':  # "\r\n\r\n"
        print('  WARNING: Extra blank line after description!')

# ── Fix EN post ──────────────────────────────────────────────────────────────
en = repo / 'content/en/posts/rhinoplasty-deep-analysis-2026-06.md'
en_data = en.read_bytes()

# Show the EN description area
idx_en = en_data.find(b'description: "')
if idx_en >= 0:
    desc_start_en = idx_en + len(b'description: "')
    q2_en = en_data.index(b'"', desc_start_en)
    desc_text_en = en_data[desc_start_en:q2_en].decode('utf-8')
    print(f'\nEN description ({len(desc_text_en)} chars): {desc_text_en[:80]}...')
    after_en = en_data[q2_en:q2_en+30]
    print(f'  After closing quote: {after_en.hex()}')
    
    # The EN file has: description: "... Zhihu."\r\n\r\n of 20 recent...
    # This means the description was truncated and there's garbage after
    
    # Find where the actual description ends in the current broken file
    # Look for the first \r\n\r\n after the closing quote
    # Then find where tags: appears
    tags_idx = en_data.find(b'\r\n\r\ntags:', q2_en)
    print(f'  tags: at byte {tags_idx}')
    
    # Find the REAL end of description by looking for the pattern:
    # after closing quote, then \r\n, then content that looks like continuation
    # The description text should be: "In-depth analysis of 20 recent..."
    # The current file has truncated description followed by garbage
    
    # Let's find the CORRECT description end:
    # After the opening `description: "`, find the FIRST `"` that's followed by `\r\n\r\n`
    # This is the properly closed description
    
    # Look for the second `"` after desc_start_en
    # Check bytes between desc_start_en and q2_en
    search_area = en_data[desc_start_en:desc_start_en+500]
    quotes_in_area = [i for i, b in enumerate(search_area) if b == 0x22]
    print(f'  Quotes in first 500 bytes of desc: {quotes_in_area[:5]}')
    
    # The correct description ends at the `"` followed by `\r\n\r\n` or `\r\n\n`
    for qi in quotes_in_area[:5]:
        abs_pos = desc_start_en + qi
        after_quote = en_data[abs_pos:abs_pos+6]
        if after_quote.startswith(b'"\r\n\r\n') or after_quote.startswith(b'"\r\n\n'):
            print(f'  Found proper description end at byte {abs_pos} (quote #{qi})')
            desc_correct = en_data[desc_start_en:abs_pos].decode('utf-8')
            print(f'  Correct description: {desc_correct[:80]}...')
            break
