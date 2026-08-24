"""Reads the box's own health for the Flutter app's dashboard (Phase 6)."""

from __future__ import annotations

import shutil

_THERMAL_ZONE_PATH = "/sys/class/thermal/thermal_zone0/temp"
_MEMINFO_PATH = "/proc/meminfo"


def collect() -> dict:
	return {
		"cpu_temperature_celsius": _cpu_temperature_celsius(),
		"memory": _memory_usage(),
		"storage": _storage_usage(),
	}


def _cpu_temperature_celsius() -> float | None:
	try:
		with open(_THERMAL_ZONE_PATH, encoding="utf-8") as temp_file:
			return int(temp_file.read().strip()) / 1000
	except OSError:
		return None


def _memory_usage() -> dict:
	totals = _read_meminfo_totals()
	total = totals.get("MemTotal", 0)
	available = totals.get("MemAvailable", 0)
	return {"used_bytes": total - available, "total_bytes": total}


def _read_meminfo_totals() -> dict[str, int]:
	values = {}
	with open(_MEMINFO_PATH, encoding="utf-8") as meminfo_file:
		for line in meminfo_file:
			key, _, rest = line.partition(":")
			if key in ("MemTotal", "MemAvailable"):
				values[key] = int(rest.strip().split()[0]) * 1024
	return values


def _storage_usage() -> dict:
	usage = shutil.disk_usage("/")
	return {"used_bytes": usage.used, "total_bytes": usage.total}
