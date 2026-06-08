## ADDED Requirements

### Requirement: The weight-loss-aesthetics deep-analysis article is published in zh-cn and en with the same slug

The system SHALL publish one deep-analysis article about the weight-loss + medical-aesthetics intersection in 2026, with the zh-cn primary file at `content/zh-cn/posts/weight-loss-aesthetics-deep-analysis-2026-06.md` and the en translation at `content/en/posts/weight-loss-aesthetics-deep-analysis-2026-06.md`. The en file's front matter SHALL declare `translations: ["/zh-cn/posts/weight-loss-aesthetics-deep-analysis-2026-06"]` (or the equivalent back-link) so the two pages cross-link bidirectionally.

#### Scenario: zh-cn article exists and references the en translation
- **WHEN** the file `content/zh-cn/posts/weight-loss-aesthetics-deep-analysis-2026-06.md` is read
- **THEN** its front matter SHALL contain a non-empty `title`, `date`, `description`, `categories`, `tags`, `keywords`, and `featuredImage` field
- **AND** its `translations` array SHALL contain `/en/posts/weight-loss-aesthetics-deep-analysis-2026-06` (or the project's canonical translation-list shape)

#### Scenario: en article exists and references the zh-cn source
- **WHEN** the file `content/en/posts/weight-loss-aesthetics-deep-analysis-2026-06.md` is read
- **THEN** its front matter SHALL mirror the zh-cn article's title, date, description, categories, tags, and keywords (translated, not identical)
- **AND** its `translations` array SHALL contain `/posts/weight-loss-aesthetics-deep-analysis-2026-06` (or the project's canonical back-link shape)

### Requirement: The article covers four required weight-loss-aesthetics themes

The system SHALL ensure the article body contains explicit `## H2` sections covering at least four of the following themes: (a) GLP-1 receptor agonist impact on body-contouring demand, (b) post-massive-weight-loss (MWL) body-contouring surgery, (c) non-invasive fat reduction and body-skin tightening, (d) regulatory / safety developments in 2026 (FDA, ASPS, ISAPS, ASA). Each section SHALL contain at least one named, dated, URL-cited source from a recognized medical-aesthetics publication (e.g., ASPS, ISAPS, Allure, PR Newswire, FDA, PubMed-indexed journal).

#### Scenario: All four theme sections are present in the zh-cn article
- **WHEN** the zh-cn article is rendered
- **THEN** the rendered HTML SHALL contain at least four `## H2` headings whose text matches one of: "GLP-1", "减重手术", "非侵入式塑形", "监管" / "安全" / "regulatory" / "safety" / "MWL" / "massive weight loss" (or the en equivalents)
- **AND** each such section SHALL contain at least one markdown footnote reference (e.g., `[^1]`) pointing to a numbered entry in `## 参考资料` / `## References`

#### Scenario: Every claim is footnoted
- **WHEN** the article body is parsed
- **THEN** the number of footnote references SHALL be ≥ 8
- **AND** the `## 参考资料` (zh-cn) / `## References` (en) section SHALL contain the same count of numbered entries with publication name, date, and URL

### Requirement: The article includes SEO + GEO extractable blocks

The system SHALL ensure the article body contains a `## Key Takeaways` (or `## 核心要点`) section with 4–6 single-sentence bullets, and a `{{< faq >}}` shortcode with 4–6 Q&A pairs, in addition to the standard `## 参考资料` block. The `description` front-matter field SHALL be ≤ 160 characters and SHALL contain the primary keyword "减肥" (zh-cn) or "weight loss" (en). The `keywords` front-matter field SHALL contain 5–10 entries.

#### Scenario: Key Takeaways section exists
- **WHEN** the zh-cn article is rendered
- **THEN** the rendered HTML SHALL contain a `<h2>` whose text is "核心要点" or "Key Takeaways"
- **AND** the next sibling list SHALL contain between 4 and 6 `<li>` items

#### Scenario: FAQ section exists and uses the shortcode
- **WHEN** the article source is parsed
- **THEN** the body SHALL contain a `{{< faq >}}` … `{{< /faq >}}` Hugo shortcode block
- **AND** the block SHALL contain 4–6 Q&A pairs

#### Scenario: Description field is within SEO budget
- **WHEN** the article front matter is parsed
- **THEN** the `description` field length SHALL be ≤ 160 characters
- **AND** the `description` field SHALL contain the substring "减肥" (zh-cn) or "weight loss" (en)

### Requirement: The article references 3–5 license-permitted images in body and front matter

The system SHALL ensure the article's `featuredImage` front-matter field points to a file under `static/images/posts/weight-loss-aesthetics-2026-06/` with a permitted license recorded in `static/images/CREDITS.md` (CC0, CC-BY, CC-BY-SA, Unsplash, Pexels, or Pixabay Content License). The article body SHALL reference at least 3 images using the `{{< figure src="…" title="…" >}}` shortcode.

#### Scenario: Featured image is sourced under a permitted license
- **WHEN** the `featuredImage` front-matter field is read
- **THEN** its value SHALL be a path under `/images/posts/weight-loss-aesthetics-2026-06/`
- **AND** `static/images/CREDITS.md` SHALL contain a row referencing that filename with a non-empty `Source URL` and a `License` value from the permitted set

#### Scenario: Body references at least 3 figures
- **WHEN** the article body is parsed
- **THEN** the number of `{{< figure src="…" >}}` shortcode invocations SHALL be ≥ 3
- **AND** each referenced image file SHALL exist under `static/images/posts/weight-loss-aesthetics-2026-06/`
- **AND** each referenced image SHALL have a row in `static/images/CREDITS.md`

### Requirement: The article is published (not stuck as a draft) once verified

The system SHALL flip the article's `draft` front-matter field to `false` only after the editor has confirmed: (a) all citations resolve, (b) all 3–5 images have valid `CREDITS.md` rows, (c) `npm run audit:posts` returns no error-severity findings for the file, and (d) `npm run audit:images:strict` reports no SHA-256 collision between the new `featuredImage` and any existing post cover.

#### Scenario: Article is not published while a citation is broken
- **WHEN** any footnote URL in `## 参考资料` returns a non-2xx status
- **THEN** the article's `draft` field SHALL remain `true`
- **AND** the daily-publish script's `Stage 5` SHALL NOT flip it to `false`

#### Scenario: Article publishes only after audit passes
- **WHEN** `npm run audit:posts content/zh-cn/posts/weight-loss-aesthetics-deep-analysis-2026-06.md` exits 0
- **AND** `npm run audit:images:strict` reports no collision involving the new featured image
- **THEN** the editor MAY set `draft: false` and the post SHALL be built into `public/`
