# Frappe Box Backend — Provisioning API Contract

Backend half of the Flutter provisioning app's spec (see the Flutter app's `specs/plan.md`, phases 3–4). This app ships pre-installed on the box's site but unconfigured; these APIs are what the phone calls once the box is reachable on the LAN.

## DocType: `Frappe Box Settings` (Single)

Sync point between the device daemon (`box-scripts`), this backend, and the Flutter app — per the project convention that any field surfaced in the frontend must be kept in sync here explicitly.

| Field | Type | Notes |
|---|---|---|
| `box_name` | Data | e.g. `FrappeBox-4F2A`, matches the BLE advertised name |
| `serial_number` | Data | |
| `provisioning_complete` | Check | Flips to 1 exactly once, by `complete_setup` |
| `provisioned_on` | Datetime | Set when `provisioning_complete` flips |
| `claim_token` | Data | Written locally by the device daemon after a successful WiFi join; consumed and never re-usable once `complete_setup` succeeds |

## API: `frappe_box_app.api.ping`

- `allow_guest=True` (no admin user exists yet at this point in the flow).
- No arguments.
- Returns `{status: "ok", box_name, provisioning_complete}`.
- Used by the Flutter app (Phase 3) purely to confirm the box is reachable over mDNS/LAN and to decide, on relaunch, whether to skip straight to the "box ready" screen (Phase 5).

## API: `frappe_box_app.api.complete_setup`

- `allow_guest=True`.
- Args: `full_name`, `email`, `password`, `claim_token`.
- Guards, in order:
  1. Reject if `Frappe Box Settings.provisioning_complete` is already `1` (one-shot).
  2. Reject if `claim_token` doesn't match the stored value (ties account creation to BLE/physical possession of the box, not merely WiFi presence).
- On success: creates/configures the admin user with the given details, sets `provisioning_complete = 1` and `provisioned_on = now`, returns an API key/secret for the app to store.
- Test explicitly for both guards (concurrent/duplicate calls, wrong token) — this is exactly the kind of logic CLAUDE.md's regression-test convention exists for: write the test, temporarily revert the guard, confirm the test fails, restore the guard, confirm it passes.
