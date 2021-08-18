cur_frm.fields_dict.items.grid.get_field("work_order").get_query = function(doc,cdt,cdn) {
    let d = locals[cdt][cdn];
    if(!d.item_name){
        frappe.throw("Please select item code")
    }
	return {
		filters: {
			  "docstatus": 1,
			  'production_item': d.item_name
		}
	};
};