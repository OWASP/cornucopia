import logging
from typing import Any

from .constants import MAPPING_FIELDS
from .utils import merge_unique, string_list


def infer_mastg_mappings(card_id: str, test_ids: list[str], mastg_data: dict[str, Any]) -> dict[str, list[str]]:
    """Collect mappings inferred from available MASTG test metadata."""
    inferred: dict[str, list[str]] = {field: [] for field in MAPPING_FIELDS}
    for test_id in test_ids:
        if test_id == "-":
            continue
        test_mapping = mastg_data.get(test_id)
        if not isinstance(test_mapping, dict):
            logging.warning("%s: skipping MASTG test %r because it is absent from generated metadata", card_id, test_id)
            continue
        inferred["owasp_mastg"].append(test_id)
        for field in ("owasp_mastg_know", "owasp_mastg_best", "owasp_maswe"):
            inferred[field] = merge_unique(
                inferred[field], string_list(test_mapping.get(field), f"MASTG {test_id} {field}")
            )
    return inferred
