# Runtime Widget

## Purpose

The `Runtime Widget` provides a concise summary of the current desktop session.

It displays the currently active location within WandererUI together with the number of running applications.

The Runtime Widget serves as a lightweight status indicator rather than an application launcher.

---

## Responsibilities

The Runtime Widget is responsible for:

- Displaying the current location.
- Displaying the number of running applications.
- Presenting runtime information inside the Header.
- Emitting activation events.

The Runtime Widget intentionally **does not** determine what information should be displayed.

---

## Information Source

Runtime information is supplied externally.

The widget receives updated information through its public interface and simply presents it to the user.

Animus acts as the source of truth for application state.

---

## Public Interface

### Runtime

- `update_runtime()`

### Signals

- `activated`

---

## Interactions

The Runtime Widget interacts with the following WandererUI components.

### Animus

Animus provides the currently active application and the number of running applications.

---

### Header

The Runtime Widget occupies the centre section of the Header.

---

### Future Overlay System

Activating the Runtime Widget may display the running applications overlay or future workspace management interface.

---

## Design Philosophy

The Runtime Widget provides **context**, not control.

It allows the user to immediately understand where they are within WandererUI while remaining visually lightweight and unobtrusive.

---

## Future Work

Potential future improvements include:

- Active workbench indicator.
- Running application switcher.
- Workspace overview.
- Recent application history.
- Session status integration with Eidolon.