"""Parse validated MASTG and MASWE source metadata into Cornucopia mapping data."""

import logging
import re
from pathlib import Path
from typing import Any

import yaml

MAX_YAML_FILE_SIZE_BYTES = 2 * 1024 * 1024


class UniqueKeySafeLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects ambiguous duplicate mapping keys."""

    def construct_mapping(self, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in mapping:
                raise ValueError(f"Duplicate YAML key: {key!r}")
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def read_yaml_source(path: Path) -> str:
    """Read a bounded YAML-bearing source file to limit resource consumption."""
    if path.stat().st_size > MAX_YAML_FILE_SIZE_BYTES:
        raise ValueError(f"{path}: file exceeds {MAX_YAML_FILE_SIZE_BYTES} byte limit")
    return path.read_text(encoding="utf-8")


def extract_front_matter(test_file: Path) -> dict[str, Any]:
    """Parse a Markdown file's YAML front matter, returning an empty mapping when absent."""
    match = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|$)", read_yaml_source(test_file), re.DOTALL)
    if not match:
        return {}
    metadata = yaml.load(match.group(1), Loader=UniqueKeySafeLoader)
    return metadata if isinstance(metadata, dict) else {}


def normalize_references(value: Any, prefix: str, test_file: Path) -> list[str]:
    """Return validated, de-prefixed references in source order."""
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{test_file}: {prefix} references must be a list of strings")

    result: list[str] = []
    for reference in value:
        if not reference.startswith(prefix) or not reference[len(prefix) :].isdigit():
            raise ValueError(f"{test_file}: invalid {prefix} reference {reference!r}")
        result.append(reference.removeprefix(prefix))
    return result


def extract_test_mapping(test_file: Path) -> tuple[str, dict[str, list[str]]] | None:
    """Extract one beta test's MASTG references, skipping files without a test identifier."""
    metadata = extract_front_matter(test_file)
    test_id = metadata.get("id")
    if not isinstance(test_id, str) or not re.fullmatch(r"MASTG-TEST-\d+", test_id):
        logging.debug("Skipping %s because it has no valid MASTG test identifier", test_file)
        return None

    mapping: dict[str, list[str]] = {}
    references = (
        ("weakness", "owasp_maswe", "MASWE-"),
        ("knowledge", "owasp_mastg_know", "MASTG-KNOW-"),
        ("best-practices", "owasp_mastg_best", "MASTG-BEST-"),
    )
    for source_field, output_field, prefix in references:
        value = metadata.get(source_field)
        normalized = normalize_references(
            [value] if source_field == "weakness" and value is not None else value, prefix, test_file
        )
        if normalized:
            mapping[output_field] = normalized
    return test_id.removeprefix("MASTG-TEST-"), mapping


def extract_mastg_mappings(repository_path: Path) -> dict[str, dict[str, list[str]]]:
    """Extract reference mappings from all beta test files in a MASTG checkout."""
    tests_path = repository_path / "tests-beta"
    if not tests_path.is_dir():
        raise FileNotFoundError(f"MASTG beta tests directory not found: {tests_path}")

    mappings: dict[str, dict[str, list[str]]] = {}
    for test_file in sorted(tests_path.rglob("MASTG-TEST-*.md")):
        if any(parent.name.startswith("MASVS-") for parent in test_file.parents):
            add_test_mapping(mappings, test_file)
    return dict(sorted(mappings.items()))


def add_test_mapping(mappings: dict[str, dict[str, list[str]]], test_file: Path) -> None:
    """Extract and add one test mapping, rejecting duplicate test identifiers."""
    extracted = extract_test_mapping(test_file)
    if extracted is None:
        return
    test_id, mapping = extracted
    if test_id in mappings:
        raise ValueError(f"Duplicate MASTG test identifier: {test_id}")
    mappings[test_id] = mapping


def output_data(mappings: dict[str, dict[str, list[str]]], edition: str, version: str) -> dict[str, Any]:
    """Build the stable YAML structure consumed by Cornucopia."""
    return {"meta": {"edition": edition, "component": "mastg", "language": "ALL", "version": version}, **mappings}


def parse_catalog(path: Path, prefix: str) -> dict[str, str]:
    """Load a MAS threat or attack catalog as de-prefixed identifiers and descriptions."""
    catalog = yaml.load(read_yaml_source(path), Loader=UniqueKeySafeLoader)
    if not isinstance(catalog, dict):
        raise ValueError(f"{path}: expected a mapping")
    return {
        deprefix_catalog_entry(path, prefix, identifier, description)[0]: deprefix_catalog_entry(
            path, prefix, identifier, description
        )[1]
        for identifier, description in catalog.items()
    }


