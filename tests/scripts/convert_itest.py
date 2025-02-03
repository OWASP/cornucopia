import unittest
from unittest.mock import patch
import argparse
import os
import platform
import sys
import docx  # type: ignore
import logging
import glob
import shutil
import typing
from typing import List, Dict, Any, Tuple

import scripts.convert as c

c.convert_vars = c.ConvertVars()


if "unittest.util" in __import__("sys").modules:
    # Show full diff in self.assertEqual.
    __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999


class TestMain(unittest.TestCase):
    def setUp(self) -> None:
        self.b = c.convert_vars.BASE_PATH
        c.convert_vars.BASE_PATH = os.sep.join([self.b, "tests", "test_files"])
        self.template_docx_file = os.sep.join(
            [
                c.convert_vars.BASE_PATH,
                "resources",
                "templates",
                "owasp_cornucopia_webapp_ver_guide_bridge_lang.docx",
            ]
        )
        self.args = ["-t", "bridge", "-lt", "guide", "-l", "en", "-v", "1.22", "-i", self.template_docx_file]
        self.argp = {
            "debug": False,
            "pdf": False,
            "edition": "webapp",
            "template": "bridge",
            "layout": "guide",
            "language": "en",
            "version": "1.22",
            "inputfile": self.template_docx_file,
            "outputfile": "",
        }
        self.mapping_file = os.sep.join(
            [
                c.convert_vars.BASE_PATH,
                "source",
                "webapp-mappings-1.22.yaml",
            ]
        )

        self.outputfile = os.sep.join(
            [
                c.convert_vars.BASE_PATH,
                "output",
                "owasp_cornucopia_webapp_1.22_guide_bridge_en.docx",
            ]
        )

    def tearDown(self) -> None:
        c.convert_vars.BASE_PATH = self.b

    def test_main(self):

        with patch.object(argparse, "ArgumentParser") as mock_parser:
            mock_parser.return_value.parse_args.return_value = argparse.Namespace(**self.argp)
            with self.assertLogs(logging.getLogger(), logging.INFO) as l6:
                with patch("sys.argv", self.args):
                    c.main()
            self.assertIn(
                f"INFO:root:New file saved: {self.outputfile}",
                l6.output,
            )


if __name__ == "__main__":
    unittest.main()
