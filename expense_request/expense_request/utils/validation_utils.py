import frappe
from frappe import _
from frappe.utils import getdate

def validate_mandatory_fields(doc):
    """Validate mandatory fields in expense entry"""
    if not doc.company:
        frappe.throw(_("Company is mandatory"))
    
    if not doc.payment_account:
        frappe.throw(_("Payment Account is mandatory"))

def validate_expense_permissions(user):
    """Check if user has permission to create/edit expenses"""
    if not frappe.has_permission("Expense Entry", "write", user=user):
        frappe.throw(_("Not permitted to create/edit expenses"))

def validate_supplier_exists(supplier):
    """Validate if supplier exists"""
    if supplier and not frappe.db.exists("Supplier", supplier):
        frappe.throw(_("Supplier {0} does not exist").format(supplier))

def validate_expense_date(expense_date):
    """Validate expense date"""
    if getdate(expense_date) > getdate():
        frappe.throw(_("Expense Date cannot be in the future"))

def validate_accounting_period(posting_date):
    """Validate if accounting period is open"""
    from erpnext.accounts.utils import get_fiscal_year
    
    fiscal_year = get_fiscal_year(posting_date)[0]
    if not fiscal_year:
        frappe.throw(_("Fiscal Year {0} does not exist").format(fiscal_year))
        
    if frappe.db.get_value("Fiscal Year", fiscal_year, "closed"):
        frappe.throw(_("Fiscal Year {0} is closed").format(fiscal_year))