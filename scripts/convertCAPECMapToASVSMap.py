#!/usr/bin/env python3
# This script converts the CAPEC mappings from webapp-mappings YAML files
# to a consolidated CAPEC-to-ASVS mapping file in source dir.
import argparse
import logging
import sys
from pathlib import Path
from typing import Any, Dict
from pathvalidate.argparse import validate_filepath_arg
import yaml


class ConvertVars:
    DEFAULT_INPUT_PATH = Path(__file__).parent / "../source/webapp-mappings-3.0.yaml"
    DEFAULT_OUTPUT_PATH = Path(__file__).parent / "../source/webapp-capec-3.0.yaml"
    args: argparse.Namespace


def extract_capec_mappings(data: dict[str, Any]) -> dict[int, set[str]]:
    """
    Extract CAPEC mappings from the suits->cards->capec_map structure
    and merge them into a unified map.

    Returns a dict where keys are CAPEC codes and values are sets of ASVS requirements.
    """
    capec_to_asvs_map: dict[int, set[str]] = {}

    if "suits" not in data:
        logging.warning("No 'suits' key found in data")
        return capec_to_asvs_map

    for suit in data["suits"]:
        _extract_capec_mapping_from_suit(suit, capec_to_asvs_map)

    logging.info("Extracted mappings for %d unique CAPEC codes", len(capec_to_asvs_map))
    return capec_to_asvs_map


def _extract_capec_mapping_from_suit(suit: dict[str, Any], capec_to_asvs_map: dict[int, set[str]]) -> None:
    """Process a single suit and extract CAPEC mappings from its cards."""
    if "cards" not in suit:
        return

    for card in suit["cards"]:
        _extract_capec_mapping_from_card(card, capec_to_asvs_map)


def _extract_capec_mapping_from_card(card: dict[str, Any], capec_to_asvs_map: dict[int, set[str]]) -> None:
    """Process a single card and extract its CAPEC mappings."""
    if "capec_map" not in card:
        return

    capec_map = card["capec_map"]
    if not isinstance(capec_map, dict):
        return

    for capec_code, asvs_reqs in capec_map.items():
        _extract_and_add_asvs_requirements(capec_code, asvs_reqs, capec_to_asvs_map)


def _extract_and_add_asvs_requirements(
    capec_code: int, asvs_reqs: dict[str, Any], capec_to_asvs_map: dict[int, set[str]]
) -> None:
    """Add ASVS requirements for a CAPEC code to the mapping."""
    if capec_code not in capec_to_asvs_map:
        capec_to_asvs_map[capec_code] = set()

    for req in asvs_reqs.get("owasp_asvs", []):
        capec_to_asvs_map[capec_code].add(req)


def convert_to_output_format(capec_map: dict[int, set[str]]) -> Dict[int, dict[str, list[str]]]:
    """
    Convert the internal mapping format to the output YAML format.
    """
    output = {}

    for capec_code, asvs_set in sorted(capec_map.items()):
        output[capec_code] = {"owasp_asvs": sorted(list(asvs_set))}

    return output


def load_yaml_file(filepath: Path) -> dict[str, Any]:
    """Load and parse a YAML file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        logging.info("Successfully loaded YAML file: %s", filepath)
        return data if data else {}
    except FileNotFoundError:
        logging.error("File not found: %s", filepath)
        return {}
    except yaml.YAMLError as e:
        logging.error("Error parsing YAML file %s: %s", filepath, str(e))
        return {}
    except Exception as e:
        logging.error("Error loading YAML file %s: %s", filepath, str(e))
        return {}


def save_yaml_file(filepath: Path, data: Dict[int, dict[str, list[str]]]) -> bool:
    """Save data as YAML file."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        logging.info("Successfully saved YAML file: %s", filepath)
        return True
    except Exception as e:
        logging.error("Error saving YAML file %s: %s", filepath, str(e))
        return False


def set_logging() -> None:
    """Configure logging based on debug flag."""
    logging.basicConfig(
        format="%(asctime)s %(filename)s | %(levelname)s | %(funcName)s | %(message)s",
    )
    if convert_vars.args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)


def parse_arguments(input_args: list[str]) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Convert webapp-mappings YAML to CAPEC-to-ASVS mapping format")
    parser.add_argument(
        "-i",
        "--input-path",
        type=validate_filepath_arg,
        default=ConvertVars.DEFAULT_INPUT_PATH,
        help="Path to input webapp-mappings YAML file",
    )
    parser.add_argument(
        "-o",
        "--output-path",
        type=validate_filepath_arg,
        default=ConvertVars.DEFAULT_OUTPUT_PATH,
        help="Path to save converted CAPEC-to-ASVS mapping YAML file",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Output additional information to debug script",
    )
    try:
        args = parser.parse_args(input_args)
    except argparse.ArgumentError as exc:
        logging.error(exc.message)
        sys.exit(1)
    return args


def main() -> None:
    """Main execution function."""
    convert_vars.args = parse_arguments(sys.argv[1:])
    set_logging()

    logging.info("Starting CAPEC-to-ASVS mapping conversion process")
    logging.debug(" --- args = %s", str(convert_vars.args))

    # Resolve paths
    directory = Path(__file__).parent.resolve()
    input_path = directory / convert_vars.args.input_path
    output_path = directory / convert_vars.args.output_path

    logging.info("Input file: %s", input_path)
    logging.info("Output file: %s", output_path)

    # Load input YAML
    data = load_yaml_file(input_path)
    if not data:
        logging.error("Failed to load input data or file is empty")
        sys.exit(1)

    # Extract and merge CAPEC mappings
    capec_map = extract_capec_mappings(data)
    if not capec_map:
        logging.warning("No CAPEC mappings found in input file")

    # Convert to output format
    output_data = convert_to_output_format(capec_map)

    # Save output YAML
    if not save_yaml_file(output_path, output_data):
        logging.error("Failed to save output file")
        sys.exit(1)

    logging.info("CAPEC-to-ASVS mapping conversion completed successfully")
    logging.info("Total CAPEC codes processed: %d", len(output_data))


if __name__ == "__main__":
    convert_vars: ConvertVars = ConvertVars()
    main()
