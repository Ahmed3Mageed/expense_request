frappe.ui.form.on('Expense Entry', {
    refresh: function(frm) {
        frm.set_query('payment_account', function() {
            return {
                filters: {
                    'account_type': ['in', ['Bank', 'Cash']],
                    'company': frm.doc.company
                }
            };
        });
    },
    
    validate: function(frm) {
        let total = 0;
        frm.doc.expenses.forEach(function(item) {
            total += flt(item.amount);
        });
        frm.set_value('total_amount', total);
    }
});

frappe.ui.form.on('Expense Entry Item', {
    expenses_add: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        row.expense_date = frappe.datetime.get_today();
        row.payment_method = 'Cash';
    },
    
    amount: function(frm, cdt, cdn) {
        frm.events.validate(frm);
    },
    
    supplier: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if(row.supplier) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Supplier',
                    name: row.supplier
                },
                callback: function(r) {
                    if(r.message) {
                        frappe.model.set_value(cdt, cdn, 'account', 
                            r.message.default_expense_account);
                    }
                }
            });
        }
    }
});