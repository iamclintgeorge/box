"""Proxies saved-WiFi-network management to the box daemon's local command
surface (`box-scripts/bin/frappe-box-wifi-networks`), reached via a narrowly
scoped sudoers rule since the daemon's config lives outside what the Frappe
worker's own OS user can write.
"""

from __future__ import annotations

import json
import subprocess

_CLI_PATH = "/usr/local/bin/frappe-box-wifi-networks"


def list_networks() -> list[str]:
	result = _run("list")
	return json.loads(result.stdout)


def add_network(ssid: str, password: str) -> None:
	_run("add", ssid, password)


def remove_network(ssid: str) -> None:
	_run("remove", ssid)


def _run(*args: str) -> subprocess.CompletedProcess:
	return subprocess.run(
		["sudo", "-n", _CLI_PATH, *args],
		check=True,
		capture_output=True,
		text=True,
	)
