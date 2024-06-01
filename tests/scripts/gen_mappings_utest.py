import unittest
import qrcode
import argparse
import yaml
from unittest.mock import MagicMock, patch
from scripts import gen_mappings as gm

if "unittest.util" in __import__("sys").modules:
    # Show full diff in self.assertEqual.
    __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999


class TestGenerateQRImages(unittest.TestCase):
    @patch("scripts.gen_mappings.make_cre_link")
    @patch("qrcode.make")
    def test_generate_qr_images(self, mock_qrcode_make, mock_make_cre_link):
        existing_mappings = {"suits": [{"cards": [{"cre": ["cre1", "cre2"]}]}]}
        directory_path = "/path/to/directory"

        mock_make_cre_link.return_value = "https://example.com/cre1"

        # Mock the qrcode.make() function to return a MagicMock object
        mock_img = MagicMock()
        mock_qrcode_make.return_value = mock_img

        # Mock the 'open' function to return a MagicMock object
        mock_open = MagicMock()
        with patch("builtins.open", mock_open):
            gm.generate_qr_images(existing_mappings, directory_path)

        # Assert that the necessary functions were called
        mock_make_cre_link.assert_called_with("cre1", frontend=True)
        mock_qrcode_make.assert_called_with("https://example.com/cre1", image_factory=qrcode.image.svg.SvgImage)
        mock_open.assert_called_with("/path/to/directory/cre1", "wb")

        # Assert that the img.save() method was called on the MagicMock object
        mock_img.save.assert_called_with(mock_open().__enter__())


class TestProducewebappMappings(unittest.TestCase):
    def test_can_add_one_standard(self):
        test_input = {
            "suits": [
                {"cards": [{"cre": ["308-515"], "value": "2"}], "name": "Data validation & encoding"},
                {"cards": [{"cre": ["138-448"], "value": "2"}], "name": "Session management"},
            ]
        }
        standards = ["ASVS"]
        expected = {
            "meta": {"component": "mappings", "edition": "webapp", "language": "ALL", "version": "1.20"},
            "suits": [
                {"cards": [{"cre": ["308-515"], "value": "2"}], "name": "Data validation & encoding"},
                {"cards": [{"ASVS": "V2.3.3", "cre": ["138-448"], "value": "2"}], "name": "Session management"},
            ],
        }

        self.assertEqual(gm.produce_webapp_mappings(test_input, standards), expected)

    @patch("security.safe_requests.get")
    def test_produce_webapp_mappings(self, mock_requests_get):
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

        result = gm.produce_webapp_mappings(source_file, standards_to_add)

        expected_result = {
            "meta": {"edition": "webapp", "component": "mappings", "language": "ALL", "version": cornucopia_version},
            "suits": [{"cards": [{"cre": ["cre1"], "ASVS": "123", "CAPEC": "456"}]}],
        }

        # Assert that the necessary functions were called
        mock_requests_get.assert_called_with(gm.make_cre_link("cre1"), timeout=60)

        # Assert the expected result
        self.assertEqual(result, expected_result)

    @patch("security.safe_requests.get")
    def test_produce_webapp_mappings_cre_not_found(self, mock_requests_get):
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

        result = gm.produce_webapp_mappings(source_file, standards_to_add)

        expected_result = {
            "meta": {"edition": "webapp", "component": "mappings", "language": "ALL", "version": cornucopia_version},
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
        mock_requests_get.assert_called_with(gm.make_cre_link("cre1"), timeout=60)

        # Assert the expected result
        self.assertEqual(result, expected_result)

    def test_make_cre_link_frontend(self):
        test_id = "cre1"
        frontend = True

        result = gm.make_cre_link(test_id, frontend)

        expected_result = f"{gm.opencre_base_url}/cre/{test_id}"

        # Assert the expected result
        self.assertEqual(result, expected_result)

    def test_make_cre_link_rest(self):
        test_id = "cre1"
        frontend = False

        result = gm.make_cre_link(test_id, frontend)

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
        args = {"cres": "source/cre-mappings.yaml", "staging": False, "qr_images": None, "target": None}
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
