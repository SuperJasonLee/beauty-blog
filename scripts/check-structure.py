import os, re, sys
from pathlib import Path

posts = sorted(Path('content').rglob('*.md'))
print(f'Posts found: {len(posts)}')

issues = []
shortcode_re = re.compile(r'\{\{<\s*([\w-]+)')
known_shortcodes = {'medical-disclaimer', 'figure', 'alert', 'faq', 'youtube', 'gist', 'tab', 'tabs', 'term'}

for p in posts:
    text = p.read_text(encoding='utf-8')
    for m in shortcode_re.finditer(text):
        sc = m.group(1)
        if sc not in known_shortcodes:
            issues.append(f'{p}: unknown shortcode "{sc}"')

img_re = re.compile(r'!\[.*?\]\((/images/[^)]+)\)')
imgs_total = 0
imgs_missing = 0
for p in posts:
    text = p.read_text(encoding='utf-8')
    for m in img_re.finditer(text):
        imgs_total += 1
        path = 'static' + m.group(1)
        if not os.path.exists(path):
            imgs_missing += 1
            issues.append(f'{p}: missing image {m.group(1)}')
print(f'Images: {imgs_total} total, {imgs_missing} missing')

for p in posts:
    text = p.read_text(encoding='utf-8')
    m = re.search(r"^featuredImage:\s*['\"]?(/images/[^'\"\n]+)", text, re.MULTILINE)
    if m:
        path = 'static' + m.group(1)
        if not os.path.exists(path):
            issues.append(f'{p}: missing featured image {m.group(1)}')

print(f'Issues: {len(issues)}')
for i in issues[:20]:
    print(' -', i)
