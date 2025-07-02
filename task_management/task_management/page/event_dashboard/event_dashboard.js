frappe.pages['event-dashboard'].on_page_load = function(wrapper) {
    let page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Event Dashboard',
        single_column: true
    });

    // Load the HTML template
    $(frappe.render_template("event_dashboard")).appendTo(page.body);

    // Fetch event data from backend
    frappe.call({
        method: "task_management.task_management.page.event_dashboard.event_dashboard.get_dashboard_data",
        callback: function(r) {
            const data = r.message;

            // Update counts
            document.getElementById("total-events").innerText = data.total_events || 0;
            document.getElementById("total-participants").innerText = data.total_participants || 0;

            // Populate events list
            const eventList = document.getElementById("upcoming-events");
            eventList.innerHTML = ""; // clear existing

            if (data.events && data.events.length > 0) {
                data.events.forEach(event => {
                    const li = document.createElement("li");

                    // Format date
                    let formattedDate = frappe.datetime.format_datetime(event.start_datetime, "dd-MM-yyyy hh:mm A");

                    li.innerText = `${event.event_name} - ${formattedDate}`;
                    eventList.appendChild(li);
                });
            } else {
                eventList.innerHTML = "<li>No upcoming events</li>";
            }
        }
    });
};

