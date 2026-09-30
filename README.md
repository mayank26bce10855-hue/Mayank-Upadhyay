# Personal Expense Tracker

A command-line expense tracker written in pure Python. Log spending across multiple accounts, organize it by category, set budgets with alerts, and view summary analytics, all from an interactive menu.

## Features

- **Expense logging**: record amount, category, description, and date
- **Multiple accounts**: comes with `Personal`, `Work`, and `Cash`; create more and switch between them at any time
- **Categories**: eight defaults (Food, Transport, Housing, Utilities, Entertainment, Healthcare, Shopping, General), plus custom categories created on the fly
- **Budgets and alerts**:
  - Set a spending cap per category (defaults: Food $300, Transport $150, Entertainment $100)
  - Get an alert when an expense would bring a category to 85% or more of its budget
  - Get a warning when an expense would exceed the budget
- **Filter and search**: by account, category, amount range, or description keyword
- **Summary analytics**: total spend, transaction count, average, highest and lowest expense, and percentage breakdowns by category and account
- **Record management**: edit or delete individual expenses, or clear everything (requires typing `YES` to confirm)
- **Input validation**: rejects negative amounts, non-numeric input, and out-of-range menu choices

## Requirements

- Python 3.6 or newer (uses f-strings)
- No third-party dependencies

## Getting Started

1. Save the script as `project.py`.
2. Run it from a terminal:

   ```bash
   python project.py
   ```

3. Choose an option from the main menu by entering its number.

## Usage

### Main menu

```
===
   Personal Expense Tracker

 Active Account : [Personal]
 Total Logged   : 0 Records

1. Add New Expense
2. View All Expenses
3. Filter & Search Expenses
4. View Summary & Financial Analytics
5. Manage Budgets & Alerts
6. Manage Accounts
7. Edit / Delete Expense Records
8. Exit Application
```

### Adding an expense

1. Select **1. Add New Expense**.
2. Enter the amount. Entering `0` cancels the entry.
3. Pick a category, or choose **+ Add New Category** to create one.
4. Optionally add a description. Leaving it blank stores `N/A`.
5. Optionally enter a date. Leaving it blank stores `Today`.

The expense is saved to the currently active account. Any budget alert or warning appears after you pick the category.

### Filtering and searching

| Option | What it does |
| --- | --- |
| Filter by Account | Lists expenses for one account and shows its total |
| Filter by Category | Lists expenses for one category and shows its total |
| Filter by Amount Range | Lists expenses between a minimum and maximum amount |
| Search by Keyword | Case-insensitive search of expense descriptions |

### Editing records

Under **Edit / Delete Expense Records**, pick an expense by its ID number. When editing, leave any field blank to keep its current value.

## Project Structure

The project is a single file, organized by responsibility:

| Area | Key functions |
| --- | --- |
| State | `create_initial_state()` |
| Input validation | `get_valid_float()`, `get_valid_int()` |
| Display helpers | `print_header()`, `print_sub_header()`, `print_divider()`, `format_expense_row()` |
| Expenses | `add_expense()`, `view_all_expenses()`, `edit_expense()`, `delete_expense()` |
| Filtering | `filter_menu()` and the `filter_expenses_by_*` / `search_expenses_by_keyword()` functions |
| Analytics | `show_overall_summary()`, `calculate_category_totals()`, `calculate_account_totals()` |
| Budgets and accounts | `manage_budgets()`, `check_budget_alert()`, `manage_accounts()` |
| Entry point | `main()` |

All data lives in a single `state` dictionary holding accounts, categories, expenses, budgets, and the next expense ID.

## Limitations

- **No persistent storage.** Data is held in memory only and is lost when the program exits. Saving to JSON or a database is a natural next step.
- **Dates are free text.** They are stored as typed and not validated or parsed, so budgets are checked against all recorded expenses in a category, not a specific month.
- **Budgets are not tied to an account.** Spending toward a budget is counted across all accounts.

## Ideas for Future Improvements

- Save and load data from a JSON or CSV file
- Validate dates and support real monthly budget periods
- Export reports to CSV
- Add unit tests and guard `main()` with `if __name__ == "__main__":`

## License

Add a license of your choice here (for example, MIT).
