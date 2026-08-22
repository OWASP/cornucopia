#!/usr/bin/env python3
"""Generate a MASTG beta-test metadata mapping for a Cornucopia mobile edition."""

import argparse
import logging
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml
from pathvalidate.argparse import validate_filepath_arg


MAX_YAML_FILE_SIZE_BYTES = 2 * 1024 * 1024
FILENAME_COMPONENT_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}")


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


class LeadingZeroStringDumper(yaml.SafeDumper):
    """YAML dumper that preserves zero-padded identifiers as strings."""


def represent_string(dumper: LeadingZeroStringDumper, value: str) -> yaml.ScalarNode:
    """Use single quotes for digit-only strings that start with zero."""
    style = "'" if re.fullmatch(r"0\d+", value) else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


LeadingZeroStringDumper.add_representer(str, represent_string)


class ConvertVars:
    """Converter configuration shared with logging setup."""

    MASTG_REPOSITORY_URL = "https://github.com/owasp/mastg.git"
    MASTG_REPOSITORY_REVISION = "d7fd7d45636ef9acbae89d0247e8dd748aa6918d"
    MASWE_REPOSITORY_URL = "https://github.com/owasp/maswe.git"
    MASWE_REPOSITORY_REVISION = "308b82b4bbe29166934fb5a621b40471cfea61db"
    DEFAULT_OUTPUT_PATH = Path(__file__).parent / "../source"
    args: argparse.Namespace


def parse_arguments(input_args: list[str]) -> argparse.Namespace:
    """Parse command-line options using the other mapping converters' conventions."""
    parser = argparse.ArgumentParser(description="Convert MASTG beta-test metadata to a Cornucopia mapping")
    parser.add_argument(
        "-i",
        "--input-path",
        type=validate_filepath_arg,
        help="Path to an existing MASTG repository checkout",
    )
    parser.add_argument(
        "--maswe-input-path",
        type=validate_filepath_arg,
        help="Path to an existing MASWE repository checkout",
    )
    parser.add_argument("-v", "--version", type=validate_filename_component, default="2.0", help="Cornucopia version, for example 2.0")
    parser.add_argument("-e", "--edition", type=validate_filename_component, default="mobileapp", help="Cornucopia edition, for example mobileapp")
    parser.add_argument(
        "-o",
        "--output-path",
        type=validate_filepath_arg,
        default=ConvertVars.DEFAULT_OUTPUT_PATH,
        help="Directory to save the generated MASTG mapping YAML file",
    )
    parser.add_argument("-d", "--debug", action="store_true", help="Output additional diagnostic information")
    return parser.parse_args(input_args)


def validate_filename_component(value: str) -> str:
    """Allow only a single filename component for generated mapping names."""
    if not FILENAME_COMPONENT_PATTERN.fullmatch(value) or value in {".", ".."}:
        raise argparse.ArgumentTypeError("must contain only letters, digits, dots, underscores, and hyphens")
    return value


def set_logging() -> None:
    """Configure logging from the parsed debug option."""
    logging.basicConfig(format="%(asctime)s %(filename)s | %(levelname)s | %(funcName)s | %(message)s")
    logging.getLogger().setLevel(logging.DEBUG if convert_vars.args.debug else logging.INFO)


def clone_repository(repository_url: str, revision: str, destination: Path) -> None:
    """Clone an official source repository at a reviewed commit without invoking a shell."""
    subprocess.run(
        ["git", "clone", "--no-checkout", "--depth", "1", repository_url, str(destination)],
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["git", "-C", str(destination), "fetch", "--depth", "1", "origin", revision],
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["git", "-C", str(destination), "checkout", "--detach", revision],
        check=True,
        capture_output=True,
        text=True,
    )


def clone_mastg(destination: Path) -> None:
    """Clone the official MASTG repository."""
    clone_repository(ConvertVars.MASTG_REPOSITORY_URL, ConvertVars.MASTG_REPOSITORY_REVISION, destination)


def clone_maswe(destination: Path) -> None:
    """Clone the official MASWE repository."""
    clone_repository(ConvertVars.MASWE_REPOSITORY_URL, ConvertVars.MASWE_REPOSITORY_REVISION, destination)


def extract_front_matter(test_file: Path) -> dict[str, Any]:
    """Parse a Markdown file's YAML front matter, returning an empty mapping when absent."""
    content = read_yaml_source(test_file)
    match = re.match(r"^---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|$)", content, re.DOTALL)
    if not match:
        return {}

    metadata = yaml.load(match.group(1), Loader=UniqueKeySafeLoader)
    return metadata if isinstance(metadata, dict) else {}


