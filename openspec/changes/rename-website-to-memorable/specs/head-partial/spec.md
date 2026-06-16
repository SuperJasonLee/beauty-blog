## MODIFIED Requirements

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
- **AND** the `<title>` SHALL contain the new SEO-optimized website name

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

### Requirement: PaperMod submodule is initialized; project layouts/ override theme layouts/

The system SHALL keep the PaperMod git submodule (`themes/PaperMod/`) initialized at the SHA recorded in the parent repo (currently `154d006e0182dfc7da38008323976b02e6bfab4a`). The project's `layouts/` partials SHALL override the theme's `_partials/` where they exist (the project's `head.html`, `header.html`, `footer.html`, `extend_head.html`, `adsense-head.html`, `disclaimer.html`, `gsap-animations.html`, `adsense-in-article.html`, `adsense-in-list.html`, `extend_post_content.html`, plus `layouts/_default/{single,list,terms}.html`, `layouts/404.html`, `layouts/page/search.html`, and the project's `layouts/shortcodes/*.html` all stay in effect). The PaperMod theme's templates exist as a fallback for the ~20 partials the project has NOT overridden (`breadcrumbs.html`, `post_meta.html`, `cover.html`, `toc.html`, `post_nav_links.html`, `share_icons.html`, `comments.html`, `index_profile.html`, `home_info.html`, `anchored_headings.html`, `edit_post.html`, `post_canonical.html`, `translation_list.html`, `social_icons.html`, `author.html`, `svg.html`, etc.).

#### Scenario: project layouts/ win over theme
- **WHEN** a page is rendered that has both a project-level override (e.g. `layouts/partials/head.html`) and a theme-level template (e.g. `themes/PaperMod/layouts/_partials/head.html`)
- **THEN** Hugo SHALL use the project-level template, NOT the theme-level one
- **AND** the rendered `<head>` SHALL contain the project's tags, not PaperMod's

#### Scenario: missing partial resolves from theme
- **WHEN** a project's `layouts/_default/*.html` calls a partial (e.g. `breadcrumbs.html`) that the project has NOT overridden
- **THEN** Hugo SHALL resolve the partial from `themes/PaperMod/layouts/_partials/breadcrumbs.html` (because the submodule is initialized)
- **AND** the build SHALL NOT fail with `partial "breadcrumbs.html" not found`

#### Scenario: a future developer bumps the submodule SHA
- **WHEN** a developer runs `git submodule update --remote themes/PaperMod` (or equivalent)
- **THEN** the parent repo's gitlink for `themes/PaperMod` SHALL update
- **AND** any new theme-level templates that no longer have a project override will start taking effect at the next build
- **AND** any new theme-level templates that conflict with a project override will be silently shadowed by the project's version (per the project-wins scenario above)

### Requirement: Website name appears in page title with SEO optimization

The system SHALL ensure that the new SEO-optimized website name appears in the page title tag, formatted as "Page Title - Website Name" for better search engine visibility.

#### Scenario: Page title includes website name
- **WHEN** any page is rendered
- **THEN** the `<title>` tag SHALL contain the new SEO-optimized website name
- **AND** the title format SHALL be "Page Title - Website Name" or "Website Name - Page Title" depending on page type

#### Scenario: Homepage title is optimized
- **WHEN** the homepage is rendered
- **THEN** the `<title>` tag SHALL primarily display the new SEO-optimized website name
- **AND** the title SHALL include relevant SEO keywords
