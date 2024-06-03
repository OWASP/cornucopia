#!/usr/bin/env python3
import argparse
import docx2pdf  # type: ignore
import docx  # type: ignore
import fnmatch
import logging
import os
import platform
import re
import shutil
import sys
import yaml
import zipfile
import xml.etree.ElementTree as ElTree
from typing import Any, Dict, Generator, List, Tuple, Union
from operator import itemgetter
from itertools import groupby
from pathvalidate.argparse import validate_filepath_arg
from pathvalidate import sanitize_filepath

import defusedxml.ElementTree


class ConvertVars:
    BASE_PATH = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
    EDITION_CHOICES: List[str] = ["all", "webapp", "mobileapp"]
    FILETYPE_CHOICES: List[str] = ["all", "docx", "pdf", "idml"]
    LAYOUT_CHOICES: List[str] = ["all", "leaflet", "guide", "cards"]
    LANGUAGE_CHOICES: List[str] = ["all", "en", "es", "fr", "nl", "no-nb", "pt-br"]
    VERSION_CHOICES: List[str] = ["all", "latest", "1.00", "1.22", "2.00"]
    LATEST_VERSION_CHOICES: List[str] = ["1.00", "2.00"]
    TEMPLATE_CHOICES: List[str] = ["all", "bridge", "bridge_qr", "tarot"]
    EDITION_VERSION_MAP: Dict[str, Dict[str, str]] = {
        "webapp": {"1.22": "1.22", "2.00": "2.00"},
        "mobileapp": {"1.00": "1.00"},
        "all": {"1.22": "1.22", "2.00": "2.00", "1.00": "1.00"},
    }
    DEFAULT_TEMPLATE_FILENAME: str = os.sep.join(
        ["resources", "templates", "owasp_cornucopia_edition_ver_layout_document_template_lang"]
    )
    DEFAULT_OUTPUT_FILENAME: str = os.sep.join(["output", "owasp_cornucopia_edition_ver_layout_document_template_lang"])
    args: argparse.Namespace
    can_convert_to_pdf: bool = False


def check_fix_file_extension(filename: str, file_type: str) -> str:
    if filename and not filename.endswith(file_type):
        filename_split = os.path.splitext(filename)
        if filename_split[1].strip(".").isnumeric():
            filename = filename + "." + file_type.strip(".")
        else:
            filename = ".".join([os.path.splitext(filename)[0], file_type.strip(".")])
        logging.debug(f" --- output_filename with new ext = {filename}")
    return filename


def check_make_list_into_text(var: List[str]) -> str:
    if not isinstance(var, list):
        return str(var)
    var = group_number_ranges(var)
    text_output = ", ".join(str(s) for s in var)
    if not text_output.strip():
        text_output = " - "

    return text_output


def convert_docx_to_pdf(docx_filename: str, output_pdf_filename: str) -> None:
    logging.debug(
        f" --- docx_file = {docx_filename} convert to {output_pdf_filename}\n--- starting pdf conversion now."
    )

    if convert_vars.can_convert_to_pdf:
        try:
            docx2pdf.convert(docx_filename, output_pdf_filename)
            logging.info(f"New file saved: {output_pdf_filename}")
        except Exception as e:
            error_msg = f"\nConvert error: {e}"
            logging.warning(error_msg)
    else:
        error_msg = (
            "Error. A temporary docx file was created in the output folder but cannot be converted "
            f"to pdf (yet) on operating system: {platform.system()}\n"
            "This does work on Windows and Mac with MS Word installed."
        )
        logging.warning(error_msg)

    # If not debugging then delete the temp file
    if not convert_vars.args.debug:
        os.remove(docx_filename)


