import frappe
from frappe import _
from frappe.utils import flt, getdate

def get_expense_account(expense_type):
    """Get the expense account for a given expense type"""
    account = frappe.get_cached_value("Expense Type", expense_type, "account")
    if not account:
        frappe.throw(_("Account not configured for Expense Type: {0}").format(expense_type))
    return account

def validate_payment_account(payment_account):
    """Validate if the payment account is valid"""
    account_type = frappe.get_cached_value("Account", payment_account, "account_type")
    if account_type not in ["Bank", "Cash"]:
        frappe.throw(_("Payment Account must be a Bank or Cash account"))
        
def get_supplier_payable_account(supplier, company):
    """Get the payable account for a supplier"""
    default_payable = frappe.get_cached_value("Company", company, "default_payable_account")
    supplier_payable = frappe.get_cached_value("Supplier", supplier, "default_payable_account")
    return supplier_payable or default_payable

def validate_expense_date(expense_date):
    """Validate expense date"""
    if getdate(expense_date) > getdate():
        frappe.throw(_("Expense Date cannot be in the future"))

def calculate_total_amount(expenses):
    """Calculate total amount from expense items"""
    return sum(flt(item.amount) for item in expenses)