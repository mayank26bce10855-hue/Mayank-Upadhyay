def create_initial_state():
    return {
        "accounts": ["Personal", "Work", "Cash"],
        "active_account": "Personal",
        "categories": [
            "Food",
            "Transport",
            "Housing",
            "Utilities",
            "Entertainment",
            "Healthcare",
            "Shopping",
            "General"
        ],
        "expenses": [],
        "budgets": {
            "Food": 300.0,
            "Transport": 150.0,
            "Entertainment": 100.0
        },
        "next_id": 1
    }


def print_header(title):
    print("\n===")
    print(f"   {title}")
    print("    ")


def print_sub_header(title):
    print("\n")
    print(f"{title}")
    print("")


def print_divider():
    print(" ")


def get_valid_float(prompt, allow_empty=False, default_val=0.0):
    while True:
        raw_input = input(prompt).strip()
        if allow_empty and raw_input == "":
            return default_val
        try:
            val = float(raw_input)
            if val < 0:
                print("Error: Amount cannot be negative. Try again.")
            else:
                return val
        except ValueError:
            print("Error: Invalid number. Please enter a valid decimal.")


def get_valid_int(prompt, min_val, max_val):
    while True:
        raw_input = input(prompt).strip()
        try:
            val = int(raw_input)
            if min_val <= val <= max_val:
                return val
            else:
                print(f"Error: Choice must be between {min_val} and {max_val}.")
        except ValueError:
            print("Error: Please enter a valid integer.")


def select_category(state):
    print_sub_header("Select Category")
    categories = state["categories"]
    idx = 1
    for cat in categories:
        print(f"{idx}. {cat}")
        idx = idx + 1
    print(f"{idx}. + Add New Category")
    
    choice = get_valid_int("Choose category option: ", 1, len(categories) + 1)
    
    if choice == len(categories) + 1:
        new_cat = input("Enter new category name: ").strip().capitalize()
        if new_cat == "":
            new_cat = "General"
        if new_cat not in categories:
            categories.append(new_cat)
            print(f"Category '{new_cat}' added!")
        return new_cat
    else:
        return categories[choice - 1]


def check_budget_alert(state, category, new_amount):
    budgets = state["budgets"]
    if category not in budgets:
        return

    budget_limit = budgets[category]
    current_spent = 0.0
    for item in state["expenses"]:
        if item["category"] == category:
            current_spent = current_spent + item["amount"]

    projected_spent = current_spent + new_amount
    
    if projected_spent > budget_limit:
        over = projected_spent - budget_limit
        print(f"\n  BUDGET WARNING: Adding this expense exceeds your '{category}' budget!")
        print(f"   Budget Limit: \({budget_limit:.2f} | Projected:\){projected_spent:.2f} | Exceeded by: ${over:.2f}")
    elif projected_spent >= (budget_limit * 0.85):
        print(f"\n BUDGET ALERT: You have used {((projected_spent/budget_limit)*100):.1f}% of your '{category}' budget!")


def add_expense(state):
    print_header("Add New Expense")
    print(f"Active Account: [{state['active_account']}]")
    
    amount = get_valid_float("Enter amount ($): ")
    if amount == 0:
        print("Expense of $0.00 cancelled.")
        return

    category = select_category(state)
    check_budget_alert(state, category, amount)

    description = input("Enter description (optional): ").strip()
    if description == "":
        description = "N/A"

    date_str = input("Enter date (YYYY-MM-DD or leave empty for 'Today'): ").strip()
    if date_str == "":
        date_str = "Today"

    expense = {
        "id": state["next_id"],
        "account": state["active_account"],
        "amount": amount,
        "category": category,
        "description": description,
        "date": date_str
    }

    state["expenses"].append(expense)
    state["next_id"] = state["next_id"] + 1
    print(f"\n Expense of ${amount:.2f} added to '{category}' under account '{state['active_account']}'!")


def format_expense_row(expense):
    eid = expense["id"]
    acc = expense["account"]
    amt = expense["amount"]
    cat = expense["category"]
    desc = expense["description"]
    dt = expense["date"]
    return f"ID #{eid:<3} | {dt:<10} | {acc:<10} | {cat:<13} | ${amt:<9.2f} | {desc}"


