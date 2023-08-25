# Personal Budget Tracker Web App
## To keep track of your finances

#### *Video presenting the functionality*: [(https://youtu.be/2vcUFBkO9G0)](https://youtu.be/2vcUFBkO9G0)

***

### *Overview*:
**Personal Budget Tracker** is a web application designed to help you manage your finances effectively. It allows you to track your expenses and income, view your financial history, and maintain an overview of your account balance. With this application, you can take control of your financial situation, make informed decisions, and achieve your financial goals.


### *Tech/Framework Used*:
* **Python**: The application is built using Python, a versatile and popular programming language.
* **Flask**: Flask is a micro web framework written in Python.
* **SQLite**: SQLite is used as the database management system to store user data and transaction records.
* **Werkzeug**: Werkzeug is employed for password hashing and user authentication.
* **HTML and CSS**: HTML and CSS are used for the front end to create a clean and visually appealing interface.


### *Features*:

#### *User Registration and Authentication*
* **User Registration**: Users can create an account by providing a unique username and password. The application checks the availability of the chosen username to ensure uniqueness.
* **User Authentication**: Registered users can log in securely using their username and password. Passwords are hashed for security.

#### *Transaction Management*
* **Add Transactions**: Users can add new transactions, specifying the amount, description, date, and type (expense or income).
* **View Transactions**: The application provides different views to display transactions, including all transactions, expenses, and incomes.
* **Date Range Selection**: Users can filter transactions based on a specified date range, allowing them to focus on specific periods of financial activity.

#### *Account Balance*
* **Real-time Balance**: The application calculates and displays the current account balance based on income and expense transactions.

#### *User-Friendly Interface*
* **Intuitive UI**: The user interface is designed for simplicity and ease of use, making it accessible to users of all levels of technical expertise.


### *Usage:*

1. **Register**: Create an account by providing a unique username and password.
    - If the selected username already exists, you will receive the message: "Username is already taken. Please choose a different one."
    - If the entered password and the password confirmation are not the same, you will see the message: "Passwords do not match. Make sure you enter the same."
    - If your registration is successful, you will be redirected to the login page with the message "Registration successful! Now you can log in." Your account will be assigned the budget.db database with the transactions table, where the data you entered will be stored.

2. **Log In**: Log in with your registered username and password.
    - If you try to log in and it turns out that the username has not yet been registered, you will receive the message: "Login failed. If you don't have an account, please register first."
    - If the account exists but an incorrect password was entered, you will receive the message: "Login failed. Make sure you have entered the correct password."
    - If the login is successful, you will be redirected to the main page with the form for adding new transactions.

3. **Add Transactions**: Fill out the form to add transactions with details such as amount, description, date, and type (expense or income). After entering the transaction, you will be redirected to the "All transactions" subpage, where your all expenses and incomes will be displayed. Transactions are ordered in descending order (newest to oldest by date).

4. **View Transactions**: Navigate between different transaction views, including all transactions, income, and expenses. Transactions with red down arrows are expenses, while those with green up arrows are incomes. You can use the date range selection to filter transactions. After selecting a date range, only transactions from that period will be displayed. If you haven't added any transaction yet, the following message will appear on the screen: "No data is available. Complete the form to add a transaction."

5. **View Account Balance**: At the end of the table in "All transactions" there is your "Current balance". It is the sum of all incomes subtracted from the sum of all expenses and is updated with each transaction you enter. The balance is recalculated according to the selected date range. The Expenses and Incomes subpages are built similarly, except that in expenses you will find only expenses and their sum, and in incomes only incomes and their sum. Here you can also observe your transactions in the selected date range. You can also use a date range here.

6. **Log Out**: Safely log out of your account when you're done. If you have successfully logged out, the following message will be displayed: "Logged out successfully!"


### *Running the Application:*

1. Download the repository to your computer.
2. Ensure that you have Python and all necessary libraries installed on your computer.
3. Navigate to the project directory, for example, by using the following command: `cd budget-tracker`
4. To start the application, type the following command in your terminal: `flask run`
5. The application will be accessible at http://localhost:5000 (or another address displayed in the console).
