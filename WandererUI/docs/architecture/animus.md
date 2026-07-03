# Animus

## Purpose

`Animus` is WandererUI's application management service.

It is responsible for managing the lifecycle of applications, workbenches and external modules.

Animus acts as the central coordinator for everything that can be launched, closed or connected to the desktop environment.

---

## Responsibilities

Animus is responsible for:

- Registering applications.
- Launching and closing applications.
- Tracking running applications.
- Tracking the currently active application.
- Managing workbenches.
- Managing external modules.
- Emitting lifecycle events.

Animus intentionally **does not** render user interfaces or manage navigation.

---

## Application Lifecycle

Applications must be registered with Animus before they can be launched.

Once launched, Animus:

- Marks the application as running.
- Tracks the active application.
- Emits an application launch event.

Closing an application removes it from the running application list and emits the corresponding lifecycle event.

---

## Workbench Management

Animus manages multiple workbenches.

Each workbench owns its own collection of running applications.

Animus is responsible for:

- Creating workbenches.
- Closing workbenches.
- Switching between workbenches.

---

## Module Management

External modules may register themselves with Animus.

Modules are treated independently from applications and have their own lifecycle.

This allows WandererUI to support expandable functionality without modifying the core desktop environment.

---

## Public Interface

### Applications

- `register_application()`
- `discover_applications()`
- `launch()`
- `close()`
- `is_running()`
- `list_applications()`

### Workbenches

- `create_workbench()`
- `close_workbench()`
- `switch_workbench()`
- `list_workbenches()`

### Modules

- `register_module()`
- `unregister_module()`
- `list_modules()`

### Signals

Applications

- `app_launched`
- `app_closed`

Workbenches

- `workbench_created`
- `workbench_closed`
- `workbench_switched`

Modules

- `module_connected`
- `module_disconnected`

---

## Interactions

Animus interacts with the following WandererUI components.

### Native Applications

Applications register themselves with Animus before they can be launched.

---

### Runtime Widget

The Runtime Widget displays information derived from Animus, such as the currently active application and the number of running applications.

Animus remains the source of truth.

---

### Workbench

Workbench relies on Animus to manage application sessions and workbench state.

---

### Eidolon *(Future)*

Eidolon will restore previous sessions by interacting with Animus rather than launching applications directly.

---

## Design Philosophy

Animus separates **application lifecycle** from **application behaviour**.

Applications decide what they do.

Animus decides whether they exist.

This separation allows the desktop environment to coordinate applications without becoming coupled to their internal implementation.

---

## Future Work

Potential future improvements include:

- Automatic application discovery.
- Session persistence.
- Background services.
- Multi-workbench application migration.
- Application permissions.
- Process monitoring.