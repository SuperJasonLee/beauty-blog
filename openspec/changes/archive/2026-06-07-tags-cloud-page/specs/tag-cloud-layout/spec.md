## ADDED Requirements

### Requirement: Tag cloud layout

The `/tags/` page SHALL display tags as a visual tag cloud rather than a flat list.

#### Scenario: Tags render in a flowing layout

- **WHEN** the user navigates to `/tags/`
- **THEN** tags SHALL be rendered as inline elements inside a `flex-wrap` container
- **THEN** tags SHALL flow naturally across multiple lines with center alignment

#### Scenario: Font size reflects post count

- **WHEN** a tag has `count` posts associated with it
- **THEN** the tag's font size SHALL scale proportionally: count 1 → base size, count 2 → ~1.3x, count 3 → ~1.6x
- **THEN** the font size SHALL be computed using Hugo template math (inline style) or CSS `clamp()`

#### Scenario: Pill-style tag appearance

- **WHEN** a tag is displayed in the cloud
- **THEN** it SHALL appear as a pill-shaped element with rounded background
- **THEN** it SHALL have adequate padding for clickability
- **THEN** the background SHALL use a subtle semi-transparent color

### Requirement: Entrance animation

Tags SHALL animate into view with a staggered GSAP entrance effect on scroll.

#### Scenario: Tags stagger-enter on page load

- **WHEN** the `/tags/` page loads and GSAP is available
- **THEN** tags SHALL animate in using `ScrollTrigger.batch()` with stagger
- **THEN** each tag SHALL transition from `{ scale: 0.8, opacity: 0, y: 20 }` to its final state
- **THEN** the animation SHALL use `once: true` (play only on first scroll)

### Requirement: Hover interaction

Tags SHALL have a hover animation for better interactivity.

#### Scenario: Tag scales up on hover

- **WHEN** the user hovers over a tag
- **THEN** the tag SHALL scale up to 1.15x with a background color highlight
- **THEN** the transition SHALL be animated via GSAP `to()` with `duration: 0.3, ease: "power2.out"`
- **THEN** on mouse leave, the tag SHALL return to its original state

### Requirement: Responsive and accessibility

The tag cloud SHALL adapt to mobile viewports and respect motion preferences.

#### Scenario: Mobile adjustment

- **WHEN** the viewport width is less than 768px
- **THEN** the font size range SHALL be narrower (count 1 → 0.85rem, count 3 → 1.2rem)
- **THEN** the stagger interval SHALL be reduced

#### Scenario: Reduced motion

- **WHEN** the user has `prefers-reduced-motion: reduce`
- **THEN** no entrance animation SHALL play
- **THEN** hover animation SHALL be disabled
