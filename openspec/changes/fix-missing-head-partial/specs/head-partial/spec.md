## ADDED Requirements

### Requirement: Hugo build completes successfully

The system SHALL provide a `layouts/partials/head.html` partial such that `npm run build:full` (which runs `hugo --minify` followed by `npx pagefind --site public`) completes with exit code 0 on a clean checkout.

#### Scenario: hugo --minify succeeds
- **WHEN** a developer runs `npm run build` (which executes `hugo --minify`) from the repository root
- **THEN** the command SHALL exit with status 0
- **AND** the command SHALL NOT emit an `error calling partial: partial "head.html" not found` message

#### Scenario: pagefind index builds
- **WHEN** a developer runs `npm run build:full` from the repository root
- **THEN** both `hugo --minify` and `npx pagefind --site public` SHALL complete with status 0
- **AND** the `public/pagefind/` directory SHALL be re-emitted

#### Scenario: every rendered page has a non-empty <head> block
- **WHEN** `hugo --minify` produces a page under `public/`
- **THEN** the page SHALL contain a `<head>` block with at least: a `<title>`, a `<meta name="description">`, an `og:title`, an `og:description`, an `og:type`, and a `<link rel="canonical">`

### Requirement: Existing customizations in extend_head.html are preserved

The system SHALL include the project's existing `layouts/partials/extend_head.html` partial from the new `head.html`, so that the Google site verification meta tag, author meta tag, `sameAs` `me` links, and AdSense script continue to render in the page `<head>`.

#### Scenario: Google site verification renders
- **WHEN** `hugo --minify` produces a page under `public/`
- **THEN** the page SHALL contain a `<meta name="google-site-verification" content="KNeph-DlbM2z78osJ4V0LySFUJQJTPcbfDuxYADz9Bo" />` tag

#### Scenario: author meta renders
- **WHEN** `hugo --minify` produces a page under `public/`
- **THEN** the page SHALL contain a `<meta name="author">` tag whose content comes from `site.Params.author.name` (defaulting to `site.Title` if absent)

#### Scenario: sameAs me links render
- **WHEN** `site.Params.schema.sameAs` is non-empty in `hugo.yaml`
- **THEN** the rendered page SHALL contain one `<link rel="me" href="...">` tag per entry

#### Scenario: AdSense script renders only in production
- **WHEN** `hugo.IsProduction` is true
- **THEN** the rendered page SHALL contain a `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=...">` tag
- **WHEN** `hugo.IsProduction` is false (e.g. local `hugo server -D`)
- **THEN** the rendered page SHALL NOT contain the AdSense script tag

### Requirement: OG image falls back to the project's site image and uses featuredImage when present

The system SHALL set the `og:image` meta tag in `head.html` such that, on a page that has a frontmatter `featuredImage`, `og:image` resolves to that featured image; on a page without `featuredImage` (e.g. a list / taxonomy page), `og:image` SHALL fall back to `site.Params.images[0]` (currently `/images/site-feature.png`).

#### Scenario: post with featuredImage
- **WHEN** a post has `featuredImage: /images/eye-surgery-news/eye-surgery-news-20260606-cover.jpg` in its frontmatter
- **THEN** the rendered page SHALL contain `<meta property="og:image" content="https://beauty-blog.cloud-ip.cc/images/eye-surgery-news/eye-surgery-news-20260606-cover.jpg" />` (or equivalent absolute URL)

#### Scenario: list page without featuredImage
- **WHEN** a list / taxonomy / homepage page (no `featuredImage`) is rendered
- **THEN** the page SHALL contain `<meta property="og:image" content="https://beauty-blog.cloud-ip.cc/images/site-feature.png" />` (or equivalent absolute URL pointing at the site image)

### Requirement: PaperMod submodule state is documented in-repo

The system SHALL include a brief `themes/PaperMod/README.md` (or equivalent) explaining that the directory is intentionally empty because the PaperMod git submodule is not initialized, and that the project's `layouts/` directory is the source of truth for templates.

#### Scenario: future developer reads the README
- **WHEN** a developer opens `themes/PaperMod/README.md`
- **THEN** the file SHALL state that the directory is intentionally empty and that the project does not depend on the upstream PaperMod templates
- **AND** the file SHALL NOT recommend running `git submodule update --init` (which would re-introduce templates the project has overridden)
