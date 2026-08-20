import frappe
from frappe.utils.synchronization import filelock


def on_setup_wizard_success(args: dict) -> None:
	"""Marks the box provisioned once Frappe's own setup wizard completes.

	Guarded by its own filelock (the same mechanism, under a different name,
	that `setup_wizard.setup_complete` already holds around this hook's
	caller) so a second concurrent call — e.g. a retried webhook — waits,
	then sees `provisioning_complete` already set and returns, instead of
	also writing `provisioned_on`.
	"""
	with filelock("frappe_box_provisioning_complete", timeout=5):
		if frappe.db.get_single_value("Frappe Box Settings", "provisioning_complete"):
			return

		frappe.db.set_single_value("Frappe Box Settings", "provisioning_complete", 1)
		frappe.db.set_single_value("Frappe Box Settings", "provisioned_on", frappe.utils.now())
