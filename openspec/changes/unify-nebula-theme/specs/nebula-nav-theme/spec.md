## ADDED Requirements

### Requirement: Navigation text readable on nebula background
The top navigation bar (`.header`) SHALL have sufficient contrast against the nebula background in both light and dark theme modes.

#### Scenario: Dark mode nav text visibility
- **WHEN** `[data-theme="dark"]`
- **THEN** `.header nav a`, `.header .logo a`, `.lang-menu a` SHALL use `color: #ffffff` or a color with a contrast ratio of at least 4.5:1 against the dark nebula background

#### Scenario: Light mode nav text visibility
- **WHEN** `[data-theme="light"]`
- **THEN** `.header nav a`, `.header .logo a`, `.lang-menu a` SHALL use `color: #1a1a2e` or a color with a contrast ratio of at least 4.5:1 against the light nebula background

#### Scenario: Active menu item visible
- **WHEN** a menu item has `aria-current="page"` or `.active`
- **THEN** it SHALL be highlighted with an underline or color treatment that is visible against the nebula background in both theme modes

### Requirement: Theme toggle button visible
The theme toggle sun/moon SVG icons SHALL be clearly visible against the nebula background.

#### Scenario: Dark mode toggle icons
- **WHEN** `[data-theme="dark"]`
- **THEN** `.theme-toggle svg` SHALL use `stroke: #ffffff` or a light color visible on dark nebula

#### Scenario: Light mode toggle icons
- **WHEN** `[data-theme="light"]`
- **THEN** `.theme-toggle svg` SHALL use `stroke: #1a1a2e` or a dark color visible on light nebula

### Requirement: Language switcher separator visible
The language switcher separator (`|`) SHALL be visible in both theme modes.

#### Scenario: Separator contrast
- **WHEN** inspecting `.nav-sep`
- **THEN** its color SHALL match the nearby text color in both `light` and `dark` theme modes

### Requirement: Navigation background blur/overlay
The header SHALL have a subtle background treatment to improve text legibility without obscuring the nebula.

#### Scenario: Header background in dark mode
- **WHEN** `[data-theme="dark"]`
- **THEN** `.header` SHALL have `background: rgba(5, 5, 16, 0.25)` with `backdrop-filter: blur(8px)` if supported

#### Scenario: Header background in light mode
- **WHEN** `[data-theme="light"]`
- **THEN** `.header` SHALL have `background: rgba(255, 255, 255, 0.2)` with `backdrop-filter: blur(8px)` if supported

### Requirement: Menu hover state visible
The GSAP menu link hover animation SHALL use colors that contrast against the nebula background.

#### Scenario: Hover color in dark mode
- **WHEN** a menu link is hovered in `[data-theme="dark"]`
- **THEN** the GSAP animation SHALL transition the link color to `#a0a0b0` (or a light gray)

#### Scenario: Hover color in light mode
- **WHEN** a menu link is hovered in `[data-theme="light"]`
- **THEN** the GSAP animation SHALL transition the link color to `#505070` (or a medium-dark gray)
