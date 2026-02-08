# This script converts the JSON from
# OWASP_Application_Security_Verification_Standard_5.0.0_en.json
# to the file structure that our cornucopia website can understand.
import argparse
import logging
import json
import os
import shutil
import sys
import yaml
from pathlib import Path
from pathvalidate.argparse import validate_filepath_arg

from typing import Any, List, TextIO


class ConvertVars:
    DEFAULT_OUTPUT_PATH = Path(Path(__file__).parent / "../cornucopia.owasp.org/data/taxonomy/en/ASVS-5.0")
    DEFAULT_INPUT_PATH = (
        Path(__file__).parent / "../cornucopia.owasp.org/data/asvs-5.0/en/"
        "OWASP_Application_Security_Verification_Standard_5.0.0_en.json"
    )
    DEFAULT_ASVS_TO_CAPEC_INPUT_PATH = Path(__file__).parent / "../source/webapp-asvs-3.0.yaml"
    LATEST_CAPEC_VERSION_CHOICES: List[str] = ["3.9"]
    LATEST_ASVS_VERSION_CHOICES: List[str] = ["5.0"]
    args: argparse.Namespace


def create_level_summary(level: int, arr: List[dict[str, Any]]) -> None:
    topic = ""
    category = ""
    os.mkdir(Path(convert_vars.args.output_path, f"level-{level}-controls"))
    f = open(Path(convert_vars.args.output_path, f"level-{level}-controls/index.md"), "w", encoding="utf-8")
    f.write(f"# Level {level} controls\n\n")
    f.write(f"Level {level} contains {len(arr)} controls listed below: \n\n")
    for link in arr:
        if link["topic"] != topic:
            topic = link["topic"]
            f.write(f"## {topic}\n\n")
        if link["cat"] != category:
            category = link["cat"]
            f.write(f"### {category}\n\n")
        shortdesc = link["description"].replace("Verify that", "").strip().capitalize()[0:50] + " ..."
        f.write(f"- [{link['name']}]({link['link']}) *{shortdesc}* \n\n")
    f.close()


def _format_directory_name(ordinal: int, name: str) -> str:
    """Format ordinal and name into directory-safe string."""
    return str(ordinal).rjust(2, "0") + "-" + name.lower().replace(" ", "-").replace(",", "")


def _get_level_requirement_text(level: int) -> str:
    """Get the requirement text for a given level."""
    level_texts = {
        1: "Required for Level 1, 2 and 3\n\n",
        2: "Required for Level 2 and 3\n\n",
        3: "Required for Level 3\n\n",
    }
    return level_texts.get(level, "")


def _write_disclaimer(file_handle: TextIO) -> None:
    """Write the OWASP ASVS disclaimer to the file."""
    file_handle.write("## Disclaimer\n\n")
    file_handle.write(
        "Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)."
        "For more information visit: "
        "[The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/)"
        " or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the "
        "[Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md)"
        " license."
    )
    file_handle.write("\n")


def _create_level_obj(
    subitem: dict[str, Any], requirement_name: str, item_name: str, asvs_version: str
) -> dict[str, Any]:
    """Create a level object for categorization."""
    shortcode = subitem["Shortcode"]
    description = subitem["Description"]
    link = f"/taxonomy/asvs-{asvs_version}/{requirement_name}/{item_name}#{shortcode}"
    return {
        "topic": requirement_name,
        "cat": item_name,
        "name": shortcode,
        "link": link,
        "description": description,
    }


def _categorize_by_level(
    subitem: dict[str, Any],
    requirement_name: str,
    item_name: str,
    L1: List[dict[str, Any]],
    L2: List[dict[str, Any]],
    L3: List[dict[str, Any]],
    asvs_version: str,
) -> None:
    """Categorize requirement by its level and add to appropriate list."""
    level = int(subitem["L"])
    obj = _create_level_obj(subitem, requirement_name, item_name, asvs_version)

    if level == 1:
        L1.append(obj)
    if level == 2:
        L2.append(obj)
    if level == 3:
        L3.append(obj)


def _write_subitem_content(
    file_handle: TextIO, subitem: dict[str, Any], asvs_map: dict[str, dict[str, List[str]]], capec_version: str
) -> None:
    """Write a single subitem's content to the file."""
    file_handle.write("## " + subitem["Shortcode"] + "\n\n")
    file_handle.write(subitem["Description"].encode("ascii", "ignore").decode("utf8", "ignore") + "\n\n")

    level = int(subitem["L"])
    level_text = _get_level_requirement_text(level)
    if level_text:
        file_handle.write(level_text)

    asvs_id = subitem["Shortcode"].replace("V", "")
    if has_no_capec_mapping(asvs_id, asvs_map):
        logging.info("ASVS ID %s has no CAPEC mapping", asvs_id)
    else:
        file_handle.write("### Related CAPEC™ Requirements\n\n")
        file_handle.write(f"CAPEC™ ({capec_version}): {create_link_list(asvs_map.get(asvs_id, {}), capec_version)}\n\n")

    logging.debug("object: %s", subitem)
    logging.debug("🟪")


