import logging
from typing import Any

from .utils import merge_unique, string_list


def infer_masvs_mappings(card_id: str, weakness_ids: list[str], maswe_data: dict[str, Any]) -> list[str]:
    """Collect MASVS mappings from MASWE metadata referenced by a card."""
    inferred: list[str] = []
    for weakness_id in weakness_ids:
        weakness_mapping = maswe_data.get(weakness_id)
        if not isinstance(weakness_mapping, dict):
            logging.warning(
                "%s: skipping MASWE weakness %r because it is absent from generated metadata", card_id, weakness_id
            )
            continue
        inferred = merge_unique(
            inferred,
            string_list(weakness_mapping.get("owasp_masvs"), f"MASWE {weakness_id} owasp_masvs"),
        )
    return inferred
