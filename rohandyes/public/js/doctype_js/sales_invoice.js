cur_frm.fields_dict.forwarder.get_query = function (doc) {
	return {
		filters: {
			"supplier_type": "Forwarder"
		}
	}
};