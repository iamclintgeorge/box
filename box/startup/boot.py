import frappe

def get_boot_data(bootinfo):
    """
    Runs on every login. Adds Box config to frappe.boot
    so the desk JS can access it at: frappe.boot.box_config
    """
    try:
        config = frappe.get_single("System Config")
        bootinfo.box_config = {
            "first_time": config.first_time,
            "zfs_pool": config.zfs_pool_name,
            # "raid_level": config.raid_level,
        }
    except Exception:
        bootinfo.box_config = {"first_time": 1}