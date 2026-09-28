from decimal import Decimal

from finance_tracker.models import Transaction, TransactionType


class FinanceTracker:
    def __init__(self):
        self.transactions: list[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

    def get_transactions(self) -> list[Transaction]:
        return self.transactions.copy()

    def get_income(self) -> list[Transaction]:
        return [
            transaction
            for transaction in self.transactions
            if transaction.type == TransactionType.INCOME
        ]

    def get_expenses(self) -> list[Transaction]:
        return [
            transaction
            for transaction in self.transactions
            if transaction.type == TransactionType.EXPENSE
        ]

    def get_total_income(self) -> Decimal:
        return sum(
            (
                transaction.amount
                for transaction in self.transactions
                if transaction.type == TransactionType.INCOME
            ),
            Decimal("0"),
        )

    def get_total_expenses(self) -> Decimal:
        return sum(
            (
                transaction.amount
                for transaction in self.transactions
                if transaction.type == TransactionType.EXPENSE
            ),
            Decimal("0"),
        )

    def get_spending_by_category(self) -> dict[str, Decimal]:
        spending: dict[str, Decimal] = {}

        for transaction in self.get_expenses():
            if transaction.category not in spending:
                spending[transaction.category] = Decimal("0")

            spending[transaction.category] += transaction.amount

        return spending

    def search_transactions(self, query: str) -> list[Transaction]:
        query = query.strip().lower()

        return [
            transaction
            for transaction in self.transactions
            if query in transaction.category.lower()
            or query in transaction.description.lower()
        ]

    def calculate_balance(self) -> Decimal:
        return self.get_total_income() - self.get_total_expenses()