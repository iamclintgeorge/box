import frappe
from frappe.tests import IntegrationTestCase

from frappe_box_app.api import box_info, system_stats


def _assert_guest_rejected(test_case, fn):
	original_user = frappe.session.user
	frappe.set_user("Guest")
	try:
		with test_case.assertRaises(frappe.PermissionError):
			frappe.is_whitelisted(fn)
	finally:
		frappe.set_user(original_user)


class TestSystemStats(IntegrationTestCase):
	def test_returns_cpu_memory_and_storage_usage(self):
		stats = system_stats()

		self.assertIn("cpu_temperature_celsius", stats)
		self.assertGreater(stats["memory"]["total_bytes"], 0)
		self.assertGreater(stats["storage"]["total_bytes"], 0)

	def test_guest_requests_are_rejected(self):
		_assert_guest_rejected(self, system_stats)


class TestBoxInfo(IntegrationTestCase):
	def setUp(self):
		frappe.db.set_single_value("Frappe Box Settings", "box_name", "FrappeBox-4F2A")
		frappe.db.set_single_value("Frappe Box Settings", "serial_number", "SN-001")

	def test_returns_identity_and_ip_address(self):
		info = box_info()

		self.assertEqual(info["box_name"], "FrappeBox-4F2A")
		self.assertEqual(info["serial_number"], "SN-001")
		self.assertTrue(info["ip_address"])

	def test_provisioning_complete_is_a_bool(self):
		frappe.db.set_single_value("Frappe Box Settings", "provisioning_complete", 1)

		info = box_info()

		self.assertIsInstance(info["provisioning_complete"], bool)
		self.assertTrue(info["provisioning_complete"])

	def test_guest_requests_are_rejected(self):
		_assert_guest_rejected(self, box_info)
