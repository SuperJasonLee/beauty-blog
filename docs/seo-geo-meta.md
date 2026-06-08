# SEO + GEO Meta Pattern

This document defines the **SEO + GEO meta pattern** applied to all editorial posts on the
Beauty-Blog site. SEO targets traditional search engines (Google, Bing); **GEO** (Generative
Engine Optimization) targets AI-powered answer engines — Perplexity, Google SGE, Bing Copilot,
ChatGPT browse, Claude with web, etc. — that increasingly cite or summarize content with
explicit extraction signals.

The pattern is enforced by the `seo-geo-meta-pattern` spec and rendered automatically by
`layouts/partials/seo-geo-schema.html`.

---

## Why a combined SEO + GEO pattern

| Audience | What they need |
| --- | --- |
| Google / Bing crawler | Valid HTML, meta description, structured headings, clean URLs |
| SGE / Perplexity / ChatGPT browse | Extractable Q&A blocks, dated references, FAQPage schema, plain-language summaries |
| RSS / aggregator readers | Front-matter `description`, `keywords`, canonical `translations` |
| Human reader | Fast scanning: Key Takeaways, FAQ, References |

The five-element pattern below is optimized to satisfy all four audiences with one
content layout.

---

## The five elements

### 1. Front-matter `description` (≤ 160 chars, primary keyword)

```yaml
---
description: "2026 减肥医美深度分析：GLP-1 减重药、大幅减重后形体雕塑、非侵入式塑形、监管与安全。8+ 权威来源。"
---
```

Rules:
- **Length**: ≤ 160 characters (Google's snippet cap).
- **Primary keyword**: must include the topic's primary keyword in the language of the post
  ("减肥" for zh-cn, "weight loss" for en, etc.).
- **Voice**: declarative, no marketing fluff, no question marks.
- **Bilingual mirror**: the en twin's `description` must include the en equivalent ("weight loss").

### 2. Front-matter `keywords` (5–10 entries)

```yaml
---
keywords: ["减肥 医美", "GLP-1 减重", "司美格鲁肽", "腹壁整形", "post-MWL 手术", "非侵入式塑形", "FDA 监管", "ASPS 2024"]
---
```

Rules:
- **Count**: 5–10 entries. Below 5 looks thin to crawlers; above 10 looks spammy.
- **Mix**: combine primary + long-tail + entity names (drug names, technique names, regulators).
- **Order**: most-searched first; primary keyword at index 0.
- **Bilingual mirror**: en twin translates every entry; do not keep zh-cn terms in en `keywords`.

### 3. `## Key Takeaways` / `## 核心要点` (4–6 bullets)

```markdown
## 核心要点

- GLP-1 减重药正在把"医美需求曲线"前移——大量求美者先以药物减重，再以手术收尾，临床路径被改写。
- 大幅减重后的腹壁整形、胸部上提、埋没阴茎修复需求在 2026 年学术文献中显著增加……
- 学术界已就"GLP-1 围手术期营养与停药窗口"形成初步共识……
- 非侵入式塑形正从"减脂"走向"紧致 + 肌肉重塑"……
- 中国市场对"司美脸""减重药副作用与医美修复"的关注度持续高位……
```

Rules:
- **Headline language**: `## 核心要点` (zh) or `## Key Takeaways` (en).
- **Count**: 4–6 bullets. Below 4 is thin; above 6 dilutes the summary.
- **Shape**: each bullet is one sentence, parallel structure (subject + verb + payoff).
- **Purpose**: this block is the most likely section to be cited verbatim by SGE / Perplexity
  in their answer card.

### 4. `{{< faq >}}` shortcode (4–6 Q&A pairs)

```markdown
{{< faq >}}
- **GLP-1 减重药减重后多久可以做腹壁整形？** 学术共识建议停药 4–6 周后……
- **"司美脸"是什么？应该如何处理？** 面部脂肪流失、皮肤松弛……
- **大幅减重后腹壁整形需要注意什么？** 影像学评估、营养与铁状态……
- **非侵入式塑形现在还安全有效吗？** FDA 安全通讯强调……
{{< /faq >}}
```

Rules:
- **Shortcode**: use the project's `{{< faq >}}` shortcode (do **not** write raw FAQPage JSON-LD
  inline; the partial reads the shortcode body).
- **Count**: 4–6 pairs.
- **Voice**: questions mirror actual People-Also-Ask phrasing (so they match what users type
  into Google/SGE).
