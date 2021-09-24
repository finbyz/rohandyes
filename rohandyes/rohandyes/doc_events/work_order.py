import frappe
from frappe.utils import flt, cstr
from erpnext.manufacturing.doctype.bom.bom import BOM

def validate(self,method):
	get_rate(self)
	yield_calculation(self)
	calculate_total(self)

def on_update_after_submit(self,method):
	update={}
	bom_concentration=frappe.db.get_value("BOM",self.bom_no,"concentration")
	frappe.db.set_value("Work Order",self.name,"bom_concentration",bom_concentration)
	update['concentration_compared_to_standard']=self.concentration_compared_to_standard
	update['bom_concentration']=bom_concentration
	update['concentration']= flt(update['bom_concentration']) * flt(update['concentration_compared_to_standard'])/100
	calculate_concentration_after_submit(self,update)
	yield_calculation_after_submit(self,update)
	calculate_total_after_submit(self,update)
	frappe.reload_doc("manufacturing","doctype","work_order")


def calculate_concentration_after_submit(self,update):
	frappe.db.set_value("Work Order",self.name,"concentration",flt(update['bom_concentration'])*flt(update['concentration_compared_to_standard'])/100)

def yield_calculation_after_submit(self,update):
	if self.concentration and self.produced_quantity:
		cal_yield = 0
		for d in self.required_items:
			if self.based_on and self.based_on == d.item_code and d.qty:
				cal_yield = flt(self.standard_quantity) / flt(d.qty)
				# cal_yield = flt(self.produced_quantity*update['concentration_compared_to_standard']/100) / flt(d.qty)	
		batch_yield = cal_yield
		frappe.db.set_value("Work Order",self.name,"batch_yield",cal_yield)

def calculate_total_after_submit(self,update):
	total_amount = 0.0
	total_qty = 0.0
	concentration = update['concentration_compared_to_standard'] or 100
	for row in self.required_items:
		total_amount += flt(row.amount)
		total_qty += flt(row.qty)
	valuation_price = flt(self.total_amount) / flt(self.produced_quantity)
	standard_quantity = flt(self.produced_quantity * concentration / 100)
	standard_price = flt((valuation_price * 100) / concentration)
	frappe.db.set_value("Work Order",self.name,"standard_quantity",standard_quantity)
	frappe.db.set_value("Work Order",self.name,"standard_price",standard_price)


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
	create_batch(self)
	#create_bom(self)

def create_batch(self):
	if frappe.db.get_value("Item",self.production_item,'has_batch_no'):
		batch = frappe.new_doc("Batch")
		batch.item = self.production_item
		batch.lot_no = cstr(self.lot_no)
		# batch.packaging_material = cstr(row.packaging_material)
		# batch.packing_size = cstr(row.packing_size)
		batch.batch_yield = flt(self.batch_yield, 3)
		batch.concentration = flt(self.concentration, 3)
		batch.valuation_rate = flt(self.valuation_price, 4)
		batch.reference_doctype = self.doctype
		batch.reference_name = self.name
		batch.insert()
	#self.db_set('batch',batch.name)

def on_cancel(self,method):
	if frappe.db.exists("Batch",{'reference_doctype':self.doctype,'reference_name':self.name}):
		batch_no = frappe.get_doc({"doctype":"Batch",'reference_doctype':self.doctype,'reference_name':self.name})
		frappe.delete_doc("Batch", batch_no.name)
	#cancel_bom(self)

def calculate_total(self):
	total_amount = 0.0
	total_qty = 0.0
	concentration = self.concentration_compared_to_standard or 100
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
				cal_yield = flt(self.standard_quantity) / flt(d.qty)	
		self.batch_yield = cal_yield