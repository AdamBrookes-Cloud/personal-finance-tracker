import json
from pathlib import Path

from finance_tracker.models import Transaction


def save_transactions(
    transactions: list[Transaction],
    file_path: Path,
) -> None:
    data = [transaction.to_dict() for transaction in transactions]

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_transactions(file_path: Path) -> list[Transaction]:
    if not file_path.exists():
        return []

    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return [Transaction.from_dict(item) for item in data]