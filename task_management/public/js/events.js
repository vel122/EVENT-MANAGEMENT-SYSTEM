frappe.ui.form.on('Events', {
    refresh: function (frm) {
        frm.add_custom_button(__('Generate Certificates'), function () {
            frappe.call({
                method: 'task_management.api.certificate.generate_certificates',
                args: {
                    event_name: frm.doc.name
                },
                callback: function (r) {
                    if (!r.exc) {
                        frappe.msgprint('Certificates Generated Successfully!');
                    }
                }
            });
        });
    }
});

