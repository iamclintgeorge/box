"""Box identity + network info for the Desk settings page."""

from __future__ import annotations

import socket


def collect() -> dict:
	return {"ip_address": _ip_address()}


def _ip_address() -> str:
	"""The box's LAN IP — what the settings page shows for SSH access.

	A UDP "connect" never actually sends a packet; the kernel just picks
	the interface it would route through, which resolves correctly even
	on the box's internet-less LAN.
	"""
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		sock.connect(("10.255.255.255", 1))
		return sock.getsockname()[0]
	except OSError:
		return "127.0.0.1"
	finally:
		sock.close()
