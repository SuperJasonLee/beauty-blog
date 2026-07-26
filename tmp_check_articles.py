import json, sys

data = json.loads(open(r'E:\git_local\beauty-blog\data\crawled\plastic-surgery-subfields-news\plastic_surgery_subfields_news_20260726_114327.json', encoding='utf-8').read())
print(f'Total articles: {len(data)}')
for a in data:
    print(f"  [{a.get('source_name')}] {a.get('title','')[:80]}")
