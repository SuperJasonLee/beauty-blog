## Why

Three recent blog posts have featured/cover images that are either duplicated from another post or visually unrelated to the post's medical-aesthetics content. This hurts reader trust, weakens SEO/OG-card presentation on social shares, and visually breaks the "medical-aesthetics" content contract of the site.

Concrete defects (verified by MD5 and direct image inspection on 2026-06-07):

- `content/{zh-cn,en}/posts/eye-surgery-news/eye-surgery-news-20260606.md` — `featuredImage` points to `eye-surgery-news-20260606-cover.jpg`, which is **byte-identical** to `eye-surgery-news-20260601-cover.jpg` (MD5 `26f045e20d464f9c3eb2a29046b51cb0`). Both show a generic stethoscope-on-laptop stock photo, not the GLP-1/blepharoplasty-specific content of the 2026-06-06 post.
- `content/{zh-cn,en}/posts/xiaohongshu-hot-may-2026.md` — `featuredImage` (`xiaohongshu-hot-may-2026-featured.jpg`) shows a **denim shirt with "Roukka" label** (clothing-product stock photo), not medical aesthetics.
- `content/{zh-cn,en}/posts/xiaohongshu-trends-2026.md` — `featuredImage` (`xiaohongshu-trends-2026-featured.jpg`) shows a **Netflix "N" logo icon**, not medical aesthetics or 小红书.

The duplicate-cover case is reinforced by a known issue in `scripts/crawl-eye-surgery-news/post_generator.py::ensure_cover_image`, which intentionally copies the most-recent existing cover when a fresh one cannot be synthesized. That safety net silently produces the duplication we are now seeing.

## What Changes

- Replace the featured/cover image for the three affected posts (both `zh-cn` and `en` versions, since they share the same image files via `static/` and identical `featuredImage` paths) with topic-relevant CC-licensed images.
- Source new images from CC-licensed providers (Unsplash, Pexels, Wikimedia Commons, Pixabay content library) using the existing `image_downloader.py` pattern; verify license + author in a `CREDITS.md` manifest.
- Regenerate the `-featured.jpg` (and `-cover.jpg` for eye-surgery-news) at the same path so existing `featuredImage` frontmatter keeps working; no frontmatter change is strictly required, but we will rewrite `featuredImage` only if dimensions/format demand it.
- Fix the root cause in `ensure_cover_image` so future posts do not silently copy a previous cover: when a fresh cover cannot be synthesized, the function must fail loudly (raise) rather than copy a sibling file, OR generate a clearly-marked placeholder, OR accept a per-post override list.
- Rebuild the site, regenerate Pagefind index, and verify the three URLs render the new images (manual smoke test + automated MD5-uniqueness check across all `static/images/posts/*-featured.jpg` and `static/images/eye-surgery-news/*-cover.jpg` files).
- Add a small audit script that, on every build, flags any `*-featured.jpg` or `*-cover.jpg` whose bytes match another file under `static/images/`, so this regression cannot recur silently.

## Capabilities

### New Capabilities

- `featured-image-sourcing`: workflow + tooling for acquiring CC-licensed featured/cover images (search, license check, download, credit attribution) and storing them under `static/images/...`.
- `featured-image-uniqueness`: a build-time audit that detects duplicate featured/cover images across posts and fails the build (or surfaces a warning) when duplicates are found.

### Modified Capabilities

<!-- No existing spec-level capabilities are being modified. -->
<!-- This change adds brand-new capabilities; nothing in openspec/specs/nebula-animation/ changes. -->

## Impact

- Files replaced (binary):
  - `static/images/eye-surgery-news/eye-surgery-news-20260606-cover.jpg` (and the `public/images/...` build output)
  - `static/images/posts/xiaohongshu-hot-may-2026-featured.jpg`
  - `static/images/posts/xiaohongshu-trends-2026-featured.jpg`
- Files added:
  - `CREDITS.md` (or `static/images/CREDITS.md`) listing image URL, license, author, attribution URL for each new image
  - `scripts/audit-dup-covers.py` (new) — duplicate-detector
- Files modified:
  - `scripts/crawl-eye-surgery-news/post_generator.py` — `ensure_cover_image` no longer silently copies a sibling cover; either raises or accepts a per-post override
  - Optional: `package.json` — add `npm run audit:images` script entry
  - `content/{zh-cn,en}/posts/.../{eye-surgery-news-20260606,xiaohongshu-hot-may-2026,xiaohongshu-trends-2026}.md` — only `featuredImage` path if dimensions/format change require it
- Build pipeline:
  - `npm run build:full` runs `hugo --minify` then `npx pagefind`; both must succeed
  - New `npm run audit:images` step can be added to CI
- No URL or frontmatter schema changes (existing `featuredImage` paths can be preserved).
- No breaking changes for readers; OG/Twitter card images for the three URLs will simply be replaced.
