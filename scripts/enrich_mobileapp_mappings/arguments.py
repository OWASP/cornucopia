import argparse
import re
from pathlib import Path

from pathvalidate.argparse import validate_filepath_arg

DEFAULT_SOURCE_DIR = Path(__file__).resolve().parents[2] / "source"
FILENAME_COMPONENT_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}")


def validate_filename_component(value: str) -> str:
    """Allow only a single filename component for generated mapping names."""
    if not FILENAME_COMPONENT_PATTERN.fullmatch(value) or value in {".", ".."}:
        raise argparse.ArgumentTypeError("must contain only letters, digits, dots, underscores, and hyphens")
    return value


def parse_arguments(input_args: list[str]) -> argparse.Namespace:
    """Parse source and output locations for one edition/version mapping set."""
    parser = argparse.ArgumentParser(description="Enrich Mobile card mappings with MASTG and MASWE metadata")
    parser.add_argument(
        "-e",
        "--edition",
        type=validate_filename_component,
        default="mobileapp",
        help="Cornucopia edition, for example mobileapp",
    )
    parser.add_argument(
        "-v", "--version", type=validate_filename_component, default="2.0", help="Cornucopia version, for example 2.0"
    )
    parser.add_argument("-s", "--source-dir", type=validate_filepath_arg, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("-i", "--input-path", type=validate_filepath_arg, help="Card mapping YAML to enrich")
    parser.add_argument("--mastg-path", type=validate_filepath_arg, help="Generated MASTG metadata YAML")
    parser.add_argument("--maswe-path", type=validate_filepath_arg, help="Generated MASWE metadata YAML")
    parser.add_argument(
        "-o", "--output-path", type=validate_filepath_arg, help="Enriched mapping YAML; defaults to input"
    )
    return parser.parse_args(input_args)
