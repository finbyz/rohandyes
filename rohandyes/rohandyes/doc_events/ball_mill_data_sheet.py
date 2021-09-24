import frappe
import json
from frappe.utils import cstr, flt

def validate(self,method):
	set_item_price_list_rate(self)
	calculate_total(self)
	# coaculte_order_diff(self)

def coaculte_order_diff(self):
	pass

def calculate_total(self):
	total_amount = 0
	for row in self.items:
		if row.work_order:
			row.basic_rate = frappe.db.get_value("Work Order",row.work_order,"valuation_price")
		if row.batch_no:
			row.basic_rate = frappe.db.get_value("Batch",row.batch_no,"valuation_rate")
		row.basic_amount = row.basic_rate * row.qty
		total_amount += row.basic_amount
	
	self.amount = total_amount

def on_submit(self,method):
	create_batch(self)
	# create_sample(self)

def on_cancel(self,method):
	delete_batch(self)
	# cancel_sample(self)

def create_batch(self):
	if self.packaging:
		for row in self.packaging:
			if frappe.db.get_value("Item",self.product_name,'has_batch_no'):
				batch = frappe.new_doc("Batch")
				batch.item = self.product_name
				batch.lot_no = cstr(row.lot_no) or self.item_lot_no
				batch.packaging_material = cstr(row.packaging_material)
				batch.packing_size = cstr(row.packing_size)
				batch.concentration = flt(row.concentration, 3)
				batch.valuation_rate = flt(self.per_unit_amount, 4)
				batch.reference_doctype = self.doctype
				batch.reference_name = self.name
				batch.insert()

def delete_batch(self):
	if frappe.db.exists("Batch",{'reference_doctype':self.doctype,'reference_name':self.name}):
		batches = frappe.get_all("Batch",{'reference_doctype':self.doctype,'reference_name':self.name},'name')
		if batches:
			for row in batches:
				frappe.delete_doc("Batch",row.name)

def create_sample(self):
	doc = frappe.new_doc("Outward Sample")
	doc.naming_series = "BMDOWT/.YY./.####"
	doc.date = self.date
	doc.company = self.company
	doc.ref_no = self.name
	doc.product_name = self.product_name
	doc.link_to = "Customer"
	doc.party = self.customer_name

	for row in self.items:
		doc.append("details",{
			'item_code': row.item_name,
			'quantity': row.quantity,
			'rate': row.price,
			'lot_no': row.lot_no,
			'concentration': row.concentration,
			'packing_size': row.packing_size,
			'no_of_packages': row.no_of_packages,
			'bom_no': frappe.db.get_value("BOM",{'from_work_order': row.work_order,'docstatus':1},'name')
		})
	doc.save(ignore_permissions=True)
	doc.submit()


def cancel_sample(self):
	if frappe.db.exists("Outward Sample",{'from_ball_mill':self.name,'docstatus':1}):
		doc = frappe.get_doc("Outward Sample",{'from_ball_mill':self.name,'docstatus':1})
		doc.flags.ignore_permissions = True
		try:
			doc.cancel()
		except Exception as e:
			raise e
		doc.db_set('from_ball_mill','')

def set_item_price_list_rate(self):
	for row in self.items:
		if not row.work_order or not row.batch_no:    
			per_unit_price=row.basic_rate
			if frappe.db.exists("Item Price",{"item_code":row.item_name,"price_list":row.price_list}) and row.basic_rate:
				name = frappe.db.get_value("Item Price",{"item_code":row.item_name,"price_list":row.price_list},'name')
				# frappe.db.set_value("Item Price",name,"price_list_rate", per_unit_price)
				item_doc = frappe.get_doc("Item Price",name)
				item_doc.db_set("price_list_rate",per_unit_price)
				item_doc.db_update()
				

			elif frappe.db.exists("Item Price",{"item_code":row.item_name,"price_list":row.price_list}) and not row.basic_rate:
				name = frappe.db.get_value("Item Price",{"item_code":row.item_name,"price_list":row.price_list},'name')
				item_doc = frappe.get_doc("Item Price",name)
				row.basic_rate = item_doc.price_list_rate
				

			else:
				item_price = frappe.new_doc("Item Price")	
				item_price.price_list = row.price_list
				item_price.item_code = row.item_name
				item_price.price_list_rate = row.basic_rate
				item_price.save()

# @frappe.whitelist()
# def get_item_rate(self):
# 	row=json.loads(self)
# 	price_list_rate =None
# 	if frappe.db.exists("Item Price",{"item_code":row.item_name,"price_list":row.price_list}) and row.basic_rate:
# 		price_list_rate = frappe.db.get_value("Item Price",{"item_code":row.item_name,"price_list":row.price_list},'price_list_rate')
# 	return price_list_rate


def set_incoming_rate(self):
	pass