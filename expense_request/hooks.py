# expense_request/hooks.py

app_name = "expense_request"
app_title = "Expense Request"
app_publisher = "Your Name"
app_description = "Expense Management System"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "your.email@example.com"
app_license = "MIT"

# Document Events
doc_events = {
    "Expense Entry": {
        "validate": "expense_request.expense_request.doctype.expense_entry.services.validation_service.ValidationService.validate",
        "on_submit": "expense_request.expense_request.doctype.expense_entry.services.accounting_service.AccountingService.create_accounting_entries",
        "on_cancel": "expense_request.expense_request.doctype.expense_entry.cancel_linked_entries"
    }
}

# Fixtures
fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            ["dt", "in", ("Expense Entry", "Expense Entry Item")]
        ]
    }
]

# Include JS/CSS files
app_include_js = [
    "/assets/expense_request/js/expense_entry.js"
]

# DocTypes to be included
doctype_js = {
    "Expense Entry": "public/js/expense_entry.js"
}

# Custom Scripts
doctype_list_js = {
    "Expense Entry": "public/js/expense_entry_list.js"
}
