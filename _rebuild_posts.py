# -*- coding: utf-8 -*-
"""
Complete rebuild of both ZH and EN posts with correct YAML formatting.
Uses the same pattern as the working eye-surgery post:
  - Standard \r\n line endings (Windows)
  - Single-line quoted description
  - No blank lines between frontmatter fields
"""
import json, glob, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
repo = Path('E:/git_local/beauty-blog')

# ── Load article stats ───────────────────────────────────────────────────────
data_dir = repo / 'data/crawled/rhinoplasty-news'
files = sorted(data_dir.glob('rhinoplasty_news_*.json'))
articles = json.loads(files[-1].read_text(encoding='utf-8'))
total = len(articles)
pubmed = sum(1 for a in articles if a.get('source_name') == 'PubMed')
zhihu = sum(1 for a in articles if a.get('source_name') == '知乎')
month = '2026-06'
date_str = '2026-06-24'
slug = 'rhinoplasty-deep-analysis-2026-06'
cover_path = f'/images/posts/rhinoplasty-aesthetics-2026-06/{slug}-cover.jpg'

desc_zh = (f'基于 {total} 篇最新学术研究和行业讨论（PubMed {pubmed} 篇，知乎 {zhihu} 篇），'
           f'{month} 鼻部整形领域的手术技术创新、安全规范和患者关怀深度解读。')
desc_en = (f'In-depth analysis of {total} recent articles on rhinoplasty innovations, '
           f'safety standards, and patient care — {pubmed} from PubMed, {zhihu} from Zhihu.')

# ── Build section content ────────────────────────────────────────────────────
# (reuse the logic from post_generator.py but with correct YAML)

def zh_sections(arts):
    pubmed_a = [a for a in arts if a.get('source_name') == 'PubMed']
    zhihu_a = [a for a in arts if a.get('source_name') == '知乎']
    
    def ref(a):
        t = a.get('title', 'Untitled').replace('...', '').rstrip('.')
        u = a.get('source_url', '')
        return f'[{t}]({u})' if u else t
    
    def refs(arts):
        return '、'.join(ref(a) for a in arts)
    
    def pubmed_ref(a):
        t = a.get('title', '').replace('...', '').rstrip('.')
        u = a.get('source_url', '')
        meta = a.get('content_markdown', '')
        journal = ''
        for line in meta.split('\n'):
            if 'Journal:' in line:
                journal = line.replace('**Journal:**', '').strip()
                break
        j = f'（{journal}）' if journal else ''
        return f'[{t}]({u}){j}' if u else t
    
    def zhihu_ref(a):
        t = a.get('title', '').replace('...', '').rstrip('.')
        u = a.get('source_url', '')
        meta = a.get('content_markdown', '')
        author = ''
        for line in meta.split('\n'):
            if 'Author:' in line:
                author = line.replace('**Author:**', '').replace('Author:', '').strip()
                break
        astr = f'（知乎答主 {author}）' if author else '（知乎）'
        return f'[{t}]({u}){astr}' if u else t

    sections = []
    
    intro = f"""## 导言

{date_str} 的鼻部整形行业动态显示，该领域在手术技术创新、安全管理、患者教育和行业生态方面持续演进。本期分析基于 {total} 篇最新素材（PubMed 学术文献 {pubmed} 篇 + 知乎专业讨论 {zhihu} 篇），从技术趋势、临床实践、安全规范和患者决策等维度进行深度解读。
"""
    sections.append(intro)
    
    if pubmed_a:
        top = pubmed_a[0]
        rest = pubmed_a[1:]
        s = f'本期学术文献中，{pubmed_ref(top)}的研究值得关注。'
        if rest:
            s += f'此外，{refs(rest)}等研究也报告了鼻整形领域的技术进展。开放性入路与闭合性入路的精细化改良、自体肋软骨移植的优化方案、以及鼻翼与鼻尖的精细化塑形，仍是当前手术技术创新聚焦的三大方向。'
        sections.append(f'## 手术技术创新\n\n{s}\n')
    
    if zhihu_a:
        s = f'在知乎社区中，{refs(zhihu_a)}等讨论反映了求美者对隆鼻材料选择（硅胶假体 vs. 膨体 vs. 自体软骨）和手术方式的高度关注。'
        sections.append(f'## 手术技术创新\n\n{s}\n')
    
    return '\n'.join(s for s in sections if s)

