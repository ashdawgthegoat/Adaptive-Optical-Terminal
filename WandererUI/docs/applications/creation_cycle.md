# WandererUI Application Development Pipeline

## Philosophy

WandererUI applications are developed in stages.

Applications should be good software before they become Wanderer-native software.

The architecture should adapt the application, not constrain its design.

---

# Stage 1 — Design

Define:

- Purpose
- Functional requirements
- Keyboard workflow
- Information architecture

No implementation.

---

# Stage 2 — Standalone Development

Build the application as a normal PyQt6 application.

Goals:

- Clean architecture
- SOLID principles
- Keyboard-first interaction
- Low memory usage
- Good user experience

The application should function completely on its own.

Do NOT introduce Wanderer-specific code.

---

# Stage 3 — Standalone Testing

Test repeatedly.

Focus on:

- usability
- keyboard flow
- stability
- responsiveness
- correctness

Refactor until the application feels complete.

---

# Stage 4 — Wanderer Retrofit

Only after the standalone application is mature.

Map the existing UI onto the Desktop.

Navigation
- Lists
- Menus
- Selection

Viewport
- Primary content

Context
- Metadata
- Information
- Secondary controls

Footer
- Status
- Shortcuts
- Feedback

Do not rewrite business logic.

Replace only the presentation layer.

---

# Stage 5 — Integration

Integrate with:

- Animus
- Kaizen
- Maaya

Add:

- .desktop file
- X-Wanderer-Native metadata
- Application lifecycle hooks

The application should now function as a Wanderer Core Application.

---

# Stage 6 — Polish

Verify:

- Keyboard navigation
- Theme compatibility
- Wallpaper compatibility
- Memory usage
- Startup time
- Shutdown behaviour

Only after successful testing should the application become part of an official release.

---

## Engineering Principles

- Build applications before integrations.
- Never redesign the Desktop to accommodate an application.
- Business logic must remain independent from Wanderer-specific UI.
- Wanderer panels are presentation surfaces, not application logic.
- One architectural change per commit.
- Small, testable milestones over large refactors.

---

## Current Core Applications

- Settings
- Archive (File Manager)

These applications define the reference architecture for future Wanderer applications.