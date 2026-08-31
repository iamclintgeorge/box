from unittest.mock import patch

import frappe
from frappe.tests import IntegrationTestCase

from frappe_box_app.api import ping


class TestPing(IntegrationTestCase):
	def setUp(self):
		frappe.db.set_single_value("Frappe Box Settings", "box_name", "FrappeBox-4F2A")

	def test_ping_returns_box_status(self):
		with patch.object(frappe, "is_setup_complete", return_value=False):
			response = ping()

		self.assertEqual(
			response,
			{"status": "ok", "box_name": "FrappeBox-4F2A", "provisioning_complete": False},
		)
		self.assertIsInstance(response["provisioning_complete"], bool)

	def test_ping_reports_complete_once_frappes_own_setup_wizard_has(self):
		"""Tracks `frappe.is_setup_complete()` directly, not our own DocType
		flag, so it can't drift out of sync with it."""
		with patch.object(frappe, "is_setup_complete", return_value=True):
			response = ping()

		self.assertTrue(response["provisioning_complete"])

	def test_ping_is_accessible_as_guest(self):
		original_user = frappe.session.user
		frappe.set_user("Guest")
		try:
			response = ping()
		finally:
			frappe.set_user(original_user)
		self.assertEqual(response["status"], "ok")