def read_yaml_source(path: Path) -> str:
    """Read a bounded YAML-bearing source file to limit resource consumption."""
    if path.stat().st_size > MAX_YAML_FILE_SIZE_BYTES:
        raise ValueError(f"{path}: file exceeds {MAX_YAML_FILE_SIZE_BYTES} byte limit")
    return path.read_text(encoding="utf-8")


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
    weakness = metadata.get("weakness")
    if weakness is not None:
        mapping["owasp_maswe"] = normalize_references([weakness], "MASWE-", test_file)

    knowledge = normalize_references(metadata.get("knowledge"), "MASTG-KNOW-", test_file)
    if knowledge:
        mapping["owasp_mastg_know"] = knowledge

    best_practices = normalize_references(metadata.get("best-practices"), "MASTG-BEST-", test_file)
    if best_practices:
        mapping["owasp_mastg_best"] = best_practices

    return test_id.removeprefix("MASTG-TEST-"), mapping


def extract_mastg_mappings(repository_path: Path) -> dict[str, dict[str, list[str]]]:
    """Extract reference mappings from all beta test files in a MASTG checkout."""
    tests_path = repository_path / "tests-beta"
    if not tests_path.is_dir():
        raise FileNotFoundError(f"MASTG beta tests directory not found: {tests_path}")

    mappings: dict[str, dict[str, list[str]]] = {}
    for test_file in sorted(tests_path.rglob("MASTG-TEST-*.md")):
        if not any(parent.name.startswith("MASVS-") for parent in test_file.parents):
            continue
        extracted = extract_test_mapping(test_file)
        if extracted is None:
            continue
        test_id, mapping = extracted
        if test_id in mappings:
            raise ValueError(f"Duplicate MASTG test identifier: {test_id}")
        mappings[test_id] = mapping
    return dict(sorted(mappings.items()))


def output_data(mappings: dict[str, dict[str, list[str]]], edition: str, version: str) -> dict[str, Any]:
    """Build the stable YAML structure consumed by Cornucopia."""
    return {
        "meta": {"edition": edition, "component": "mastg", "language": "ALL", "version": version},
        **mappings,
    }


def parse_catalog(path: Path, prefix: str) -> dict[str, str]:
    """Load a MAS threat or attack catalog as de-prefixed identifiers and descriptions."""
    catalog = yaml.load(read_yaml_source(path), Loader=UniqueKeySafeLoader)
    if not isinstance(catalog, dict):
        raise ValueError(f"{path}: expected a mapping")

    result: dict[str, str] = {}
    for identifier, description in catalog.items():
        if not isinstance(identifier, str) or not identifier.startswith(prefix) or not identifier[len(prefix) :].isdigit():
            raise ValueError(f"{path}: invalid {prefix} identifier {identifier!r}")
        if not isinstance(description, str):
            raise ValueError(f"{path}: {identifier} description must be a string")
        result[identifier.removeprefix(prefix)] = description
    return result


def extract_maswe_metadata(repository_path: Path, weakness_id: str) -> dict[str, Any]:
    """Extract MASVS, threat, and attack references for one MASWE weakness."""
    matches = list((repository_path / "weaknesses").glob(f"MASVS-*/MASWE-{weakness_id}.md"))
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one MASWE-{weakness_id} document, found {len(matches)}")

    metadata = extract_front_matter(matches[0])
    if metadata.get("id") != f"MASWE-{weakness_id}":
        raise ValueError(f"{matches[0]}: invalid MASWE identifier")

    mappings = metadata.get("mappings")
    if not isinstance(mappings, dict):
        raise ValueError(f"{matches[0]}: mappings must be a mapping")
    masvs = mappings.get("masvs-v2", [])
    attacks = metadata.get("attacks", [])
    threat = metadata.get("threat")
    if not isinstance(masvs, list) or not all(isinstance(item, str) for item in masvs):
        raise ValueError(f"{matches[0]}: masvs-v2 must be a list of strings")
    if not isinstance(attacks, list) or not all(isinstance(item, str) for item in attacks):
        raise ValueError(f"{matches[0]}: attacks must be a list of strings")
    if not isinstance(threat, str):
        raise ValueError(f"{matches[0]}: threat must be a string")

    return {"owasp_masvs": masvs, "threat": threat, "attacks": attacks}


