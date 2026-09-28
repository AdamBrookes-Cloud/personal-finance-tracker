from decimal import Decimal

from finance_tracker.models import Transaction, TransactionType
from finance_tracker.tracker import FinanceTracker


tracker = FinanceTracker()

tracker.add_transaction(
    Transaction(
        type=TransactionType.INCOME,
        amount=Decimal("2000.00"),
        category="Salary",
        description="Monthly salary",
    )
)

tracker.add_transaction(
    Transaction(
        type=TransactionType.EXPENSE,
        amount=Decimal("500.00"),
        category="Rent",
        description="Monthly rent",
    )
)

tracker.add_transaction(
    Transaction(
        type=TransactionType.EXPENSE,
        amount=Decimal("75.50"),
        category="Food",
        description="Groceries",
    )
)

print(f"Total income: £{tracker.get_total_income()}")
print(f"Total expenses: £{tracker.get_total_expenses()}")
print(f"Balance: £{tracker.calculate_balance()}")
print(f"Spending by category: {tracker.get_spending_by_category()}")
print("\nSearch results for 'food':")

for transaction in tracker.search_transactions("food"):
    print(transaction)