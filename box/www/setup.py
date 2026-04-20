import frappe

no_cache = 1  # Don't cache this page

def get_context(context):
    context.no_cache = 1
    # Check setup status — redirect if already done
    try:
        config = frappe.get_single("System Config")
        if not config.first_time:
            # Setup done, redirect to login
            frappe.local.flags.redirect_location = "/login"
            raise frappe.Redirect
    except frappe.Redirect:
        raise
    except Exception:
        pass  # First time — show the setup page