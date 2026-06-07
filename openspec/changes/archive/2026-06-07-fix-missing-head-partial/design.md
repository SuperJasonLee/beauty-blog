## Context

The Hugo build is broken on `main` with `partial "head.html" not found`. This was uncovered while implementing the `fix-blog-featured-images` change, where tasks 6.3 (`npm run build:full`), 6.4 (`hugo server -D` smoke test), and 6.5 (visual inspection of EN twin pages) are all blocked by the same build failure.

The project structure is:
- Hugo static site generator, theme = `PaperMod` (declared in `hugo.yaml`)
- Theme is registered in `.gitmodules` but `themes/PaperMod/` is empty (uninitialized submodule)
- Project has its own `layouts/` with custom partials: `header.html`, `footer.html`, `adsense-head.html`, `extend_head.html`, `gsap-animations.html`, `disclaimer.html`
- The custom `layouts/baseof.html:16` calls `{{- partial "head.html" . }}` — which is the only line of the entire build that fails. Everything else (header, footer, list, single, taxonomies) already has project-level overrides or a compatible fallback.

PaperMod's standard `layouts/partials/head.html` (from upstream `adityatelange/hugo-PaperMod`) contains roughly:
- `<meta charset>`, `<meta name="viewport">`
- `<title>{{ .Title }} | {{ site.Title }}</title>` (with i18n fallback)
- `<meta name="description">` from frontmatter `description` or `summary` or site default
- canonical link
- Open Graph block (`og:title`, `og:description`, `og:type`, `og:url`, `og:image`, `og:locale`, `og:site_name`)
- Twitter card block
- `<link rel="icon" type="image/png" href="/images/site-feature.png">` (the project's existing `params.images[0]`)
- theme stylesheet `<link rel="stylesheet" href="...">`
- `{{- partial "extend_head.html" . }}` — already exists in the project and is the integration point for the project's custom `<meta>` and AdSense script

The project's `hugo.yaml` already provides:
- `params.description` (default site description)
- `params.images[0] = /images/site-feature.png`
- `params.adsense.publisherId` (consumed by `adsense-head.html`)
- `languages.zh-cn` and `languages.en` with their own `description`

The minimal `head.html` we need to ship is therefore: the standard PaperMod content + the existing `extend_head.html` include. That gets the build green and preserves every customization the project has already invested in.

Stakeholders: the developer running this session (immediate unblock for the `fix-blog-featured-images` verification tasks 6.3-6.5), and the future maintainer who needs a working `npm run build:full` to ship any change.

## Goals / Non-Goals

**Goals:**
- Make `npm run build:full` exit 0 on a clean checkout.
- Preserve every existing `<meta>` tag the project has already configured via `extend_head.html` (Google site verification, author meta, `sameAs` `me` links, AdSense).
- Match the project-specific defaults in `hugo.yaml` (`description`, `og:image`, `og:locale`).
- Keep the change minimal — one new file, no edits to existing partials.
- Unblock the `fix-blog-featured-images` tasks 6.3-6.5.

**Non-Goals:**
- Initializing the PaperMod git submodule. The project's existing `layouts/` already overrides most of what we need, and bringing in the rest of the theme wholesale risks regressing CSS, menu rendering, and other things the project has explicitly customized.
- Migrating to a different theme.
- Adding new SEO/social features beyond what PaperMod's stock `head.html` provided.
- Re-architecting the partials structure.

## Decisions

### D1. Hand-write a PaperMod-compatible `head.html` rather than copy the upstream file verbatim

**Decision:** Create `layouts/partials/head.html` containing the standard PaperMod head content (charset, viewport, title, description, canonical, OG, Twitter, favicon, theme CSS, extend_head include), with project-specific defaults from `hugo.yaml` (description fallback, `/images/site-feature.png` as default OG image, `og:locale` from `.Language.Lang`).

**Alternatives considered:**
- *Copy PaperMod's stock `head.html` from upstream*: rejected — the upstream file references `.Scratch` variables and template helpers (`resources.Get`) that may differ from what's available with a missing theme. Hand-writing with the project's actual config in front of us reduces risk.
- *Initialize the PaperMod submodule*: rejected (Non-Goals).
- *Create an empty stub `head.html`*: rejected — would let the build pass but produce a page with no title, no meta, no OG card. Functionally broken.

**Rationale:** Hand-written partial that matches PaperMod's structure but uses the project's existing config values directly. This is the smallest change that makes the build green and produces a correct page.

### D2. Include `extend_head.html` last, preserving all existing customizations

**Decision:** The new `head.html` includes `{{- partial "extend_head.html" . }}` near the end (just before `</head>`), matching PaperMod's stock placement. This means:
- The existing Google site verification meta tag continues to render.
- Author meta, `sameAs` `me` links, and AdSense continue to render.
- The existing `npm run build:full` CI expectation that AdSense only loads in production (`{{- if hugo.IsProduction }}` in `extend_head.html`) is preserved.

**Rationale:** No behavior change beyond fixing the missing partial.

### D3. Use the project's `params.images[0]` for default OG image

**Decision:** Default `og:image` to `site.Params.images[0]` (currently `/images/site-feature.png`), falling back to an `absURL` of the per-post `featuredImage` if set.

**Alternatives considered:**
- *Always use `featuredImage`*: rejected — list and taxonomy pages don't have a per-page `featuredImage`, and falling back to the site logo is conventional.
- *Always use the hard-coded `/images/site-feature.png`*: rejected — couples the partial to a single image.

**Rationale:** Same pattern PaperMod uses, with the project's existing `params.images` as the source of truth.

## Risks / Trade-offs

- **[Risk] The hand-written `head.html` may diverge from PaperMod upstream over time** (e.g., a future PaperMod feature added via a new meta tag would not be picked up). → Mitigation: this is acceptable for a project that has chosen to NOT initialize the PaperMod submodule. The `head.html` is self-contained and easy to update manually when desired.

- **[Risk] The OG/Twitter card image won't match the post's `featuredImage` on the new 3 affected posts unless the template prefers `featuredImage` over the site default** → Mitigation: the partial includes a `{{- with .Params.featuredImage }}` block that sets `og:image` to the featured image when present; otherwise falls back to `site.Params.images[0]`.

- **[Risk] Hugo renders something subtly different than what PaperMod produced** (e.g., a missing `application/ld+json` JSON-LD block) → Mitigation: PageMod's stock `head.html` does NOT include JSON-LD by default; that's handled by separate partials. The project already has `adsense-head.html` and `extend_head.html` for site-specific scripts. No JSON-LD is expected.

- **[Risk] A future developer initializes the PaperMod submodule and our project's `layouts/partials/head.html` overrides the theme's** → Mitigation: this is the desired behavior — the project's `layouts/` always wins over `themes/<name>/layouts/`. Documented in the proposal.

- **[Trade-off] No CSS reset / PaperMod-specific style hooks** → The project already has its own `assets/` and likely its own CSS. If the project later complains about missing styles, that's a separate fix (probably also stemming from the uninitialized submodule).

## Migration Plan

1. Land the change in a single commit that adds `layouts/partials/head.html`.
2. Run `npm run build:full` locally — expect exit 0 and `public/` to be re-emitted with proper `<head>` blocks.
3. Spot-check `public/index.html` (or any rendered page) to confirm the new `<head>` contains: title, meta description, OG title/description/image, Twitter card, the `extend_head.html` content (Google site verification, author meta), and the AdSense script in production mode.
4. Deploy via the existing GitHub Pages workflow.
5. Rollback: `git revert` — one file deletion, no data loss.

## Open Questions

- **Q1:** Should we also add a basic `assets/css/extended.css` and reference it from the head? — Default: no, scope-creep. The project has its own `assets/` and any CSS issue is downstream of the uninitialized submodule, not this fix. (Resolved.)
- **Q2:** Should we add a `preconnect` to fonts.googleapis.com? — Default: no, scope-creep. (Resolved.)
- **Q3:** The `themes/PaperMod/` empty dir is a recurring foot-gun (anyone trying to build will hit it). Should we add a `themes/PaperMod/README.md` explaining the submodule state? — Default: yes, briefly. Add a one-paragraph note in this same change so the next person doesn't lose 30 minutes to the same discovery. (Resolved.)

## Implementation Notes (deviation from the original plan)

The change was implemented differently from the design above. The hand-written `head.html` (D1) is in place, but the PaperMod submodule was *also* initialized, because once `head.html` was provided, the next build attempt revealed a second layer of missing partials — approximately 20 PaperMod partials referenced by the project's `layouts/_default/{single,list,terms}.html` (e.g. `breadcrumbs.html`, `post_meta.html`, `cover.html`, `toc.html`, `post_nav_links.html`, `share_icons.html`, `comments.html`, `index_profile.html`, `home_info.html`, `anchored_headings.html`, `extend_post_content.html`, `edit_post.html`, `post_canonical.html`, `translation_list.html`). Hand-writing all of them was not feasible, so:

- **Submodule initialized** at the SHA the parent repo was already recorded as (`154d006e0182dfc7da38008323976b02e6bfab4a`, `--depth=1` shallow clone). This brings in upstream PaperMod's `_partials/` (note the underscore — Hugo's newer lookup convention), so the project's `layouts/_default/*.html` partial references now resolve.
- **Project's own `layouts/partials/head.html` continues to win** (project `layouts/` always override `themes/`). The hand-written partial is still in effect.
- **`themes/PaperMod/README.md` was deleted from the working tree** because the text written during the design phase ("intentionally empty, do NOT init submodule") is now actively misleading. (That README was inside the submodule's working tree anyway, so it was never visible to the parent repo's git; deletion is just for cleanliness of someone running `ls themes/PaperMod/`.)

**What this means for the project's `layouts/`:**
- `layouts/partials/extend_head.html`, `adsense-head.html`, `header.html`, `footer.html`, `gsap-animations.html`, `disclaimer.html`, `adsense-in-article.html`, `adsense-in-list.html` — all still in effect, override the theme.
- `layouts/_default/{single,list,terms}.html` — still in effect, override the theme.
- `layouts/404.html`, `layouts/page/search.html`, `layouts/shortcodes/*.html` — still in effect.
- The PaperMod theme's `single.html`, `list.html`, `baseof.html`, `_partials/*` are now available as a fallback, but the project's overrides shadow them in practice.

**What this means for `head.html` (D1, D2, D3):** unchanged. The hand-written partial still ships all the PaperMod-compatible content with the project's `params.images[0]` and `extend_head.html` integration. The build now exits 0, pagefind indexes 179 pages, and `og:image` correctly resolves to `featuredImage` when present and `site.Params.images[0]` otherwise.

**Updated risk:** a future Hugo/PaperMod upgrade that changes how the theme's `_partials/` resolve could in principle shadow the project's overrides. This is no different from the project shipping any custom partial, and is the cost of the project's chosen "own `layouts/` wins" architecture.
