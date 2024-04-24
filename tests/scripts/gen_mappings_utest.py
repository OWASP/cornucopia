import unittest
import argparse
import yaml
from unittest.mock import patch
from scripts import gen_mappings as gm

if "unittest.util" in __import__("sys").modules:
    # Show full diff in self.assertEqual.
    __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999


class TestProduceEcommerceMappings(unittest.TestCase):
    def test_can_produce_ecommerce_mappings(self):
        test_input = {
            "meta": {"language": "EN", "version": "1.30"},
            "suits": [
                {"cards": [{"cre": ["308-515"], "value": "2"}], "name": "Data validation & encoding", "code": "VE"},
                {"cards": [{"cre": ["138-448"], "value": "2"}], "name": "Session management", "code": "SM"},
            ],
        }
        language_mapping = {
            "meta": {"language": "EN", "version": "1.30"},
            "suits": [
                {"name": "Data validation & encoding", "cards": [{"desc": "DV2 test"}]},
                {"name": "Session management", "cards": [{"desc": "SM2 test"}]},
            ],
        }
        expected = {
            "meta": {"component": "mappings", "edition": "ecommerce", "language": "EN", "version": "1.30"},
            "standards": [
                {
                    "doctype": "Tool",
                    "name": "Data validation & encoding",
                    "section": "DV2 test",
                    "sectionID": "VE2",
                    "hyperlink": "https://github.com/OWASP/cornucopia/wiki/VE2",
                    "links": [{"document": {"doctype": "CRE", "id": "308-515"}}],
                    "tags": [],
                    "tooltype": "Defensive",
                },
                {
                    "doctype": "Tool",
                    "name": "Session management",
                    "section": "SM2 test",
                    "sectionID": "SM2",
                    "hyperlink": "https://github.com/OWASP/cornucopia/wiki/SM2",
                    "links": [{"document": {"doctype": "CRE", "id": "138-448"}}],
                    "tags": [],
                    "tooltype": "Defensive",
                },
            ],
        }
        self.assertEqual(gm.produce_ecommerce_mappings(test_input, language_mapping), expected)


class MainTestCase(unittest.TestCase):

    @patch("builtins.print")
    @patch("builtins.open")
    def test_main(self, mock_open, mock_print):
        args = {
            "cres": "source/cre-mappings.yaml",
            "lang": "source/ecommerce-cards-1.30-en.yaml",
            "qr_images": None,
            "target": "output/mapping.json",
        }
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.read.return_value = "content"
        with patch.object(argparse, "ArgumentParser") as mock_parser:
            mock_parser.return_value.parse_args.return_value = argparse.Namespace(**args)
            with patch.object(yaml, "safe_load") as mock_load:
                with open("output/mapping.json", "w") as mock_write:
                    mock_write("test")
                    mock_load.return_value = {
                        "meta": {"language": "EN", "version": "1.30"},
                        "suits": [
                            {
                                "cards": [{"cre": ["308-515"], "value": "2", "desc": ""}],
                                "name": "Data validation & encoding",
                                "code": "VE",
                            },
                            {
                                "cards": [{"cre": ["138-448"], "value": "2", "desc": ""}],
                                "name": "Session management",
                                "code": "SM",
                            },
                        ],
                    }
                    gm.main()
                    mock_print.assert_not_called()
                    mock_open.assert_called_with("output/mapping.json", "w")


if __name__ == "__main__":
    unittest.main()
