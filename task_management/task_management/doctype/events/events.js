frappe.ui.form.on('Events', {
    onload: function(frm) {
        frappe.call({
            method: "task_management.api.event_status.update_event_statuses"
        });
    }
});
// Copyright (c) 2025, JOHN DOE and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Events", {
// 	refresh(frm) {

// 	},
// });
