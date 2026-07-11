# Skill: medical-aesthetics-deep-analysis

Create bilingual (zh-cn + en) medical-aesthetics deep-analysis articles for the beauty-blog Hugo site.

## When to Use

Use this skill when creating a new "deep-analysis" article in the medical aesthetics domain — e.g., breast augmentation, rhinoplasty, eye surgery, facial contouring, liposuction, hair transplantation, etc.

## Workflow

1. **Research** — Gather 20 recent sources: 10 PubMed academic articles + 10 Zhihu community discussions + industry reports (ASPS, Allure, FDA, ISAPS). Use web search and PubMed search.
2. **Images** — Source 5-6 images from Pexels (Pexels License). Download to `static/images/posts/<topic>-aesthetics-YYYY-MM/image-N.jpg`. Update `static/images/CREDITS.md`.
3. **Write zh-cn article** — `content/zh-cn/posts/<topic>-aesthetics-deep-analysis-YYYY-MM.md`
4. **Write en article** — `content/en/posts/<topic>-aesthetics-deep-analysis-YYYY-MM.md` (same filename, translated content)
5. **Verify** — Run `hugo build` to confirm no errors.

## File Naming

- Article slug: `<topic>-aesthetics-deep-analysis-YYYY-MM` (e.g., `breast-augmentation-aesthetics-deep-analysis-2026-07`)
- Image folder: `<topic>-aesthetics-YYYY-MM` (e.g., `breast-augmentation-aesthetics-2026-07`)
- Both zh-cn and en versions share the **same filename** and **same image folder**

## YAML Frontmatter Template

### zh-cn version

```yaml
---
title: "YYYY 年 M 月[主题]医美深度分析：[副标题关键词列表]"
date: YYYY-MM-DD
lastmod: YYYY-MM-DD
description: "[主题]医美深度分析：[关键词列表]。N+ 权威来源。"
categories: ["行业资讯"]
tags: ["[标签1]", "[标签2]", ...]  # 5-8 tags
keywords: ["[关键词1]", "[关键词2]", ...]  # 8-9 keywords
draft: false
featuredImage: "/images/posts/<topic>-aesthetics-YYYY-MM/image-1.jpg"
author: "Beauty-Blog 医学审核团队"
reviewer: "执业医师审核"
lastReviewed: "YYYY-MM-DD"
medicalAudience: "Patient"
translations:
  - "/en/posts/<topic>-aesthetics-deep-analysis-YYYY-MM"
---
```

### en version

```yaml
---
title: "[Topic] Deep Analysis — Month YYYY: [Subtitle]"
date: YYYY-MM-DD
lastmod: YYYY-MM-DD
description: "[Topic] deep dive: [keyword list]. N+ sources."
categories: ["Industry News"]
tags: ["[tag1]", "[tag2]", ...]  # 5-8 tags (English)
keywords: ["[keyword1]", "[keyword2]", ...]  # 8-9 keywords (English)
draft: false
featuredImage: "/images/posts/<topic>-aesthetics-YYYY-MM/image-1.jpg"
author: "Beauty-Blog Medical Review Board"
reviewer: "Licensed Physician Review"
lastReviewed: "YYYY-MM-DD"
medicalAudience: "Patient"
translations:
  - "/posts/<topic>-aesthetics-deep-analysis-YYYY-MM"
---
```

### Frontmatter Rules

- `translations` field: zh-cn points to `/en/posts/<slug>`, en points to `/posts/<slug>` (no `/zh-cn/` prefix because zh-cn is default language)
- `categories`: use `行业资讯` / `Industry News` for deep-analysis articles (topic-specific categories also acceptable for breast/body articles)
- `author`: `Beauty-Blog 医学审核团队` / `Beauty-Blog Medical Review Board`
- `reviewer`: `执业医师审核` / `Licensed Physician Review`
- `medicalAudience`: always `"Patient"`
- `draft`: always `false`
- `featuredImage`: always `/images/posts/<folder>/image-1.jpg`
- `description` (zh): ends with `N+ 权威来源。`
- `description` (en): ends with `N+ sources.`

## Article Body Structure

Body order (both languages, identical structure):

### 1. Opening Figure + Medical Disclaimer

```markdown
{{< figure src="/images/posts/<folder>/image-2.jpg" title="[Opening caption]" >}}

{{< medical-disclaimer />}}
```

### 2. Intro Paragraph

Describes the structural shifts in the field. Ends with source count:

