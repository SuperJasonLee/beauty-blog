with open('E:/git_local/beauty-blog/scripts/crawl-rhinoplasty-news/post_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if 'description' in line and '{description}' in line:
        print(f'Line {i}: {line[:100]}')
