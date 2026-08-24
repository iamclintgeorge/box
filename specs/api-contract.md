# Frappe Box Backend — Provisioning API Contract

Backend half of the Flutter provisioning app's spec (see the Flutter app's `specs/plan.md`, phases 3–7). This app ships pre-installed on the box's site but unconfigured; these APIs are what the phone calls once the box is reachable on the LAN.

## DocType: `Frappe Box Settings` (Single)

Sync point between the device daemon (`box-scripts`), this backend, and the Flutter app — per the project convention that any field surfaced in the frontend must be kept in sync here explicitly.

| Field | Type | Notes |
|---|---|---|
| `box_name` | Data | e.g. `FrappeBox-4F2A`, matches the BLE advertised name |
| `serial_number` | Data | |
| `provisioning_complete` | Check | Flips to 1 exactly once, by the `setup_wizard_success` hook |
| `provisioned_on` | Datetime | Set when `provisioning_complete` flips |
| `claim_token` | Data | Written locally by the device daemon after a successful WiFi join. Currently unused by any API — see the Flutter spec's Phase 4 note on why account creation is no longer gated by it |

## API: `frappe_box_app.api.ping`

- `allow_guest=True` (no admin user exists yet at this point in the flow).
- No arguments.
- Returns `{status: "ok", box_name, provisioning_complete}`.
- Used by the Flutter app (Phase 3) purely to confirm the box is reachable over mDNS/LAN and to decide, on relaunch, whether to skip straight to the "box ready" screen (Phase 5) or, from Phase 6, straight to the dashboard.

## Hook: `setup_wizard_success` → `frappe_box_app.setup.on_setup_wizard_success`

Replaces the originally-planned `complete_setup` API (Phase 4 revision — see the Flutter spec). Frappe's own setup wizard already handles admin account creation on a fresh site; this app doesn't need its own. Frappe calls every function registered under the `setup_wizard_success` hook with the wizard's `args` once it completes successfully.

- Sets `Frappe Box Settings.provisioning_complete = 1` and `provisioned_on = now`.
- Idempotent: safe to call more than once (re-checked in Phase 5).

## API: `frappe_box_app.api.get_api_key`

- Authenticated (`@frappe.whitelist()`, no `allow_guest`).
- No arguments.
- Returns `{api_key, api_secret}` for `frappe.session.user`. Idempotent: reuses the existing key/secret if already set (`api_keys.get_or_create`), so re-signing in doesn't invalidate a previously issued pair. Sets `User.api_key`/`api_secret` directly via `frappe.db.set_value`/`set_encrypted_password` rather than loading and saving the whole `User` document, to avoid unrelated save side effects (global search indexing, etc.) on every sign-in.

## API: `frappe_box_app.api.system_stats`

- Authenticated.
- No arguments.
- Returns `{cpu_temperature_celsius, memory: {used_bytes, total_bytes}, storage: {used_bytes, total_bytes}}`, read from `/sys/class/thermal/thermal_zone0/temp`, `/proc/meminfo`, and `shutil.disk_usage("/")` (`system_stats.py`). `cpu_temperature_celsius` is `null` when no thermal zone is available (e.g. in a dev container).

## APIs: `frappe_box_app.api.list_wifi_networks` / `add_wifi_network(ssid, password)` / `remove_wifi_network(ssid)`

- Authenticated.
- Proxy to the box daemon's local command surface (`box-scripts/bin/frappe-box-wifi-networks`, see that repo's Phase 7 notes) over `sudo -n <path> <command> [args]` — the Frappe worker's OS user is granted exactly that one command via a sudoers rule (`box-scripts/config/sudoers.d/frappe-box-wifi`), since writing `wpa_supplicant.conf` and reloading it needs root (`wifi_networks.py`).
- `list_wifi_networks()` returns `{networks: [ssid, ...]}`; `add_wifi_network`/`remove_wifi_network` return `{status: "ok"}`.
