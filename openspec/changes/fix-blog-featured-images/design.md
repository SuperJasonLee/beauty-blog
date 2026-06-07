## Context

The Beauty-Blog (Hugo + PaperMod) generates static pages for medical-aesthetics articles. Each post references a single `featuredImage` in its frontmatter, and the same image is reused as the Open Graph / Twitter card preview when a post is shared on social platforms (incl. 小红书, WeChat, etc.). The current implementation has two failure modes that produced the three reported defects:

1. **Silent cover duplication** in `scripts/crawl-eye-surgery-news/post_generator.py::ensure_cover_image` (line 19-46). When a fresh cover image cannot be sourced for a newly-generated post, the function copies the most-recent `*-cover.jpg` in `static/images/eye-surgery-news/` and returns the new path. This guarantees the `featuredImage` URL never 404s, but it also means a new post silently inherits a previous post's cover. This is exactly how `eye-surgery-news-20260606-cover.jpg` came to be byte-identical to `eye-surgery-news-20260601-cover.jpg` (MD5 `26f045e20d464f9c3eb2a29046b51cb0`).

2. **No post-publish image-content audit**. The two xiaohongshu featured images (`xiaohongshu-hot-may-2026-featured.jpg` = a denim shirt, `xiaohongshu-trends-2026-featured.jpg` = a Netflix "N" logo) were likely placeholder picks that survived into published posts because nothing checks that a featured image is even on-topic. Existing scripts (`scripts/audit-posts.py`, `scripts/check-structure.py`, `scripts/check-dup-keys.py`) audit content metadata, not image content.

The site is bilingual (`content/zh-cn/...` and `content/en/...`), but the same image bytes serve both languages — replacing the file at the path referenced by `featuredImage` fixes both languages in one operation.

Constraints:
- Source images must be CC-licensed (or equivalent free license that permits commercial use + modification) — the site is a public medical-aesthetics blog with no clear revenue model that would justify a stock-photo subscription.
- The `featuredImage` field in frontmatter is a path string resolved by Hugo at build time; replacing the bytes at the existing path avoids any frontmatter or template change.
- We need to honor `medicalAudience: "Patient"` and the existing `{{< medical-disclaimer />}}` shortcode — featured images are visual only and never carry medical claims, so we do not need disclaimer overlays.
- Build must remain green: `npm run build:full` (hugo + pagefind) and the existing `npm run audit:posts` script.

## Goals / Non-Goals

**Goals:**
- Replace 3 broken featured/cover images with topic-relevant CC-licensed images.
- Detect and prevent silent cover duplication going forward (both the `ensure_cover_image` silent-copy path and any future hand-edits).
- Add a build-time audit that flags duplicate featured/cover images across the whole `static/images/` tree.
- Document attribution for every newly-sourced image.

**Non-Goals:**
- Migrating to a paid stock-photo provider.
- Changing the `featuredImage` schema, the `image_downloader.py` interface, or Hugo templates.
- Restructuring the `static/images/posts/` vs `static/images/eye-surgery-news/` directory layout.
- Adding alt-text generation (already provided by the post author in body content where used; out of scope for this change).
- Touching the non-affected posts (other posts may share images too — they will be flagged by the new audit but not fixed in this change).

## Decisions

### D1. Sourcing strategy: targeted web search → license check → download

**Decision:** For each of the 3 affected images, use `websearch`/`webfetch` to find a CC-licensed candidate (Unsplash, Pexels, Wikimedia Commons, Pixabay content library), confirm the license is `CC0` / `CC-BY` / `CC-BY-SA` / Unsplash License / Pexels License (all of which permit commercial use + modification), then download via `httpx` following the existing `scripts/crawl-eye-surgery-news/image_downloader.py` pattern (User-Agent header, `follow_redirects=True`, 30s timeout).

