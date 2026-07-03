# Native Applications

## Purpose

A Wanderer Native Application is an application designed specifically for the WandererUI desktop environment.

Unlike conventional desktop applications, native applications are aware of the WandererUI layout and integrate directly with its architecture, services and navigation model.

Their goal is to feel like a natural extension of the desktop environment rather than an independent window.

---

## Layout

A native application occupies the central workspace of WandererUI.

Applications must occupy **at least two** of the following panels:

- Navigation
- Viewport
- Context
- Footer

Applications may occupy **up to all four** of these panels depending on their requirements.

The **Header** is reserved for global desktop information and is never owned by an application.

Applications populate existing panels rather than replacing the desktop itself.

---

## Core Services

Native applications should integrate with WandererUI's core services whenever appropriate.

### Maaya

Responsible for presentation.

Applications should retrieve:

- Colours
- Fonts
- Typography
- Spacing
- Theme information

Applications should never hardcode presentation values.

---

### Kaizen

Responsible for desktop-wide focus and inter-panel navigation.

Kaizen determines which panel currently owns focus.

Navigation inside a panel remains the responsibility of the application itself.

---

### Animus

Responsible for application lifecycle management.

Applications register themselves with Animus and rely on it for:

- Registration
- Launching
- Closing
- Runtime tracking
- Workbench interaction

Animus remains the source of truth for application state.

---

### Eidolon *(Future)*

Responsible for session persistence.

Applications should expose sufficient state for Eidolon to restore previous sessions when required.

---

## Native Application Principles

A native application should:

- Respect the WandererUI layout.
- Integrate with the core services.
- Reuse existing desktop panels.
- Avoid replacing the desktop interface.
- Feel visually consistent with the rest of WandererUI.

---

# Non-Native Applications

A non-native application is an application that was not designed specifically for WandererUI.

These applications are executed inside the **Workbench**, where they remain isolated from the native desktop layout.

Non-native applications are not required to understand WandererUI's architecture.

---

# Workbench

## Purpose

The Workbench is WandererUI's runtime environment for executing applications.

It provides an isolated workspace where both native and non-native applications can coexist without affecting the primary desktop experience.

Unlike the standard desktop, the Workbench explicitly supports multitasking.

---

## Responsibilities

The Workbench is responsible for:

- Hosting non-native applications.
- Supporting simultaneous execution of multiple applications.
- Providing a flexible runtime environment.
- Managing application workspaces.

---

## Multitasking

The Workbench is the only location within WandererUI where explicit multitasking is encouraged.

Supported combinations include:

- Multiple native applications.
- Multiple non-native applications.
- A mixture of native and non-native applications.

This allows users to perform complex workflows while keeping the primary desktop focused on single-task interactions.

---

## Design Philosophy

WandererUI promotes focused interaction.

The desktop encourages users to concentrate on a single task at a time.

When multitasking becomes necessary, responsibility shifts to the Workbench, allowing the primary desktop to remain clean, predictable and distraction-free.

## Design Philosophy

WandererUI is designed around focused interaction.

Rather than presenting multiple independent windows, native applications become part of the desktop environment itself.

This creates a consistent user experience while allowing applications to share a common interaction model.