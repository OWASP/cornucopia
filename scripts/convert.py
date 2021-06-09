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
# from typing import List
import xml.etree.ElementTree as ElTree

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_PATH = os.path.normpath(SCRIPT_PATH + "/..")

args: {}


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s %(filename)s | %(levelname)s | %(funcName)s | %(message)s",
        level=logging.INFO,
    )
    global args
    args = parse_arguments(sys.argv[1:])
    args.debug and print("--- args = " + str(args))

    # Get the file type to output.
    if args.outputfiletype is None:
        file_type = os.path.splitext(os.path.basename(args.outputfile))[1].strip(".")
        # Specify a fallback default
        if file_type in ("", None):
            file_type = "docx"
    else:
        file_type = args.outputfiletype.strip(".")
    args.debug and print("--- file_type = " + str(file_type))

    # Get the language files and find the output language needed
    yaml_files = get_files_from_of_type(BASE_PATH + "/source", "yaml")

    if len(yaml_files) == 0:
        msg = "Error. No language files found in folder: " + BASE_PATH + "/source"
        print(msg)
        not args.debug and warnings.warn(msg)
        # Todo: log this error
        return

    # Get the language data from the correct language file (checks args.language to select the correct file)
    language_data = get_replacement_data(yaml_files, data_type="translation", language_code=args.language.lower())

    # Get the dict of replacement data
    data = get_replacement_dict(language_data, mappings=False, make_template=(args.language.lower() == "template"))

    # Get the mapping data
    mapping_data = get_replacement_data(yaml_files, data_type="mappings")
    # args.debug and print("--- Mapping_data[data][:1] = " + str(mapping_data["suits"][:1]))

    # Get the dict of replacement data
    data2 = get_replacement_dict(mapping_data, mappings=True, make_template=(args.language.lower() == "template"))
    # args.debug and print("--- data2 = " + str(data2))

    # Get meta data from language file
    meta = get_meta_data(language_data)
    # If no meta data found, then exit with an error
    if meta in (None, {}):
        msg = "Error. Could not find meta tag in the language file. Please ensure required language file is in the " \
              "source folder."
        print(msg)
        not args.debug and warnings.warn(msg)
        # Todo: Log this error
        return
    args.debug and print("--- meta data = " + str(meta))

    # If no data found in the language file, then exit with error
    if "suits" not in list(language_data.keys()):
        msg = "Error. Could not find the `suits` tag in the language file."
        print(msg)
        not args.debug and warnings.warn(msg)
        # Todo: Log this error
        return

    # Name output file with correct edition, component, language & version
    output_file = rename_output_file(args.outputfile, meta, (args.language.lower() == "template"))

    # If the output file has the wrong extension, then replace the file extension with the file_type
    if file_type != os.path.splitext(output_file)[1][1:]:
        output_file = os.path.splitext(output_file)[0] + "." + file_type
        args.debug and print("--- output_file with new ext = " + str(output_file))

    # Work with docx file (and maybe convert to pdf afterwards)
    if file_type in ("docx", "pdf"):
        # Creating a new template
        if args.language.lower() == "template":
            if args.inputfile == "../resources/templates/owasp_cornucopia_edition_lang_ver_template.docx":
                template_doc = os.sep.join([BASE_PATH, "source", "owasp_cornucopia_en.docx"])
            else:
                if os.path.isabs(args.inputfile):
                    template_doc = args.inputfile
                else:
                    template_doc = os.path.normpath(SCRIPT_PATH + os.sep + args.inputfile)
        # Use source template docx file as input
        else:
            if os.path.isabs(args.inputfile):
                template_doc = args.inputfile
            else:
                template_doc = os.path.normpath(SCRIPT_PATH + os.sep + args.inputfile)
            # If the input file has the wrong extension, then replace the file extension with the file_type
            if "." + file_type != os.path.splitext(template_doc)[1] and \
                    (file_type != "pdf" and os.path.splitext(template_doc)[1] != "docx"):
                # args.debug and print("--- old template_doc = " + str(template_doc))
                template_doc = os.path.splitext(template_doc)[0] + "." + file_type
                args.debug and print("--- template_doc with new ext = " + str(template_doc))

        args.debug and print("--- template_doc = " + str(template_doc))
        if not os.path.isfile(template_doc):
            msg = "Error. Source file not found: " + template_doc + ". Please ensure file exists and try again."
            print(msg)
            not args.debug and warnings.warn(msg)
            # Todo: Log this msg
            return

        # Check output path exists
        ensure_destination_folder_exists(output_file)

        # Get the input (template) document
        doc = docx.Document(template_doc)

        # Replace the text with the data from the source translation file
        docx_replace(doc, data)

        # Replace the text with the data from the source translation file
        docx_replace(doc, data2)
        # args.debug and print("--- finished docx_replace with mapping data")

        if file_type == "docx":
            # Save the output file
            doc.save(output_file)

        # If file type is pdf, then save a temp docx file, convert the pdf to a docx and remove the temp docx file
        if file_type == "pdf":
            temp_output_file = BASE_PATH + os.sep + "output" + os.sep + "temp.docx"

            doc.save(temp_output_file)
            args.debug and print(
                "--- temp_output_file = " + str(temp_output_file) + "\n--- starting pdf conversion now.")

            # Check which operating system we are on to use different methods for converting docx to pdf
            operating_system = sys.platform
            if operating_system.lower().find("win") != -1:
                # Use docx2pdf for windows with MS Word installed
                docx2pdf.convert(temp_output_file, output_file)
            # elif operating_system.lower().find("linux") != -1:
            #     # Use pandoc (with pypandoc)
            #     import pypandoc
            #     # Required additional packages: pandoc, pypandoc, texlive-latex-recommended, librsvg2-bin,
            #     # texlive-latex-extra texlive-fonts-recommended
            #     pypandoc.convert_file(temp_output_file, "pdf", outputfile=output_file)
            #     extra_args = ['--pdf-engine=pdflatex']
            #     pypandoc.convert_file(temp_output_file, "pdf", extra_args=extra_args, outputfile=output_file)
            else:
                msg = "Error. A temporary docx file was created but cannot be converted to pdf (yet) on operating " \
                      "system: " + str(operating_system) + "\nThis does work in Windows with MS Word installed."
                print(msg)
                not args.debug and warnings.warn(msg)
                return

            not args.debug and os.remove(temp_output_file)

        print("New file saved: " + str(output_file))

    # Process idml xml files
    if file_type == "idml":
        args.debug and print("--- Starting the processing of the idml-pack xml files")
        # Check if we are creating the template files and exclude card numbers
        card_numbers = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "0", "J", "Q", "K"]
        data2 = {}
        if args.language.lower() == "template":
            for key, text in data.items():
                if key not in card_numbers:
                    data2[key] = text
            args.debug and print("--- len data = " + str(len(data)) + ", len data2 = " + str(len(data2)))
            data = data2

        # Extract source xml files and place in temp output folder
        src_idml_file = BASE_PATH + "/resources/templates/owasp_cornucopia_ecommerce_cards_template.idml"
        if not os.path.isfile(src_idml_file):
            msg = "Error. Source .IDML file does not exists. Please ensure the idml template file exists: " + str(
                src_idml_file)
            # Todo: log this error
            print(msg)
            return

        # Get the output path and temp output path to put the temp xml files
        output_path = BASE_PATH + "/output"
        temp_output_path = output_path + "/temp"

        # Ensure the output path exists
        ensure_destination_folder_exists(temp_output_path)
        args.debug and print("--- temp_folder = " + str(temp_output_path))

        # Unzip the files
        with zipfile.ZipFile(src_idml_file) as idml_archive:
            idml_archive.extractall(temp_output_path)
            args.debug and print("--- namelist of files in archive = " + str(idml_archive.namelist()[:15]))

        xml_files = get_files_from_of_type(temp_output_path, "xml")

        # Only Stories files have content to update
        for file in fnmatch.filter(xml_files, "*Stories*Story*"):
            # Check file size
            if os.path.getsize(file) == 0:
                continue
            # args.debug and print("--- starting on file: " + str(file))
            tree = ElTree.parse(file)
            all_content_elements = tree.findall('.//Content')
            found_el = False
            for el in all_content_elements:
                for k in data.keys():
                    if el.text.lower() == k.lower():
                        found_el = True
                        new_text = data[k]
                        el.text = new_text
            if found_el:
                with open(file, 'bw') as f:
                    f.write(ElTree.tostring(tree.getroot(), encoding="utf-8"))

        # Zip the files as an idml file in output folder
        args.debug and print("--- finished replacing text in xml files. Now zipping into idml file")

        zip_dir(temp_output_path, output_file)
        print("New file saved: " + str(output_file))

        # If not debugging, delete temp folder and files
        if not args.debug and os.path.exists(temp_output_path):
            shutil.rmtree(temp_output_path, ignore_errors=True)


