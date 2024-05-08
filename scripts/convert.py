#!/usr/bin/env python3
import argparse
import docx2pdf  # type: ignore
import docx  # type: ignore
import fnmatch
import logging
import os
import platform
import pyqrcode  # type: ignore
import re
import shutil
import sys
import yaml
import zipfile
import xml.etree.ElementTree as ElTree
from typing import Any, Dict, Generator, List, Tuple, Union
from operator import itemgetter
from itertools import groupby


class ConvertVars:
    BASE_PATH = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
    EDITION_CHOICES: List[str] = ["all", "webapp", "mobileapp"]
    FILETYPE_CHOICES: List[str] = ["all", "docx", "pdf", "idml"]
    LANGUAGE_CHOICES: List[str] = ["template", "all", "en", "es", "fr", "nl", "no-nb", "pt-br"]
    VERSION_CHOICES: List[str] = ["all", "latest", "1.00", "1.20", "1.21", "1.22", "2.00"]
    LATEST_VERSION_CHOICES: List[str] = ["1.00", "2.00"]
    STYLE_CHOICES: List[str] = ["all", "static", "dynamic", "leaflet"]
    DEFAULT_TEMPLATE_FILENAME: str = os.sep.join(
        ["resources", "templates", "owasp_cornucopia_edition_lang_ver_template"]
    )
    DEFAULT_OUTPUT_FILENAME: str = os.sep.join(["output", "owasp_cornucopia_edition_component_lang_ver"])
    args: argparse.Namespace
    can_convert_to_pdf: bool = False
    making_template: bool = False


def check_fix_file_extension(filename: str, file_type: str) -> str:
    if filename and not filename.endswith(file_type):
        filename_split = os.path.splitext(filename)
        if filename_split[1].strip(".").isnumeric():
            filename = filename + "." + file_type.strip(".")
        else:
            filename = ".".join([os.path.splitext(filename)[0], file_type.strip(".")])
        logging.debug(f" --- output_filename with new ext = {filename}")
    return filename


def check_make_list_into_text(var: List[str], group_numbers: bool = True) -> str:
    if not isinstance(var, list):
        return str(var)

    if group_numbers:
        var = group_number_ranges(var)

    text_output = ", ".join(str(s) for s in var)
    if not text_output.strip():
        text_output = " - "

    return text_output


def convert_docx_to_pdf(docx_filename: str, output_pdf_filename: str) -> str:
    logging.debug(f" --- docx_file = {docx_filename}\n--- starting pdf conversion now.")

    if convert_vars.can_convert_to_pdf:
        try:
            docx2pdf.convert(docx_filename, output_pdf_filename)
        except Exception as e:
            error_msg = f"\nConvert error: {e}"
            logging.warning(error_msg)
            return docx_filename

    else:
        error_msg = (
            f"Error. A temporary docx file was created in the output folder but cannot be converted "
            f"to pdf (yet) on operating system: {platform.system()}\n"
            "This does work on Windows and Mac with MS Word installed."
        )
        logging.warning(error_msg)
        return docx_filename

    # If not debugging then delete the temp file
    if not convert_vars.args.debug:
        os.remove(docx_filename)

    return output_pdf_filename


