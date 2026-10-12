from typing import Any

from .constants import MAPPING_FIELDS
from .masvs import infer_masvs_mappings
from .mastg import infer_mastg_mappings
from .maswe import collect_maswe_references
from .utils import merge_unique, string_list


def enrich_card(card: dict[str, Any], mastg_data: dict[str, Any], maswe_data: dict[str, Any]) -> None:
    """Merge MASTG siblings and their MASWE and MASVS metadata into one card."""
    card_id = card.get("id", "unknown card")
    test_ids = string_list(card.get("owasp_mastg"), f"{card_id} owasp_mastg")
    inferred = infer_mastg_mappings(card_id, test_ids, mastg_data)
    threats, attack_vectors = collect_maswe_references(card_id, inferred["owasp_maswe"], maswe_data)

    for field in MAPPING_FIELDS:
        card[field] = merge_unique(string_list(card.get(field), f"{card_id} {field}"), inferred[field])
    card["owasp_masvs"] = infer_masvs_mappings(
        card_id, string_list(card["owasp_maswe"], f"{card_id} owasp_maswe"), maswe_data
    )
    if threats:
        card["threat"] = threats
    if attack_vectors:
        card["attack_vector"] = attack_vectors
