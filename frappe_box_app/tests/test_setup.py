import threading

import frappe
from frappe.tests import IntegrationTestCase

from frappe_box_app.setup import on_setup_wizard_success


class TestOnSetupWizardSuccess(IntegrationTestCase):
	def setUp(self):
		frappe.db.set_single_value("Frappe Box Settings", "provisioning_complete", 0)
		frappe.db.set_single_value("Frappe Box Settings", "provisioned_on", None)
		frappe.db.commit()

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

	def test_concurrent_calls_resolve_to_exactly_one_success(self):
		"""Simulates two `setup_wizard_success` calls racing on separate DB
		connections (e.g. a retried webhook) to confirm the filelock in
		`on_setup_wizard_success` serializes them instead of both winning."""
		site = frappe.local.site
		sites_path = frappe.local.sites_path
		ready = threading.Barrier(2, timeout=5)
		provisioned_on_values = []
		results_lock = threading.Lock()

		def call_from_new_connection():
			frappe.init(site=site, sites_path=sites_path)
			frappe.connect()
			try:
				ready.wait()
				on_setup_wizard_success({})
				frappe.db.commit()
				with results_lock:
					provisioned_on_values.append(
						frappe.db.get_single_value("Frappe Box Settings", "provisioned_on", cache=False)
					)
			finally:
				frappe.destroy()

		threads = [threading.Thread(target=call_from_new_connection) for _ in range(2)]
		for thread in threads:
			thread.start()
		for thread in threads:
			thread.join(timeout=10)

		self.assertEqual(
			frappe.db.get_single_value("Frappe Box Settings", "provisioning_complete", cache=False), 1
		)
		self.assertEqual(len(provisioned_on_values), 2)
		self.assertEqual(len(set(provisioned_on_values)), 1)
