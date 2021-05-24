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
        # log this error
        exit()

    for file in yaml_files:
        # if args.debug: print("--- file = " + str(file))
        with open(file, "r") as f:
            data = yaml.safe_load(f)
        # if args.debug: print("--- loaded data successfully. " + str(file) + " with " + str(len(data)) + " keys: " + str(data.keys()))

        if (data["meta"]["language"].lower() == args.language.lower()) or (data["meta"]["language"].lower() == "en" and args.language.lower() == "template"):
            lang_out_data = data
            if args.debug: print("--- found output language file: " + os.path.split(file)[1])
        if data["meta"]["language"].lower() == "en":
            lang_template_data = data
            if args.debug: print("--- found template language file: " + os.path.split(file)[1])

    if "data" not in list(lang_out_data) or "data" not in list(lang_template_data):
        msg = "Error. Could not find the `data` tag in one- or both of the language files."
        print(msg)
        # log this error
        exit()
        
    ## Loop through language files and build up a find-replace dict
    data = {}
    card_numbers = ['a','2','3','4','5','6','7','8','9','j','q','k']
    for suit, suit_out in lang_out_data["data"].items():
        if suit in lang_template_data["data"].keys():
            suit_find = lang_template_data["data"][suit]
            for tag, tag_out in suit_out.items():
                if tag in suit_find.keys():
                    tag_find = suit_find[tag]
                    if isinstance(tag_out, dict):
                        for tag_sub, tag_sub_out in tag_out.items():
                            if tag_sub in tag_find.keys():
                                tag_sub_find = tag_find[tag_sub]
                                #Do not need replace if input and output are the same
                                if tag_sub_find.lower() not in card_numbers:
                                    if args.language == "template":
                                        # use placeholders in the form ${PlaceholderName}
                                        key_name =  "_".join([suit,tag,tag_sub])
                                        data[tag_sub_find] = '${{{}}}'.format(key_name)
                                    else:
                                        if tag_sub_find != tag_sub_out:
                                            data[tag_sub_find] = tag_sub_out
                    else:
                        #Do not need replace if input and output are the same
                        if tag_find.lower() not in card_numbers:
                            if args.language == "template":
                                # use placeholders in the form ${PlaceholderName}
                                key_name =  "_".join([suit,tag])
                                data[tag_find] = '${{{}}}'.format(key_name)
                            else:
                                #Do not need replace if input and output are the same
                                if tag_find != tag_out:
                                    data[tag_find] = tag_out

    # if args.debug: print("--- data keys()[:5]:\n* " + "\n* ".join(list(data.keys())[:5]))
    
    ## Work with docx file
    # template_doc = SCRIPT_PATH + "/../../owasp_cornucopia_v1.21.docx"
    template_doc = SCRIPT_PATH + "/../../www-project-cornucopia/assets/files/ecommerce/EN/OWASP-Cornucopia-Ecommerce_Website-EN-1v20.docx"
    if args.language == "template":
        output_file_name = SCRIPT_PATH + "/../../template.docx" #Ignore type for now + args.output
    else:
        output_file_name = SCRIPT_PATH + "/../../test_output.docx" #Ignore type for now + args.output

    doc = docx.Document(template_doc)
    docx_replace(doc, data)
    doc.save(output_file_name)
    


