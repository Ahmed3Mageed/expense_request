import frappe
from frappe import _
from ..utils.expense_utils import get_expense_account

def create_journal_entries(expense_entry):
    """Create separate journal entries for each expense item"""
    journal_entries = []
    
    # Group expenses by date
    expenses_by_date = {}
    for item in expense_entry.expenses:
        date = item.expense_date
        if date not in expenses_by_date:
            expenses_by_date[date] = []
        expenses_by_date[date].append(item)
    
    # Create journal entry for each date
    for posting_date, items in expenses_by_date.items():
        je = frappe.new_doc("Journal Entry")
        je.posting_date = posting_date
        je.company = expense_entry.company
        je.user_remark = f"Expense Entry {expense_entry.name} - {posting_date}"
        
        # Calculate total amount for this date
        total_amount = sum(flt(item.amount) for item in items)
        
        # Credit entry for payment account
        je.append("accounts", {
            "account": expense_entry.payment_account,
            "credit_in_account_currency": total_amount,
            "reference_type": "Expense Entry",
            "reference_name": expense_entry.name,
            "posting_date": posting_date
        })
        
        # Debit entries for expenses on this date
        for item in items:
            expense_account = item.account or get_expense_account(item.expense_type)
            
            je.append("accounts", {
                "account": expense_account,
                "debit_in_account_currency": item.amount,
                "cost_center": item.cost_center,
                "project": item.project,
                "party_type": "Supplier" if item.supplier else None,
                "party": item.supplier,
                "reference_type": "Expense Entry",
                "reference_name": expense_entry.name,
                "posting_date": posting_date
            })
        
        journal_entries.append(je)
    
    return journal_entries