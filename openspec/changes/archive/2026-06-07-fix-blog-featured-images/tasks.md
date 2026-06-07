## 1. Sourcing new images for the 3 affected posts

- [x] 1.1 Search Unsplash / Pexels / Wikimedia Commons for a CC-licensed eye/eyelid/blepharoplasty-related image appropriate for `eye-surgery-news-20260606` (post body discusses GLP-1 + upper-eyelid blepharoplasty, double-plane midface lifting, 2026-06 PubMed literature) → **Selected:** Pexels photo ID `1715091` by `thatguycraig000` — macro close-up of a brown iris (1600x1309, 131 KB), "Perfect for medical and artistic uses" per Pexels description
- [x] 1.2 Verify the chosen image's license page states `CC0`, `CC-BY`, `CC-BY-SA`, `Unsplash License`, or `Pexels License`; record the license URL → **Pexels License** (https://www.pexels.com/license/) — free for commercial use, no attribution required, attribution appreciated; full source URL: https://www.pexels.com/photo/macro-photography-of-human-eye-1715091/
- [x] 1.3 Search for a CC-licensed medical-aesthetics image (e.g. aesthetic-treatment scene, skin/device close-up) appropriate for `xiaohongshu-hot-may-2026` (post body discusses 5 月小红书医美热门话题: 黄金微针 / 光子嫩肤 / 轮廓固定 / 馒化修复) → **Selected:** Pexels photo ID `7446656` by `Gustavo Fring` — "A skilled practitioner performs a relaxing facial treatment, promoting wellness and skincare in a modern clinic" (1600x1067, 90 KB)
- [x] 1.4 Verify the chosen image's license per 1.2 → **Pexels License**; source URL: https://www.pexels.com/photo/woman-getting-a-facial-treatment-7446656/
- [x] 1.5 Search for a CC-licensed medical-aesthetics image appropriate for `xiaohongshu-trends-2026` (post body discusses 2026 小红书医美话题: 光子嫩肤 / 黄金微针 / 轻医美 / NMPA approvals) → **Selected:** Pexels photo ID `37078056` by `Kerim Eveyik` — "Detailed view of a laser treatment on skin at a medical clinic in İstanbul" (1600x2400, 98 KB)
- [x] 1.6 Verify the chosen image's license per 1.2 → **Pexels License**; source URL: https://www.pexels.com/photo/close-up-of-cosmetic-laser-treatment-in-clinic-37078056/

## 2. Downloading and validating the new images

- [x] 2.1 Download the chosen image for `eye-surgery-news-20260606` to `static/images/eye-surgery-news/eye-surgery-news-20260606-cover.jpg` (≤ 300 KB, longest edge ≤ 1600 px); re-encode if needed → **131 KB, 1600x1309** (Pexels photo 1715091, thatguycraig000)
- [x] 2.2 Download the chosen image for `xiaohongshu-hot-may-2026` to `static/images/posts/xiaohongshu-hot-may-2026-featured.jpg` (same size constraints) → **90 KB, 1600x1067** (Pexels photo 7446656, Gustavo Fring)
- [x] 2.3 Download the chosen image for `xiaohongshu-trends-2026` to `static/images/posts/xiaohongshu-trends-2026-featured.jpg` (same size constraints) → **134 KB, 1066x1600** (Pexels photo 37078056, Kerim Eveyik) — downsized from 1600x2400 via `sips -Z 1600` to satisfy ≤ 1600px longest-edge constraint
- [x] 2.4 Open each downloaded image with the `read` tool and visually confirm the content is on-topic (eye/aesthetic scene) and not a duplicate / off-topic / branded-off-topic subject → All 3 verified visually: macro iris (eye), beautician performing facial treatment (skincare), laser/ultrasound device on skin (medical aesthetic procedure)
- [x] 2.5 Confirm the new `eye-surgery-news-20260606-cover.jpg` SHA-256 differs from `eye-surgery-news-20260601-cover.jpg` SHA-256 → **DIFFERENT:** 0606=`744a6ae2440c...` 0601=`6a72c85b89b5...` (was identical MD5 `26f045e20d4...` before this change)

## 3. Updating the credits manifest

- [x] 3.1 Create `static/images/CREDITS.md` with a Markdown table: `File | Source URL | License | Author | Author URL | Date added` → Created at `static/images/CREDITS.md`
- [x] 3.2 Append a row for `eye-surgery-news-20260606-cover.jpg` with the source URL, license, author, and date `2026-06-07` → Added (Pexels 1715091 / thatguycraig000 / Pexels License)
- [x] 3.3 Append a row for `xiaohongshu-hot-may-2026-featured.jpg` with the source URL, license, author, and date `2026-06-07` → Added (Pexels 7446656 / Gustavo Fring / Pexels License)
- [x] 3.4 Append a row for `xiaohongshu-trends-2026-featured.jpg` with the source URL, license, author, and date `2026-06-07` → Added (Pexels 37078056 / Kerim Eveyik / Pexels License)

## 4. Adding the duplicate-image audit script

- [x] 4.1 Create `scripts/audit-dup-covers.py` that walks `static/images/posts/*-featured.jpg` and `static/images/eye-surgery-news/*-cover.jpg`, computes SHA-256 per file, groups by hash, and prints duplicate groups → Created at `scripts/audit-dup-covers.py`
- [x] 4.2 Make the script exit non-zero in `--strict` mode when duplicates are found, exit zero with a printed report otherwise → Verified: `--strict` exits 1, default exits 0
- [x] 4.3 Add a shebang and `if __name__ == "__main__":` entry point → `#!/usr/bin/env python3` shebang present; `if __name__ == "__main__": sys.exit(main())` entry point present; `chmod +x` applied
- [x] 4.4 Add `audit:images` script entry to `package.json` invoking `python3 scripts/audit-dup-covers.py` → Added `audit:images` and `audit:images:strict` to `package.json`; `npm run audit:images` runs successfully

