cur_frm.fields_dict.standard_ref.get_query = function (doc) {
	return {
		filters: {
			"naming_series": ['=',doc.naming_series]
		}
	}
};
frappe.ui.form.on("Outward Sample",{
	refresh: function(frm){
		frm.trigger('change_remarks_mandatory')
	},
	status: function(frm){
		frm.trigger('change_remarks_mandatory')
	},
	change_remarks_mandatory: function(frm){
		if (frm.doc.status == "Fail"){
         	   frm.set_df_property("remarks", "reqd",1);
        	}
		else{
			frm.set_df_property("remarks", "reqd",0);
		}
	}
})
frappe.ui.form.on("Outward Sample Detail",{
	standard_reference: function(frm,cdt,cdn){
		let d = locals[cdt][cdn]
		if(d.standard_reference){
			frappe.db.get_value("Item Standard Concentration",d.standard_reference,['item_name','concentration'],function(r){
				frappe.model.set_value(d.doctype,d.name,'item_code',r.item_name)
				frappe.model.set_value(d.doctype,d.name,'concentration',r.concentration)
				frm.script_manager.trigger('item_code', d.doctype, d.name);
				frm.script_manager.trigger('concentration', d.doctype, d.name);
			})
		}
		else{
			frappe.model.set_value(d.doctype,d.name,'item_code','')
			frappe.model.set_value(d.doctype,d.name,'concentration',0)
			frm.script_manager.trigger('item_code', d.doctype, d.name);
			frm.script_manager.trigger('concentration', d.doctype, d.name);
		}
		frm.refresh_field('details')
	}
})