# Kaizen

## Purpose

`Kaizen` is WandererUI's navigation and focus management service.

It is responsible for determining which panel currently owns focus and how focus moves throughout the user interface.

Kaizen treats the interface as a navigation graph rather than a collection of widgets, allowing different layouts to coexist under a common navigation model.

---

## Responsibilities

Kaizen is responsible for:

- Managing panel focus.
- Moving focus between panels.
- Supporting multiple navigation modes.
- Locking and unlocking panel focus.
- Emitting focus change events.

Kaizen intentionally **does not** manage navigation inside applications. Once focus enters a panel, the application becomes responsible for navigating its own contents.

---

## Navigation Model

Kaizen represents the user interface as a directed graph.

Each panel stores its neighbouring panels for the four cardinal directions:

- Up
- Down
- Left
- Right

Moving focus simply traverses this graph.

This design allows new layouts to be introduced without changing Kaizen's navigation logic.

---

## Navigation Modes

Kaizen currently supports two navigation modes.

### Native Mode

Used by WandererUI's native applications.

Focus moves between the standard Wanderer panels:

- Header
- Navigation
- Viewport
- Context
- Footer

---

### Workbench Mode

Used when running non-native applications.

The workbench dynamically generates its own navigation graph and supplies it to Kaizen.

This allows Kaizen to reuse the same navigation system regardless of layout complexity.

---

## Panel Lock

Kaizen allows panel focus to be temporarily locked.

When panel locking is enabled:

- Focus remains inside the current panel.
- Directional navigation between panels is ignored.

This allows applications to implement their own internal navigation without interfering with WandererUI's global focus system.

---

## Theme Independence

Kaizen has no knowledge of:

- Colours
- Widgets
- Layout rendering
- Themes

Its responsibility is purely logical.

Visual feedback is handled by the Panel class.

---

## Public Interface

### Focus

- `initialize()`
- `current()`
- `set_focus()`
- `has_focus()`

### Navigation

- `move_up()`
- `move_down()`
- `move_left()`
- `move_right()`

### Locking

- `toggle_lock()`
- `unlock()`
- `is_locked()`

### Modes

- `set_mode()`
- `load_workbench_graph()`
- `active_graph()`

### Utilities

- `reset()`

### Signals

- `focus_changed`

---

## Interactions

Kaizen interacts with the following WandererUI components.

### Panel

Kaizen determines which panel owns focus.

Each Panel updates its visual appearance when focus changes.

---

### Applications

Applications use Kaizen to determine which panel currently owns focus.

Applications remain responsible for navigation within their own interface.

---

### Workbench

Workbench generates a navigation graph for non-native applications and provides it to Kaizen.

---

## Design Philosophy

Kaizen separates **global navigation** from **local navigation**.

Global navigation determines which panel currently owns focus.

Local navigation remains the responsibility of the focused application.

This separation allows every application to implement its own interaction model while maintaining a consistent desktop-wide navigation experience.

---

## Future Work

Potential future improvements include:

- User-configurable navigation graphs.
- Mouse-assisted focus transitions.
- Accessibility navigation modes.
- Additional layout modes.
- Navigation history.
- Multi-display focus support.