## Context

The site is a Hugo-based bilingual (zh-cn default, en secondary) medical-aesthetics knowledge blog at `https://beauty-blog.cloud-ip.cc/`. It runs on the PaperMod theme with custom nebula backgrounds, GSAP animations, pagefind search, and Google AdSense. Content lives in `content/{zh-cn,en}/posts/`.

There are two existing content-production systems to learn from:

1. **`scripts/crawl-eye-surgery-news/`** — a Python pipeline (crawler → image downloader → post generator) driven by `opencli` shells. It crawls PubMed / Zhihu / Google, downloads images, and emits bilingual draft posts into `content/{zh-cn,en}/posts/eye-surgery-news/`. It is wired into `scripts/daily-publish/daily-publish.sh` for automated 12:00 daily publishing.
2. **Hand-curated news posts** like `aesthetic-medicine-trends-may-2026.md` — long-form roundups that combine 8–11 sourced news items with FAQs, references, and front-matter `keywords` / `featuredImage` / `translations` fields.

What is missing:
- A weight-loss + medical-aesthetics post (the highest-demand cross-section: GLP-1 drugs ↔ body contouring ↔ post-massive-weight-loss surgery)
- A codified SEO + GEO meta pattern reusable across future posts
- A crawl pipeline for the weight-loss domain (the eye-surgery pipeline uses domain-specific opencli commands and a domain-specific dedup JSON, so it does not generalize)

Key files for context:
- `scripts/crawl-eye-surgery-news/{crawler,image_downloader,post_generator,run}.py` — pattern to mirror
- `scripts/crawl-eye-surgery-news/requirements.txt` — `opencli` Python shim
- `scripts/daily-publish/daily-publish.sh` — daily 12:00 trigger; the new pipeline is **not** added here in this change
- `content/zh-cn/posts/aesthetic-medicine-trends-may-2026.md` — front-matter shape and section structure to inherit
- `package.json` `crawl:eye-news` script — pattern for adding `crawl:weight-loss-aesthetics`
- `openspec/specs/featured-image-sourcing/spec.md` — license / CREDITS.md rules the new article must obey
- `openspec/specs/featured-image-uniqueness/spec.md` — SHA-256 uniqueness rule for `featuredImage`
- `static/images/CREDITS.md` — append-only attribution log
- `CONTRIBUTING.md` — front-matter and shortcode rules

## Goals / Non-Goals

**Goals:**
- Publish one new deep-analysis article (zh-cn + en translation) covering 2026 weight-loss + medical-aesthetics news with 4–6 themed sections, a FAQ block, and a fully cited `## 参考资料` block.
- Acquire 3–5 license-permitted images (CC0/CC-BY/Unsplash/Pexels/Pixabay only), log each in `static/images/CREDITS.md`, keep each ≤ 300 KB and ≤ 1600 px on the longest edge.
- Apply a documented SEO + GEO meta pattern to the new article and capture it as a spec so future posts inherit it.
- Add a `scripts/crawl-weight-loss-aesthetics-news/` Python pipeline that mirrors the eye-surgery pipeline structure and emits a draft post, so a future regeneration is one command.
- Add a `package.json` script `crawl:weight-loss-aesthetics` that runs the new pipeline.

**Non-Goals:**
- Wiring the new pipeline into `scripts/daily-publish/daily-publish.sh` (out of scope — manual invocation only this round).
- Modifying existing specs (`featured-image-sourcing`, `featured-image-uniqueness`, `head-partial`, `nebula-animation`).
- Translating existing posts; only the new article gets bilingual.
- Adding new content types or theme changes.

## Decisions

**1. Article scope: "2026-06 weight-loss + medical-aesthetics deep analysis"**
- **Choice**: Frame the article around four themes — (a) GLP-1 (semaglutide/tirzepatide) impact on body-contouring demand, (b) post-massive-weight-loss (MWL) surgery (panniculectomy, fleur-de-lis, 360° abdominoplasty), (c) non-invasive fat reduction (CoolSculpting, Emsculpt Neo, Morpheus8 Body), (d) regulatory + safety (FDA black-box on compounded GLP-1, ASA/ISAPS guidelines).
- **Rationale**: These four themes map 1:1 to high-volume search queries and are what credible sources (ASPS, ISAPS, Allure, PR Newswire) are publishing on. They give the article depth without diluting the topic.
- **Alternative considered**: A single-theme "GLP-1 only" post — rejected as too narrow for a "deep analysis" framing.

**2. Article location and naming**
- **Choice**: `content/zh-cn/posts/weight-loss-aesthetics-deep-analysis-2026-06.md` (primary) and `content/en/posts/weight-loss-aesthetics-deep-analysis-2026-06.md` (translation), with images in `static/images/posts/weight-loss-aesthetics-2026-06/`.
- **Rationale**: Matches the existing `<topic>-<period>` naming convention (e.g., `aesthetic-medicine-trends-may-2026.md`, `aesthetic-news-may-2026.md`). The en post gets the same slug so the `translations:` front-matter line can cross-link.
- **Alternative considered**: Nesting under `content/{zh-cn,en}/posts/weight-loss-aesthetics-news/` (matching the eye-surgery layout) — rejected because the new article is a one-off deep-analysis, not a recurring daily series. A directory makes sense only for ≥ 3 posts on the same domain.

