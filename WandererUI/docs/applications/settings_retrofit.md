# Settings Retrofit Plan
## WandererUI Core Application Integration

**Status:** In Progress

---

# Objective

Transform the standalone Settings Linux application into a WandererUI Core Application while preserving its business logic.

Core Rule:

> Business logic is never rewritten during retrofit.
> WandererUI adapts to the application—not the other way around.

---

# Phase 1 — Runtime Integration

**Goal**

Replace standalone providers with WandererUI services.

## Tasks

- [ ] Replace ThemeProvider with Maaya
- [ ] Replace WallpaperProvider with Maaya
- [ ] Replace FontProvider with Maaya
- [ ] Replace SystemInfoProvider with Wanderer runtime utilities
- [ ] Verify no business logic changes were required

**Status**

Complete!!!

---

# Phase 2 — Presentation Integration

**Goal**

Replace the standalone shell with the Wanderer Desktop.

## Tasks

- [ ] Remove standalone Sidebar
- [ ] Remove standalone StatusBar
- [ ] Map Categories → Navigation Panel
- [ ] Map Pages → Viewport
- [ ] Map Metadata → Context Panel
- [ ] Map Status Hints → Footer
- [ ] Verify page logic remains unchanged

**Status**

⬜ Not Started

---

# Phase 3 — Lifecycle Integration

**Goal**

Integrate the application into the Wanderer runtime.

## Tasks

- [ ] Register Settings as a Core Application
- [ ] Integrate launch lifecycle with Animus
- [ ] Restore Desktop when application exits
- [ ] Prepare hook for future Layout Profiles

**Status**

⬜ Not Started

---

# Phase 4 — Persistence Integration

**Goal**

Persist user settings using Eidolon.

## Tasks

- [ ] Load saved theme
- [ ] Load saved wallpaper
- [ ] Load saved font
- [ ] Save presentation changes
- [ ] Restore session on startup

**Status**

⬜ Not Started

---

# Phase 5 — Polish

**Goal**

Bring the application to release quality.

## Tasks

- [ ] Keyboard navigation audit
- [ ] Mouse support audit
- [ ] Visual consistency audit
- [ ] Error handling
- [ ] Performance review
- [ ] Documentation review

**Status**

⬜ Not Started

---

# Completion Criteria

Settings is considered complete when:

- [ ] All retrofit phases are complete.
- [ ] Business logic remained untouched.
- [ ] The application runs entirely inside WandererUI.
- [ ] All functionality matches the standalone application.
- [ ] No critical bugs remain.

---

# Lessons Learned

(Engineering notes written during development.)

---

# Future Improvements

- Dynamic Layout Profiles
- Wallpaper Crop Tool
- Audio Settings
- Animation Settings
- Theme Editor
- Font Manager