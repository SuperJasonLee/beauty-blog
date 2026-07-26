with open(r'E:\git_local\beauty-blog\scripts\crawl-plastic-surgery-subfields-2026-07\post_generator.py', encoding='utf-8') as f:
    content = f.read()

# Find all instances of {{{{< and >}}}}
import re

# Fix frontmatter: lines that are NOT inside f-strings and have {{{{<
# Strategy: replace {{{{< in frontmatter blocks (after '---\n' and before next '---')
# with {{< 

# Replace the two specific frontmatter lines
fixes = [
    (
        "{{{{< figure src=\"/images/posts/plastic-surgery-subfields-2026-07/image-2.jpg\" title='2026 年整形美容八大细分领域全景：技术前沿、安全动态与消费趋势深度分析' >}}}}",
        "{{< figure src=\"/images/posts/plastic-surgery-subfields-2026-07/image-2.jpg\" title='2026 年整形美容八大细分领域全景：技术前沿、安全动态与消费趋势深度分析' >}}"
    ),
    (
        '{{{{< figure src="/images/posts/plastic-surgery-subfields-2026-07/image-2.jpg" title="2026 deep dive into 8 plastic-surgery subspecialties: frontier tech, safety dynamics, and consumer trends" >}}}}',
        '{{< figure src="/images/posts/plastic-surgery-subfields-2026-07/image-2.jpg" title="2026 deep dive into 8 plastic-surgery subspecialties: frontier tech, safety dynamics, and consumer trends" >}}'
    ),
]

for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        print(f"Fixed: {old[:60]}...")
    else:
        print(f"NOT FOUND: {old[:60]}...")

with open(r'E:\git_local\beauty-blog\scripts\crawl-plastic-surgery-subfields-2026-07\post_generator.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
