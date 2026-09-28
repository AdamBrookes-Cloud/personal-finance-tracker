from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import uuid4


class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"


@dataclass
class Transaction:
    type: TransactionType
    amount: Decimal
    category: str
    description: str
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError("Transaction amount must be greater than zero.")

        if not self.category.strip():
            raise ValueError("Transaction category cannot be empty.")

        if not self.description.strip():
            raise ValueError("Transaction description cannot be empty.")

    def to_dict(self) -> dict[str, str]:
        return {
            "id": self.id,
            "type": self.type.value,
            "amount": str(self.amount),
            "category": self.category,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Transaction":
        return cls(
            type=TransactionType(data["type"]),
            amount=Decimal(data["amount"]),
            category=data["category"],
            description=data["description"],
            id=data["id"],
            created_at=datetime.fromisoformat(data["created_at"]),
        )