import frappe
from frappe.utils import now_datetime
from frappe.utils.pdf import get_pdf
from textwrap import dedent

def generate_certificates_for_ended_events():
    frappe.log_error("Scheduler Triggered", "Certificate Debug")

    try:
      
        events = frappe.get_all(
            "Events",
            filters={"end_datetime": ["<=", now_datetime()]},
            fields=["name", "event_name"]
        )

        if not events:
            frappe.log_error("No ended events found", "Certificate Debug")
            return

        for event in events:
            frappe.log_error("Processing Event", event.name)

            
            participants = frappe.get_all(
                "Participant",
                filters={"events": event.name},
                fields=["name", "full_name", "email", "certificate_issued"]
            )

            frappe.log_error("Participants Fetched", f"{len(participants)} for {event.name}")

            for p in participants:
                if p.certificate_issued:
                    frappe.log_error("Skipped Already Issued", p.full_name)
                    continue

               
                exists = frappe.get_all(
                    "Certificate Generation",
                    filters={"participant_name": p.name, "events": event.name},
                    limit=1
                )

                if exists:
                    frappe.db.set_value("Participant", p.name, "certificate_issued", 1)
                    frappe.db.commit()
                    frappe.log_error("Skipped Duplicate", f"{p.name} / {event.name}")
                    continue

                try:
                    
                    cert = frappe.new_doc("Certificate Generation")
                    cert.participant_name = p.name
                    cert.events = event.name
                    cert.generated_on = now_datetime()
                    cert.insert(ignore_permissions=True)

                   
                    print_format_doc = frappe.get_doc("Print Format", "Certificate Print")
                    template_html = print_format_doc.html

                  
                    doc = frappe.get_doc("Certificate Generation", cert.name)
                    rendered_html = frappe.render_template(template_html, {"doc": doc})

                  
                    pdf = get_pdf(
                        rendered_html,
                        options={"page-size": "A4", "orientation": "Landscape"}
                    )

                    if not pdf:
                        frappe.log_error("PDF Generation Failed", cert.name)
                        continue

                    frappe.log_error("PDF Size", f"{cert.name}: {len(pdf)} bytes")

                  
                    email_body = dedent(f"""
                        <p>Hi {p.full_name},</p>
                        <p>Thank you for attending <strong>{event.event_name}</strong>.</p>
                        <p>Your certificate is attached.</p>
                        <p>Best regards,<br>AERELE Team</p>
                    """)

                   
                    frappe.enqueue(
                        method=frappe.sendmail,
                        queue='short',
                        recipients=[p.email],
                        subject="Your Participation Certificate",
                        message=email_body,
                        attachments=[{
                            "fname": f"{p.full_name.replace(' ', '_')}_certificate.pdf",
                            "fcontent": pdf
                        }]
                    )

                    
                    frappe.db.set_value("Participant", p.name, "certificate_issued", 1)
                    frappe.db.commit()
                    frappe.log_error("Certificate Created", f"{p.full_name} for {event.name}")

                except Exception:
                    frappe.log_error(frappe.get_traceback(), f"Certificate Generation Failed for {p.full_name}")

    except Exception:
        frappe.log_error(frappe.get_traceback(), "Certificate Debug - FATAL")