**3. Image acquisition: hybrid opencli + Unsplash/Pexels fallback**
- **Choice**: The crawler emits candidate image URLs from each source article. `image_downloader.py` tries them in order; on 4xx/5xx or non-permitted license it falls back to a curated Unsplash/Pexels search via `opencli unsplash search` / `opencli pexels search` with the topic keyword.
- **Rationale**: News-article images often have unclear or restrictive licenses; a permissive-stock fallback guarantees the post never lands without a hero image while keeping the `featured-image-sourcing` license whitelist intact.
- **Alternative considered**: Stock-only — rejected because news-image candidates are more topic-specific when they work.

**4. SEO + GEO meta pattern (codified in a spec)**
- **Choice**: Apply a fixed shape — front-matter `description` (≤ 160 chars, includes the primary keyword "减肥 医美" and a year), `keywords` array (5–10 items), an explicit `## Key Takeaways` section (5 bullets, single sentence each, parallel structure), an `## FAQ` section (4–6 Q&A pairs that mirror People-Also-Ask phrasing), a `## 参考资料` block (numbered footnotes with URL + publication + date), and a JSON-LD payload of `Article` + `FAQPage` types injected by a new partial `layouts/partials/seo-geo-schema.html` that is invoked from the head partial.
- **Rationale**: Google's SGE, Perplexity, Bing Copilot, and ChatGPT browse all prefer explicit extractable Q&A blocks, dated references, and FAQPage schema for citation. The pattern is broad enough to apply to any future post.
- **Alternative considered**: Inline JSON-LD inside the post body — rejected because it duplicates payload and the partial is the single source of truth.

**5. JSON-LD partial scope: a new partial, not a layout change**
- **Choice**: Add `layouts/partials/seo-geo-schema.html` that reads `description`, `keywords`, `lastmod`, and the post body, extracts FAQ pairs from a `{{< faq >}}` shortcode, and emits `<script type="application/ld+json">…</script>`. The partial is invoked from `layouts/_default/single.html` (or `baseof.html`).
- **Rationale**: Keeps the JSON-LD emission as a side-effect of the article's own front matter, not a hand-coded string in each post. Matches the project's existing partial pattern.
- **Alternative considered**: Per-post inline JSON-LD in the markdown — rejected as unmaintainable.

**6. Crawl pipeline directory and naming**
- **Choice**: `scripts/crawl-weight-loss-aesthetics-news/` with the same `crawler.py / image_downloader.py / post_generator.py / run.py / requirements.txt / README.md` shape as the eye-surgery pipeline. Data lands in `data/crawled/weight-loss-aesthetics-news/` with a `crawled_urls.json` dedup file.
- **Rationale**: Direct mirror of the working eye-surgery pipeline. Editors familiar with that one can immediately run the new one.
- **Alternative considered**: Generalizing the existing pipeline via a config file — rejected because the source adapters (`pubmed`, `zhihu`, `google`) and the `SOURCES` list are domain-specific enough that a single config-driven pipeline would be a significant refactor not justified by a second use site.

**7. `package.json` script name**
- **Choice**: `crawl:weight-loss-aesthetics` (parallel to `crawl:eye-news`).
- **Rationale**: Naming convention is the existing one; one command to invoke the whole pipeline.

## Risks / Trade-offs

- **[Content quality] LLM synthesis can fabricate citations** → Mitigation: All sources must be a real, dated, named publication (Allure, ASPS, FDA, ISAPS, PR Newswire, PubMed). The `post_generator.py` must record the source URL next to every claim. Editor must verify each citation before flipping `draft: true → false`.
- **[Image license drift] opencli source URLs sometimes lack license metadata** → Mitigation: The downloader must check the page HTML / `og:image` URL for a `license` / `cc:` indicator. If absent, it discards the candidate and falls back to the curated Unsplash/Pexels search.
- **[SEO + GEO partial breaking head-partial spec] The new `seo-geo-schema.html` partial is invoked from `layouts/_default/single.html`** → Mitigation: Keep the partial as a no-op when front-matter lacks the required fields (graceful degradation), so the head-partial spec's invariants remain intact.
- **[Bilingual drift] The en translation can lag behind the zh-cn content** → Mitigation: Emit both files from `post_generator.py` in one run, with the same data, and use a single `translations:` front-matter entry pointing to the paired slug.
- **[Crawl pipeline separate from daily-publish] Editors must remember to invoke `npm run crawl:weight-loss-aesthetics` manually** → Mitigation: Document this in the pipeline `README.md` and in `docs/seo-geo-meta.md`.
- **[Image uniqueness vs featured-image-uniqueness spec] The new cover must not collide with an existing post cover** → Mitigation: After download, run `npm run audit:images:strict` and rotate the cover if SHA-256 collides with an existing post.

## Migration Plan

- No data migration. No DB. All new files. Bilingual post goes live when `draft: false` and the change is archived.
- Rollback: revert the merge of this change (git revert) and re-deploy. The new `seo-geo-schema.html` partial is additive — removing it does not affect rendering of posts that don't depend on it.

## Open Questions

- Should the new partial `seo-geo-schema.html` apply retroactively to existing posts, or only to the new one? **Proposed**: Only the new one in this change; a follow-up change can opt in older posts if desired.
- Should the crawl pipeline also be wired into `daily-publish.sh` as a second daily post? **Deferred** — out of scope for this change.