def view_all_expenses(state):
    print_header("All Logged Expenses")
    expenses = state["expenses"]
    
    if len(expenses) == 0:
        print("No expenses recorded yet.")
        return

    print_divider()
    for item in expenses:
        print(format_expense_row(item))
    print_divider()
    print(f"Total Records: {len(expenses)}")


def filter_expenses_by_account(state):
    print_sub_header("Filter By Account")
    accs = state["accounts"]
    idx = 1
    for a in accs:
        print(f"{idx}. {a}")
        idx = idx + 1

    choice = get_valid_int("Select account to filter: ", 1, len(accs))
    selected_acc = accs[choice - 1]

    filtered = []
    for item in state["expenses"]:
        if item["account"] == selected_acc:
            filtered.append(item)

    print(f"\n--- Expenses for Account: {selected_acc} ---")
    if len(filtered) == 0:
        print("No records found for this account.")
        return

    print_divider()
    total = 0.0
    for item in filtered:
        print(format_expense_row(item))
        total = total + item["amount"]
    print_divider()
    print(f"Total Spent in {selected_acc}: ${total:.2f}")


def filter_expenses_by_category(state):
    print_sub_header("Filter By Category")
    cats = state["categories"]
    idx = 1
    for c in cats:
        print(f"{idx}. {c}")
        idx = idx + 1

    choice = get_valid_int("Select category: ", 1, len(cats))
    selected_cat = cats[choice - 1]

    filtered = []
    for item in state["expenses"]:
        if item["category"] == selected_cat:
            filtered.append(item)

    print(f"\n--- Expenses for Category: {selected_cat} ---")
    if len(filtered) == 0:
        print("No records found for this category.")
        return

    print_divider()
    total = 0.0
    for item in filtered:
        print(format_expense_row(item))
        total = total + item["amount"]
    print_divider()
    print(f"Total Spent in {selected_cat}: ${total:.2f}")


def filter_expenses_by_amount_range(state):
    print_sub_header("Filter By Amount Range")
    min_amt = get_valid_float("Enter minimum amount ($): ")
    max_amt = get_valid_float("Enter maximum amount ($): ")

    if min_amt > max_amt:
        print("Error: Minimum amount cannot be greater than maximum amount.")
        return

    filtered = []
    for item in state["expenses"]:
        if min_amt <= item["amount"] <= max_amt:
            filtered.append(item)

    print(f"\n--- Expenses Between \({min_amt:.2f} and\){max_amt:.2f} ---")
    if len(filtered) == 0:
        print("No records match this range.")
        return

    print_divider()
    for item in filtered:
        print(format_expense_row(item))
    print_divider()


def search_expenses_by_keyword(state):
    print_sub_header("Search Description Keyword")
    keyword = input("Enter search term: ").strip().lower()

    if keyword == "":
        print("Error: Search term cannot be empty.")
        return

    filtered = []
    for item in state["expenses"]:
        if keyword in item["description"].lower():
            filtered.append(item)

    print(f"\n--- Search Results for '{keyword}' ---")
    if len(filtered) == 0:
        print("No matching expenses found.")
        return

    print_divider()
    for item in filtered:
        print(format_expense_row(item))
    print_divider()


def filter_menu(state):
    if len(state["expenses"]) == 0:
        print_header("Filter Expenses")
        print("No expenses recorded yet to filter.")
        return

    while True:
        print_header("Filter & Search Menu")
        print("1. Filter by Account")
        print("2. Filter by Category")
        print("3. Filter by Amount Range")
        print("4. Search by Keyword")
        print("5. Back to Main Menu")

        choice = get_valid_int("Select option (1-5): ", 1, 5)

        if choice == 1:
            filter_expenses_by_account(state)
        elif choice == 2:
            filter_expenses_by_category(state)
        elif choice == 3:
            filter_expenses_by_amount_range(state)
        elif choice == 4:
            search_expenses_by_keyword(state)
        elif choice == 5:
            break


def calculate_category_totals(expenses):
    totals = {}
    for item in expenses:
        cat = item["category"]
        if cat in totals:
            totals[cat] = totals[cat] + item["amount"]
        else:
            totals[cat] = item["amount"]
    return totals


def calculate_account_totals(expenses):
    totals = {}
    for item in expenses:
        acc = item["account"]
        if acc in totals:
            totals[acc] = totals[acc] + item["amount"]
        else:
            totals[acc] = item["amount"]
    return totals


