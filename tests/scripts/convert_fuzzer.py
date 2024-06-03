import argparse
import logging
import unittest
from unittest.mock import patch
import sys
import atheris
import os
import convert as c

c.convert_vars = c.ConvertVars()


def test_main(data):
    test = unittest.TestCase()
    fdp = atheris.FuzzedDataProvider(data)
    edition = fdp.ConsumeUnicodeNoSurrogates(1024)
    template = fdp.ConsumeUnicodeNoSurrogates(1024)
    layout = fdp.ConsumeUnicodeNoSurrogates(1024)
    lang = fdp.ConsumeUnicodeNoSurrogates(1024)
    version = fdp.ConsumeUnicodeNoSurrogates(1024)
    inputtemplate = fdp.ConsumeUnicodeNoSurrogates(1024)
    outputfile = fdp.ConsumeUnicodeNoSurrogates(1024)
    b = c.convert_vars.BASE_PATH
    c.convert_vars.BASE_PATH = os.sep.join([b, "test_files"])
    template_docx_file = os.sep.join(
        [
            c.convert_vars.BASE_PATH,
            "resources",
            "templates",
            "owasp_cornucopia_webapp_ver_guide_bridge_lang.docx",
        ]
    )
    args = ["-t", template, "-lt", "guide", "-l", "en", "-v", "1.22", "-i", template_docx_file]
    argp = {
        "debug": False,
        "pdf": False,
        "edition": "webapp",
        "template": template,
        "layout": "guide",
        "language": "en",
        "version": "1.22",
        "inputfile": template_docx_file,
        "outputfile": "",
    }

    outputfile = os.sep.join(
        [
            c.convert_vars.BASE_PATH,
            "output",
            "owasp_cornucopia_webapp_1.22_guide_bridge_en.docx",
        ]
    )

    try:
        with patch.object(argparse, "ArgumentParser") as mock_parser:
            mock_parser.return_value.parse_args.return_value = argparse.Namespace(**argp)
            with test.assertLogs(logging.getLogger(), logging.INFO) as l6:
                with patch("sys.argv", args):
                    c.main()

            args = ["-e", edition, "-t", "bridge", "-lt", "guide", "-l", "en", "-v", "1.22", "-i", template_docx_file]
            argp = {
                "debug": False,
                "pdf": False,
                "edition": edition,
                "template": "bridge",
                "layout": "guide",
                "language": "en",
                "version": "1.22",
                "inputfile": template_docx_file,
                "outputfile": "",
            }

            mock_parser.return_value.parse_args.return_value = argparse.Namespace(**argp)
            with test.assertLogs(logging.getLogger(), logging.INFO) as l6:
                with patch("sys.argv", args):
                    c.main()

            args = ["-e", "webapp", "-t", "bridge", "-lt", layout, "-l", "en", "-v", "1.22", "-i", template_docx_file]
            argp = {
                "debug": False,
                "pdf": False,
                "edition": "webapp",
                "template": "bridge",
                "layout": layout,
                "language": "en",
                "version": "1.22",
                "inputfile": template_docx_file,
                "outputfile": "",
            }

            mock_parser.return_value.parse_args.return_value = argparse.Namespace(**argp)
            with test.assertLogs(logging.getLogger(), logging.INFO) as l6:
                with patch("sys.argv", args):
                    c.main()

            args = ["-e", "webapp", "-t", "bridge", "-lt", "guide", "-l", lang, "-v", "1.22", "-i", template_docx_file]
            argp = {
                "debug": False,
                "pdf": False,
                "edition": "webapp",
                "template": "bridge",
                "layout": "guide",
                "language": lang,
                "version": "1.22",
                "inputfile": template_docx_file,
                "outputfile": "",
            }

            mock_parser.return_value.parse_args.return_value = argparse.Namespace(**argp)
            with test.assertLogs(logging.getLogger(), logging.INFO) as l6:
                with patch("sys.argv", args):
                    c.main()

            args = ["-e", "webapp", "-t", "bridge", "-lt", "guide", "-l", "en", "-v", version, "-i", template_docx_file]
            argp = {
                "debug": False,
                "pdf": False,
                "edition": "webapp",
                "template": "bridge",
                "layout": "guide",
                "language": "en",
                "version": version,
                "inputfile": template_docx_file,
                "outputfile": "",
            }

            mock_parser.return_value.parse_args.return_value = argparse.Namespace(**argp)
            with test.assertLogs(logging.getLogger(), logging.INFO) as l6:
                with patch("sys.argv", args):
                    c.main()

            args = ["-e", "webapp", "-t", "bridge", "-lt", "guide", "-l", lang, "-v", "1.22", "-i", template_docx_file]
            argp = {
                "debug": False,
                "pdf": False,
                "edition": "webapp",
                "template": "bridge",
                "layout": "guide",
                "language": lang,
                "version": "1.22",
                "inputfile": template_docx_file,
                "outputfile": "",
            }

            mock_parser.return_value.parse_args.return_value = argparse.Namespace(**argp)
            with test.assertLogs(logging.getLogger(), logging.INFO) as l6:
                with patch("sys.argv", args):
                    c.main()

            args = [
                "-e",
                "webapp",
                "-t",
                "bridge",
                "-lt",
                "guide",
                "-l",
                "en",
                "-v",
                "1.22",
                "-i",
                template_docx_file,
                "-o",
                outputfile,
            ]
            argp = {
                "debug": False,
                "pdf": False,
                "edition": "webapp",
                "template": "bridge",
                "layout": "guide",
                "language": "en",
                "version": "1.22",
                "inputfile": template_docx_file,
                "outputfile": outputfile,
            }

            mock_parser.return_value.parse_args.return_value = argparse.Namespace(**argp)
            with test.assertLogs(logging.getLogger(), logging.INFO) as l6:
                with patch("sys.argv", args):
                    c.main()

            args = ["-e", "webapp", "-t", "bridge", "-lt", "guide", "-l", "en", "-v", "1.22", "-i", inputtemplate]
            argp = {
                "debug": False,
                "pdf": False,
                "edition": "webapp",
                "template": "bridge",
                "layout": "guide",
                "language": "en",
                "version": "1.22",
                "inputfile": inputtemplate,
                "outputfile": "",
            }

            mock_parser.return_value.parse_args.return_value = argparse.Namespace(**argp)
            with test.assertLogs(logging.getLogger(), logging.INFO) as l6:
                with patch("sys.argv", args):
                    c.main()

    except Exception:
        c.convert_vars.BASE_PATH = b
        print(f"{l6}")
        raise Exception("Convert main died!")
    test.assertTrue(True)
    c.convert_vars.BASE_PATH = b


def main():
    atheris.instrument_all()
    atheris.Setup(sys.argv, test_main)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
