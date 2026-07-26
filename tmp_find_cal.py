with open(r'E:\git_local\beauty-blog\scripts\crawl-plastic-surgery-subfields-2026-07\post_generator.py', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if '76.4' in line or ('CAL' in line and 'fat' in line.lower()):
        print(f'{i+1}: {repr(line.strip()[:100])}')
