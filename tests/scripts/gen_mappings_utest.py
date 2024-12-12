import unittest
import qrcode
import argparse
import yaml
from unittest.mock import MagicMock, patch
from scripts import gen_mappings as gm

if "unittest.util" in __import__("sys").modules:
    # Show full diff in self.assertEqual.
    __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999


class TestMakeCreLink(unittest.TestCase):
    def test_make_cre_link_valid(self):
        self.assertEqual(gm.make_cre_link("123", frontend=True), f"{gm.opencre_base_url}/cre/123")
        self.assertEqual(gm.make_cre_link("123", frontend=False), f"{gm.opencre_rest_url}/id/123")

    def test_make_cre_link_empty(self):
        self.assertEqual(gm.make_cre_link("", frontend=True), f"{gm.opencre_base_url}/cre/")
        self.assertEqual(gm.make_cre_link("", frontend=False), f"{gm.opencre_rest_url}/id/")


class TestProduceWebappMappings(unittest.TestCase):
    @patch("security.safe_requests.get")
    def test_produce_webapp_mappings_valid(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"links": [{"document": {"name": "ASVS", "sectionID": "123-ASVS"}}]}}
        mock_get.return_value = mock_response

        source_file = {"suits": [{"cards": [{"cre": ["123"]}]}]}
        standards_to_add = ["ASVS"]

        result = gm.produce_webapp_mappings(source_file, standards_to_add)

        expected = {
            "meta": {
                "edition": "webapp",
                "component": "mappings",
                "language": "ALL",
                "version": "1.20",
            },
            "suits": [{"cards": [{"cre": ["123"], "ASVS": "123-ASVS"}]}],
        }
        self.assertEqual(result, expected)

    @patch("security.safe_requests.get")
    def test_produce_webapp_mappings_api_error(self, mock_get):
        mock_get.return_value = MagicMock(status_code=500)

        source_file = {"suits": [{"cards": [{"cre": ["123"]}]}]}
        standards_to_add = ["ASVS"]

        result = gm.produce_webapp_mappings(source_file, standards_to_add)

        expected = {
            "meta": {
                "edition": "webapp",
                "component": "mappings",
                "language": "ALL",
                "version": "1.20",
            },
            "suits": [{"cards": [{"cre": ["123"]}]}],
        }
        self.assertEqual(result, expected)

    def test_produce_webapp_mappings_empty_input(self):
        result = gm.produce_webapp_mappings({"suits": []}, ["ASVS"])
        expected = {
            "meta": {
                "edition": "webapp",
                "component": "mappings",
                "language": "ALL",
                "version": "1.20",
            },
            "suits": [],
        }
        self.assertEqual(result, expected)


class TestGenerateQrImages(unittest.TestCase):
    @patch("qrcode.make")
    @patch("builtins.open", new_callable=MagicMock)
    def test_generate_qr_images(self, mock_open, mock_qrcode):
        mock_img = MagicMock()
        mock_qrcode.return_value = mock_img

        existing_mappings = {"suits": [{"cards": [{"cre": ["123"]}]}]}
        gm.generate_qr_images(existing_mappings, "/path/to/directory")

        mock_qrcode.assert_called_once_with(f"{gm.opencre_base_url}/cre/123", image_factory=qrcode.image.svg.SvgImage)
        mock_open.assert_called_once_with("/path/to/directory/123", "wb")
        mock_img.save.assert_called()

    def test_generate_qr_images_invalid_mapping(self):
        with self.assertRaises(KeyError):
            gm.generate_qr_images({"invalid_key": []}, "/path/to/directory")


class TestMain(unittest.TestCase):
    @patch("builtins.open", new_callable=MagicMock)
    @patch("yaml.safe_load")
    @patch("yaml.safe_dump")
    @patch("scripts.gen_mappingsgit chec.produce_webapp_mappings")
    @patch("argparse.ArgumentParser.parse_args")
    def test_main_generate_mappings(self, mock_args, mock_produce, mock_dump, mock_load, mock_open):
        mock_args.return_value = argparse.Namespace(
            cres="test.yaml", target="output.yaml", staging=False, qr_images=None
        )
        mock_load.return_value = {"suits": []}

        gm.main()

        mock_load.assert_called_once()
        mock_produce.assert_called_once()
        mock_dump.assert_called_once()
        mock_open.assert_any_call("output.yaml", "w")

    @patch("builtins.print")
    @patch("argparse.ArgumentParser.parse_args")
    def test_main_missing_file(self, mock_args, mock_print):
        mock_args.return_value = argparse.Namespace(cres="nonexistent.yaml", target=None, staging=False, qr_images=None)

        with self.assertRaises(FileNotFoundError):
            gm.main()

        mock_print.assert_not_called()


