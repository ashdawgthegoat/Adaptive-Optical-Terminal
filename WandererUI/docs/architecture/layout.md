# Layout

## Purpose

The Layout defines the overall structure of WandererUI.

It assembles the desktop environment by arranging the primary interface panels into a consistent and predictable workspace.

Every native WandererUI application is expected to integrate with this layout rather than creating its own desktop structure.

---

## Layout Structure

The desktop is composed of five primary regions.

```
Header

Navigation | Viewport | Context

Footer
```

Each region has a dedicated responsibility and remains visually consistent across the desktop environment.

---

## Panel Responsibilities

### Header

Provides global desktop information and quick actions.

Typical responsibilities include:

- Runtime information
- System status
- Appearance shortcuts
- Date and time

---

### Navigation

Provides application-specific navigation.

Each native application supplies its own navigation entries while preserving the Navigation Panel itself.

---

### Viewport

The primary workspace.

This panel displays the application's main content.

Most user interaction occurs within the Viewport.

---

### Context

Displays contextual information related to the currently selected item or active application.

Context should complement the Viewport rather than duplicate it.

---

### Footer

Displays persistent desktop status information.

The Footer remains visible regardless of the active application.

---

## Layout Ratios

The body layout currently follows the ratio:

```
Navigation : Viewport : Context

2 : 6 : 2
```

This prioritizes the Viewport while maintaining sufficient space for navigation and contextual information.

---

## Theme Integration

All spacing, margins and presentation values are provided by Maaya.

The Layout should never hardcode visual styling beyond structural positioning.

---

## Interactions

The Layout assembles the following components:

- Header
- Navigation Panel
- Viewport
- Context Panel
- Footer

Each component remains independently responsible for its own rendering and behaviour.

---

## Design Philosophy

The Layout separates **desktop structure** from **application content**.

Applications populate the existing panels rather than replacing the desktop itself.

This ensures every native application feels like a natural extension of WandererUI while preserving a consistent user experience.

---

## Future Work

Potential future improvements include:

- Collapsible panels.
- Dynamic panel resizing.
- Multi-monitor layouts.
- Tablet-friendly layouts.
- Application-specific layout presets.