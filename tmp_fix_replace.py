with open(r'E:\git_local\beauty-blog\scripts\crawl-plastic-surgery-subfields-2026-07\post_generator.py', encoding='utf-8') as f:
    content = f.read()

idx = content.find('.replace("{date}"')
if idx >= 0:
    print(f'Found at {idx}: {repr(content[max(0,idx-5):idx+70])}')
    # Find the exact replace string
    start = content.rfind('\n', 0, idx)
    end = content.find('\n', idx)
    exact = content[start+1:end]
    print(f'Exact line: {repr(exact)}')
    # Replace it with just the closing triple quote
    new_content = content[:start+1] + '    """' + content[end:]
    with open(r'E:\git_local\beauty-blog\scripts\crawl-plastic-surgery-subfields-2026-07\post_generator.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Fixed!')
else:
    print('NOT FOUND')
