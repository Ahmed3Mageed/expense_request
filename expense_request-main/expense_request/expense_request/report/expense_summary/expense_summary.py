import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "fieldname": "posting_date",
            "label": _("Date"),
            "fieldtype": "Date",
            "width": 90
        },
        {
            "fieldname": "expense_type",
            "label": _("Expense Type"),
            "fieldtype": "Link",
            "options": "Expense Type",
            "width": 120
        },
        {
            "fieldname": "supplier",
            "label": _("Supplier"),
            "fieldtype": "Link",
            "options": "Supplier",
            "width": 120
        },
        {
            "fieldname": "payment_method",
            "label": _("Payment Method"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "amount",
            "label": _("Amount"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "status",
            "label": _("Status"),
            "fieldtype": "Data",
            "width": 100
        }
    ]

def get_data(filters):
    conditions = get_conditions(filters)
    
    data = frappe.db.sql("""
        SELECT 
            ee.posting_date,
            ei.expense_type,
            ei.supplier,
            ei.payment_method,
            ei.amount,
            ee.status
        FROM 
            `tabExpense Entry` ee
        INNER JOIN 
            `tabExpense Entry Item` ei ON ee.name = ei.parent
        WHERE 
            ee.docstatus = 1
            AND {conditions}
        ORDER BY 
            ee.posting_date DESC
    """.format(conditions=conditions), filters, as_dict=1)
    
    return data

def get_conditions(filters):
    conditions = []
    
    if filters.get("company"):
        conditions.append("ee.company = %(company)s")
    if filters.get("from_date"):
        conditions.append("ee.posting_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append("ee.posting_date <= %(to_date)s")
    if filters.get("expense_type"):
        conditions.append("ei.expense_type = %(expense_type)s")
    if filters.get("supplier"):
        conditions.append("ei.supplier = %(supplier)s")
        
    return " AND ".join(conditions)