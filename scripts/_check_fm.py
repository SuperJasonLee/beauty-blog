import yaml, sys

for lang in ['zh-cn', 'en']:
    path = f'E:/git_local/beauty-blog/content/{lang}/posts/rhinoplasty-deep-analysis-2026-06.md'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    fm = content.split('---')[1]
    data = yaml.safe_load(fm)
    required = ['title','date','lastmod','draft','description','tags','categories','author','lastReviewed','medicalAudience','featuredImage']
    missing = [k for k in required if k not in data]
    status = 'OK' if not missing else f'MISSING: {missing}'
    print(f'{lang}: {status} | draft={data.get("draft")} | date={data.get("date")} | featuredImage={data.get("featuredImage","N/A")[:60]}')