- **zh-cn**: `本期深度分析基于 N 条最新素材（PubMed 学术文献 X 篇 + 知乎专业讨论 Y 篇），并结合 ASPS、Allure 等行业资料综合整理。`
- **en**: `This analysis synthesizes N recent sources (X PubMed-indexed articles + Y Zhihu community discussions) alongside ASPS, Allure, and industry materials.`

### 3. Key Takeaways / 核心要点

```markdown
## 核心要点          (zh-cn)
## Key Takeaways     (en)
```

5-6 bullet points, each with `[^N]` footnote citations.

### 4. Main Analysis Sections (3-5 sections)

Each section:
- `## ` heading with descriptive title (often with colon subtitle)
- Prose with inline `[^N]` footnote citations
- One `{{< figure src="/images/posts/<folder>/image-N.jpg" title="Caption" >}}` shortcode

Figure image assignment: image-2 (opening), image-3 through image-5 (or image-6) in section order.

### 5. FAQ Section

```markdown
## 常见问题解答       (zh-cn)
## Frequently Asked Questions  (en)

{{< faq >}}
- **Question 1?** Answer with [^ref] citations.
- **Question 2?** Answer...
- **Question 3?** Answer...
- **Question 4?** Answer...
- **Question 5?** Answer...
- **Question 6?** Answer...
{{< /faq >}}
```

**FAQ shortcode parsing rules (CRITICAL)**:
- Each Q&A on its own line, starting with `- **`
- Format: `- **Question text** Answer text` or `- **Question**: Answer`
- Parser splits on `**`: parts[1] = question, parts[2] = answer
- Answer is markdownified — can contain links, `[^N]` refs
- Typically 6 Q&As

### 6. References Section

```markdown
## 参考资料      (zh-cn)
## References    (en)

[^1]: [Title](URL) — *Publisher* (Date).
[^2]: [Title](URL) — *Publisher* (Date).
[^3]: [Article Title](https://pubmed.ncbi.nlm.nih.gov/PMID/). *Journal* (2026; Article Type).
...
[^N]: [Title](https://zhuanlan.zhihu.com/p/...) — 知乎答主 Name（N 赞）.
```

Reference ordering: industry sources first ([^1], [^2]), then PubMed, with Zhihu interspersed.

**Three reference source types**:
- **Industry/authority**: ASPS, Allure, FDA, ISAPS — `[^N]: [Title](URL) — *Publisher* (Date).`
- **PubMed academic**: — `[^N]: [Article Title](https://pubmed.ncbi.nlm.nih.gov/PMID/). *Journal* (2026; Article Type).`
- **Zhihu discussions** (zh-cn): — `[^N]: [Title](URL) — 知乎答主 Name（N 赞）.`
  - en version: — `Zhihu contributor Name.` (no thumbs-up count)

### 7. Closing Disclaimer

After `---` horizontal rule:

- **zh-cn**: `*本文基于 [date] 前后的 PubMed 学术文献、知乎专业讨论、ASPS / FDA / NMPA 公开资料综合整理，仅供医学知识科普用途。任何医美决策，请咨询具备资质的执业医师。*`
- **en**: `*This article synthesizes PubMed-indexed literature, Zhihu professional discussions, and public material from ASPS / ISAPS / FDA around [date], for educational purposes only. For any aesthetic-medicine decision, please consult a qualified licensed physician.*`

## Section Header Mapping

| zh-cn | en |
|---|---|
| `## 核心要点` | `## Key Takeaways` |
| `## 常见问题解答` | `## Frequently Asked Questions` |
| `## 参考资料` | `## References` |

## Image Conventions

- Images from **Pexels** (Pexels License)
- Folder: `static/images/posts/<topic>-aesthetics-YYYY-MM/`
- Files: `image-1.jpg` (cover/featuredImage) through `image-5.jpg` or `image-6.jpg`
- Both zh-cn and en share the **same** image paths
- **CREDITS.md**: Append rows to `static/images/CREDITS.md` for each new image:

```
| `posts/<folder>/image-N.jpg` | <source-url> | Pexels License | <author> | <author-url> | YYYY-MM-DD |
```

## Hugo Shortcodes Reference

- `{{< medical-disclaimer />}}` — self-closing, auto-selects language variant
- `{{< figure src="..." title="..." >}}` — Hugo built-in, use only `src` + `title`
- `{{< faq >}}` ... `{{< /faq >}}` — wrapping block, parses `- **Q** A` lines, emits FAQPage JSON-LD

## Verification

After creating articles, verify the Hugo build:

```bash
hugo --gc --minify 2>&1 | Select-String -Pattern "Error|WARN"
```

If Hugo is not installed locally, check if `npx hugo` or the CI build command works.
