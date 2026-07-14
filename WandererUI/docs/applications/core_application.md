# Core Applications

## Overview

Core Applications are applications designed specifically for WandererUI.

Unlike traditional Linux applications, Core Applications do not own their
entire user interface. Instead, they borrow parts of the Desktop and provide
only their application logic.

This allows every Core Application to feel like a natural extension of
WandererUI while remaining modular.

---

# Categories

There are two categories of Core Applications.

## Desktop Core

Desktop Core applications exist only inside WandererUI.

Examples:

- Settings
- Modules
- Future System Monitor

Desktop Core applications do not create their own windows.

Instead, they occupy the Desktop itself.

They make use of:

- Navigation Panel
- Context Panel
- Viewport
- Footer
- Overlay

The Header always remains owned by the Desktop.

---

## Hybrid Core

Hybrid Core applications can operate in two environments.

Examples:

- Archive
- Music
- Astronomy
- Terminal

Inside WandererUI they borrow the Desktop just like Desktop Core
applications.

Outside WandererUI they launch inside a traditional application window.

This allows them to behave as normal Linux applications while still providing
a native WandererUI experience.

---

# Desktop Ownership

The Desktop always owns the following components.

- Header
- Navigation Panel
- Context Panel
- Viewport
- Footer
- Overlay

Core Applications never create replacements for these components.

Instead, they provide data that the Desktop renders.

---

# Core Application Responsibilities

A Core Application is responsible for:

- Application state
- Navigation structure
- Business logic
- Preview generation
- Context generation
- Footer hints

A Core Application is NOT responsible for:

- Window management
- Runtime selection
- Focus management between Desktop panels
- Rendering Desktop widgets

---

# Runtime Selection

Runtime selection is performed by Animus.

Applications declare their preferred runtime through metadata.

Desktop Core applications use:

X-Wanderer-Runtime=desktop

Hybrid Core applications may support both:

desktop
workbench

The application itself does not decide where it runs.

---

# Interaction Model

Navigation Panel

↓

Select category

↓

Context Panel

↓

Modify current setting

↓

Viewport

↓

Live preview

↓

Overlay

↓

Selection dialogs when required

---

# Overlay

The Overlay is a shared Desktop component.

It is used whenever an application requires temporary item selection.

Examples:

- Theme picker
- Wallpaper picker
- Font picker
- Wi-Fi networks
- Bluetooth devices
- File selection
- Module selection

Core Applications never create their own picker dialogs.

---

# Design Philosophy

Core Applications should feel like part of the Desktop rather than separate
windows.

The Desktop provides the shell.

The application provides the experience.

This separation keeps the architecture modular while giving WandererUI a
consistent interaction model across every Core Application.

# Future Direction

A Core Application should expose a stable interface to the Desktop.

The Desktop asks the application what should be displayed.

The application never directly manipulates Desktop widgets.

This contract will be finalized during the Settings retrofit and reused by all
future Core Applications.