def create_edition_from_template(
    layout: str, language: str = "en", template: str = "bridge", version: str = "1.22", edition: str = "webapp"
) -> None:

    # Get the list of available translation files
    yaml_files = get_files_from_of_type(os.sep.join([convert_vars.BASE_PATH, "source"]), "yaml")
    if not yaml_files:
        return

    mapping: Dict[str, Any] = get_mapping_for_edition(yaml_files, version, language, edition, template, layout)

    if not mapping:
        logging.warning(
            f"No mapping file found for version: {version}, lang: {language}, edition: {edition},"
            f" template: {template}, layout: {layout}"
        )
        return

    # Get the language data from the correct language file (checks vars.args.language to select the correct file)
    language_data: Dict[str, Dict[str, str]] = get_language_data(yaml_files, language, version, edition)

    # Get the dict of replacement data
    language_dict: Dict[str, str] = get_replacement_dict(language_data)

    # Get meta data from language data
    meta: Dict[str, str] = get_meta_data(language_data)

    if not meta:
        return

    template_doc: str = get_template_for_edition(layout, template, edition)
    if template_doc == "None":
        return
    file_name, file_extension = os.path.splitext(template_doc)
    logging.debug(f"template_doc: {template_doc}")
    # Name output file with correct edition, component, language & version
    output_file: str = rename_output_file(file_extension, template, layout, meta)
    ensure_folder_exists(os.path.dirname(output_file))

    # Work with docx file (and maybe convert to pdf afterwards)
    if file_extension in ".docx":
        # Get the input (template) document
        doc: docx.Document = get_docx_document(template_doc)
        language_dict.update(mapping)
        doc = replace_docx_inline_text(doc, language_dict)
        doc.save(output_file)
        if convert_vars.args.pdf:
            # If file type is pdf, then save a temp docx file, convert the docx to pdf
            temp_docx_file = os.sep.join([convert_vars.BASE_PATH, "output", "temp.docx"])
            save_docx_file(doc, temp_docx_file)
            convert_docx_to_pdf(temp_docx_file, output_file)
    elif file_extension == ".idml":
        language_dict.update(mapping)
        save_idml_file(template_doc, language_dict, output_file)

    logging.info(f"New file saved: {output_file}")


def valid_meta(meta: Dict[str, Any], language: str, edition: str, version: str, template: str, layout: str) -> bool:
    if not has_translation_for_edition(meta, language):
        logging.warning(
            f"Translation in {language} does not exist for edition: {edition}, version: {version} "
            "or the translation choices are missing from the meta -> languages section in the mappings file"
        )
        return False

    if not has_template_for_edition(meta, template) and not convert_vars.args.inputfile:
        logging.warning(
            f"The template: {template} does not exist for edition: {edition}, version: {version} "
            "or the template choices are missing from the meta templates section in the mappings file"
        )
        return False

    if not has_layout_for_edition(meta, layout) and not convert_vars.args.inputfile:
        logging.warning(
            f"The layout: {layout} does not exist for edition: {edition}, version: {version} "
            "or the layout choices are missing from the meta -> layouts section in the mappings file"
        )
        return False
    return True


def has_translation_for_edition(meta: Dict[str, Any], language: str) -> bool:
    if meta and "languages" in meta and language in meta["languages"]:
        return True
    return False


def has_template_for_edition(meta: Dict[str, Any], template: str) -> bool:
    if meta and "templates" in meta and template in meta["templates"]:
        return True
    return False


def has_layout_for_edition(meta: Dict[str, Any], layout: str) -> bool:
    if meta and "layouts" in meta and layout in meta["layouts"]:
        return True
    return False


