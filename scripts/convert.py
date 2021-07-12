#!/usr/bin/env python3
import os
import re
import sys
import argparse
import logging
import yaml
import fnmatch
import shutil
import zipfile
import docx2pdf
import docx
from docx import Document
import xml.etree.ElementTree as ElTree
from typing import List

class Convert:
    SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
    BASE_PATH = os.path.normpath(SCRIPT_PATH + "/..")
    FILETYPE_CHOICES: List[str] = ["docx", "pdf", "idml"]
    LANGUAGE_CHOICES: List[str] = ["en", "es", "fr", "pt-br", "template"]
    DEFAULT_TEMPLATE_FILENAME: str = "../resources/templates/owasp_cornucopia_edition_lang_ver_template"
    DEFAULT_OUTPUT_FILENAME: str = "../output/owasp_cornucopia_edition_component_lang_ver"
    args: argparse.Namespace

    def main(self) -> None:
        logging.basicConfig(
            format="%(asctime)s %(filename)s | %(levelname)s | %(funcName)s | %(message)s",
            level=logging.INFO,
        )
        self.args = self.parse_arguments(sys.argv[1:])
        if self.args.debug:
            print("--- args = " + str(self.args))

        # Get the file type to output.
        file_type: str
        if self.args.outputfiletype:
            file_type = self.args.outputfiletype.strip(".")
        else:
            file_type = os.path.splitext(os.path.basename(self.args.outputfile))[1].strip(".")
            # Specify a fallback default
            if file_type in ("", None):
                file_type = "docx"
        if self.args.debug:
            print(f"--- file_type = {file_type}")

        # Get the language files and find the output language needed
        yaml_files = self.get_files_from_of_type(os.sep.join([self.BASE_PATH, "source"]), "yaml")

        if not yaml_files:
            logging.error("Error. No language files found in folder: " + str(os.sep.join([self.BASE_PATH, "source"])))
            return None

        # Get the language data from the correct language file (checks self.args.language to select the correct file)
        language_data: {} = self.get_replacement_data(yaml_files, "translation")
        # If no data found in the language file, then exit with error
        if "suits" not in list(language_data.keys()):
            logging.error("Error. Could not find the `suits` tag in the language file.")
            return None

        # Get the dict of replacement data
        language_dict: dict = self.get_replacement_dict(language_data, False)

        # Get the mapping data
        mapping_data: {} = self.get_replacement_data(yaml_files, "mappings")
        # Get the dict of replacement data
        mapping_dict: dict = self.get_replacement_dict(mapping_data, True)

        language_dict.update(mapping_dict)
        if self.make_template():
            language_dict = self.remove_short_keys(language_dict)

        # Get meta data from language file
        meta: dict = self.get_meta_data(language_data)
        # If no meta data found, then exit with an error
        if meta in (None, {}):
            logging.error(
                "Error. Could not find meta tag in the language file. "
                "Please ensure required language file is in the source folder."
            )
            return None
        if self.args.debug:
            print(f"--- meta data = {meta}")

        template_doc: str = self.get_template_doc(self.args.inputfile, file_type)

        # Name output file with correct edition, component, language & version
        output_file: str = self.rename_output_file(self.args.outputfile, file_type, meta)
        self.ensure_folder_exists(os.path.dirname(output_file))

        # Work with docx file (and maybe convert to pdf afterwards)
        if file_type in ("docx", "pdf"):
            # Get the input (template) document
            doc: docx.document.Document = self.get_docx_document(template_doc)

            self.replace_docx_inline_text(doc, language_dict)

            if file_type == "docx":
                doc.save(output_file)

            else:
                # If file type is pdf, then save a temp docx file, convert the docx to pdf
                temp_output_file = os.sep.join([self.BASE_PATH, "output", "temp.docx"])
                doc.save(temp_output_file)
                if self.args.debug:
                    print(f"--- temp_output_file = {temp_output_file}\n--- starting pdf conversion now.")

                # Currently only Windows with Word installed can converting docx to pdf
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
                #     extra_self.args = ['--pdf-engine=pdflatex']
                #     pypandoc.convert_file(temp_output_file, "pdf", extra_self.args=extra_self.args,
                #     outputfile=output_file)
                else:
                    logging.error(
                        "Error. A temporary docx file was created in the output folder but cannot be converted "
                        f"to pdf (yet) on operating system: {operating_system}\n"
                        "This does work in Windows with MS Word installed."
                    )
                    return None

                # If not debugging then delete the temp file
                not self.args.debug and os.remove(temp_output_file)

        # Process idml xml files
        if file_type == "idml":
            # Get the output path and temp output path to put the temp xml files
            output_path = self.BASE_PATH + "/output"
            temp_output_path = output_path + "/temp"
            # Ensure the output folder and temp output folder exist
            self.ensure_folder_exists(temp_output_path)
            if self.args.debug:
                print("--- temp_folder for extraction of xml files = " + str(temp_output_path))

            # Unzip source xml files and place in temp output folder
            with zipfile.ZipFile(template_doc) as idml_archive:
                idml_archive.extractall(temp_output_path)
                if self.args.debug:
                    print("--- namelist of first few files in archive = " + str(idml_archive.namelist()[:5]))

            xml_files = self.get_files_from_of_type(temp_output_path, "xml")
            # Only Stories files have content to update
            for file in fnmatch.filter(xml_files, "*Stories*Story*"):
                self.replace_text_in_xml_file(file, language_dict)

            # Zip the files as an idml file in output folder
            if self.args.debug:
                print("--- finished replacing text in xml files. Now zipping into idml file")
            self.zip_dir(temp_output_path, output_file)

            # If not debugging, delete temp folder and files
            if not self.args.debug and os.path.exists(temp_output_path):
                shutil.rmtree(temp_output_path, ignore_errors=True)
        print("New file saved: " + str(output_file))

    @staticmethod
    def sort_keys_longest_to_shortest(replacement_dict) -> List[tuple]:
        new_list = replacement_dict.items()
        return sorted(new_list, key=lambda s: len(s[0]), reverse=True)

    def replace_text_in_xml_file(self, file, replacement_dict) -> None:
        if os.path.getsize(file) == 0:
            return
        if self.make_template():
            replacement_values = self.sort_keys_longest_to_shortest(replacement_dict)
        else:
            replacement_values = replacement_dict.items()

        tree = ElTree.parse(file)
        all_content_elements = tree.findall(".//Content")

        found_element = False
        for el in all_content_elements:
            for k, v in replacement_values:
                if self.key_matches_text(el.text, k, v):
                    if self.args.debug and (el.text.startswith("${WC_Jo") or k.startswith("${WC_Jo")):
                        print(f"--- found a match. k = {k}, txt = {el.text}")
                    found_element = True
                    new_text = el.text.replace(k, v)
                    el.text = new_text
        if found_element:
            with open(file, "bw") as f:
                f.write(ElTree.tostring(tree.getroot(), encoding="utf-8"))

    def key_matches_text(self, txt: str, key: str, val: str) -> bool:
        if txt == key:
            if self.args.debug and (txt.startswith("${WC_Jo") and key.startswith("${WC_Jo")):
                print(f"--- Text Matches Key: text = {txt}, key = {key}")
            return True
        if self.args.debug and (txt.startswith("${WC_") and key.startswith("${WC_")):
            print(f"--- Text does NOT Match Key: text = {txt}, key = {key}")
        tmp = txt.lower()[:-len(key) - 1].replace(" ", "_")
        if txt.endswith(key) and (key[:-1].endswith(tmp) or val[:-1].endswith(tmp)):
            return True
        return False

    def remove_short_keys(self, replacement_dict) -> dict:
        data2: dict = {}
        for key, value in replacement_dict.items():
            if len(key) > 3:
                data2[key] = value
        if self.args.debug:
            print("--- Making template. Removed card_numbers. len replacement_dict = "
                  f"{len(replacement_dict)}, len data2 = {len(data2)}")
        return data2

    def get_template_doc(self, args_input_file: str, file_type: str) -> str:
        template_doc: str
        source_file_ext = file_type.replace("pdf", "docx")  # Pdf output uses docx source file
        if args_input_file:
            # Input file was specified
            if os.path.isabs(args_input_file):
                template_doc = args_input_file
            else:
                template_doc = os.path.normpath(self.SCRIPT_PATH + os.sep + args_input_file)
        else:
            # No input file specified - using defaults
            if self.make_template():
                # Creating a new template from an original docx or idml file
                template_doc = os.sep.join(
                    [self.BASE_PATH, "resources", "originals", "owasp_cornucopia_en." + source_file_ext])
            else:
                template_doc = os.path.normpath(
                    self.SCRIPT_PATH + os.sep + self.DEFAULT_TEMPLATE_FILENAME + "." + source_file_ext)

            self.check_fix_file_type(template_doc, source_file_ext)
        if self.args.debug:
            print(f"--- template_doc = {template_doc}")

        if not os.path.isfile(template_doc):
            logging.error(f"Error. Source file not found: {template_doc}. Please ensure file exists and try again.")
            return ""
        return template_doc

    def rename_output_file(self, args_output_file: str, file_type: str, meta: dict) -> str:
        """Rename output file replacing place-holders from meta dict (edition, component, language, version)."""
        if args_output_file:
            # Output file is specified as an argument
            if os.path.isabs(args_output_file):
                output_filename = args_output_file
            else:
                output_filename = os.path.normpath(self.SCRIPT_PATH + os.sep + args_output_file)
        else:
            # No output file specified - using default
            output_filename = os.path.normpath(
                self.SCRIPT_PATH + os.sep + self.DEFAULT_OUTPUT_FILENAME + (
                    "_template" if self.make_template() else "") + "." + file_type.strip(".")
            )

        self.check_fix_file_type(output_filename, file_type)

        # Do the replacement of filename place-holders with meta data
        find_replace = self.get_find_replace_list(meta)
        f = os.path.basename(output_filename)
        for r in find_replace:
            f = f.replace(*r)
        output_filename = os.path.dirname(output_filename) + os.sep + f

        if self.args.debug:
            print(f"--- output_filename = {output_filename}")
        return output_filename

    def check_fix_file_type(self, filename: str, file_type: str) -> None:
        if not filename.endswith(file_type):
            filename = ".".join([os.path.splitext(filename)[0], file_type])
            if self.args.debug:
                print(f"--- output_filename with new ext = {filename}")

    def get_find_replace_list(self, meta: dict) -> List[tuple]:
        ll = [
            ("_type", "_" + meta["edition"].lower()),
            ("_edition", "_" + meta["edition"].lower()),
            ("_component", "_" + meta["component"].lower()),
            ("_language", "_" + meta["language"].lower()),
            ("_lang", "_" + meta["language"].lower()),
            ("_version", "_" + meta["version"].lower()),
            ("_ver", "_" + meta["version"].lower()),
        ]
        if not self.make_template():
            ll.append(("_template", ""))
        return ll

    @staticmethod
    def get_meta_data(language_data) -> dict:
        if "meta" in list(language_data):
            meta = {}
            for key, value in language_data["meta"].items():
                if key in ("edition", "component", "language", "version"):
                    meta[key] = value
            return meta
        else:
            return {}

    def get_replacement_data(self, yaml_files: List[str], data_type: str = "translation") -> dict:
        """Get the raw data of the replacement text from correct yaml file"""
        if self.args.debug:
            print("--- Starting get_replacement_data()")
        for file in yaml_files:
            with open(file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if data_type in ("translation", "translations") and (
                    (data["meta"]["language"].lower() == self.args.language.lower())
                    or (data["meta"]["language"].lower() == "en" and self.args.language.lower() == "template")
            ):
                if self.args.debug:
                    print("--- found source language file: " + os.path.split(file)[1])
                return data
            elif (data_type in ("mapping", "mappings")
                    and "meta" in data.keys()
                    and "component" in data["meta"].keys()
                    and data["meta"]["component"] == "mappings"):
                if self.args.debug:
                    print("--- found source mappings file: " + os.path.split(file)[1])
                return data

    def get_replacement_dict(self, input_data, mappings=False) -> dict:
        """Loop through language file and build up a find-replace dict"""
        data = {}
        # Short tags to match the suits in the template documents
        suit_tags = suit_key = ""
        for key in list(k for k in input_data.keys() if k != "meta"):
            if key == "suits":
                suit_tags = ["VE", "AT", "SM", "AZ", "CR", "CO", "WC"]
                suit_key = "cards"
            elif key == "paragraphs":
                suit_tags = ["Common"]
                suit_key = "sentences"
            for suit, suit_tag in zip(input_data[key], suit_tags):
                if self.args.debug:
                    print("--- suit [name] = " + str(suit["name"]), "\n--- suit_tag = " + str(suit_tag))
                data.update(self.get_tag_for_suit_name(suit, suit_tag))

                card_tag = ""
                for card in suit[suit_key]:
                    if self.args.debug:
                        print("--- card.keys() = " + str(card.keys()))
                    for tag, text_output in card.items():
                        if self.args.debug:
                            print(f"--- tag = {tag}, text output[:10] = {text_output[:10]}")
                        if tag != "value":
                            # If no output text then do not include this replacement tag
                            if len(text_output) == 0:
                                continue

                            full_tag = self.get_full_tag(suit_tag, card["value"], tag)

                            # Mappings is seen as a list. Convert to string
                            if mappings and isinstance(text_output, list):
                                text_output = ", ".join(str(s) for s in list(text_output))

                            # Add a translation for "Joker"
                            if suit_tag == "WC" and tag == "value":
                                full_tag = "${{{}}}".format("_".join([suit_tag, card_tag, tag]))

                            if self.args.debug:
                                print(f"--- full_tag = {full_tag}, text[:10] = {text_output[:10]}")

                            if self.make_template():
                                data[text_output] = full_tag
                            else:
                                data[full_tag] = text_output
        if self.args.debug:
            print("--- Translation data showing first 4 (key: text):\n* ["
                  "]\n* [".join(l1 + "] : " + data[l1] for l1 in list(data.keys())[:4]))
            print("--- Translation data showing last 4 (key: text):\n* ["
                  "]\n* [".join(l2 + "] : " + data[l2] for l2 in list(data.keys())[-4:]))
        return data

    def get_tag_for_suit_name(self, suit, suit_tag) -> dict:
        data = {}
        if self.make_template():
            data[suit["name"]] = "${{{}}}".format(suit_tag + "_suit")
            if suit_tag == "WC":
                data["Joker"] = "${WC_Joker}"
        else:
            data["${{{}}}".format(suit_tag + "_suit")] = suit["name"]
            if suit_tag == "WC":
                data["${WC_Joker}"] = "Joker"
        if self.args.debug:
            print(f"--- make_template = {self.make_template()}, suit_tag dict = {data}")
        return data

    @staticmethod
    def get_full_tag(suit_tag, card, tag) -> str:
        if suit_tag == "WC":
            full_tag = "${{{}}}".format("_".join([suit_tag, card, tag]))
        elif suit_tag == "Common":
            full_tag = "${{{}}}".format("_".join([suit_tag, card]))
        else:
            full_tag = "${{{}}}".format("_".join([suit_tag, suit_tag + card, tag]))
        return full_tag

    @staticmethod
    def zip_dir(path, zip_filename) -> None:
        """Zip all the files recursively from path into zip_filename (excluding root path)"""
        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(path):
                for file in files:
                    f = os.path.join(root, file)
                    zip_file.write(f, f[len(path):])

    @staticmethod
    def ensure_folder_exists(folder_path: str) -> None:
        """Check if folder exists and if not, create folders recursively."""
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def replace_docx_inline_text(self, doc, data) -> None:
        """Replace the text in the docx document."""
        if self.args.debug:
            print("--- starting docx_replace")

        if self.make_template():
            replacement_values = self.sort_keys_longest_to_shortest(data)
        else:
            replacement_values = data.items()
        if self.args.debug:
            print(f"--- replacement values is = \n\n{replacement_values[-5:]}")

        # Get all the paragraphs together
        paragraphs = list(doc.paragraphs)
        for t in doc.tables:
            for row in t.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        paragraphs.append(paragraph)
        for p in paragraphs:
            runs_text = "".join(r.text for r in p.runs)
            if self.make_template() and re.search("\$\{.*\}", runs_text):
                continue
            for key, val in replacement_values:
                if key in runs_text:
                    t = runs_text.replace(key, val)
                    for i, r in enumerate(p.runs):
                        p.runs[i].text = ""
                    p.runs[0].text = str(t).strip()
                    if key.find("${Common_") != -1 and val.find("${Common_") != -1:
                        # Not a repeated key. Used it so now remove it in case of repeat
                        data[key] = None
        if self.args.debug:
            print("--- finished replacing text in doc")

    @staticmethod
    def get_docx_document(docx_file) -> docx.document.Document:
        """Open the file and return the docx document."""
        if os.path.isfile(docx_file):
            return docx.Document(docx_file)
        else:
            print("Error. Could not find file at: " + str(docx_file))
            return docx.Document()

    def get_files_from_of_type(self, path, ext) -> List[str]:
        """Get a list of files from a specified folder recursively, that have the specified extension."""
        files = []
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, "*." + str(ext)):
                files.append(os.path.join(root, filename))
        if self.args.debug:
            print(f"--- found {len(files)} files of type {ext}. Showing first few:\n* " + str("\n* ".join(files[:3])))
        return files

    def make_template(self) -> bool:
        return self.args.language.lower() == "template"

    def parse_arguments(self, input_args: List[str]) -> argparse.Namespace:
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
                f"\nDefault={self.DEFAULT_TEMPLATE_FILENAME}.(docx|idml)"
                "\nTemplate type is dependent on output type (-t) or file (-o) specified."
            ),
        )
        group = parser.add_mutually_exclusive_group(required=False)
        group.add_argument(
            "-t",
            "--outputfiletype",
            type=str,
            choices=self.FILETYPE_CHOICES,
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
                f"\ndefault = {self.DEFAULT_OUTPUT_FILENAME}.(docx|pdf|idml)"
            ),
        )
        group = parser.add_mutually_exclusive_group(required=False)
        group.add_argument(
            # parser.add_argument(
            "-l",
            "--language",
            type=str,
            choices=self.LANGUAGE_CHOICES,
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
    c = Convert()
    c.main()
