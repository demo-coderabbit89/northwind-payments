"""Shared presentation helpers."""


def to_display_amount(amount_cents: int) -> float:
    """Convert stored cents to a display amount in major currency units."""
    return amount_cents / 100
