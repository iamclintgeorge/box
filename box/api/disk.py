import frappe
import subprocess
import json
from frappe import _


@frappe.whitelist()
def scan_disks():
    """
    Runs lsblk and returns parsed disk info.
    Called by the Vue SPA during the SSD scan step.
    """
    # Security: only System Manager can trigger shell commands
    frappe.only_for("System Manager")

    try:
        result = subprocess.run(
            ["lsblk", "-J", "-o", "NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE,MODEL,SERIAL,ROTA"],
            capture_output=True,
            text=True,
            timeout=15
        )

        if result.returncode != 0:
            frappe.throw(_(f"lsblk failed: {result.stderr}"))

        raw = json.loads(result.stdout)
        # Filter to only physical disks (type == "disk"), exclude loop/rom
        disks = [
            d for d in raw.get("blockdevices", [])
            if d.get("type") == "disk"
        ]

        return {"disks": disks, "raw": result.stdout}

    except subprocess.TimeoutExpired:
        frappe.throw(_("Disk scan timed out."))
    except FileNotFoundError:
        frappe.throw(_("`lsblk` not found. Is this a Linux system?"))
    except json.JSONDecodeError:
        frappe.throw(_("Could not parse lsblk output."))


@frappe.whitelist()
def configure_zfs(pool_name: str, raid_level: str, devices: str):
    """
    Creates a ZFS pool with the given configuration.
    `devices` is a JSON-encoded list of device paths e.g. '["/dev/sdb", "/dev/sdc"]'
    """
    frappe.only_for("System Manager")

    if isinstance(devices, str):
        devices = json.loads(devices)

    # Validate inputs
    if not pool_name or not pool_name.isidentifier():
        frappe.throw(_("Invalid pool name. Use only letters, numbers, underscores."))

    if not devices or len(devices) < 1:
        frappe.throw(_("At least one device is required."))

    # Map UI label to zpool vdev keyword
    raid_map = {
        "RAID 0": "",          # stripe (no keyword)
        "RAID 1": "mirror",
        "RAID Z1": "raidz",
        "RAID Z2": "raidz2",
        "RAID Z3": "raidz3",
    }

    vdev_type = raid_map.get(raid_level, "mirror")

    # Build the zpool create command
    cmd = ["zpool", "create", pool_name]
    if vdev_type:
        cmd.append(vdev_type)
    cmd.extend(devices)

    frappe.logger().info(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            frappe.throw(_(f"ZFS pool creation failed: {result.stderr}"))

        # Persist config to system_config
        config = frappe.get_single("System Config")
        config.zfs_pool_name = pool_name
        config.raid_level = raid_level
        config.selected_disks = json.dumps(devices)
        config.save(ignore_permissions=True)
        frappe.db.commit()

        return {"success": True, "pool_name": pool_name, "stdout": result.stdout}

    except subprocess.TimeoutExpired:
        frappe.throw(_("ZFS pool creation timed out."))


@frappe.whitelist()
def get_zfs_status():
    """Returns current zpool status"""
    frappe.only_for("System Manager")

    try:
        result = subprocess.run(
            ["zpool", "status", "-v"],
            capture_output=True, text=True, timeout=10
        )
        return {"output": result.stdout, "returncode": result.returncode}
    except FileNotFoundError:
        return {"output": "ZFS not available on this system.", "returncode": 1}
