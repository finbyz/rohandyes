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
