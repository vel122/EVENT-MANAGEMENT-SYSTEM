import frappe
from frappe.utils import format_datetime
from datetime import datetime, timedelta

# 🔹 Function 1: Registration Confirmation Email
def send_registration_confirmation(doc, method):
    if not doc.email:
        return

    event_doc = frappe.get_doc("Events", doc.events)

    subject = f"Registration Confirmed: {event_doc.event_name}"

    message = f"""
    <div style="font-family: Arial, sans-serif;">
        <p>Hello <strong>{doc.full_name}</strong>,</p>

        <p>You have successfully registered for the event: <strong>{event_doc.event_name}</strong>.</p>

        <h3 style="margin-top: 30px;">Event Schedule</h3>
        <table style="border-collapse: collapse; width: 100%; max-width: 600px; font-size: 15px;">
            <tr style="background-color: #f2f2f2;">
                <th style="padding: 8px; border: 1px solid #ccc;">Field</th>
                <th style="padding: 8px; border: 1px solid #ccc;">Details</th>
            </tr>
            <tr><td style="padding: 8px; border: 1px solid #ccc;">Event Name</td><td style="padding: 8px; border: 1px solid #ccc;">{event_doc.event_name}</td></tr>
            <tr><td style="padding: 8px; border: 1px solid #ccc;">Event Type</td><td style="padding: 8px; border: 1px solid #ccc;">{event_doc.event_type}</td></tr>
            <tr><td style="padding: 8px; border: 1px solid #ccc;">Location</td><td style="padding: 8px; border: 1px solid #ccc;">{event_doc.event_location}</td></tr>
            <tr><td style="padding: 8px; border: 1px solid #ccc;">Start Date & Time</td><td style="padding: 8px; border: 1px solid #ccc;">{format_datetime(event_doc.start_datetime)}</td></tr>
            <tr><td style="padding: 8px; border: 1px solid #ccc;">End Date & Time</td><td style="padding: 8px; border: 1px solid #ccc;">{format_datetime(event_doc.end_datetime)}</td></tr>
            <tr><td style="padding: 8px; border: 1px solid #ccc;">Capacity</td><td style="padding: 8px; border: 1px solid #ccc;">{event_doc.capacity}</td></tr>
        </table>

        <p style="margin-top: 30px;">Thank you!</p>
    </div>
    """

    frappe.sendmail(
        recipients=[doc.email],
        subject=subject,
        message=message
    )


# 🔹 Function 2: Reminder Email 1 Day Before the Event
def send_event_reminders():
    tomorrow = (datetime.now() + timedelta(days=1)).date()

    events = frappe.get_all("Events", filters={"start_date": tomorrow}, fields=[
        "name", "event_name", "event_location", "start_datetime", "end_datetime"
    ])

    for event in events:
        participants = frappe.get_all("Participant", filters={
            "events": event.name, "status": "Registered"
        }, fields=["full_name", "email"])

        for participant in participants:
            if not participant.email:
                continue

            subject = f"Reminder: Upcoming Event - {event.event_name}"

            message = f"""
            <div style="font-family: Arial, sans-serif;">
                <p>Hello <strong>{participant.full_name}</strong>,</p>

                <p>This is a kind reminder that you’re registered for the upcoming event:</p>

                <h3>{event.event_name}</h3>
                <table style="border-collapse: collapse; width: 100%; max-width: 600px; font-size: 15px;">
                    <tr style="background-color: #f2f2f2;">
                        <th style="padding: 8px; border: 1px solid #ccc;">Field</th>
                        <th style="padding: 8px; border: 1px solid #ccc;">Details</th>
                    </tr>
                    <tr><td style="padding: 8px; border: 1px solid #ccc;">Location</td><td style="padding: 8px; border: 1px solid #ccc;">{event.event_location}</td></tr>
                    <tr><td style="padding: 8px; border: 1px solid #ccc;">Start</td><td style="padding: 8px; border: 1px solid #ccc;">{format_datetime(event.start_datetime)}</td></tr>
                    <tr><td style="padding: 8px; border: 1px solid #ccc;">End</td><td style="padding: 8px; border: 1px solid #ccc;">{format_datetime(event.end_datetime)}</td></tr>
                </table>

                <p style="margin-top: 30px;">We look forward to seeing you there!</p>
            </div>
            """

            frappe.sendmail(
                recipients=[participant.email],
                subject=subject,
                message=message
            )

