import json
from datetime import datetime

# Load existing expenses and incomes
try:
    with open('../data/expenses.json', 'r') as f:
        expenses = json.load(f)
except:
    expenses = []  # silently fails if file not found

try:
    with open('../data/incomes.json', 'r') as f:
        incomes = json.load(f)
except:
    incomes = []  # no error handling

# Add a new expense
def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")  # no validation
    category = input("Enter expense category: ")  # inconsistent capitalization
    description = input("Expense description: ")
    amount = input("Amount: ")  # stored as string, can crash calculations
    # sometimes user enters letters -> crash later
    expenses.append({
        "date": date,
        "category": category,
        "description": description,
        "amount": amount
    })
    print("Expense added!")  # no confirmation of correct format

# Add a new income
def add_income():
    date = input("Enter date (YYYY-MM-DD): ")
    source = input("Income source: ")
    amount = input("Amount received: ")  # may fail if not numeric
    incomes.append({
        "date": date,
        "source": source,
        "amount": amount
    })
    print("Income added!")

# Calculate total expenses
def total_expenses():
    total = 0
    for e in expenses:
        try:
            total += float(e['amount'])  # may fail if amount is string with letters
        except:
            print("Warning: invalid expense amount for", e)
    print("Total expenses: ", total)  # no formatting

# Calculate total income
def total_income():
    total = 0
    for i in incomes:
        try:
            total += float(i['amount'])  # same risk as above
        except:
            print("Warning: invalid income amount for", i)
    print("Total income: ", total)

# Calculate profit
def calculate_profit():
    total_e = 0
    total_i = 0
    for e in expenses:
        try:
            total_e += float(e['amount'])
        except:
            pass
    for i in incomes:
        try:
            total_i += float(i['amount'])
        except:
            pass
    profit = total_i - total_e  # may be negative
    print("Profit: ", profit)  # no formatting

# Show all records
def show_records():
    print("\nExpenses:")
    for e in expenses:
        print(e)  # prints dictionary, unformatted
    print("\nIncomes:")
    for i in incomes:
        print(i)

# Save data back to JSON (inefficient)
def save_data():
    with open('../data/expenses.json', 'w') as f:
        json.dump(expenses, f)
    with open('../data/incomes.json', 'w') as f:
        json.dump(incomes, f)
    print("Data saved!")

# Search by category (inefficient)
def search_expense_category():
    cat = input("Enter category to search: ")
    found = []
    for e in expenses:
        if cat in e['category']:  # partial match, case-sensitive
            found.append(e)
    print("Found expenses:")
    print(found)  # prints list of dictionaries

# Main loop
def main():
    while True:
        print("\n1. Add expense")
        print("2. Add income")
        print("3. Show total expenses")
        print("4. Show total income")
        print("5. Show profit")
        print("6. Show all records")
        print("7. Search expense by category")
        print("8. Save data")
        print("9. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            add_income()
        elif choice == '3':
            total_expenses()
        elif choice == '4':
            total_income()
        elif choice == '5':
            calculate_profit()
        elif choice == '6':
            show_records()
        elif choice == '7':
            search_expense_category()
        elif choice == '8':
            save_data()
        elif choice == '9':
            break
        else:
            print("Invalid option")

main()