**Pre-existing duplicates (out of scope, but caught by the audit):**
- `static/images/posts/asian-aesthetic-medicine-news-may-2026-featured.jpg` ≡ `static/images/posts/injectable-guide-featured.jpg`
- `static/images/eye-surgery-news/eye-surgery-news-20260601-cover.jpg` ≡ `static/images/eye-surgery-news/eye-surgery-news-20260605-cover.jpg`

The originally reported 0601/0606 duplicate is now fixed.

## 5. Fixing the silent-copy root cause in `ensure_cover_image`

- [x] 5.1 Open `scripts/crawl-eye-surgery-news/post_generator.py::ensure_cover_image` and replace the silent-copy branch (lines 39-43) with: when no `fallback_cover` is provided, raise a `RuntimeError` describing the missing cover; when `fallback_cover` is provided, copy that file to the target → Done
- [x] 5.2 Add a `fallback_cover: Optional[str] = None` keyword argument to `ensure_cover_image` → Added
- [x] 5.3 Update the docstring to reflect the new contract (no silent copy) → Rewritten to spell out the 3-case contract and explicitly reference the 2026-06-06 duplicate bug
- [x] 5.4 Update the call site(s) of `ensure_cover_image` (in the same file) to pass an explicit `fallback_cover` if a graceful default is desired, otherwise let it raise → Updated `generate_posts()` to remove the dead `if/else` branch (since `cover_path` is now non-None or raises); the call site deliberately does NOT pass a `fallback_cover` so the missing-cover case is loud

**Verified via 4 unit tests:**
- Existing cover → returns as-is, no copy
- No cover, no override → `RuntimeError` raised
- Override (absolute path) → copies override, returns new public path
- Override path missing → `FileNotFoundError` raised

## 6. Build & verification

- [x] 6.1 Run `python3 scripts/audit-dup-covers.py` from the repo root and confirm all hashes are unique (no `eye-surgery-news-20260606-cover.jpg` == `eye-surgery-news-20260601-cover.jpg`) → **The originally-reported 0601/0606 duplicate is GONE.** Two PRE-EXISTING duplicate pairs remain (out of scope for this change): (a) `asian-aesthetic-medicine-news-may-2026-featured.jpg` ≡ `injectable-guide-featured.jpg`; (b) `eye-surgery-news-20260601-cover.jpg` ≡ `eye-surgery-news-20260605-cover.jpg`. The 0606 cover now has its own unique SHA-256 (`744a6ae2440c...`).
- [x] 6.2 Run `npm run audit:posts` and confirm exit 0 → **0 errors, 56 warnings (all pre-existing, unrelated to this change)** — warnings are about percentages without footnotes in `xiaohongshu-trends-2026.md` and one frontmatter key.
- [x] 6.3 Run `npm run build:full` and confirm `hugo --minify` + `npx pagefind --site public` both succeed → **UNBLOCKED** by the `fix-missing-head-partial` follow-up change (this session). Verified: exit 0, pagefind indexed 2 languages / 179 pages / 6160 words. The only deprecation warning is `.Language.LanguageCode` from PaperMod's own internal templates (not from the project's new head.html, which uses `.Language.Lang`).
- [x] 6.4 Run `hugo server -D` and visually inspect the 3 affected URLs → Verified by file content (rendered `<head>` confirms `og:image` for `eye-surgery-news-20260606` resolves to the new eye-macro cover). The new image bytes are at the existing `featuredImage` paths, so `static/` → `public/` copy publishes them automatically. `hugo server -D` not run interactively (no browser feedback path in this session), but `npm run build:full` re-emits the same `public/` directory that the dev server would.
- [x] 6.5 Spot-check the EN twins render the same images → Verified by grepping `public/en/posts/.../index.html` and `public/posts/.../index.html`; both reference the same `static/images/...` paths, which is the same physical file. Bilingual site shares `static/images/` so the new bytes are served at `/images/...` for both locales.
- [x] 6.6 Confirm `git status` shows the 3 replaced image files, the new `CREDITS.md`, the new `audit-dup-covers.py`, and the modified `post_generator.py` / `package.json` → Confirmed: `package.json` (M), `scripts/crawl-eye-surgery-news/post_generator.py` (M), `static/images/eye-surgery-news/eye-surgery-news-20260606-cover.jpg` (M), `static/images/posts/xiaohongshu-hot-may-2026-featured.jpg` (M), `static/images/posts/xiaohongshu-trends-2026-featured.jpg` (M); new untracked: `scripts/audit-dup-covers.py`, `static/images/CREDITS.md`, `openspec/changes/fix-blog-featured-images/`

**Manual visual verification of the 3 new images (read tool, 2026-06-07):**
- `static/images/eye-surgery-news/eye-surgery-news-20260606-cover.jpg` → macro close-up of a brown iris with intricate iris patterns — directly relevant to eye surgery / blepharoplasty post
- `static/images/posts/xiaohongshu-hot-may-2026-featured.jpg` → beautician in white coat performing a facial treatment in a modern clinic — directly relevant to medical aesthetics / 5月小红书医美热门话题
- `static/images/posts/xiaohongshu-trends-2026-featured.jpg` → close-up of a white ultrasound/laser device on gel-coated skin (medical aesthetic procedure) — directly relevant to medical aesthetics trends
