import frappe
from frappe.utils import now_datetime, add_days

@frappe.whitelist()
def get_dashboard_data():
    start = now_datetime()
    end = add_days(start, 7)  # Show only next 7 days

    events = frappe.get_all(
        "Events",
        fields=["name", "event_name", "start_datetime", "registered_participants"],
        filters={"start_datetime": ["between", [start, end]]},
        order_by="start_datetime asc"
    )

    total_events = len(events)
    
    # NOTE: Using typo field name "rgistered_participants" as per your DocType
    total_participants = sum(event.get("registered_participants", 0) or 0 for event in events)

    return {
        "events": events,
        "total_events": total_events,
        "total_participants": total_participants
    }

