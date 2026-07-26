with open(r'E:\git_local\beauty-blog\scripts\crawl-plastic-surgery-subfields-2026-07\post_generator.py', encoding='utf-8') as f:
    content = f.read()

# Check the current state of the file
import re
# Find all instances of {{< 
positions = [m.start() for m in re.finditer(r'\{\{<', content)]
print(f"Total occurrences of '{{{{<': {len(positions)}")
for pos in positions[:5]:
    ctx = content[max(0,pos-10):pos+20]
    print(f"  pos={pos}: {repr(ctx)}")

# Now count different brace patterns
print(f"\n'{{{{<': {content.count('{{{{<')}")
print(f"'{{<' preceded by another {{: {content.count('{{{{<')}")
# Check for single {{<
single = content.count('{{<')
quad = content.count('{{{{<')
print(f"'{{<' total: {single}, '{{{{<' total: {quad}")
# Single minus quad = bare {{< that needs fixing
bare = single - quad
print(f"Bare '{{<' that need escaping: {bare}")
