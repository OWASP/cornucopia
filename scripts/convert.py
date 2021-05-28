#!/usr/bin/env python3

import argparse
# import json
import logging
import os
import sys
import yaml
import fnmatch
from typing import List #, TextIO
import docx

# from simple_idml import idml
# from simple_idml.indesign import indesign
# from simple_idml import indesign

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
# pdf_template_file = SCRIPT_PATH + "/../resources/templates/cornucopia.pdf"
# idml_template_file = SCRIPT_PATH + "/../resources/templates/print-ready/template.idml"

args: {}

def main() -> None:
    logging.basicConfig(
        format="%(asctime)s %(filename)s | %(levelname)s | %(funcName)s | %(message)s",
        level=logging.INFO,
    )
    global args
    args = parse_arguments(sys.argv[1:])

    ## Get the language files and find the output language needed
    yaml_files = get_yaml_files(SCRIPT_PATH + "/../source")

    if len(yaml_files) == 0:
        msg = "Error. No language files found in folder: " + SCRIPT_PATH + "/../source"
        print(msg)
        ## Todo: log this error
        exit()

    for file in yaml_files:
        # if args.debug: print("--- file = " + str(file))
        with open(file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        # if args.debug: print("--- loaded data successfully. " + str(file) + " with " + str(len(data)) + " keys: " + str(data.keys()))

        if (data["meta"]["language"].lower() == args.language.lower()) \
            or (data["meta"]["language"].lower() == "en" and args.language.lower() == "template"):
            lang_out_data = data
            if args.debug: print("--- found source language file: " + os.path.split(file)[1])
            break

    ## If no language found
    if "data" not in list(lang_out_data): # or "data" not in list(lang_template_data):
        msg = "Error. Could not find the `data` tag in one- or both of the language files."
        print(msg)
        # log this error
        exit()


    ## Get the dict of replacement data
    data = get_replacement_dict(lang_out_data)


    ## Work with docx file
    if args.inputfile == "":
        template_doc = SCRIPT_PATH + "/../source/owasp_cornucopia_template_v1.21.docx"
    else:
        template_doc = args.inputfile
    template_doc = os.path.normpath(template_doc)

    ## If outputting a template
    if args.language == "template":
        if args.outputfile in ["", None]:
            output_file = SCRIPT_PATH + "/../source/owasp_cornucopia_template.docx"
        else:
            output_file = args.outputfile
    else:
        if args.debug: print("--- args.outputfile = " + str(args.outputfile))
        if args.outputfile in ["", None]:
            output_file = template_doc.replace("_template_", "_"+args.language+"_").replace("source","output")
        else:
            output_file = args.outputfile
    output_file = os.path.normpath(output_file)


    ## Get the input (template) document
    doc = docx.Document(template_doc)

    ## Replace the text with the data from the source translation file
    docx_replace(doc, data)

    ## Check output path exists
    if not os.path.exists(os.path.dirname(output_file)):
        os.mkdir(os.path.dirname(output_file))

    ## Save the output file
    doc.save(output_file)
    print("New file saved: " + str(output_file))




##
# function: docx_replace()
# Credits: github/adejones
# URL: https://gist.github.com/adejones/a6d42984f66ea9990d78974531863bee
# Modified and simplified by GDBryant
##
def docx_replace(doc, data) -> docx.Document:
    if args.debug: print("--- starting docx_replace")

    ## Get all the paragraphs together
    paragraphs = list(doc.paragraphs)
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    paragraphs.append(paragraph)
    for p in paragraphs:
        for key, val in data.items():
            runs_text = "".join(r.text for r in p.runs)
            if key in runs_text:
                if args.debug and key.find("VE_VE0_desc") != -1: print("--- found key: " + str(key) + ", \n--- runs before = [" + str(",".join(r.text for r in p.runs)), "] val = " + str(val))
                t = runs_text.replace(key, val)
                for i,r in enumerate(p.runs):
                    p.runs[i].text = ""
                p.runs[0].text = str(t).strip()
                if args.debug and key.find("VE_VE0_desc") != -1: print("--- runs after = " + str("; ".join(r.text for r in p.runs)))
    if args.debug: print("--- finished replacing text in doc")


def get_replacement_dict(lang_out_data) -> dict:
    ## Loop through language files and build up a find-replace dict
    data = {}
    ## Stuff to ignore
    card_numbers = ['a','2','3','4','5','6','7','8','9', '10', '0', 'j','q','k']
    for suit, suit_out in lang_out_data["data"].items():
        for card, card_out in suit_out.items():
            if isinstance(card_out, dict):
                for tag, tag_out in card_out.items():
                    ## Ignore the card numbers/letters
                    if tag_out.lower() not in card_numbers:
                        ## Create template placeholders in the form ${suit_card_tag}.
                        key_name =  "_".join([suit,card,tag])
                        if args.language == "template":
                            data[tag_out] = '${{{}}}'.format(key_name)
                        else:
                            data['${{{}}}'.format(key_name)] = tag_out
                            # if args.debug and suit == "VE": print("--- tag = " + '${{{}}}'.format(key_name) + ", out [:20] = " + tag_out[:20])
            else:
                ## Ignore the card numbers/letters
                if card_out.lower() not in card_numbers:
                    ## Create template placeholders in the form ${suit_card}
                    key_name =  "_".join([suit,card])
                    if args.language == "template":
                        data[card_out] = '${{{}}}'.format(key_name)
                    else:
                        data['${{{}}}'.format(key_name)] = card_out
    if args.debug: print("--- data keys()[:10]:\n* " + "\n* ".join(list(data.keys())[:10]))
    return data


def get_docx(docx_file) -> docx.Document:
    if os.path.isfile(docx_file):
        return docx.Document(docx_file, encoding="utf-8")
    else:
        print("Error. Could not find file at: " + str(docx_file))
        return docx.Document()


def get_yaml_files(path) -> List[str]:
    yaml_files = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, "*.yaml"):
            yaml_files.append(os.path.join(root, filename))
    if args.debug: print("--- found yaml files:\n* " + str("\n* ".join(yaml_files)))
    return yaml_files


def parse_arguments(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tool to convert.")
    parser.add_argument(
        "-if",
        "--inputfile",
        type=str,
        default="",
        help="Input (template) file to use. ",
    )
    parser.add_argument(
        "-of",
        "--outputfile",
        type=str,
        help="Path and name of output file to generate. (caution: existing file will be overwritten)",
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-oft",
        "--outputfiletype",
        type=str,
        choices=["json", "pdf", "indd", "docx"],
        default="docx",
        help="Output format to produce. Default = docx",
    )
    # group = parser.add_mutually_exclusive_group(required=False)
    # group.add_argument(
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        # choices=["en", "es", "fr", "pt-br"],
        default="en",
        help="Output language to produce. [`en`, `es`, `fr`, `pt-br`, `template`] (template will attempt to create a template from the english input file - replacing strings with the template lookup codes",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Output additional information to debug script",
        )
    return parser.parse_args(args)


if __name__ == "__main__":
    main()
