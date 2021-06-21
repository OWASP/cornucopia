#!/usr/bin/env python3

import os
import sys
import argparse
import logging
import yaml
import fnmatch
import shutil
import zipfile
import warnings
import docx
import docx2pdf
import xml.etree.ElementTree as ElTree
from typing import List
from docx import document

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_PATH = os.path.normpath(SCRIPT_PATH + "/..")
FILETYPE_CHOICES: List[str] = ["docx", "pdf", "idml"]
LANGUAGE_CHOICES: List[str] = ["en", "es", "fr", "pt-br", "template"]
DEFAULT_TEMPLATE_FILENAME: str = "../resources/templates/owasp_cornucopia_edition_lang_ver_template"
DEFAULT_OUTPUT_FILENAME: str = "../output/owasp_cornucopia_edition_component_lang_ver"
args: argparse.Namespace


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s %(filename)s | %(levelname)s | %(funcName)s | %(message)s",
        level=logging.INFO,
    )
    global args
    args = parse_arguments(sys.argv[1:])
    print("--- args = " + str(args)) if args.debug else None

    # Get the file type to output.
    file_type: str
    if args.outputfiletype is None:
        file_type = os.path.splitext(os.path.basename(args.outputfile))[1].strip(".")
        # Specify a fallback default
        if file_type in ("", None):
            file_type = "docx"
    else:
        file_type = args.outputfiletype.strip(".")
    print(f"--- file_type = {file_type}") if args.debug else None

    # Get the language files and find the output language needed
    yaml_files = get_files_from_of_type(os.sep.join([BASE_PATH, "source"]), "yaml")

    if not yaml_files:
        msg = "Error. No language files found in folder: " + str(os.sep.join([BASE_PATH, "source"]))
        print(msg)
        not args.debug and warnings.warn(msg)
        # Todo: log this error
        return None

    make_template: bool = args.language.lower() == "template"
    # Get the language data from the correct language file (checks args.language to select the correct file)
    language_data: {} = get_replacement_data(yaml_files, data_type="translation", language_code=args.language.lower())
    # Get the dict of replacement data
    language_dict: dict = get_replacement_dict(language_data, False, make_template)
    # If no data found in the language file, then exit with error
    if "suits" not in list(language_data.keys()):
        msg = "Error. Could not find the `suits` tag in the language file."
        print(msg)
        not args.debug and warnings.warn(msg)
        # Todo: Log this error
        return None

    # Get the mapping data
    mapping_data: {} = get_replacement_data(yaml_files, data_type="mappings")
    # Get the dict of replacement data
    mapping_dict: dict = get_replacement_dict(mapping_data, True, make_template)

    # Get meta data from language file
    meta: dict = get_meta_data(language_data)
    # If no meta data found, then exit with an error
    if meta in (None, {}):
        msg = (
            "Error. Could not find meta tag in the language file. "
            "Please ensure required language file is in the source folder."
        )
        print(msg)
        not args.debug and warnings.warn(msg)
        # Todo: Log this error
        return None
    print(f"--- meta data = {meta}") if args.debug else None

    # Name output file with correct edition, component, language & version
    output_file: str = rename_output_file(args.outputfile, file_type, meta, make_template)

    # Work with docx file (and maybe convert to pdf afterwards)
    if file_type in ("docx", "pdf"):
        template_doc: str = get_template_doc(args.inputfile, file_type, make_template)
        # Get the input (template) document
        doc: document.Document = get_docx_document(template_doc)

        # Replace the text with the data from the source translation file
        replace_docx_inline_text(doc, language_dict)
        # Replace the text with the data from the source mapping file
        replace_docx_inline_text(doc, mapping_dict)

        # Ensure the output folder exists
        ensure_folder_exists(os.path.dirname(output_file))

        if file_type == "docx":
            # Save the output file
            doc.save(output_file)

        else:
            # If file type is pdf, then save a temp docx file, convert the pdf to a docx
            # and remove the temp docx file if not debugging
            temp_output_file = os.sep.join([BASE_PATH, "output", "temp.docx"])
            doc.save(temp_output_file)
            print(
                f"--- temp_output_file = {temp_output_file}\n--- starting pdf conversion now."
            ) if args.debug else None

            # Check which operating system we are on to use different methods for converting docx to pdf
            operating_system: str = sys.platform
            if operating_system.lower().find("win") != -1:
                # Use docx2pdf for windows with MS Word installed
                docx2pdf.convert(temp_output_file, output_file)
            # Todo: Test additional methods to convert docx to pdf in linux.
            # elif operating_system.lower().find("linux") != -1:
            #     # Use pandoc (with pypandoc)
            #     import pypandoc
            #     # Required additional packages: pandoc, pypandoc, texlive-latex-recommended, librsvg2-bin,
            #     # texlive-latex-extra texlive-fonts-recommended
            #     pypandoc.convert_file(temp_output_file, "pdf", outputfile=output_file)
            #     extra_args = ['--pdf-engine=pdflatex']
            #     pypandoc.convert_file(temp_output_file, "pdf", extra_args=extra_args, outputfile=output_file)
            else:
                msg = (
                    "Error. A temporary docx file was created in the output folder but cannot be converted "
                    f"to pdf (yet) on operating system: {operating_system}\n"
                    "This does work in Windows with MS Word installed."
                )
                print(msg)
                not args.debug and warnings.warn(msg)
                return None

            # If not debugging then delete the temp file
            not args.debug and os.remove(temp_output_file)

    # Process idml xml files
    if file_type == "idml":
        print("--- Starting the processing of the idml-pack xml files") if args.debug else None
        if make_template:
            # If we are creating the template files, then exclude card numbers
            card_numbers = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "0", "J", "Q", "K"]
            data2: dict = {}
            for key, text in language_dict.items():
                if key not in card_numbers and text != "${WC_JOB_misc}":
                    data2[key] = text
            print(
                (
                    "--- Making template. Removed card_numbers. len language_dict = "
                    f"{len(language_dict)}, len data2 = {len(data2)}"
                )
            ) if args.debug else None
            language_dict = data2

        # Get the source file
        template_doc: str = get_template_doc(args.inputfile, file_type, make_template)

        # Get the output path and temp output path to put the temp xml files
        output_path = BASE_PATH + "/output"
        temp_output_path = output_path + "/temp"
        # Ensure the output folder and temp output folder exist
        ensure_folder_exists(temp_output_path)
        print("--- temp_folder for extraction of xml files = " + str(temp_output_path)) if args.debug else None

        # Unzip source xml files and place in temp output folder
        with zipfile.ZipFile(template_doc) as idml_archive:
            idml_archive.extractall(temp_output_path)
            print(
                "--- namelist of first few files in archive = " + str(idml_archive.namelist()[:5])
            ) if args.debug else None

        xml_files = get_files_from_of_type(temp_output_path, "xml")
        language_dict_keys = list(language_dict.keys())
        mapping_dict_keys = list(mapping_dict.keys())
        # Only Stories files have content to update
        for file in fnmatch.filter(xml_files, "*Stories*Story*"):
            if os.path.getsize(file) == 0:
                # Skip empty files
                continue
            tree = ElTree.parse(file)
            all_content_elements = tree.findall(".//Content")
            found_el = False
            for el in all_content_elements:
                if el.text in language_dict_keys:
                    found_el = True
                    new_text = language_dict[el.text]
                    el.text = new_text
                elif el.text in mapping_dict_keys:
                    found_el = True
                    new_text = mapping_dict[el.text]
                    el.text = new_text
            if found_el:
                with open(file, "bw") as f:
                    f.write(ElTree.tostring(tree.getroot(), encoding="utf-8"))

        # Zip the files as an idml file in output folder
        print("--- finished replacing text in xml files. Now zipping into idml file") if args.debug else None
        zip_dir(temp_output_path, output_file)

        # If not debugging, delete temp folder and files
        if not args.debug and os.path.exists(temp_output_path):
            shutil.rmtree(temp_output_path, ignore_errors=True)
    print("New file saved: " + str(output_file))


