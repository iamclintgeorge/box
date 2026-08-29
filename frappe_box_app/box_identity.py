"""Writes this box's hardware identity into Frappe Box Settings.

Sourced from the BLE daemon's own hardware read (box-scripts' identity.py)
and passed in at pairing time (see api.pair) — this backend has no reason to
independently shell out to /sys/class/dmi/id/product_serial itself.
"""

from __future__ import annotations

import frappe


def sync(box_name: str, serial_number: str) -> None:
	frappe.db.set_single_value("Frappe Box Settings", "box_name", box_name)
	frappe.db.set_single_value("Frappe Box Settings", "serial_number", serial_number)
