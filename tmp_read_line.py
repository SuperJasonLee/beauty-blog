with open(r'E:\git_local\beauty-blog\content\en\posts\plastic-surgery-subfields-deep-analysis-2026-07.md', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(62, 70):
    print(f'{i+1}: {lines[i].rstrip()[:100]}')