def get_template_doc(args_input_file: str, file_type: str, make_template: bool = False) -> str:
    template_doc: str
    source_file_ext = file_type.replace("pdf", "docx")  # Pdf output uses docx source file
    if args_input_file:
        # Input file was specified
        if os.path.isabs(args_input_file):
            template_doc = args_input_file
        else:
            template_doc = os.path.normpath(SCRIPT_PATH + os.sep + args_input_file)
    else:
        # No input file specified - using defaults
        if make_template:
            # Creating a new template from an original docx or idml file
            template_doc = os.sep.join([BASE_PATH, "resources", "originals", "owasp_cornucopia_en." + source_file_ext])
        else:
            template_doc = os.path.normpath(SCRIPT_PATH + os.sep + DEFAULT_TEMPLATE_FILENAME + "." + source_file_ext)

        # If the input file has the wrong extension, then replace the file extension with the filetype
        if not template_doc.endswith(source_file_ext):
            template_doc = ".".join([os.path.splitext(template_doc)[0], source_file_ext])
            print(f"--- template_doc with new ext = {template_doc}") if args.debug else None
    print(f"--- template_doc = {template_doc}") if args.debug else None

    if not os.path.isfile(template_doc):
        msg = f"Error. Source file not found: {template_doc}. Please ensure file exists and try again."
        print(msg)
        not args.debug and warnings.warn(msg)
        # Todo: Log this msg
        return ""

    return template_doc


