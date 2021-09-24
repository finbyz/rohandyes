import frappe
from frappe.utils import flt

def on_update_after_submit(self,method):
    pass
    # change_bom_concentration(self)

def change_bom_concentration(self):
    doc=frappe.db.get_all("Work Order",{"bom_no":self.name})
    for each in doc:
        frappe.db.set_value("Work Order",each.name,"bom_concentration",self.concentration)