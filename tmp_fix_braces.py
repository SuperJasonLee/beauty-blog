with open(r'E:\git_local\beauty-blog\scripts\crawl-plastic-surgery-subfields-2026-07\post_generator.py', encoding='utf-8') as f:
    content = f.read()

import re
# Replace {{< that is NOT preceded by { (i.e. not already {{{{< )
fixed = re.sub(r'(?<!\{)\{\{<', '{{{{<', content)
# Also replace >}} that is NOT followed by } (i.e. not already >}}}})
fixed = re.sub(r'>\}\}(?!\})', '>}}}}', fixed)

count_before = content.count('{{<')
count_after = fixed.count('{{<')
count_quad = fixed.count('{{{{<')
print(f'Double-brace {{< before: {count_before}, after: {count_after}, quadruple-brace {{{{<: {count_quad}')

with open(r'E:\git_local\beauty-blog\scripts\crawl-plastic-surgery-subfields-2026-07\post_generator.py', 'w', encoding='utf-8') as f:
    f.write(fixed)
print('Done!')