# Name output file with correct edition, component, language & version
def rename_output_file(filename, meta, make_template=False) -> str:
    find_replace = [("_type", "_" + meta["edition"].lower()),
                    ("_edition", "_" + meta["edition"].lower()),
                    ("_component", "_" + meta["component"].lower()),
                    ("_language", "_" + meta["language"].lower()),
                    ("_lang", "_" + meta["language"].lower()),
                    ("_version", "_" + meta["version"].lower()),
                    ("_ver", "_" + meta["version"].lower()), ("_template", "")]
    dirname = os.path.dirname(filename)
    if not os.path.isabs(dirname):
        dirname = SCRIPT_PATH + os.sep + dirname
    f = os.path.basename(filename)
    # Do the replacement
    for r in find_replace:
        f = f.replace(*r)
    if make_template:
        f = os.path.splitext(f)[0] + "_template" + os.path.splitext(f)[1]

    filename = os.path.abspath(os.sep.join([dirname, f]))
    args.debug and print("--- output_file = " + str(filename))
    return filename


def get_meta_data(language_data) -> dict:
    if "meta" in list(language_data):
        meta = {}
        for key, value in language_data["meta"].items():
            if key in ("edition", "component", "language", "version"):
                meta[key] = value
        return meta


##
# function  get_replacement_data()
# Description: opens each file and checks if the meta data matches the data_type and language short-code specified
# var: list[string] (list of yaml files containing translations and/or mappings)
# var: string [translations|mappings]
# var: string language short-code identifying which translation file data to return. Ignored if data_type is mappings.
# returns: dict 
##
def get_replacement_data(yaml_files, data_type="translation", language_code="en") -> dict:
    for file in yaml_files:
        args.debug and print("--- file = " + str(file))
        with open(file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        args.debug and print(
            "--- loaded data successfully. " + str(file) + " with " + str(len(data)) + " keys: " + str(data.keys()))

        if data_type in ("translation", "translations"):
            if (data["meta"]["language"].lower() == language_code.lower()) \
                    or (data["meta"]["language"].lower() == "en" and language_code.lower() == "template"):
                args.debug and print("--- found source language file: " + os.path.split(file)[1])
                return data
        elif data_type in ("mapping", "mappings"):
            if "meta" in data.keys() and "component" in data["meta"].keys() and data["meta"]["component"] == "mappings":
                return data


# Loop through language file and build up a find-replace dict
def get_replacement_dict(input_data, mappings=False, make_template=False) -> dict:
    data = {}
    # Short tags to match the tags in the template documents
    suit_tags = ["VE", "AT", "SM", "AZ", "CR", "CO", "WC", "Common"]
    for suit, suit_tag in zip(input_data["suits"], suit_tags):
        # args.debug and print("--- suit [name] = " + str(suit["name"]), "\n--- suit_tag = " + str(suit_tag))
        if suit_tag != "Common":
            if make_template:
                data[suit["name"]] = '${{{}}}'.format(suit_tag + "_suit")
            else:
                data['${{{}}}'.format(suit_tag + "_suit")] = suit["name"]
        card_tag = ""
        for card in suit["cards"]:
            # args.debug and print("--- card.keys() = " + str(card.keys()))
            if suit_tag == "WC":
                if card_tag == "JOA":
                    card_tag = "JOB"
                else:
                    card_tag = "JOA"
            else:
                card_tag = suit_tag + card["value"]
            for tag, tag_out in card.items():
                if tag != "value":
                    full_tag = '${{{}}}'.format("_".join([suit_tag, card_tag, tag]))
                    # Common (suit) is additional data added to the language files for Title, No Card, etc
                    if suit_tag == "Common":
                        full_tag = '${{{}}}'.format("_".join([suit_tag, card["value"]]))

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
                    full_tag = '${{{}}}'.format("_".join([suit_tag, card_tag, tag]))
                    if make_template:
                        data[tag_out] = full_tag
                    else:
                        data[full_tag] = tag_out

    args.debug and print("--- Translation data showing first 4 (key: text):\n* [" + "]\n* [".join(
        l1 + "] : " + data[l1] for l1 in list(data.keys())[:4]))
    args.debug and print("--- Translation data showing last 4 (key: text):\n* [" + "]\n* [".join(
        l2 + "] : " + data[l2] for l2 in list(data.keys())[-4:]))
    return data


# Zip all the files recursively from path into zip_filename (excluding root path)
def zip_dir(path, zip_filename) -> None:
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(path):
            for file in files:
                f = os.path.join(root, file)
                zip_file.write(f, f[len(path):])


# Check output path exists
def ensure_destination_folder_exists(file_or_path) -> None:
    if not os.path.exists(os.path.dirname(file_or_path)):
        os.makedirs(os.path.dirname(file_or_path))


##
# function: docx_replace()
# Credits: github/adejones
# URL: https://gist.github.com/adejones/a6d42984f66ea9990d78974531863bee
# Modified and simplified by GDBryant
##
def docx_replace(doc, data) -> docx.Document:
    args.debug and print("--- starting docx_replace")

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
            args.debug and runs_text.find("28") != -1 and print(
                "--- found run with 28 in it. key = " + str(key) + "; val = " + str(val))
            if key in runs_text:
                args.debug and key.find("28") != -1 and print(
                    "--- found key: " + str(key) + ", \n--- runs before = [" + str(",".join(r.text for r in p.runs)),
                    "] val = " + str(val))
                t = runs_text.replace(key, val)
                for i, r in enumerate(p.runs):
                    p.runs[i].text = ""
                p.runs[0].text = str(t).strip()
                args.debug and key.find("VE_VE0_desc") != -1 and print(
                    "--- runs after = " + str("; ".join(r.text for r in p.runs)))
                if key.find("${Common_") != -1 and val.find("${Common_") != -1:
                    # Not a repeated key. Used it so now remove it in case of repeat
                    data[key] = None
    args.debug and print("--- finished replacing text in doc")


def get_docx(docx_file) -> docx.Document:
    if os.path.isfile(docx_file):
        return docx.Document(docx_file)
    else:
        print("Error. Could not find file at: " + str(docx_file))
        return docx.Document()


def get_files_from_of_type(path, ext) -> list[str]:
    files = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, "*." + str(ext)):
            files.append(os.path.join(root, filename))
    args.debug and print("--- found " + str(len(files)) + " files of type " + str(ext) + ". Showing first 5:\n* " + str(
        "\n* ".join(files[:5])))
    return files


