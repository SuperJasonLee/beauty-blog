## MODIFIED Requirements

### Requirement: Featured/cover images for published posts are visually relevant to the post topic

The system SHALL ensure that every published post's `featuredImage` depicts content semantically related to the post's title and `categories`. For medical-aesthetics posts, the image SHALL depict a recognizable medical-aesthetics subject (e.g. a clinical scene, a procedure, a treatment device, a skin/aesthetic close-up) and SHALL NOT depict unrelated subjects (e.g. clothing items, unrelated brand logos, generic office stock).

#### Scenario: Eye-surgery-news post 2026-06-06 cover is no longer a duplicate of 2026-06-01
- **WHEN** the file `static/images/eye-surgery-news/eye-surgery-news-20260606-cover.jpg` is read
- **THEN** its SHA-256 SHALL differ from the SHA-256 of `static/images/eye-surgery-news/eye-surgery-news-20260601-cover.jpg`
- **AND** the image SHALL depict an eye/eyelid/blepharoplasty-related subject appropriate to a 2026-06-06 post whose body discusses GLP-1 + upper-eyelid blepharoplasty, double-plane midface lifting, and related 2026-06 literature

#### Scenario: Xiaohongshu-hot-may-2026 featured image depicts medical aesthetics or a Xiaohongshu-related subject
- **WHEN** the file `static/images/posts/xiaohongshu-hot-may-2026-featured.jpg` is read
- **THEN** it SHALL NOT depict a clothing item
- **AND** it SHALL depict either a medical-aesthetics subject (aesthetic treatment, clinical/spa scene, skin-device close-up) OR a Xiaohongshu-platform-related subject consistent with the post's "5 月小红书医美热门话题" topic

#### Scenario: Xiaohongshu-trends-2026 featured image depicts medical aesthetics
- **WHEN** the file `static/images/posts/xiaohongshu-trends-2026-featured.jpg` is read
- **THEN** it SHALL NOT depict a streaming-service logo or any non-aesthetic brand logo
- **AND** it SHALL depict a medical-aesthetics subject consistent with the post's "2026 小红书医美热门话题梳理" topic

### Requirement: Sourced images carry a permitted license with recorded attribution

The system SHALL only accept images whose license is one of: `CC0`, `CC-BY`, `CC-BY-SA`, `Unsplash`, `Pexels`, or `Pixabay Content License`. For each newly-sourced image, the system SHALL append a row to `static/images/CREDITS.md` with the file name, source URL, license, author, author URL, and date added.

#### Scenario: Newly added image has a CREDITS.md entry
- **WHEN** a new image file is added under `static/images/` to fix a featured-image defect
- **THEN** `static/images/CREDITS.md` SHALL contain a row referencing that file name with a non-empty `Source URL` and `License` column
- **AND** the `License` value SHALL be one of the permitted licenses listed above

#### Scenario: Reject download when license is missing or unsupported
- **WHEN** the image-downloader script is invoked without an explicit `--license` argument whose value is in the permitted set
- **THEN** the script SHALL refuse to write the file
- **AND** the script SHALL exit with a non-zero status and a printed error explaining the missing/unsupported license

### Requirement: Downloaded images are size-constrained

The system SHALL ensure each newly-downloaded featured/cover image is ≤ 300 KB on disk and has a longest-edge pixel dimension ≤ 1600 px, so it does not regress page-load performance.

#### Scenario: Downloaded JPEG is within size budget
- **WHEN** a new image is written under `static/images/posts/` or `static/images/eye-surgery-news/`
- **THEN** the resulting file size SHALL be ≤ 300 KB
- **AND** the resulting longest-edge pixel dimension SHALL be ≤ 1600 px
- **AND** if either constraint is violated, the downloader script SHALL re-encode the image to meet both constraints before writing

### Requirement: Featured images include SEO-optimized alt text and metadata

The system SHALL ensure that featured images include SEO-optimized alt text and metadata that incorporates the new website name and relevant keywords.

#### Scenario: Image alt text includes website context
- **WHEN** a featured image is rendered on a page
- **THEN** the image's alt text SHALL include relevant keywords from the post title
- **AND** the alt text SHALL be optimized for search engine crawling

#### Scenario: Image metadata includes website branding
- **WHEN** a featured image is processed for upload
- **THEN** the image metadata SHALL include the new website name where technically feasible
- **AND** the metadata SHALL not violate image license terms
