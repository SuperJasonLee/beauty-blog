with open(r'E:\git_local\beauty-blog\scripts\crawl-plastic-surgery-subfields-2026-07\post_generator.py', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Add date_cn before body assignment
old1 = '    body = f"""{{{{< medical-disclaimer />}}}}\n'
new1 = '    date_cn = f"{date.today().year} \u5e74 {date.today().month} \u6708"\n    body = f"""{{{{< medical-disclaimer />}}}}\n'
if old1 in content:
    content = content.replace(old1, new1, 1)
    print('Fix 1 done')
else:
    print('Fix 1 NOT FOUND')

# Fix 2: Replace {date} with {date_cn} in body strings
old2 = '*本文基于 {date} 前后的 PubMed 学术文献'
new2 = '*本文基于 {date_cn} 前后的 PubMed 学术文献'
count = content.count(old2)
if count > 0:
    content = content.replace(old2, new2, count)
    print(f'Fix 2 done: replaced {count} occurrences')
else:
    print('Fix 2 NOT FOUND')

# Fix 3: Remove .replace() call
old3 = '"""\n'.replace('"""', '\\"\\"\\"') + '.replace("{date}", f"{date.today().year} \u5e74 {date.today().month} \u6708")\n'
new3 = '"""\n'
if old3.replace('"""', '\\"\\"\\"') in content:
    content = content.replace(old3.replace('"""', '\\"\\"\\"'), new3, 2)
    print('Fix 3 done')
else:
    # Try another approach
    import re
    pattern = r'"""\.replace\("\{date\}", f"\{date\.today\(\)\.year\} 年 \{date\.today\(\)\.month\} 月"\)\n'
    m = re.search(pattern, content)
    if m:
        content = content[:m.start()] + '"""\n' + content[m.end():]
        print('Fix 3 done (regex)')
    else:
        print('Fix 3 NOT FOUND, checking...')
        # Show context
        idx = content.find('.replace("{date}"')
        if idx >= 0:
            print(f'  Found at pos {idx}: {repr(content[max(0,idx-30):idx+60])}')

with open(r'E:\git_local\beauty-blog\scripts\crawl-plastic-surgery-subfields-2026-07\post_generator.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
