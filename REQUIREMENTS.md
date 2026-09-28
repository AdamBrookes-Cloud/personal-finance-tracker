# Personal Finance Tracker — Requirements

## Goal

Build a command-line application that allows a user to record, view, search, and analyse personal financial transactions.

## Functional Requirements

### FR1 — Add Transaction

The user must be able to add a transaction containing:

- Transaction type
- Amount
- Category
- Description

The transaction type must be either income or expense.

### FR2 — View Transactions

The user must be able to view all recorded transactions.

Each transaction should display its relevant information clearly.

### FR3 — Calculate Balance

The application must calculate the current balance using:

Balance = Total Income - Total Expenses

### FR4 — Category Spending

The application must calculate total spending for each expense category.

### FR5 — Search Transactions

The user must be able to search transactions using information such as category or description.

### FR6 — Save Transactions

Transactions must be saved to a local file so they persist after the application closes.

### FR7 — Load Transactions

Previously saved transactions must be loaded when the application starts.

### FR8 — Input Validation

The application must validate user input and handle invalid input without crashing.

### FR9 — Exit

The user must be able to exit the application cleanly.

## Non-Functional Requirements

- The application must be written in Python.
- The code should be separated into logical modules.
- Functions should have clear responsibilities.
- Type hints should be used.
- Automated tests should be written using pytest.
- The application should handle expected errors gracefully.
- The project should be documented in the README.
- The project should be managed using Git.
