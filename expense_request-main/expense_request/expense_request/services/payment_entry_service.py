import frappe
from frappe import _
from ..utils.expense_utils import get_supplier_payable_account

def create_supplier_payment_entry(expense_entry, expense_item):
    """Create payment entry for supplier expenses"""
    if not expense_item.supplier:
        return
        
    pe = frappe.new_doc("Payment Entry")
    pe.payment_type = "Pay"
    pe.posting_date = expense_item.expense_date  # Use expense item date
    pe.company = expense_entry.company
    pe.paid_from = expense_entry.payment_account
    pe.paid_amount = expense_item.amount
    pe.received_amount = expense_item.amount
    pe.party_type = "Supplier"
    pe.party = expense_item.supplier
    
    # Set references
    pe.reference_no = expense_entry.name
    pe.reference_date = expense_item.expense_date  # Use expense item date
    
    # Set accounts
    pe.paid_to = get_supplier_payable_account(expense_item.supplier, expense_entry.company)
    
    # Set payment details
    pe.mode_of_payment = expense_item.payment_method
    pe.remarks = f"Payment against Expense Entry {expense_entry.name} dated {expense_item.expense_date}"
    
    pe.submit()
    return pe