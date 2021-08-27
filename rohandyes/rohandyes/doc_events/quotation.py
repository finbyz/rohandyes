from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, flt, cint, get_url_to_form
from rohandyes.api import creation_comment,cancellation_comment,delete_comment

def on_submit(self,method):
    creation_comment(self)

def before_cancel(self,method):
    cancellation_comment(self)

def on_trash(self,method):
    delete_comment(self)