import frappe

def on_submit(self,method):
    so_status_change(self)



def so_status_change(self):
    for each in self.items:
        if each.sales_order:
            if frappe.db.get_value("Sales Order",each.sales_order,"per_billed")==100.0 and frappe.db.get_value("Sales Order",each.sales_order,"status") != "Completed":
                frappe.db.set_value("Sales Order",each.sales_order,"status","Completed")