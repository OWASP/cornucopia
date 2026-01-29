#!/usr/bin/env python3
# This script takes JSON from
# cornucopia.owasp.org/data/capec-3.9/3000.json
# and extracts CAPEC information from entries under Attack_Pattern_Catalog -> Attack_Patterns -> Attack_Pattern
# Like the _Name and _ID and merges this with the source/webapp-capec-3.0.yaml mappings by matching the _ID with the
# dictionary keys and ensure that each CAPEC entry contains the name together with the existing owasp_asvs map entries.
# The enricher, by default, writes the enriched CAPEC mapping file to the source directory and by default also reads
# from the source directory and finds the file based on --input-path argument, --edition and --version arguments.
# By default, it looks for a file named edition-capec-latest.yaml in the source directory, but this can be changed
# by providing different values for --edition and --version arguments.
import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any
from pathvalidate.argparse import validate_filepath_arg
import yaml


class EnricherVars:
    TEMPLATE_FILE_NAME: str = "EDITION-capec-VERSION.yaml"
    DEFAULT_CAPEC_JSON_PATH = Path(__file__).parent / "../cornucopia.owasp.org/data/capec-3.9/3000.json"
    DEFAULT_SOURCE_DIR = Path(__file__).parent / "../source"
    args: argparse.Namespace


def extract_capec_names(json_data: dict[str, Any]) -> dict[int, str]:
    """
    Extract CAPEC ID to Name mappings from JSON data.

    Args:
        json_data: CAPEC JSON data containing Attack_Pattern_Catalog

    Returns:
        Dictionary mapping CAPEC IDs (as integers) to their names
    """
    capec_names: dict[int, str] = {}

    if "Attack_Pattern_Catalog" not in json_data:
        logging.warning("No 'Attack_Pattern_Catalog' key found in JSON data")
        return capec_names

    catalog = json_data["Attack_Pattern_Catalog"]
    if "Attack_Patterns" not in catalog:
        logging.warning("No 'Attack_Patterns' key found in catalog")
        return capec_names

    patterns = catalog["Attack_Patterns"]
    if "Attack_Pattern" not in patterns:
        logging.warning("No 'Attack_Pattern' key found in patterns")
        return capec_names

    attack_patterns = patterns["Attack_Pattern"]
    if not isinstance(attack_patterns, list):
        logging.warning("'Attack_Pattern' is not a list")
        return capec_names

    for pattern in attack_patterns:
        if "_ID" in pattern and "_Name" in pattern:
            capec_id = int(pattern["_ID"])
            capec_name = pattern["_Name"]
            capec_names[capec_id] = capec_name

    logging.info("Extracted %d CAPEC name mappings", len(capec_names))
    return capec_names


def enrich_capec_mappings(
    capec_mappings: dict[int, dict[str, Any]], capec_names: dict[int, str]
) -> dict[int, dict[str, Any]]:
    """
    Enrich CAPEC mappings with names from the CAPEC catalog.

    Args:
        capec_mappings: Existing CAPEC to ASVS mappings
        capec_names: CAPEC ID to name mappings

    Returns:
        Enriched mappings with 'name' field added to each CAPEC entry
    """
    enriched: dict[int, dict[str, Any]] = {}

    for capec_id, mapping_data in capec_mappings.items():
        enriched_entry = mapping_data.copy()

        if capec_id in capec_names:
            enriched_entry["name"] = capec_names[capec_id]
        else:
            logging.warning("No name found for CAPEC-%d", capec_id)
            enriched_entry["name"] = f"CAPEC-{capec_id}"

        enriched[capec_id] = enriched_entry

    logging.info("Enriched %d CAPEC mappings", len(enriched))
    return enriched


