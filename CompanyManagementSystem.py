import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta



class CompanyManagementSystem:
    def __init__(self):

        self.db_connection = sqlite3.connect('company_database.db')
        self.create_tables()
        self.add_first_administrator()
        self.initialize_annual_leave_lists()

    def create_tables(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS administrators (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                leave_balance INTEGER DEFAULT 30,
                salary INTEGER DEFAULT 0,
                grievances TEXT DEFAULT ''

            )
        ''')
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS annual_leave_lists ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'year INTEGER NOT NULL, '
            'leave_start DATE NOT NULL, '
            'leave_end DATE NOT NULL, '
            'description TEXT);'
            '')
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS leave_applications (
                        leave_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        emp_id INTEGER NOT NULL,
                        leave_type TEXT NOT NULL,
                        start_date DATETIME NOT NULL,
                        end_date DATETIME NOT NULL,
                        status TEXT DEFAULT 'Pending',
                        FOREIGN KEY (emp_id) REFERENCES employees(id)
                    )
                ''')

        self.db_connection.commit()

    def initialize_annual_leave_lists(self):
        cursor = self.db_connection.cursor()

        try:
            # Create the table if it does not exist
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS annual_leave_lists (id INTEGER PRIMARY KEY AUTOINCREMENT, year INTEGER NOT NULL, leave_start DATE NOT NULL, leave_end DATE NOT NULL, description TEXT);')

            # Check if the table is empty
            cursor.execute('SELECT COUNT(*) FROM annual_leave_lists')
            count = cursor.fetchone()[0]

            if count == 0:
                # Insert sample data only if it's empty
                cursor.executemany('''
                        INSERT INTO annual_leave_lists (year, leave_start, leave_end, description)
                        VALUES (?, ?, ?, ?)
                    ''', [
                    (2023, '2023-12-25', '2023-12-31', 'Christmas Holiday'),
                    (2023, '2023-07-01', '2023-07-07', 'Summer Vacation')
                ])

                self.db_connection.commit()
                print("Annual leave lists initialized successfully.")
            else:
                print("Annual leave lists table already contains data.")
        except Exception as e:
            print(f"Error initializing annual leave lists: {e}")

    def add_first_administrator(self):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM administrators')
        admin_count = cursor.fetchone()[0]

        if admin_count == 0:
            admin_username = input("Enter the first Administrator username: ")
            admin_password = input("Enter the first Administrator password: ")
            cursor.execute('INSERT INTO administrators (username, password) VALUES (?, ?)',
                           (admin_username, admin_password))
            self.db_connection.commit()
            print(f"Administrator '{admin_username}' added successfully.")


if __name__ == "__main__":
    cms = CompanyManagementSystem()