- **Bilingual**: the en twin must have its own `{{< faq >}}` block with translated Q&A, not
  machine-translated literal.

### 5. Numbered `## 参考资料` / `## References` (≥ 8 footnotes)

```markdown
## 参考资料

[^1]: Preoperative nutritional resilience in the era of GLP-1 therapy. *Surgery for obesity and related diseases* (2026). <https://pubmed.ncbi.nlm.nih.gov/42248747/>
[^2]: Combining Abdominal Hernia Repair With Abdominoplasty — Is it Safe? *Aesthetic surgery journal. Open forum* (2026). <https://pubmed.ncbi.nlm.nih.gov/42232107/>
…
```

Rules:
- **Format**: numbered Markdown footnotes (`[^N]:`).
- **In-text references**: use `[^N]` markers throughout the body; ≥ 8 distinct footnotes.
- **Per-entry content**: title + publication + date + URL. For PubMed entries, include journal name.
- **Live URLs only**: every footnote URL must return 2xx when verified. The
  `npm run audit:posts` script flags non-2xx URLs as errors.
- **Bilingual**: the en twin gets a parallel `## References` block; the numbering matches the
  zh-cn post (1:1) so editors can cross-reference during review.

---

## Optional: featured + body images

Beyond the five required elements, the pattern also expects:

- A `featuredImage` front-matter field pointing to a permitted-license image
  (`static/images/CREDITS.md` row required).
- At least 3 `{{< figure src="…" title="…" >}}` shortcodes in the body, each pointing to a
  different downloaded image with its own `CREDITS.md` row.

These are enforced by the `featured-image-sourcing` and `featured-image-uniqueness` specs.

---

## Front-matter template (copy-paste)

```yaml
---
title: "<TITLE: 20–80 chars, primary keyword at start>"
date: YYYY-MM-DD
lastmod: YYYY-MM-DD
description: "<=160 chars, primary keyword included>"
categories: ["行业资讯"]   # or ["Industry News"] for en
tags: ["<tag1>", "<tag2>", "<tag3>"]
keywords: ["<kw1>", "<kw2>", "<kw3>", "<kw4>", "<kw5>"]
draft: true
featuredImage: "/images/posts/<slug>/image-1.jpg"
author: "Beauty-Blog 医学审核团队"
reviewer: "执业医师审核"
lastReviewed: YYYY-MM-DD
medicalAudience: "Patient"
translations:
  - "/en/posts/<slug>"
---
```

Replace `Beauty-Blog 医学审核团队` / `执业医师审核` with the en equivalents
(`Beauty-Blog Medical Review Board` / `Licensed Physician Review`) for the en twin.

---

## Editor checklist (apply to every new post)

- [ ] `description` ≤ 160 chars and contains the primary keyword
- [ ] `keywords` has 5–10 entries
- [ ] `## 核心要点` / `## Key Takeaways` has 4–6 bullets
- [ ] `{{< faq >}}` shortcode has 4–6 Q&A pairs
- [ ] `## 参考资料` / `## References` has ≥ 8 numbered footnotes
- [ ] Every footnote URL returns 2xx (`curl -I <url>`)
- [ ] `featuredImage` points to a file in `static/images/CREDITS.md`
- [ ] At least 3 `{{< figure >}}` shortcodes in the body, each backed by a CREDITS.md row
- [ ] `translations:` array points to the bilingual twin (and back)
- [ ] `npm run audit:posts content/<lang>/posts/<slug>.md --severity error` exits 0
- [ ] `npm run audit:images:strict` reports no SHA-256 collision involving `featuredImage`
- [ ] Render the post (Hugo server or `hugo --minify`) and confirm the JSON-LD
      `Article` + `FAQPage` block is in the head

When all 12 boxes are checked, flip `draft: true` to `draft: false` and commit.

---

## What the partial renders

`layouts/partials/seo-geo-schema.html` emits a single `<script type="application/ld+json">`
block in the post's `<head>` containing:

- `Article` schema with `headline`, `description`, `datePublished`, `dateModified`,
  `keywords`, `author`, `image`, `inLanguage`.
- `FAQPage` schema with one `Question` per Q&A pair extracted from the `{{< faq >}}` shortcode.

If the post lacks `description` / `keywords` / a `{{< faq >}}` shortcode, the partial
**silently emits nothing** — it does not throw. This is the graceful-degradation
guarantee required by the `seo-geo-meta-pattern` spec.