def load_json_file(filepath: Path) -> dict[str, Any]:
    """Load and parse a JSON file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        logging.info("Successfully loaded JSON file: %s", filepath)
        return data if data else {}
    except FileNotFoundError:
        logging.error("File not found: %s", filepath)
        return {}
    except json.JSONDecodeError as e:
        logging.error("Error parsing JSON file %s: %s", filepath, str(e))
        return {}
    except Exception as e:
        logging.error("Error loading JSON file %s: %s", filepath, str(e))
        return {}


def load_yaml_file(filepath: Path) -> dict[int, dict[str, Any]]:
    """Load and parse a YAML file with integer keys."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        logging.info("Successfully loaded YAML file: %s", filepath)

        # Convert string keys to integers
        if data:
            converted = {int(k): v for k, v in data.items()}
            return converted
        return {}
    except FileNotFoundError:
        logging.error("File not found: %s", filepath)
        return {}
    except yaml.YAMLError as e:
        logging.error("Error parsing YAML file %s: %s", filepath, str(e))
        return {}
    except Exception as e:
        logging.error("Error loading YAML file %s: %s", filepath, str(e))
        return {}


def save_yaml_file(filepath: Path, data: dict[int, dict[str, Any]]) -> bool:
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
    if enricher_vars.args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)


def parse_arguments(input_args: list[str]) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Enrich CAPEC mappings with names from CAPEC JSON catalog")
    parser.add_argument(
        "-c",
        "--capec-json",
        type=validate_filepath_arg,
        default=EnricherVars.DEFAULT_CAPEC_JSON_PATH,
        help="Path to CAPEC JSON file (3000.json)",
    )
    parser.add_argument(
        "-i",
        "--input-path",
        type=validate_filepath_arg,
        default=None,
        help="Path to input CAPEC mapping YAML file (overrides edition/version)",
    )
    parser.add_argument(
        "-v",
        "--version",
        type=str,
        default="latest",
        help="Version of the CAPEC mapping file (e.g., 3.0)",
    )
    parser.add_argument(
        "-e",
        "--edition",
        type=str,
        default="edition",
        help="Edition of the CAPEC mapping file (e.g., webapp or mobileapp)",
    )
    parser.add_argument(
        "-s",
        "--source-dir",
        type=validate_filepath_arg,
        default=EnricherVars.DEFAULT_SOURCE_DIR,
        help="Source directory containing CAPEC mapping files",
    )
    parser.add_argument(
        "-o",
        "--output-path",
        type=validate_filepath_arg,
        default=None,
        help="Path to save enriched CAPEC mapping YAML file (default: overwrites input)",
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
    enricher_vars.args = parse_arguments(sys.argv[1:])
    set_logging()

    logging.info("Starting CAPEC mapping enrichment process")
    logging.debug(" --- args = %s", str(enricher_vars.args))

    # Resolve paths
    directory = Path(enricher_vars.args.source_dir).resolve()

    # Determine input file path
    if enricher_vars.args.input_path:
        input_path = Path(enricher_vars.args.input_path).resolve()
    else:
        filename = EnricherVars.TEMPLATE_FILE_NAME.replace("EDITION", enricher_vars.args.edition).replace(
            "VERSION", enricher_vars.args.version
        )
        input_path = directory / filename

    # Determine output file path
    if enricher_vars.args.output_path:
        output_path = Path(enricher_vars.args.output_path).resolve()
    else:
        output_path = input_path  # Overwrite input by default

    capec_json_path = Path(enricher_vars.args.capec_json).resolve()

    logging.info("CAPEC JSON file: %s", capec_json_path)
    logging.info("Input YAML file: %s", input_path)
    logging.info("Output YAML file: %s", output_path)

    # Load CAPEC JSON
    json_data = load_json_file(capec_json_path)
    if not json_data:
        logging.error("Failed to load CAPEC JSON data or file is empty")
        sys.exit(1)

    # Extract CAPEC names
    capec_names = extract_capec_names(json_data)
    if not capec_names:
        logging.warning("No CAPEC names extracted from JSON")

    # Load existing CAPEC mappings
    capec_mappings = load_yaml_file(input_path)
    if not capec_mappings:
        logging.error("Failed to load CAPEC mappings or file is empty")
        sys.exit(1)

    # Enrich mappings
    enriched_mappings = enrich_capec_mappings(capec_mappings, capec_names)

    # Save enriched mappings
    if not save_yaml_file(output_path, enriched_mappings):
        logging.error("Failed to save enriched mappings")
        sys.exit(1)

    logging.info("CAPEC mapping enrichment completed successfully")
    logging.info("Total CAPEC entries enriched: %d", len(enriched_mappings))


if __name__ == "__main__":
    enricher_vars: EnricherVars = EnricherVars()
    main()
