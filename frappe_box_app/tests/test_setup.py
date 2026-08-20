import frappe
from frappe.tests import IntegrationTestCase

from frappe_box_app.setup import on_setup_wizard_success


class TestOnSetupWizardSuccess(IntegrationTestCase):
	def setUp(self):
		frappe.db.set_single_value("Frappe Box Settings", "provisioning_complete", 0)
		frappe.db.set_single_value("Frappe Box Settings", "provisioned_on", None)

	def test_marks_provisioning_complete(self):
		on_setup_wizard_success({"full_name": "Clint George"})

		self.assertEqual(frappe.db.get_single_value("Frappe Box Settings", "provisioning_complete"), 1)
		self.assertIsNotNone(frappe.db.get_single_value("Frappe Box Settings", "provisioned_on"))

	def test_is_idempotent(self):
		on_setup_wizard_success({})
		first_provisioned_on = frappe.db.get_single_value("Frappe Box Settings", "provisioned_on")

		on_setup_wizard_success({})

		self.assertEqual(
			frappe.db.get_single_value("Frappe Box Settings", "provisioned_on"), first_provisioned_on
		)
