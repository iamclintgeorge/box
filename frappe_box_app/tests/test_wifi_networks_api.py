import json
from unittest.mock import MagicMock, patch

import frappe
from frappe.tests import IntegrationTestCase

from frappe_box_app.api import add_wifi_network, list_wifi_networks, remove_wifi_network

_CLI_PATH = "/usr/local/bin/frappe-box-wifi-networks"


def _assert_guest_rejected(test_case, fn):
	original_user = frappe.session.user
	frappe.set_user("Guest")
	try:
		with test_case.assertRaises(frappe.PermissionError):
			frappe.is_whitelisted(fn)
	finally:
		frappe.set_user(original_user)


class TestListWifiNetworks(IntegrationTestCase):
	def test_returns_the_daemon_reported_networks(self):
		completed = MagicMock(stdout=json.dumps(["Frappe_Home_5G", "Spam"]))
		with patch("frappe_box_app.wifi_networks.subprocess.run", return_value=completed):
			result = list_wifi_networks()

		self.assertEqual(result, {"networks": ["Frappe_Home_5G", "Spam"]})

	def test_guest_requests_are_rejected(self):
		_assert_guest_rejected(self, list_wifi_networks)


class TestAddWifiNetwork(IntegrationTestCase):
	def test_invokes_the_daemon_cli_with_ssid_and_password(self):
		with patch("frappe_box_app.wifi_networks.subprocess.run") as mock_run:
			result = add_wifi_network("Frappe_Home_5G", "letmein123")

		self.assertEqual(result, {"status": "ok"})
		mock_run.assert_called_once_with(
			["sudo", "-n", _CLI_PATH, "add", "Frappe_Home_5G", "letmein123"],
			check=True,
			capture_output=True,
			text=True,
		)

	def test_guest_requests_are_rejected(self):
		_assert_guest_rejected(self, add_wifi_network)


class TestRemoveWifiNetwork(IntegrationTestCase):
	def test_invokes_the_daemon_cli_with_ssid(self):
		with patch("frappe_box_app.wifi_networks.subprocess.run") as mock_run:
			result = remove_wifi_network("Frappe_Home_5G")

		self.assertEqual(result, {"status": "ok"})
		mock_run.assert_called_once_with(
			["sudo", "-n", _CLI_PATH, "remove", "Frappe_Home_5G"],
			check=True,
			capture_output=True,
			text=True,
		)

	def test_guest_requests_are_rejected(self):
		_assert_guest_rejected(self, remove_wifi_network)