def show_overall_summary(state):
    print_header("Financial Summary & Analytics")
    expenses = state["expenses"]

    if len(expenses) == 0:
        print("No expenses logged yet.")
        return

    total_spent = 0.0
    highest_expense = expenses[0]
    lowest_expense = expenses[0]

    for item in expenses:
        amt = item["amount"]
        total_spent = total_spent + amt

        if amt > highest_expense["amount"]:
            highest_expense = item
        if amt < lowest_expense["amount"]:
            lowest_expense = item

    avg_spent = total_spent / len(expenses)

    print(f"Total Expenditure  : ${total_spent:.2f}")
    print(f"Total Transactions : {len(expenses)}")
    print(f"Average / Transaction: ${avg_spent:.2f}")
    print(f"Highest Single Spend : ${highest_expense['amount']:.2f} ({highest_expense['category']} - {highest_expense['description']})")
    print(f"Lowest Single Spend  : ${lowest_expense['amount']:.2f} ({lowest_expense['category']} - {lowest_expense['description']})")

    print_sub_header("Category Breakdown")
    cat_totals = calculate_category_totals(expenses)
    for cat, amt in cat_totals.items():
        percentage = (amt / total_spent) * 100
        print(f"  • {cat:<15}: ${amt:<8.2f} ({percentage:>5.1f}%)")

    print_sub_header("Account Breakdown")
    acc_totals = calculate_account_totals(expenses)
    for acc, amt in acc_totals.items():
        percentage = (amt / total_spent) * 100
        print(f"  • {acc:<15}: ${amt:<8.2f} ({percentage:>5.1f}%)")


def manage_budgets(state):
    while True:
        print_header("Budget Management")
        budgets = state["budgets"]

        print("Current Budget Caps:")
        if len(budgets) == 0:
            print("  (No active category budgets set)")
        else:
            for cat, limit in budgets.items():
                spent = 0.0
                for item in state["expenses"]:
                    if item["category"] == cat:
                        spent = spent + item["amount"]
                pct = (spent / limit) * 100 if limit > 0 else 0
                print(f"  • {cat:<15}: Limit = \({limit:<7.2f} | Spent =\){spent:<7.2f} ({pct:.1f}%)")

        print("\nOptions:")
        print("1. Set / Edit Category Budget")
        print("2. Delete Category Budget")
        print("3. Back to Main Menu")

        choice = get_valid_int("Select option (1-3): ", 1, 3)

        if choice == 1:
            cat = select_category(state)
            limit = get_valid_float(f"Enter monthly budget limit for '{cat}' ($): ")
            budgets[cat] = limit
            print(f" Budget for '{cat}' set to ${limit:.2f}.")
        elif choice == 2:
            if len(budgets) == 0:
                print("No budgets available to delete.")
            else:
                cat_list = []
                idx = 1
                for c in budgets.keys():
                    print(f"{idx}. {c}")
                    cat_list.append(c)
                    idx = idx + 1
                c_choice = get_valid_int("Select budget to remove: ", 1, len(cat_list))
                removed_cat = cat_list[c_choice - 1]
                del budgets[removed_cat]
                print(f" Budget for '{removed_cat}' removed.")
        elif choice == 3:
            break


def manage_accounts(state):
    while True:
        print_header("Account Management")
        print(f"Current Active Account: [{state['active_account']}]\n")
        
        print("Available Accounts:")
        idx = 1
        for a in state["accounts"]:
            status = " (Active)" if a == state["active_account"] else ""
            print(f"  {idx}. {a}{status}")
            idx = idx + 1

        print("\nOptions:")
        print("1. Switch Active Account")
        print("2. Create New Account")
        print("3. Back to Main Menu")

        choice = get_valid_int("Select option (1-3): ", 1, 3)

        if choice == 1:
            acc_choice = get_valid_int("Select account to switch to: ", 1, len(state["accounts"]))
            state["active_account"] = state["accounts"][acc_choice - 1]
            print(f" Active account switched to '{state['active_account']}'.")
        elif choice == 2:
            new_acc = input("Enter new account name: ").strip().capitalize()
            if new_acc == "":
                print("Account name cannot be empty.")
            elif new_acc in state["accounts"]:
                print("Account name already exists.")
            else:
                state["accounts"].append(new_acc)
                print(f" Account '{new_acc}' created!")
        elif choice == 3:
            break


