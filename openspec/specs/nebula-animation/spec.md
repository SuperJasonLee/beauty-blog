## ADDED Requirements

### Requirement: Nebula particle system

The system SHALL render a moving nebula (star cloud) particle background on the tags page using GSAP-driven DOM animation.

#### Scenario: Particles are created on page load

- **WHEN** the tags page loads and `gsap` is defined
- **THEN** the system SHALL dynamically create 100-200 particle elements inside the nebula container
- **THEN** each particle SHALL be a `<span>` element with the `nebula-particle` class

#### Scenario: Particles begin animating immediately

- **WHEN** particles are created
- **THEN** each particle SHALL start a continuous GSAP `to()` animation with random position, duration, and delay
- **THEN** the animation SHALL use `repeat: -1` and `yoyo: true` for continuous back-and-forth motion

#### Scenario: Mouse interaction shifts particles

- **WHEN** the user moves the mouse over the tags page
- **THEN** particles near the cursor SHALL subtly shift away (parallax effect)
- **THEN** the shift SHALL be animated via GSAP with `overwrite: "auto"` for smooth transitions

### Requirement: Nebula container and styling

The system SHALL provide a full-screen background container for particles, styled with a dark gradient background.

#### Scenario: Container is positioned behind content

- **WHEN** the tags page loads
- **THEN** a `<div id="nebula-container">` SHALL exist as the first child of the page `<main>` element
- **THEN** it SHALL use `position: fixed` covering the full viewport
- **THEN** it SHALL have `z-index: 0` so page content renders above it
- **THEN** it SHALL have a dark radial gradient background to contrast particle glow

#### Scenario: Particle styling

- **WHEN** a particle is created
- **THEN** it SHALL be `position: absolute` with `border-radius: 50%`
- **THEN** its size SHALL be between 2px and 6px (random)
- **THEN** it SHALL have a semi-transparent glow effect via `box-shadow`

### Requirement: Responsive and accessibility

The system SHALL degrade gracefully on mobile devices and respect user motion preferences.

#### Scenario: Mobile device reduces particle count

- **WHEN** the viewport width is less than 768px
- **THEN** the system SHALL create no more than 60 particles

#### Scenario: Reduced motion preference disables animation

- **WHEN** the user has `prefers-reduced-motion: reduce`
- **THEN** the system SHALL NOT create or animate any particles
- **THEN** no nebula container SHALL be rendered

### Requirement: Tags page only

The animation SHALL only activate on the tags taxonomy page.

#### Scenario: Only activates on /tags/ page

- **WHEN** the current page is the tags listing (`/tags/` with HTML title matching "标签" or "Tags")
- **THEN** the nebula animation SHALL initialize

#### Scenario: Does not activate on other pages

- **WHEN** the current page is a single post, home page, or search page
- **THEN** the nebula animation SHALL NOT initialize
