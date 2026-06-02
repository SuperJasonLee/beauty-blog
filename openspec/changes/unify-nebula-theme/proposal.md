## Why

Currently, the nebula starry-sky background effect only exists on the `/tags/` page, creating an inconsistent visual experience. The rest of the site uses PaperMod's default solid-color backgrounds. Unifying the background across all pages to a consistent nebula theme will create a cohesive brand identity and immersive visual experience that aligns with the beauty/aesthetic medicine content. Additionally, the top navigation needs color adjustments to ensure text remains readable against the nebula background in both light and dark modes.

## What Changes

- Extend the nebula particle background from `/tags/` page to all pages on the site (home, articles, archives, about, etc.)
- Adjust CSS custom properties (theme variables) so text and UI elements contrast properly against the nebula background in both light and dark modes
- Update top navigation (header) styling to ensure all menu items, logo, theme toggle, and language switcher are readable
- Reposition or rework the nebula container for universal use (not just tags page)
- Ensure the particle animation (GSAP) works across all pages without performance degradation
- Apply consistent nebula-themed color palette (deep space purples, blues, with visible text) across both themes
- Maintain existing dark/light mode toggle functionality — both modes should have nebula backgrounds but with different color overlays

## Capabilities

### New Capabilities
- `nebula-background`: Full-site nebula starry-sky particle background system spanning all pages with configurable colors per theme mode
- `nebula-nav-theme`: Top navigation theming that ensures text/UI readability on the nebula background in both light and dark modes

### Modified Capabilities
None — this is a visual/thematic overhaul, not a change to existing feature requirements.

## Impact

- `assets/css/extended/custom.css`: Major CSS changes — new CSS variables for nebula theme, nav readability overrides, background styling for all page types
- `layouts/partials/header.html`: Nav styling adjustments, potentially structural changes for nebula overlay compatibility
- `layouts/partials/gsap-animations.html`: Particle animation configuration extended from tags-only to site-wide
- `layouts/_default/list.html`, `single.html`, `baseof.html`, `terms.html`: Nebula container placement across page templates
- `hugo.yaml`: Potential theme parameter additions
- Site performance: Particle animation on every page may impact render performance; mitigation needed
