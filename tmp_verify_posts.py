import re

for lang, path in [
    ('zh', r'E:\git_local\beauty-blog\content\zh-cn\posts\plastic-surgery-subfields-deep-analysis-2026-07.md'),
    ('en', r'E:\git_local\beauty-blog\content\en\posts\plastic-surgery-subfields-deep-analysis-2026-07.md'),
]:
    with open(path, encoding='utf-8') as f:
        content = f.read()
    
    footer_lines = [l for l in content.split('\n') if '本文基于' in l or 'synthesizes' in l]
    for l in footer_lines:
        print(f'{lang} footer: {l.strip()[:120]}')
    
    has_date = '{date}' in content
    has_datetime = 'datetime' in content
    has_faq = '{{< faq >}}' in content
    has_disclaimer = '{{< medical-disclaimer />}}' in content
    figures = len(re.findall(r'\{\{< figure ', content))
    pct_warnings = len(re.findall(r'\b\d{1,4}(?:\.\d+)?%', content))
    print(f'{lang}: date_placeholder={has_date}, datetime={has_datetime}, faq={has_faq}, disclaimer={has_disclaimer}, figures={figures}, pct_count={pct_warnings}')
    print()
