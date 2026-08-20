import frappe


def on_setup_wizard_success(args: dict) -> None:
	"""Marks the box provisioned once Frappe's own setup wizard completes."""
	if frappe.db.get_single_value("Frappe Box Settings", "provisioning_complete"):
		return

	frappe.db.set_single_value("Frappe Box Settings", "provisioning_complete", 1)
	frappe.db.set_single_value("Frappe Box Settings", "provisioned_on", frappe.utils.now())
