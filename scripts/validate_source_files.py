"""
Source File Validator for OWASP Cornucopia.

Validates syntax, structure, and mapping schema integrity for source YAML files.
Can be executed locally or in GitHub Actions on changed files in a pull request.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


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


ASVS_ID_PATTERN = re.compile(r"^(-|\d+(\.\d+)+)$")
CAPEC_ID_PATTERN = re.compile(r"^(-|\d+)$")
SAFECODE_ID_PATTERN = re.compile(r"^(-|\d+)$")

VALID_STRIDE_VALUES = {
    "S",
    "T",
    "R",
    "I",
    "D",
    "E",
    "Spoofing",
    "Tampering",
    "Repudiation",
    "Information Disclosure",
    "Denial of Service",
    "Elevation of Privilege",
}


class SourceValidator:
    """Validates YAML structure and schema integrity of Cornucopia source files."""

    def __init__(self, catalog_dir: Path | None = None) -> None:
        self.errors: list[str] = []
        self.catalog_dir = catalog_dir
        self._asvs_catalog_cache: dict[Path, set[str]] = {}
        self._current_meta: dict[str, Any] = {}
        self._current_content: dict[str, Any] = {}

    def validate_file(self, file_path: Path) -> bool:
        """Validate a single source file. Returns True if valid, False otherwise."""
        if not file_path.is_file():
            self.errors.append(f"{file_path}: File does not exist or is not a regular file")
            return False

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = yaml.load(f, Loader=UniqueKeySafeLoader)  # nosec B506
        except Exception as exc:
            self.errors.append(f"{file_path}: Failed to parse YAML: {exc}")
            return False

        if content is None:
            self.errors.append(f"{file_path}: YAML file is empty")
            return False

        if not isinstance(content, dict):
            self.errors.append(f"{file_path}: Root content must be a mapping (dictionary)")
            return False

        initial_error_count = len(self.errors)

        raw_meta = content.get("meta")
        self._current_meta = raw_meta if isinstance(raw_meta, dict) else {}
        self._current_content = content

        # Enforce required meta section across all source file categories
        self._validate_meta(file_path, raw_meta)

        self._dispatch_by_filename(file_path, content)
        return len(self.errors) == initial_error_count

    def _dispatch_by_filename(self, file_path: Path, content: dict[str, Any]) -> bool:
        """Route file content to appropriate validator based on filename convention."""
        filename = file_path.name
        component = self._current_meta.get("component")

        if "mappings" in filename or component == "mappings":
            return self._validate_mappings_file(file_path, content)
        if "cards" in filename or component == "cards":
            return self._validate_cards_file(file_path, content)
        if "asvs" in filename:
            return self._validate_catalog_file(file_path, content, ASVS_ID_PATTERN, "ASVS")
        if "capec" in filename or "mastg" in filename or "maswe" in filename:
            name = "CAPEC" if "capec" in filename else ("MASTG" if "mastg" in filename else "MASWE")
            return self._validate_catalog_file(file_path, content, CAPEC_ID_PATTERN, name)
        if component == "asvs":
            return self._validate_catalog_file(file_path, content, ASVS_ID_PATTERN, "ASVS")
        if component in ("capec", "mastg", "maswe"):
            name = "CAPEC" if component == "capec" else ("MASTG" if component == "mastg" else "MASWE")
            return self._validate_catalog_file(file_path, content, CAPEC_ID_PATTERN, name)

        return self._validate_generic_yaml(file_path, content)

    def _validate_meta(self, file_path: Path, meta: Any) -> bool:
        """Validate the meta section of a source file."""
        if not isinstance(meta, dict):
            self.errors.append(f"{file_path}: Missing or invalid 'meta' section (must be a dictionary)")
            return False

        required_keys = ["edition", "component", "version"]
        for key in required_keys:
            if key not in meta or meta[key] is None or not str(meta[key]).strip():
                self.errors.append(f"{file_path}: 'meta' section missing required key '{key}'")
                return False
        return True

    def _get_asvs_candidate_patterns(self) -> list[str]:
        """Determine candidate catalog filenames based on metadata and labels."""
        edition = self._current_meta.get("edition")
        version = self._current_meta.get("version")

        labels = self._current_content.get("labels", {}) if isinstance(self._current_content, dict) else {}
        asvs_label = str(labels.get("owasp_asvs", labels.get("asvs", "")))
        match = re.search(r"(\d+(\.\d+)*)", asvs_label)
        referenced_asvs_version = match.group(1) if match else None

        candidates: list[str] = []
        if referenced_asvs_version == "5.0":
            candidates.extend(["webapp-asvs-3.0.yaml", "*-asvs-5.0.yaml"])
        elif referenced_asvs_version and referenced_asvs_version.startswith("4.0"):
            candidates.extend(
                [
                    "*-asvs-4.0*.yaml",
                    f"{edition}-asvs-4.0*.yaml",
                    "OWASP_Application_Security_Verification_Standard_4.0.3.flat.json",
                    "OWASP Application Security Verification Standard 4.0.3-*.json",
                ]
            )
        elif referenced_asvs_version:
            candidates.extend(
                [f"*-asvs-{referenced_asvs_version}.yaml", f"{edition}-asvs-{referenced_asvs_version}.yaml"]
            )

        if edition and version and not referenced_asvs_version:
            candidates.append(f"{edition}-asvs-{version}.yaml")

        return candidates

    def _find_catalog_file(self, search_dirs: list[Path], candidate_patterns: list[str]) -> Path | None:
        """Search given directories for matching catalog files."""
        for d in search_dirs:
            for pattern in candidate_patterns:
                if "*" in pattern:
                    matches = sorted(d.glob(pattern))
                    if matches and matches[0].is_file():
                        return matches[0]
                elif (d / pattern).is_file():
                    return d / pattern

            if self.catalog_dir and not candidate_patterns:
                fallback = sorted(d.glob("*-asvs-*.yaml"))
                if fallback and fallback[0].is_file():
                    return fallback[0]

        return None

    def _parse_catalog_keys(self, catalog_path: Path) -> set[str] | None:
        """Parse non-meta dictionary keys from catalog YAML or JSON."""
        try:
            if catalog_path.suffix == ".json":
                with open(catalog_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    reqs = data.get("requirements")
                    if isinstance(reqs, list):
                        return {
                            str(r["req_id"]).lstrip("V").strip()
                            for r in reqs
                            if isinstance(r, dict) and "req_id" in r and r["req_id"] is not None
                        }
                    return {str(k).strip() for k in data.keys() if k != "meta"}
                return None

            with open(catalog_path, "r", encoding="utf-8") as f:
                data = yaml.load(f, Loader=UniqueKeySafeLoader)  # nosec B506
            if isinstance(data, dict):
                return {str(k).strip() for k in data.keys() if k != "meta"}
        except Exception:
            return None
        return None

    def _load_asvs_catalog_keys(self, file_path: Path) -> set[str] | None:
        """Load and cache valid ASVS IDs from the matching catalog if available."""
        search_dirs: list[Path] = []
        if self.catalog_dir:
            search_dirs.append(self.catalog_dir)
        search_dirs.append(file_path.parent)

        resolved_parent = file_path.resolve().parent
        repo_asvs_4_dir = resolved_parent.parent / "cornucopia.owasp.org" / "data" / "asvs-4.0.3" / "en"
        if repo_asvs_4_dir.is_dir() and repo_asvs_4_dir not in search_dirs:
            search_dirs.append(repo_asvs_4_dir)

        candidate_patterns = self._get_asvs_candidate_patterns()
        catalog_path = self._find_catalog_file(search_dirs, candidate_patterns)

        if not catalog_path or not catalog_path.is_file():
            return None

        if catalog_path in self._asvs_catalog_cache:
            return self._asvs_catalog_cache[catalog_path]

        keys = self._parse_catalog_keys(catalog_path)
        if keys is not None:
            self._asvs_catalog_cache[catalog_path] = keys
        return keys

    def _validate_mappings_file(self, file_path: Path, content: dict[str, Any]) -> bool:
        """Validate structure and mapping tokens of a *-mappings-*.yaml file."""
        initial_error_count = len(self.errors)

        suits = content.get("suits")
        if not isinstance(suits, list):
            self.errors.append(f"{file_path}: 'suits' must be a list of suits")
            return False

        for suit in suits:
            if not isinstance(suit, dict):
                self.errors.append(f"{file_path}: Suit entry must be a dictionary")
                continue

            suit_name = str(suit.get("name", suit.get("id", "Unknown")))
            cards = suit.get("cards")
            if not isinstance(cards, list):
                self.errors.append(f"{file_path}: Suit '{suit_name}' must contain a 'cards' list")
                continue

            for card in cards:
                if not isinstance(card, dict):
                    self.errors.append(f"{file_path}: Card in suit '{suit_name}' must be a dictionary")
                    continue

                card_id = card.get("id", "Unknown")
                self._validate_card_mappings(file_path, suit_name, card_id, card)

        return len(self.errors) == initial_error_count

    def _validate_card_mappings(self, file_path: Path, suit_name: str, card_id: Any, card: dict[str, Any]) -> None:
        """Validate individual card mapping fields (ASVS, CAPEC, STRIDE, capec_map, etc.)."""
        context = f"{file_path} [{suit_name} -> {card_id}]"

        if "owasp_asvs" in card:
            self._validate_asvs_mapping(context, card["owasp_asvs"], file_path)

        if "capec" in card:
            self._validate_capec_mapping(context, card["capec"])

        if "safecode" in card:
            self._validate_safecode_mapping(context, card["safecode"])

        if "stride" in card:
            self._validate_stride_mapping(context, card["stride"])

        if "capec_map" in card:
            self._validate_capec_map(context, card["capec_map"], file_path)

        if "owasp_cre" in card and not isinstance(card["owasp_cre"], dict):
            self.errors.append(f"{context}: 'owasp_cre' must be a dictionary")

    def _validate_capec_map(self, context: str, capec_map: Any, file_path: Path) -> None:
        """Validate capec_map dictionary and its child mappings."""
        if not isinstance(capec_map, dict):
            self.errors.append(f"{context}: 'capec_map' must be a dictionary")
            return

        for capec_id, child_mappings in capec_map.items():
            child_context = f"{context} [capec_map -> {capec_id}]"
            raw_id = str(capec_id)
            if raw_id != raw_id.strip():
                self.errors.append(f"{child_context}: CAPEC key '{capec_id}' contains surrounding whitespace")
                continue
            if not CAPEC_ID_PATTERN.match(raw_id):
                self.errors.append(f"{child_context}: CAPEC key '{capec_id}' must be numeric")
            if not isinstance(child_mappings, dict):
                self.errors.append(f"{child_context}: Mapping for CAPEC '{capec_id}' must be a dictionary")
                continue
            if "owasp_asvs" in child_mappings:
                self._validate_asvs_mapping(child_context, child_mappings["owasp_asvs"], file_path)

    def _validate_asvs_mapping(self, context: str, asvs_list: Any, file_path: Path | None = None) -> None:
        """Validate ASVS entries within a card mapping, including catalog reference integrity."""
        if not isinstance(asvs_list, list):
            self.errors.append(f"{context}: 'owasp_asvs' must be a list")
            return

        known_catalog_keys: set[str] | None = None
        if file_path:
            known_catalog_keys = self._load_asvs_catalog_keys(file_path)

        for item in asvs_list:
            raw_token = str(item)
            if raw_token != raw_token.strip():
                self.errors.append(f"{context}: Malformed ASVS ID '{item}' contains surrounding whitespace")
                continue
            if " " in raw_token:
                self.errors.append(
                    f"{context}: Malformed ASVS entry '{raw_token}' (space-separated tokens not allowed)"
                )
                continue

            token = raw_token.strip()
            if not ASVS_ID_PATTERN.match(token):
                self.errors.append(f"{context}: Malformed ASVS ID '{token}' (must match dotted numeric pattern X.Y.Z)")
            elif token != "-":
                if known_catalog_keys is None:
                    self.errors.append(
                        f"{context}: Unable to resolve authoritative ASVS catalog for reference validation"
                    )
                    break
                elif token not in known_catalog_keys:
                    self.errors.append(f"{context}: ASVS ID '{token}' does not exist in authoritative catalog")

    def _validate_capec_mapping(self, context: str, capec_list: Any) -> None:
        """Validate CAPEC entries within a card mapping."""
        if not isinstance(capec_list, list):
            self.errors.append(f"{context}: 'capec' must be a list")
            return

        for item in capec_list:
            raw_token = str(item)
            if raw_token != raw_token.strip():
                self.errors.append(f"{context}: Malformed CAPEC ID '{item}' contains surrounding whitespace")
                continue
            if not CAPEC_ID_PATTERN.match(raw_token):
                self.errors.append(f"{context}: Malformed CAPEC ID '{raw_token}' (must be numeric)")

    def _validate_safecode_mapping(self, context: str, safecode_list: Any) -> None:
        """Validate SAFECode entries within a card mapping."""
        if not isinstance(safecode_list, list):
            self.errors.append(f"{context}: 'safecode' must be a list")
            return

        for item in safecode_list:
            raw_token = str(item)
            if raw_token != raw_token.strip():
                self.errors.append(f"{context}: Malformed SAFECode ID '{item}' contains surrounding whitespace")
                continue
            if not SAFECODE_ID_PATTERN.match(raw_token):
                self.errors.append(f"{context}: Malformed SAFECode ID '{item}' (must be numeric or '-')")

    def _validate_stride_mapping(self, context: str, stride_list: Any) -> None:
        """Validate STRIDE entries within a card mapping."""
        if not isinstance(stride_list, list):
            self.errors.append(f"{context}: 'stride' must be a list")
            return

        for item in stride_list:
            raw_token = str(item)
            if not raw_token.strip():
                self.errors.append(f"{context}: Empty STRIDE token found")
                continue
            if raw_token != raw_token.strip():
                self.errors.append(f"{context}: Malformed STRIDE token '{item}' contains surrounding whitespace")
                continue
            if raw_token not in VALID_STRIDE_VALUES:
                self.errors.append(f"{context}: Invalid STRIDE token '{raw_token}'")

    def _validate_cards_file(self, file_path: Path, content: dict[str, Any]) -> bool:
        """Validate a *-cards-*.yaml file."""
        initial_error_count = len(self.errors)

        suits = content.get("suits")
        if not isinstance(suits, list):
            self.errors.append(f"{file_path}: 'suits' must be a list")
            return False

        for suit in suits:
            if not isinstance(suit, dict):
                self.errors.append(f"{file_path}: Suit entry must be a dictionary")
                continue
            if "name" not in suit or suit["name"] is None or not str(suit["name"]).strip():
                self.errors.append(f"{file_path}: Suit entry missing 'name'")
            if "id" not in suit or suit["id"] is None or not str(suit["id"]).strip():
                self.errors.append(f"{file_path}: Suit entry missing 'id'")

            cards = suit.get("cards")
            if not isinstance(cards, list):
                self.errors.append(f"{file_path}: Suit '{suit.get('name')}' must contain a 'cards' list")
                continue

            for card in cards:
                if not isinstance(card, dict):
                    self.errors.append(f"{file_path}: Card in suit '{suit.get('name')}' must be a dictionary")
                    continue
                if "id" not in card or card["id"] is None or not str(card["id"]).strip():
                    self.errors.append(f"{file_path}: Card missing 'id' in suit '{suit.get('name')}'")

        return len(self.errors) == initial_error_count

    def _validate_catalog_file(
        self,
        file_path: Path,
        content: dict[str, Any],
        key_pattern: re.Pattern[str],
        catalog_name: str,
    ) -> bool:
        """Validate catalog reference files like *-asvs-*.yaml, *-capec-*.yaml, etc."""
        initial_error_count = len(self.errors)

        for key, val in content.items():
            if key == "meta":
                continue
            raw_key = str(key)
            if raw_key != raw_key.strip():
                self.errors.append(
                    f"{file_path}: Malformed {catalog_name} catalog key '{key}' contains surrounding whitespace"
                )
                continue
            if " " in raw_key:
                self.errors.append(f"{file_path}: Malformed {catalog_name} catalog key '{raw_key}' contains whitespace")
            elif not key_pattern.match(raw_key):
                self.errors.append(
                    f"{file_path}: Malformed {catalog_name} catalog key '{raw_key}' does not match pattern"
                )

            if not isinstance(val, dict):
                self.errors.append(f"{file_path}: Catalog entry '{raw_key}' must be a dictionary")
                continue

            context = f"{file_path} [{catalog_name} {raw_key}]"
            if "owasp_asvs" in val:
                self._validate_asvs_mapping(context, val["owasp_asvs"], file_path)
            if "capec_codes" in val:
                self._validate_capec_mapping(context, val["capec_codes"])
            if catalog_name in ("MASTG", "MASWE"):
                for field in ("owasp_maswe", "owasp_mastg", "owasp_mastg_know", "owasp_mastg_best"):
                    references = val.get(field)
                    if references is not None and (
                        not isinstance(references, list) or not all(isinstance(item, str) for item in references)
                    ):
                        self.errors.append(f"{context}: '{field}' must be a list of strings")

        return len(self.errors) == initial_error_count

    def _validate_generic_yaml(self, file_path: Path, content: dict[str, Any]) -> bool:
        """Basic validation for other source YAML files."""
        if not content:
            self.errors.append(f"{file_path}: YAML file contains no data")
            return False
        return True


def parse_arguments(argv: list[str]) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate YAML structure and schema integrity of Cornucopia source files."
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Specific YAML files to validate (e.g. source/webapp-mappings-3.0.yaml)",
    )
    parser.add_argument(
        "--source-dir",
        type=str,
        default=None,
        help="Directory containing source YAML files to validate",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Entry point for the validator."""
    if argv is None:
        argv = sys.argv[1:]

    args = parse_arguments(argv)
    validator = SourceValidator()
    files_to_validate: list[Path] = []

    if args.files:
        for f in args.files:
            p = Path(f)
            files_to_validate.append(p)
    elif args.source_dir:
        src_path = Path(args.source_dir)
        if src_path.is_dir():
            files_to_validate.extend(sorted(src_path.glob("*.yaml")))
        else:
            print(f"Error: Directory '{args.source_dir}' does not exist", file=sys.stderr)
            return 1

    if not files_to_validate:
        print("No source files specified for validation. Pass file paths or --source-dir.")
        return 0

    print(f"Validating {len(files_to_validate)} source file(s)...")
    for file_path in files_to_validate:
        validator.validate_file(file_path)

    if validator.errors:
        print(
            f"\n[FAILED] Found {len(validator.errors)} validation error(s):",
            file=sys.stderr,
        )
        for err in validator.errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("[PASSED] All source files passed validation successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
