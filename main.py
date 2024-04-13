import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

class ExpenseManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Manager")

        # Establish a database connection
        self.conn = sqlite3.connect('expenses_database.db')
        self.cursor = self.conn.cursor()

        # Create table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses
                               (name text, category text, amount real, date text)''')

        # Create frames
        self.entry_frame = tk.Frame(self.root, bg='sky blue')
        self.entry_frame.pack(fill='x')

        self.display_frame = tk.Frame(self.root, bg='light green')
        self.display_frame.pack(fill='x')

        # Add expense widgets
        self.name_label = tk.Label(self.entry_frame, text="Name", bg='sky blue')
        self.name_label.pack(side=tk.LEFT)
        self.name_entry = tk.Entry(self.entry_frame)
        self.name_entry.pack(side=tk.LEFT)

        self.category_label = tk.Label(self.entry_frame, text="Category", bg='sky blue')
        self.category_label.pack(side=tk.LEFT)
        self.category_entry = tk.Entry(self.entry_frame)
        self.category_entry.pack(side=tk.LEFT)

        self.amount_label = tk.Label(self.entry_frame, text="Amount", bg='sky blue')
        self.amount_label.pack(side=tk.LEFT)
        self.amount_entry = tk.Entry(self.entry_frame)
        self.amount_entry.pack(side=tk.LEFT)

        self.add_button = tk.Button(self.entry_frame, text="Add Expense", command=self.add_expense, bg='light yellow')
        self.add_button.pack(side=tk.LEFT)

        # View expenses widgets
        self.view_button = tk.Button(self.display_frame, text="View Expenses", command=self.view_expenses, bg='light yellow')
        self.view_button.pack(side=tk.LEFT)

        self.delete_label = tk.Label(self.display_frame, text="Delete Expense", bg='light green')
        self.delete_label.pack(side=tk.LEFT)
        self.delete_entry = tk.Entry(self.display_frame)
        self.delete_entry.pack(side=tk.LEFT)

        self.delete_button = tk.Button(self.display_frame, text="Delete", command=self.delete_expense, bg='light yellow')
        self.delete_button.pack(side=tk.LEFT)

    def add_expense(self):
        name = self.name_entry.get()
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not name or not amount or not category:
            messagebox.showerror("Error", "Name, category and amount are required.")
            return

        # Insert a row of data
        self.cursor.execute("INSERT INTO expenses VALUES (?, ?, ?, ?)", (name, category, amount, date))

        # Save (commit) the changes
        self.conn.commit()

        messagebox.showinfo("Success", "Expense added successfully.")

    def view_expenses(self):
        self.cursor.execute("SELECT * FROM expenses")
        expenses = self.cursor.fetchall()

        expenses_str = "\n".join([f"{name} ({category}): {amount} on {date}" for name, category, amount, date in expenses])
        messagebox.showinfo("Expenses", expenses_str if expenses_str else "No expenses to show.")

    def delete_expense(self):
        name = self.delete_entry.get()

        if not name:
            messagebox.showerror("Error", "Name is required.")
            return

        # Delete expense
        self.cursor.execute("DELETE FROM expenses WHERE name=?", (name,))

        # Save (commit) the changes
        self.conn.commit()

        messagebox.showinfo("Success", "Expense deleted successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseManager(root)
    root.mainloop()
