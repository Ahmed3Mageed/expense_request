# expense_request/utils/expense_utils.py
import frappe
from frappe import _
from frappe.utils import flt, getdate

def get_expense_account(expense_type):
    """Get the expense account for a given expense type"""
    account = frappe.get_cached_value("Expense Type", expense_type, "account")
    if not account:
        frappe.throw(_("Account not configured for Expense Type: {0}").format(expense_type))
    return account

def get_supplier_payable_account(supplier, company):
    """Get the payable account for a supplier"""
    default_payable = frappe.get_cached_value("Company", company, "default_payable_account")
    supplier_payable = frappe.get_cached_value("Supplier", supplier, "default_payable_account")
    return supplier_payable or default_payable

def calculate_total_amount(expenses):
    """Calculate total amount from expense items"""
    return sum(flt(item.amount) for item in expenses)

def get_payment_account_type(payment_account):
    """Get account type for payment account"""
    return frappe.get_cached_value("Account", payment_account, "account_type")

def validate_payment_account(payment_account):
    """Validate if the payment account is valid"""
    account_type = get_payment_account_type(payment_account)
    if account_type not in ["Bank", "Cash"]:
        frappe.throw(_("Payment Account must be a Bank or Cash account"))

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

def validate_expense_date(expense_date):
    """Validate expense date"""
    if getdate(expense_date) > getdate():
        frappe.throw(_("Expense Date cannot be in the future"))

def validate_accounting_period(posting_date):
    """Validate if accounting period is open"""
    from erpnext.accounts.utils import get_fiscal_year

    fiscal_year = get_fiscal_year(posting_date)[0]
    if not fiscal_year:
        frappe.throw(_("Fiscal Year for date {0} does not exist").format(posting_date))

    if frappe.db.get_value("Fiscal Year", fiscal_year, "closed"):
        frappe.throw(_("Fiscal Year {0} is closed").format(fiscal_year))
