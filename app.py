from flask import Flask, render_template, request, redirect, session, flash, url_for
from datetime import datetime
import os
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash


# Configure application
app = Flask(__name__)
app.secret_key = "your_secret_key"


# Auxiliary function
def calculate_account_balance(transactions):
    """
    Calculates the current account balance by subtracting total expenses from total incomes.
    Returns:
        The calculated account balance.
    """
    total_income = sum(
        transaction[1] for transaction in transactions if transaction[4] == "income"
    )
    total_expense = sum(
        transaction[1] for transaction in transactions if transaction[4] == "expense"
    )

    return total_income - total_expense


# Auxiliary function
def calculate_total_amount_period(transactions, transaction_type):
    """
    Calculates the total amount of transactions (incomes or expenses) in a given period.
    Returns:
        The calculated total amount of incomes or expenses.
    """
    return sum(
        transaction[1]
        for transaction in transactions
        if transaction[4] == transaction_type
    )


# Auxiliary function
def is_username_taken(username):
    """
    Checks if the username already exists.
    Returns:
        True if the username is taken and False if it is available.
    """
    # Construct the path to the user's directory
    user_data_dir = os.path.join("data", username)

    # Check if the user's directory exists
    return os.path.exists(user_data_dir)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if the username is already taken
        if is_username_taken(username):
            flash(
                "Username is already taken. Please choose a different one.",
                "registration_error",
            )
            return render_template(
                "register.html"
            )  # Render the registration page again with the flash message

        # Check if password and confirmation match
        if password != confirmation:
            flash(
                "Passwords do not match. Make sure you enter the same.",
                "registration_error",
            )
            return render_template(
                "register.html"
            )  # Render the registration page again with the flash message

        # Define the path to the user's directory
        user_data_dir = f"data/{username}"
        os.makedirs(
            user_data_dir, exist_ok=True
        )  # Create the directory if it doesn't exist

        # Define the path to the user's database file
        user_db_file = f"{user_data_dir}/budget.db"

        # Hash the password before adding to the database
        hashed_password = generate_password_hash(password)

        # Connect to the user's database
        conn = sqlite3.connect(user_db_file)
        cursor = conn.cursor()

        # Check if the user table exists, and create it if not
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
        )

        # Insert the new user
        cursor.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (username, hashed_password),
        )

        # Create the transactions table if it doesn't exist
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, amount REAL, description TEXT, date DATE, type TEXT)"
        )

        conn.commit()
        conn.close()

        flash("Registration successful! Now you can log in.", "registration_success")
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Define the path to the user's database file
        user_db_file = f"data/{username}/budget.db"

        # Check if the user's database file exists
        if os.path.exists(user_db_file):
            # Connect to the user's database
            conn = sqlite3.connect(user_db_file)
            cursor = conn.cursor()

            # Query the user's table for the provided username
            cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
            user = cursor.fetchone()

            # Compare passwords
            if user and check_password_hash(user[2], password):
                # Logged in successfully
                conn.close()
                session["user_id"] = user[0]
                session["username"] = user[1]  # Store the username in the session
                return redirect("/")
            else:
                # Password mismatch
                flash(
                    "Login failed. Make sure you have entered the correct password.",
                    "error",
                )
                conn.close()
        else:
            # User's database file doesn't exist, login failed
            flash(
                "Login failed. If you don't have an account, please register first.",
                "error",
            )

    return render_template("login.html")


@app.route("/logout")
def logout():
    # Delete session information
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect("/login")


@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("index.html")


@app.route("/add_transaction", methods=["GET", "POST"])
def add_transaction():
    # Retrieve transaction details from form
    amount = float(request.form.get("amount"))
    description = request.form.get("description")
    date_str = request.form.get("date")
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    transaction_type = request.form.get("transaction_type")

    # Get the username for the session
    username = session.get("username")

    if username is not None:
        # Connect to the user's database file
        conn = sqlite3.connect(f"data/{username}/budget.db")
        cursor = conn.cursor()

        # Insert the transactions details into the database
        cursor.execute(
            "INSERT INTO transactions (amount, description, date, type) VALUES (?, ?, ?, ?)",
            (amount, description, date, transaction_type),
        )
        conn.commit()
        conn.close()

    return redirect("/all_transactions")


@app.route("/expenses")
def expenses():
    # Check if the user is logged in
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Get the username from the session
    username = session.get("username")

    if username is not None:
        # Connect to the user's database file
        conn = sqlite3.connect(f"data/{username}/budget.db")
        cursor = conn.cursor()

        # Retrieve optional start_date and end_date from the form
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        if start_date and end_date:
            # Convert start_date and end_date to date objects
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

            # Fetch expense transactions within the specified date range
            cursor.execute(
                "SELECT * FROM transactions WHERE type = 'expense' AND date >= ? AND date <= ? ORDER BY date DESC",
                (start_date_obj, end_date_obj),
            )
        else:
            # Fetch all expense transactions
            cursor.execute(
                "SELECT * FROM transactions WHERE type = 'expense' ORDER BY date DESC"
            )

        expenses = cursor.fetchall()
        conn.close()

        # Calculate the total expenses within the selected date range
        total_expenses = calculate_total_amount_period(expenses, "expense")

    return render_template(
        "expenses.html",
        expenses=expenses,
        total_expenses=total_expenses,
        start_date=start_date,
        end_date=end_date,
    )


@app.route("/incomes")
def incomes():
    # Check if the user is logged in
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Get the username from the session
    username = session.get("username")

    if username is not None:
        # Connect to the user's database file
        conn = sqlite3.connect(f"data/{username}/budget.db")
        cursor = conn.cursor()

        # Retrieve optional start_date and end_date from the form
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        if start_date and end_date:
            # Convert start_date and end_date to date objects
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

            # Fetch income transactions within the specified date range
            cursor.execute(
                "SELECT * FROM transactions WHERE type = 'income' AND date >= ? AND date <= ? ORDER BY date DESC",
                (start_date_obj, end_date_obj),
            )
        else:
            # Fetch all income transactions
            cursor.execute(
                "SELECT * FROM transactions WHERE type = 'income' ORDER BY date DESC"
            )

        incomes = cursor.fetchall()
        conn.close()

        # Calculate the total incomes within the selected date range
        total_incomes = calculate_total_amount_period(incomes, "income")

    return render_template(
        "incomes.html",
        incomes=incomes,
        total_incomes=total_incomes,
        start_date=start_date,
        end_date=end_date,
    )


@app.route("/all_transactions", methods=["GET"])
def all_transactions():
    # Check if the user is logged in
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Get the username from the session
    username = session.get("username")

    if username is not None:
        # Connect to the user's database file
        conn = sqlite3.connect(f"data/{username}/budget.db")
        cursor = conn.cursor()

        # Retrieve optional start_date and end_date from the form
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        if start_date and end_date:
            # Convert start_date and end_date to date objects
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

            # Fetch all transactions within the specified date range
            cursor.execute(
                "SELECT * FROM transactions WHERE date >= ? AND date <= ? ORDER BY date DESC",
                (start_date_obj, end_date_obj),
            )
        else:
            # Fetch all transactions
            cursor.execute("SELECT * FROM transactions ORDER BY date DESC")

        transactions = cursor.fetchall()
        conn.close()

        # Calculate the account balance based on all transactions
        account_balance = calculate_account_balance(transactions)

    return render_template(
        "all_transactions.html",
        transactions=transactions,
        account_balance=account_balance,
        start_date=start_date,
        end_date=end_date,
    )


if __name__ == "__main__":
    app.run(debug=True)
