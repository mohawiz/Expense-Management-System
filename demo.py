from expense import Expense
import calendar
import datetime
import os
import csv
from ocr_receipt_parser import parse_receipt  # Add a module to handle receipt OCR
import matplotlib.pyplot as plt

def main():
    print(f"Running Expense Tracker!")
    expense_file_path = "expenses.csv"

    # Ensure the CSV file exists
    if not os.path.exists(expense_file_path):
        with open(expense_file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Amount', 'Category', 'Date'])

    # Get user input for total budget
    total_budget = float(input("Enter your total budget for the month: "))

    # Offer two input methods
    input_method = input("Would you like to (1) Manually input expense or (2) Scan a receipt? Enter 1 or 2: ")

    if input_method == '1':
        expense = get_user_expense()
    elif input_method == '2':
        receipt_file = input("Enter the path to the receipt image: ")
        expense = get_receipt_expense(receipt_file)
    else:
        print("Invalid input method. Exiting.")
        return

    # Save the expense to a file.
    save_expense_to_file(expense, expense_file_path)

    # Summarize expenses.
    summarize_expenses(expense_file_path, total_budget)

def get_user_expense():
    print(f"Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    expense_date = input("Enter the date (YYYY-MM-DD): ")
    
    expense_categories = [
        "Food",
        "Home",
        "Work",
        "Fun",
        "Misc"
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f" {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, 
                category=selected_category, 
                amount=expense_amount,
                date=expense_date  # Adding date information
            )
            return new_expense
        else:
            print("Invalid category. Please try again!")

def get_receipt_expense(receipt_file_path):
    """Use OCR to extract expense information from a receipt."""
    print(f"Processing receipt: {receipt_file_path}")
    expense_data = parse_receipt(receipt_file_path)  # Call OCR function to extract data
    if expense_data:
        return Expense(
            name=expense_data['name'],
            amount=expense_data['amount'],
            category=expense_data['category'],
            date=expense_data['date']
        )
    else:
        print("Error processing the receipt.")
        return None

def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([expense.name, expense.amount, expense.category, expense.date])

def summarize_expenses(expense_file_path, total_budget):
    print(f"Summarizing User Expense")
    expenses = []
    
    with open(expense_file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            expenses.append(
                Expense(name=row['Name'], amount=float(row['Amount']), category=row['Category'], date=row['Date'])
            )

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        amount_by_category[key] = amount_by_category.get(key, 0) + expense.amount

    # Show expenses by category
    print("Expenses By Category :")
    for key, amount in amount_by_category.items():
        print(f" {key}: ${amount:.2f}")

    total_spent = sum([x.amount for x in expenses])
    print(f"Total Spent: ${total_spent:.2f}")

    remaining_budget = total_budget - total_spent
    print(f"Budget Remaining: ${remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    if remaining_days > 0:
        daily_budget = remaining_budget / remaining_days
        print(green(f"Budget Per Day: ${daily_budget:.2f}"))
    else:
        print(f"No remaining days in this month.")

    # Generate Report and Analysis
    generate_report(expenses, total_budget)

def generate_report(expenses, total_budget):
    """Generates a monthly report with visualizations and insights."""
    amount_by_category = {}
    for expense in expenses:
        amount_by_category[expense.category] = amount_by_category.get(expense.category, 0) + expense.amount

    # Plot a bar chart of expenses by category
    categories = list(amount_by_category.keys())
    amounts = list(amount_by_category.values())

    plt.bar(categories, amounts)
    plt.xlabel("Category")
    plt.ylabel("Amount Spent")
    plt.title("Expenses by Category")
    plt.savefig("monthly_expense_report.png")
    print("Monthly expense report saved as 'monthly_expense_report.png'.")

def green(text):
    return f"\033[92m{text}\033[0m"

if __name__ == "__main__":
    main()
