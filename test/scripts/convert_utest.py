import argparse
import unittest

from scripts.convert import (
    parse_arguments,
)


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

        got_args = parse_arguments(input_args)
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

        got_args = parse_arguments(input_args)
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

        got_args = parse_arguments(input_args)
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

        got_args = parse_arguments(input_args)
        self.maxDiff = None
        self.assertEqual(got_args, want_args)
