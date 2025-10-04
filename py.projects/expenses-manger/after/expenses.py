import json
from datetime import datetime
from collections import defaultdict

# File paths
EXPENSE_FILE = '../data/expenses.json'
INCOME_FILE = '../data/incomes.json'

# Load data with proper error handling
def load_json(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

expenses = load_json(EXPENSE_FILE)
incomes = load_json(INCOME_FILE)

# Save data to JSON
def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Validate float input
def get_float(prompt):
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Invalid input. Please enter a number.")

# Validate date input
def get_date(prompt):
    while True:
        date_str = input(prompt)
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")

# Standardize category names
def standardize_category(category):
    return category.strip().title()

# Add new expense
def add_expense():
    date = get_date("Enter date (YYYY-MM-DD): ")
    category = standardize_category(input("Enter expense category: "))
    description = input("Expense description: ").strip()
    amount = get_float("Amount: ")

    expenses.append({
        "date": date,
        "category": category,
        "description": description,
        "amount": amount
    })
    print(f"Expense added: {description}, ${amount} under {category}")

# Add new income
def add_income():
    date = get_date("Enter date (YYYY-MM-DD): ")
    source = input("Income source: ").strip()
    amount = get_float("Amount received: ")

    incomes.append({
        "date": date,
        "source": source,
        "amount": amount
    })
    print(f"Income added: {source}, ${amount}")

# Calculate totals
def calculate_total(data):
    return sum(item['amount'] for item in data)

# Display all records nicely
def display_records(records, record_type):
    print(f"\n{'='*10} {record_type} {'='*10}")
    for r in records:
        print(f"{r['date']} | {r.get('category', r.get('source'))} | {r.get('description','')} | ${r['amount']:.2f}")
    print(f"{'='*30}\n")

# Show totals and profit
def show_summary():
    total_e = calculate_total(expenses)
    total_i = calculate_total(incomes)
    profit = total_i - total_e
    print(f"Total Expenses: ${total_e:.2f}")
    print(f"Total Income:   ${total_i:.2f}")
    print(f"Net Profit:     ${profit:.2f}")

# Show summary by category
def summary_by_category():
    category_totals = defaultdict(float)
    for e in expenses:
        category_totals[e['category']] += e['amount']

    print("\nExpenses by Category:")
    for cat, amt in category_totals.items():
        print(f"{cat}: ${amt:.2f}")

# Show monthly summary
def summary_by_month():
    month_totals = defaultdict(lambda: {'income': 0, 'expense':0})
    for e in expenses:
        month = e['date'][:7]  # YYYY-MM
        month_totals[month]['expense'] += e['amount']
    for i in incomes:
        month = i['date'][:7]
        month_totals[month]['income'] += i['amount']

    print("\nMonthly Summary:")
    for month, data in sorted(month_totals.items()):
        profit = data['income'] - data['expense']
        print(f"{month} | Income: ${data['income']:.2f} | Expenses: ${data['expense']:.2f} | Profit: ${profit:.2f}")

# Search expenses by category
def search_expense_category():
    cat = standardize_category(input("Enter category to search: "))
    results = [e for e in expenses if e['category'] == cat]
    display_records(results, f"Expenses in {cat}")

# Main menu
def main():
    while True:
        print("\n1. Add Expense")
        print("2. Add Income")
        print("3. Show All Records")
        print("4. Show Totals and Profit")
        print("5. Show Expenses by Category")
        print("6. Show Monthly Summary")
        print("7. Save Data")
        print("8. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            add_income()
        elif choice == '3':
            display_records(expenses, "Expenses")
            display_records(incomes, "Incomes")
        elif choice == '4':
            show_summary()
        elif choice == '5':
            summary_by_category()
        elif choice == '6':
            summary_by_month()
        elif choice == '7':
            save_json(EXPENSE_FILE, expenses)
            save_json(INCOME_FILE, incomes)
            print("Data saved successfully!")
        elif choice == '8':
            save_json(EXPENSE_FILE, expenses)
            save_json(INCOME_FILE, incomes)
            print("Exiting... Data saved.")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
