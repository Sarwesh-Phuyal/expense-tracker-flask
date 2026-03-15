from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    conn = get_db()

    expenses = conn.execute("SELECT * FROM expenses").fetchall()

    total = conn.execute(
        "SELECT SUM(amount) FROM expenses"
    ).fetchone()[0] or 0

    category_data = conn.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses
        GROUP BY category
    """).fetchall()

    categories = [row["category"] for row in category_data]
    category_totals = [row["total"] for row in category_data]

    conn.close()

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        categories=categories,
        category_totals=category_totals
    )


@app.route("/add", methods=["POST"])
def add_expense():
    name = request.form["name"]
    amount = request.form["amount"]
    category = request.form["category"]

    conn = get_db()

    conn.execute(
        "INSERT INTO expenses (name, amount, category) VALUES (?, ?, ?)",
        (name, amount, category)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete_expense(id):
    conn = get_db()

    conn.execute("DELETE FROM expenses WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)