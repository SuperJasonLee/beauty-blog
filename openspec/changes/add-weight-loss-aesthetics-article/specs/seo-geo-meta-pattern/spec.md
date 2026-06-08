## ADDED Requirements

### Requirement: A reusable SEO + GEO meta pattern is documented and applied to the new article

The system SHALL document the SEO + GEO meta pattern in `docs/seo-geo-meta.md` and apply it to `content/zh-cn/posts/weight-loss-aesthetics-deep-analysis-2026-06.md` (and its en twin). The pattern SHALL include: (a) front-matter `description` ≤ 160 characters containing the primary keyword, (b) `keywords` array with 5–10 entries, (c) an explicit `## Key Takeaways` / `## 核心要点` section with 4–6 single-sentence bullets, (d) a `{{< faq >}}` shortcode with 4–6 Q&A pairs, (e) a numbered `## 参考资料` / `## References` block with publication name + date + URL.

#### Scenario: Pattern is documented in docs
- **WHEN** the file `docs/seo-geo-meta.md` is read
- **THEN** it SHALL exist
- **AND** it SHALL describe all five pattern elements (description, keywords, takeaways, FAQ, references) with a code example for each
- **AND** it SHALL provide a checklist editors can apply to any new post

#### Scenario: Pattern is applied to the new article
- **WHEN** the new article is read
- **THEN** its front matter SHALL match the documented pattern
- **AND** its body SHALL contain all five required sections

### Requirement: A `seo-geo-schema` Hugo partial emits Article + FAQPage JSON-LD

The system SHALL provide `layouts/partials/seo-geo-schema.html` that emits a `<script type="application/ld+json">` block with `Article` and `FAQPage` schemas. The partial SHALL be invoked from the post single template (`layouts/_default/single.html` or `layouts/baseof.html`) so every post that defines a `{{< faq >}}` shortcode and the required front-matter fields automatically gets the schema. The partial SHALL be a no-op when the required fields are missing (graceful degradation) so existing posts are not broken.

#### Scenario: Partial emits JSON-LD for a post with the required fields
- **WHEN** a post with `description`, `keywords`, `date`, `lastmod`, and a `{{< faq >}}` shortcode is rendered
- **THEN** the rendered HTML SHALL contain a `<script type="application/ld+json">` element
- **AND** the JSON payload SHALL validate as a `Article` schema with `headline`, `description`, `datePublished`, `dateModified`, `keywords`, and `author` set from the post's front matter
- **AND** the JSON payload SHALL validate as a `FAQPage` schema with one `Question` per FAQ pair extracted from the `{{< faq >}}` shortcode

#### Scenario: Partial degrades gracefully when fields are missing
- **WHEN** a post lacks one or more of `description`, `keywords`, or a `{{< faq >}}` shortcode
- **THEN** the partial SHALL still render without throwing
- **AND** the emitted JSON-LD SHALL be empty (no `<script type="application/ld+json">` element) or SHALL include only the schemas for which fields are present

### Requirement: A new `package.json` script invokes the weight-loss-aesthetics crawl pipeline

The system SHALL add a `crawl:weight-loss-aesthetics` script to `package.json` (parallel to the existing `crawl:eye-news` script) that runs `cd scripts/crawl-weight-loss-aesthetics-news && .venv/bin/python run.py` (or the equivalent direct invocation if `.venv` is not used in this pipeline).

#### Scenario: Script is present and runnable
- **WHEN** `package.json` is read
- **THEN** the `scripts` field SHALL contain a `crawl:weight-loss-aesthetics` key
- **AND** `npm run crawl:weight-loss-aesthetics` from the project root SHALL invoke the new pipeline's `run.py`

#### Scenario: Pipeline is not auto-wired into daily publish in this change
- **WHEN** `scripts/daily-publish/daily-publish.sh` is read
- **THEN** it SHALL NOT call `npm run crawl:weight-loss-aesthetics`
- **AND** weight-loss-aesthetics articles SHALL be published only via manual `draft: true → draft: false` editing (or via a follow-up change)
