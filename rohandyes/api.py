from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, flt, cint, get_url_to_form,get_fullname

def creation_comment(self):
    if self.doctype in ["Outward Sample","Outward Tracking"]:
        reference_doctype = self.link_to
        reference_name = self.party
    elif self.doctype == "Quotation":
        reference_doctype = self.quotation_to
        reference_name = self.party_name
    else:
        reference_doctype = "Customer"
        reference_name = self.customer

    comment_doc = frappe.new_doc("Comment")
    comment_doc.comment_type = "Info"
    comment_doc.comment_email = frappe.session.user
    comment_doc.reference_doctype = reference_doctype
    comment_doc.reference_name = reference_name
    comment_doc.link_doctype = self.doctype
    comment_doc.link_name = self.name
    comment_doc.comment_by = get_fullname(frappe.session.user)
    url = get_url_to_form(self.doctype, self.name)
    comment_doc.content = "Created {} <b><a href='{}'>{}</a></b>".format(self.doctype,url,self.name)

    comment_doc.save(ignore_permissions=True)

def status_change_comment(self):
    docstatus = "Submitted" if self.docstatus == 1 else "Cancelled"
    if self.doctype == "Outward Tracking":
        select_status = "tracking_status"
        status = self.tracking_status
        reference_doctype = self.link_to
        reference_name = self.party

    elif self.doctype == "Outward Sample":
        select_status = "status"
        status = self.status
        reference_doctype = self.link_to
        reference_name = self.party   

    elif self.doctype == "Quotation":
        select_status = "docstatus"
        status = docstatus
        reference_doctype = self.quotation_to
        reference_name = self.party_name

    else:
        select_status = "docstatus"
        status = docstatus
        reference_doctype = "Customer"
        reference_name = self.customer
    
    before_status_value = frappe.db.get_value(self.doctype,self.name,select_status)
    if self.doctype not in ["Outward Sample","Outward Tracking"]:
        before_status_value = "Submitted" if before_status_value == 1 else "Cancelled"
        
    comment_doc = frappe.new_doc("Comment")
    comment_doc.comment_type = "Info"
    comment_doc.comment_email = frappe.session.user
    comment_doc.reference_doctype = reference_doctype
    comment_doc.reference_name = reference_name
    comment_doc.link_doctype = self.doctype
    comment_doc.link_name = self.name
    comment_doc.comment_by = get_fullname(frappe.session.user)
    url = get_url_to_form(self.doctype, self.name)
    comment_doc.content = "Changed value of Status from <b>{}</b> to <b>{}</b> in {} <b><a href='{}'>{}</a></b> ".format(before_status_value,status, self.doctype,url,self.name)

    comment_doc.save(ignore_permissions=True)

def cancellation_comment(self):
    if self.doctype == "Outward Tracking":
        self.tracking_status = "Cancelled"
    elif self.doctype == "Outward Sample":
        self.status = "Rejected"
    status_change_comment(self)

def delete_comment(self):
    if self.doctype in ["Outward Sample","Outward Tracking"]:
        reference_doctype = self.link_to
        reference_name = self.party
    elif self.doctype == "Quotation":
        reference_doctype = self.quotation_to
        reference_name = self.party_name
    else:
        reference_doctype = "Customer"
        reference_name = self.customer

    comment_list = frappe.db.get_all("Comment",{"comment_type":"Info","reference_doctype":reference_doctype,
                "reference_name":reference_name,"link_doctype":self.doctype,"link_name":self.name})
    for comment in comment_list:
        frappe.delete_doc("Comment",comment.name)