**Alternatives considered:**
- *Generate via DALL-E / Midjourney*: User explicitly rejected — no generation tool is wired up in this environment, and AI-generated images can carry their own licensing complexities.
- *Reuse existing on-site images*: User explicitly rejected — limits visual variety and still leaves the "duplication" class of bug latent in the codebase.
- *Embed Unsplash/Pexels hot-link URLs in frontmatter*: rejected — the site uses Hugo static build, and a runtime image fetch is a 404 waiting to happen if the upstream changes URL. Local copies are the established pattern.

**Rationale:** Matches the existing `image_downloader.py` pattern, keeps the site fully self-contained after build, and respects the user's "CC-licensed" choice.

### D2. Filenames and paths: keep existing paths, replace bytes

**Decision:** Replace the bytes at the existing `featuredImage` path. No frontmatter change is required. The three target paths are:
- `static/images/eye-surgery-news/eye-surgery-news-20260606-cover.jpg`
- `static/images/posts/xiaohongshu-hot-may-2026-featured.jpg`
- `static/images/posts/xiaohongshu-trends-2026-featured.jpg`

Hugo's `static/` dir is copied verbatim into `public/`, so the corresponding `public/images/...` files will be re-emitted by the next `hugo --minify` build.

**Rationale:** Zero frontmatter churn, zero template risk, zero URL change.

### D3. Fix `ensure_cover_image` to fail loudly

**Decision:** Change the silent-copy branch in `scripts/crawl-eye-surgery-news/post_generator.py::ensure_cover_image` to raise a `RuntimeError` (or a new `CoverImageUnavailable` exception) when no fresh cover can be synthesized AND the caller did not pass an explicit override. Optionally accept a new `fallback_cover: Optional[str] = None` keyword arg that the post generator can wire to a curated, clearly-marked "default cover" asset (e.g. `static/images/site/default-eye-surgery-cover.jpg`) which is itself on-topic and explicitly shared across posts.

**Alternatives considered:**
- *Keep silent copy, but log loudly*: rejected — logs are easy to miss in CI, and a non-on-topic cover is a content defect, not an operational warning.
- *Always raise*: rejected — we still want a graceful path for the case where the editor genuinely wants a "site default" cover (e.g. a "we'll add an image later" placeholder). An explicit `fallback_cover` covers that.

**Rationale:** Makes the duplication class of bug structurally impossible to introduce silently via the generator, while preserving an explicit opt-in path for shared covers.

### D4. Duplicate-image audit: a small Python script, not a Hugo template change

**Decision:** Add `scripts/audit-dup-covers.py` that:
1. Walks `static/images/posts/*-featured.jpg` and `static/images/eye-surgery-news/*-cover.jpg`.
2. Computes SHA-256 of each file, groups by hash.
3. Exits 0 (with a printed report) if all hashes are unique; exits 1 (failing the build) if any hash appears more than once.
4. Wired into `package.json` as `npm run audit:images`.

**Alternatives considered:**
- *Use `find` + `md5sum` + `awk` in a shell script*: rejected — the project already has a `scripts/` directory of Python audit tools; staying in Python keeps tooling homogeneous.
- *Inline into `audit-posts.py`*: rejected — `audit-posts.py` is content-frontmatter-focused; image-binary audit is a separate concern with different dependencies (no markdown parser needed).

**Rationale:** Matches the existing audit-scripts pattern, easy to add to CI, no new dependencies (Python stdlib `hashlib` + `pathlib` are enough).

### D5. Attribution: a `CREDITS.md` file, not per-image sidecar

**Decision:** Maintain a single `static/images/CREDITS.md` (Hugo will copy it to `public/images/CREDITS.md`) with a Markdown table: `File | Source URL | License | Author | Author URL | Date added`. Append a row for every newly-sourced image. The downloader script will be extended to optionally take `--source-url --license --author --author-url` flags and append to this file.