##
# function: docx_replace()
# Credits: github/adejones
# URL: https://gist.github.com/adejones/a6d42984f66ea9990d78974531863bee
# Credits: github/GastonDonnet
# URL: https://gist.github.com/GastonDonnet/cff16e773a6245e536f957bd8b5eba6c
##
def docx_replace(doc, data):
    def replace_inline(key_name, val, inline):
        # Replace strings and retain the same style.
        # The text to be replaced can be split over several runs so
        # search through, identify which runs need to have text replaced
        # then replace the text in those identified
        started = False
        key_index = 0
        # found_runs is a list of (inline index, index of match, length of match)
        found_runs = list()
        found_all = False
        replace_done = False
        for i in range(len(inline)):
    
            # case 1: found in single run so short circuit the replace
            # if key_name in inline[i].text and not started:
            if key_name == inline[i].text and not started:
                found_runs.append((i, inline[i].text.find(key_name), len(key_name)))
                text = inline[i].text.replace(key_name, str(val))
                inline[i].text = text
                replace_done = True
                found_all = True
                break
    
            # if key_name[key_index] not in inline[i].text and not started:
            if key_name[key_index] != inline[i].text and not started:
                # keep looking ...
                continue
    
            # case 2: search for partial text, find first run
            # if key_name[key_index] in inline[i].text and inline[i].text[-1] in key_name and not started:
            if key_name[key_index] == inline[i].text and inline[i].text[-1] in key_name and not started:
                # check sequence
                start_index = inline[i].text.find(key_name[key_index])
                check_length = len(inline[i].text)
                for text_index in range(start_index, check_length):
                    if inline[i].text[text_index] != key_name[key_index]:
                        # no match so must be false positive
                        break
                if key_index == 0:
                    started = True
                chars_found = check_length - start_index
                key_index += chars_found
                found_runs.append((i, start_index, chars_found))
                if key_index != len(key_name):
                    continue
                else:
                    # found all chars in key_name
                    found_all = True
                    break
    
            # case 2: search for partial text, find subsequent run
            # if key_name[key_index] in inline[i].text and started and not found_all:
            if key_name[key_index] == inline[i].text and started and not found_all:
                # check sequence
                chars_found = 0
                check_length = min(len(inline[i].text), len(key_name[key_index]) - key_index)
                for text_index in range(0, check_length):
                    if inline[i].text[text_index] == key_name[key_index]:
                        key_index += 1
                        chars_found += 1
                    else:
                        break
                # no match so must be end
                found_runs.append((i, 0, chars_found))
                if key_index == len(key_name):
                    found_all = True
                    break
    
        if found_all and not replace_done:
            for i, item in enumerate(found_runs):
                index, start, length = [t for t in item]
                if i == 0:
                    text = inline[index].text.replace(inline[index].text[start:start + length], str(val))
                    inline[index].text = text
                else:
                    text = inline[index].text.replace(inline[index].text[start:start + length], '')
                    inline[index].text = text
            if key_name in p.text:
                replace_inline(key_name, val, inline)

    ## Now start the work
    paragraphs = list(doc.paragraphs)
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    paragraphs.append(paragraph)
    for p in paragraphs:
        for key, val in data.items():
            # key_name = '${{{}}}'.format(key) # use placeholders in the form ${PlaceholderName}
            key_name = key
            if key_name in p.text:
                inline = p.runs
                replace_inline(key_name, val, inline)    



def get_docx(docx_file) -> docx.Document:
    if os.path.isfile(docx_file):
        return docx.Document(docx_file)
    else:
        print("Error. Could not find file at: " + str(docx_file))
        return docx.Document()


# def get_idml_package(idml_file) -> idml.IDMLPackage:
#     if os.path.isfile(idml_file):
#         idml_package = idml.IDMLPackage(idml_file)
#         # if args.debug: print("--- idml_package stories [:5] = " + str(idml_package.spreads[:5]))
#         return idml_package
#     else:
#         return None

def get_yaml_files(path) -> List[str]:
    yaml_files = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, "*.yaml"):
            yaml_files.append(os.path.join(root, filename))
    if args.debug: print("--- yaml_files = " + str(yaml_files))
    return yaml_files


def parse_arguments(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tool to convert.")
    parser.add_argument(
        "-if",
        "--inputfile",
        type=str,
        default="",
        help="Input file to use. ",
    )
    parser.add_argument(
        "-ift",
        "--inputfiletype",
        type=str,
        default="docxtemplate",
        help="Input file is of type: [`docxtemplate`,`docx`]. Default = docxtemplate",
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
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        # choices=["en", "es", "fr", "pr-br"],
        default="en",
        help="Output language to produce. [`en`, `es`, `fr`, `pr-br`, `template`] (template will generate a new template file using english input)",
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
