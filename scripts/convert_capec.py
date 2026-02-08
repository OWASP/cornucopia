#!/usr/bin/env python3
# This script converts the JSON from
# data/capec-3.9/3000.json
# to the file structure that our cornucopia website can understand.
import argparse
import logging
import shutil
import json
import os
import sys
import yaml
from pathlib import Path
from typing import Any, List
from pathvalidate.argparse import validate_filepath_arg


class ConvertVars:
    DEFAULT_OUTPUT_PATH = Path(__file__).parent / "../cornucopia.owasp.org/data/taxonomy/en/capec-3.9"
    DEFAULT_INPUT_PATH = Path(__file__).parent / "../cornucopia.owasp.org/data/capec-3.9/3000.json"
    DEFAULT_CAPEC_TO_ASVS_INPUT_PATH = Path(__file__).parent / "../source/webapp-capec-3.0.yaml"
    DEFAULT_ASVS_MAPPING_PATH = (
        Path(__file__).parent / "../cornucopia.owasp.org/data/asvs-5.0/en/"
        "OWASP_Application_Security_Verification_Standard_5.0.0_en.json"
    )
    LATEST_ASVS_VERSION_CHOICES: List[str] = ["5.0"]
    args: argparse.Namespace


def create_capec_pages(
    data: dict[str, Any],
    capec_to_asvs_map: dict[int, dict[str, List[str]]],
    asvs_map: dict[str, Any],
    asvs_version: str,
) -> None:
    data = data["Attack_Pattern_Catalog"]["Attack_Patterns"]
    directory = Path(__file__).parent.resolve()
    for i in data["Attack_Pattern"]:
        name = str(i["_ID"])
        capec_path = directory / convert_vars.args.output_path / name
        create_folder(capec_path)
        f = open(capec_path / "index.md", "w", encoding="utf-8")
        f.write(f"# CAPEC™ {i['_ID']}: {i['_Name']}\n\n")
        f.write("## Description\n\n")
        f.write(f"{parse_description(i.get('Description', ''))}\n\n")
        capec_id = int(i["_ID"])
        f.write(f"Source: [CAPEC™ {capec_id}](https://capec.mitre.org/data/definitions/{capec_id}.html)\n\n")
        if has_no_asvs_mapping(capec_id, capec_to_asvs_map):
            logging.debug("CAPEC ID %d has no ASVS mapping", capec_id)
        else:
            f.write("## Related ASVS Requirements\n\n")
            f.write(f"ASVS ({asvs_version}): \
{create_link_list(capec_to_asvs_map.get(capec_id, {}), asvs_map, asvs_version)}\n")

        f.close()
    logging.info("Created %d CAPEC pages", len(data["Attack_Pattern"]))


def has_no_asvs_mapping(capec_id: int, capec_to_asvs_map: dict[int, dict[str, List[str]]]) -> bool:
    return not capec_to_asvs_map.get(capec_id) or not capec_to_asvs_map.get(capec_id, {"owasp_asvs": []}).get(
        "owasp_asvs"
    )


def parse_description(description_field: Any) -> str:
    """Parse CAPEC description field which can be dict, list, or string."""
    if isinstance(description_field, dict):
        if "Description" in description_field and "p" in description_field["Description"]:
            p_content = description_field["Description"]["p"]
            if isinstance(p_content, dict) and "__text" in p_content:
                return str(p_content["__text"])
            elif isinstance(p_content, list):
                return " ".join(
                    [str(p["__text"]) if isinstance(p, dict) and "__text" in p else str(p) for p in p_content]
                )
    return str(description_field)


def create_link_list(requirements: dict[str, Any], asvs_map: dict[str, Any], asvs_version: str) -> str:
    link_list = ""
    asvs_requirements = requirements.get("owasp_asvs", [])
    if not asvs_requirements:
        logging.debug("No ASVS requirements found in requirements: %s", str(requirements))
        return ""
    sorted_requirements = sorted(asvs_requirements)
    for idx, shortcode in enumerate(sorted_requirements):
        link = createlink(asvs_map, shortcode, asvs_version)
        if idx > 0:
            link_list += ", "
        link_list += link
    return link_list


def createlink(data: dict[str, Any], shortcode: str, asvs_version: str) -> str:
    for i in data["Requirements"]:
        name = str(i["Ordinal"]).rjust(2, "0") + "-" + i["Name"].lower().replace(" ", "-").replace(",", "")

        for item in i["Items"]:
            itemname = (
                str(item["Ordinal"]).rjust(2, "0") + "-" + item["Name"].lower().replace(" ", "-").replace(",", "")
            )
            for subitem in item["Items"]:
                if shortcode in subitem["Shortcode"]:
                    return f"[{shortcode}](/taxonomy/asvs-{asvs_version}/{name}/{itemname}#{subitem['Shortcode']})"
    return shortcode if shortcode else ""


