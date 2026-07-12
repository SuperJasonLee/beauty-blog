# -*- coding: utf-8 -*-
"""Fix description: | block scalar issue in rhinoplasty posts."""
import json
import glob
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

repo = Path('E:/git_local/beauty-blog')

# Load article stats
data_dir = repo / 'data/crawled/rhinoplasty-news'
files = sorted(data_dir.glob('rhinoplasty_news_*.json'))
articles = json.loads(files[-1].read_text(encoding='utf-8'))
total = len(articles)
pubmed = sum(1 for a in articles if a.get('source_name') == 'PubMed')
zhihu = sum(1 for a in articles if a.get('source_name') == '知乎')
month = '2026-06'

desc_zh = f'基于 {total} 篇最新学术研究和行业讨论（PubMed {pubmed} 篇，知乎 {zhihu} 篇），{month} 鼻部整形领域的手术技术创新、安全规范和患者关怀深度解读。'
desc_en = f'In-depth analysis of {total} recent articles on rhinoplasty innovations, safety standards, and patient care — {pubmed} from PubMed, {zhihu} from Zhihu.'

print(f'Articles: {total} (PubMed: {pubmed}, Zhihu: {zhihu})')
print(f'ZH desc: {desc_zh}')
print(f'EN desc: {desc_en}')

# ── Fix ZH post ──────────────────────────────────────────────────────────────
zh_file = repo / 'content/zh-cn/posts/rhinoplasty-deep-analysis-2026-06.md'
zh_content = zh_file.read_text(encoding='utf-8')

# The broken block: description: |\n\n  <long text>\n\n
# Find and replace
old_zh = 'description: |\n\n  基于'
if old_zh in zh_content:
    new_zh = f'description: "{desc_zh}"\n'
    zh_content2 = zh_content.replace(old_zh, new_zh, 1)
    zh_file.write_text(zh_content2, encoding='utf-8')
    print('ZH post: Fixed description block scalar → single-line quoted')
else:
    print('ZH post: Pattern not found, checking actual content...')
    idx = zh_content.find('description:')
    if idx >= 0:
        print(f'  Found at byte {idx}: {repr(zh_content[idx:idx+300])}')

# ── Fix EN post ──────────────────────────────────────────────────────────────
en_file = repo / 'content/en/posts/rhinoplasty-deep-analysis-2026-06.md'
if en_file.exists():
    en_content = en_file.read_text(encoding='utf-8')
    old_en = 'description: |\n\n  In-depth analysis'
    if old_en in en_content:
        new_en = f'description: "{desc_en}"\n'
        en_content2 = en_content.replace(old_en, new_en, 1)
        en_file.write_text(en_content2, encoding='utf-8')
        print('EN post: Fixed description block scalar → single-line quoted')
    else:
        print('EN post: Pattern not found, checking actual content...')
        idx = en_content.find('description:')
        if idx >= 0:
            print(f'  Found at byte {idx}: {repr(en_content[idx:idx+300])}')
else:
    print('EN post: File not found, skipping')

# ── Fix post_generator.py template ──────────────────────────────────────────
gen_file = repo / 'scripts/crawl-rhinoplasty-news/post_generator.py'
gen_content = gen_file.read_text(encoding='utf-8')

# Replace ZH description block in template
old_template_zh = 'description: |\n  {description}\n'
new_template_zh = f'description: "{{description}}"\n'
if old_template_zh in gen_content:
    gen_content2 = gen_content.replace(old_template_zh, new_template_zh, 1)
    gen_file.write_text(gen_content2, encoding='utf-8')
    print('post_generator.py (ZH): Fixed template')
else:
    print('post_generator.py (ZH): Pattern not found')

# Replace EN description block in template
old_template_en = 'description: |\n  {description}\n'
# count occurrences
count = gen_content.count(old_template_en)
print(f'post_generator.py: Found {count} occurrence(s) of description: | template')
# Replace all occurrences
gen_content2 = gen_content.replace(old_template_en, new_template_zh)
if gen_content2 != gen_content:
    gen_file.write_text(gen_content2, encoding='utf-8')
    print('post_generator.py: Fixed ALL description: | templates')
