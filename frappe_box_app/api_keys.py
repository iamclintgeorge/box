"""Issues the API key pair the Flutter app authenticates with from Phase 6 on."""

from __future__ import annotations

import frappe
from frappe.utils.password import get_decrypted_password, set_encrypted_password


def get_or_create(user: str) -> dict:
	"""Returns [user]'s API key pair, generating one on first call.

	Idempotent: reuses both the key and the secret if already set, so a
	repeated call (e.g. re-pairing over BLE) doesn't invalidate a
	previously issued pair. Sets the two fields directly rather than
	loading and saving the full User document, to avoid unrelated save
	side effects (global search indexing, notification sync, ...).
	"""
	api_key = frappe.db.get_value("User", user, "api_key")
	if not api_key:
		api_key = frappe.generate_hash(length=15)
		frappe.db.set_value("User", user, "api_key", api_key)

	api_secret = get_decrypted_password("User", user, "api_secret", raise_exception=False)
	if not api_secret:
		api_secret = frappe.generate_hash(length=15)
		set_encrypted_password("User", user, api_secret, fieldname="api_secret")

	return {"api_key": api_key, "api_secret": api_secret}