def validate_json_data(data: dict[str, Any]) -> bool:
    if not data:
        logging.error("No data provided")
        return False
    if "Attack_Pattern_Catalog" not in data:
        logging.error("Missing 'Attack_Pattern_Catalog' key in data")
        return False
    catalog = data["Attack_Pattern_Catalog"]
    if not isinstance(catalog, dict):
        logging.error("'Attack_Pattern_Catalog' is not a dictionary")
        return False
    if "Attack_Patterns" not in catalog:
        logging.error("Missing 'Attack_Patterns' key in 'Attack_Pattern_Catalog'")
        return False
    patterns = catalog["Attack_Patterns"]
    if not isinstance(patterns, dict):
        logging.error("'Attack_Patterns' is not a dictionary")
        return False
    if "Attack_Pattern" not in patterns:
        logging.error("Missing 'Attack_Pattern' key in 'Attack_Patterns'")
        return False
    if not isinstance(patterns["Attack_Pattern"], list):
        logging.error("'Attack_Pattern' is not a list")
        return False
    return True


def set_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s %(filename)s | %(levelname)s | %(funcName)s | %(message)s",
    )
    if convert_vars.args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)


def empty_folder(path: Path) -> None:
    try:
        # Empty the folder
        shutil.rmtree(path)
    except Exception as e:
        logging.error("Error while emptying folder %s: %s", str(path), str(e))


def create_folder(path: Path) -> None:
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        logging.error("Error while creating folder %s: %s", str(path), str(e))


def load_json_file(filepath: Path) -> dict[str, Any]:
    try:
        with open(filepath, encoding="utf8") as f:
            data: dict[str, Any] = json.load(f)
        return data
    except Exception as e:
        logging.error("Error while loading JSON file %s: %s", str(filepath), str(e))
        return {}


def load_capec_to_asvs_mapping(filepath: Path) -> dict[int, dict[str, List[str]]]:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data: dict[int, dict[str, List[str]]] = yaml.safe_load(f)
        logging.info("Successfully loaded YAML file: %s", filepath)
        return data
    except Exception as e:
        logging.error("Error loading YAML file %s: %s", filepath, str(e))
        return {}


def parse_arguments(input_args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert CAPEC JSON to Cornucopia format")
    parser.add_argument(
        "-o",
        "--output-path",
        type=validate_filepath_arg,
        default=ConvertVars.DEFAULT_OUTPUT_PATH,
        help="Path to store converted CAPEC files",
    )
    parser.add_argument(
        "-i",
        "--input-path",
        type=validate_filepath_arg,
        default=ConvertVars.DEFAULT_INPUT_PATH,
        help="Path to read CAPEC JSON files from",
    )
    parser.add_argument(
        "-ca",
        "--capec-to-asvs",
        type=validate_filepath_arg,
        default=ConvertVars.DEFAULT_CAPEC_TO_ASVS_INPUT_PATH,
        help="Path to read CAPEC to ASVS map source from, defaults to source/webapp-capec-3.0.yaml",
    )
    parser.add_argument(
        "-am",
        "--asvs-mapping",
        type=validate_filepath_arg,
        default=ConvertVars.DEFAULT_ASVS_MAPPING_PATH,
        help="Path to read ASVS mapping source from, defaults to "
        "taxonomy/en/ASVS-5.0/OWASP_Application_Security_Verification_Standard_5.0.0_en.json",
    )
    parser.add_argument(
        "-av",
        "--asvs-version",
        type=str,
        default="5.0",
        help="ASVS version to map to, defaults to 5.0",
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
        sys.exit()
    return args


def get_valid_version(version: str) -> str:
    for v in ConvertVars.LATEST_ASVS_VERSION_CHOICES:
        if version == v:
            return version
    return ConvertVars.LATEST_ASVS_VERSION_CHOICES[-1]


def main() -> None:

    convert_vars.args = parse_arguments(sys.argv[1:])
    asvs_version = get_valid_version(convert_vars.args.asvs_version)
    logging.debug("Using ASVS version: %s", asvs_version)
    set_logging()
    logging.info("Starting CAPEC conversion process")
    logging.debug(" --- args = %s", str(convert_vars.args))
    empty_folder(Path(convert_vars.args.output_path))
    create_folder(Path(convert_vars.args.output_path))
    capec_to_asvs_map: dict[int, dict[str, List[str]]] = {}
    data = load_json_file(Path(convert_vars.args.input_path))
    asvs_map: dict[str, Any] = load_json_file(Path(convert_vars.args.asvs_mapping))
    if not data or not validate_json_data(data):
        logging.error("Invalid CAPEC data structure")
        return
    if not asvs_map:
        logging.error("Failed to load ASVS mapping data")
        return
    capec_to_asvs_map = load_capec_to_asvs_mapping(Path(convert_vars.args.capec_to_asvs))
    if not capec_to_asvs_map:
        logging.error("Failed to load CAPEC to ASVS mapping")
        return
    create_capec_pages(data, capec_to_asvs_map, asvs_map, asvs_version)

    logging.info("CAPEC conversion process completed")


if __name__ == "__main__":
    convert_vars: ConvertVars = ConvertVars()
    main()
