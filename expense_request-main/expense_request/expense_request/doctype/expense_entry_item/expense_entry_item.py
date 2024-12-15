import frappe
from frappe.model.document import Document
from ...utils.expense_utils import get_expense_account

class ExpenseEntryItem(Document):
    def validate(self):
        self.validate_amount()
        self.set_expense_account()
        
    def validate_amount(self):
        if self.amount <= 0:
            frappe.throw("Amount must be greater than zero")
            
    def set_expense_account(self):
        if not self.account:
            self.account = get_expense_account(self.expense_type)