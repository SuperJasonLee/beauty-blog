## Why

`npm run build:full` (Hugo + Pagefind) currently fails with:

```
error building site: render: [zh-cn v1.0.0 guest] failed to render pages:
  render of "/categories/皮肤美容" failed:
  "/Users/jasonlee/money/beauty-blog/layouts/baseof.html:16:8":
  execute of template failed: template: list.html:16:8:
  executing "list.html" at <partial "head.html" .>:
  error calling partial: partial "head.html" not found
```

Root cause: `layouts/baseof.html:16` calls `{{- partial "head.html" . }}`, but the project has no `layouts/partials/head.html`. The PaperMod theme is registered as a git submodule in `.gitmodules` but `themes/PaperMod/` is empty (the submodule was never initialized), so the theme's stock `head.html` is also missing.

This blocks every downstream task that depends on a working `hugo` build: Pagefind indexing, deploy previews, the duplicate-image-audit's static-output check, and any visual smoke test of the 3 affected URLs in the `fix-blog-featured-images` change (tasks 6.3, 6.4, 6.5).

It is also a latent risk on its own: the build is broken on `main` today and nobody can ship anything.

## What Changes

- Add `layouts/partials/head.html` containing the minimal HTML `<head>` metadata Hugo needs: charset, viewport, title, description, canonical, Open Graph / Twitter card, favicon, theme stylesheet, and the existing project-specific `extend_head.html` partial (which adds Google site verification, author meta, `sameAs` `me` links, and AdSense).
- Do **not** initialize the PaperMod submodule in this change. The project has built up a substantial `layouts/` override that does not depend on most of the theme's templates; adding the theme back wholesale would re-introduce templates the project has explicitly overridden and risks a much larger blast radius (CSS, menu rendering, etc.). The minimal `head.html` is the surgical fix.
- After the partial is added, `npm run build:full` (hugo + pagefind) must complete exit 0.
- Add a smoke-test task that runs the build before any future change can merge, so this regression cannot recur silently.

## Capabilities

### New Capabilities

- `head-partial`: a Hugo partial at `layouts/partials/head.html` that produces a complete, valid HTML `<head>` block, including the existing `extend_head.html` content (Google verification, author meta, `sameAs` `me` links, AdSense), and matches the project-specific `description`, `og:type`, and image defaults from `hugo.yaml`.

### Modified Capabilities

<!-- No existing spec-level capabilities are being modified. -->

## Impact

- Files added: `layouts/partials/head.html`
- Files NOT modified: `hugo.yaml`, `baseof.html`, `extend_head.html`, `adsense-head.html`, `header.html`, `footer.html`, `package.json`, `themes/PaperMod/.gitmodules`
- Build pipeline: `hugo --minify` now exits 0; `npx pagefind --site public` runs successfully
- Visual output: pages now render the same `description` / `og:title` / `og:image` / `og:locale` already configured in `hugo.yaml`
- No URL or frontmatter changes
- No breaking changes for readers; this is a build-fixes-no-content change
- Risk: low. The `head.html` content is derived from PaperMod's stock partial and the project's existing `hugo.yaml` config. If the project later wants to initialize the PaperMod submodule, the project's own `layouts/partials/head.html` will override the theme's, so there is no conflict.