# Parse the input arguments
def parse_arguments(input_args: list[str]) -> argparse.Namespace:
    description = "Tool to output OWASP Cornucopia playing cards into different file types and languages. "
    description += "\nExample usage: $ ./cornucopia/convert.py -t docx -l es "
    description += "\nExample usage: c:\cornucopia\scripts\convert.py -t idml -l fr "
    description += "-o 'my_output_folder/owasp_cornucopia_edition_language_version.idml'"
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "-i",
        "--inputfile",
        type=str,
        default="../resources/templates/owasp_cornucopia_edition_lang_ver_template.docx",
        help="Input (template) file to use."
             "\ndefault=../resources/templates/owasp_cornucopia_edition_lang_ver_template[.docx|.idml]"
             "\nTemplate type is dependent on output type (-t) or file (-o) specified.",
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-t",
        "--outputfiletype",
        type=str,
        choices=["docx", "pdf", "idml"],
        # default="docx",
        help="Type of file to output. Default = docx. If specified, this overwrites the output file extension",
    )
    parser.add_argument(
        "-o",
        "--outputfile",
        default="../output/owasp_cornucopia_edition_lang_ver.docx",
        type=str,
        help="Path and name of output file to generate. (caution: existing file will be overwritten). "
             "\ndefault = ../output/owasp_cornucopia_edition_lang_ver.docx",
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        # parser.add_argument(
        "-l",
        "--language",
        type=str,
        choices=["en", "es", "fr", "pt-br", "template"],
        default="en",
        help="Output language to produce. [`en`, `es`, `fr`, `pt-br`, `template`] "
             "\nTemplate will attempt to create a template from the english input file and "
             "replacing strings with the template lookup codes",
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
