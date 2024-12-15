import frappe
from frappe.model.document import Document
from frappe.utils import flt, getdate
from ..expense_entry_item.expense_entry_item import ExpenseEntryItem
from ...utils.expense_utils import get_expense_account
from ...services.journal_entry_service import create_journal_entries
from ...services.payment_entry_service import create_supplier_payment_entry

class ExpenseEntry(Document):
    def validate(self):
        self.validate_expenses()
        self.calculate_total()
        
    def validate_expenses(self):
        if not self.expenses:
            frappe.throw("At least one expense item is required")
            
    def calculate_total(self):
        self.total_amount = sum(flt(item.amount) for item in self.expenses)
        
    def before_submit(self):
        self.status = "Submitted"
        
    def on_submit(self):
        self.create_accounting_entries()
        
    def on_cancel(self):
        self.status = "Cancelled"
        
    def create_accounting_entries(self):
        # Create separate journal entries for each expense
        journal_entries = create_journal_entries(self)
        
        # Submit all journal entries
        for je in journal_entries:
            je.submit()
        
        # Create supplier payment entries
        for item in self.expenses:
            if item.supplier:
                create_supplier_payment_entry(self, item)
                
    def on_trash(self):
        self.check_if_deletable()
        
    def check_if_deletable(self):
        if self.status == "Submitted":
            frappe.throw("Cannot delete submitted expense entry")