def deprefix_catalog_entry(path: Path, prefix: str, identifier: Any, description: Any) -> tuple[str, str]:
    """Validate and normalize one catalog entry."""
    if not isinstance(identifier, str) or not identifier.startswith(prefix) or not identifier[len(prefix) :].isdigit():
        raise ValueError(f"{path}: invalid {prefix} identifier {identifier!r}")
    if not isinstance(description, str):
        raise ValueError(f"{path}: {identifier} description must be a string")
    return identifier.removeprefix(prefix), description


def extract_maswe_metadata(repository_path: Path, weakness_id: str) -> dict[str, Any]:
    """Extract MASVS, threat, and attack references for one MASWE weakness."""
    matches = list((repository_path / "weaknesses").glob(f"MASVS-*/MASWE-{weakness_id}.md"))
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one MASWE-{weakness_id} document, found {len(matches)}")

    metadata = extract_front_matter(matches[0])
    if metadata.get("id") != f"MASWE-{weakness_id}":
        raise ValueError(f"{matches[0]}: invalid MASWE identifier")
    return validate_maswe_metadata(matches[0], metadata)


def validate_maswe_metadata(path: Path, metadata: dict[str, Any]) -> dict[str, Any]:
    """Validate MASWE front matter required for mapping enrichment."""
    mappings = metadata.get("mappings")
    if not isinstance(mappings, dict):
        raise ValueError(f"{path}: mappings must be a mapping")
    result = {
        "owasp_masvs": mappings.get("masvs-v2", []),
        "threat": metadata.get("threat"),
        "attacks": metadata.get("attacks", []),
    }
    for field in ("owasp_masvs", "attacks"):
        if not isinstance(result[field], list) or not all(isinstance(item, str) for item in result[field]):
            raise ValueError(f"{path}: {field.removeprefix('owasp_').replace('_', '-')} must be a list of strings")
    if not isinstance(result["threat"], str):
        raise ValueError(f"{path}: threat must be a string")
    return result


def collect_maswe_mappings(mastg_mappings: dict[str, dict[str, list[str]]]) -> dict[str, dict[str, list[str]]]:
    """Invert MASTG mappings, retaining every test's knowledge and best-practice siblings."""
    result: dict[str, dict[str, list[str]]] = {}
    for test_id, mapping in mastg_mappings.items():
        for weakness_id in mapping.get("owasp_maswe", []):
            add_maswe_mapping(result, weakness_id, test_id, mapping)
    return dict(sorted(result.items()))


def add_maswe_mapping(
    result: dict[str, dict[str, list[str]]], weakness_id: str, test_id: str, mapping: dict[str, list[str]]
) -> None:
    """Merge one MASTG test and its siblings under a MASWE weakness."""
    weakness_mapping = result.setdefault(
        weakness_id, {"owasp_mastg": [], "owasp_mastg_know": [], "owasp_mastg_best": []}
    )
    for field, values in (
        ("owasp_mastg", [test_id]),
        ("owasp_mastg_know", mapping.get("owasp_mastg_know", [])),
        ("owasp_mastg_best", mapping.get("owasp_mastg_best", [])),
    ):
        weakness_mapping[field] = list(dict.fromkeys(weakness_mapping[field] + values))


def output_maswe_data(
    mastg_mappings: dict[str, dict[str, list[str]]], repository_path: Path, edition: str, version: str
) -> dict[str, Any]:
    """Build enriched MASWE metadata mapped from MASTG tests and MASWE source files."""
    threats = parse_catalog(repository_path / ".github" / "instructions" / "threats.yaml", "MAS-THREAT-")
    attacks = parse_catalog(repository_path / ".github" / "instructions" / "attacks.yaml", "MAS-ATTACK-")
    mappings = {
        weakness_id: build_maswe_mapping(weakness_id, mapping, repository_path, threats, attacks)
        for weakness_id, mapping in collect_maswe_mappings(mastg_mappings).items()
    }
    return {"meta": {"edition": edition, "component": "maswe", "language": "ALL", "version": version}, **mappings}


def build_maswe_mapping(
    weakness_id: str,
    mapping: dict[str, list[str]],
    repository_path: Path,
    threats: dict[str, str],
    attacks: dict[str, str],
) -> dict[str, Any]:
    """Resolve a MASWE weakness's source metadata and catalog descriptions."""
    metadata = extract_maswe_metadata(repository_path, weakness_id)
    threat_id = metadata.pop("threat").removeprefix("MAS-THREAT-")
    attack_ids = [attack.removeprefix("MAS-ATTACK-") for attack in metadata.pop("attacks")]
    if threat_id not in threats or any(attack_id not in attacks for attack_id in attack_ids):
        raise ValueError(f"MASWE-{weakness_id}: referenced threat or attack is missing from its catalog")
    return {
        **mapping,
        **metadata,
        "owasp_mas_threat": {threat_id: threats[threat_id]},
        "owasp_mas_attack": {attack_id: attacks[attack_id] for attack_id in attack_ids},
    }