def rename_output_file(args_output_file: str, file_type: str, meta: dict, make_template: bool = False) -> str:
    """Rename output file replacing place-holders from meta dict (edition, component, language, version)."""
    if args_output_file:
        # Output file specified
        if os.path.isabs(args_output_file):
            output_filename = args_output_file
        else:
            output_filename = os.path.normpath(SCRIPT_PATH + os.sep + args_output_file)
    else:
        # No output file specified - using default
        if make_template:
            # Creating a new template from an original docx or idml file
            output_filename = os.path.normpath(
                SCRIPT_PATH + os.sep + DEFAULT_OUTPUT_FILENAME + "_template." + file_type
            )
        else:
            # Use source template file as input
            output_filename = os.path.normpath(SCRIPT_PATH + os.sep + DEFAULT_OUTPUT_FILENAME + "." + file_type)

    # If the output file has the wrong extension, then replace the file extension with the filetype
    if not output_filename.endswith(file_type):
        output_filename = ".".join([os.path.splitext(output_filename)[0], file_type])
        print(f"--- output_filename with new ext = {output_filename}") if args.debug else None

    # Do the replacement of filename place-holders with meta data
    find_replace = [
        ("_type", "_" + meta["edition"].lower()),
        ("_edition", "_" + meta["edition"].lower()),
        ("_component", "_" + meta["component"].lower()),
        ("_language", "_" + meta["language"].lower()),
        ("_lang", "_" + meta["language"].lower()),
        ("_version", "_" + meta["version"].lower()),
        ("_ver", "_" + meta["version"].lower()),
    ]
    if not make_template:
        find_replace.append(("_template", ""))
    f = os.path.basename(output_filename)
    for r in find_replace:
        f = f.replace(*r)
    output_filename = os.path.dirname(output_filename) + os.sep + f

    print(f"--- output_filename = {output_filename}") if args.debug else None
    return output_filename


def get_meta_data(language_data) -> dict:
    if "meta" in list(language_data):
        meta = {}
        for key, value in language_data["meta"].items():
            if key in ("edition", "component", "language", "version"):
                meta[key] = value
        return meta
    else:
        return {}


