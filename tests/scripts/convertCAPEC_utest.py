#!/usr/bin/env python3
import unittest
from unittest.mock import patch, mock_open, MagicMock
import argparse
import json
import logging
from pathlib import Path

import scripts.convertCAPEC as capec

capec.convert_vars = capec.ConvertVars()


if "unittest.util" in __import__("sys").modules:
    # Show full diff in self.assertEqual.
    __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999


class TestParseDescription(unittest.TestCase):
    def test_parse_description_with_dict_and_text(self):
        """Test parsing description with __text field in dict"""
        description = {"Description": {"p": {"__text": "This is a test description"}}}
        result = capec.parse_description(description)
        self.assertEqual(result, "This is a test description")

    def test_parse_description_with_list_of_paragraphs(self):
        """Test parsing description with list of paragraphs"""
        description = {
            "Description": {
                "p": [{"__text": "First paragraph"}, {"__text": "Second paragraph"}, {"__text": "Third paragraph"}]
            }
        }
        result = capec.parse_description(description)
        self.assertEqual(result, "First paragraph Second paragraph Third paragraph")

    def test_parse_description_with_mixed_list(self):
        """Test parsing description with mixed list content"""
        description = {
            "Description": {"p": [{"__text": "First paragraph"}, "Plain string", {"__text": "Third paragraph"}]}
        }
        result = capec.parse_description(description)
        self.assertEqual(result, "First paragraph Plain string Third paragraph")

    def test_parse_description_simple_string(self):
        """Test parsing simple string description"""
        description = "Simple description text"
        result = capec.parse_description(description)
        self.assertEqual(result, "Simple description text")

    def test_parse_description_empty_dict(self):
        """Test parsing empty dict"""
        description = {}
        result = capec.parse_description(description)
        self.assertEqual(result, "{}")

    def test_parse_description_none_value(self):
        """Test parsing None value"""
        description = None
        result = capec.parse_description(description)
        self.assertEqual(result, "None")


class TestValidateJsonData(unittest.TestCase):
    def test_validate_json_data_valid(self):
        """Test validation with valid data structure"""
        data = {
            "Attack_Pattern_Catalog": {"Attack_Patterns": {"Attack_Pattern": [{"_ID": "1", "_Name": "Test Pattern"}]}}
        }
        result = capec.validate_json_data(data)
        self.assertTrue(result)

    def test_validate_json_data_no_data(self):
        """Test validation with no data"""
        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            result = capec.validate_json_data(None)
        self.assertFalse(result)
        self.assertIn("No data provided", log.output[0])

    def test_validate_json_data_missing_catalog(self):
        """Test validation missing Attack_Pattern_Catalog"""
        data = {"some_other_key": {}}
        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            result = capec.validate_json_data(data)
        self.assertFalse(result)
        self.assertIn("Missing 'Attack_Pattern_Catalog' key", log.output[0])

    def test_validate_json_data_catalog_not_dict(self):
        """Test validation when Attack_Pattern_Catalog is not a dict"""
        data = {"Attack_Pattern_Catalog": "not a dict"}
        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            result = capec.validate_json_data(data)
        self.assertFalse(result)
        self.assertIn("'Attack_Pattern_Catalog' is not a dictionary", log.output[0])

    def test_validate_json_data_missing_attack_patterns(self):
        """Test validation missing Attack_Patterns"""
        data = {"Attack_Pattern_Catalog": {"some_other_key": {}}}
        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            result = capec.validate_json_data(data)
        self.assertFalse(result)
        self.assertIn("Missing 'Attack_Patterns' key", log.output[0])

    def test_validate_json_data_attack_patterns_not_dict(self):
        """Test validation when Attack_Patterns is not a dict"""
        data = {"Attack_Pattern_Catalog": {"Attack_Patterns": "not a dict"}}
        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            result = capec.validate_json_data(data)
        self.assertFalse(result)
        self.assertIn("'Attack_Patterns' is not a dictionary", log.output[0])

    def test_validate_json_data_missing_attack_pattern(self):
        """Test validation missing Attack_Pattern"""
        data = {"Attack_Pattern_Catalog": {"Attack_Patterns": {"some_other_key": []}}}
        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            result = capec.validate_json_data(data)
        self.assertFalse(result)
        self.assertIn("Missing 'Attack_Pattern' key", log.output[0])

    def test_validate_json_data_attack_pattern_not_list(self):
        """Test validation when Attack_Pattern is not a list"""
        data = {"Attack_Pattern_Catalog": {"Attack_Patterns": {"Attack_Pattern": "not a list"}}}
        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            result = capec.validate_json_data(data)
        self.assertFalse(result)
        self.assertIn("'Attack_Pattern' is not a list", log.output[0])


