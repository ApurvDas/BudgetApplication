import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

columns = ["Date", "Description", "Category", "Amount (₹)"]
transactions = pd.DataFrame(columns=columns)

DARK_BG = "#2E2E2E"
DARK_FG = "#F0F0F0"
BUTTON_BG = "#444444"
BUTTON_FG = "#FFFFFF"
ENTRY_BG = "#3C3C3C"
ENTRY_FG = "#F0F0F0"
TABLE_BG = "#2E2E2E"
TABLE_ALT_BG = "#383838"
HIGHLIGHT = "#555555"

def add_transaction():
    date = date_entry.get()
    description = description_entry.get()
    category = category_entry.get()
    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Amount must be a number.")
        return
    global transactions
    new_transaction = pd.DataFrame([[date, description, category, amount]], columns=columns)
    transactions = pd.concat([transactions, new_transaction], ignore_index=True)
    date_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    refresh_table()
    messagebox.showinfo("Success", "Transaction added successfully.")

def refresh_table():
    for row in table.get_children():
        table.delete(row)
    for i, row in transactions.iterrows():
        table.insert("", "end", values=list(row), tags=("evenrow" if i % 2 == 0 else "oddrow"))

def show_summary():
    total_income = transactions[transactions["Amount (₹)"] > 0]["Amount (₹)"].sum()
    total_expense = transactions[transactions["Amount (₹)"] < 0]["Amount (₹)"].sum()
    balance = total_income + total_expense
    summary_message = (
        f"कुल आय (Total Income): ₹{total_income:.2f}\n"
        f"कुल खर्चा (Total Expenses): ₹{abs(total_expense):.2f}\n"
        f"बचत (Balance): ₹{balance:.2f}"
    )
    messagebox.showinfo("Summary", summary_message)

def save_transactions():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        transactions.to_csv(file_path, index=False)
        messagebox.showinfo("Success", f"Transactions saved to {file_path}")

def load_transactions():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        global transactions
        transactions = pd.read_csv(file_path)
        refresh_table()
        messagebox.showinfo("Success", f"Transactions loaded from {file_path}")

root = tk.Tk()
root.title("Indian Expense Tracker (Dark Mode)")
root.geometry("800x600")
root.configure(bg=DARK_BG)

input_frame = tk.Frame(root, bg=DARK_BG)
input_frame.pack(pady=10)

tk.Label(input_frame, text="तारीख (Date) [DD-MM-YYYY]:", bg=DARK_BG, fg=DARK_FG).grid(row=0, column=0, padx=5, pady=5)
date_entry = tk.Entry(input_frame, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=DARK_FG)
date_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="विवरण (Description):", bg=DARK_BG, fg=DARK_FG).grid(row=1, column=0, padx=5, pady=5)
description_entry = tk.Entry(input_frame, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=DARK_FG)
description_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="श्रेणी (Category):", bg=DARK_BG, fg=DARK_FG).grid(row=2, column=0, padx=5, pady=5)
category_entry = ttk.Combobox(input_frame, values=["Groceries", "Travel", "Rent", "Medical", "Education", "Utilities", "Other"])
category_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(input_frame, text="राशि (Amount ₹):", bg=DARK_BG, fg=DARK_FG).grid(row=3, column=0, padx=5, pady=5)
amount_entry = tk.Entry(input_frame, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=DARK_FG)
amount_entry.grid(row=3, column=1, padx=5, pady=5)

add_button = tk.Button(input_frame, text="लेन-देन जोड़ें (Add Transaction)", bg=BUTTON_BG, fg=BUTTON_FG, command=add_transaction)
add_button.grid(row=4, column=0, columnspan=2, pady=10)

table_frame = tk.Frame(root, bg=DARK_BG)
table_frame.pack(pady=10)

columns = ["Date", "Description", "Category", "Amount (₹)"]
table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
for col in columns:
    table.heading(col, text=col)
    table.column(col, anchor="center")
table.tag_configure("evenrow", background=TABLE_ALT_BG, foreground=DARK_FG)
table.tag_configure("oddrow", background=TABLE_BG, foreground=DARK_FG)
table.pack()

button_frame = tk.Frame(root, bg=DARK_BG)
button_frame.pack(pady=10)

summary_button = tk.Button(button_frame, text="सारांश देखें (Show Summary)", bg=BUTTON_BG, fg=BUTTON_FG, command=show_summary)
summary_button.grid(row=0, column=0, padx=10)

save_button = tk.Button(button_frame, text="सेव करें (Save Transactions)", bg=BUTTON_BG, fg=BUTTON_FG, command=save_transactions)
save_button.grid(row=0, column=1, padx=10)

load_button = tk.Button(button_frame, text="लोड करें (Load Transactions)", bg=BUTTON_BG, fg=BUTTON_FG, command=load_transactions)
load_button.grid(row=0, column=2, padx=10)

root.mainloop()
