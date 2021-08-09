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
import xml.etree.ElementTree as ElTree
import typing


class Convert:
    SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
    BASE_PATH = os.path.normpath(SCRIPT_PATH + "/..")
    FILETYPE_CHOICES: typing.List[str] = ["all", "docx", "pdf", "idml"]
    LANGUAGE_CHOICES: typing.List[str] = ["template", "all", "en", "es", "fr", "pt-br"]
    DEFAULT_TEMPLATE_FILENAME: str = "../resources/templates/owasp_cornucopia_edition_lang_ver_template"
    DEFAULT_OUTPUT_FILENAME: str = "../output/owasp_cornucopia_edition_component_lang_ver"
    args: argparse.Namespace
    can_convert_to_pdf: bool = False
    making_template: bool = False

    def main(self) -> None:
        self.args = self.parse_arguments(sys.argv[1:])
        self.set_logging(self)
        logging.debug(" --- args = " + str(self.args))

        self.set_can_convert_to_pdf()
        if self.args.outputfiletype == "pdf" and not self.can_convert_to_pdf and not self.args.debug:
            logging.error(
                "Cannot convert to pdf on this system. "
                "Pdf conversion is available on Windows and Mac, if MS Word is installed"
            )
            return

        self.set_making_template(self)

        # Create output files
        for file_type in self.get_valid_file_types():
            for language in self.get_valid_language_choices():
                self.convert_type_language(file_type, language)

    def get_valid_file_types(self) -> typing.List[str]:
        if not self.args.outputfiletype:
            file_type = os.path.splitext(os.path.basename(self.args.outputfile))[1].strip(".")
            if file_type in ("", None):
                file_type = "docx"
            return [file_type]
        if self.args.outputfiletype.lower() == "pdf":
            if self.can_convert_to_pdf:
                return ["pdf"]
            else:
                logging.error("PDF output selected but currently unable to output PDF on this OS.")
                return []
        if self.args.outputfiletype.lower() == "all":
            file_types = []
            for file_type in self.FILETYPE_CHOICES:
                if file_type != "all" and (file_type != "pdf" or self.can_convert_to_pdf):
                    file_types.append(file_type)
            return file_types
        if self.args.outputfiletype.lower() in self.FILETYPE_CHOICES:
            return [self.args.outputfiletype.lower()]
        return []

    def get_valid_language_choices(self) -> typing.List[str]:
        languages = []
        if self.args.language.lower() == "all":
            for language in self.LANGUAGE_CHOICES:
                if language not in ("all", "template"):
                    languages.append(language)
        elif self.args.language == "":
            languages.append("en")
        else:
            languages.append(self.args.language)
        return languages

    @staticmethod
    def set_logging(self) -> None:
        logging.basicConfig(
            format="%(asctime)s %(filename)s | %(levelname)s | %(funcName)s | %(message)s",
        )
        if self.args.debug:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)

    def convert_type_language(self, file_type: str, language: str = "en") -> None:
        # Get the list of available translation files
        yaml_files = self.get_files_from_of_type(os.sep.join([self.BASE_PATH, "source"]), "yaml")
        if not yaml_files:
            return

        # Get the language data from the correct language file (checks self.args.language to select the correct file)
        language_data: typing.Dict = self.get_replacement_data(yaml_files, "translation", language)
        if not language_data:
            return
        # If no data found in the language file, then exit with error
        if "suits" not in list(language_data.keys()):
            logging.error("Could not find the `suits` tag in the language file.")
            return
        # Get the dict of replacement data
        language_dict: typing.Dict = self.get_replacement_dict(language_data, False)

        # Get meta data from language data
        meta: typing.Dict = self.get_meta_data(language_data)
        if not meta:
            return

        mapping_dict: typing.Dict = self.get_mapping_dict(yaml_files)
        if not mapping_dict:
            return

        language_dict.update(mapping_dict)
        if Convert.making_template:
            language_dict = self.remove_short_keys(language_dict)

        template_doc: str = self.get_template_doc(file_type)

        # Name output file with correct edition, component, language & version
        output_file: str = self.rename_output_file(file_type, meta)
        self.ensure_folder_exists(os.path.dirname(output_file))

        # Work with docx file (and maybe convert to pdf afterwards)
        if file_type in ("docx", "pdf"):
            # Get the input (template) document
            doc: docx.Document = self.get_docx_document(template_doc)
            doc = self.replace_docx_inline_text(doc, language_dict)

            if file_type == "docx":
                doc.save(output_file)
            else:
                self.save_pdf_file(doc, output_file)

        elif file_type == "idml":
            self.save_idml_file(template_doc, language_dict, output_file)

        logging.info("New file saved: " + str(output_file))

    def save_idml_file(self, template_doc, language_dict, output_file) -> None:
        # Get the output path and temp output path to put the temp xml files
        output_path = self.BASE_PATH + "/output"
        temp_output_path = output_path + "/temp"
        # Ensure the output folder and temp output folder exist
        self.ensure_folder_exists(temp_output_path)
        logging.debug(" --- temp_folder for extraction of xml files = " + str(temp_output_path))

        # Unzip source xml files and place in temp output folder
        with zipfile.ZipFile(template_doc) as idml_archive:
            idml_archive.extractall(temp_output_path)
            logging.debug(" --- namelist of first few files in archive = " + str(idml_archive.namelist()[:5]))

        xml_files = self.get_files_from_of_type(temp_output_path, "xml")
        # Only Stories files have content to update
        for file in fnmatch.filter(xml_files, "*Stories*Story*"):
            self.replace_text_in_xml_file(file, language_dict)

        # Zip the files as an idml file in output folder
        logging.debug(" --- finished replacing text in xml files. Now zipping into idml file")
        self.zip_dir(temp_output_path, output_file)

        # If not debugging, delete temp folder and files
        if not self.args.debug and os.path.exists(temp_output_path):
            shutil.rmtree(temp_output_path, ignore_errors=True)

    def save_pdf_file(self, doc, output_file) -> None:
        # If file type is pdf, then save a temp docx file, convert the docx to pdf
        temp_output_file = os.sep.join([self.BASE_PATH, "output", "temp.docx"])
        doc.save(temp_output_file)
        logging.debug(f" --- temp_output_file = {temp_output_file}\n--- starting pdf conversion now.")

        if self.can_convert_to_pdf:
            # Use docx2pdf for windows and mac with MS Word installed
            docx2pdf.convert(temp_output_file, output_file)
        else:
            logging.warning(
                "Error. A temporary docx file was created in the output folder but cannot be converted "
                f"to pdf (yet) on operating system: {sys.platform}\n"
                "This does work on Windows and Mac with MS Word installed."
            )
            return None

        # If not debugging then delete the temp file
        if not self.args.debug:
            os.remove(temp_output_file)

    def get_mapping_dict(self, yaml_files: typing.List[str]) -> typing.Dict:
        mapping_data: typing.Dict = self.get_replacement_data(yaml_files, "mappings")
        if not mapping_data:
            return {}
        return self.get_replacement_dict(mapping_data, True)

    def set_can_convert_to_pdf(self) -> None:
        operating_system: str = sys.platform.lower()
        can_convert_to_pdf = operating_system.find("win") != -1 or operating_system.find("darwin") != -1
        logging.debug(f" --- operating system = {operating_system}, can_convert_to_pdf = {can_convert_to_pdf}")
        self.can_convert_to_pdf = can_convert_to_pdf

    @staticmethod
    def sort_keys_longest_to_shortest(replacement_dict) -> typing.List[tuple]:
        new_list = replacement_dict.items()
        return sorted(new_list, key=lambda s: len(s[0]), reverse=True)

    def replace_text_in_xml_file(self, file, replacement_dict) -> None:
        if os.path.getsize(file) == 0:
            return
        if Convert.making_template:
            replacement_values = self.sort_keys_longest_to_shortest(replacement_dict)
        else:
            replacement_values = replacement_dict.items()

        tree = ElTree.parse(file)
        all_content_elements = tree.findall(".//Content")

        found_element = False
        for el in all_content_elements:
            if el is not None:
                for k, v in replacement_values:
                    if el.text.find(k):
                        found_element = True
                        new_text = el.text.replace(k, v)
                        el.text = new_text
        if found_element:
            with open(file, "bw") as f:
                f.write(ElTree.tostring(tree.getroot(), encoding="utf-8"))

    @staticmethod
    def remove_short_keys(replacement_dict: typing.Dict, min_length: int = 40) -> typing.Dict:
        data2: typing.Dict = {}
        for key, value in replacement_dict.items():
            if len(key) >= min_length:
                data2[key] = value
        logging.debug(
            " --- Making template. Removed card_numbers. len replacement_dict = "
            f"{len(replacement_dict)}, len data2 = {len(data2)}"
        )
        return data2

    def get_template_doc(self, file_type: str) -> str:
        template_doc: str
        args_input_file: str = self.args.inputfile
        source_file_ext = file_type.replace("pdf", "docx")  # Pdf output uses docx source file
        if args_input_file:
            # Input file was specified
            if os.path.isabs(args_input_file):
                template_doc = args_input_file
            else:
                template_doc = os.path.normpath(self.SCRIPT_PATH + os.sep + args_input_file)
        else:
            # No input file specified - using defaults
            if Convert.making_template:
                # Creating a new template from an original docx or idml file
                template_doc = os.sep.join(
                    [self.BASE_PATH, "resources", "originals", "owasp_cornucopia_en." + source_file_ext]
                )
            else:
                template_doc = os.path.normpath(
                    self.SCRIPT_PATH + os.sep + self.DEFAULT_TEMPLATE_FILENAME + "." + source_file_ext
                )

            template_doc = self.check_fix_file_extension(template_doc, source_file_ext)
        logging.debug(f" --- template_doc = {template_doc}")

        if not os.path.isfile(template_doc):
            logging.error(f"Source file not found: {template_doc}. Please ensure file exists and try again.")
            return ""
        return template_doc

    def rename_output_file(self, file_type: str, meta: typing.Dict) -> str:
        """Rename output file replacing place-holders from meta dict (edition, component, language, version)."""
        args_output_file: str = self.args.outputfile
        logging.debug(f" --- args_output_file = {args_output_file}")
        if args_output_file:
            # Output file is specified as an argument
            if os.path.isabs(args_output_file):
                output_filename = args_output_file
            else:
                output_filename = os.path.normpath(self.SCRIPT_PATH + os.sep + args_output_file)
        else:
            # No output file specified - using default
            output_filename = os.path.normpath(
                self.SCRIPT_PATH
                + os.sep
                + self.DEFAULT_OUTPUT_FILENAME
                + ("_template" if Convert.making_template else "")
                + "."
                + file_type.strip(".")
            )

        logging.debug(f" --- output_filename before fix extension = {output_filename}")
        output_filename = self.check_fix_file_extension(output_filename, file_type)
        logging.debug(f" --- output_filename AFTER fix extension = {output_filename}")

        # Do the replacement of filename place-holders with meta data
        find_replace = self.get_find_replace_list(meta)
        f = os.path.basename(output_filename)
        for r in find_replace:
            f = f.replace(*r)
        output_filename = os.path.dirname(output_filename) + os.sep + f

        logging.debug(f" --- output_filename = {output_filename}")
        return output_filename

    @staticmethod
    def check_fix_file_extension(filename: str, file_type: str) -> str:
        if not filename.endswith(file_type):
            filename_split = os.path.splitext(filename)
            if filename_split[1].strip(".").isnumeric():
                filename = filename + "." + file_type.strip(".")
            else:
                filename = ".".join([os.path.splitext(filename)[0], file_type.strip(".")])
            logging.debug(f" --- output_filename with new ext = {filename}")
        return filename

    @staticmethod
    def get_find_replace_list(meta: typing.Dict) -> typing.Sequence[tuple]:
        ll = [
            ("_type", "_" + meta["edition"].lower()),
            ("_edition", "_" + meta["edition"].lower()),
            ("_component", "_" + meta["component"].lower()),
            ("_language", "_" + meta["language"].lower()),
            ("_lang", "_" + meta["language"].lower()),
            ("_version", "_" + meta["version"].lower()),
            ("_ver", "_" + meta["version"].lower()),
        ]
        if not Convert.making_template:
            ll.append(("_template", ""))
        return ll

    @staticmethod
    def get_meta_data(language_data: typing.Dict) -> typing.Dict:
        meta = {}
        if "meta" in list(language_data.keys()):
            for key, value in language_data["meta"].items():
                if key in ("edition", "component", "language", "version"):
                    meta[key] = value
            return meta
        else:
            logging.error(
                "Could not find meta tag in the language data. "
                "Please ensure required language file is in the source folder."
            )
        logging.debug(f" --- meta data = {meta}")
        return meta

    @staticmethod
    def get_replacement_data(yaml_files: typing.List[str], data_type: str = "translation", language: str = "") \
            -> typing.Dict:
        """Get the raw data of the replacement text from correct yaml file"""
        data = {}
        logging.debug(f" --- Starting get_replacement_data() for data_type = {data_type} and language = {language}")
        if Convert.making_template:
            lang = "en"
        else:
            lang = language
        for file in yaml_files:
            if (
                os.path.basename(file).find("-" + lang + ".") >= 0
                or os.path.basename(file).find("-" + lang.replace("-", "_") + ".") >= 0
                or os.path.basename(file).find("mappings") >= 0
            ):
                with open(file, "r", encoding="utf-8") as f:
                    try:
                        data = yaml.safe_load(f)
                    except yaml.YAMLError as e:
                        logging.info(f"Error loading yaml file: {f}. Error = {e}")
                        continue

                if data_type in ("translation", "translations") and (
                    (data["meta"]["language"].lower() == language)
                    or (data["meta"]["language"].lower() == "en" and language == "template")
                ):
                    logging.debug(" --- found source language file: " + os.path.split(file)[1])
                    return data
                elif (
                    data_type in ("mapping", "mappings")
                    and "meta" in data.keys()
                    and "component" in data["meta"].keys()
                    and data["meta"]["component"] == "mappings"
                ):
                    logging.debug(" --- found mappings file: " + os.path.split(file)[1])
                logging.debug(" --- found source file: " + os.path.split(file)[1])
                meta_keys = data["meta"].keys()
                logging.debug(f" --- data.keys() = {data.keys()}, data[meta].keys() = {meta_keys}")
        if not data:
            logging.error("Could not get language data from yaml files.")
        logging.debug(f" --- Len = {len(data)}.")
        return data

    def get_replacement_dict(self, input_data: typing.Dict, mappings=False) -> typing.Dict:
        """Loop through language file data and build up a find-replace dict"""
        data = {}
        for key in list(k for k in input_data.keys() if k != "meta"):
            suit_tags, suit_key = self.get_suit_tags_and_key(key)

            for suit, suit_tag in zip(input_data[key], suit_tags):
                logging.debug(" --- suit [name] = " + str(suit["name"]) + "\n --- suit_tag = " + str(suit_tag))
                tag_for_suit_name = Convert.get_tag_for_suit_name(suit, suit_tag)
                data.update(tag_for_suit_name)

                card_tag = ""
                for card in suit[suit_key]:
                    for tag, text_output in card.items():
                        if tag == "value":
                            continue

                        full_tag = self.get_full_tag(suit_tag, card["value"], tag)

                        # Mappings is sometimes loaded as a list. Convert to string
                        if mappings:
                            text_output = self.check_make_list_into_text(text_output)

                        # Add a translation for "Joker"
                        if suit_tag == "WC" and tag == "value":
                            full_tag = "${{{}}}".format("_".join([suit_tag, card_tag, tag]))

                        if Convert.making_template:
                            data[text_output] = full_tag
                        else:
                            data[full_tag] = text_output
        if self.args.debug:
            debug_txt = " --- Translation data showing First 4 (key: text):\n* "
            debug_txt += "\n* ".join(l1 + ": " + str(data[l1]) for l1 in list(data.keys())[:4])
            logging.debug(debug_txt)
            debug_txt = " --- Translation data showing Last 4 (key: text):\n* "
            debug_txt += "\n* ".join(l1 + ": " + str(data[l1]) for l1 in list(data.keys())[-4:])
            logging.debug(debug_txt)
        return data

    @staticmethod
    def check_make_list_into_text(var) -> str:
        if isinstance(var, list):
            text_output = ", ".join(str(s) for s in list(var))
            if len(text_output.strip()) == 0:
                text_output = " - "
            return text_output
        else:
            return var

    @staticmethod
    def get_suit_tags_and_key(key: str) -> typing.Tuple:
        # Short tags to match the suits in the template documents
        suit_tags = []
        suit_key = ""
        if key == "suits":
            suit_tags = ["VE", "AT", "SM", "AZ", "CR", "CO", "WC"]
            suit_key = "cards"
        elif key == "paragraphs":
            suit_tags = ["Common"]
            suit_key = "sentences"
        return suit_tags, suit_key

    @staticmethod
    def get_tag_for_suit_name(suit, suit_tag) -> typing.Dict:
        data = {}
        if Convert.making_template:
            data[suit["name"]] = "${{{}}}".format(suit_tag + "_suit")
            if suit_tag == "WC":
                data["Joker"] = "${WC_Joker}"
        else:
            data["${{{}}}".format(suit_tag + "_suit")] = suit["name"]
            if suit_tag == "WC":
                data["${WC_Joker}"] = "Joker"
        logging.debug(f" --- making_template = {Convert.making_template}, suit_tag dict = {data}")
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

    def replace_docx_inline_text(self, doc, data) -> docx.Document:
        """Replace the text in the docx document."""
        logging.debug(" --- starting docx_replace")

        if Convert.making_template:
            replacement_values = self.sort_keys_longest_to_shortest(data)
        else:
            replacement_values = data.items()
        rv = list(k + ": " + v + "; " for k, v in replacement_values)
        logging.debug(f" --- last 5 replacement values are:\n{rv[-5:]}")

        paragraphs = self.get_document_paragraphs(doc)
        for p in paragraphs:
            runs_text = "".join(r.text for r in p.runs)
            if Convert.making_template and re.search(re.escape("${") + ".*" + re.escape("}"), runs_text):
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

    @staticmethod
    def get_document_paragraphs(doc) -> typing.List:
        paragraphs = list(doc.paragraphs)
        l1 = l2 = len(paragraphs)
        for t in doc.tables:
            for row in t.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        if len(paragraph.runs):
                            paragraphs.append(paragraph)
                    l2 = len(paragraphs)
        if not len(paragraphs):
            logging.error("No paragraphs found in doc")
        logging.debug(f" --- count doc paragraphs = {l1}, with table paragraphs = {l2}")
        return paragraphs

    @staticmethod
    def get_docx_document(docx_file: str) -> docx.Document:
        """Open the file and return the docx document."""
        if os.path.isfile(docx_file):
            return docx.Document(docx_file)
        else:
            logging.error("Could not find file at: " + str(docx_file))
            return docx.Document()

    def get_files_from_of_type(self, path: str, ext: str) -> typing.List[str]:
        """Get a list of files from a specified folder recursively, that have the specified extension."""
        files = []
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, "*." + str(ext)):
                files.append(os.path.join(root, filename))
        if not files:
            logging.error("No language files found in folder: " + str(os.sep.join([self.BASE_PATH, "source"])))
        logging.debug(
            f" --- found {len(files)} files of type {ext}. Showing first few:\n* " + str("\n* ".join(files[:3]))
        )
        return files

    @staticmethod
    def set_making_template(self) -> None:
        if hasattr(self.args, "language"):
            self.making_template = self.args.language.lower() == "template"
        else:
            self.making_template = False

    def parse_arguments(self, input_args: typing.List[str]) -> argparse.Namespace:
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
                "Specify a path and name of output file to generate. (caution: existing file will be overwritten). "
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
