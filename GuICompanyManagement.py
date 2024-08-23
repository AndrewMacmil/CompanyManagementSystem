import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta


class CompanyManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Company Management System")
        self.root.geometry("600x300")
        self.root.configure(bg='#333')  # Set background color to dark

        # Connect to the database
        self.db_connection = sqlite3.connect('company_database.db')
        self.current_user = None

        # buttons with updated styles
        button_style = {
            'bg': '#8BC34A',  # Light green color
            'fg': '#333',  # Dark text color
            'border': 0,  # No border
            'padx': 10,
            'pady': 5,
            'font': ('Arial', 12),
        }

        self.Label = tk.Label(root, text="LOGIN WINDOW", fg="white", bg='#333', font=('Arial', 16))
        self.Label.pack(pady=10)

        self.admin_button = tk.Button(root, text="Administrator Login", command=self.admin_login, **button_style)
        self.admin_button.pack(pady=10)

        self.employee_button = tk.Button(root, text="Employee Login", command=self.employee_login, **button_style)
        self.employee_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", command=self.root.destroy, **button_style)
        self.exit_button.pack(pady=10)

    def admin_login(self):
        admin_window = tk.Toplevel(self.root)
        admin_window.title("Administrator Login")

        # widgets for username and password
        username_label = tk.Label(admin_window, text="Username:")
        username_label.grid(row=0, column=0, pady=10)

        username_entry = tk.Entry(admin_window)
        username_entry.grid(row=0, column=1, pady=10)

        password_label = tk.Label(admin_window, text="Password:")
        password_label.grid(row=1, column=0, pady=10)

        password_entry = tk.Entry(admin_window, show="*")
        password_entry.grid(row=1, column=1, pady=10)

        # login button
        login_button = tk.Button(admin_window, text="Login",
                                 command=lambda: self.admin_login_handler(admin_window, username_entry.get(),
                                                                          password_entry.get()))
        login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def admin_login_handler(self, admin_window, username, password):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM administrators WHERE username=? AND password=?', (username, password))
        admin_data = cursor.fetchone()

        if admin_data:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!\nYou are logged in as an Administrator.")
            admin_window.destroy()
            self.current_user = {'username': username, 'role': 'admin'}
            self.admin_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password for Administrator.")

    def admin_menu(self):
        admin_menu_window = tk.Toplevel(self.root)
        admin_menu_window.title("Administrator Menu")

        # Create buttons for each menu option
        add_employee_button = tk.Button(admin_menu_window, text="Add Employee", command=self.add_employee)
        add_employee_button.pack(pady=10)

        modify_employee_button = tk.Button(admin_menu_window, text="Modify Employee Details",
                                           command=self.modify_employee_details)
        modify_employee_button.pack(pady=10)

        leave_management_button = tk.Button(admin_menu_window, text="Leave Management", command=self.leave_management)
        leave_management_button.pack(pady=10)

        view_all_employees_button = tk.Button(admin_menu_window, text="View All Employees",
                                              command=self.view_all_employees)
        view_all_employees_button.pack(pady=10)

        exit_button = tk.Button(admin_menu_window, text="Exit", command=admin_menu_window.destroy)
        exit_button.pack(pady=10)

    def add_employee(self):
        add_employee_window = tk.Toplevel(self.root)
        add_employee_window.title("Add Employee")

        # widgets for employee details
        name_label = tk.Label(add_employee_window, text="Name:")
        name_label.grid(row=0, column=0, pady=10)

        name_entry = tk.Entry(add_employee_window)
        name_entry.grid(row=0, column=1, pady=10)

        password_label = tk.Label(add_employee_window, text="Password:")
        password_label.grid(row=1, column=0, pady=10)

        password_entry = tk.Entry(add_employee_window, show="*")
        password_entry.grid(row=1, column=1, pady=10)

        salary_label = tk.Label(add_employee_window, text="Salary:")
        salary_label.grid(row=2, column=0, pady=10)

        salary_entry = tk.Entry(add_employee_window)
        salary_entry.grid(row=2, column=1, pady=10)

        # add employee button
        add_button = tk.Button(add_employee_window, text="Add Employee",
                               command=lambda: self.add_employee_handler(add_employee_window, name_entry.get(),
                                                                         password_entry.get(), salary_entry.get()))
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

    def add_employee_handler(self, add_employee_window, name, password, salary):
        cursor = self.db_connection.cursor()
        cursor.execute('INSERT INTO employees (name, password, salary) VALUES (?, ?, ?)', (name, password, salary))
        self.db_connection.commit()
        messagebox.showinfo("Employee Added", f"Employee {name} added successfully!")
        add_employee_window.destroy()

    def view_all_employees(self):
        view_all_employees_window = tk.Toplevel(self.root)
        view_all_employees_window.title("Employees")

        # widget to display all employees
        all_employees_tree = ttk.Treeview(view_all_employees_window, columns=('Employee ID', 'Name', 'Salary',
                                                                              'Leave Balance', 'Grievances'))
        all_employees_tree.heading('Employee ID', text='Employee ID')
        all_employees_tree.heading('Name', text='Name')
        all_employees_tree.heading('Salary', text='Salary')
        all_employees_tree.heading('Leave Balance', text='Leave Balance')
        all_employees_tree.heading('Grievances', text='Grievances')

        all_employees_tree.pack(pady=10)

        # Fetch all employees from the database
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT id, name, salary, leave_balance, grievances FROM employees')
        all_employees_data = cursor.fetchall()

        # Insert employee data into the treeview
        for emp in all_employees_data:
            try:
                all_employees_tree.insert('', 'end', values=(emp[0], emp[1], emp[2], emp[3], emp[4]))
            except IndexError as e:
                print(f"Error processing employee data: {e}")

    def modify_employee_details(self):
        modify_employee_window = tk.Toplevel(self.root)
        modify_employee_window.title("Modify Employee Details")

        # entry widgets for employee ID and new details
        id_label = tk.Label(modify_employee_window, text="Employee ID:")
        id_label.grid(row=0, column=0, pady=10)

        id_entry = tk.Entry(modify_employee_window)
        id_entry.grid(row=0, column=1, pady=10)

        name_label = tk.Label(modify_employee_window, text="New Name:")
        name_label.grid(row=1, column=0, pady=10)

        name_entry = tk.Entry(modify_employee_window)
        name_entry.grid(row=1, column=1, pady=10)

        password_label = tk.Label(modify_employee_window, text="New Password:")
        password_label.grid(row=2, column=0, pady=10)

        password_entry = tk.Entry(modify_employee_window, show="*")
        password_entry.grid(row=2, column=1, pady=10)

        salary_label = tk.Label(modify_employee_window, text="New Salary:")
        salary_label.grid(row=3, column=0, pady=10)

        salary_entry = tk.Entry(modify_employee_window)
        salary_entry.grid(row=3, column=1, pady=10)

        # modify employee button
        modify_button = tk.Button(modify_employee_window, text="Modify Employee",
                                  command=lambda: self.modify_employee_handler(id_entry.get(), name_entry.get(),
                                                                               password_entry.get(),
                                                                               salary_entry.get()))
        modify_button.grid(row=4, column=0, columnspan=2, pady=10)

    def modify_employee_handler(self, emp_id, new_name, new_password, new_salary):
        cursor = self.db_connection.cursor()
        cursor.execute('UPDATE employees SET name=?, password=?, salary=? WHERE id=?',
                       (new_name, new_password, new_salary, emp_id))
        self.db_connection.commit()
        messagebox.showinfo("Employee Modified", f"Employee with ID {emp_id} modified successfully!")

    def leave_management(self):
        self.leave_management_window = tk.Toplevel(self.root)
        self.leave_management_window.title("Leave Management")

        # Treeview widget to display leave requests
        leave_tree = ttk.Treeview(self.leave_management_window,
                                  columns=('Leave ID', 'Employee ID', 'Leave Type', 'Start Date', 'End Date', 'Status'))
        leave_tree.heading('#0', text='Leave ID')
        leave_tree.heading('Leave ID', text='Leave ID')
        leave_tree.heading('Employee ID', text='Employee ID')
        leave_tree.heading('Leave Type', text='Leave Type')
        leave_tree.heading('Start Date', text='Start Date')
        leave_tree.heading('End Date', text='End Date')
        leave_tree.heading('Status', text='Status')

        leave_tree.pack(pady=10)

        # Fetch leave requests from the database
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM leave_applications')
        leave_requests = cursor.fetchall()

        # Insert leave requests into the treeview
        for leave_request in leave_requests:
            try:
                leave_tree.insert('', 'end', text=leave_request[0], values=(
                    leave_request[0], leave_request[1], leave_request[2], leave_request[3], leave_request[4],
                    leave_request[5]))
            except IndexError as e:
                print(f"Error processing leave request: {e}")

        # Approve and reject buttons
        approve_button = tk.Button(self.leave_management_window, text="Approve Leave",
                                   command=lambda: self.approve_leave(leave_tree))
        approve_button.pack(pady=10)

        reject_button = tk.Button(self.leave_management_window, text="Reject Leave",
                                  command=lambda: self.reject_leave(leave_tree))
        reject_button.pack(pady=10)

        # Button to delete selected leave applications
        delete_button = tk.Button(self.leave_management_window, text="Delete Selected Leave Applications",
                                  command=lambda: self.delete_leave_application(leave_tree))
        delete_button.pack(pady=10)

    def view_personal_details(self, emp_id):
        # personal details from the database
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM employees WHERE id=?', (emp_id,))
        emp_data = cursor.fetchone()

        if emp_data:
            # new window to display personal details using Treeview
            personal_details_window = tk.Toplevel(self.root)
            personal_details_window.title("Personal Details")

            # Create a Treeview widget
            personal_details_tree = ttk.Treeview(personal_details_window, columns=('Attribute', 'Value'))
            personal_details_tree.heading('#0', text='Attribute')
            personal_details_tree.heading('Attribute', text='Attribute')
            personal_details_tree.heading('Value', text='Value')

            # Insert personal details into the Treeview
            attributes = ['Employee ID', 'Name', 'Password', 'Leave Balance', 'Salary', 'Grievances']
            for attr, value in zip(attributes, emp_data):
                personal_details_tree.insert('', 'end', text=attr, values=(value,))

            personal_details_tree.pack(pady=10)

            # Add a button to delete the grievance
            delete_grievance_button = tk.Button(personal_details_window, text="Delete Grievance",
                                                command=lambda: self.delete_grievance(emp_id))
            delete_grievance_button.pack(pady=10)
        else:
            messagebox.showerror("Error", "Failed to retrieve personal details.")

    def delete_grievance(self, emp_id):
        cursor = self.db_connection.cursor()
        cursor.execute('UPDATE employees SET grievances=NULL WHERE id=?', (emp_id,))
        self.db_connection.commit()
        messagebox.showinfo("Grievance Deleted", "Your grievance has been deleted successfully!")

    def delete_leave_application(self, leave_tree):
        selected_items = leave_tree.selection()

        if selected_items:
            for selected_item in selected_items:
                leave_id = leave_tree.item(selected_item, 'text')
                cursor = self.db_connection.cursor()
                cursor.execute('DELETE FROM leave_applications WHERE leave_id=?', (leave_id,))
                self.db_connection.commit()
                leave_tree.delete(selected_item)
            messagebox.showinfo("Leave Deleted", "Selected leave application(s) deleted successfully.")
        else:
            messagebox.showwarning("Select Leave Application",
                                   "Please select one or more leave applications to delete.")

    def approve_leave(self, leave_tree):
        selected_item = leave_tree.selection()

        if selected_item:
            leave_id = leave_tree.item(selected_item, 'text')
            cursor = self.db_connection.cursor()

            # Fetch leave application details
            cursor.execute('SELECT emp_id, start_date, end_date FROM leave_applications WHERE leave_id=?', (leave_id,))
            leave_data = cursor.fetchone()

            if leave_data:
                emp_id, start_date_str, end_date_str = leave_data

                # Convert date strings to datetime objects
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S.%f")
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S.%f")

                # Calculate leave_days
                leave_days = (end_date - start_date).days + 1

                # Fetch current leave balance
                cursor.execute('SELECT leave_balance FROM employees WHERE id=?', (emp_id,))
                current_leave_balance = cursor.fetchone()[0]

                # Check if approving the leave request exceeds leave balance
                if leave_days <= current_leave_balance:
                    # Update leave balance in the database
                    new_leave_balance = current_leave_balance - leave_days
                    cursor.execute('UPDATE employees SET leave_balance=? WHERE id=?', (new_leave_balance, emp_id))
                    self.db_connection.commit()

                    # Update leave application status
                    cursor.execute('UPDATE leave_applications SET status="Approved" WHERE leave_id=?', (leave_id,))
                    self.db_connection.commit()

                    messagebox.showinfo("Leave Approved", f"Leave request ID {leave_id} approved successfully.")
                    self.close_window()

                else:
                    messagebox.showerror("Insufficient Leave Balance",
                                         "Approving this leave request would exceed the leave balance.")
                    self.close_window()
            else:
                messagebox.showerror("Error", f"Failed to retrieve leave details for leave request ID {leave_id}.")
                self.close_window()
        else:
            messagebox.showwarning("Select Leave Request", "Please select a leave request to approve.")
            self.close_window()

    def close_window(self):
        # Assuming `self.root` is the Tkinter root window
        self.leave_management_window.destroy()

    def reject_leave(self, leave_tree):
        selected_item = leave_tree.selection()

        if selected_item:
            leave_id = leave_tree.item(selected_item, 'text')
            cursor = self.db_connection.cursor()
            cursor.execute('UPDATE leave_applications SET status="Rejected" WHERE leave_id=?', (leave_id,))
            self.db_connection.commit()
            messagebox.showinfo("Leave Rejected", f"Leave request ID {leave_id} rejected.")
            # Refresh the leave requests in the treeview after rejection
            self.leave_management()
        else:
            messagebox.showwarning("Select Leave Request", "Please select a leave request to reject.")

    def employee_login(self):
        employee_window = tk.Toplevel(self.root)
        employee_window.title("Employee Login")

        # Create entry widgets for employee ID, name, and password
        id_label = tk.Label(employee_window, text="Employee ID:")
        id_label.grid(row=0, column=0, pady=10)

        id_entry = tk.Entry(employee_window)
        id_entry.grid(row=0, column=1, pady=10)

        name_label = tk.Label(employee_window, text="Name:")
        name_label.grid(row=1, column=0, pady=10)

        name_entry = tk.Entry(employee_window)
        name_entry.grid(row=1, column=1, pady=10)

        password_label = tk.Label(employee_window, text="Password:")
        password_label.grid(row=2, column=0, pady=10)

        password_entry = tk.Entry(employee_window, show="*")
        password_entry.grid(row=2, column=1, pady=10)

        # Create login button
        login_button = tk.Button(employee_window, text="Login",
                                 command=lambda: self.employee_login_handler(employee_window, id_entry.get(),
                                                                             name_entry.get(), password_entry.get()))
        login_button.grid(row=3, column=0, columnspan=2, pady=10)

    def employee_login_handler(self, employee_window, emp_id, name, password):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM employees WHERE id=? AND name=? AND password=?', (emp_id, name, password))
        emp_data = cursor.fetchone()

        if emp_data:
            messagebox.showinfo("Login Successful", f"Welcome, Employee {name}!\nYou are logged in.")
            employee_window.destroy()
            self.current_user = {'emp_id': emp_id, 'username': name, 'role': 'employee'}
            self.employee_menu(emp_id, name, password)
        else:
            messagebox.showerror("Login Failed", "Invalid Employee name or password.")

    def employee_menu(self, emp_id, name, password):
        employee_menu_window = tk.Toplevel(self.root)
        employee_menu_window.title("Employee Menu")

        # Create buttons for each employee menu option
        view_details_button = tk.Button(employee_menu_window, text="View Personal Details",
                                        command=lambda: self.view_personal_details(emp_id))
        view_details_button.pack(pady=10)

        apply_leave_button = tk.Button(employee_menu_window, text="Apply for Leave", command=self.apply_for_leave)
        apply_leave_button.pack(pady=10)

        check_leave_status_button = tk.Button(employee_menu_window, text="Check Leave Status",
                                              command=self.check_leave_status)
        check_leave_status_button.pack(pady=10)

        check_annual_leave_list_button = tk.Button(employee_menu_window, text="Check Annual Leave List",
                                                   command=self.check_annual_leave_list)
        check_annual_leave_list_button.pack(pady=10)

        enter_grievance_button = tk.Button(employee_menu_window, text="Enter Grievance", command=self.enter_grievance)
        enter_grievance_button.pack(pady=10)

        resign_button = tk.Button(employee_menu_window, text="resign", command=self.resign)
        resign_button.pack(pady=10)

        sign_out_button = tk.Button(employee_menu_window, text="Sign Out", command=employee_menu_window.destroy)
        sign_out_button.pack(pady=10)

    def view_personal_details(self, emp_id):
        # Fetch personal details from the database
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM employees WHERE id=?', (emp_id,))
        emp_data = cursor.fetchone()

        if emp_data:
            # Create a new window to display personal details using Treeview
            personal_details_window = tk.Toplevel(self.root)
            personal_details_window.title("Personal Details")

            # Create a Treeview widget
            personal_details_tree = ttk.Treeview(personal_details_window, columns=('Attribute',))
            personal_details_tree.heading('#0', text='Attribute')
            personal_details_tree.heading('Attribute', text='Attribute')

            # Insert personal details into the Treeview
            attributes = ['Employee ID', 'Name', 'Password', 'Leave Balance', 'Salary', 'Grievances']
            for attr, value in zip(attributes, emp_data):
                personal_details_tree.insert('', 'end', text=attr, values=(value,))

            personal_details_tree.pack(pady=10)

            # Add a button to delete the grievance
            delete_grievance_button = tk.Button(personal_details_window, text="Delete Grievance",
                                                command=lambda: self.delete_grievance(emp_id))
            delete_grievance_button.pack(pady=10)
        else:
            messagebox.showerror("Error", "Failed to retrieve personal details.")

    def delete_grievance(self, emp_id):
        cursor = self.db_connection.cursor()
        cursor.execute('UPDATE employees SET grievances=NULL WHERE id=?', (emp_id,))
        self.db_connection.commit()
        messagebox.showinfo("Grievance Deleted", "Your grievance has been deleted successfully!")

    def apply_for_leave(self):
        leave_application_window = tk.Toplevel(self.root)
        leave_application_window.title("Leave Application Form")

        leave_type_label = tk.Label(leave_application_window, text="Leave Type:")
        leave_type_label.grid(row=0, column=0, pady=10)

        leave_type_entry = tk.Entry(leave_application_window)
        leave_type_entry.grid(row=0, column=1, pady=10)

        duration_label = tk.Label(leave_application_window, text="Duration (days):")
        duration_label.grid(row=1, column=0, pady=10)

        duration_entry = tk.Entry(leave_application_window)
        duration_entry.grid(row=1, column=1, pady=10)

        apply_button = tk.Button(leave_application_window, text="Apply",
                                 command=lambda: self.apply_leave(leave_type_entry.get(), duration_entry.get()))
        apply_button.grid(row=2, column=0, columnspan=2, pady=10)

    def apply_leave(self, leave_type, duration):
        emp_id = self.get_employee_id()

        if emp_id is not None:
            try:
                # Validate the input values
                if not leave_type or not duration.isdigit() or int(duration) <= 0:
                    raise ValueError("Invalid input. Please provide valid leave type and duration.")

                # Calculate the end date of the leave based on the current date and duration
                end_date = datetime.now() + timedelta(days=int(duration))

                # Insert leave application details into the database
                cursor = self.db_connection.cursor()
                cursor.execute(
                    'INSERT INTO leave_applications (emp_id, leave_type, start_date, end_date, status) VALUES (?, ?, '
                    '?, ?, ?)',
                    (emp_id, leave_type, datetime.now(), end_date, 'Pending')
                )
                self.db_connection.commit()

                # Provide feedback to the user
                messagebox.showinfo("Leave Application",
                                    f"Leave application submitted successfully!\nType: {leave_type}\nDuration: {duration} days")



            except ValueError as ve:
                messagebox.showerror("Error", str(ve))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply leave. Error: {e}")
        else:
            messagebox.showerror("Error", "Employee not found.")

    def get_employee_id(self):
        if self.current_user and self.current_user.get('role') == 'employee':
            cursor = self.db_connection.cursor()
            cursor.execute('SELECT id FROM employees WHERE name = ?', (self.current_user.get('username', ''),))
            employee_id = cursor.fetchone()

            if (employee_id is not None) and (len(employee_id) > 0):
                return employee_id[0]
            else:
                # Log the error or raise an exception
                print("Error: Employee not found in the database.")
                return None
        else:
            # Log the error or raise an exception
            print("Error: Invalid current_user or not an employee.")
            return None

    def check_leave_status(self):
        emp_id = self.get_employee_id()

        if emp_id is not None:
            # Fetch leave requests for the logged-in employee
            cursor = self.db_connection.cursor()
            cursor.execute('SELECT * FROM leave_applications WHERE emp_id=?', (emp_id,))
            leave_requests = cursor.fetchall()

            # Create a new window to display leave status
            leave_status_window = tk.Toplevel(self.root)
            leave_status_window.title("Leave Status")

            # Create a treeview widget to display leave requests
            leave_tree = ttk.Treeview(leave_status_window,
                                      columns=('Leave ID', 'Leave Type', 'Start Date', 'End Date', 'Status'))
            leave_tree.heading('#0', text='Leave ID')
            leave_tree.heading('Leave ID', text='Leave ID')
            leave_tree.heading('Leave Type', text='Leave Type')
            leave_tree.heading('Start Date', text='Start Date')
            leave_tree.heading('End Date', text='End Date')
            leave_tree.heading('Status', text='Status')

            leave_tree.pack(pady=10)

            # Insert leave requests into the treeview
            for leave_request in leave_requests:
                try:
                    leave_tree.insert('', 'end', text=leave_request[0], values=(
                        leave_request[0], leave_request[2], leave_request[3], leave_request[4], leave_request[5]))
                except IndexError as e:
                    # Handle the case where the leave_request tuple doesn't have enough elements
                    print(f"Error processing leave request: {e}")

        else:
            messagebox.showerror("Error", "Employee not found.")

    def check_annual_leave_list(self):
        # Fetch annual leave lists from the database
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM annual_leave_lists')
        annual_leave_lists = cursor.fetchall()

        # Create a new window to display the annual leave list
        annual_leave_window = tk.Toplevel(self.root)
        annual_leave_window.title("Annual Leave List")

        # Create a treeview widget to display annual leave lists
        annual_leave_tree = ttk.Treeview(annual_leave_window,
                                         columns=('Year', 'Leave Start', 'Leave End', 'Description'))
        annual_leave_tree.heading('#0', text='ID')
        annual_leave_tree.heading('Year', text='Year')
        annual_leave_tree.heading('Leave Start', text='Leave Start')
        annual_leave_tree.heading('Leave End', text='Leave End')
        annual_leave_tree.heading('Description', text='Description')

        annual_leave_tree.pack(pady=10)

        # Insert annual leave lists into the treeview
        for annual_leave in annual_leave_lists:
            try:
                annual_leave_tree.insert('', 'end', text=annual_leave[0], values=(
                    annual_leave[1], annual_leave[2], annual_leave[3], annual_leave[4]))
            except IndexError as e:
                # Handle the case where the annual_leave tuple doesn't have enough elements
                print(f"Error processing annual leave list: {e}")

    def enter_grievance(self):
        grievance_window = tk.Toplevel(self.root)
        grievance_window.title("Enter Grievance")

        grievance_label = tk.Label(grievance_window, text="Enter your grievance:")
        grievance_label.pack(pady=10)

        grievance_entry = tk.Entry(grievance_window, width=50)
        grievance_entry.pack(pady=10)

        submit_button = tk.Button(grievance_window, text="Submit",
                                  command=lambda: self.submit_grievance(grievance_entry.get()))
        submit_button.pack(pady=10)

    def submit_grievance(self, grievance_text):
        emp_id = self.get_employee_id()

        if emp_id is not None:
            # Insert grievance into the database
            cursor = self.db_connection.cursor()
            cursor.execute('UPDATE employees SET grievances=? WHERE id=?', (grievance_text, emp_id))
            self.db_connection.commit()

            messagebox.showinfo("Grievance Submitted", "Your grievance has been submitted successfully!")
        else:
            messagebox.showerror("Error", "Employee not found.")

    def resign(self):
        if self.current_user and self.current_user.get('role') == 'employee':
            emp_id = self.current_user.get('emp_id')
            confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to resign?")

            if confirmation:
                cursor = self.db_connection.cursor()
                cursor.execute('DELETE FROM employees WHERE id=?', (emp_id,))
                self.db_connection.commit()
                messagebox.showinfo("Resignation Successful", "Resignation successful. Thank you for your service.")

            else:
                messagebox.showinfo("Resignation Canceled", "Resignation canceled.")
        else:
            messagebox.showerror("Error", "Invalid current_user or not an employee.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CompanyManagementApp(root)
    root.mainloop()