class TestLoadJsonFile(unittest.TestCase):
    def test_load_json_file_valid(self):
        """Test loading valid JSON file"""
        test_data = {"test": "data"}
        mock_file = mock_open(read_data=json.dumps(test_data))

        with patch("builtins.open", mock_file):
            with patch("json.load", return_value=test_data):
                result = capec.load_json_file(Path("/test/file.json"))

        self.assertEqual(result, test_data)

    def test_load_json_file_not_found(self):
        """Test loading non-existent file"""
        with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
            with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
                result = capec.load_json_file(Path("/nonexistent/file.json"))

        self.assertEqual(result, {})
        self.assertIn("Error while loading JSON file", log.output[0])

    def test_load_json_file_invalid_json(self):
        """Test loading invalid JSON file"""
        mock_file = mock_open(read_data="invalid json content {")

        with patch("builtins.open", mock_file):
            with patch("json.load", side_effect=json.JSONDecodeError("Invalid", "doc", 0)):
                with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
                    result = capec.load_json_file(Path("/test/file.json"))

        self.assertEqual(result, {})
        self.assertIn("Error while loading JSON file", log.output[0])


class TestParseArguments(unittest.TestCase):
    def test_parse_arguments_defaults(self):
        """Test parsing arguments with defaults"""
        args = capec.parse_arguments([])
        self.assertEqual(args.output_path, capec.ConvertVars.DEFAULT_OUTPUT_PATH)
        self.assertEqual(args.input_path, capec.ConvertVars.DEFAULT_INPUT_PATH)
        self.assertFalse(args.debug)

    def test_parse_arguments_custom_output(self):
        """Test parsing arguments with custom output path"""
        args = capec.parse_arguments(["-o", "custom/output"])
        self.assertEqual(args.output_path, "custom/output")

    def test_parse_arguments_custom_input(self):
        """Test parsing arguments with custom input path"""
        args = capec.parse_arguments(["-i", "custom/input.json"])
        self.assertEqual(args.input_path, "custom/input.json")

    def test_parse_arguments_debug_flag(self):
        """Test parsing arguments with debug flag"""
        args = capec.parse_arguments(["-d"])
        self.assertTrue(args.debug)

    def test_parse_arguments_all_options(self):
        """Test parsing arguments with all options"""
        args = capec.parse_arguments(["-o", "custom/output", "-i", "custom/input.json", "-d"])
        self.assertEqual(args.output_path, "custom/output")
        self.assertEqual(args.input_path, "custom/input.json")
        self.assertTrue(args.debug)


class TestCreateFolder(unittest.TestCase):
    @patch("os.makedirs")
    def test_create_folder_new(self, mock_makedirs):
        """Test creating a new folder"""
        test_path = Path("/test/folder")
        capec.create_folder(test_path)
        mock_makedirs.assert_called_once_with(test_path, exist_ok=True)

    @patch("os.makedirs")
    def test_create_folder_exists(self, mock_makedirs):
        """Test creating a folder that already exists"""
        test_path = Path("/existing/folder")
        capec.create_folder(test_path)
        mock_makedirs.assert_called_once_with(test_path, exist_ok=True)

    @patch("os.makedirs")
    def test_create_folder_nested(self, mock_makedirs):
        """Test creating nested folders"""
        test_path = Path("/level1/level2/level3")
        capec.create_folder(test_path)
        mock_makedirs.assert_called_once_with(test_path, exist_ok=True)

    @patch("os.makedirs")
    def test_create_folder_error(self, mock_makedirs):
        """Test error handling when creating folder fails"""
        test_path = Path("/test/folder")
        mock_makedirs.side_effect = OSError("Permission denied")

        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            capec.create_folder(test_path)

        self.assertIn("Error while creating folder", log.output[0])


class TestEmptyFolder(unittest.TestCase):
    @patch("shutil.rmtree")
    def test_empty_folder_with_files(self, mock_rmtree):
        """Test emptying a folder with files"""
        test_path = Path("/test/folder")
        capec.empty_folder(test_path)
        mock_rmtree.assert_called_once_with(test_path)

    @patch("shutil.rmtree")
    def test_empty_folder_with_subfolders(self, mock_rmtree):
        """Test emptying a folder with subfolders"""
        test_path = Path("/test/folder")
        capec.empty_folder(test_path)
        mock_rmtree.assert_called_once_with(test_path)

    @patch("shutil.rmtree")
    def test_empty_folder_nonexistent(self, mock_rmtree):
        """Test emptying a non-existent folder"""
        test_path = Path("/nonexistent/folder")
        mock_rmtree.side_effect = FileNotFoundError("Folder not found")

        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            capec.empty_folder(test_path)

        self.assertIn("Error while emptying folder", log.output[0])

    @patch("shutil.rmtree")
    def test_empty_folder_permission_error(self, mock_rmtree):
        """Test emptying a folder with permission error"""
        test_path = Path("/test/folder")
        mock_rmtree.side_effect = PermissionError("Permission denied")

        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            capec.empty_folder(test_path)

        self.assertIn("Error while emptying folder", log.output[0])


