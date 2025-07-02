import frappe
from frappe.utils import now_datetime, get_datetime

@frappe.whitelist()
def update_event_statuses():
    now = now_datetime()

    events = frappe.get_all("Events", fields=["name", "end_datetime", "capacity", "registered_participants"])

    for e in events:
        end_dt = get_datetime(e.end_datetime) if e.end_datetime else None
        status = "Open"

        if end_dt and end_dt <= now:
            status = "Full"
        elif e.registered_participants >= e.capacity:
            status = "Full"

        frappe.db.set_value("Events", e.name, "custom_current_status", status)