def ensure_folder_exists(folder_path: str) -> None:
    """Check if folder exists and if not, create folders recursively."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def main() -> None:
    convert_vars.args = parse_arguments(sys.argv[1:])
    set_logging()
    logging.debug(" --- args = %s", str(convert_vars.args))

    set_can_convert_to_pdf()
    if convert_vars.args.pdf and not convert_vars.can_convert_to_pdf and not convert_vars.args.debug:
        logging.error(
            "Cannot convert to pdf on this system. "
            "Pdf conversion is available on Windows and Mac, if MS Word is installed"
        )
        return

    # Create output files
    for edition in get_valid_edition_choices():
        for layout in get_valid_layout_choices():
            for language in get_valid_language_choices():
                for template in get_valid_templates():
                    for version in get_valid_version_choices():
                        create_edition_from_template(layout, language, template, version, edition)


def parse_arguments(input_args: List[str]) -> argparse.Namespace:
    """Parse and validate the input arguments. Return object containing argument values."""
    description = "Tool to output OWASP Cornucopia playing cards into different file types and languages. "
    description += "\nExample usage: $ ./cornucopia/convert.py --pdf -lt guide -l es -v 2.00"
    description += "\nExample usage: c:\\cornucopia\\scripts\\convert.py -t bridge -lt cards -l fr -v 2.00 "
    description += "-o 'my_output_folder/owasp_cornucopia_edition_version_layout_language_template.idml'"
    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.RawTextHelpFormatter, exit_on_error=False
    )
    parser.add_argument(
        "-i",
        "--inputfile",
        type=validate_filepath_arg,
        default="",
        help=(
            "Input (template) file to use."
            f"\nDefault={convert_vars.DEFAULT_TEMPLATE_FILENAME}.(docx|idml)"
            "\nTemplate type is dependent on the file (-o) specified."
        ),
    )
    parser.add_argument(
        "-v",
        "--version",
        type=is_valid_string_argument,
        required=False,
        default="latest",
        help=(
            "Output version to produce. [`all`, `latest`, `1.00`, `1.22`, `2.00`] "
            "\nVersion 1.22 and 1.2x will deliver cards mapped to ASVS 3.0"
            "\nVersion 2.00 and 2.0x will deliver cards mapped to ASVS 4.0"
            "\nVersion 1.00 and 1.0x will deliver cards mapped to MASVS 2.0"
            "\nVersion all will deliver all versions"
            "\nVersion latest will deliver the latest deck versions"
        ),
    )
    parser.add_argument(
        "-o",
        "--outputfile",
        default="",
        type=validate_filepath_arg,
        help=(
            "Specify a path and name of output file to generate. (caution: existing file will be overwritten). "
            f"\ndefault = {convert_vars.DEFAULT_OUTPUT_FILENAME}.(docx|pdf|idml)"
        ),
    )
    parser.add_argument(
        "-p",
        "--pdf",
        action="store_true",
        default=False,
        help="whether to generate a pdf in addition to the printable document. Default = Does not generate pdf",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Output additional information to debug script",
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-l",
        "--language",
        type=is_valid_string_argument,
        default="en",
        help="Output language to produce. [`en`, `es`, `fr`, `nl`, `no-nb`, `pt-br`]",
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-t",
        "--template",
        type=is_valid_string_argument,
        default="bridge",
        help=(
            "From which template to produce the document. [`bridge`, `qr` or `tarot`]\n"
            "Templates need to be added to ./resource/templates or specified with (-i or --inputfile)\n"
            "Bridge cards are 2.25 x 3.5 inch and have the mappings printed on them, "
            "tarot cards are 2.75 x 4.75 (71 x 121 mm) inch large, "
            "qr cards have a QRCode that points to an maintained list."
        ),
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-e",
        "--edition",
        type=is_valid_string_argument,
        default="all",
        help=(
            "Output decks to produce. [`all`, `webapp` or `mobileapp`]\n"
            "The various Cornucopia decks. `web` will give you the Website App edition."
            "`mobileapp` will give you the Mobile App edition."
        ),
    )

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-lt",
        "--layout",
        type=is_valid_string_argument,
        default="all",
        help=(
            "Document layouts to produce. [`all`, `guide`, `leaflet` or `cards`]\n"
            "The various Cornucopia document layouts.\n"
            "`cards` will output the high quality print card deck.\n"
            "`guide` will generate the docx guide with the low quality print deck.\n"
            "`leaflet` will output the high quality print leaflet.\n"
        ),
    )
    try:
        args = parser.parse_args(input_args)
    except argparse.ArgumentError as exc:
        # sys.tracebacklimit = 0
        logging.error(exc.message)
        sys.exit()
    return args


def is_valid_string_argument(argument: str) -> str:
    if len(argument) > 255:
        raise argparse.ArgumentTypeError("The option can not have more the 255 char.")
    if not re.match(r"^[A-Za-z0-9._-]+$", argument):
        raise argparse.ArgumentTypeError(
            "The option can only contain a-z letters, numbers, periods, dash or underscore"
        )
    return argument


def is_valid_argument_list(arguments: List[str]) -> Any:
    if not isinstance(arguments, List):
        return arguments
    for argument in arguments:
        is_valid_string_argument(argument)
    return arguments


def get_card_ids(language_data: Union[Dict[Any, Any], List[Any]], key: str = "id") -> Generator[str, None, None]:
    if isinstance(language_data, dict):
        for k, v in language_data.items():
            if k == key:
                yield v
            if isinstance(v, (dict, list)):
                yield from get_card_ids(v, key)
    elif isinstance(language_data, list):
        for d in language_data:
            yield from get_card_ids(d, key)


def get_document_paragraphs(doc: docx) -> List[docx.Document]:
    paragraphs = list(doc.paragraphs)
    l1 = len(paragraphs)
    for table in doc.tables:
        paragraphs += get_paragraphs_from_table_in_doc(table)
    l2 = len(paragraphs)
    if not len(paragraphs):
        logging.error("No paragraphs found in doc")
    logging.debug(f" --- count doc paragraphs = {l1}, with table paragraphs = {l2}")
    return paragraphs


def get_docx_document(docx_file: str) -> docx.Document:
    """Open the file and return the docx document."""
    if os.path.isfile(docx_file):
        return docx.Document(docx_file)
    else:
        logging.error("Could not find file at: %s", str(docx_file))
        return docx.Document()


def get_files_from_of_type(path: str, ext: str) -> List[str]:
    """Get a list of files from a specified folder recursively, that have the specified extension."""
    files = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, "*." + str(ext)):
            files.append(os.path.join(root, filename))
    if not files:
        logging.error("No language files found in folder: %s", str(os.sep.join([convert_vars.BASE_PATH, "source"])))
        return files
    logging.debug(
        "%s%s", f" --- found {len(files)} files of type {ext}. Showing first few:\n* ", str("\n* ".join(files[:3]))
    )
    return files


def get_find_replace_list(meta: Dict[str, str], template: str, layout: str) -> List[Tuple[str, str]]:
    ll: List[Tuple[str, str]] = [
        ("_edition", "_" + meta["edition"].lower()),
        ("_layout", "_" + layout.lower()),
        ("_document_template", "_" + template.lower()),
        ("_lang", "_" + meta["language"].lower()),
        ("_ver", "_" + meta["version"].lower()),
    ]
    return ll


def get_full_tag(suit_tag: str, card: str, tag: str) -> str:
    if suit_tag == "WC":
        full_tag = "${{{}}}".format("_".join([suit_tag, card, tag]))
    elif suit_tag == "Common":
        full_tag = "${{{}}}".format("_".join([suit_tag, card]))
    else:
        full_tag = "${{{}}}".format("_".join([suit_tag, suit_tag + card, tag]))
    return full_tag


def get_mapping_for_edition(
    yaml_files: List[str], version: str, language: str, edition: str, template: str, layout: str
) -> Dict[str, Any]:
    mapping_data: Dict[str, Dict[str, str]] = get_mapping_data_for_edition(yaml_files, language, version, edition)
    if not mapping_data:
        logging.warning("Could not retrieve valid mapping information")
        return {}
    if "meta" not in mapping_data.keys() or not valid_meta(
        mapping_data["meta"], language, edition, version, template, layout
    ):
        logging.warning("Could not retrieve valid meta information from the mapping file")
        return {}
    return get_replacement_mapping_data(mapping_data)


def get_mapping_data_for_edition(
    yaml_files: List[str],
    language: str,
    version: str = "1.22",
    edition: str = "webapp",
) -> Dict[Any, Dict[Any, Any]]:
    """Get the raw data of the replacement text from correct yaml file"""
    data: Dict[Any, Dict[Any, Any]] = {}
    logging.debug(
        " --- Starting get_mapping_data_for_edition() for edition: "
        f"{edition} , language: {language} and version: {version} "
        f" with mapping to version {get_valid_mapping_for_version(version, edition)}"
    )
    mappingfile: str = ""
    for file in yaml_files:
        if is_yaml_file(file) and is_mapping_file_for_version(file, version, edition):
            mappingfile = file
    if not mappingfile:
        return data

    with open(mappingfile, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            logging.info(f"Error loading yaml file: {mappingfile}. Error = {e}")
            data = {}
    if "meta" in data.keys() and "component" in data["meta"].keys() and data["meta"]["component"] == "mappings":
        logging.debug(" --- found mappings file: " + os.path.split(mappingfile)[1])
    else:
        logging.debug(" --- found source file, but it was missing metadata: " + os.path.split(mappingfile)[1])
        if "meta" in list(data.keys()):
            meta_keys = data["meta"].keys()
            logging.debug(f" --- data.keys() = {data.keys()}, data[meta].keys() = {meta_keys}")
        data = {}
    logging.debug(f" --- Len = {len(data)}.")
    return data


def get_replacement_mapping_data(input_data: Dict[str, Any]) -> Dict[str, str]:
    """Loop through language file data and build up a find-replace dict"""
    data: Dict[str, Any] = {"meta": get_meta_data(input_data)}
    for key in list(k for k in input_data.keys() if k != "meta"):
        suit_tags, suit_key = get_suit_tags_and_key(key, input_data["meta"]["edition"])
        logging.debug(f" --- key = {key}.")
        logging.debug(f" --- suit_tags = {suit_tags}")
        logging.debug(f" --- suit_key = {suit_key}")

        for suit, suit_tag in zip(input_data[key], suit_tags):
            logging.debug(f" --- suit [name] = {suit['name']}")
            logging.debug(f" --- suit_tag = {suit_tag}")
            card_tag = ""
            for card in suit[suit_key]:
                for tag, text_output in card.items():
                    if tag == "value":
                        continue

                    full_tag = get_full_tag(suit_tag, card["value"], tag)

                    # Add a translation for "Joker"
                    if suit_tag == "WC" and tag == "value":
                        full_tag = "${{{}}}".format("_".join([suit_tag, card_tag, tag]))

                    data[full_tag] = check_make_list_into_text(text_output)
    return data


def get_meta_data(data: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
    meta = {}
    try:
        if "meta" in list(data.keys()):
            for key, value in data["meta"].items():
                if key in ("edition", "component", "language", "version", "languages", "layouts", "templates"):
                    meta[key] = (isinstance(value, str) and is_valid_string_argument(value)) or (
                        isinstance(value, List) and is_valid_argument_list(value)
                    )
            return meta
        else:
            logging.error(
                "Could not find meta tag in the language data. " "Please ensure the language file is available."
            )
        logging.debug(f" --- meta data = {meta}")
    except argparse.ArgumentError as exc:
        logging.error(f"Could not get meta because of invalid data. error: {exc.message}")
        return {}
    return meta


def get_paragraphs_from_table_in_doc(doc_table: docx.Document) -> List[docx.Document]:
    paragraphs: List[docx.Document] = []
    for row in doc_table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                if len(paragraph.runs):
                    paragraphs.append(paragraph)
            for t2 in cell.tables:
                paragraphs += get_paragraphs_from_table_in_doc(t2)
    return paragraphs


def get_language_data(
    yaml_files: List[str],
    language: str,
    version: str = "1.22",
    edition: str = "webapp",
) -> Dict[Any, Dict[Any, Any]]:
    """Get the raw data of the replacement text from correct yaml file"""
    logging.debug(
        f" --- Starting get_language_data() for edition: {edition} "
        "requesting language: {language} for version: {version} "
    )
    language_file: str = ""
    for file in yaml_files:
        if is_yaml_file(file) and is_lang_file_for_version(file, version, language, edition):
            language_file = file
    if not language_file:
        logging.debug(
            "Did not find translation for version: " + version + ", lang: " + language + ", edition: " + edition
        )
        return {}

    with open(language_file, "r", encoding="utf-8") as f:
        try:
            data: dict[Any, Any] = yaml.safe_load(f)
        except yaml.YAMLError as e:
            logging.info(f"Error loading yaml file: {language_file}. Error = {e}")
            data = {}

    if data["meta"]["language"].lower() == language:
        logging.debug(" --- found source language file: " + os.path.split(language_file)[1])
    else:
        logging.debug(" --- found source file: " + os.path.split(language_file)[1])
        if "meta" in list(data.keys()):
            meta_keys = data["meta"].keys()
            logging.debug(f" --- data.keys() = {data.keys()}, data[meta].keys() = {meta_keys}")
        data = {}

    if not data or "suits" not in list(data.keys()):
        logging.error(
            "Could not get "
            + language
            + " language data from yaml "
            + os.path.split(language_file)[1]
            + " for edition: "
            + edition
            + " under version:"
            + version
        )
    logging.debug(f" --- Len = {len(data)}.")
    return data


def is_mapping_file_for_version(path: str, version: str, edition: str) -> bool:
    return (
        os.path.basename(path).find("mappings") >= 0
        and os.path.basename(path).find(edition) >= 0
        and os.path.basename(path).find(version) >= 0
    )


def is_lang_file_for_version(path: str, version: str, lang: str, edition: str) -> bool:
    return (
        os.path.basename(path).find("-" + lang + ".") >= 0
        and os.path.basename(path).find(version) >= 0
        and os.path.basename(path).find(edition) >= 0
    ) or (
        os.path.basename(path).find("-" + lang.replace("-", "_") + ".") >= 0
        and os.path.basename(path).find(version) >= 0
        and os.path.basename(path).find(edition) >= 0
    )


def is_yaml_file(path: str) -> bool:
    return os.path.splitext(path)[1] in (".yaml", ".yml")


def get_replacement_dict(input_data: Dict[str, Any]) -> Dict[str, str]:
    """Loop through language file data and build up a find-replace dict"""
    data: Dict[str, str] = {}
    for key in list(k for k in input_data.keys() if k != "meta"):
        suit_tags, suit_key = get_suit_tags_and_key(key, is_valid_string_argument(input_data["meta"]["edition"]))
        logging.debug(f" --- key = {key}.")
        logging.debug(f" --- suit_tags = {suit_tags}")
        logging.debug(f" --- suit_key = {suit_key}")

        for suit, suit_tag in zip(input_data[key], suit_tags):
            logging.debug(f" --- suit [name] = {suit['name']}")
            logging.debug(f" --- suit_tag = {suit_tag}")
            data = update_tag_for_suit_name(data, suit, suit_tag)
            card_tag = ""
            for card in suit[suit_key]:
                for tag, text_output in card.items():
                    if tag == "value":
                        continue

                    full_tag = get_full_tag(suit_tag, card["value"], tag)

                    # Add a translation for "Joker"
                    if suit_tag == "WC" and tag == "value":
                        full_tag = "${{{}}}".format("_".join([suit_tag, card_tag, tag]))

                    data[full_tag] = check_make_list_into_text(text_output)
    if convert_vars.args.debug:
        debug_txt = " --- Translation data showing First 4 (key: text):\n* "
        debug_txt += "\n* ".join(l1 + ": " + str(data[l1]) for l1 in list(data.keys())[:4])
        logging.debug(debug_txt)
        debug_txt = " --- Translation data showing Last 4 (key: text):\n* "
        debug_txt += "\n* ".join(l1 + ": " + str(data[l1]) for l1 in list(data.keys())[-4:])
        logging.debug(debug_txt)
    return data


def update_tag_for_suit_name(data: Dict[str, str], suit: Dict[str, Any], suit_tag: str) -> Dict[str, str]:
    tag_for_suit_name = get_tag_for_suit_name(suit, suit_tag)
    data.update(tag_for_suit_name)
    return data


def get_replacement_mapping_value(k: str, v: str, el_text: str) -> str:
    reg_str: str = (
        "^(OWASP MASTG|OWASP MASVS|OWASP SCP|OWASP ASVS|OWASP AppSensor|CAPEC|SAFECODE)\u2028"
        + k.replace("$", "\\$").strip()
        + "$"
    )
    if re.match(reg_str, el_text.strip()):
        if len(v) >= 38:
            return el_text[: el_text.find("\u2028")] + ": " + v
        else:
            return el_text.replace(k, v)
    return ""


def get_replacement_value_from_dict(el_text: str, replacement_values: List[Tuple[str, str]]) -> str:
    for k, v in replacement_values:
        el_new = get_replacement_mapping_value(k, v, el_text)
        if el_new:
            return el_new
        if k.strip() in el_text:
            reg = r"(?<!\S)" + re.escape(k.strip()) + "(?!\S)"  # # noqa: W605
            el_text = re.sub(reg, v, el_text)
    return el_text


def get_suit_tags_and_key(key: str, edition: str) -> Tuple[List[str], str]:
    # Short tags to match the suits in the template documents
    suit_tags: List[str] = []
    suit_key: str = ""
    if key == "suits" and edition == "webapp":
        suit_tags = ["VE", "AT", "SM", "AZ", "CR", "CO", "WC"]
        suit_key = "cards"
    if key == "suits" and edition == "mobileapp":
        suit_tags = ["PC", "AA", "NS", "RS", "CRM", "COM", "WC"]
        suit_key = "cards"
    elif key == "paragraphs":
        suit_tags = ["Common"]
        suit_key = "sentences"
    return suit_tags, suit_key


def get_tag_for_suit_name(suit: Dict[str, Any], suit_tag: str) -> Dict[str, str]:
    data: Dict[str, str] = {}
    logging.debug(f" --- suit_tag = {suit_tag}, suit[name] = {suit['name']}")
    data["${{{}}}".format(suit_tag + "_suit")] = suit["name"]
    if suit_tag == "WC":
        data["${WC_Joker}"] = "Joker"
    return data


def get_template_for_edition(layout: str = "guide", template: str = "bridge", edition: str = "webapp") -> str:
    template_doc: str
    args_input_file: str = convert_vars.args.inputfile
    sfile_ext = "idml"
    if layout == "guide":
        sfile_ext = "docx"
    if args_input_file:
        # Input file was specified
        if os.path.isabs(args_input_file):
            template_doc = args_input_file
        elif os.path.isfile(convert_vars.BASE_PATH + os.sep + args_input_file):
            template_doc = os.path.normpath(convert_vars.BASE_PATH + os.sep + args_input_file)
        elif os.path.isfile(convert_vars.BASE_PATH + os.sep + args_input_file.replace(".." + os.sep, "")):
            template_doc = os.path.normpath(
                convert_vars.BASE_PATH + os.sep + args_input_file.replace(".." + os.sep, "")
            )
        elif args_input_file.find("..") == -1 and os.path.isfile(
            convert_vars.BASE_PATH + os.sep + ".." + os.sep + args_input_file
        ):
            template_doc = os.path.normpath(convert_vars.BASE_PATH + os.sep + ".." + os.sep + args_input_file)
        elif os.path.isfile(convert_vars.BASE_PATH + os.sep + args_input_file.replace("scripts" + os.sep, "")):
            template_doc = os.path.normpath(
                convert_vars.BASE_PATH + os.sep + args_input_file.replace("scripts" + os.sep, "")
            )
        else:
            template_doc = args_input_file
            logging.debug(f" --- Template_doc NOT found. Input File = {args_input_file}")
    else:
        # No input file specified - using defaults
        template_doc = os.path.normpath(
            convert_vars.BASE_PATH
            + os.sep
            + convert_vars.DEFAULT_TEMPLATE_FILENAME.replace("edition", edition)
            .replace("layout", layout)
            .replace("document_template", template)
            + "."
            + sfile_ext
        )

    template_doc = template_doc.replace("\\ ", " ")
    template_doc = sanitize_filepath(template_doc)
    if os.path.isfile(template_doc):
        template_doc = check_fix_file_extension(template_doc, sfile_ext)
        logging.debug(f" --- Returning template_doc = {template_doc}")
        return template_doc
    else:
        logging.error(f"Source file not found: {template_doc}. Please ensure file exists and try again.")
        return "None"


def get_valid_layout_choices() -> List[str]:
    layouts = []
    if convert_vars.args.layout.lower() == "all" or convert_vars.args.layout == "":
        for layout in convert_vars.LAYOUT_CHOICES:
            if layout not in ("all", "guide"):
                layouts.append(layout)
            if layout == "guide" and convert_vars.args.edition.lower() in "webapp":
                layouts.append(layout)
    else:
        layouts.append(convert_vars.args.layout)
    return layouts


def get_valid_language_choices() -> List[str]:
    languages = []
    if convert_vars.args.language.lower() == "all":
        for language in convert_vars.LANGUAGE_CHOICES:
            if language not in ("all", "template"):
                languages.append(language)
    elif convert_vars.args.language == "":
        languages.append("en")
    else:
        languages.append(convert_vars.args.language)
    return languages


def get_valid_version_choices() -> List[str]:
    versions = []
    edition: str = convert_vars.args.edition.lower()
    if convert_vars.args.version.lower() == "all":
        for version in convert_vars.VERSION_CHOICES:
            if version not in ("all", "latest") and not get_valid_mapping_for_version(version, edition) == "":
                versions.append(version)
    elif convert_vars.args.version == "" or convert_vars.args.version == "latest":
        for version in convert_vars.LATEST_VERSION_CHOICES:
            if not get_valid_mapping_for_version(version, edition) == "":
                versions.append(version)
    else:
        versions.append(convert_vars.args.version)

    if not versions:
        logging.debug(f"No deck with version: {convert_vars.args.version} for edition: {edition} exists")
    return versions


def get_valid_mapping_for_version(version: str, edition: str) -> str:
    return ConvertVars.EDITION_VERSION_MAP.get(edition, {}).get(version, "")


def get_valid_templates() -> List[str]:
    templates = []
    if convert_vars.args.template.lower() == "all":
        for template in [t for t in convert_vars.TEMPLATE_CHOICES if t not in ("all", "bridge_qr")]:
            templates.append(template)
    elif convert_vars.args.template == "":
        templates.append("bridge")
        templates.append("tarot")
    else:
        templates.append(convert_vars.args.template)
    return templates


def get_valid_edition_choices() -> List[str]:
    editions = []
    if convert_vars.args.edition.lower() == "all" or not convert_vars.args.edition.lower():
        for edition in convert_vars.EDITION_CHOICES:
            if edition not in "all":
                editions.append(edition)
    if convert_vars.args.edition and convert_vars.args.edition not in "all":
        editions.append(convert_vars.args.edition)
    return editions


def group_number_ranges(data: List[str]) -> List[str]:
    if len(data) < 2 or len([s for s in data if not str(s).isnumeric()]):
        return data
    list_ranges: List[str] = []
    data_numbers = [int(s) for s in data]
    for k, g in groupby(enumerate(data_numbers), lambda x: x[0] - x[1]):
        group: List[int] = list(map(itemgetter(1), g))
        group = list(map(int, group))
        if group[0] == group[-1]:
            list_ranges.append(str(group[0]))
        else:
            list_ranges.append(str(group[0]) + "-" + str(group[-1]))
    return list_ranges


def save_docx_file(doc: docx.Document, output_file: str) -> None:
    ensure_folder_exists(os.path.dirname(output_file))
    doc.save(output_file)


def save_idml_file(template_doc: str, language_dict: Dict[str, str], output_file: str) -> None:
    # Get the output path and temp output path to put the temp xml files
    output_path = convert_vars.BASE_PATH + os.sep + "output"
    temp_output_path = output_path + os.sep + "temp"
    # Ensure the output folder and temp output folder exist
    ensure_folder_exists(temp_output_path)
    logging.debug(" --- temp_folder for extraction of xml files = %s", str(temp_output_path))

    # Unzip source xml files and place in temp output folder
    with zipfile.ZipFile(template_doc) as idml_archive:
        idml_archive.extractall(temp_output_path)
        logging.debug(" --- namelist of first few files in archive = %s", str(idml_archive.namelist()[:5]))

    xml_files = get_files_from_of_type(temp_output_path, "xml")
    # Only Stories files have content to update
    for file in fnmatch.filter(xml_files, "*Stories*Story*"):
        if os.path.getsize(file) == 0:
            continue
        replace_text_in_xml_file(file, language_dict)

    # Zip the files as an idml file in output folder
    logging.debug(" --- finished replacing text in xml files. Now zipping into idml file")
    zip_dir(temp_output_path, output_file)

    # If not debugging, delete temp folder and files
    if not convert_vars.args.debug and os.path.exists(temp_output_path):
        shutil.rmtree(temp_output_path, ignore_errors=True)


def set_can_convert_to_pdf() -> bool:
    operating_system: str = sys.platform.lower()
    can_convert = operating_system.find("win") != -1 or operating_system.find("darwin") != -1
    convert_vars.can_convert_to_pdf = can_convert
    logging.debug(f" --- operating system = {operating_system}, can_convert_to_pdf = {convert_vars.can_convert_to_pdf}")
    return can_convert


def set_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s %(filename)s | %(levelname)s | %(funcName)s | %(message)s",
    )
    if convert_vars.args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)


def sort_keys_longest_to_shortest(replacement_dict: Dict[str, str]) -> List[Tuple[str, str]]:
    new_list = list((k, v) for k, v in replacement_dict.items())
    return sorted(new_list, key=lambda s: len(s[0]), reverse=True)


def remove_short_keys(replacement_dict: Dict[str, str], min_length: int = 8) -> Dict[str, str]:
    data2: Dict[str, str] = {}
    for key, value in replacement_dict.items():
        if len(key) >= min_length:
            data2[key] = value
    logging.debug(
        " --- Making template. Removed card_numbers. len replacement_dict = "
        f"{len(replacement_dict)}, len data2 = {len(data2)}"
    )
    return data2


def rename_output_file(file_extension: str, template: str, layout: str, meta: Dict[str, str]) -> str:
    """Rename output file replacing place-holders from meta dict (edition, component, language, version)."""
    args_output_file: str = convert_vars.args.outputfile
    logging.debug(f" --- args_output_file = {args_output_file}")
    if args_output_file:
        # Output file is specified as an argument
        if os.path.isabs(args_output_file):
            output_filename = args_output_file
        else:
            output_filename = os.path.normpath(convert_vars.BASE_PATH + os.sep + args_output_file)
    else:

        # No output file specified - using default
        output_filename = os.path.normpath(
            convert_vars.BASE_PATH + os.sep + convert_vars.DEFAULT_OUTPUT_FILENAME + file_extension
        )

    logging.debug(f" --- output_filename before fix extension = {output_filename}")
    output_filename = check_fix_file_extension(output_filename, file_extension)
    logging.debug(f" --- output_filename AFTER fix extension = {output_filename}")

    # Do the replacement of filename place-holders with metadata
    find_replace = get_find_replace_list(meta, template, layout)
    f = os.path.basename(output_filename)
    for r in find_replace:
        f = f.replace(*r)
    output_filename = os.path.dirname(output_filename) + os.sep + f
    output_filename = sanitize_filepath(output_filename)

    logging.debug(f" --- output_filename = {output_filename}")
    return output_filename


def replace_docx_inline_text(doc: docx.Document, data: Dict[str, str]) -> docx.Document:
    """Replace the text in the docx document."""
    logging.debug(" --- starting docx_replace")
    replacement_values = list(data.items())
    paragraphs = get_document_paragraphs(doc)
    for p in paragraphs:
        runs_text = "".join(r.text for r in p.runs)
        if runs_text.strip() == "":
            continue
        for key, val in replacement_values:
            replaced_key = False
            for i, run in enumerate(p.runs):
                if run.text.find(key) != -1:
                    p.runs[i].text = run.text.replace(key, val)
                    replaced_key = True
                    runs_text = runs_text.replace(key, val)
            if not replaced_key:
                if runs_text.find(key) != -1:
                    runs_text = runs_text.replace(key, val)
                    for i, r in enumerate(p.runs):
                        p.runs[i].text = ""
                    p.runs[0].text = runs_text

    logging.debug(" --- finished replacing text in doc")
    return doc


def replace_text_in_xml_file(filename: str, replacement_dict: Dict[str, str]) -> None:
    replacement_values = list(replacement_dict.items())
    try:
        tree = defusedxml.ElementTree.parse(filename)
    except ElTree.ParseError as e:
        logging.error(f" --- parsing xml file: {filename}. error = {e}")
        return

    all_content_elements = tree.findall(".//Content")

    for el in [el for el in all_content_elements]:
        if el.text == "" or el.text is None:
            continue
        el.text = get_replacement_value_from_dict(el.text, replacement_values)
        with open(filename, "bw") as f:
            f.write(ElTree.tostring(tree.getroot(), encoding="utf-8"))


def zip_dir(path: str, zip_filename: str) -> None:
    """Zip all the files recursively from path into zip_filename (excluding root path)"""
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(path):
            for file in files:
                f = os.path.join(root, file)
                zip_file.write(f, f[len(path) :])


if __name__ == "__main__":
    convert_vars: ConvertVars = ConvertVars()
    main()
