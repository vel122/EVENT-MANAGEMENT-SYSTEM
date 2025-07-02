import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
from frappe import _

class Participant(Document):

    def validate(self):
        event_doc = frappe.get_doc("Events", self.events)

        # Check if event has ended
        if event_doc.end_datetime <= now_datetime():
            frappe.throw(_("Cannot register. The event '{0}' has already ended.".format(event_doc.event_name)))

        # Check if capacity is full
        current_count = frappe.db.count("Participant", {
            "events": self.events,
            "status": "Registered"
        })
        if current_count >= event_doc.capacity:
            frappe.throw(_("Event '{0}' is already full.".format(event_doc.event_name)))

    def after_insert(self):
        self.update_event_participant_count()

    def on_update(self):
        if self.status == "Attended" and not self.certificate_issued:
            generate_certificate(self.name)

        self.update_event_participant_count()

    def update_event_participant_count(self):
        if self.events:
            count = frappe.db.count("Participant", {
                "events": self.events,
                "status": "Registered"
            })

            event_doc = frappe.get_doc("Events", self.events)
            event_doc.registered_participants = count

            # Update event status based on capacity
            if count >= event_doc.capacity:
                event_doc.status = "Full"
            else:
                event_doc.status = "Open"

            event_doc.save(ignore_permissions=True)


def generate_certificate(participant_name):
    participant = frappe.get_doc("Participant", participant_name)

    certificate = frappe.new_doc("Event Certificate")
    certificate.participant = participant.name
    certificate.email = participant.email
    certificate.event = participant.events
    certificate.insert(ignore_permissions=True)

    pdf = frappe.get_print("Event Certificate", certificate.name, print_format="Certificate Format")
    file = frappe.get_doc({
        "doctype": "File",
        "file_name": f"{participant.name}_certificate.pdf",
        "attached_to_doctype": "Participant",
        "attached_to_name": participant.name,
        "content": pdf,
        "is_private": 1
    })
    file.insert(ignore_permissions=True)

    participant.certificate_issued = 1
    participant.save(ignore_permissions=True)

