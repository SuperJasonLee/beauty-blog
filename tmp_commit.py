import subprocess

# Stage only the relevant files
files_to_add = [
    'content/zh-cn/posts/plastic-surgery-subfields-deep-analysis-2026-07.md',
    'content/en/posts/plastic-surgery-subfields-deep-analysis-2026-07.md',
    'static/images/posts/plastic-surgery-subfields-2026-07/',
    'scripts/crawl-plastic-surgery-subfields-2026-07/',
]

for f in files_to_add:
    r = subprocess.run(['git', 'add', f], capture_output=True, text=True, cwd=r'E:\git_local\beauty-blog')
    if r.returncode != 0:
        print(f'Error adding {f}: {r.stderr}')

# Commit
r = subprocess.run(
    ['git', 'commit', '-m', 
     'feat: add plastic-surgery-subfields deep analysis (2026-07)\n\nCovers all 8 subspecialties: eye, nose, lip, breast, weight loss,\nfacial contouring, intimate aesthetics, deformity correction.\n- 21 PubMed articles crawled\n- 8 Pexels images downloaded (CC0/Pexels License)\n- Bilingual (zh-cn + en) posts generated\n- Audit: pass (errors=0, warnings=0 for new posts)'],
    capture_output=True, text=True, cwd=r'E:\git_local\beauty-blog'
)
with open(r'E:\git_local\beauty-blog\tmp_commit_result.txt', 'w', encoding='utf-8') as f:
    f.write(r.stdout)
    f.write(r.stderr)
print(f'Exit: {r.returncode}')
