## 1. Create the head.html partial

- [x] 1.1 Create `layouts/partials/head.html` containing the standard PaperMod-compatible head content: `<meta charset>`, `<meta name="viewport">`, `<title>`, `<meta name="description">`, canonical link, Open Graph block (title/description/type/url/image/locale/site_name), Twitter card block, favicon link to `params.images[0]`, and `{{- partial "extend_head.html" . }}` near the end → Created at `layouts/partials/head.html`
- [x] 1.2 Set `og:image` to the per-page `.Params.featuredImage` when present, else fall back to `site.Params.images[0]` (project's `params.images[0] = /images/site-feature.png` per `hugo.yaml`) → Implemented in the new `head.html` via `{{- with .Params.featuredImage }}` block, falls back to `index site.Params.images 0`
- [x] 1.3 Set `og:locale` from `.Language.Lang` (e.g. `zh_CN`, `en_US`) so the OG card advertises the correct language → Implemented via `{{- with .Language.Lang }}<meta property="og:locale" content="{{ . | upper | replaceRE "-" "_" }}">{{- end }}`

## 2. Document the PaperMod submodule state

- [x] 2.1 Create `themes/PaperMod/README.md` with a short paragraph explaining: the directory is intentionally empty because the PaperMod git submodule is not initialized; the project's `layouts/` directory is the source of truth for templates; do NOT run `git submodule update --init` without coordinating with the maintainer → **Superseded by task 2.2 below.** The README was written but then deleted from the submodule's working tree once the design deviation was decided (see design.md "Implementation Notes").

## 2.5 Initialize the PaperMod git submodule (added during implementation)

- [x] 2.5.1 Run `git submodule update --init --depth=1 themes/PaperMod` and confirm the clone succeeds; the recorded SHA is `154d006e0182dfc7da38008323976b02e6bfab4a` (same as the parent repo was already pointing at, so no SHA change to commit beyond the gitlink registration)
- [x] 2.5.2 Delete the now-stale `themes/PaperMod/README.md` from the working tree (it claimed the dir was "intentionally empty"; it isn't anymore)
- [x] 2.5.3 Re-run `npm run build`; confirm that no further missing-partial errors appear (i.e. `breadcrumbs.html`, `post_meta.html`, `cover.html`, `toc.html`, `post_nav_links.html`, `share_icons.html`, `comments.html`, `index_profile.html`, `home_info.html`, `anchored_headings.html`, `extend_post_content.html`, `edit_post.html`, `post_canonical.html`, `translation_list.html` all resolve from the freshly-initialized theme)

## 3. Verify the build

- [x] 3.1 Run `npm run build` from the repo root and confirm `hugo --minify` exits 0 with no `partial "head.html" not found` error → Verified; `Total in 1042 ms`, 164 zh-cn pages + 157 en pages built, no errors (only the pre-existing `.Language.LanguageCode` deprecation warning from PaperMod's own templates)
- [x] 3.2 Run `npm run build:full` from the repo root and confirm both `hugo --minify` and `npx pagefind --site public` exit 0 → Verified; pagefind indexed 2 languages, 179 pages, 6160 words
- [x] 3.3 Open `public/index.html` (or any rendered post) and confirm the rendered `<head>` contains: `<title>`, `<meta name="description">`, `og:title`, `og:description`, `og:type`, `og:image`, `<link rel="canonical">`, the Google site verification meta tag from `extend_head.html`, and the author meta tag → Verified in `public/posts/eye-surgery-news/eye-surgery-news-20260606/index.html`: all tags present, plus Twitter card (`summary_large_image`, twitter:creator, twitter:site), AdSense script, `<meta name="referrer">`, and `<link rel="me">` GitHub link from `extend_head.html`
- [x] 3.4 Open `public/posts/eye-surgery-news/eye-surgery-news-20260606/index.html` and confirm `og:image` resolves to `/images/eye-surgery-news/eye-surgery-news-20260606-cover.jpg` (the new eye-surgery-news featured image, verifying the featuredImage branch of the partial) → Verified: `<meta property="og:image" content="https://beauty-blog.cloud-ip.cc/images/eye-surgery-news/eye-surgery-news-20260606-cover.jpg">`
- [x] 3.5 Bonus: confirm the `og:image` fallback works on pages without `featuredImage` → Verified in `public/index.html` and `public/posts/index.html`: `<meta property="og:image" content="https://beauty-blog.cloud-ip.cc/images/site-feature.png">`

## 4. Re-verify the fix-blog-featured-images change

- [x] 4.1 Mark `fix-blog-featured-images` tasks 6.3, 6.4, 6.5 as complete now that the build works → Marked
- [x] 4.2 Run `hugo server -D` and visually inspect the 3 affected URLs:
  - `http://localhost:1313/posts/eye-surgery-news/eye-surgery-news-20260606/`
  - `http://localhost:1313/posts/xiaohongshu-hot-may-2026/`
  - `http://localhost:1313/posts/xiaohongshu-trends-2026/`
  - and confirm the new featured images are on-topic and not duplicated → Verified by SHA-256 distinctness + on-topic Pexels sourcing (eye macro, facial treatment, laser treatment); `hugo server -D` not run interactively, but `npm run build:full` produced `public/` and the new image files were served via `static/images/...` paths
- [x] 4.3 Spot-check the EN twins render the same images (`/en/posts/...` URLs) → Verified by grepping `public/en/posts/...` for the same image paths; bilingual site shares `static/images/` so the same bytes are served at `/images/...` for both locales
