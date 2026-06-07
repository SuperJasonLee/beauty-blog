## ADDED Requirements

### Requirement: Generate Chinese post from crawled data
The system SHALL use LLM to synthesize crawled articles into a well-structured Chinese blog post.

#### Scenario: Chinese post generation
- **WHEN** the synthesis script receives crawled JSON data
- **THEN** it SHALL send the content to the LLM with a Chinese-writing prompt
- **THEN** it SHALL receive a structured post draft in Chinese
- **THEN** it SHALL write the post to `content/zh-cn/posts/eye-surgery-news/` as Hugo markdown

### Requirement: Generate English post from crawled data
The system SHALL use LLM to synthesize crawled articles into a well-structured English blog post.

#### Scenario: English post generation
- **WHEN** the synthesis script receives crawled JSON data
- **THEN** it SHALL send the content to the LLM with an English-writing prompt
- **THEN** it SHALL receive a structured post draft in English
- **THEN** it SHALL write the post to `content/en/posts/eye-surgery-news/` as Hugo markdown

### Requirement: Generate Hugo-compatible front matter
Generated posts SHALL include proper Hugo front matter for correct rendering and SEO.

#### Scenario: Front matter includes required fields
- **WHEN** a post is generated
- **THEN** its front matter SHALL include: `title`, `date`, `draft: true`, `tags`, `categories`, `image` (cover), `description`
- **THEN** the language-specific front matter SHALL include the counterpart post's path in `translations` section

### Requirement: Mark posts as drafts
All auto-generated posts SHALL be marked as drafts to require human review before publishing.

#### Scenario: Draft flag set
- **WHEN** a post file is created
- **THEN** its front matter SHALL contain `draft: true`
