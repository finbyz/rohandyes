from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import flt, cint

def auto_close_lead():
	""" auto close the `Replied` Leads after 15 days """
	auto_close_after_days = 15

	leads = frappe.db.sql(""" select name from `tabLead` where (status='Replied' or status='Open') and
		modified<DATE_SUB(CURDATE(), INTERVAL %s DAY) """, (auto_close_after_days), as_dict=True)

	for lead in leads:
		doc = frappe.get_doc("Lead", lead.get("name"))
		doc.status = "Closed"
		doc.flags.ignore_permissions = True
		doc.flags.ignore_mandatory = True
		doc.save()    