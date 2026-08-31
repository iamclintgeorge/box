import frappe
from frappe.tests import IntegrationTestCase

from frappe_box_app.api import ping


class TestPing(IntegrationTestCase):
	def setUp(self):
		frappe.db.set_single_value("Frappe Box Settings", "box_name", "FrappeBox-4F2A")
		frappe.db.set_single_value("Frappe Box Settings", "provisioning_complete", 0)

	def test_ping_returns_box_status(self):
		response = ping()
		self.assertEqual(
			response,
			{"status": "ok", "box_name": "FrappeBox-4F2A", "provisioning_complete": False},
		)
		self.assertIsInstance(response["provisioning_complete"], bool)

	def test_ping_is_accessible_as_guest(self):
		original_user = frappe.session.user
		frappe.set_user("Guest")
		try:
			response = ping()
		finally:
			frappe.set_user(original_user)
		self.assertEqual(response["status"], "ok")
