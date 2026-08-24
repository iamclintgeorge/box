import frappe

from frappe_box_app import api_keys, wifi_networks
from frappe_box_app import system_stats as system_stats_module


@frappe.whitelist(allow_guest=True, methods=["GET"])
def ping():
	"""Confirms the box is reachable on the LAN, before an admin user exists."""
	return {
		"status": "ok",
		"box_name": frappe.db.get_single_value("Frappe Box Settings", "box_name"),
		"provisioning_complete": frappe.db.get_single_value("Frappe Box Settings", "provisioning_complete"),
	}


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
