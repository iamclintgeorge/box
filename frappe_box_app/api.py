import frappe
from frappe.utils.password import check_password

from frappe_box_app import api_keys, box_identity, wifi_networks
from frappe_box_app import box_info as box_info_module
from frappe_box_app import system_stats as system_stats_module


@frappe.whitelist(allow_guest=True, methods=["GET"])
def ping():
	"""Confirms the box is reachable on the LAN, before an admin user exists."""
	return {
		"status": "ok",
		"box_name": frappe.db.get_single_value("Frappe Box Settings", "box_name"),
		"provisioning_complete": frappe.db.get_single_value("Frappe Box Settings", "provisioning_complete"),
	}


@frappe.whitelist(allow_guest=True, methods=["POST"])
def pair(password: str, box_name: str, serial_number: str):
	"""The BLE pairing exchange (Phase 9): the daemon calls this over
	loopback only (see box-scripts' nginx config, which denies this path to
	anything but 127.0.0.1) once the phone has written its claimed password
	over a bonded BLE link and the daemon has read back its own hardware
	identity.

	`allow_guest=True` because no session exists yet at this point in the
	flow; the real gate is `check_password`, which raises
	`frappe.AuthenticationError` on a wrong password.
	"""
	check_password("Administrator", password)
	box_identity.sync(box_name, serial_number)
	return {**api_keys.get_or_create("Administrator"), "box_name": box_name, "serial_number": serial_number}


@frappe.whitelist()
def get_api_key():
	"""Issues (or reuses) the calling user's API key pair for Phase 6 sign-in."""
	return api_keys.get_or_create(frappe.session.user)


@frappe.whitelist()
def system_stats():
	"""CPU temperature, memory, and storage usage for the dashboard."""
	return system_stats_module.collect()


@frappe.whitelist()
def list_wifi_networks():
	return {"networks": wifi_networks.list_networks()}


@frappe.whitelist()
def add_wifi_network(ssid: str, password: str):
	wifi_networks.add_network(ssid, password)
	return {"status": "ok"}


@frappe.whitelist()
def remove_wifi_network(ssid: str):
	wifi_networks.remove_network(ssid)
	return {"status": "ok"}


@frappe.whitelist()
def box_info():
	"""Box identity, network, and provisioning info for the Desk settings page."""
	settings = frappe.get_single("Frappe Box Settings")
	return {
		"box_name": settings.box_name,
		"serial_number": settings.serial_number,
		"provisioning_complete": settings.provisioning_complete,
		"provisioned_on": settings.provisioned_on,
		**box_info_module.collect(),
	}
