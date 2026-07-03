# Maaya

## Purpose

`Maaya` is WandererUI's presentation service.

It is responsible for loading, managing and exposing the visual and multimedia assets used throughout the desktop environment.

Maaya ensures that every visual component retrieves its appearance from a single source of truth.

---

## Responsibilities

Maaya is responsible for:

- Loading themes.
- Loading fonts and typography.
- Loading wallpapers.
- Loading sounds.
- Loading animations.
- Managing presentation packages.
- Caching loaded resources.

Maaya intentionally does **not** render widgets or control application behaviour.

---

## Presentation Packages

Maaya manages the following asset categories:

- Themes
- Fonts
- Wallpapers
- Sounds
- Animations

Each package is loaded dynamically from the `assets/` directory.

---

## Theme System

Themes define the visual appearance of WandererUI.

A theme may expose:

- Colours
- Borders
- Spacing
- Other presentation properties

Applications should always retrieve visual properties through Maaya rather than hardcoding values.

---

## Typography

Fonts are loaded dynamically at runtime.

Each font package may optionally provide its own typography definition.

If no typography definition exists, Maaya provides a default typography configuration.

---

## Wallpaper System

Maaya supports multiple wallpaper types, including:

- ASCII
- Static images
- Native animated wallpapers

Wallpaper alignment is managed independently from wallpaper loading.

---

## Animation System

Animations may be implemented using:

- Frame sequences
- Native media formats

Frame-based animations are controlled internally using a timer.

Applications receive animation updates through signals.

---

## Cache

Loaded packages are cached to avoid unnecessary disk access and repeated imports.

---

## Public Interface

### Package Discovery

- `available_themes()`
- `available_fonts()`
- `available_wallpapers()`
- `available_sounds()`
- `available_animations()`

### Presentation

- `load_theme()`
- `load_font()`
- `load_wallpaper()`
- `load_sound()`
- `load_animation()`

### Animation

- `play()`
- `pause()`
- `stop()`
- `next_frame()`
- `set_fps()`
- `current_frame()`

### Utilities

- `typography()`
- `clear_cache()`

### Signals

- `frame_changed`

---

## Interactions

Maaya interacts with:

### Panel

Provides colours, borders and spacing used for rendering.

### Native Applications

Provides fonts, typography and presentation assets.

### Wallpaper System

Supplies wallpaper information to the Viewport.

---

## Design Philosophy

Maaya separates **presentation** from **logic**.

Native applications should never hardcode visual properties.

Instead, every component retrieves its appearance through Maaya, allowing the entire desktop environment to change its presentation without modifying application code.

---

## Future Work

Potential future improvements include:

- Icon themes.
- Cursor themes.
- Sound themes.
- Dynamic theme switching.
- User-defined presentation packages.
- Theme inheritance.