with open(r'E:\git_local\beauty-blog\scripts\crawl-plastic-surgery-subfields-2026-07\post_generator.py', encoding='utf-8') as f:
    content = f.read()

# Add [^6] before 76.4% in ZH body
old_zh = '76.4%–84.0% 的脂肪存活率'
new_zh = '[^6] 76.4%–84.0% 的脂肪存活率'
if old_zh in content:
    content = content.replace(old_zh, new_zh, 1)
    print('ZH CAL fix done')
else:
    print('ZH CAL NOT FOUND')

# Add [^6] before 76.4% in EN body  
old_en = 'achieves 76.4%–84.0% 12-month'
new_en = 'achieves[^6] 76.4%–84.0% 12-month'
if old_en in content:
    content = content.replace(old_en, new_en, 1)
    print('EN CAL fix done')
else:
    print('EN CAL NOT FOUND')

with open(r'E:\git_local\beauty-blog\scripts\crawl-plastic-surgery-subfields-2026-07\post_generator.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