@patch("builtins.open", new_callable=MagicMock)
@patch("yaml.safe_dump")
def test_main_with_target(self, mock_safe_dump, mock_open):
    args = {"cres": "source/cre-mappings.yaml", "staging": False, "qr_images": None, "target": "output.yaml"}
    mock_file = mock_open.return_value.__enter__.return_value
    mock_file.read.return_value = """
    suits:
      - name: "Test Suit"
        cards:
          - cre: ["cre1"]
            value: "Test Value"
    """

    with patch.object(argparse, "ArgumentParser") as mock_parser:
        mock_parser.return_value.parse_args.return_value = argparse.Namespace(**args)
        with patch.object(yaml, "safe_load") as mock_load:
            mock_load.return_value = {
                "suits": [{"name": "Test Suit", "cards": [{"cre": ["cre1"], "value": "Test Value"}]}]
            }
            gm.main()

            # Check that produce_webapp_mappings was called
            mock_safe_dump.assert_called_once()
            mock_open.assert_called_with("output.yaml", "w")


@patch("scripts.gen_mappings.generate_qr_images")
@patch("builtins.open", new_callable=MagicMock)
@patch("yaml.safe_load")
def test_main_with_qr_images(self, mock_safe_load, mock_open, mock_generate_qr_images):
    args = {"cres": "source/cre-mappings.yaml", "staging": False, "qr_images": "/path/to/qr_images", "target": None}
    mock_file = mock_open.return_value.__enter__.return_value
    mock_file.read.return_value = """
    suits:
      - name: "Test Suit"
        cards:
          - cre: ["cre1"]
            value: "Test Value"
    """
    mock_safe_load.return_value = {
        "suits": [{"name": "Test Suit", "cards": [{"cre": ["cre1"], "value": "Test Value"}]}]
    }

    with patch.object(argparse, "ArgumentParser") as mock_parser:
        mock_parser.return_value.parse_args.return_value = argparse.Namespace(**args)
        gm.main()

        # Check that generate_qr_images was called
        mock_generate_qr_images.assert_called_once_with(
            {"suits": [{"name": "Test Suit", "cards": [{"cre": ["cre1"], "value": "Test Value"}]}]},
            "/path/to/qr_images",
        )


@patch("builtins.open", new_callable=MagicMock)
@patch("builtins.print")
def test_main_without_target_or_qr_images(self, mock_print, mock_open):
    args = {"cres": "source/cre-mappings.yaml", "staging": False, "qr_images": None, "target": None}
    mock_file = mock_open.return_value.__enter__.return_value
    mock_file.read.return_value = """
    suits:
      - name: "Test Suit"
        cards:
          - cre: ["cre1"]
            value: "Test Value"
    """

    with patch.object(argparse, "ArgumentParser") as mock_parser:
        mock_parser.return_value.parse_args.return_value = argparse.Namespace(**args)
        with patch.object(yaml, "safe_load") as mock_load:
            mock_load.return_value = {
                "suits": [{"name": "Test Suit", "cards": [{"cre": ["cre1"], "value": "Test Value"}]}]
            }
            gm.main()

            # Ensure print was not called since no output is specified
            mock_print.assert_not_called()


class TestProduceWebappMappingsAdditional(unittest.TestCase):
    @patch("security.safe_requests.get")
    def test_empty_suits(self, mock_requests_get):
        source_file = {"suits": []}
        standards_to_add = ["ASVS"]

        result = gm.produce_webapp_mappings(source_file, standards_to_add)

        expected_result = {
            "meta": {"edition": "webapp", "component": "mappings", "language": "ALL", "version": gm.CORNUCOPIA_VERSION},
            "suits": [],
        }
        self.assertEqual(result, expected_result)

    @patch("security.safe_requests.get")
    def test_missing_links_in_response(self, mock_requests_get):
        source_file = {"suits": [{"cards": [{"cre": ["cre1"]}]}]}
        standards_to_add = ["ASVS"]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"links": []}}
        mock_requests_get.return_value = mock_response

        result = gm.produce_webapp_mappings(source_file, standards_to_add)

        expected_result = {
            "meta": {"edition": "webapp", "component": "mappings", "language": "ALL", "version": gm.CORNUCOPIA_VERSION},
            "suits": [{"cards": [{"cre": ["cre1"]}]}],
        }
        self.assertEqual(result, expected_result)


class TestGenerateQRImagesAdditional(unittest.TestCase):
    @patch("qrcode.make")
    def test_invalid_directory_path(self, mock_qrcode_make):
        existing_mappings = {"suits": [{"cards": [{"cre": ["cre1"]}]}]}
        directory_path = "/invalid/path/to/directory"

        with self.assertRaises(Exception):
            gm.generate_qr_images(existing_mappings, directory_path)


class TestMainAdditional(unittest.TestCase):
    @patch("builtins.open", side_effect=FileNotFoundError)
    @patch("builtins.print")
    def test_main_file_not_found(self, mock_print, mock_open):
        args = {"cres": "missing.yaml", "staging": False, "qr_images": None, "target": None}

        with patch.object(argparse, "ArgumentParser") as mock_parser:
            mock_parser.return_value.parse_args.return_value = argparse.Namespace(**args)
            with self.assertRaises(FileNotFoundError):
                gm.main()


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
