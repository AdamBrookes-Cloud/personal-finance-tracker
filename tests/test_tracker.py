from decimal import Decimal
from pathlib import Path

import pytest

from finance_tracker.models import Transaction, TransactionType
from finance_tracker.storage import load_transactions, save_transactions
from finance_tracker.tracker import FinanceTracker


def test_add_transaction():
    tracker = FinanceTracker()

    transaction = Transaction(
        type=TransactionType.INCOME,
        amount=Decimal("2000.00"),
        category="Salary",
        description="Monthly salary",
    )

    tracker.add_transaction(transaction)

    assert len(tracker.get_transactions()) == 1
    assert tracker.get_transactions()[0] == transaction


def test_calculate_balance():
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

    assert tracker.calculate_balance() == Decimal("1424.50")


def test_get_total_income():
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
            type=TransactionType.INCOME,
            amount=Decimal("250.00"),
            category="Freelance",
            description="Freelance work",
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

    assert tracker.get_total_income() == Decimal("2250.00")


def test_get_total_expenses():
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

    assert tracker.get_total_expenses() == Decimal("575.50")


def test_get_spending_by_category():
    tracker = FinanceTracker()

    tracker.add_transaction(
        Transaction(
            type=TransactionType.EXPENSE,
            amount=Decimal("75.50"),
            category="Food",
            description="Groceries",
        )
    )

    tracker.add_transaction(
        Transaction(
            type=TransactionType.EXPENSE,
            amount=Decimal("25.00"),
            category="Food",
            description="Lunch",
        )
    )

    tracker.add_transaction(
        Transaction(
            type=TransactionType.EXPENSE,
            amount=Decimal("40.00"),
            category="Transport",
            description="Train ticket",
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
            type=TransactionType.INCOME,
            amount=Decimal("2000.00"),
            category="Salary",
            description="Monthly salary",
        )
    )

    spending = tracker.get_spending_by_category()

    assert spending == {
        "Food": Decimal("100.50"),
        "Transport": Decimal("40.00"),
        "Rent": Decimal("500.00"),
    }


def test_search_transactions():
    tracker = FinanceTracker()

    food_transaction = Transaction(
        type=TransactionType.EXPENSE,
        amount=Decimal("75.50"),
        category="Food",
        description="Groceries",
    )

    rent_transaction = Transaction(
        type=TransactionType.EXPENSE,
        amount=Decimal("500.00"),
        category="Rent",
        description="Monthly rent",
    )

    tracker.add_transaction(food_transaction)
    tracker.add_transaction(rent_transaction)

    results = tracker.search_transactions("food")

    assert len(results) == 1
    assert results[0] == food_transaction


def test_transaction_rejects_zero_amount():
    with pytest.raises(ValueError):
        Transaction(
            type=TransactionType.EXPENSE,
            amount=Decimal("0"),
            category="Food",
            description="Lunch",
        )


def test_transaction_rejects_negative_amount():
    with pytest.raises(ValueError):
        Transaction(
            type=TransactionType.EXPENSE,
            amount=Decimal("-10.00"),
            category="Food",
            description="Lunch",
        )


def test_transaction_rejects_empty_category():
    with pytest.raises(ValueError):
        Transaction(
            type=TransactionType.EXPENSE,
            amount=Decimal("10.00"),
            category="",
            description="Lunch",
        )


def test_transaction_rejects_empty_description():
    with pytest.raises(ValueError):
        Transaction(
            type=TransactionType.EXPENSE,
            amount=Decimal("10.00"),
            category="Food",
            description="",
        )


def test_empty_tracker():
    tracker = FinanceTracker()

    assert tracker.get_transactions() == []
    assert tracker.get_income() == []
    assert tracker.get_expenses() == []
    assert tracker.get_total_income() == Decimal("0")
    assert tracker.get_total_expenses() == Decimal("0")
    assert tracker.calculate_balance() == Decimal("0")
    assert tracker.get_spending_by_category() == {}
    assert tracker.search_transactions("food") == []


def test_transaction_serialization():
    transaction = Transaction(
        type=TransactionType.EXPENSE,
        amount=Decimal("75.50"),
        category="Food",
        description="Groceries",
    )

    data = transaction.to_dict()
    restored_transaction = Transaction.from_dict(data)

    assert restored_transaction == transaction


def test_save_and_load_transactions(tmp_path: Path):
    transactions = [
        Transaction(
            type=TransactionType.INCOME,
            amount=Decimal("2000.00"),
            category="Salary",
            description="Monthly salary",
        ),
        Transaction(
            type=TransactionType.EXPENSE,
            amount=Decimal("75.50"),
            category="Food",
            description="Groceries",
        ),
    ]

    file_path = tmp_path / "transactions.json"

    save_transactions(transactions, file_path)
    loaded_transactions = load_transactions(file_path)

    assert loaded_transactions == transactions


def test_tracker_save_and_load(tmp_path: Path):
    tracker = FinanceTracker()

    transaction = Transaction(
        type=TransactionType.EXPENSE,
        amount=Decimal("50.00"),
        category="Food",
        description="Lunch",
    )

    tracker.add_transaction(transaction)

    file_path = tmp_path / "transactions.json"

    tracker.save(file_path)

    new_tracker = FinanceTracker()
    new_tracker.load(file_path)

    assert new_tracker.get_transactions() == [transaction]

def test_load_invalid_json(tmp_path: Path):
    file_path = tmp_path / "transactions.json"

    file_path.write_text("this is not valid JSON", encoding="utf-8")

    with pytest.raises(ValueError):
        load_transactions(file_path)

def test_load_invalid_transaction_data(tmp_path: Path):
    file_path = tmp_path / "transactions.json"

    file_path.write_text(
        """
        [
            {
                "id": "123",
                "type": "expense",
                "category": "Food",
                "description": "Lunch",
                "created_at": "2026-09-28T12:00:00"
            }
        ]
        """,
        encoding="utf-8",
    )

    with pytest.raises(KeyError):
        load_transactions(file_path)