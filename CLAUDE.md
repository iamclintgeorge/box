## About

Frappe Box (Version 0.1), is a provisioning app for Frappe Box Device

## IMPORTANT

Always load frappe-app-dev and frappe-ui skills before any implementation

## Implementation

Guidelines for writing good code for a developer:

1. Choose clean code over clever code.
2. Write object oriented code as much as possible.
3. Keep function sizes small, ideally 10 lines.
4. Try and keep files between 100 and 300 lines.
5. Don't keep too many files in a folder or module. Try and keep it under 15.
6. Avoid abbreviations.
7. Use standard API as much as possible.
8. Reuse. Write as little code as possible.
9. Use Frappe UI, espresso design system for UI styling.
10. Always write tests, and make sure they work.
11. Build the minimum working app, then iterate towards your goals.
12. Keep the verbosity less in new changes (inline comments, docstrings erc).
    Explain only what's absolutely needed in inline comments.
    Actual changes explanation can be part of commit message.


## Development Details

Unless mentioned, the site is site2.localhost with clint@frappe.io/Admin@123 credentials.

## Planning / Spec-ing

Use Tracer bullets comes from the Pragmatic Programmer. When building systems, you want to write code that gets you feedback as quickly as possible. Tracer bullets are small slices of functionality that go through all layers of the system, allowing you to test and validate your approach early. This helps in identifying potential issues and ensures that the overall architecture is sound before investing significant time in development.

Create specs in specs/. Maintain a PROGRESS.md file to track progress of implementation phases.

## Implementation Guidelines

* Create a new branch before working on a new feature/spec (branch name patterns: feat/, fix/, just like conventional commit pre-fixes)
* Reconcile the spec and log the progress after each phase of development
* Commit after each meaningful phase
* Commit the spec before the development commits
* Use comments only when necessary to explain "why?" not "how?", how must be clear from the code itself

## Frontend / Backend Sync

* Whenever a new field is added to a backend DocType that is surfaced in the frontend (e.g. settings panels), it must also be handled in the corresponding frontend component so the two stay in sync. This is a convention/reminder only — there is no automatic syncing mechanism; the frontend enumerates fields explicitly.

## Regression tests

* When we fix a bug, add at the very least a Unit test, and verify before/after by temp revert of fix to make sure the test tests what is intended
* For bigger features/workflows, e2e playwright tests are a must.

Use agent-browser for quick manual e2e checks.
