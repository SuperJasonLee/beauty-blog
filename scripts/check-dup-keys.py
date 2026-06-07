"""Check for duplicate frontmatter keys in all posts."""
import re
from pathlib import Path
from collections import Counter

posts = sorted(Path('content').rglob('*.md'))
issues = []
for p in posts:
    text = p.read_text(encoding='utf-8')
    # Extract frontmatter (between first two ---)
    m = re.match(r'---\n(.*?)\n---', text, re.DOTALL)
    if not m:
        continue
    fm = m.group(1)
    keys = []
    for line in fm.split('\n'):
        stripped = line.strip()
        if not stripped or stripped.startswith('#') or stripped.startswith('-'):
            continue
        # Match "key:" at start of line
        km = re.match(r'^([\w-]+):', stripped)
        if km:
            keys.append(km.group(1))
    dups = [k for k, c in Counter(keys).items() if c > 1]
    if dups:
        issues.append((p, dups))

if issues:
    print(f'Duplicate keys found in {len(issues)} files:')
    for p, dups in issues:
        print(f'  {p}: {dups}')
else:
    print('No duplicate frontmatter keys.')
