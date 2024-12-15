import frappe
from frappe import _
from frappe.model.document import Document
from .services.validation_service import ValidationService
from .services.accounting_service import AccountingService
from ...utils.expense_utils import calculate_total_amount

class ExpenseEntry(Document):
    def validate(self):
        validation_service = ValidationService(self)
        validation_service.validate()
        self.calculate_total()
        
    def calculate_total(self):
        self.total_amount = calculate_total_amount(self.expenses)
        
    def on_submit(self):
        self.status = "Submitted"
        accounting_service = AccountingService(self)
        accounting_service.create_accounting_entries()
        
    def on_cancel(self):
        self.status = "Cancelled"
        self.cancel_linked_entries()
        
    def cancel_linked_entries(self):
        """Cancel related accounting entries"""
        # Cancel Journal Entries
        journal_entries = frappe.get_all(
            "Journal Entry",
            filters={
                "reference_type": "Expense Entry",
                "reference_name": self.name,
                "docstatus": 1
            }
        )
        
        for je in journal_entries:
            doc = frappe.get_doc("Journal Entry", je.name)
            doc.cancel()
            
        # Cancel Payment Entries
        payment_entries = frappe.get_all(
            "Payment Entry",
            filters={
                "reference_no": self.name,
                "docstatus": 1
            }
        )
        
        for pe in payment_entries:
            doc = frappe.get_doc("Payment Entry", pe.name)
            doc.cancel()