def edit_expense(state):
    print_header("Edit Expense Entry")
    expenses = state["expenses"]

    if len(expenses) == 0:
        print("No expenses recorded to edit.")
        return

    view_all_expenses(state)
    target_id = get_valid_int("Enter ID # of expense to edit (0 to cancel): ", 0, state["next_id"])

    if target_id == 0:
        return

    target = None
    for item in expenses:
        if item["id"] == target_id:
            target = item
            break

    if target is None:
        print(f"No expense found with ID #{target_id}.")
        return

    print(f"\nEditing Expense #{target['id']}:")
    print(f"Current Amount     : ${target['amount']:.2f}")
    print(f"Current Category   : {target['category']}")
    print(f"Current Description: {target['description']}")
    print(f"Current Date       : {target['date']}")

    print("\nLeave inputs empty to keep current values.")

    new_amt = get_valid_float("Enter new amount ($): ", allow_empty=True, default_val=target["amount"])
    
    print("\nChange Category?")
    change_cat = input("Type 'y' to change category or press Enter to keep: ").strip().lower()
    if change_cat == "y":
        new_cat = select_category(state)
    else:
        new_cat = target["category"]

    new_desc = input("Enter new description: ").strip()
    if new_desc == "":
        new_desc = target["description"]

    new_date = input("Enter new date: ").strip()
    if new_date == "":
        new_date = target["date"]

    target["amount"] = new_amt
    target["category"] = new_cat
    target["description"] = new_desc
    target["date"] = new_date

    print(f"\n Expense #{target_id} updated successfully!")


def delete_expense(state):
    print_header("Delete Expense Entry")
    expenses = state["expenses"]

    if len(expenses) == 0:
        print("No expenses recorded to delete.")
        return

    view_all_expenses(state)
    target_id = get_valid_int("Enter ID # of expense to delete (0 to cancel): ", 0, state["next_id"])

    if target_id == 0:
        return

    found_idx = -1
    idx = 0
    for item in expenses:
        if item["id"] == target_id:
            found_idx = idx
            break
        idx = idx + 1

    if found_idx == -1:
        print(f"No expense found with ID #{target_id}.")
        return

    removed = expenses.pop(found_idx)
    print(f"\n Expense #{target_id} (${removed['amount']:.2f} - {removed['category']}) deleted successfully!")


def manage_data_menu(state):
    while True:
        print_header("Manage Records & Data")
        print("1. Edit Expense Record")
        print("2. Delete Single Expense Record")
        print("3. Clear ALL Expense Records")
        print("4. Back to Main Menu")

        choice = get_valid_int("Select option (1-4): ", 1, 4)

        if choice == 1:
            edit_expense(state)
        elif choice == 2:
            delete_expense(state)
        elif choice == 3:
            confirm = input("\n Are you SURE you want to clear ALL expenses? (type 'YES' to confirm): ")
            if confirm == "YES":
                state["expenses"] = []
                print(" All expense records wiped.")
            else:
                print("Operation cancelled.")
        elif choice == 4:
            break


def main():
    state = create_initial_state()
    
    running = True
    while running:
        print_header("Personal Expense Tracker")
        print(f" Active Account : [{state['active_account']}]")
        print(f" Total Logged   : {len(state['expenses'])} Records")
        print_divider()
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. Filter & Search Expenses")
        print("4. View Summary & Financial Analytics")
        print("5. Manage Budgets & Alerts")
        print("6. Manage Accounts")
        print("7. Edit / Delete Expense Records")
        print("8. Exit Application")
        print_divider()

        choice = get_valid_int("Select option (1-8): ", 1, 8)

        if choice == 1:
            add_expense(state)
        elif choice == 2:
            view_all_expenses(state)
        elif choice == 3:
            filter_menu(state)
        elif choice == 4:
            show_overall_summary(state)
        elif choice == 5:
            manage_budgets(state)
        elif choice == 6:
            manage_accounts(state)
        elif choice == 7:
            manage_data_menu(state)
        elif choice == 8:
            print("\n")
            print("   Thank you for using Expense Tracker! Goodbye.")
            print("\n")
            running = False


main()
