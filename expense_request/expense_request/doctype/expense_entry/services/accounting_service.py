import frappe
from frappe import _
from frappe.utils import flt, getdate
from ....utils.validation_utils import validate_accounting_period

class AccountingService:
    def __init__(self, expense_entry):
        self.expense_entry = expense_entry
        
    def create_accounting_entries(self):
        """Create accounting entries for each expense date"""
        expenses_by_date = self._group_expenses_by_date()
        journal_entries = []
        
        for posting_date, items in expenses_by_date.items():
            validate_accounting_period(posting_date)
            je = self._create_journal_entry(posting_date, items)
            journal_entries.append(je)
            
            # Create payment entries for supplier expenses
            for item in items:
                if item.supplier:
                    self._create_supplier_payment(item, posting_date)
                    
        return journal_entries
    
    def _group_expenses_by_date(self):
        """Group expenses by their individual expense dates"""
        expenses_by_date = {}
        for expense in self.expense_entry.expenses:
            if expense.expense_date not in expenses_by_date:
                expenses_by_date[expense.expense_date] = []
            expenses_by_date[expense.expense_date].append(expense)
        return expenses_by_date
    
    def _create_journal_entry(self, posting_date, expenses):
        """Create a journal entry for expenses on a specific date"""
        je = frappe.new_doc("Journal Entry")
        je.posting_date = posting_date
        je.company = self.expense_entry.company
        je.user_remark = f"Expense Entry {self.expense_entry.name} for date {posting_date}"
        
        total_amount = sum(flt(item.amount) for item in expenses)
        
        # Credit entry (payment account)
        je.append("accounts", {
            "account": self.expense_entry.payment_account,
            "credit_in_account_currency": total_amount,
            "reference_type": "Expense Entry",
            "reference_name": self.expense_entry.name
        })
        
        # Debit entries for each expense
        for item in expenses:
            je.append("accounts", {
                "account": item.account,
                "debit_in_account_currency": item.amount,
                "cost_center": item.cost_center,
                "project": item.project,
                "party_type": "Supplier" if item.supplier else None,
                "party": item.supplier,
                "reference_type": "Expense Entry",
                "reference_name": self.expense_entry.name
            })
            
        je.submit()
        return je
    
    def _create_supplier_payment(self, expense, posting_date):
        """Create payment entry for supplier expenses"""
        from ....utils.expense_utils import get_supplier_payable_account
        
        pe = frappe.new_doc("Payment Entry")
        pe.payment_type = "Pay"
        pe.posting_date = posting_date
        pe.company = self.expense_entry.company
        pe.paid_from = self.expense_entry.payment_account
        pe.paid_amount = expense.amount
        pe.received_amount = expense.amount
        pe.party_type = "Supplier"
        pe.party = expense.supplier
        
        # Set accounts
        pe.paid_to = get_supplier_payable_account(expense.supplier, self.expense_entry.company)
        
        # Set payment details
        pe.mode_of_payment = expense.payment_method
        pe.reference_no = self.expense_entry.name
        pe.reference_date = posting_date
        pe.remarks = f"Payment against Expense Entry {self.expense_entry.name}"
        
        pe.submit()
        return pe