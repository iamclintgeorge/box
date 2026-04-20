import frappe
from frappe import _
from frappe.utils import now


@frappe.whitelist(allow_guest=True)
def get_setup_status():
    """
    Called FIRST by the Vue SPA to decide whether to show onboarding.
    allow_guest=True because the user isn't logged in yet on first visit.

    Returns: { "first_time": 1 or 0 }
    """
    config = frappe.get_single("System Config")
    return {
        "first_time": config.first_time,
        "site_name": frappe.local.site
    }


@frappe.whitelist()
def complete_setup():
    """
    Called after the user finishes all onboarding steps.
    Sets first_time = 0 so subsequent visits skip onboarding.
    """
    frappe.only_for("System Manager")

    config = frappe.get_single("System Config")
    config.first_time = 0
    config.setup_completed_at = now()
    config.save(ignore_permissions=True)
    frappe.db.commit()

    return {"success": True, "message": "Setup marked as complete."}


@frappe.whitelist()
def get_system_overview():
    """For the /desk Box dashboard"""
    frappe.only_for("System Manager")

    import subprocess, shutil

    overview = {}

    # Disk usage
    result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
    overview["disk_usage"] = result.stdout

    # Uptime
    result = subprocess.run(["uptime", "-p"], capture_output=True, text=True)
    overview["uptime"] = result.stdout.strip()

    # ZFS config
    config = frappe.get_single("System Config")
    overview["zfs_pool"] = config.zfs_pool_name
    overview["raid_level"] = config.raid_level

    return overview


@frappe.whitelist()
def run_backup():
    """Trigger a Frappe site backup (enqueued)"""
    frappe.only_for("System Manager")
    frappe.enqueue(
        "frappe.desk.doctype.backup_manager.backup_manager.take_backups_if_applicable",
        queue="long",
        timeout=3600
    )
    return {"status": "queued", "message": "Backup started in background."}
