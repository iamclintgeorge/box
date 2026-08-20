import frappe


@frappe.whitelist(allow_guest=True, methods=["GET"])
def ping():
	"""Confirms the box is reachable on the LAN, before an admin user exists."""
	return {
		"status": "ok",
		"box_name": frappe.db.get_single_value("Frappe Box Settings", "box_name"),
		"provisioning_complete": frappe.db.get_single_value("Frappe Box Settings", "provisioning_complete"),
	}