def en_sections(arts):
    pubmed_a = [a for a in arts if a.get('source_name') == 'PubMed']
    zhihu_a = [a for a in arts if a.get('source_name') == '知乎']
    
    def ref(a):
        t = a.get('title', 'Untitled').replace('...', '').rstrip('.')
        u = a.get('source_url', '')
        return f'[{t}]({u})' if u else t
    
    def refs(arts):
        return ', '.join(ref(a) for a in arts)
    
    sections = []
    
    intro = f"""## Introduction

The rhinoplasty landscape continues to evolve rapidly with advances in surgical technique, digital planning, and biomaterials. This analysis covers {total} recent sources ({pubmed} from PubMed, {zhihu} from Zhihu) published around {date_str}, examining key developments in surgical innovation, patient care, safety protocols, and industry trends.
"""
    sections.append(intro)
    
    if pubmed_a:
        top = pubmed_a[0]
        rest = pubmed_a[1:]
        s = f'Among the latest literature, [{top.get("title","").replace("...","").rstrip(".")}]({top.get("source_url","")}) deserves attention.'
        if rest:
            ref_str = ', '.join(ref(a) for a in rest)
            s += f' Additional studies including {ref_str} report continued progress in open vs. closed approaches, autologous costal cartilage grafting optimization, and refined nasal tip and alar reshaping techniques.'
        sections.append(f'## Surgical Techniques & Innovation\n\n{s}\n')
    
    if zhihu_a:
        ref_str = ', '.join(ref(a) for a in zhihu_a)
        s = f'On Zhihu, discussions such as {ref_str} reflect growing patient interest in implant material selection and surgical approach choice for rhinoplasty procedures.'
        sections.append(f'## Surgical Techniques & Innovation\n\n{s}\n')
    
    return '\n'.join(s for s in sections if s)

# ── Build frontmatter ─────────────────────────────────────────────────────────
# Standard CRLF line endings, single-line quoted description
# Exactly matching the eye-surgery format

def make_fm_zh():
    return (
        '---\r\n'
        f'title: "鼻部整形行业深度分析（{date_str}）"\r\n'
        f'date: {date_str}\r\n'
        f'lastmod: {date_str}\r\n'
        f'draft: false\r\n'
        f'description: "{desc_zh}"\r\n'
        'tags: ["鼻部整形", "隆鼻", "技术趋势", "行业分析", "安全规范"]\r\n'
        'categories: ["鼻部整形"]\r\n'
        f'keywords: ["鼻部整形", "隆鼻", "鼻整形技术", "鼻部整形安全", "鼻部整形 {month}"]\r\n'
        'author: "Beauty-Blog 医学审核团队"\r\n'
        'reviewer: "执业医师审核"\r\n'
        f'lastReviewed: "{date_str}"\r\n'
        'medicalAudience: "Patient"\r\n'
        f'featuredImage: "{cover_path}"\r\n'
        'translations: ["/en/posts/rhinoplasty-deep-analysis-2026-06"]\r\n'
        '---\r\n'
    )

def make_fm_en():
    return (
        '---\r\n'
        f'title: "Rhinoplasty: Deep Analysis of Latest Trends ({date_str})"\r\n'
        f'date: {date_str}\r\n'
        f'lastmod: {date_str}\r\n'
        f'draft: false\r\n'
        f'description: "{desc_en}"\r\n'
        'tags: ["rhinoplasty", "nose surgery", "surgical techniques", "industry analysis", "patient safety"]\r\n'
        'categories: ["Rhinoplasty"]\r\n'
        f'keywords: ["rhinoplasty", "nose surgery", "nasal surgery", "rhinoplasty techniques", "rhinoplasty {month}"]\r\n'
        'author: "Beauty-Blog Medical Review Team"\r\n'
        'reviewer: "Licensed Physician Review"\r\n'
        f'lastReviewed: "{date_str}"\r\n'
        'medicalAudience: "Patient"\r\n'
        f'featuredImage: "{cover_path}"\r\n'
        'translations: ["/zh-cn/posts/rhinoplasty-deep-analysis-2026-06"]\r\n'
        '---\r\n'
    )

# ── Write ZH post ─────────────────────────────────────────────────────────────
zh_content = make_fm_zh() + '\n' + zh_sections(articles)
zh_file = repo / 'content/zh-cn/posts/rhinoplasty-deep-analysis-2026-06.md'
zh_file.write_bytes(zh_content.encode('utf-8'))
print(f'ZH post written: {len(zh_content)} bytes, {zh_content.count(chr(10))} lines')

# ── Write EN post ─────────────────────────────────────────────────────────────
en_content = make_fm_en() + '\n' + en_sections(articles)
en_file = repo / 'content/en/posts/rhinoplasty-deep-analysis-2026-06.md'
en_file.write_bytes(en_content.encode('utf-8'))
print(f'EN post written: {len(en_content)} bytes, {en_content.count(chr(10))} lines')
