## ADDED Requirements

### Requirement: Download images from crawled articles
The system SHALL download images referenced in crawled articles to the local filesystem.

#### Scenario: Download all images from a crawled article
- **WHEN** images are available in the crawled JSON data
- **THEN** the downloader SHALL fetch each image URL
- **THEN** it SHALL save images to `static/images/eye-surgery-news/` with unique filenames
- **THEN** it SHALL update the post content to reference local image paths

#### Scenario: Image download failure
- **WHEN** an image URL returns HTTP error or times out
- **THEN** the downloader SHALL log the error and continue to the next image
- **THEN** it SHALL not fail the entire pipeline

### Requirement: Assign unique filenames to downloaded images
Downloaded images SHALL have unique, descriptive filenames to avoid collisions.

#### Scenario: Filename generation
- **WHEN** an image is downloaded
- **THEN** its filename SHALL follow the pattern: `eye-surgery-news-{date}-{increment}.{ext}`
- **THEN** if two images have the same original filename, they SHALL get different increment numbers

### Requirement: Update post image references
After downloading, the system SHALL update markdown post content to reference local image paths.

#### Scenario: Image URL replaced with local path
- **WHEN** a post references an image that was successfully downloaded
- **THEN** the image URL in the post SHALL be updated to the local path: `/images/eye-surgery-news/{filename}`
