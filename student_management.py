import tkinter as tk
import os
from tkinter import ttk, messagebox
import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password=os.environ["MYSQL_PASSWORD"],
    database="college"
)

cursor = db.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    roll_no VARCHAR(50),
    grade VARCHAR(10)
)
""")
db.commit()


# Add student
def add_student():
    name = name_var.get().strip()
    roll = roll_var.get().strip()
    grade = grade_var.get().strip()

    if not name or not roll or not grade:
        messagebox.showwarning("Error", "All fields required")
        return

    cursor.execute(
        "INSERT INTO students (name, roll_no, grade) VALUES (%s, %s, %s)",
        (name, roll, grade)
    )
    db.commit()

    messagebox.showinfo("Success", "Student added successfully")

    name_var.set("")
    roll_var.set("")
    grade_var.set("")
    fetch_students()


# Display students
def fetch_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    tree.delete(*tree.get_children())

    for row in rows:
        tree.insert("", tk.END, values=row)


# Delete student
def delete_student():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning("Error", "Select a student to delete")
        return

    item = tree.item(selected[0])
    student_id = item["values"][0]

    cursor.execute(
        "DELETE FROM students WHERE id=%s",
        (student_id,)
    )
    db.commit()

    fetch_students()
    messagebox.showinfo("Success", "Student deleted successfully")


# Search student
def search_student():
    query = search_var.get().strip()

    if not query:
        messagebox.showwarning("Error", "Enter Roll No to search")
        return

    for row in tree.get_children():
        values = tree.item(row)["values"]

        if str(values[2]) == query:
            tree.selection_set(row)
            tree.focus(row)
            tree.see(row)
            return

    messagebox.showinfo("Not Found", "Student not found")


# Sort students by name
def sort_students():
    records = [
        tree.item(row)["values"]
        for row in tree.get_children()
    ]

    records.sort(key=lambda x: str(x[1]).lower())

    tree.delete(*tree.get_children())

    for record in records:
        tree.insert("", tk.END, values=record)


# GUI setup
root = tk.Tk()
root.title("Student Record Management")
root.geometry("650x520")
root.configure(bg="#fdf6f0")

# Styling
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TLabel",
    background="#fdf6f0",
    font=("Segoe UI", 10)
)

style.configure(
    "TButton",
    font=("Segoe UI", 10, "bold"),
    padding=6
)

style.configure(
    "Treeview.Heading",
    font=("Segoe UI", 10, "bold")
)

style.configure("Treeview", rowheight=25)

# Variables
name_var = tk.StringVar()
roll_var = tk.StringVar()
grade_var = tk.StringVar()
search_var = tk.StringVar()

# Labels
tk.Label(root, text="Name").grid(
    row=0, column=0, padx=10, pady=5
)

tk.Label(root, text="Roll No").grid(
    row=1, column=0, padx=10, pady=5
)

tk.Label(root, text="Grade").grid(
    row=2, column=0, padx=10, pady=5
)

# Input fields
tk.Entry(root, textvariable=name_var, width=30).grid(
    row=0, column=1, padx=10, pady=5
)

tk.Entry(root, textvariable=roll_var, width=30).grid(
    row=1, column=1, padx=10, pady=5
)

tk.Entry(root, textvariable=grade_var, width=30).grid(
    row=2, column=1, padx=10, pady=5
)

# Buttons
ttk.Button(root, text="Add Student",
           command=add_student).grid(
    row=3, column=0, padx=10, pady=10
)

ttk.Button(root, text="Delete Student",
           command=delete_student).grid(
    row=3, column=1, padx=10, pady=10
)

ttk.Button(root, text="Sort by Name",
           command=sort_students).grid(
    row=4, column=0, padx=10, pady=5
)

ttk.Button(root, text="Search Roll No",
           command=search_student).grid(
    row=4, column=1, padx=10, pady=5
)

tk.Entry(root, textvariable=search_var, width=30).grid(
    row=5, column=0, columnspan=2, padx=10, pady=5
)

# Table
tree = ttk.Treeview(
    root,
    columns=("ID", "Name", "Roll", "Grade"),
    show="headings"
)

for col in ("ID", "Name", "Roll", "Grade"):
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=120)

tree.grid(
    row=6, column=0, columnspan=2, padx=10, pady=10
)

# Load records
fetch_students()

# Run application
root.mainloop()