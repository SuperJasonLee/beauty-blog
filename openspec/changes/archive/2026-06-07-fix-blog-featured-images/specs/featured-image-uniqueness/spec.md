## ADDED Requirements

### Requirement: Build-time audit detects duplicate featured/cover images

The system SHALL provide a build-time audit script that walks `static/images/posts/*-featured.jpg` and `static/images/eye-surgery-news/*-cover.jpg`, computes a SHA-256 hash of each file, and reports any hash that appears more than once. In `--strict` mode the script SHALL exit non-zero on any duplicate; in default mode the script SHALL print a report and exit zero.

#### Scenario: Two featured images are byte-identical
- **WHEN** two files under the audited directories share the same SHA-256 hash
- **AND** the script is invoked with `--strict`
- **THEN** the script SHALL print both file paths and the shared hash
- **AND** the script SHALL exit with a non-zero status

#### Scenario: Default mode surfaces duplicates but does not fail
- **WHEN** the script is invoked without `--strict` and two files share the same hash
- **THEN** the script SHALL print both file paths and the shared hash
- **AND** the script SHALL exit with status 0

#### Scenario: No duplicates
- **WHEN** the script is invoked and all hashes in the audited directories are unique
- **THEN** the script SHALL print "OK: N files, all unique" (or equivalent)
- **AND** the script SHALL exit with status 0

### Requirement: The post generator MUST NOT silently copy a sibling cover

The system SHALL ensure that `scripts/crawl-eye-surgery-news/post_generator.py::ensure_cover_image` does not silently produce a featured image that is byte-identical to a previous post's cover. The function SHALL either (a) raise a `RuntimeError` (or a project-specific `CoverImageUnavailable` exception) when no fresh cover is available, OR (b) accept an explicit `fallback_cover: Optional[str]` argument naming a designated default cover path. A silent copy of the most-recent existing sibling cover without an explicit operator override is forbidden.

#### Scenario: No fresh cover, no override → exception
- **WHEN** `ensure_cover_image` is called for a new slug
- **AND** the target `*-cover.jpg` does not exist
- **AND** no `fallback_cover` is provided
- **THEN** the function SHALL raise a `RuntimeError` (or a `CoverImageUnavailable`)
- **AND** the function SHALL NOT copy any sibling `*-cover.jpg` from `static/images/eye-surgery-news/`

#### Scenario: No fresh cover, explicit override → use override
- **WHEN** `ensure_cover_image` is called for a new slug with `fallback_cover="static/images/site/default-eye-surgery-cover.jpg"`
- **AND** the target `*-cover.jpg` does not exist
- **AND** the override file exists
- **THEN** the function SHALL copy the override file to the target path
- **AND** the function SHALL return the public path of the newly-written target
- **AND** no sibling `*-cover.jpg` SHALL be touched

#### Scenario: Fresh cover already exists → return as-is
- **WHEN** `ensure_cover_image` is called for a slug whose `*-cover.jpg` already exists
- **THEN** the function SHALL return the public path of the existing file
- **AND** no copy operation SHALL occur

### Requirement: The audit script is wired into npm scripts

The system SHALL expose the duplicate-image audit as `npm run audit:images`, so it can be invoked from CI and from local developer workflows the same way as the existing `npm run audit:posts`.

#### Scenario: npm run audit:images works
- **WHEN** a developer runs `npm run audit:images` from the repository root
- **THEN** npm SHALL invoke the duplicate-image audit script
- **AND** the script SHALL exit with status reflecting the duplicate status per the audit-script requirement above
