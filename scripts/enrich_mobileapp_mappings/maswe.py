from typing import Any


def collect_maswe_references(
    card_id: str, weakness_ids: list[str], maswe_data: dict[str, Any]
) -> tuple[dict[str, str], dict[str, str]]:
    """Collect threat and attack descriptions for inferred MASWE weaknesses."""
    threats: dict[str, str] = {}
    attack_vectors: dict[str, str] = {}
    for weakness_id in weakness_ids:
        weakness_mapping = maswe_data.get(weakness_id)
        if not isinstance(weakness_mapping, dict):
            raise ValueError(f"{card_id}: MASWE {weakness_id!r} is missing from generated metadata")
        for field, destination in (("owasp_mas_threat", threats), ("owasp_mas_attack", attack_vectors)):
            references = weakness_mapping.get(field, {})
            if not isinstance(references, dict) or not all(
                isinstance(identifier, str) and isinstance(description, str)
                for identifier, description in references.items()
            ):
                raise ValueError(f"MASWE {weakness_id} {field}: expected identifier-to-description mapping")
            destination.update(references)
    return threats, attack_vectors
