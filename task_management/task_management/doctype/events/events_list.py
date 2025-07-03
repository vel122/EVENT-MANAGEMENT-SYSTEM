import frappe
from frappe.desk.reportview import get_list as base_get_list

def get_list(args):
    # Ensure s_sub_event = 0 is always applied
    if "filters" not in args:
        args["filters"] = []

    args["filters"].append(["Events", "s_sub_event", "=", 0])

    return base_get_list(args)

