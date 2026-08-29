import frappe
from frappe.tests import IntegrationTestCase

from frappe_box_app.box_identity import sync


class TestBoxIdentitySync(IntegrationTestCase):
	def test_writes_box_name_and_serial_number(self):
		sync(box_name="FrappeBox-9C21", serial_number="SN-042")

		self.assertEqual(frappe.db.get_single_value("Frappe Box Settings", "box_name"), "FrappeBox-9C21")
		self.assertEqual(frappe.db.get_single_value("Frappe Box Settings", "serial_number"), "SN-042")

	def test_overwrites_previous_identity(self):
		sync(box_name="FrappeBox-9C21", serial_number="SN-042")
		sync(box_name="FrappeBox-AA11", serial_number="SN-099")

		self.assertEqual(frappe.db.get_single_value("Frappe Box Settings", "box_name"), "FrappeBox-AA11")
		self.assertEqual(frappe.db.get_single_value("Frappe Box Settings", "serial_number"), "SN-099")
