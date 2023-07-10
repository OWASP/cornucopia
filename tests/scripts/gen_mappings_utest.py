import unittest
import argparse
import yaml
from unittest.mock import MagicMock, patch
from scripts import gen_mappings as gm

if "unittest.util" in __import__("sys").modules:
    # Show full diff in self.assertEqual.
    __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999


class TestProduceEcommerceMappings(unittest.TestCase):
    def test_can_add_one_standard(self):
        test_input = {
            "suits": [
                {"cards": [{"cre": ["138-448"], "value": "2"}], "name": "Session management"},
            ]
        }
        standards = ["ASVS"]
        expected = {
            "meta": {"component": "mappings", "edition": "ecommerce", "language": "ALL", "version": "1.20"},
            "suits": [
                {"cards": [{"ASVS": "V2.3.3", "cre": ["138-448"], "value": "2"}], "name": "Session management"},
            ],
        }

        self.assertEqual(gm.produce_ecommerce_mappings(test_input, standards, "cre"), expected)

    @patch("requests.get")
    def test_produce_ecommerce_mappings(self, mock_requests_get):
        cornucopia_version = "1.20"
        source_file = {
            "suits": [
                {
                    "cards": [
                        {
                            "cre": ["cre1"],
                        }
                    ]
                }
            ]
        }
        standards_to_add = ["ASVS", "CAPEC", "SCP"]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "links": [
                    {"document": {"name": "ASVS", "sectionID": "123"}},
                    {"document": {"name": "CAPEC", "sectionID": "456"}},
                    {"document": {"name": "OTHER", "sectionID": "789"}},
                ]
            }
        }
        mock_requests_get.return_value = mock_response

        result = gm.produce_ecommerce_mappings(source_file, standards_to_add, "cre")

        expected_result = {
            "meta": {"edition": "ecommerce", "component": "mappings", "language": "ALL", "version": cornucopia_version},
            "suits": [{"cards": [{"cre": ["cre1"], "ASVS": "123", "CAPEC": "456"}]}],
        }

        # Assert that the necessary functions were called
        mock_requests_get.assert_called_with(gm.make_mapping_link("cre1", "cre"))

        # Assert the expected result
        self.assertEqual(result, expected_result)

    @patch("requests.get")
    def test_produce_ecommerce_mappings_cre_not_found(self, mock_requests_get):
        cornucopia_version = "1.20"
        source_file = {
            "suits": [
                {
                    "cards": [
                        {
                            "cre": ["cre1"],
                        }
                    ]
                }
            ]
        }
        standards_to_add = ["ASVS", "CAPEC", "SCP"]

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response

        result = gm.produce_ecommerce_mappings(source_file, standards_to_add, "cre")

        expected_result = {
            "meta": {"edition": "ecommerce", "component": "mappings", "language": "ALL", "version": cornucopia_version},
            "suits": [
                {
                    "cards": [
                        {
                            "cre": ["cre1"],
                        }
                    ]
                }
            ],
        }

        # Assert that the necessary functions were called
        mock_requests_get.assert_called_with(gm.make_mapping_link("cre1", "cre"))

        # Assert the expected result
        self.assertEqual(result, expected_result)

    def test_make_cre_link_capec(self):
        test_id = "cre1"

        result = gm.make_mapping_link(test_id, "CAPEC")

        expected_result = f"{gm.opencre_rest_url}/standard/CAPEC?sectionID={test_id}"

        # Assert the expected result
        self.assertEqual(result, expected_result)

    def test_make_cre_link_cre(self):
        test_id = "cre1"

        result = gm.make_mapping_link(test_id, "cre")

        expected_result = f"{gm.opencre_rest_url}/id/{test_id}"

        # Assert the expected result
        self.assertEqual(result, expected_result)


class MainTestCase(unittest.TestCase):
    # @patch("builtins.print")
    # @patch("builtins.open")
    # def test_main_with_staging(self, mock_open, mock_print):
    #     args = {"cres": "source/cre-mappings.yaml", "staging": True, "qr_images": None, "target": None}
    #     mock_file = mock_open.return_value.__enter__.return_value
    #     mock_file.read.return_value = "content"
    #
    #     with patch.object(argparse, "ArgumentParser") as mock_parser:
    #         mock_parser.return_value.parse_args.return_value = argparse.Namespace(**args)
    #         with patch.object(yaml, "safe_load") as mock_load:
    #             mock_load.return_value = {"key": "value"}
    #             gm.main()
    #             mock_print.assert_called_with("Using staging.opencre.org")
    #             mock_open.assert_called_with("source/cre-mappings.yaml")

    @patch("builtins.print")
    @patch("builtins.open")
    def test_main_without_staging(self, mock_open, mock_print):
        args = {"cre": "source/cre-mappings.yaml", "staging": False, "qr_images": None, "target": None}
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.read.return_value = "content"

        with patch.object(argparse, "ArgumentParser") as mock_parser:
            mock_parser.return_value.parse_args.return_value = argparse.Namespace(**args)
            with patch.object(yaml, "safe_load") as mock_load:
                mock_load.return_value = {"key": "value"}
                gm.main()
                mock_print.assert_not_called()
                mock_open.assert_called_with("source/cre-mappings.yaml")


if __name__ == "__main__":
    unittest.main()
