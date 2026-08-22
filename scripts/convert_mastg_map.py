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

from scripts.mastg_mapping_sources import extract_mastg_mappings, output_data, output_maswe_data

FILENAME_COMPONENT_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}")


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


convert_vars = ConvertVars()


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
    parser.add_argument(
        "-v", "--version", type=validate_filename_component, default="2.0", help="Cornucopia version, for example 2.0"
    )
    parser.add_argument(
        "-e",
        "--edition",
        type=validate_filename_component,
        default="mobileapp",
        help="Cornucopia edition, for example mobileapp",
    )
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
        save_yaml_file(
            maswe_output_path,
            output_maswe_data(mappings, maswe_repository_path, convert_vars.args.edition, convert_vars.args.version),
        )
        logging.info("Generated %s with %d MASTG tests and %s", mastg_output_path, len(mappings), maswe_output_path)
    finally:
        for temporary_checkout in temporary_checkouts:
            temporary_checkout.cleanup()


if __name__ == "__main__":
    main()
