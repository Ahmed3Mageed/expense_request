// expense_request/public/js/expense_entry_list.js

frappe.listview_settings['Expense Entry'] = {
    add_fields: ["status", "total_amount", "company"],
    
    get_indicator: function(doc) {
        if (doc.status === "Draft") {
            return [__("Draft"), "red", "status,=,Draft"];
        } else if (doc.status === "Submitted") {
            return [__("Submitted"), "green", "status,=,Submitted"];
        } else if (doc.status === "Cancelled") {
            return [__("Cancelled"), "grey", "status,=,Cancelled"];
        }
    },
    
    formatters: {
        total_amount: function(value) {
            return format_currency(value, frappe.defaults.get_default("currency"));
        }
    }
};
