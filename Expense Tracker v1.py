#  Expense Tracker by Yug
#  A simple and friendly program to
#  track your money using a CSV file.
# ==================================

# We need a few tools (libraries) to make our program work.
import csv  # For reading and writing spreadsheet-like files.
import os   # To check if files exist on your computer.
import matplotlib.pyplot as plt # To cre
from datetime import datetime # To get the current date.

# --- Global ---
# We'll store all our data in this file.
DATA_FILE = 'transactions.csv'
# These are the column titles for our spreadsheet.
HEADERS = ['date', 'type', 'amount', 'category', 'description']

def initialize_file():
    """
    This function checks if our data file exists.
    If it doesn't, it creates a new one with the right headers.
    """
    if not os.path.exists(DATA_FILE):
        print("Welcome! It looks like this is your first time.")
        print(f"Creating a new file to store your data: '{DATA_FILE}'")
        # 'with open' is a safe way to work with files.
        with open(DATA_FILE, 'w', newline='') as f:
            # A 'writer' helps us write rows into the CSV file.
            writer = csv.writer(f)
            writer.writerow(HEADERS)

def read_transactions():
    """
    This function opens the CSV file and reads all the saved transactions.
    It returns everything as a list, which is easy to work with in Python.
    """
    try:
        with open(DATA_FILE, 'r', newline='') as f:
            # DictReader is cool because it lets us use column names (like 'amount').
            reader = csv.DictReader(f)
            transactions = list(reader)
            # The amount is read as text, so we convert it back to a number (float).
            for t in transactions:
                t['amount'] = float(t['amount'])
            return transactions
    except FileNotFoundError:
        # This happens if the file doesn't exist, but our initialize_file() should prevent this.
        return []
    except Exception as e:
        print(f"Oops! Something went wrong when reading the file: {e}")
        return []

