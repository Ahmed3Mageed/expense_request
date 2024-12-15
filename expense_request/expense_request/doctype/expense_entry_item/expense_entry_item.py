import frappe
from frappe import _
from frappe.model.document import Document
from ...utils.expense_utils import get_expense_account

class ExpenseEntryItem(Document):
    def validate(self):
        self.validate_amount()
        self.set_expense_account()
        
    def validate_amount(self):
        """Validate expense amount"""
        if self.amount <= 0:
            frappe.throw(_("Amount must be greater than zero"))
            
    def set_expense_account(self):
        """Set default expense account if not specified"""
        if not self.account:
            self.account = get_expense_account(self.expense_type)