import os
path_zh = r'E:\git_local\beauty-blog\content\zh-cn\posts\plastic-surgery-subfields-deep-analysis-2026-07.md'
path_en = r'E:\git_local\beauty-blog\content\en\posts\plastic-surgery-subfields-deep-analysis-2026-07.md'
result = []
for lang, path in [('zh', path_zh), ('en', path_en)]:
    if not os.path.exists(path):
        result.append(f'{lang}: NOT FOUND')
        continue
    size = os.path.getsize(path)
    with open(path, encoding='utf-8') as f:
        content = f.read()
    has_faq = '{{< faq >}}' in content
    has_disc = '{{< medical-disclaimer />}}' in content
    has_dt = 'datetime' in content
    footer = [l for l in content.split('\n') if '本文基于' in l or 'synthesizes' in l]
    result.append(f'{lang}: size={size} faq={has_faq} disc={has_disc} dt={has_dt}')
    for fl in footer:
        result.append(f'  footer: {fl[:120]}')
with open(r'E:\git_local\beauty-blog\tmp_verify2.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(result))
