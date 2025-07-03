import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, get_datetime

class Events(Document):
    def validate(self):
        self.registered_participants = self.registered_participants or 0
        self.capacity = self.capacity or 0
        self.set_status()

    def on_update(self):
        self.set_status()

        # Certificate generation trigger if event has ended
        if self.end_datetime and get_datetime(self.end_datetime) <= now_datetime():
            already_generated = frappe.db.exists(
                "Certificate Generation",
                {"events": self.name}
            )
            if not already_generated:
                frappe.enqueue(
                    "task_management.api.certificate.generate_certificates_for_event",
                    event_name=self.name
                )

    def set_status(self):
        now = now_datetime()
        end_dt = get_datetime(self.end_datetime) if self.end_datetime else None

        if end_dt and end_dt <= now:
            status = "Full"
        elif self.registered_participants >= self.capacity:
            status = "Full"
        else:
            status = "Open"

        self.status = status
        self.current_status = status

        # Save to DB (so it updates List View)
        if self.get("name"):
            frappe.db.set_value("Events", self.name, "current_status", status)

# ✅ Place this **outside** the class
def get_permission_query_conditions(user):
    return "`tabEvents`.`s_sub_event` = 0"