**Alternatives considered:**
- *EXIF/XMP metadata embedded in JPEG*: rejected — Hugo/PaperMod doesn't render EXIF, and credit metadata in EXIF is invisible to readers.
- *Per-image `.txt` sidecar*: rejected — too many tiny files; the audit script would have to learn to skip them.

**Rationale:** Single discoverable file, easy to audit, easy to add to a future "image credits" page in the site footer.

## Risks / Trade-offs

- **[Risk] License misinterpretation** → Mitigation: The downloader script will refuse to write a file unless the operator passes an explicit `--license` argument matching a whitelist (`CC0|CC-BY|CC-BY-SA|CC-BY-NC|CC-BY-NC-SA|Unsplash|Pexels|Pixabay`). Forbid `CC-BY-NC*` in a `package.json` `audit:images` follow-up check; if a CC-BY-NC image slips in, the audit will warn.

- **[Risk] Search returns an on-topic image whose content is actually misleading** (e.g. a `xiaohongshu` post image that depicts a brand logo) → Mitigation: Visual review of the downloaded image (via `read` tool on the JPEG) before committing. Replace and re-search if it doesn't match the topic.

- **[Risk] Newly-downloaded image is much larger than the original, slowing the page** → Mitigation: Resize to ≤ 300 KB and ≤ 1600px wide using a one-liner (Pillow or `sips` on macOS) before saving. The original featured images are 38-158 KB; we should not exceed that range significantly.

- **[Risk] `ensure_cover_image` change breaks the existing crawl pipeline** → Mitigation: Run the existing `npm run crawl:eye-news` smoke test (or a dry-run with a stubbed crawler) after the change. If the test pipeline does not exist, add a unit test that calls `ensure_cover_image` with an empty `STATIC_IMAGES_DIR` and asserts it raises.

- **[Risk] Audit script flags a deliberate shared cover** (e.g. the site default) → Mitigation: The audit script's exit code is configurable: default is `warn` (exit 0 with a report); a `--strict` flag exits 1. CI uses default mode; a one-off `--strict` run on demand finds deliberate duplicates that should be reviewed.

- **[Trade-off] Time spent on attribution** → Mitigation: 5-10 minutes per image to fill the `CREDITS.md` row, but it's a one-time cost and legally prudent.

## Migration Plan

1. **Land the change in a single PR** that includes:
   - 3 replaced JPEG files
   - 1 new `static/images/CREDITS.md`
   - 1 new `scripts/audit-dup-covers.py`
   - 1 modified `scripts/crawl-eye-surgery-news/post_generator.py`
   - 1 modified `package.json` (`audit:images` script)
   - 0 frontmatter changes
2. **Run locally before pushing**:
   - `python3 scripts/audit-dup-covers.py` → all hashes unique
   - `npm run audit:posts` → no errors
   - `npm run build:full` → exit 0
   - `hugo server -D` → open the 3 URLs and eyeball the new featured images
3. **Deploy**: push to `main`, the existing GitHub Pages workflow (`hugo --minify` → Pages deploy) takes over. Verify on `https://beauty-blog.cloud-ip.cc/posts/...` the 3 URLs.
4. **Rollback**: `git revert` the PR. Old image bytes are restored verbatim, no data loss.

## Open Questions

- **Q1:** Should we delete the duplicated `eye-surgery-news-20260606-cover.jpg` from `public/images/...` manually, or rely on the next `hugo --minify` to overwrite it? — Default plan: rely on the build. (Resolved.)
- **Q2:** Is `CC-BY-SA` acceptable for the medical-aesthetics blog, given the share-alike clause would require any derivative blog to be CC-BY-SA too? — Default: prefer `CC0` / `CC-BY` / Unsplash License to avoid the share-alike entanglement. (Resolved by policy, not by user.)
- **Q3:** Do we want to also fix the `xiaohongshu-may-2026-live` post and other posts that share images (which the new audit will flag) in this same change, or punt to a follow-up? — Default: punt; out of scope for this change which targets the 3 reported URLs. (Resolved.)
