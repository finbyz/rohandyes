import frappe

def validate(self,method):
	calculate_total(self)

def calculate_total(self):
	total_amount = 0
	for row in self.items:
		row.basic_amount = row.basic_rate * row.qty
		total_amount += row.basic_amount 
	self.amount = total_amount

def on_submit(self,method):
	pass
	# create_sample(self)

def on_cancel(self,method):
	pass
	# cancel_sample(self)

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