class TestCreateCAPECPages(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    @patch("scripts.convertCAPEC.create_folder")
    def test_create_capec_pages_single_pattern(self, mock_create_folder, mock_file):
        """Test creating CAPEC pages for a single attack pattern"""
        # Setup
        test_output_path = Path("/test/output")
        capec.convert_vars.args = argparse.Namespace(
            output_path=test_output_path, input_path=Path("dummy.json"), debug=False
        )

        test_data = {
            "Attack_Pattern_Catalog": {
                "Attack_Patterns": {
                    "Attack_Pattern": [
                        {"_ID": "123", "_Name": "Test Attack Pattern", "Description": "This is a test description"}
                    ]
                }
            }
        }

        with patch.object(Path, "parent") as mock_parent:
            mock_parent.resolve.return_value = Path("/mock/directory")
            capec.createCAPECPages(test_data)

        # Verify create_folder was called
        mock_create_folder.assert_called()

        # Verify file was opened for writing
        mock_file.assert_called()

        # Get the written content
        handle = mock_file()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)

        # Verify content
        self.assertIn("CAPEC-123: Test Attack Pattern", written_content)
        self.assertIn("## Description", written_content)
        self.assertIn("This is a test description", written_content)
        self.assertIn("Source: [CAPEC-123](https://capec.mitre.org/data/definitions/123.html)", written_content)

    @patch("builtins.open", new_callable=mock_open)
    @patch("scripts.convertCAPEC.create_folder")
    def test_create_capec_pages_multiple_patterns(self, mock_create_folder, mock_file):
        """Test creating CAPEC pages for multiple attack patterns"""
        # Setup
        test_output_path = Path("/test/output")
        capec.convert_vars.args = argparse.Namespace(
            output_path=test_output_path, input_path=Path("dummy.json"), debug=False
        )

        test_data = {
            "Attack_Pattern_Catalog": {
                "Attack_Patterns": {
                    "Attack_Pattern": [
                        {"_ID": "1", "_Name": "First Pattern", "Description": "First description"},
                        {"_ID": "2", "_Name": "Second Pattern", "Description": "Second description"},
                    ]
                }
            }
        }

        with patch.object(Path, "parent") as mock_parent:
            mock_parent.resolve.return_value = Path("/mock/directory")
            capec.createCAPECPages(test_data)

        # Verify create_folder was called twice (once for each pattern)
        self.assertEqual(mock_create_folder.call_count, 2)

        # Verify file was opened twice
        self.assertEqual(mock_file.call_count, 2)

    @patch("builtins.open", new_callable=mock_open)
    @patch("scripts.convertCAPEC.create_folder")
    def test_create_capec_pages_complex_description(self, mock_create_folder, mock_file):
        """Test creating CAPEC pages with complex description format"""
        # Setup
        test_output_path = Path("/test/output")
        capec.convert_vars.args = argparse.Namespace(
            output_path=test_output_path, input_path=Path("dummy.json"), debug=False
        )

        test_data = {
            "Attack_Pattern_Catalog": {
                "Attack_Patterns": {
                    "Attack_Pattern": [
                        {
                            "_ID": "456",
                            "_Name": "Complex Pattern",
                            "Description": {"Description": {"p": {"__text": "Complex description text"}}},
                        }
                    ]
                }
            }
        }

        with patch.object(Path, "parent") as mock_parent:
            mock_parent.resolve.return_value = Path("/mock/directory")
            capec.createCAPECPages(test_data)

        # Get the written content
        handle = mock_file()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)

        # Verify complex description was parsed
        self.assertIn("Complex description text", written_content)


class TestSetLogging(unittest.TestCase):
    @patch("logging.basicConfig")
    @patch("logging.getLogger")
    def test_set_logging_debug(self, mock_get_logger, mock_basic_config):
        """Test setting logging to debug level"""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        capec.convert_vars.args = argparse.Namespace(debug=True)
        capec.set_logging()

        mock_basic_config.assert_called_once()
        mock_logger.setLevel.assert_called_with(logging.DEBUG)

    @patch("logging.basicConfig")
    @patch("logging.getLogger")
    def test_set_logging_info(self, mock_get_logger, mock_basic_config):
        """Test setting logging to info level"""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        capec.convert_vars.args = argparse.Namespace(debug=False)
        capec.set_logging()

        mock_basic_config.assert_called_once()
        mock_logger.setLevel.assert_called_with(logging.INFO)


if __name__ == "__main__":
    unittest.main()
