## Why

The site currently publishes themed news roundups (eye-surgery-news, breast-augmentation-news, xiaohongshu-trends) but has no deep-analysis content in the high-demand **weight-loss + medical-aesthetics** intersection — a domain where GLP-1 drugs, body contouring, and post-massive-weight-loss surgery are reshaping patient demand. There is also no documented, reusable SEO + GEO (Generative Engine Optimization, for AI search citation) meta approach applied to these articles, so every new post reinvents the meta block. This change adds (a) one new deeply analyzed article covering the latest weight-loss-aesthetics news and (b) the SEO + GEO meta pattern, codified as a spec, so future posts in this domain inherit it.

## What Changes

- Add a new deep-analysis article (zh-cn primary + en translation) at `content/{zh-cn,en}/posts/weight-loss-aesthetics-deep-analysis-2026-06.md` that synthesizes the latest 2026 weight-loss-aesthetics news (GLP-1, body contouring, post-MWL surgery, regulatory updates) with sourced citations.
- Acquire and persist 3–5 license-permitted images (CC0/CC-BY/Unsplash/Pexels/Pixabay) under `static/images/posts/weight-loss-aesthetics-2026-06/` and reference them in the article body + front matter (`featuredImage`).
- Apply an SEO + GEO meta pattern to the new article: front-matter `description` ≤ 160 chars, `keywords` array, an explicit FAQ block, a `## Key Takeaways` / `## 常见问题` block, a sourced `## 参考资料` block, and a JSON-LD `Article` + `FAQPage` payload (added via Hugo front matter or layout hook) so the page is citable by both Google and generative search engines (Perplexity, SGE, Bing Copilot, ChatGPT browse).
- Add a crawl pipeline under `scripts/crawl-weight-loss-aesthetics-news/` mirroring the existing `crawl-eye-surgery-news/` structure (crawler → image downloader → post generator) so future weight-loss posts can be regenerated. The new pipeline is **not** wired into `daily-publish.sh` (out of scope for this change) — it is invoked manually.
- Document the SEO + GEO meta pattern in `docs/seo-geo-meta.md` so editors can apply it to future posts.

## Capabilities

### New Capabilities
- `weight-loss-aesthetics-article`: The new deep-analysis article (zh-cn + en), its required structural elements (intro, 4–6 themed sections, FAQ, references, image placement, front-matter fields), and the content-coverage scope (GLP-1 + body contouring + post-MWL surgery + regulatory).
- `weight-loss-aesthetics-crawl-pipeline`: A Python pipeline (`scripts/crawl-weight-loss-aesthetics-news/`) that uses `opencli` to pull recent weight-loss-aesthetics news from PubMed / Google / Zhihu, downloads source-permitted images, and emits a draft post — replicating the existing `crawl-eye-surgery-news/` pattern.
- `seo-geo-meta-pattern`: A reusable SEO + GEO meta pattern for editorial posts: front-matter `description` (≤ 160 chars), `keywords` (5–10), an explicit `Key Takeaways` block, an `FAQ` block, a `## 参考资料` block, and a JSON-LD `Article` + `FAQPage` schema injection. Documented in `docs/seo-geo-meta.md`.

### Modified Capabilities
None — existing specs (`featured-image-sourcing`, `featured-image-uniqueness`, `head-partial`, `nebula-animation`) are not changing in requirement. The new article inherits those specs' requirements (e.g., permitted licenses, unique SHA-256 cover, etc.).

## Impact

- `content/zh-cn/posts/weight-loss-aesthetics-deep-analysis-2026-06.md` (new)
- `content/en/posts/weight-loss-aesthetics-deep-analysis-2026-06.md` (new)
- `static/images/posts/weight-loss-aesthetics-2026-06/` (new directory, 3–5 images)
- `static/images/CREDITS.md` (append 3–5 rows)
- `scripts/crawl-weight-loss-aesthetics-news/` (new — `crawler.py`, `image_downloader.py`, `post_generator.py`, `run.py`, `requirements.txt`, `README.md`)
- `package.json` (add `crawl:weight-loss-aesthetics` script)
- `docs/seo-geo-meta.md` (new)
- `data/crawled/weight-loss-aesthetics-news/` (new — JSON output of the crawl step, plus a `crawled_urls.json` dedup file)
- `layouts/partials/seo-geo-schema.html` (new — partial that emits JSON-LD `Article` + `FAQPage`; consumed by `head-partial` capability but does not modify that spec)
