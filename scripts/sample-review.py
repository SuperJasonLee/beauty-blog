"""Sample review: verify footnote URLs are well-formed across 5 representative posts."""
import re
from pathlib import Path
from urllib.parse import urlparse

samples = [
    "content/zh-cn/posts/blepharoplasty-guide.md",
    "content/zh-cn/posts/medical-aesthetics-news-may-31-2026.md",
    "content/zh-cn/posts/xiaohongshu-hot-may-2026.md",
    "content/zh-cn/posts/eye-surgery-news/eye-surgery-news-20260601.md",
    "content/zh-cn/posts/breast-augmentation-news-may-2026.md",
    "content/en/posts/rhinoplasty-guide.md",
    "content/en/posts/aesthetic-news-may-2026.md",
]

url_re = re.compile(r"<https?://[^>]+>")
footnote_re = re.compile(r"\[\^\d+\]:\s*(.+)")

print(f"{'File':<55} {'FN':>3}  {'URLs':>5}  {'OK'}")
print("-" * 80)
total_issues = 0
for p in samples:
    text = Path(p).read_text(encoding='utf-8')
    fns = footnote_re.findall(text)
    issues = []
    for fn in fns:
        urls = url_re.findall(fn)
        for u in urls:
            parsed = urlparse(u.strip('<>').strip())
            if not parsed.netloc or '.' not in parsed.netloc:
                issues.append(f"  bad URL: {u}")
    print(f"{p.split('content/')[-1]:<55} {len(fns):>3}  {sum(len(url_re.findall(f)) for f in fns):>5}  {'OK' if not issues else 'FAIL'}")
    for i in issues:
        print(i)
    total_issues += len(issues)

# FAQ rendering check
print()
print("FAQ rendering check (5+ items expected for guides/news)")
faq_re = re.compile(r"\{\{<\s*faq\s*>\}\}(.+?)\{\{<\s*/faq\s*>\}\}", re.DOTALL)
item_re = re.compile(r"^- \*\*(.+?)\*\*", re.MULTILINE)
for p in samples:
    text = Path(p).read_text(encoding='utf-8')
    faq_blocks = faq_re.findall(text)
    if faq_blocks:
        items = item_re.findall(faq_blocks[0])
        ok = "OK" if len(items) >= 3 else "TOO FEW"
        print(f"  {p.split('content/')[-1]:<55} {len(items):>3} items  {ok}")
    else:
        print(f"  {p.split('content/')[-1]:<55} (no FAQ)")

print()
print(f"Total URL issues: {total_issues}")