def convert_type_language_style(
    file_type: str, language: str = "en", style: str = "static", version: str = "1.21", edition: str = "webapp"
) -> None:
    if has_not_valid_file_style(style, edition, file_type):
        return
    if not get_valid_mapping_for_version(version, edition):
        logging.debug("No deck with version: " + version + " for edition: " + edition + " exists")
        return
    # Get the list of available translation files
    yaml_files = get_files_from_of_type(os.sep.join([convert_vars.BASE_PATH, "source"]), "yaml")
    if not yaml_files:
        return

    # Get the language data from the correct language file (checks vars.args.language to select the correct file)
    language_data: Dict[str, Dict[str, str]] = get_replacement_data(
        yaml_files, "translation", language, version, edition
    )

    # Get the dict of replacement data
    language_dict: Dict[str, str] = get_replacement_dict(language_data, False)

    # Get meta data from language data
    meta: Dict[str, str] = get_meta_data(language_data)

    mapping_dict: Dict[str, str] = get_mapping_dict(yaml_files, version, language, edition)

    if convert_vars.making_template:
        language_dict = remove_short_keys(language_dict)

    template_doc: str = get_template_doc(file_type, style, edition)

    if has_no_matching_translations(language_data, mapping_dict, meta):
        logging.debug(
            "Has not matching translations for deck with language: "
            + language
            + ", version: "
            + version
            + ", style: "
            + style
            + ", edition: "
            + edition
        )
        return

    # Name output file with correct edition, component, language & version
    output_file: str = rename_output_file(file_type, style, meta)
    ensure_folder_exists(os.path.dirname(output_file))

    generate_qr_code_images(style, language_data)

    # Work with docx file (and maybe convert to pdf afterwards)
    if file_type in ("docx", "pdf"):
        # Get the input (template) document
        doc: docx.Document = get_docx_document(template_doc)
        if convert_vars.making_template:
            doc = replace_docx_inline_text(doc, language_dict)
            doc = replace_docx_inline_text(doc, mapping_dict)
        else:
            language_dict.update(mapping_dict)
            doc = replace_docx_inline_text(doc, language_dict)

        if file_type == "docx":
            doc.save(output_file)
        else:
            # If file type is pdf, then save a temp docx file, convert the docx to pdf
            temp_docx_file = os.sep.join([convert_vars.BASE_PATH, "output", "temp.docx"])
            save_docx_file(doc, temp_docx_file)
            output_file = convert_docx_to_pdf(temp_docx_file, output_file)

    elif file_type == "idml":
        language_dict.update(mapping_dict)
        save_idml_file(template_doc, language_dict, output_file)

    logging.info("New file saved: " + str(output_file))


def has_no_matching_translations(
    language_data: Dict[str, Dict[str, str]], mapping_dict: Dict[str, str], meta: Dict[str, str]
) -> bool:
    if not language_data or not mapping_dict or not meta:
        return True
    return False


# Generate QR Code images if required
def generate_qr_code_images(style: str, language_data: Dict[str, Dict[str, str]]) -> None:
    if style == "dynamic":
        for card_id in get_card_ids(language_data, "id"):
            save_qrcode_image(card_id, convert_vars.args.url)


