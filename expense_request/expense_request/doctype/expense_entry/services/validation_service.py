# expense_request/expense_request/doctype/expense_entry/services/validation_service.py

import frappe
from frappe import _
from ...utils.expense_utils import (
    validate_mandatory_fields,
    validate_expense_permissions,
    validate_supplier_exists,
    validate_expense_date,
    validate_accounting_period
)

class ValidationService:
    def __init__(self, expense_entry):
        self.expense_entry = expense_entry

    def validate(self):
        """Perform all validations for expense entry"""
        self._validate_basic_requirements()
        self._validate_expenses()
        self._validate_dates()

    def _validate_basic_requirements(self):
        """Validate basic document requirements"""
        validate_mandatory_fields(self.expense_entry)
        validate_expense_permissions(frappe.session.user)

    def _validate_expenses(self):
        """Validate expense entries"""
        if not self.expense_entry.expenses:
            frappe.throw(_("At least one expense item is required"))

        for expense in self.expense_entry.expenses:
            self._validate_expense_item(expense)

    def _validate_expense_item(self, expense):
        """Validate individual expense item"""
        if expense.amount <= 0:
            frappe.throw(_("Amount must be greater than zero"))

        if expense.supplier:
            validate_supplier_exists(expense.supplier)

        validate_expense_date(expense.expense_date)

    def _validate_dates(self):
        """Validate accounting period"""
        for expense in self.expense_entry.expenses:
            validate_accounting_period(expense.expense_date)
