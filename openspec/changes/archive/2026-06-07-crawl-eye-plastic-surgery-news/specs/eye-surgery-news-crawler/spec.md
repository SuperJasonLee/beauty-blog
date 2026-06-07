## ADDED Requirements

### Requirement: Crawl latest eye plastic surgery news
The system SHALL crawl the latest news about eye plastic surgery from at least 3 medical/aesthetic websites.

#### Scenario: Successful crawl from configured sources
- **WHEN** the crawler script is executed
- **THEN** it SHALL visit each configured source URL
- **THEN** it SHALL extract article title, publication date, content body, and image URLs
- **THEN** it SHALL output structured JSON with all extracted articles

#### Scenario: Source is unreachable
- **WHEN** a source URL returns HTTP error or times out
- **THEN** the crawler SHALL log the error and continue to the next source
- **THEN** it SHALL not crash on individual source failure

### Requirement: Deduplicate crawled articles
The system SHALL deduplicate articles by URL to avoid re-crawling the same content.

#### Scenario: Duplicate URL encountered
- **WHEN** the same article URL is crawled in a subsequent run
- **THEN** the system SHALL skip it and log as skipped

#### Scenario: Similar content from different sources
- **WHEN** two articles from different sources cover the same news
- **THEN** the system SHALL retain both as separate entries (human will decide during synthesis)

### Requirement: Output crawled data as JSON
The crawler SHALL output a structured JSON file with all crawled articles.

#### Scenario: JSON output format
- **WHEN** the crawler finishes execution
- **THEN** it SHALL write a JSON file to `data/crawled/eye-surgery-news/` with timestamp in filename
- **THEN** each article SHALL contain: `source_url`, `source_name`, `title`, `date`, `content_markdown`, `image_urls` (array), `crawled_at`
