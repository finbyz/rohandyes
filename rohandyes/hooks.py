from . import __version__ as app_version

app_name = "rohandyes"
app_title = "Rohandyes"
app_publisher = "Finbyz Tech Pvt Ltd"
app_description = "Custom App"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@finbyz.com"
app_license = "GPL 3.0"

from chemical.chemical.doctype.ball_mill_data_sheet.ball_mill_data_sheet import BallMillDataSheet
from rohandyes.rohandyes.doc_events.ball_mill_data_sheet import set_incoming_rate
BallMillDataSheet.set_incoming_rate=set_incoming_rate



doctype_js = {
	"Ball Mill Data Sheet": "public/js/doctype_js/ball_mill_data_sheet.js",
	"Outward Sample":"public/js/doctype_js/outward_sample.js",
	"Sales Invoice":"public/js/doctype_js/sales_invoice.js"
}

doc_events = {
	"Work Order": {
		"validate": "rohandyes.rohandyes.doc_events.work_order.validate",
		"on_submit": "rohandyes.rohandyes.doc_events.work_order.on_submit",
		"on_cancel": "rohandyes.rohandyes.doc_events.work_order.on_cancel",
		"on_update_after_submit":"rohandyes.rohandyes.doc_events.work_order.on_update_after_submit",
	},
	"Ball Mill Data Sheet": {
		"validate": "rohandyes.rohandyes.doc_events.ball_mill_data_sheet.validate",
		"on_submit": "rohandyes.rohandyes.doc_events.ball_mill_data_sheet.on_submit",
		"on_cancel": "rohandyes.rohandyes.doc_events.ball_mill_data_sheet.on_cancel",
	},
	"Sales Invoice":{
		"on_submit":"rohandyes.rohandyes.doc_events.sales_invoice.on_submit"
	},
	"Outward Sample":{
		"on_submit":"rohandyes.rohandyes.doc_events.outward_sample.on_submit",
		"before_update_after_submit":"rohandyes.rohandyes.doc_events.outward_sample.before_update_after_submit",
		"on_cancel":"rohandyes.rohandyes.doc_events.outward_sample.on_cancel",
		"on_trash":"rohandyes.rohandyes.doc_events.outward_sample.on_trash"
	},
	"Outward Tracking":{
		"on_submit":"rohandyes.rohandyes.doc_events.outward_tracking.on_submit",
		"before_update_after_submit":"rohandyes.rohandyes.doc_events.outward_tracking.before_update_after_submit",
		"on_cancel":"rohandyes.rohandyes.doc_events.outward_tracking.on_cancel",
		"on_trash":"rohandyes.rohandyes.doc_events.outward_tracking.on_trash"
	},
	"Quotation":{
		"on_submit":"rohandyes.rohandyes.doc_events.quotation.on_submit",
		"before_cancel":"rohandyes.rohandyes.doc_events.quotation.before_cancel",
		"on_trash":"rohandyes.rohandyes.doc_events.quotation.on_trash"		
	},
	"Sales Order":{
		"on_submit":"rohandyes.rohandyes.doc_events.sales_order.on_submit",
		"before_update_after_submit":"rohandyes.rohandyes.doc_events.sales_order.before_update_after_submit",
		"before_cancel":"rohandyes.rohandyes.doc_events.sales_order.before_cancel",
		"on_trash":"rohandyes.rohandyes.doc_events.sales_order.on_trash"		
	},
	"BOM":{
		"on_update_after_submit":"rohandyes.rohandyes.doc_events.bom.on_update_after_submit",
	}
}

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/rohandyes/css/rohandyes.css"
# app_include_js = "/assets/rohandyes/js/rohandyes.js"

# include js, css files in header of web template
# web_include_css = "/assets/rohandyes/css/rohandyes.css"
# web_include_js = "/assets/rohandyes/js/rohandyes.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "rohandyes/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "rohandyes.install.before_install"
# after_install = "rohandyes.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "rohandyes.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------
scheduler_events = {
	"daily":[
		"rohandyes.rohandyes.doc_events.lead.auto_close_lead"
	]
}
# scheduler_events = {
# 	"all": [
# 		"rohandyes.tasks.all"
# 	],
# 	"daily": [
# 		"rohandyes.tasks.daily"
# 	],
# 	"hourly": [
# 		"rohandyes.tasks.hourly"
# 	],
# 	"weekly": [
# 		"rohandyes.tasks.weekly"
# 	]
# 	"monthly": [
# 		"rohandyes.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "rohandyes.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "rohandyes.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Quotation": "rohandyes.rohandyes.dashboard.quotation.get_data",
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"rohandyes.auth.validate"
# ]