def get_replacement_data(yaml_files: List[str], data_type: str = "translation", language_code="en") -> dict:
    """Get the raw data of the replacement text from correct yaml file

    :param yaml_files: list of files containing replacement language data or replacement mapping data
    :param data_type: type of data requested. Either translation data or mapping data
    :param language_code: code of the language requested. Looked up in the meta data of language files
    :return: dict of lookup tags and replacement text
    """
    print("--- Starting get_replacement_data()") if args.debug else None
    for file in yaml_files:
        with open(file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if data_type in ("translation", "translations") and (
            (data["meta"]["language"].lower() == language_code.lower())
            or (data["meta"]["language"].lower() == "en" and language_code.lower() == "template")
        ):
            print("--- found source language file: " + os.path.split(file)[1]) if args.debug else None
            return data
        elif data_type in ("mapping", "mappings") and (
            "meta" in data.keys() and "component" in data["meta"].keys() and data["meta"]["component"] == "mappings"
        ):
            print("--- found source mappings file: " + os.path.split(file)[1]) if args.debug else None
            return data


def get_replacement_dict(input_data, mappings=False, make_template=False) -> dict:
    """Loop through language file and build up a find-replace dict"""
    data = {}
    # Short tags to match the tags in the template documents
    suit_tags = ["VE", "AT", "SM", "AZ", "CR", "CO", "WC", "Common"]
    for suit, suit_tag in zip(input_data["suits"], suit_tags):
        # print ("--- suit [name] = " + str(suit["name"]), "\n--- suit_tag = " + str(suit_tag)) if args.debug else None
        if suit_tag != "Common":
            if make_template:
                data[suit["name"]] = "${{{}}}".format(suit_tag + "_suit")
            else:
                data["${{{}}}".format(suit_tag + "_suit")] = suit["name"]
        card_tag = ""
        for card in suit["cards"]:
            # print ("--- card.keys() = " + str(card.keys())) if args.debug else None
            if suit_tag == "WC":
                if card_tag == "JOA":
                    card_tag = "JOB"
                else:
                    card_tag = "JOA"
            else:
                card_tag = suit_tag + card["value"]
            for tag, tag_out in card.items():
                if tag != "value":
                    full_tag = "${{{}}}".format("_".join([suit_tag, card_tag, tag]))
                    # Common (suit) is additional data added to the language files for Title, No Card, etc
                    if suit_tag == "Common":
                        full_tag = "${{{}}}".format("_".join([suit_tag, card["value"]]))

                    # Mappings is seen as a list. Convert to string
                    if mappings:
                        if isinstance(tag_out, list):
                            tag_out = ", ".join(str(s) for s in list(tag_out))

                    # If no output text then do not include this replacement tag
                    if len(tag_out) == 0:
                        continue
                    if make_template:
                        data[tag_out] = full_tag
                    else:
                        data[full_tag] = tag_out
                # Add a translation for "Joker"
                if suit_tag == "WC" and tag == "value":
                    full_tag = "${{{}}}".format("_".join([suit_tag, card_tag, tag]))
                    if make_template:
                        data[tag_out] = full_tag
                    else:
                        data[full_tag] = tag_out

    print(
        "--- Translation data showing first 4 (key: text):\n* ["
        + "]\n* [".join(l1 + "] : " + data[l1] for l1 in list(data.keys())[:4])
    ) if args.debug else None
    print(
        "--- Translation data showing last 4 (key: text):\n* ["
        + "]\n* [".join(l2 + "] : " + data[l2] for l2 in list(data.keys())[-4:])
    ) if args.debug else None
    return data


def zip_dir(path, zip_filename) -> None:
    """Zip all the files recursively from path into zip_filename (excluding root path)"""
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(path):
            for file in files:
                f = os.path.join(root, file)
                zip_file.write(f, f[len(path) :])


def ensure_folder_exists(file_or_path) -> None:
    """Check if folder exists and if not, create folders recursively."""
    if not os.path.exists(os.path.dirname(file_or_path)):
        os.makedirs(os.path.dirname(file_or_path))


def replace_docx_inline_text(doc, data) -> None:
    """Replace the text in the docx document.

    :param doc: docx document object
    :param data: dict of replacement data
    :return: docx document object
    """
    print("--- starting docx_replace") if args.debug else None

    # Get all the paragraphs together
    paragraphs = list(doc.paragraphs)
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    paragraphs.append(paragraph)
    for p in paragraphs:
        runs_text = "".join(r.text for r in p.runs)
        for key, val in data.items():
            print(
                "--- found run with 28 in it. key = " + str(key) + "; val = " + str(val)
            ) if args.debug and runs_text.find("28") != -1 else None
            if key in runs_text:
                print(
                    "--- found key: " + str(key) + ", \n--- runs before = [" + str(",".join(r.text for r in p.runs)),
                    "] val = " + str(val),
                ) if args.debug and key.find("28") != -1 else None
                t = runs_text.replace(key, val)
                for i, r in enumerate(p.runs):
                    p.runs[i].text = ""
                p.runs[0].text = str(t).strip()
                print(
                    "--- runs after = " + str("; ".join(r.text for r in p.runs))
                ) if args.debug and key.find("VE_VE0_desc") != -1 else None
                if key.find("${Common_") != -1 and val.find("${Common_") != -1:
                    # Not a repeated key. Used it so now remove it in case of repeat
                    data[key] = None
    print("--- finished replacing text in doc") if args.debug else None


def get_docx_document(docx_file) -> docx.document.Document:
    """Open the file and return the docx document."""
    if os.path.isfile(docx_file):
        return docx.Document(docx_file)
    else:
        print("Error. Could not find file at: " + str(docx_file))
        return docx.Document()


def get_files_from_of_type(path, ext) -> List[str]:
    """Get a list of files from a specified folder recursively, that have the specified extension."""
    files = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, "*." + str(ext)):
            files.append(os.path.join(root, filename))
    print((f"--- found {len(files)} files of type {ext}. Showing first few:\n* ") + str("\n* ".join(files[:3])))
    return files