def write_transaction(date, trans_type, amount, category, description):
    """
    This function adds a single, new transaction to the end of our CSV file.
    The 'a' in open(..., 'a') stands for 'append', which means "add to the end".
    """
    try:
        with open(DATA_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([date, trans_type, amount, category, description])
        return True # Return True to signal that it worked!
    except Exception as e:
        print(f"Oops! Could not save your transaction to the file: {e}")
        return False # Return False to signal that something went wrong.

def add_transaction():
    """
    This function handles the user interaction for adding a new transaction.
    It asks the user for all the details.
    """
    print("\n--- Let's Add a New Transaction! ---")
    try:
        # First, we ask if it's an expense or income.
        trans_type = input("Is this an 'Expense' or 'Income'?: ").capitalize()
        if trans_type not in ['Expense', 'Income']:
            print("\nWhoops! Please type either 'Expense' or 'Income'. Let's try again.")
            return

        # Then, we get the rest of the details.
        amount = float(input("How much was it? (₹): "))
        category = input("What category should this be? (e.g., Food, Salary, Travel): ")
        description = input("Enter a short note or description: ")
        # We get today's date and format it nicely.
        trans_date = datetime.now().strftime('%Y-%m-%d')

        # Now, we call our other function to write this data to the file.
        if write_transaction(trans_date, trans_type, amount, category, description):
            print("\nSuccess! Your transaction has been saved.")
        else:
            print("\nOh no! Something went wrong while saving.")

    except ValueError:
        # This 'except' block catches errors if the user types text for the amount.
        print("\nPlease enter a valid number for the amount (e.g., 500 or 29.99).")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

def view_transactions():
    """
    This function shows the user all their past transactions in a nicely formatted table.
    """
    print("\n--- Here is Your Transaction History ---")
    transactions = read_transactions()
    
    if not transactions:
        print("Your history is empty. Try adding a transaction first!")
    else:
        # It's nice to see the newest transactions first, so we sort the list by date.
        sorted_transactions = sorted(transactions, key=lambda x: x['date'], reverse=True)
        
        # Print a header for our table to make it look neat.
        print("-" * 90)
        print(f"{'Date':<12} | {'Type':<10} | {'Amount (₹)':<15} | {'Category':<20} | {'Description'}")
        print("-" * 90)
        
        # We loop through each transaction and print its details.
        for row in sorted_transactions:
            print(f"{row['date']:<12} | {row['type']:<10} | {row['amount']:<15.2f} | {row['category']:<20} | {row['description']}")
        print("-" * 90)

def generate_pie_chart():
    """
    This function creates and displays a pie chart of expenses.
    It shows you where your money is going!
    """
    print("\n--- Generating Your Expense Pie Chart ---")
    transactions = read_transactions()
    # We'll use a dictionary to keep track of the total for each category.
    expense_data = {}

    # We go through all transactions...
    for t in transactions:
        # ...but we only care about the 'Expense' ones for this chart.
        if t['type'] == 'Expense':
            category = t['category']
            amount = t['amount']
            # We add the amount to the category's total.
            expense_data[category] = expense_data.get(category, 0) + amount
    
    if not expense_data:
        print("No expense data found. Add some expenses to see a chart!")
        return

    # Now we get the labels (categories) and sizes (amounts) for our pie chart.
    categories = list(expense_data.keys())
    amounts = list(expense_data.values())

    # Time to draw the chart using matplotlib!
    plt.figure(figsize=(8, 8)) # Makes the chart window a nice size.
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('A Breakdown of Your Expenses by Category')
    print("\nDisplaying chart... Please close the chart window when you are done.")
    plt.show() # This command displays the chart on your screen.

def generate_bar_chart():
    """
    This function creates a bar chart to show how much you spend each day.
    """
    print("\n--- Generating Your Daily Spending Bar Chart ---")
    transactions = read_transactions()
    daily_expenses = {}

    # Loop through transactions to sum up expenses for each day.
    for t in transactions:
        if t['type'] == 'Expense':
            date = t['date']
            amount = t['amount']
            daily_expenses[date] = daily_expenses.get(date, 0) + amount
    
    if not daily_expenses:
        print("No expense data found. Add some expenses to see a chart!")
        return

    # We should sort the dates so the chart is in chronological order.
    sorted_dates = sorted(daily_expenses.keys())
    amounts = [daily_expenses[date] for date in sorted_dates]

    # Let's draw the bar chart.
    plt.figure(figsize=(10, 6))
    plt.bar(sorted_dates, amounts, color='skyblue')
    plt.xlabel('Date')
    plt.ylabel('Total Amount Spent (₹)')
    plt.title('Your Daily Expenses')
    plt.xticks(rotation=45, ha="right") # Rotates the date labels so they don't overlap.
    plt.tight_layout() # Fits everything neatly in the window.
    print("\nDisplaying chart... Please close the chart window when you are done.")
    plt.show()

def main_menu():
    """
    This is the heart of our program. It displays the menu and waits for the user's choice.
    It will loop forever until the user decides to exit.
    """
    # First, let's make sure our data file is ready.
    initialize_file()

    while True:
        # Print the menu options for the user.
        print("\n" + "="*10 + " Main Menu " + "="*10)
        print("Hello, Yug! What would you like to do?")
        print("1. Add a Transaction")
        print("2. View All Transactions")
        print("3. See Expense Pie Chart")
        print("4. See Daily Spending Bar Chart")
        print("5. Exit")
        print("="*31)
        
        choice = input("Enter your choice (1-5): ")
        
        # Based on the user's choice, we call the correct function.
        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            generate_pie_chart()
        elif choice == '4':
            generate_bar_chart()
        elif choice == '5':
            print("\nThank you for using the Expense Tracker. Have a great day!")
            break # This 'break' command stops the 'while' loop.
        else:
            print("\nHmm, that's not a valid choice. Please enter a number from 1 to 5.")
        
        # A little pause to let the user read the output before showing the menu again.
        input("\nPress Enter to return to the menu...")

# This is the official starting point of our Python script.
# When you run the file, this is the first line of code that actually runs.
if __name__ == "__main__":

    main_menu()

