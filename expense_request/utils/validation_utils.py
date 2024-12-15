import frappe
from frappe import _

def validate_mandatory_fields(doc):
    """Validate mandatory fields in expense entry"""
    if not doc.company:
        frappe.throw(_("Company is mandatory"))
    
    if not doc.payment_account:
        frappe.throw(_("Payment Account is mandatory"))
        
    if not doc.expenses:
        frappe.throw(_("At least one expense item is required"))

def validate_expense_permissions(user):
    """Check if user has permission to create/edit expenses"""
    if not frappe.has_permission("Expense Entry", "write", user=user):
        frappe.throw(_("Not permitted to create/edit expenses"))

def validate_supplier_exists(supplier):
    """Validate if supplier exists"""
    if supplier and not frappe.db.exists("Supplier", supplier):
        frappe.throw(_("Supplier {0} does not exist").format(supplier))