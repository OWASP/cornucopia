import unittest
import argparse
import os
import docx

from scripts.convert import Convert as c


class TestParseArguments(unittest.TestCase):
    def test_successfully_parsing_arguments_short_form_basic(self) -> None:
        input_args = ["-t", "idml"]
        want_args = argparse.Namespace(
            inputfile="",
            outputfiletype="idml",
            outputfile="",
            language="en",
            debug=False,
        )

        got_args = c.parse_arguments(c, input_args)
        self.maxDiff = None
        self.assertEqual(got_args, want_args)

    def test_successfully_parsing_arguments_short_form_language(self) -> None:
        input_args = ["-t", "idml", "-l", "fr"]
        want_args = argparse.Namespace(
            inputfile="",
            outputfiletype="idml",
            outputfile="",
            language="fr",
            debug=False,
        )

        got_args = c.parse_arguments(c, input_args)
        self.maxDiff = None
        self.assertEqual(got_args, want_args)

    def test_successfully_parsing_arguments_long_form_basic(self) -> None:
        input_args = ["--outputfiletype", "idml"]
        want_args = argparse.Namespace(
            inputfile="",
            outputfiletype="idml",
            outputfile="",
            language="en",
            debug=False,
        )

        got_args = c.parse_arguments(c, input_args)
        self.maxDiff = None
        self.assertEqual(got_args, want_args)

    def test_successfully_parsing_arguments_long_form_language(self) -> None:
        input_args = ["--outputfiletype", "idml", "--language", "fr"]
        want_args = argparse.Namespace(
            inputfile="",
            outputfiletype="idml",
            outputfile="",
            language="fr",
            debug=False,
        )

        got_args = c.parse_arguments(c, input_args)
        self.maxDiff = None
        self.assertEqual(got_args, want_args)


class TestMakeTemplate(unittest.TestCase):
    def test_make_template_true(self) -> None:
        c.args = argparse.Namespace(language="template")

        result = c.make_template(c)
        self.assertTrue(result)

    def test_make_template_false(self) -> None:
        c.args = argparse.Namespace(language="en")

        result = c.make_template(c)
        self.assertFalse(result)

    def test_make_template_empty(self) -> None:
        c.args = argparse.Namespace()

        result = c.make_template(c)
        self.assertFalse(result)


class TestGetFilesFromOfType(unittest.TestCase):
    def test_get_files_from_of_type_source_yaml_files(self) -> None:
        c.args = argparse.Namespace(debug=False)
        path = c.BASE_PATH + "/test/test_files/"
        ext = "yaml"
        want_list = ["ecommerce-cards-1.21-en.yaml",
                     "ecommerce-mappings-1.2.yaml"]

        got_list = c.get_files_from_of_type(c, path, ext)
        got_files = list(os.path.basename(f) for f in got_list)
        for f in want_list:
            self.assertIn(f, got_files)

    def test_get_files_from_of_type_source_docx_files(self) -> None:
        c.args = argparse.Namespace(debug=False)
        path = c.BASE_PATH + "/test/test_files/"
        ext = "docx"
        want_list = ["owasp_cornucopia_edition_lang_ver_template.docx"]

        got_list = c.get_files_from_of_type(c, path, ext)
        got_files = list(os.path.basename(f) for f in got_list)
        for f in want_list:
            self.assertIn(f, got_files)

    def test_get_files_from_of_type_source_empty_list(self) -> None:
        c.args = argparse.Namespace(debug=False)
        path = c.BASE_PATH + "/test/test_files/"
        ext = "ext"
        want_list = []

        got_list = c.get_files_from_of_type(c, path, ext)
        self.assertListEqual(got_list, want_list)


class TestGetDocxDocument(unittest.TestCase):
    def test_get_docx_document_success(self) -> None:
        c.args = argparse.Namespace(debug=False)
        file = c.BASE_PATH + "/test/test_files/owasp_cornucopia_edition_lang_ver_template.docx"
        want_type = docx.document.Document
        want_len_paragraphs = 36


# print("--- doc first 500:\n" + str(type(doc_test)))
# print("--- doc first 500:\n" + str(isinstance(doc_test, docx.document.Document)))
# print("--- doc first 500:\n" + str(len(doc_test.paragraphs)));
# exit()