def _process_requirement_item(
    item: dict[str, Any],
    requirement_name: str,
    asvs_map: dict[str, dict[str, List[str]]],
    capec_version: str,
    L1: List[dict[str, Any]],
    L2: List[dict[str, Any]],
    L3: List[dict[str, Any]],
    asvs_version: str,
) -> None:
    """Process a single requirement item and create its documentation."""
    item_name = _format_directory_name(item["Ordinal"], item["Name"])
    logging.debug(item)

    item_path = Path(convert_vars.args.output_path, requirement_name, item_name)
    os.mkdir(item_path)
    logging.debug("🟩")

    with open(item_path / "index.md", "w", encoding="utf-8") as f:
        f.write("# " + item["Name"].replace(",", "") + "\n\n")

        for subitem in item["Items"]:
            _write_subitem_content(f, subitem, asvs_map, capec_version)
            _categorize_by_level(subitem, requirement_name, item_name, L1, L2, L3, asvs_version)

        _write_disclaimer(f)


def create_asvs_pages(
    data: dict[str, Any], asvs_map: dict[str, dict[str, List[str]]], capec_version: str, asvs_version: str
) -> None:
    """Create ASVS documentation pages from JSON data."""
    L1: List[dict[str, Any]] = []
    L2: List[dict[str, Any]] = []
    L3: List[dict[str, Any]] = []

    for requirement in data["Requirements"]:
        requirement_name = _format_directory_name(requirement["Ordinal"], requirement["Name"])
        logging.debug(requirement_name)
        os.mkdir(Path(convert_vars.args.output_path, requirement_name))

        for item in requirement["Items"]:
            _process_requirement_item(item, requirement_name, asvs_map, capec_version, L1, L2, L3, asvs_version)

    create_level_summary(1, L1)
    create_level_summary(2, L2)
    create_level_summary(3, L3)


def has_no_capec_mapping(asvs_id: str, capec_to_asvs_map: dict[str, dict[str, List[str]]]) -> bool:
    return not capec_to_asvs_map.get(asvs_id) or not capec_to_asvs_map.get(asvs_id, {"capec_codes": []}).get(
        "capec_codes"
    )


def create_link_list(requirements: dict[str, Any], capec_version: str) -> str:
    link_list = ""
    asvs_requirements = requirements.get("capec_codes", [])
    if not asvs_requirements:
        logging.debug("No CAPEC requirements found in requirements: %s", str(requirements))
        return ""
    sorted_requirements = sorted(asvs_requirements)
    for idx, capec_code in enumerate(sorted_requirements):
        link = f"[{capec_code}](/taxonomy/capec-{capec_version}/{capec_code}/index.md)"
        if idx > 0:
            link_list += ", "
        link_list += link
    return link_list


def parse_arguments(input_args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert CAPEC™ JSON to Cornucopia format")
    parser.add_argument(
        "-o",
        "--output-path",
        type=validate_filepath_arg,
        default=ConvertVars.DEFAULT_OUTPUT_PATH,
        help="Path to store converted ASVS files",
    )
    parser.add_argument(
        "-i",
        "--input-path",
        type=validate_filepath_arg,
        default=ConvertVars.DEFAULT_INPUT_PATH,
        help="Path to read ASVS JSON files from",
    )
    parser.add_argument(
        "-ac",
        "--asvs-to-capec",
        type=validate_filepath_arg,
        default=ConvertVars.DEFAULT_ASVS_TO_CAPEC_INPUT_PATH,
        help="Path to read ASVS to CAPEC™ map source from, defaults to source/webapp-capec-3.0.yaml",
    )
    parser.add_argument(
        "-cv",
        "--capec-version",
        type=str,
        default="3.9",
        help="CAPEC™ version to map to, defaults to 3.9",
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


def get_valid_capec_version(version: str) -> str:
    for v in ConvertVars.LATEST_CAPEC_VERSION_CHOICES:
        if version == v:
            return version
    return ConvertVars.LATEST_CAPEC_VERSION_CHOICES[-1]


def get_valid_asvs_version(version: str) -> str:
    for v in ConvertVars.LATEST_ASVS_VERSION_CHOICES:
        if version == v:
            return version
    return ConvertVars.LATEST_ASVS_VERSION_CHOICES[-1]


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


def load_asvs_to_capec_mapping(filepath: Path) -> dict[str, dict[str, List[str]]]:
    data: dict[str, dict[str, List[str]]] = {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        logging.info("Successfully loaded YAML file: %s", filepath)
        return data
    except Exception as e:
        logging.error("Error loading YAML file %s: %s", filepath, str(e))
        return data


def main() -> None:
    convert_vars.args = parse_arguments(sys.argv[1:])
    asvs_version = get_valid_asvs_version(convert_vars.args.asvs_version)
    capec_version = get_valid_capec_version(convert_vars.args.capec_version)
    logging.debug("Using CAPEC version: %s", capec_version)
    set_logging()
    logging.info("Starting ASVS conversion process")
    logging.debug(" --- args = %s", str(convert_vars.args))
    empty_folder(Path(convert_vars.args.output_path))
    create_folder(Path(convert_vars.args.output_path))
    data = load_json_file(Path(convert_vars.args.input_path))
    asvs_map: dict[str, dict[str, List[str]]] = load_asvs_to_capec_mapping(Path(convert_vars.args.asvs_to_capec))

    create_asvs_pages(data, asvs_map, capec_version, asvs_version)
    logging.info("ASVS conversion process completed")


if __name__ == "__main__":
    convert_vars: ConvertVars = ConvertVars()
    main()
