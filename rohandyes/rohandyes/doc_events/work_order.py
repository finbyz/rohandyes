import frappe
from frappe.utils import flt
from erpnext.manufacturing.doctype.bom.bom import BOM

def validate(self,method):
	get_rate(self)
	yield_calculation(self)
	calculate_total(self)

def get_rate(self):
	for d in self.get("required_items"):
		if not d.rate:
			d.rate = BOM.get_rm_rate(frappe.get_doc("BOM",self.bom_no),{
				"company": self.company,
				"item_code": d.item_code,
			})

def on_submit(self,method):
	if self.produced_quantity:
		self.db_set('status',"Completed")
	#create_bom(self)

def on_cancel(self,method):
	pass
	#cancel_bom(self)

def calculate_total(self):
	total_amount = 0.0
	total_qty = 0.0
	concentration = self.concentration or 100
	for row in self.required_items:
		row.amount = flt(row.rate) * flt(row.qty)
		total_amount += flt(row.amount)
		total_qty += flt(row.qty)
	self.total_amount = total_amount
	self.total_qty = total_qty
	if not self.produced_quantity:
		frappe.throw("Please enter Produced quantity")
	self.valuation_price = flt(self.total_amount) / flt(self.produced_quantity)
	self.standard_quantity = flt(self.produced_quantity * concentration / 100)
	self.standard_price = flt((self.valuation_price * 100) / concentration)

def create_bom(self):
	doc = frappe.new_doc("BOM")
	doc.item = self.production_item
	doc.is_active = 1
	doc.is_default = 0
	doc.company = self.company
	doc.quantity = self.qty
	doc.based_on = self.based_on
	doc.from_work_order = self.name
	for row in self.required_items:
		doc.append("items",{
			'item_code': row.item_code,
			'qty': row.qty,
			'rate': row.rate
		})
	doc.save(ignore_permissions=True)
	doc.submit()

def cancel_bom(self):
	if frappe.db.exists("BOM",{'from_work_order':self.name,'docstatus':1}):
		doc = frappe.get_doc("BOM",{'from_work_order':self.name,'docstatus':1})
		doc.flags.ignore_permissions = True
		from_work_order=frappe.db.get_value(doc.doctype,doc.name,'from_work_order')
		try:
			frappe.db.set_value(doc.doctype,doc.name,'from_work_order','')
			doc.cancel()
			doc.delete()
		except Exception as e:
			frappe.db.set_value(doc.doctype,doc.name,'from_work_order',from_work_order)
			raise e

def yield_calculation(self):
	if self.concentration and self.produced_quantity:
		cal_yield = 0
		for d in self.required_items:
			if self.based_on and self.based_on == d.item_code and d.qty:
				cal_yield = flt(self.produced_quantity*self.concentration/100) / flt(d.qty)	
		self.batch_yield = cal_yield