def parse_arguments(input_args: List[str]) -> argparse.Namespace:
    """Parse and validate the input arguments. Return object containing argument values."""
    description = "Tool to output OWASP Cornucopia playing cards into different file types and languages. "
    description += "\nExample usage: $ ./cornucopia/convert.py -t docx -l es "
    description += "\nExample usage: c:\\cornucopia\\scripts\\convert.py -t idml -l fr "
    description += "-o 'my_output_folder/owasp_cornucopia_edition_language_version.idml'"
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "-i",
        "--inputfile",
        type=str,
        default="",
        help=(
            "Input (template) file to use."
            f"\nDefault={DEFAULT_TEMPLATE_FILENAME}.(docx|idml)"
            "\nTemplate type is dependent on output type (-t) or file (-o) specified."
        ),
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-t",
        "--outputfiletype",
        type=str,
        choices=FILETYPE_CHOICES,
        # default="docx",
        help="Type of file to output. Default = docx. If specified, this overwrites the output file extension",
    )
    parser.add_argument(
        "-o",
        "--outputfile",
        default="",
        type=str,
        help=(
            "Path and name of output file to generate. (caution: existing file will be overwritten). "
            f"\ndefault = {DEFAULT_OUTPUT_FILENAME}.(docx|pdf|idml)"
        ),
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        # parser.add_argument(
        "-l",
        "--language",
        type=str,
        choices=LANGUAGE_CHOICES,
        default="en",
        help="Output language to produce. [`en`, `es`, `fr`, `pt-br`, `template`] "
        "\nTemplate will attempt to create a template from the english input file and "
        "\nreplacing strings with the template lookup codes",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Output additional information to debug script",
    )
    return parser.parse_args(input_args)


if __name__ == "__main__":
    main()
