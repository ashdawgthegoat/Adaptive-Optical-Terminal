# Panel

## Purpose

The `Panel` class is the fundamental visual building block of WandererUI.

It provides a common foundation for every major user interface surface, ensuring a consistent appearance, interaction model and focus behaviour throughout the desktop environment.

Every major UI component (Header, Navigation Panel, Viewport, Context Panel and Footer) inherits from this class.

---

## Responsibilities

The `Panel` class is responsible for:

- Managing the panel's focus state.
- Rendering borders consistently using the active theme.
- Providing a safe content area inside panel borders.
- Emitting mouse interaction events.
- Providing a common base class for all WandererUI panels.

The `Panel` class intentionally **does not** decide what a panel displays. Its responsibility ends at rendering and interaction.

---

## Focus System

Each panel exists in one of two states:

- **Active**
- **Inactive**

The active state is controlled by Kaizen and determines how the panel is visually rendered.

The Panel itself does not decide when it becomes active or inactive.

---

## Border Rendering

Unlike traditional Qt widgets that rely heavily on stylesheets, WandererUI renders its borders manually.

Rendering is performed inside the `paintEvent()` function using Qt's painting system.

This provides:

- Consistent rendering.
- Theme-controlled border colours.
- Variable border thickness.
- Future support for more advanced border styles.

Panels that do not require a visible border (such as the Header's child widgets) can disable border rendering while still participating in the focus system.

---

## Content Padding

A panel automatically reserves space for its border before placing child widgets.

The required padding is calculated using the current theme's border properties.

This ensures that child widgets never overlap the panel border regardless of border thickness.

---

## Theme Integration

`Panel` retrieves all visual properties from Maaya.

These include:

- Border colours
- Border thickness
- Border padding

The Panel never hardcodes visual values.

---

## Public Interface

### Focus

- `set_active()`
- `set_inactive()`
- `is_active()`

### Layout

- `content_padding()`

### Signals

- `clicked`

---

## Interactions

The Panel interacts with the following WandererUI services:

### Maaya

Provides colours, border widths and border padding.

### Kaizen

Controls which panel currently owns focus.

The Panel only reflects the focus state visually.

---

## Design Philosophy

The Panel exists to separate **behaviour** from **content**.

Every panel in WandererUI should behave consistently regardless of what information it displays.

This allows higher-level components to focus solely on their own responsibilities while relying on Panel for rendering, focus behaviour and layout management.

---

## Future Work

Potential future improvements include:

- Rounded border support.
- Animated focus transitions.
- Theme-controlled border styles.
- Optional shadow rendering.
- Additional accessibility states.

These features should be implemented inside `Panel` so that every inheriting component benefits automatically.