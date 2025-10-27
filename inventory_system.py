"""Simple inventory management utilities with basic persistence.

This module provides helper functions to manage an in-memory inventory
dictionary and persist to a JSON file. It includes safe input validation,
PEP8-compliant naming, and avoids unsafe patterns flagged by static analyzers.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Dict, List, Optional

stock_data: Dict[str, int] = {}


def add_item(
    item: str,
    qty: int = 0,
    logs: Optional[List[str]] = None,
) -> None:
    """Add a non-negative quantity of an item to the inventory.

    Args:
        item: Non-empty item name.
        qty: Quantity to add (must be a non-negative integer).
        logs: Optional list to append a human-readable log entry.

    Raises:
        ValueError: If inputs are invalid.
    """
    if not isinstance(item, str) or not item.strip():
        raise ValueError("item must be a non-empty string")
    if not isinstance(qty, int) or qty < 0:
        raise ValueError("qty must be a non-negative integer")

    stock_data[item] = stock_data.get(item, 0) + qty

    if logs is not None:
        logs.append(f"{datetime.now().isoformat()}: Added {qty} of {item}")


def remove_item(item: str, qty: int) -> None:
    """Remove a non-negative quantity of an item; delete when quantity <= 0.

    Missing items are ignored.

    Args:
        item: Item name to decrement.
        qty: Quantity to remove (must be a non-negative integer).

    Raises:
        ValueError: If inputs are invalid.
    """
    if not isinstance(item, str) or not item.strip():
        raise ValueError("item must be a non-empty string")
    if not isinstance(qty, int) or qty < 0:
        raise ValueError("qty must be a non-negative integer")

    current = stock_data.get(item, 0)
    new_qty = current - qty
    if new_qty <= 0:
        stock_data.pop(item, None)
    else:
        stock_data[item] = new_qty


def get_qty(item: str) -> int:
    """Return current quantity for an item; 0 if missing."""
    if not isinstance(item, str) or not item.strip():
        raise ValueError("item must be a non-empty string")
    return stock_data.get(item, 0)


def load_data(file: str = "inventory.json") -> None:
    """Load inventory from a JSON file into the in-memory store.

    The file must contain a JSON object mapping string item names to integer
    quantities. Invalid entries are ignored.
    """
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("inventory file must contain a JSON object")

    new_data: Dict[str, int] = {}
    for key, value in data.items():
        if isinstance(key, str) and isinstance(value, int) and value >= 0:
            new_data[key] = value

    stock_data.clear()
    stock_data.update(new_data)


def save_data(file: str = "inventory.json") -> None:
    """Persist the current inventory to a JSON file using UTF-8 encoding."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, ensure_ascii=False, indent=2)


def print_data() -> None:
    """Print a simple report of items and their quantities."""
    print("Items Report")
    for item in sorted(stock_data):
        print(f"{item} -> {stock_data[item]}")


def check_low_items(threshold: int = 5) -> List[str]:
    """Return items with quantity less than the provided threshold."""
    if not isinstance(threshold, int) or threshold < 0:
        raise ValueError("threshold must be a non-negative integer")
    return [i for i, q in stock_data.items() if q < threshold]


def main() -> None:
    """Demonstrate basic inventory operations."""
    logs: List[str] = []
    add_item("apple", 10, logs)
    add_item("banana", 2, logs)
    remove_item("apple", 3)
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()


if __name__ == "__main__":
    main()
