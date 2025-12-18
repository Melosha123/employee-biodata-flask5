from flask import Flask, render_template, request, redirect, send_file
import sqlite3
import csv

app = Flask(__name__)

# Database connection
def get_db():
    return sqlite3.connect("employees.db")

# Create table once
conn = get_db()
conn.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    emp_id TEXT,
    department TEXT,
    email TEXT,
    phone TEXT
)
""")
conn.close()

# Form page
@app.route("/")
def form():
    return render_template("form.html")

# Submit data
@app.route("/submit", methods=["POST"])
def submit():
    data = (
        request.form["name"],
        request.form["emp_id"],
        request.form["department"],
        request.form["email"],
        request.form["phone"]
    )

    conn = get_db()
    conn.execute(
        "INSERT INTO employees (name, emp_id, department, email, phone) VALUES (?, ?, ?, ?, ?)",
        data
    )
    conn.commit()
    conn.close()

    return redirect("/view")

# View all data
@app.route("/view")
def view():
    conn = get_db()
    employees = conn.execute("SELECT * FROM employees").fetchall()
    conn.close()
    return render_template("view.html", employees=employees)

# Download CSV
@app.route("/download")
def download():
    conn = get_db()
    rows = conn.execute("SELECT * FROM employees").fetchall()
    conn.close()

    with open("employees.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Emp ID", "Department", "Email", "Phone"])
        writer.writerows(rows)

    return send_file("employees.csv", as_attachment=True)

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

