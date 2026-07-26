import os, re
from pathlib import Path

for lang, path in [
    ('zh', r'E:\git_local\beauty-blog\content\zh-cn\posts\plastic-surgery-subfields-deep-analysis-2026-07.md'),
    ('en', r'E:\git_local\beauty-blog\content\en\posts\plastic-surgery-subfields-deep-analysis-2026-07.md'),
]:
    if not os.path.exists(path):
        with open(r'E:\git_local\beauty-blog\tmp_verify_result.txt', 'a') as f:
            f.write(f'{lang}: FILE NOT FOUND\n')
        continue
    with open(path, encoding='utf-8') as f:
        content = f.read()
    has_faq = '{{< faq >}}' in content
    has_disclaimer = '{{< medical-disclaimer />}}' in content
    has_datetime = 'datetime' in content
    has_date_ph = '{date}' in content
    footer_lines = [l.strip() for l in content.split('\n') if '本文基于' in l or 'synthesizes' in l]
    result = f'{lang}: faq={has_faq}, disclaimer={has_disclaimer}, datetime={has_datetime}, {{date}}={has_date_ph}\n'
    for fl in footer_lines:
        result += f'  footer: {fl[:100]}\n'
    with open(r'E:\git_local\beauty-blog\tmp_verify_result.txt', 'a') as f:
        f.write(result)
