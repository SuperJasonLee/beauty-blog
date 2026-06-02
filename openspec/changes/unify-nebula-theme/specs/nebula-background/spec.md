## ADDED Requirements

### Requirement: Full-site nebula container
The nebula background container SHALL be rendered in `baseof.html` after the `<body>` tag so it appears on every page.

#### Scenario: Container exists on all pages
- **WHEN** any page is loaded (home, list, single, terms)
- **THEN** the DOM SHALL contain `<div id="nebula-container"></div>` as a child of `<body>`

#### Scenario: Container z-index is behind content
- **WHEN** inspecting `#nebula-container` position
- **THEN** it SHALL have `position: fixed; z-index: 0; pointer-events: none`

### Requirement: Nebula background gradient per theme mode
The nebula container SHALL display a different background gradient depending on the current `data-theme` attribute.

#### Scenario: Dark mode nebula gradient
- **WHEN** `[data-theme="dark"]` (or `auto` with `prefers-color-scheme: dark`)
- **THEN** `#nebula-container` SHALL use `radial-gradient(ellipse at 50% 40%, #12102a 0%, #0a0a1a 40%, #050510 100%)`

#### Scenario: Light mode nebula gradient
- **WHEN** `[data-theme="light"]` (or `auto` with `prefers-color-scheme: light`)
- **THEN** `#nebula-container` SHALL use a lighter gradient: `radial-gradient(ellipse at 50% 40%, #d4c9e6 0%, #e8e0f0 40%, #f5f0fa 100%)`

### Requirement: Semi-transparent content overlay
A CSS overlay SHALL be applied between the nebula background and the page content to ensure text readability.

#### Scenario: Light mode overlay
- **WHEN** `[data-theme="light"]`
- **THEN** `.main` SHALL have a `::before` pseudo-element with `background: rgba(255,255,255,0.2)` covering the full area

#### Scenario: Dark mode overlay
- **WHEN** `[data-theme="dark"]`
- **THEN** `.main` SHALL have a `::before` pseudo-element with `background: rgba(0,0,0,0.35)` covering the full area

#### Scenario: Overlay does not block interactions
- **WHEN** clicking or scrolling on the overlay
- **THEN** events SHALL pass through to underlying content (`pointer-events: none`)

### Requirement: Particle animation on all pages
The GSAP nebula particle system SHALL initialize on every page, not only on the `/tags/` page.

#### Scenario: Particles created on all pages
- **WHEN** any page loads and the DOM contains `#nebula-container`
- **THEN** `nebula-particle` span elements SHALL be appended to `#nebula-container`

#### Scenario: Mobile particle count reduced
- **WHEN** `window.innerWidth < 768`
- **THEN** no more than 60 particles SHALL be created (otherwise 150)

#### Scenario: Theme transition matches site
- **WHEN** the `data-theme` attribute changes
- **THEN** `#nebula-container` background SHALL transition in `0.3s ease` to match the site theme transition

### Requirement: Nebula cleanup on page navigation
The GSAP cleanup function SHALL properly remove all nebula particles and styles when navigating away.

#### Scenario: Particles removed on cleanup
- **WHEN** the GSAP `matchMedia` cleanup function runs
- **THEN** `#nebula-container` SHALL have class `active` removed and all `.nebula-particle` elements SHALL be removed from DOM