def collect_maswe_mappings(mastg_mappings: dict[str, dict[str, list[str]]]) -> dict[str, dict[str, list[str]]]:
    """Invert MASTG mappings, retaining every test's knowledge and best-practice siblings."""
    result: dict[str, dict[str, list[str]]] = {}
    for test_id, mapping in mastg_mappings.items():
        for weakness_id in mapping.get("owasp_maswe", []):
            weakness_mapping = result.setdefault(weakness_id, {"owasp_mastg": [], "owasp_mastg_know": [], "owasp_mastg_best": []})
            for field, values in (
                ("owasp_mastg", [test_id]),
                ("owasp_mastg_know", mapping.get("owasp_mastg_know", [])),
                ("owasp_mastg_best", mapping.get("owasp_mastg_best", [])),
            ):
                for value in values:
                    if value not in weakness_mapping[field]:
                        weakness_mapping[field].append(value)
    return dict(sorted(result.items()))


def output_maswe_data(
    mastg_mappings: dict[str, dict[str, list[str]]], repository_path: Path, edition: str, version: str
) -> dict[str, Any]:
    """Build enriched MASWE metadata mapped from MASTG tests and MASWE source files."""
    threats = parse_catalog(repository_path / ".github" / "instructions" / "threats.yaml", "MAS-THREAT-")
    attacks = parse_catalog(repository_path / ".github" / "instructions" / "attacks.yaml", "MAS-ATTACK-")
    mappings: dict[str, Any] = {}
    for weakness_id, mapping in collect_maswe_mappings(mastg_mappings).items():
        metadata = extract_maswe_metadata(repository_path, weakness_id)
        threat_id = metadata.pop("threat").removeprefix("MAS-THREAT-")
        attack_ids = [attack.removeprefix("MAS-ATTACK-") for attack in metadata.pop("attacks")]
        if threat_id not in threats or any(attack_id not in attacks for attack_id in attack_ids):
            raise ValueError(f"MASWE-{weakness_id}: referenced threat or attack is missing from its catalog")
        mappings[weakness_id] = {
            **mapping,
            **metadata,
            "owasp_mas_threat": {threat_id: threats[threat_id]},
            "owasp_mas_attack": {attack_id: attacks[attack_id] for attack_id in attack_ids},
        }
    return {"meta": {"edition": edition, "component": "maswe", "language": "ALL", "version": version}, **mappings}


def save_yaml_file(output_path: Path, data: dict[str, Any]) -> None:
    """Write generated YAML with stable key order and UTF-8 text."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as output_file:
        yaml.dump(data, output_file, Dumper=LeadingZeroStringDumper, allow_unicode=True, sort_keys=False)


def main() -> None:
    """Clone or read MASTG and generate the requested versioned mapping file."""
    convert_vars.args = parse_arguments(sys.argv[1:])
    set_logging()

    temporary_checkouts: list[tempfile.TemporaryDirectory[str]] = []
    try:
        if convert_vars.args.input_path:
            repository_path = Path(convert_vars.args.input_path).resolve()
        else:
            temporary_checkout = tempfile.TemporaryDirectory(prefix="cornucopia-mastg-")
            temporary_checkouts.append(temporary_checkout)
            repository_path = Path(temporary_checkout.name) / "mastg"
            clone_mastg(repository_path)

        if convert_vars.args.maswe_input_path:
            maswe_repository_path = Path(convert_vars.args.maswe_input_path).resolve()
        else:
            temporary_checkout = tempfile.TemporaryDirectory(prefix="cornucopia-maswe-")
            temporary_checkouts.append(temporary_checkout)
            maswe_repository_path = Path(temporary_checkout.name) / "maswe"
            clone_maswe(maswe_repository_path)

        mappings = extract_mastg_mappings(repository_path)
        output_directory = Path(convert_vars.args.output_path).resolve()
        mastg_output_path = output_directory / f"{convert_vars.args.edition}-mastg-{convert_vars.args.version}.yaml"
        maswe_output_path = output_directory / f"{convert_vars.args.edition}-maswe-{convert_vars.args.version}.yaml"
        save_yaml_file(mastg_output_path, output_data(mappings, convert_vars.args.edition, convert_vars.args.version))
        save_yaml_file(maswe_output_path, output_maswe_data(mappings, maswe_repository_path, convert_vars.args.edition, convert_vars.args.version))
        logging.info("Generated %s with %d MASTG tests and %s", mastg_output_path, len(mappings), maswe_output_path)
    finally:
        for temporary_checkout in temporary_checkouts:
            temporary_checkout.cleanup()


if __name__ == "__main__":
    convert_vars = ConvertVars()
    main()