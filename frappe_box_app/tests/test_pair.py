import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils.password import update_password

from frappe_box_app.api import pair

_TEST_PASSWORD = "correct-horse-battery-staple"


class TestPair(IntegrationTestCase):
	def setUp(self):
		update_password("Administrator", _TEST_PASSWORD)
		frappe.db.set_single_value("Frappe Box Settings", "box_name", None)
		frappe.db.set_single_value("Frappe Box Settings", "serial_number", None)

	def test_correct_password_returns_key_and_syncs_identity(self):
		result = pair(_TEST_PASSWORD, box_name="FrappeBox-4F2A", serial_number="SN-001")

		self.assertTrue(result["api_key"])
		self.assertTrue(result["api_secret"])
		self.assertEqual(result["box_name"], "FrappeBox-4F2A")
		self.assertEqual(result["serial_number"], "SN-001")
		self.assertEqual(frappe.db.get_single_value("Frappe Box Settings", "box_name"), "FrappeBox-4F2A")
		self.assertEqual(frappe.db.get_single_value("Frappe Box Settings", "serial_number"), "SN-001")

	def test_reuses_existing_key_pair(self):
		first = pair(_TEST_PASSWORD, box_name="FrappeBox-4F2A", serial_number="SN-001")
		second = pair(_TEST_PASSWORD, box_name="FrappeBox-4F2A", serial_number="SN-001")

		self.assertEqual(first["api_key"], second["api_key"])
		self.assertEqual(first["api_secret"], second["api_secret"])

	def test_wrong_password_is_rejected_and_identity_is_not_synced(self):
		with self.assertRaises(frappe.AuthenticationError):
			pair("not-the-password", box_name="FrappeBox-4F2A", serial_number="SN-001")

		self.assertFalse(frappe.db.get_single_value("Frappe Box Settings", "box_name"))
