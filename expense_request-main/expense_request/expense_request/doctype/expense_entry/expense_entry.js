frappe.ui.form.on('Expense Entry', {
    setup: function(frm) {
        frm.set_query('payment_account', function() {
            return {
                filters: {
                    'account_type': ['in', ['Bank', 'Cash']],
                    'company': frm.doc.company
                }
            };
        });
        
        frm.set_query('expense_type', 'expenses', function() {
            return {
                filters: {
                    'disabled': 0
                }
            };
        });
    },
    
    refresh: function(frm) {
        frm.events.show_general_ledger(frm);
    },
    
    show_general_ledger: function(frm) {
        if(frm.doc.docstatus > 0) {
            frm.add_custom_button(__('General Ledger'), function() {
                frappe.route_options = {
                    "voucher_no": frm.doc.name,
                    "from_date": frappe.datetime.add_days(frm.doc.posting_date, -7), // Show entries for a week around posting
                    "to_date": frappe.datetime.add_days(frm.doc.posting_date, 7),
                    "company": frm.doc.company
                };
                frappe.set_route("query-report", "General Ledger");
            }, __("View"));
        }
    },
    
    company: function(frm) {
        if(frm.doc.company) {
            frm.events.set_payment_account(frm);
        }
    },
    
    set_payment_account: function(frm) {
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'Company',
                filters: { name: frm.doc.company },
                fieldname: 'default_cash_account'
            },
            callback: function(r) {
                if(r.message && r.message.default_cash_account) {
                    frm.set_value('payment_account', r.message.default_cash_account);
                }
            }
        });
    }
});

frappe.ui.form.on('Expense Entry Item', {
    expenses_add: function(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        row.payment_method = 'Cash'; // Set default payment method
        row.expense_date = frappe.datetime.get_today(); // Set default expense date
    },
    
    amount: function(frm, cdt, cdn) {
        frm.events.calculate_total(frm);
    },
    
    expenses_remove: function(frm) {
        frm.events.calculate_total(frm);
    },
    
    calculate_total: function(frm) {
        var total = 0;
        frm.doc.expenses.forEach(function(item) {
            total += flt(item.amount);
        });
        frm.set_value('total_amount', total);
    },
    
    supplier: function(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
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