def ensure_folder_exists(folder_path: str) -> None:
    """Check if folder exists and if not, create folders recursively."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def main() -> None:
    convert_vars.args = parse_arguments(sys.argv[1:])
    set_logging()
    logging.debug(" --- args = " + str(convert_vars.args))

    set_can_convert_to_pdf()
    if (
        convert_vars.args.outputfiletype == "pdf"
        and not convert_vars.can_convert_to_pdf
        and not convert_vars.args.debug
    ):
        logging.error(
            "Cannot convert to pdf on this system. "
            "Pdf conversion is available on Windows and Mac, if MS Word is installed"
        )
        return

    set_making_template()

    # Create output files
    for edition in get_valid_edition_choices():
        for file_type in get_valid_file_types():
            for language in get_valid_language_choices():
                for style in get_valid_styles():
                    for version in get_valid_version_choices():
                        convert_type_language_style(file_type, language, style, version, edition)


def parse_arguments(input_args: List[str]) -> argparse.Namespace:
    """Parse and validate the input arguments. Return object containing argument values."""
    description = "Tool to output OWASP Cornucopia playing cards into different file types and languages. "
    description += "\nExample usage: $ ./cornucopia/convert.py -t docx -l es -v 2.00"
    description += "\nExample usage: c:\\cornucopia\\scripts\\convert.py -t idml -l fr -v 2.00"
    description += "-o 'my_output_folder/owasp_cornucopia_edition_language_version.idml'"
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "-i",
        "--inputfile",
        type=str,
        default="",
        help=(
            "Input (template) file to use."
            f"\nDefault={convert_vars.DEFAULT_TEMPLATE_FILENAME}.(docx|idml)"
            "\nTemplate type is dependent on output type (-t) or file (-o) specified."
        ),
    )
    parser.add_argument(
        "-v",
        "--version",
        type=str,
        choices=convert_vars.VERSION_CHOICES,
        required=False,
        default="latest",
        help=(
            "Output version to produce. [`all`, `latest`, `1.00`, `1.20`, `1.21`, `1.22`, `2.00`] "
            "\nVersion 1.20 and 1.2x will deliver cards mapped to ASVS 3.0.1"
            "\nVersion 2.00 and 2.0x will deliver cards mapped to ASVS 4.0"
            "\nVersion 1.00 and 1.0x will deliver cards mapped to MASVS 2.0"
            "\nVersion all will deliver all versions"
            "\nVersion latest will deliver the latest deck versions"
        ),
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-t",
        "--outputfiletype",
        type=str,
        choices=convert_vars.FILETYPE_CHOICES,
        help="Type of file to output. Default = docx. If specified, this overwrites the output file extension",
    )
    parser.add_argument(
        "-o",
        "--outputfile",
        default="",
        type=str,
        help=(
            "Specify a path and name of output file to generate. (caution: existing file will be overwritten). "
            f"\ndefault = {convert_vars.DEFAULT_OUTPUT_FILENAME}.(docx|pdf|idml)"
        ),
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-l",
        "--language",
        type=str,
        choices=convert_vars.LANGUAGE_CHOICES,
        default="en",
        help=(
            "Output language to produce. [`en`, `es`, `fr`, `nl`, `no-nb`, `pt-br`, `template`] "
            "\nTemplate will attempt to create a template from the english input file and "
            "\nreplacing strings with the template lookup codes"
        ),
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Output additional information to debug script",
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-s",
        "--style",
        type=str,
        choices=convert_vars.STYLE_CHOICES,
        default="static",
        help=(
            "Output style to produce. [`static`, `dynamic` or `leaflet`]\n"
            "Static cards have the mappings printed on them, dynamic ones a QRCode that points to an maintained list."
            "The leaflet contains the instructions"
        ),
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-e",
        "--edition",
        type=str,
        choices=convert_vars.EDITION_CHOICES,
        default="all",
        help=(
            "Output decks to produce. [`all`, `webapp` or `mobileapp`]\n"
            "The various Cornucopia decks. `web` will give you the web webapp edition."
            "`mobileapp` will give you the MASVS/MASTG edition."
        ),
    )

    parser.add_argument(
        "-u",
        "--url",
        default="https://copi.securedelivery.io/cards",
        type=str,
        help=(
            "Specify a URL to use in generating dynamic cards. (caution: URL will be suffixed with / and the card ID). "
        ),
    )
    args = parser.parse_args(input_args)
    return args


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
        logging.error("Could not find file at: " + str(docx_file))
        return docx.Document()


def get_files_from_of_type(path: str, ext: str) -> List[str]:
    """Get a list of files from a specified folder recursively, that have the specified extension."""
    files = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, "*." + str(ext)):
            files.append(os.path.join(root, filename))
    if not files:
        logging.error("No language files found in folder: " + str(os.sep.join([convert_vars.BASE_PATH, "source"])))
    logging.debug(f" --- found {len(files)} files of type {ext}. Showing first few:\n* " + str("\n* ".join(files[:3])))
    return files


def get_find_replace_list(meta: Dict[str, str], file_type: str) -> List[Tuple[str, str]]:
    if file_type in ["docx", "pdf"]:
        meta["component"] = "guide"
    ll: List[Tuple[str, str]] = [
        ("_type", "_" + meta["edition"].lower()),
        ("_edition", "_" + meta["edition"].lower()),
        ("_component", "_" + meta["component"].lower()),
        ("_language", "_" + meta["language"].lower()),
        ("_lang", "_" + meta["language"].lower()),
        ("_version", "_" + meta["version"].lower()),
        ("_ver", "_" + meta["version"].lower()),
    ]
    if not convert_vars.making_template:
        ll.append(("_template", ""))
    return ll


def get_full_tag(suit_tag: str, card: str, tag: str) -> str:
    if suit_tag == "WC":
        full_tag = "${{{}}}".format("_".join([suit_tag, card, tag]))
    elif suit_tag == "Common":
        full_tag = "${{{}}}".format("_".join([suit_tag, card]))
    else:
        full_tag = "${{{}}}".format("_".join([suit_tag, suit_tag + card, tag]))
    return full_tag


def get_mapping_dict(
    yaml_files: List[str], version: str = "1.21", language: str = "en", edition: str = "webapp"
) -> Dict[str, str]:
    mapping_data: Dict[str, Dict[str, str]] = get_replacement_data(yaml_files, "mappings", language, version, edition)
    if not mapping_data:
        return {}
    return get_replacement_dict(mapping_data, True)


def get_meta_data(language_data: Dict[str, Dict[str, str]]) -> Dict[str, str]:
    meta = {}
    if "meta" in list(language_data.keys()):
        for key, value in language_data["meta"].items():
            if key in ("edition", "component", "language", "version"):
                meta[key] = value
        return meta
    else:
        logging.error("Could not find meta tag in the language data. " "Please ensure the language file is available.")
    logging.debug(f" --- meta data = {meta}")
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


def get_replacement_data(
    yaml_files: List[str],
    data_type: str = "translation",
    language: str = "",
    version: str = "1.21",
    edition: str = "webapp",
) -> Dict[Any, Dict[Any, Any]]:
    """Get the raw data of the replacement text from correct yaml file"""
    data = {}
    logging.debug(
        f" --- Starting get_replacement_data() for data_type: {data_type}, language: {language} and version: {version} "
        f"     with mapping to version {get_valid_mapping_for_version(version, edition)}"
    )
    if convert_vars.making_template:
        lang = "en"
    else:
        lang = language
    for file in yaml_files:
        if is_yaml_file(file) and (
            is_lang_file_for_version(file, version, lang, edition)
            or is_mapping_file_for_version(file, version, edition)
        ):
            with open(file, "r", encoding="utf-8") as f:
                try:
                    data = yaml.load(f, Loader=yaml.BaseLoader)
                except yaml.YAMLError as e:
                    logging.info(f"Error loading yaml file: {file}. Error = {e}")
                    continue

            if data_type in ("translation", "translations") and (
                (data["meta"]["language"].lower() == language)
                or (data["meta"]["language"].lower() == "en" and language == "template")
            ):
                logging.debug(" --- found source language file: " + os.path.split(file)[1])
                break
            elif (
                data_type in ("mapping", "mappings")
                and "meta" in data.keys()
                and "component" in data["meta"].keys()
                and data["meta"]["component"] == "mappings"
            ):
                logging.debug(" --- found mappings file: " + os.path.split(file)[1])
                break

            else:
                logging.debug(" --- found source file: " + os.path.split(file)[1])
                if "meta" in list(data.keys()):
                    meta_keys = data["meta"].keys()
                    logging.debug(f" --- data.keys() = {data.keys()}, data[meta].keys() = {meta_keys}")
                data = {}
                continue
        else:
            logging.debug(
                "This file: "
                + file
                + " did not load for version: "
                + version
                + ", lang: "
                + lang
                + ", edition: "
                + edition
            )
    if not data or "suits" not in list(data.keys()):
        logging.error(
            "Could not get "
            + language
            + " language data from yaml "
            + os.path.split(file)[1]
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
        and os.path.basename(path).find(get_valid_mapping_for_version(version, edition)) >= 0
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


def get_replacement_dict(input_data: Dict[str, Any], mappings: bool = False) -> Dict[str, str]:
    """Loop through language file data and build up a find-replace dict"""
    data: Dict[str, str] = {}
    for key in list(k for k in input_data.keys() if k != "meta"):
        suit_tags, suit_key = get_suit_tags_and_key(key, input_data["meta"]["edition"])
        logging.debug(f" --- key = {key}.")
        logging.debug(f" --- suit_tags = {suit_tags}")
        logging.debug(f" --- suit_key = {suit_key}")

        for suit, suit_tag in zip(input_data[key], suit_tags):
            logging.debug(f" --- suit [name] = {suit['name']}")
            logging.debug(f" --- suit_tag = {suit_tag}")
            data = update_tag_for_suit_name(data, suit, suit_tag, mappings)
            card_tag = ""
            for card in suit[suit_key]:
                for tag, text_output in card.items():
                    if tag == "value":
                        continue

                    full_tag = get_full_tag(suit_tag, card["value"], tag)

                    # Add a translation for "Joker"
                    if suit_tag == "WC" and tag == "value":
                        full_tag = "${{{}}}".format("_".join([suit_tag, card_tag, tag]))

                    # Mappings is sometimes loaded as a list. Convert to string
                    if convert_vars.making_template:
                        text1 = check_make_list_into_text(text_output, False)
                        data[text1] = full_tag
                        if mappings:
                            data[text1.replace(", ", ",")] = full_tag
                            text1 = check_make_list_into_text(text_output, True)
                            data[text1] = full_tag
                    else:
                        data[full_tag] = check_make_list_into_text(text_output, True)
    if convert_vars.args.debug and not mappings:
        debug_txt = " --- Translation data showing First 4 (key: text):\n* "
        debug_txt += "\n* ".join(l1 + ": " + str(data[l1]) for l1 in list(data.keys())[:4])
        logging.debug(debug_txt)
        debug_txt = " --- Translation data showing Last 4 (key: text):\n* "
        debug_txt += "\n* ".join(l1 + ": " + str(data[l1]) for l1 in list(data.keys())[-4:])
        logging.debug(debug_txt)
    return data


def update_tag_for_suit_name(
    data: Dict[str, str], suit: Dict[str, Any], suit_tag: str, is_mappings: bool
) -> Dict[str, str]:
    if is_mappings is False:
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
    if convert_vars.making_template:
        data[suit["name"]] = "${{{}}}".format(suit_tag + "_suit")
        if suit_tag == "WC":
            data["Joker"] = "${WC_Joker}"
    else:
        data["${{{}}}".format(suit_tag + "_suit")] = suit["name"]
        if suit_tag == "WC":
            data["${WC_Joker}"] = "Joker"
    logging.debug(f" --- making_template {convert_vars.making_template}. suit_tag dict = {data}")
    return data


def get_template_doc(file_type: str, style: str = "static", edition: str = "webapp") -> str:
    template_doc: str
    args_input_file: str = convert_vars.args.inputfile
    sfile_ext = file_type.replace("pdf", "docx")  # Pdf output uses docx source file
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
        if convert_vars.making_template:
            template_doc = os.sep.join(
                [convert_vars.BASE_PATH, "resources", "originals", "owasp_cornucopia_en_static." + sfile_ext]
            )
        else:
            template_doc = os.path.normpath(
                convert_vars.BASE_PATH
                + os.sep
                + convert_vars.DEFAULT_TEMPLATE_FILENAME.replace("edition", edition)
                + "_"
                + style
                + "."
                + sfile_ext
            )

    template_doc = template_doc.replace("\\ ", " ")
    if os.path.isfile(template_doc):
        template_doc = check_fix_file_extension(template_doc, sfile_ext)
        logging.debug(f" --- Returning template_doc = {template_doc}")
        return template_doc
    else:
        logging.error(f"Source file not found: {template_doc}. Please ensure file exists and try again.")
        return "None"


def has_not_valid_file_style(style: str, edition: str, file_type: str) -> bool:
    if (style == "leaflet" or edition == "mobileapp") and file_type != "idml":
        return True
    return False


def get_valid_file_types() -> List[str]:
    if not convert_vars.args.outputfiletype:
        file_type = os.path.splitext(os.path.basename(convert_vars.args.outputfile))[1].strip(".")
        if file_type in ("", None):
            file_type = "docx"
        return [file_type]
    if convert_vars.args.outputfiletype.lower() == "pdf":
        if convert_vars.can_convert_to_pdf:
            return ["pdf"]
        else:
            logging.error("PDF output selected but currently unable to output PDF on this OS.")
            return []
    if convert_vars.args.outputfiletype.lower() == "all":
        file_types = []
        for file_type in convert_vars.FILETYPE_CHOICES:
            if file_type != "all" and (file_type != "pdf" or convert_vars.can_convert_to_pdf):
                file_types.append(file_type)
        return file_types
    if convert_vars.args.outputfiletype.lower() in convert_vars.FILETYPE_CHOICES:
        return [convert_vars.args.outputfiletype.lower()]
    return []


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
    if convert_vars.args.version.lower() == "all":
        for version in convert_vars.VERSION_CHOICES:
            if version not in ("all", "latest"):
                versions.append(version)
    elif convert_vars.args.version == "" or convert_vars.args.version == "latest":
        for version in convert_vars.LATEST_VERSION_CHOICES:
            versions.append(version)
    else:
        versions.append(convert_vars.args.version)
    return versions


def get_valid_mapping_for_version(version: str, edition: str) -> str:
    return (
        {
            "webapp": {"1.20": "1.2", "1.21": "1.2", "1.22": "1.2", "2.00": "2.0", "2.0": "2.0", "1.2": "1.2"},
            "mobileapp": {"1.0": "1.0", "1.00": "1.0"},
        }
        .get(edition, {})
        .get(version, "")
    )


def get_valid_styles() -> List[str]:
    styles = []
    if convert_vars.args.style.lower() == "all":
        for style in convert_vars.STYLE_CHOICES:
            if style != "all":
                styles.append(style)
    elif convert_vars.args.style == "":
        styles.append("static")
    else:
        styles.append(convert_vars.args.style)
    return styles


def get_valid_edition_choices() -> List[str]:
    editions = []
    if convert_vars.args.edition.lower() == "all":
        for edition in convert_vars.EDITION_CHOICES:
            if edition != "all":
                editions.append(edition)
    elif convert_vars.args.edition == "":
        editions.append("webapp")
    else:
        editions.append(convert_vars.args.edition)
    return editions


def group_number_ranges(data: List[str]) -> List[str]:
    if len(data) < 2 or len([s for s in data if not s.isnumeric()]):
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
    logging.debug(" --- temp_folder for extraction of xml files = " + str(temp_output_path))

    # Unzip source xml files and place in temp output folder
    with zipfile.ZipFile(template_doc) as idml_archive:
        idml_archive.extractall(temp_output_path)
        logging.debug(" --- namelist of first few files in archive = " + str(idml_archive.namelist()[:5]))

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


def save_qrcode_image(card_id: str, location_url: str = "https://copi.securedelivery.io/cards") -> None:
    output_file = os.sep.join([convert_vars.BASE_PATH, "output", "images", card_id + ".png"])
    ensure_folder_exists(os.path.dirname(output_file))
    if os.path.exists(output_file):
        pass
    else:
        try:
            url = location_url + "/" + card_id
            img = pyqrcode.create(url)
            img.svg(output_file, scale=8)
        except Exception as e:
            logging.debug("Could not create qr code for file: " + output_file + ", exception: " + str(e))


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


def rename_output_file(file_type: str, style: str, meta: Dict[str, str]) -> str:
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
            convert_vars.BASE_PATH
            + os.sep
            + convert_vars.DEFAULT_OUTPUT_FILENAME
            + ("_template" if convert_vars.making_template else "")
            + "_"
            + style
            + "."
            + file_type.strip(".")
        )

    logging.debug(f" --- output_filename before fix extension = {output_filename}")
    output_filename = check_fix_file_extension(output_filename, file_type)
    logging.debug(f" --- output_filename AFTER fix extension = {output_filename}")

    # Do the replacement of filename place-holders with meta data
    find_replace = get_find_replace_list(meta, file_type)
    f = os.path.basename(output_filename)
    for r in find_replace:
        f = f.replace(*r)
    output_filename = os.path.dirname(output_filename) + os.sep + f

    logging.debug(f" --- output_filename = {output_filename}")
    return output_filename


def replace_docx_inline_text(doc: docx.Document, data: Dict[str, str]) -> docx.Document:
    """Replace the text in the docx document."""
    logging.debug(" --- starting docx_replace")

    if convert_vars.making_template:
        replacement_values = sort_keys_longest_to_shortest(data)
    else:
        replacement_values = list(data.items())

    paragraphs = get_document_paragraphs(doc)
    for p in paragraphs:
        runs_text = "".join(r.text for r in p.runs)
        if runs_text.strip() == "" or (
            convert_vars.making_template and re.search(re.escape("${") + ".*" + re.escape("}"), runs_text)
        ):
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
    if convert_vars.making_template:
        replacement_values = sort_keys_longest_to_shortest(replacement_dict)
    else:
        replacement_values = list(replacement_dict.items())

    try:
        tree = ElTree.parse(filename)
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


def set_making_template() -> None:
    if hasattr(convert_vars.args, "language"):
        convert_vars.making_template = convert_vars.args.language.lower() == "template"
    else:
        convert_vars.making_template = False


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
