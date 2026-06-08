## ADDED Requirements

### Requirement: A `crawl-weight-loss-aesthetics-news` Python pipeline exists and is invokable via npm

The system SHALL provide a Python pipeline at `scripts/crawl-weight-loss-aesthetics-news/` with the same module shape as `scripts/crawl-eye-surgery-news/`: `crawler.py`, `image_downloader.py`, `post_generator.py`, `run.py`, `requirements.txt`, and `README.md`. The pipeline SHALL be invokable via `npm run crawl:weight-loss-aesthetics` (added to `package.json`).

#### Scenario: Pipeline runs end-to-end and emits a draft post
- **WHEN** `npm run crawl:weight-loss-aesthetics` is executed from the project root
- **THEN** the pipeline SHALL create or update a JSON file under `data/crawled/weight-loss-aesthetics-news/` containing the crawled article records
- **AND** the image downloader SHALL write at least one image file under `static/images/posts/weight-loss-aesthetics-2026-06/`
- **AND** the post generator SHALL write a draft file at `content/zh-cn/posts/weight-loss-aesthetics-deep-analysis-2026-06.md` with `draft: true`
- **AND** the post generator SHALL write the paired en file at `content/en/posts/weight-loss-aesthetics-deep-analysis-2026-06.md` with `draft: true`

#### Scenario: Pipeline records its sources
- **WHEN** the pipeline completes
- **THEN** `data/crawled/weight-loss-aesthetics-news/crawled_urls.json` SHALL contain every URL that was successfully crawled
- **AND** re-running the pipeline SHALL NOT re-crawl URLs already present in that file (idempotency)

### Requirement: The pipeline crawls at least three sources

The pipeline's `crawler.py` SHALL define a `SOURCES` list with at least three entries, each invoking an `opencli` command targeting a different source adapter (e.g., `opencli pubmed search`, `opencli zhihu search`, `opencli web read` for a Google results page). The first source SHALL be a clinical/academic source (PubMed), the second a Chinese-language social source (Zhihu), and the third a general web source (Google).

#### Scenario: SOURCES list is configured with three or more entries
- **WHEN** `scripts/crawl-weight-loss-aesthetics-news/crawler.py` is read
- **THEN** the `SOURCES` list SHALL contain ≥ 3 entries
- **AND** the first entry's `command` SHALL include `opencli pubmed` and a weight-loss-aesthetics query string
- **AND** the second entry's `command` SHALL include `opencli zhihu` and a Chinese weight-loss-aesthetics query string
- **AND** the third entry's `command` SHALL include `opencli web` and a Google results URL for weight-loss-aesthetics news in 2026

### Requirement: Image downloader enforces the permitted-license whitelist

The pipeline's `image_downloader.py` SHALL refuse to write any image whose `License` is not in the permitted set (CC0, CC-BY, CC-BY-SA, Unsplash, Pexels, Pixabay Content License), and SHALL fall back to a curated Unsplash/Pexels search when a source-article image candidate is rejected.

#### Scenario: Download is rejected on missing or unsupported license
- **WHEN** `image_downloader.py` is invoked with a candidate URL whose page HTML does not declare a license in the permitted set
- **THEN** the script SHALL NOT write the image file
- **AND** the script SHALL log a warning naming the rejected URL
- **AND** the script SHALL continue to the next candidate or the fallback search

#### Scenario: Successful download records attribution
- **WHEN** an image is downloaded under a permitted license
- **THEN** the script SHALL append a row to `static/images/CREDITS.md` with `File`, `Source URL`, `License`, `Author`, `Author URL`, and `Date added` columns
- **AND** the downloaded file SHALL be ≤ 300 KB
- **AND** the downloaded file's longest-edge pixel dimension SHALL be ≤ 1600 px
