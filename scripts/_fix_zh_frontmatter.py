"""Regenerate zh-cn frontmatter for plastic-surgery-subfields post with clean UTF-8 encoding."""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent
path = REPO / "content" / "zh-cn" / "posts" / "plastic-surgery-subfields-deep-analysis-2026-07.md"

with open(path, "r", encoding="utf-8-sig") as f:
    raw = f.read()

m = re.match(r"^(---\s*\n)(.*?)(\n---\s*\n)(.*)$", raw, re.DOTALL)
if not m:
    print("Cannot split frontmatter")
    sys.exit(1)

sep = m.group(3)
body = m.group(4)

# Write fresh, clean frontmatter
new_fm = '''\
title: "2026年整形美容八大细分领域深度分析：眼部·鼻部·唇部·隆胸·减肥·瘦脸·私密·畸形矫正前沿趋势"
date: 2026-07-30
lastmod: 2026-07-30
description: "2026年整形美容八大细分领域深度分析：眼部、鼻部、唇部、隆胸、减肥、瘦脸、私密、畸形矫正的前沿技术与安全趋势。"
categories: ["行业资讯"]
tags: ["眼部整形", "鼻综合", "唇部填充", "隆胸", "减肥体雕", "瘦脸", "私密整形", "畸形矫正", "医美前沿"]
keywords: ["眼部整形 眼综合", "鼻综合 肋软骨", "唇部填充 玻尿酸", "隆胸 假体 干细胞", "GLP-1 体雕", "瘦脸针 咬肌", "私密整形 labiaplasty", "畸形矫正 颅颌面"]
draft: false
featuredImage: "/images/posts/plastic-surgery-subfields-2026-07/image-1.jpg"
author: "Beauty-Blog 医学审核团队"
reviewer: "执业医师审核"
lastReviewed: "2026-07-30"
medicalAudience: "Patient"
translations:
  - "/en/posts/plastic-surgery-subfields-deep-analysis-2026-07"
'''

new_content = "---\n" + new_fm + sep + body

with open(path, "w", encoding="utf-8-sig") as f:
    f.write(new_content)

# Verify: can Python yaml parse it?
try:
    import yaml
    fm_parsed = yaml.safe_load(new_fm)
    print("Frontmatter YAML parse OK")
    print("tags:", fm_parsed.get("tags"))
    print("translations:", fm_parsed.get("translations"))
except Exception as e:
    print(f"YAML parse still fails: {e}")

print("zh-cn frontmatter regenerated")
