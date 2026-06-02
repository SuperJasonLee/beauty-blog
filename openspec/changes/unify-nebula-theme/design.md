## Context

The site currently uses PaperMod's default solid-color backgrounds (white in light mode, near-black in dark mode) on all pages except `/tags/`, which has a nebula particle background with GSAP animation. The proposal aims to unify the nebula theme across all pages while ensuring text and navigation remain readable.

Key files involved:
- `assets/css/extended/custom.css` — all custom CSS including nebula styles (lines 286-309), nav, card grid
- `layouts/_default/terms.html` — nebula container and tag cloud (tags page only)
- `layouts/partials/gsap-animations.html` — particle animation JS (section L, lines 178-271)
- `layouts/partials/header.html` — nav structure
- `layouts/baseof.html` — base template with data-theme attribute

## Goals / Non-Goals

**Goals:**
- Move the nebula container from `terms.html` to `baseof.html` so it renders on every page
- Ensure the nebula particle system initializes on all pages (not just `/tags/`)
- Adjust CSS custom properties to maintain readable text contrast against the nebula in both light and dark modes
- Override navigation (`.header`, `.menu`, `.logo`, `.theme-toggle`, `.lang-menu`) colors specifically for nebula readability
- Maintain the existing dark/light mode toggle — both modes get nebula backgrounds with distinct color treatments
- Keep the GSAP cleanup on page navigation working correctly

**Non-Goals:**
- Changing the particle count, size, color range, or mouse repulsion behavior (keep existing parameters)
- Adding new animation effects or interactivity
- Modifying article content, card grid, footer, or other non-header/non-background elements beyond theming
- Changing the tag cloud layout or behavior

## Decisions

**1. Move nebula container to `baseof.html`**
- **Choice**: Insert `<div id="nebula-container"></div>` immediately after `<body>` in `baseof.html`
- **Rationale**: Ensures universal coverage without editing each page template
- **Alternative considered**: Adding via Hugo partial in each template — rejected as more error-prone

**2. Use CSS overlay + blurred background for readability**
- **Choice**: Add a semi-transparent overlay (`::after` pseudo-element on `.main`) between content and nebula to soften the background for text readability. Light mode: light overlay (white/transparent). Dark mode: dark overlay.
- **Rationale**: Cleanest way to ensure text readability without changing the vibrant nebula colors. Avoids needing complex per-element contrast adjustments.
- **Alternative considered**: Adjusting nebula particle opacity/colors per mode — rejected because it reduces visual impact

**3. Navigation readability via separate CSS variables**
- **Choice**: Define `--nav-text`, `--nav-text-hover`, `--nav-bg` CSS variables that override for the header specifically
- **Rationale**: The nav sits on top of the nebula and needs its own contrast treatment independent of page content
- **Alternative considered**: Using shadows/backdrop-filter on nav — rejected for browser compatibility concerns

**4. Light mode nebula treatment**
- **Choice**: Nebula background uses a lighter gradient (pastel space colors with lighter overlay) and particles with higher opacity
- **Rationale**: In light mode, the default dark nebula would make content unreadable without heavy overlays
- **Implementation**: `[data-theme="light"] #nebula-container` overrides the background to a lighter nebula palette

**5. Particle animation initialization**
- **Choice**: Initialize particles in GSAP animations on all pages, not just `/tags/`
- **Rationale**: Consistent visual experience across the entire site
- **Action**: Remove the `window.location.pathname.startsWith('/tags/')` guard in section L of `gsap-animations.html`
- **Performance**: Keep existing `isMobile` particle count reduction (60 vs 150) and mousemove throttle

## Risks / Trade-offs

- **[Performance] Full-site particle animation on every page** — The particle system was designed for a single page. Running it on every page visit may increase CPU usage. **Mitigation**: The existing throttle (40ms) and mobile reduction (60 particles) are reasonable. Monitor via Lighthouse.
- **[SEO] Content readability with nebula background** — The overlay approach could make text harder to read if overlay opacity is too low. **Mitigation**: Test with actual content and adjust overlay opacity (target 0.15-0.25 for light mode, 0.3-0.4 for dark mode).
- **[Cleanup] Nebula container state on SPA-like navigation** — The GSAP cleanup function already handles removing particles. **Mitigation**: Verify the cleanup in `gsap-animations.html` (line 300-307) works correctly when nebula is on every page (not just tags).
- **[Theme transition] Flash between modes** — The nebula background transition (1.5s ease) may clash with the existing 0.3s theme transition. **Mitigation**: Keep nebula transition at 0.3s to match the theme transition.
