from typing import Any

from .card import enrich_card


def enrich_mappings(
    mapping_data: dict[str, Any], mastg_data: dict[str, Any], maswe_data: dict[str, Any]
) -> dict[str, Any]:
    """Enrich every card mapping in a Mobile edition mapping document."""
    suits = mapping_data.get("suits")
    if not isinstance(suits, list):
        raise ValueError("Card mappings: expected suits list")
    for suit in suits:
        if not isinstance(suit, dict) or not isinstance(suit.get("cards"), list):
            raise ValueError("Card mappings: each suit must contain a cards list")
        for card in suit["cards"]:
            if not isinstance(card, dict):
                raise ValueError("Card mappings: each card must be a mapping")
            enrich_card(card, mastg_data, maswe_data)
    return mapping_data
