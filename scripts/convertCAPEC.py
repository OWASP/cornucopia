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
from pathlib import Path
from typing import Any
from pathvalidate.argparse import validate_filepath_arg


class ConvertVars:
    DEFAULT_OUTPUT_PATH = Path(__file__).parent / "../cornucopia.owasp.org/data/taxonomy/en/CAPEC-3.9"
    DEFAULT_INPUT_PATH = Path(__file__).parent / "../cornucopia.owasp.org/data/capec-3.9/3000.json"
    args: argparse.Namespace


def createCAPECPages(data: dict[str, Any]) -> None:
    data = data["Attack_Pattern_Catalog"]["Attack_Patterns"]
    directory = Path(__file__).parent.resolve()
    for i in data["Attack_Pattern"]:
        name = str(i["_ID"])
        capecPath = directory / convert_vars.args.output_path / name
        create_folder(capecPath)

        f = open(capecPath / "index.md", "w", encoding="utf-8")
        f.write(f"# CAPEC-{i['_ID']}: {i['_Name']}\r\n")
        f.write("## Description\r\n")
        f.write(f"{parse_description(i['Description'])}\r\n")
        f.write(f"Source: [CAPEC-{i['_ID']}](https://capec.mitre.org/data/definitions/{i['_ID']}.html)\r\n")
        f.close()
    logging.info("Created %d CAPEC pages", len(data["Attack_Pattern"]))


def parse_description(description_field: dict[str, Any]) -> str:
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


def validate_json_data(data: dict[str, Any]) -> bool:
    if not data:
        logging.error("No data provided")
        return False
    if "Attack_Pattern_Catalog" not in data:
        logging.error("Missing 'Attack_Pattern_Catalog' key in data")
        return False
    if not isinstance(data["Attack_Pattern_Catalog"], dict):
        logging.error("'Attack_Pattern_Catalog' is not a dictionary")
        return False
    if "Attack_Patterns" not in data["Attack_Pattern_Catalog"]:
        logging.error("Missing 'Attack_Patterns' key in 'Attack_Pattern_Catalog'")
        return False
    if not isinstance(data["Attack_Pattern_Catalog"]["Attack_Patterns"], dict):
        logging.error("'Attack_Patterns' is not a dictionary")
        return False
    if "Attack_Pattern" not in data["Attack_Pattern_Catalog"]["Attack_Patterns"]:
        logging.error("Missing 'Attack_Pattern' key in 'Attack_Patterns'")
        return False
    if not isinstance(data["Attack_Pattern_Catalog"]["Attack_Patterns"]["Attack_Pattern"], list):
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
        "-d",
        "--debug",
        action="store_true",
        help="Output additional information to debug script",
    )
    try:
        args = parser.parse_args(input_args)
    except argparse.ArgumentError as exc:
        # sys.tracebacklimit = 0
        logging.error(exc.message)
        sys.exit()
    return args


def main() -> None:

    convert_vars.args = parse_arguments(sys.argv[1:])
    set_logging()
    logging.info("Starting CAPEC conversion process")
    logging.debug(" --- args = %s", str(convert_vars.args))
    directory = Path(__file__).parent.resolve()
    empty_folder(directory / ConvertVars.DEFAULT_OUTPUT_PATH)
    create_folder(directory / ConvertVars.DEFAULT_OUTPUT_PATH)

    data = load_json_file(directory / ConvertVars.DEFAULT_INPUT_PATH)
    if not validate_json_data(data):
        logging.error("Invalid CAPEC data structure")
        return
    createCAPECPages(data)

    logging.info("CAPEC conversion process completed")


if __name__ == "__main__":
    convert_vars: ConvertVars = ConvertVars()
    main()
