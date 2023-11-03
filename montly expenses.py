# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 19:22:47 2023

@author: SHIRISHA
"""

import sqlite3
import calendar

def create_database():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        date TEXT,
        category TEXT,
        description TEXT,
        amount REAL
    )
    ''')

    conn.commit()
    conn.close()

def add_expense(date, category, description, amount):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO expenses (date, category, description, amount)
    VALUES (?, ?, ?, ?)
    ''', (date, category, description, amount))

    conn.commit()
    conn.close()

def view_expenses():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()

    for expense in expenses:
        print(expense)

    conn.close()

def delete_expense(expense_id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))

    conn.commit()
    conn.close()

def generate_monthly_report(year, month):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    start_date = f'{year}-{month:02d}-01'
    end_date = f'{year}-{month:02d}-{calendar.monthrange(year, month)[1]}'

    cursor.execute('''
    SELECT category, SUM(amount)
    FROM expenses
    WHERE date >= ? AND date <= ?
    GROUP BY category
    ''', (start_date, end_date))

    report_data = cursor.fetchall()

    conn.close()

    return report_data

def main():
    create_database()

    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Generate Monthly Report")
        print("5. Exit")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == '1':
            date = input("Date (YYYY-MM-DD): ")
            category = input("Category: ")
            description = input("Description: ")
            amount = float(input("Amount: "))
            add_expense(date, category, description, amount)
            print("Expense added.")

        elif choice == '2':
            print("\nExpenses:")
            view_expenses()

        elif choice == '3':
            expense_id = int(input("Enter the ID of the expense to delete: "))
            delete_expense(expense_id)
            print(f"Expense with ID {expense_id} deleted.")

        elif choice == '4':
            year = int(input("Enter the year (YYYY): "))
            month = int(input("Enter the month (1-12): "))
            report_data = generate_monthly_report(year, month)
            print(f"Monthly Report for {calendar.month_name[month]} {year}:")
            for category, total_amount in report_data:
                print(f"{category}: ${total_amount:.2f}")

        elif choice == '5':
            print("Goodbye!")
            break

if __name__ == '__main__':
    main()
