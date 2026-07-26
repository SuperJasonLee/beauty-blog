with open(r'E:\git_local\beauty-blog\scripts\crawl-plastic-surgery-subfields-2026-07\post_generator.py', encoding='utf-8') as f:
    content = f.read()

# Fix EN body footer
old = '*This analysis synthesizes PubMed-indexed literature, Zhihu professional discussions, and public material from ASPS / ISAPS / FDA around {date}, for educational purposes only.'
new = '*This analysis synthesizes PubMed-indexed literature, Zhihu professional discussions, and public material from ASPS / ISAPS / FDA around {date_en}, for educational purposes only.'
if old in content:
    content = content.replace(old, new, 1)
    print('Fix EN footer ref done')
else:
    print('EN footer ref NOT FOUND')

old2 = '"""\n'.replace('"""', '\\"\\"\\"') + '.replace("{date}", f"{date.today().strftime(\'%B %Y\')}")'
new2 = '"""\n'
if old2.replace('"""', '\\"\\"\\"') in content:
    content = content.replace(old2.replace('"""', '\\"\\"\\"'), new2, 1)
    print('Fix EN replace() done')
else:
    print('EN replace() NOT FOUND, checking...')
    idx = content.find('.replace("{date}"')
    if idx >= 0:
        print(f'  Found at pos {idx}: {repr(content[max(0,idx-20):idx+60])}')

# Also add date_en before build_en_post
old3 = 'def build_en_post(refs'
new3 = '    date_en = f"{date.today().strftime(\'%B %Y\')}"\ndef build_en_post(refs'
if old3 in content:
    content = content.replace(old3, new3, 1)
    print('Fix EN date_en added')
else:
    print('EN date_en NOT FOUND')

with open(r'E:\git_local\beauty-blog\scripts\crawl-plastic-surgery-subfields-2026-07\post_generator.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
