## 1. Move nebula container to baseof.html

- [x] 1.1 Move `<div id="nebula-container"></div>` from `layouts/_default/terms.html` to `layouts/baseof.html` after `<body>` opening
- [x] 1.2 Remove the conditional nebula wrapper (`{{- if eq .Type "tags" }}...{{- end }}`) from `terms.html`
- [x] 1.3 Ensure the closing `</div>` for the container is removed from the end of `terms.html`

## 2. Add nebula CSS per theme mode

- [x] 2.1 Add `[data-theme="light"]` nebula gradient override in `custom.css` (pastel light palette)
- [x] 2.2 Ensure the existing `[data-theme="dark"]` nebula gradient remains unchanged
- [x] 2.3 Add semi-transparent overlay (`.main::before`) for light mode and dark mode to improve text readability
- [x] 2.4 Match nebula container's `transition` duration to the site's 0.3s theme transition
- [x] 3.1 Remove the `window.location.pathname.startsWith('/tags/')` guard from `gsap-animations.html` section L
- [x] 3.2 Verify the particle system initializes on home, list, single, and terms pages
- [x] 3.3 Verify GSAP cleanup function still removes particles correctly on navigation

## 4. Style navigation for nebula readability (dark mode)

- [x] 4.1 Add `.header` background with `rgba(5, 5, 16, 0.25)` + `backdrop-filter: blur(8px)` for dark mode
- [x] 4.2 Set `.header nav a, .logo a, .lang-menu a` to `#ffffff` for dark mode
- [x] 4.3 Set `.theme-toggle svg` stroke to `#ffffff` for dark mode
- [x] 4.4 Update GSAP menu hover colors for dark mode (`var(--secondary)` → light gray)
- [x] 5.1 Add `.header` background with `rgba(255, 255, 255, 0.2)` + `backdrop-filter: blur(8px)` for light mode
- [x] 5.2 Set `.header nav a, .logo a, .lang-menu a` to `#1a1a2e` (dark navy) for light mode
- [x] 5.3 Set `.theme-toggle svg` stroke to `#1a1a2e` for light mode
- [x] 5.4 Update GSAP menu hover colors for light mode (`var(--secondary)` → medium-dark gray)
- [x] 6.1 Remove the `position: relative; z-index: 1` rule from `.header` in `custom.css` if no longer needed

## 6. Clean up CSS and verify

- [ ] 6.1 Remove the `position: relative; z-index: 1` rule from `.header` in `custom.css` if no longer needed
- [x] 6.2 Update `.post-content` and card grid entry backgrounds to be slightly transparent to show nebula beneath
- [ ] 6.3 Run `hugo server` and verify the site renders correctly in both light and dark modes (requires local Hugo install)
- [ ] 6.4 Verify all nav text, toggle icons, and language switcher are readable in both modes (visual check)
