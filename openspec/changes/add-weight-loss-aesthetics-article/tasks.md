## 1. Scaffold the new crawl pipeline directory

- [x] 1.1 Create `scripts/crawl-weight-loss-aesthetics-news/` with `__init__.py`-less module files mirroring `scripts/crawl-eye-surgery-news/`: `crawler.py`, `image_downloader.py`, `post_generator.py`, `run.py`, `requirements.txt`, `README.md`
- [x] 1.2 Create `data/crawled/weight-loss-aesthetics-news/` with an empty `crawled_urls.json` (`{}` or `[]`)
- [x] 1.3 Add `crawl:weight-loss-aesthetics` script to `package.json` pointing to the new pipeline's `run.py`
- [x] 1.4 Add `opencli` and any required Python deps to the new `requirements.txt`

## 2. Implement `crawler.py` with three SOURCES

- [x] 2.1 Define the `SOURCES` list with ≥ 3 entries: (a) `opencli pubmed search` with a weight-loss-aesthetics query (e.g., "GLP-1 body contouring OR panniculectomy OR massive weight loss surgery"), (b) `opencli zhihu search` with a Chinese query (e.g., "GLP-1 减重 整形"), (c) `opencli web read` against a 2026 Google results page for "weight loss aesthetics news 2026"
- [x] 2.2 Implement `run_opencli(cmd, timeout)` to shell out to `opencli` and return parsed JSON, gracefully handling non-zero exit / invalid JSON / timeout
- [x] 2.3 Implement `crawl_all()` returning a list of normalized article dicts with at minimum `title`, `url`, `source`, `date`, `summary`, `image_url`
- [x] 2.4 Implement `save_results(articles)` writing the JSON to `data/crawled/weight-loss-aesthetics-news/articles-YYYYMMDD.json` and updating `crawled_urls.json` (dedup)
- [x] 2.5 Manually run the crawler once and confirm ≥ 6 usable articles are returned (so the article can quote ≥ 8 citations per spec)

## 3. Implement `image_downloader.py` with license enforcement

- [x] 3.1 Implement a license-checker that fetches the candidate page HTML, parses for `license` / `cc:` / `og:license` / source-domain hints, and accepts only the permitted set (CC0, CC-BY, CC-BY-SA, Unsplash, Pexels, Pixabay)
- [x] 3.2 Implement an Unsplash/Pexels fallback via `opencli unsplash search` / `opencli pexels search` when a source-article image candidate is rejected
- [x] 3.3 Download images to `static/images/posts/weight-loss-aesthetics-2026-06/` with a deterministic filename pattern (e.g., `image-1.jpg`)
- [x] 3.4 Resize / re-encode each image so it is ≤ 300 KB and has longest-edge ≤ 1600 px (use `Pillow` or `sips` on macOS)
- [x] 3.5 Append a row to `static/images/CREDITS.md` for each successfully downloaded image (File, Source URL, License, Author, Author URL, Date added)
- [x] 3.6 Run the downloader and confirm 3–5 images land in the target directory with valid CREDITS.md rows

## 4. Implement `post_generator.py` emitting bilingual drafts

- [x] 4.1 Read the JSON from `data/crawled/weight-loss-aesthetics-news/articles-YYYYMMDD.json` and the image map from the downloader
- [x] 4.2 Generate the zh-cn article body following the four-theme structure (GLP-1, MWL surgery, non-invasive, regulatory) with `## 核心要点` (4–6 bullets), `{{< faq >}}` (4–6 Q&A), `## 参考资料` (numbered footnotes)
- [x] 4.3 Generate the en article body as a translation of the zh-cn content (same themes, same structure, English FAQ + References)
- [x] 4.4 Emit `content/zh-cn/posts/weight-loss-aesthetics-deep-analysis-2026-06.md` with full front matter (title, date, description ≤ 160 chars containing "减肥", categories, tags, keywords[5–10], featuredImage, translations, author, draft: true)
- [x] 4.5 Emit `content/en/posts/weight-loss-aesthetics-deep-analysis-2026-06.md` with mirrored front matter (description containing "weight loss", translations pointing back)
- [x] 4.6 Run the post generator and confirm both files are created with `draft: true` and pass `npm run audit:posts --severity error`

## 5. Author the SEO + GEO pattern docs and JSON-LD partial

- [x] 5.1 Create `docs/seo-geo-meta.md` documenting the five-element pattern (description, keywords, Key Takeaways, FAQ, References) with code examples and a copy-pasteable checklist
- [x] 5.2 Create `layouts/partials/seo-geo-schema.html` that emits `<script type="application/ld+json">` with `Article` + `FAQPage` schemas sourced from the post's front matter + the `{{< faq >}}` shortcode
- [x] 5.3 Wire the partial into `layouts/_default/single.html` (or `layouts/baseof.html`) via `{{- partial "seo-geo-schema.html" . -}}` placed inside `<head>`
- [x] 5.4 Make the partial a graceful no-op when required front-matter fields are missing, so existing posts are not broken
- [x] 5.5 Run `hugo --minify` and inspect a rendered post to confirm the `<script type="application/ld+json">` block is present and validates as `Article` + `FAQPage`

## 6. Verify and publish the new article

- [x] 6.1 Run `npm run audit:posts content/zh-cn/posts/weight-loss-aesthetics-deep-analysis-2026-06.md` — must exit 0
- [x] 6.2 Run `npm run audit:images:strict` — confirm no SHA-256 collision between the new `featuredImage` and any existing post cover; rotate cover if collision detected
- [x] 6.3 Manually verify each `## 参考资料` URL returns a 2xx (use `curl -I`); fix or remove any that fail
- [x] 6.4 Spot-check that the rendered article displays the JSON-LD `Article` + `FAQPage` payload and that the FAQ block renders the expected Q&A pairs
- [x] 6.5 Flip `draft: true → draft: false` in both the zh-cn and en files
- [ ] 6.6 Commit with message `add: weight-loss-aesthetics deep-analysis article (zh-cn + en) + crawl pipeline + SEO/GEO pattern` and push — requires explicit user permission (system rule: do not commit without explicit request)

## 7. Out of scope (deferred)

- [ ] 7.1 Wire `crawl:weight-loss-aesthetics` into `scripts/daily-publish/daily-publish.sh` — deferred to a follow-up change
- [ ] 7.2 Apply the new SEO + GEO partial retroactively to existing posts — deferred to a follow-up change
