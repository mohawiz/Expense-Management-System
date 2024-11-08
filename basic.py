import csv
import calendar
import datetime
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# ... (existing functions remain unchanged)

# Generate comparative analysis report
def generate_comparative_analysis(csv_file, month1, year1, month2, year2):
    expenses1 = {}
    expenses2 = {}
    
    # Read data for the first month
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            expense_date = datetime.datetime.strptime(row['date'], '%Y-%m-%d')
            if expense_date.month == month1 and expense_date.year == year1:
                category = row['category']
                amount = float(row['amount'])
                if category in expenses1:
                    expenses1[category] += amount
                else:
                    expenses1[category] = amount

    # Read data for the second month
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            expense_date = datetime.datetime.strptime(row['date'], '%Y-%m-%d')
            if expense_date.month == month2 and expense_date.year == year2:
                category = row['category']
                amount = float(row['amount'])
                if category in expenses2:
                    expenses2[category] += amount
                else:
                    expenses2[category] = amount

    # Generate comparative analysis
    print(f"Comparative Analysis between {calendar.month_name[month1]} {year1} and {calendar.month_name[month2]} {year2}:")
    print(f"{'Category':<20}{calendar.month_name[month1]:<15}{calendar.month_name[month2]:<15}")
    for category in set(expenses1.keys()).union(expenses2.keys()):
        amount1 = expenses1.get(category, 0)
        amount2 = expenses2.get(category, 0)
        print(f"{category:<20}{amount1:<15}${amount2:<15}")

# Predict future expenses based on historical data
def predict_future_expenses(csv_file):
    monthly_expenses = {}
    
    # Read all expenses and organize by month
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            expense_date = datetime.datetime.strptime(row['date'], '%Y-%m-%d')
            month_year = (expense_date.year, expense_date.month)
            amount = float(row['amount'])
            if month_year in monthly_expenses:
                monthly_expenses[month_year] += amount
            else:
                monthly_expenses[month_year] = amount

    # Prepare data for prediction
    months = np.array(list(monthly_expenses.keys()))
    amounts = np.array(list(monthly_expenses.values()))
    
    # Convert months into a numeric format for regression
    X = np.array([(year * 12 + month) for year, month in months]).reshape(-1, 1)
    y = amounts

    # Train linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict future expense for next month
    next_month = (months[-1][0] * 12 + months[-1][1]) + 1  # Next month in numeric format
    predicted_amount = model.predict([[next_month]])

    print(f"Predicted expenses for next month: ${predicted_amount[0]:.2f}")

# Main function to run the expense tracker
def main():
    print("Welcome to the Enhanced Expense Tracker!")

    while True:
        print("\n1. Enter Expense Manually")
        print("2. Add Expense via Receipt Scan")
        print("3. Update an Expense")
        print("4. Delete an Expense")
        print("5. View Expenses")
        print("6. Generate Monthly Report")
        print("7. Generate Comparative Analysis")
        print("8. Predict Future Expenses")
        print("9. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            expense = get_user_expense()
            save_expense_to_csv(expense['name'], expense['category'], expense['amount'], str(datetime.datetime.now().date()))

        elif choice == '2':
            receipt_image = input("Enter the path to the receipt image: ")
            save_receipt_to_csv(receipt_image)

        elif choice == '3':
            expense_name = input("Enter the name of the expense you want to update: ")
            updated_category = input("Enter the new category: ")
            updated_amount = float(input("Enter the new amount: "))
            updated_date = input("Enter the new date (YYYY-MM-DD): ")
            update_expense_in_csv(expense_name, updated_category, updated_amount, updated_date)

        elif choice == '4':
            filter_type = input("Delete by (name/category/date)? ")
            if filter_type == 'name':
                expense_name = input("Enter the expense name to delete: ")
                delete_expense_from_csv(expense_name=expense_name)
            elif filter_type == 'category':
                category = input("Enter the category to delete: ")
                delete_expense_from_csv(category=category)
            elif filter_type == 'date':
                date = input("Enter the date (YYYY-MM-DD) to delete: ")
                delete_expense_from_csv(date=date)

        elif choice == '5':
            filter_type = input("View by (name/category/date/all)? ")
            if filter_type == 'name':
                expense_name = input("Enter the expense name to view: ")
                view_expenses('expenses.csv', filter_by='name', filter_value=expense_name)
            elif filter_type == 'category':
                category = input("Enter the category to view: ")
                view_expenses('expenses.csv', filter_by='category', filter_value=category)
            elif filter_type == 'date':
                date = input("Enter the date (YYYY-MM-DD) to view: ")
                view_expenses('expenses.csv', filter_by='date', filter_value=date)
            else:
                view_expenses('expenses.csv')

        elif choice == '6':
            month = int(input("Enter month (MM): "))
            year = int(input("Enter year (YYYY): "))
            generate_monthly_report('expenses.csv', month, year)

        elif choice == '7':
            month1 = int(input("Enter first month (MM): "))
            year1 = int(input("Enter first year (YYYY): "))
            month2 = int(input("Enter second month (MM): "))
            year2 = int(input("Enter second year (YYYY): "))
            generate_comparative_analysis('expenses.csv', month1, year1, month2, year2)

        elif choice == '8':
            predict_future_expenses('expenses.csv')

        elif choice == '9':
            print("Exiting the Expense Tracker.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
