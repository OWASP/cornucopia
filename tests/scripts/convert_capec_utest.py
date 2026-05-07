#!/usr/bin/env python3
import unittest
from unittest.mock import patch, mock_open, MagicMock
import argparse
import json
import logging
from pathlib import Path
import yaml

import scripts.convert_capec as capec

capec.convert_vars = capec.ConvertVars()


if "unittest.util" in __import__("sys").modules:
    # Show full diff in self.assertEqual.
    __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999


class TestFileHandleClosure(unittest.TestCase):
    """Ensure CAPEC page generators close file handles on errors"""

    def setUp(self):
        self.mock_output_path = Path("/fake/output")
        capec.convert_vars.args = argparse.Namespace(output_path=self.mock_output_path)

    @patch("builtins.open", new_callable=mock_open)
    @patch("scripts.convert_capec.create_folder")
    def test_create_capec_pages_close_on_error(self, mock_create_folder, mock_file):
        handle = mock_file()
        # first write succeeds, second write throws
        handle.write.side_effect = [None, ValueError("oops")]

        # Minimal data causing one pattern entry
        test_data = {
            "Attack_Pattern_Catalog": {
                "Attack_Patterns": {"Attack_Pattern": [{"_ID": "1", "_Name": "foo", "Description": "bar"}]},
                "Categories": {"Category": []},
            }
        }
        capec_to_asvs_map = {}
        asvs_map = {"Requirements": []}
        with self.assertRaises(ValueError):
            capec.create_capec_pages(test_data, capec_to_asvs_map, asvs_map, "5.0")

        self.assertTrue(handle.close.called)


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
            "Attack_Pattern_Catalog": {
                "Attack_Patterns": {"Attack_Pattern": [{"_ID": "1", "_Name": "Test Pattern"}]},
                "Categories": {
                    "Category": [
                        {
                            "_ID": "152",
                            "_Name": "Inject Unexpected Items",
                            "Summary": "Attack patterns within this category focus on the ability to control or "
                            "disrupt the behavior of a target either through crafted data submitted via an interface"
                            " for data input, or the installation and execution of malicious code on the target"
                            " system. The former happens when an adversary adds material to their input that is"
                            " interpreted by the application causing the targeted application to perform steps"
                            " unintended by the application manager or causing the application to enter an "
                            "unstable state. Attacks of this type differ from Data Structure Attacks in that the"
                            " latter attacks subvert the underlying structures that hold user-provided data, either"
                            " pre-empting interpretation of the input (in the case of Buffer Overflows) or resulting"
                            " in values that the targeted application is unable to handle correctly (in the case of "
                            "Integer Overflows). In Injection attacks, the input is interpreted by the application, "
                            "but the attacker has included instructions to the interpreting functions that the target"
                            " application then follows.",
                        }
                    ]
                },
            }
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
        args = capec.parse_arguments(
            [
                "-o",
                "custom/output",
                "-i",
                "custom/input.json",
                "-am",
                "custom/asvs.json",
                "-ca",
                "custom/capec.yaml",
                "-av",
                "5.0",
                "-d",
            ]
        )
        self.assertEqual(args.output_path, "custom/output")
        self.assertEqual(args.input_path, "custom/input.json")
        self.assertEqual(args.asvs_mapping, "custom/asvs.json")
        self.assertEqual(args.capec_to_asvs, "custom/capec.yaml")
        self.assertEqual(args.asvs_version, "5.0")
        self.assertTrue(args.debug)

    @patch("argparse.ArgumentParser.parse_args")
    @patch("scripts.convert_capec.sys.exit", side_effect=SystemExit)
    def test_parse_arguments_handles_argument_error(self, mock_exit, mock_parse_args):
        """Test parser error branch logs and exits."""
        mock_parse_args.side_effect = argparse.ArgumentError(None, "bad argument")

        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            with self.assertRaises(SystemExit):
                capec.parse_arguments([])

        self.assertIn("bad argument", " ".join(log.output))
        mock_exit.assert_called_once()


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


class TestCreateCapecPages(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    @patch("scripts.convert_capec.create_folder")
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
                },
                "Categories": {
                    "Category": [
                        {
                            "_ID": "152",
                            "_Name": "Inject Unexpected Items",
                            "Summary": "Attack patterns within this category focus on the ability to control or "
                            "disrupt the behavior of a target either through crafted data submitted via an interface"
                            " for data input, or the installation and execution of malicious code on the target"
                            " system. The former happens when an adversary adds material to their input that is"
                            " interpreted by the application causing the targeted application to perform steps"
                            " unintended by the application manager or causing the application to enter an "
                            "unstable state. Attacks of this type differ from Data Structure Attacks in that the"
                            " latter attacks subvert the underlying structures that hold user-provided data, either"
                            " pre-empting interpretation of the input (in the case of Buffer Overflows) or resulting"
                            " in values that the targeted application is unable to handle correctly (in the case of "
                            "Integer Overflows). In Injection attacks, the input is interpreted by the application, "
                            "but the attacker has included instructions to the interpreting functions that the target"
                            " application then follows.",
                        }
                    ]
                },
            }
        }

        test_asvs_map = {"Requirements": []}
        test_capec_to_asvs_map = {}

        with patch.object(Path, "parent") as mock_parent:
            mock_parent.resolve.return_value = Path("/mock/directory")
            capec.create_capec_pages(test_data, test_capec_to_asvs_map, test_asvs_map, "5.0")

        # Verify create_folder was called
        mock_create_folder.assert_called()

        # Verify file was opened for writing
        mock_file.assert_called()

        # Get the written content
        handle = mock_file()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)

        # Verify content
        self.assertIn("CAPEC™ 123: Test Attack Pattern", written_content)
        self.assertIn("## Description", written_content)
        self.assertIn("This is a test description", written_content)
        self.assertIn("Source: [CAPEC™ 123](https://capec.mitre.org/data/definitions/123.html)", written_content)
        # ensure file closed
        self.assertTrue(handle.close.called)

    @patch("builtins.open", new_callable=mock_open)
    @patch("scripts.convert_capec.create_folder")
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
                },
                "Categories": {
                    "Category": [
                        {
                            "_ID": "152",
                            "_Name": "Inject Unexpected Items",
                            "Summary": "Attack patterns within this category focus on the ability to control or "
                            "disrupt the behavior of a target either through crafted data submitted via an interface"
                            " for data input, or the installation and execution of malicious code on the target"
                            " system. The former happens when an adversary adds material to their input that is"
                            " interpreted by the application causing the targeted application to perform steps"
                            " unintended by the application manager or causing the application to enter an "
                            "unstable state. Attacks of this type differ from Data Structure Attacks in that the"
                            " latter attacks subvert the underlying structures that hold user-provided data, either"
                            " pre-empting interpretation of the input (in the case of Buffer Overflows) or resulting"
                            " in values that the targeted application is unable to handle correctly (in the case of "
                            "Integer Overflows). In Injection attacks, the input is interpreted by the application, "
                            "but the attacker has included instructions to the interpreting functions that the target"
                            " application then follows.",
                        }
                    ]
                },
            }
        }

        test_asvs_map = {"Requirements": []}
        test_capec_to_asvs_map = {}

        with patch.object(Path, "parent") as mock_parent:
            mock_parent.resolve.return_value = Path("/mock/directory")
            capec.create_capec_pages(test_data, test_capec_to_asvs_map, test_asvs_map, "5.0")

        # Verify create_folder was called twice (once for each pattern)
        self.assertEqual(mock_create_folder.call_count, 3)

        # Verify file was opened twice
        self.assertEqual(mock_file.call_count, 3)

    @patch("builtins.open", new_callable=mock_open)
    @patch("scripts.convert_capec.create_folder")
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
                },
                "Categories": {
                    "Category": [
                        {
                            "_ID": "152",
                            "_Name": "Inject Unexpected Items",
                            "Summary": "Attack patterns within this category focus on the ability to control or "
                            "disrupt the behavior of a target either through crafted data submitted via an interface"
                            " for data input, or the installation and execution of malicious code on the target"
                            " system. The former happens when an adversary adds material to their input that is"
                            " interpreted by the application causing the targeted application to perform steps"
                            " unintended by the application manager or causing the application to enter an "
                            "unstable state. Attacks of this type differ from Data Structure Attacks in that the"
                            " latter attacks subvert the underlying structures that hold user-provided data, either"
                            " pre-empting interpretation of the input (in the case of Buffer Overflows) or resulting"
                            " in values that the targeted application is unable to handle correctly (in the case of "
                            "Integer Overflows). In Injection attacks, the input is interpreted by the application, "
                            "but the attacker has included instructions to the interpreting functions that the target"
                            " application then follows.",
                        }
                    ]
                },
            }
        }

        test_asvs_map = {"Requirements": []}
        test_capec_to_asvs_map = {}

        with patch.object(Path, "parent") as mock_parent:
            mock_parent.resolve.return_value = Path("/mock/directory")
            capec.create_capec_pages(test_data, test_capec_to_asvs_map, test_asvs_map, "5.0")

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


class TestGetValidVersion(unittest.TestCase):
    def test_get_valid_version_valid(self):
        """Test get_valid_version with valid version"""
        result = capec.get_valid_version("5.0")
        self.assertEqual(result, "5.0")

    def test_get_valid_version_invalid(self):
        """Test get_valid_version with invalid version returns latest"""
        latest = capec.ConvertVars.LATEST_ASVS_VERSION_CHOICES[-1]
        result = capec.get_valid_version("invalid")
        self.assertEqual(result, latest)

    def test_get_valid_version_old_version(self):
        """Test get_valid_version with old version returns latest"""
        latest = capec.ConvertVars.LATEST_ASVS_VERSION_CHOICES[-1]
        result = capec.get_valid_version("4.0")
        self.assertEqual(result, latest)


class TestLoadCapecToAsvsMapping(unittest.TestCase):
    @patch("yaml.safe_load")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_capec_to_asvs_mapping_valid(self, mock_file, mock_yaml_load):
        """Test loading valid CAPEC to ASVS mapping"""
        test_data = {1: {"owasp_asvs": ["V8.1.1", "V8.2.1"]}, 5: {"owasp_asvs": ["V1.2.9"]}}
        mock_yaml_load.return_value = test_data

        result = capec.load_capec_to_asvs_mapping(Path("test.yaml"))

        self.assertIsInstance(result, dict)
        self.assertIn(1, result)
        self.assertIn(5, result)
        self.assertEqual(result[1]["owasp_asvs"], ["V8.1.1", "V8.2.1"])
        self.assertEqual(result[5]["owasp_asvs"], ["V1.2.9"])

    def test_load_capec_to_asvs_mapping_file_not_found(self):
        """Test loading non-existent CAPEC to ASVS mapping"""
        with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
            with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
                result = capec.load_capec_to_asvs_mapping(Path("nonexistent.yaml"))

        self.assertEqual(result, {})
        self.assertIn("Error loading YAML file", log.output[0])

    @patch("yaml.safe_load")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_capec_to_asvs_mapping_invalid_yaml(self, mock_file, mock_yaml_load):
        """Test loading invalid YAML file"""
        mock_yaml_load.side_effect = yaml.YAMLError("Invalid YAML")

        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            result = capec.load_capec_to_asvs_mapping(Path("invalid.yaml"))

        self.assertEqual(result, {})
        self.assertIn("Error loading YAML file", log.output[0])


class TestCreateLinkList(unittest.TestCase):
    def test_create_link_list_with_requirements(self):
        """Test creating link list with ASVS requirements"""
        requirements = {"owasp_asvs": ["V8.1.1", "V8.2.1"]}
        asvs_map = {
            "Requirements": [
                {
                    "Ordinal": 8,
                    "Name": "Authorization",
                    "Items": [
                        {
                            "Ordinal": 1,
                            "Name": "General Authorization Design",
                            "Items": [{"Shortcode": "V8.1.1", "Text": "Test"}],
                        },
                        {"Ordinal": 2, "Name": "Operation Level", "Items": [{"Shortcode": "V8.2.1", "Text": "Test"}]},
                    ],
                }
            ]
        }

        result = capec.create_link_list(requirements, asvs_map, "5.0")

        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        self.assertIn("[", result)
        self.assertIn("]", result)
        self.assertIn("/taxonomy/asvs-5.0/", result)
        self.assertIn("V8.1.1", result)
        self.assertIn(", ", result)  # Should have comma separator

    def test_create_link_list_empty(self):
        """Test creating link list with no requirements"""
        requirements = {}
        asvs_map = {"Requirements": []}

        result = capec.create_link_list(requirements, asvs_map, "5.0")

        self.assertEqual(result, "")

    def test_create_link_list_empty_owasp_asvs(self):
        """Test creating link list with empty owasp_asvs list"""
        requirements = {"owasp_asvs": []}
        asvs_map = {"Requirements": []}

        result = capec.create_link_list(requirements, asvs_map, "5.0")

        self.assertEqual(result, "")


class TestCreatelink(unittest.TestCase):
    def test_createlink_found(self):
        """Test creating link for found shortcode"""
        asvs_map = {
            "Requirements": [
                {
                    "Ordinal": 8,
                    "Name": "Authorization",
                    "Items": [
                        {
                            "Ordinal": 1,
                            "Name": "General Authorization Design",
                            "Items": [{"Shortcode": "V8.1.1", "Text": "Test requirement"}],
                        }
                    ],
                }
            ]
        }

        result = capec.createlink(asvs_map, "V8.1.1", "5.0")

        self.assertIn("V8.1.1", result)
        self.assertIn("/taxonomy/asvs-5.0/", result)
        self.assertIn("08-authorization", result)
        self.assertIn("01-general-authorization-design", result)

    def test_createlink_not_found(self):
        """Test creating link for not found shortcode"""
        asvs_map = {"Requirements": []}

        result = capec.createlink(asvs_map, "V99.99.99", "5.0")

        # Should return the shortcode itself
        self.assertEqual(result, "V99.99.99")

    def test_createlink_no_prefix_collision(self):
        """Exact equality check: V1.1.1 must not match V1.1.10 or V1.1.11."""
        asvs_map = {
            "Requirements": [
                {
                    "Ordinal": 1,
                    "Name": "Architecture",
                    "Items": [
                        {
                            "Ordinal": 1,
                            "Name": "Secure Design",
                            "Items": [
                                {"Shortcode": "V1.1.10", "Text": "Req ten"},
                                {"Shortcode": "V1.1.11", "Text": "Req eleven"},
                                {"Shortcode": "V1.1.1", "Text": "Req one"},
                            ],
                        }
                    ],
                }
            ]
        }

        # Looking up the shorter code must return a link anchored to V1.1.1, not V1.1.10
        result = capec.createlink(asvs_map, "V1.1.1", "5.0")

        self.assertIn("#V1.1.1)", result)
        self.assertNotIn("#V1.1.10)", result)
        self.assertNotIn("#V1.1.11)", result)

    def test_createlink_exact_match_multi_digit(self):
        """Looking up V1.1.10 must match V1.1.10 exactly, not V1.1.1."""
        asvs_map = {
            "Requirements": [
                {
                    "Ordinal": 1,
                    "Name": "Architecture",
                    "Items": [
                        {
                            "Ordinal": 1,
                            "Name": "Secure Design",
                            "Items": [
                                {"Shortcode": "V1.1.1", "Text": "Req one"},
                                {"Shortcode": "V1.1.10", "Text": "Req ten"},
                            ],
                        }
                    ],
                }
            ]
        }

        result = capec.createlink(asvs_map, "V1.1.10", "5.0")

        self.assertIn("#V1.1.10)", result)
        self.assertNotIn("#V1.1.1)", result.replace("#V1.1.10)", ""))

    def test_createlink_empty_shortcode(self):
        """Empty shortcode returns empty string."""
        asvs_map = {"Requirements": []}

        result = capec.createlink(asvs_map, "", "5.0")

        self.assertEqual(result, "")


class TestHasNoAsvsMapping(unittest.TestCase):
    def test_has_no_asvs_mapping_exists(self):
        """Test checking ASVS mapping when it exists"""
        capec_to_asvs_map = {1: {"owasp_asvs": ["V8.1.1", "V8.2.1"]}}

        result = capec.has_no_asvs_mapping(1, capec_to_asvs_map)

        self.assertFalse(result)

    def test_has_no_asvs_mapping_not_exists(self):
        """Test checking ASVS mapping when it doesn't exist"""
        capec_to_asvs_map = {}

        result = capec.has_no_asvs_mapping(999, capec_to_asvs_map)

        self.assertTrue(result)

    def test_has_no_asvs_mapping_empty_list(self):
        """Test checking ASVS mapping when list is empty"""
        capec_to_asvs_map = {1: {"owasp_asvs": []}}

        result = capec.has_no_asvs_mapping(1, capec_to_asvs_map)

        self.assertTrue(result)


class TestCapecPagesWithAsvsMapping(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    @patch("scripts.convert_capec.create_folder")
    def test_create_capec_pages_with_asvs_mapping(self, mock_create_folder, mock_file):
        """Test creating CAPEC pages with ASVS mappings"""
        test_output_path = Path("/test/output")
        capec.convert_vars.args = argparse.Namespace(
            output_path=test_output_path, input_path=Path("dummy.json"), debug=False
        )

        test_data = {
            "Attack_Pattern_Catalog": {
                "Attack_Patterns": {
                    "Attack_Pattern": [{"_ID": "1", "_Name": "Test Pattern", "Description": "Test description"}]
                },
                "Categories": {
                    "Category": [
                        {
                            "_ID": "152",
                            "_Name": "Inject Unexpected Items",
                            "Summary": "Attack patterns within this category focus on the ability to control or "
                            "disrupt the behavior of a target either through crafted data submitted via an interface"
                            " for data input, or the installation and execution of malicious code on the target"
                            " system. The former happens when an adversary adds material to their input that is"
                            " interpreted by the application causing the targeted application to perform steps"
                            " unintended by the application manager or causing the application to enter an "
                            "unstable state. Attacks of this type differ from Data Structure Attacks in that the"
                            " latter attacks subvert the underlying structures that hold user-provided data, either"
                            " pre-empting interpretation of the input (in the case of Buffer Overflows) or resulting"
                            " in values that the targeted application is unable to handle correctly (in the case of "
                            "Integer Overflows). In Injection attacks, the input is interpreted by the application, "
                            "but the attacker has included instructions to the interpreting functions that the target"
                            " application then follows.",
                        }
                    ]
                },
            }
        }

        test_capec_to_asvs_map = {
            1: {"owasp_asvs": ["V8.1.1", "V8.2.1"]},
            152: {"owasp_asvs": ["V8.1.1"]},
        }

        test_asvs_map = {
            "Requirements": [
                {
                    "Ordinal": 8,
                    "Name": "Authorization",
                    "Items": [
                        {"Ordinal": 1, "Name": "General Design", "Items": [{"Shortcode": "V8.1.1"}]},
                        {"Ordinal": 2, "Name": "Operation Level", "Items": [{"Shortcode": "V8.2.1"}]},
                    ],
                }
            ]
        }

        with patch.object(Path, "parent") as mock_parent:
            mock_parent.resolve.return_value = Path("/mock/directory")
            capec.create_capec_pages(test_data, test_capec_to_asvs_map, test_asvs_map, "5.0")

        handle = mock_file()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)

        # Verify ASVS section is included
        self.assertIn("## Related ASVS Requirements", written_content)
        self.assertIn("ASVS (5.0):", written_content)
        self.assertIn("V8.1.1", written_content)


class TestMainFlow(unittest.TestCase):
    def _base_args(self) -> argparse.Namespace:
        return argparse.Namespace(
            output_path=Path("/tmp/out"),
            input_path=Path("/tmp/in.json"),
            asvs_mapping=Path("/tmp/asvs.json"),
            capec_to_asvs=Path("/tmp/capec.yaml"),
            asvs_version="5.0",
            debug=False,
        )

    @patch("scripts.convert_capec.create_capec_pages")
    @patch("scripts.convert_capec.load_capec_to_asvs_mapping", return_value={1: {"owasp_asvs": ["V8.1.1"]}})
    @patch("scripts.convert_capec.validate_json_data", return_value=True)
    @patch(
        "scripts.convert_capec.load_json_file",
        side_effect=[
            {
                "Attack_Pattern_Catalog": {
                    "Attack_Patterns": {"Attack_Pattern": []},
                    "Categories": {"Category": []},
                }
            },
            {"Requirements": []},
        ],
    )
    @patch("scripts.convert_capec.create_folder")
    @patch("scripts.convert_capec.empty_folder")
    @patch("scripts.convert_capec.set_logging")
    @patch("scripts.convert_capec.get_valid_version", return_value="5.0")
    @patch("scripts.convert_capec.parse_arguments")
    def test_main_happy_path(
        self,
        mock_parse_arguments,
        mock_get_valid_version,
        mock_set_logging,
        mock_empty_folder,
        mock_create_folder,
        mock_load_json,
        mock_validate_json,
        mock_load_capec_to_asvs,
        mock_create_capec_pages,
    ):
        mock_parse_arguments.return_value = self._base_args()

        capec.main()

        mock_set_logging.assert_called_once()
        mock_empty_folder.assert_called_once()
        mock_create_folder.assert_called_once()
        mock_create_capec_pages.assert_called_once()

    @patch("scripts.convert_capec.load_json_file", side_effect=[{}, {"Requirements": []}])
    @patch("scripts.convert_capec.get_valid_version", return_value="5.0")
    @patch("scripts.convert_capec.parse_arguments")
    @patch("scripts.convert_capec.set_logging")
    @patch("scripts.convert_capec.empty_folder")
    @patch("scripts.convert_capec.create_folder")
    @patch("scripts.convert_capec.create_capec_pages")
    def test_main_returns_on_invalid_data(
        self,
        mock_create_capec_pages,
        mock_create_folder,
        mock_empty_folder,
        mock_set_logging,
        mock_parse_arguments,
        mock_get_valid_version,
        mock_load_json,
    ):
        mock_parse_arguments.return_value = self._base_args()

        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            capec.main()

        self.assertIn("Invalid CAPEC data structure", " ".join(log.output))
        mock_create_capec_pages.assert_not_called()

    @patch("scripts.convert_capec.load_json_file")
    @patch("scripts.convert_capec.validate_json_data", return_value=True)
    @patch("scripts.convert_capec.get_valid_version", return_value="5.0")
    @patch("scripts.convert_capec.parse_arguments")
    @patch("scripts.convert_capec.set_logging")
    @patch("scripts.convert_capec.empty_folder")
    @patch("scripts.convert_capec.create_folder")
    @patch("scripts.convert_capec.create_capec_pages")
    def test_main_returns_when_asvs_map_missing(
        self,
        mock_create_capec_pages,
        mock_create_folder,
        mock_empty_folder,
        mock_set_logging,
        mock_parse_arguments,
        mock_get_valid_version,
        mock_validate,
        mock_load_json,
    ):
        mock_parse_arguments.return_value = self._base_args()
        mock_load_json.side_effect = [
            {
                "Attack_Pattern_Catalog": {
                    "Attack_Patterns": {"Attack_Pattern": []},
                    "Categories": {"Category": []},
                }
            },
            {},
        ]

        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            capec.main()

        self.assertIn("Failed to load ASVS mapping data", " ".join(log.output))
        mock_create_capec_pages.assert_not_called()

    @patch("scripts.convert_capec.load_capec_to_asvs_mapping", return_value={})
    @patch("scripts.convert_capec.load_json_file")
    @patch("scripts.convert_capec.validate_json_data", return_value=True)
    @patch("scripts.convert_capec.get_valid_version", return_value="5.0")
    @patch("scripts.convert_capec.parse_arguments")
    @patch("scripts.convert_capec.set_logging")
    @patch("scripts.convert_capec.empty_folder")
    @patch("scripts.convert_capec.create_folder")
    @patch("scripts.convert_capec.create_capec_pages")
    def test_main_returns_when_capec_to_asvs_missing(
        self,
        mock_create_capec_pages,
        mock_create_folder,
        mock_empty_folder,
        mock_set_logging,
        mock_parse_arguments,
        mock_get_valid_version,
        mock_validate,
        mock_load_json,
        mock_load_capec_to_asvs,
    ):
        mock_parse_arguments.return_value = self._base_args()
        mock_load_json.side_effect = [
            {
                "Attack_Pattern_Catalog": {
                    "Attack_Patterns": {"Attack_Pattern": []},
                    "Categories": {"Category": []},
                }
            },
            {"Requirements": []},
        ]

        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            capec.main()

        self.assertIn("Failed to load CAPEC to ASVS mapping", " ".join(log.output))
        mock_create_capec_pages.assert_not_called()


class TestConvertCapecEdgeCases(unittest.TestCase):

    # -------- create_capec_pages --------

    @patch("scripts.convert_capec.has_no_asvs_mapping", return_value=False)
    @patch("scripts.convert_capec.create_link_list", return_value="link")
    @patch("scripts.convert_capec.parse_description", return_value="desc")
    @patch("scripts.convert_capec.create_folder")
    def test_create_capec_pages_category_with_mapping(self, mock_folder, mock_desc, mock_link, mock_no_map):
        data = {
            "Attack_Pattern_Catalog": {
                "Attack_Patterns": {"Attack_Pattern": []},
                "Categories": {"Category": [{"_ID": "1", "_Name": "Test", "Summary": "sum"}]},
            }
        }

        capec_to_asvs_map = {1: {"v": ["1"]}}
        asvs_map = {}

        with patch("scripts.convert_capec.open", mock_open()):
            with patch("scripts.convert_capec.convert_vars.args", type("x", (), {"output_path": "out"})):
                capec.create_capec_pages(data, capec_to_asvs_map, asvs_map, "5.0")

    @patch("scripts.convert_capec.has_no_asvs_mapping", return_value=True)
    @patch("scripts.convert_capec.parse_description", return_value="desc")
    @patch("scripts.convert_capec.create_folder")
    def test_create_capec_pages_no_mapping(self, mock_folder, mock_desc, mock_no_map):
        data = {
            "Attack_Pattern_Catalog": {
                "Attack_Patterns": {"Attack_Pattern": [{"_ID": "1", "_Name": "Test", "Description": "d"}]},
                "Categories": {"Category": []},
            }
        }

        with patch("scripts.convert_capec.open", mock_open()):
            with patch("scripts.convert_capec.convert_vars.args", type("x", (), {"output_path": "out"})):
                capec.create_capec_pages(data, {}, {}, "5.0")

    # -------- main --------

    @patch("scripts.convert_capec.parse_arguments")
    @patch("scripts.convert_capec.load_json_file", return_value=None)
    @patch("scripts.convert_capec.set_logging")
    def test_main_invalid_data(self, mock_set_logging, mock_load, mock_parse):

        mock_parse.return_value = type(
            "x",
            (),
            {
                "input_path": "a",
                "asvs_mapping": "b",
                "capec_to_asvs": "c",
                "output_path": "out",
                "asvs_version": "5.0",
            },
        )

        capec.main()

    @patch("scripts.convert_capec.create_capec_pages")
    @patch("scripts.convert_capec.load_capec_to_asvs_mapping", return_value={1: {}})
    @patch("scripts.convert_capec.validate_json_data", return_value=True)
    @patch("scripts.convert_capec.load_json_file", side_effect=[{"a": 1}, {"b": 2}])
    @patch("scripts.convert_capec.parse_arguments")
    @patch("scripts.convert_capec.set_logging")
    def test_main_success(self, mock_log, mock_parse, mock_load, mock_validate, mock_map, mock_create):
        mock_parse.return_value = type(
            "x",
            (),
            {
                "input_path": "a",
                "asvs_mapping": "b",
                "capec_to_asvs": "c",
                "output_path": "out",
                "asvs_version": "5.0",
            },
        )

        capec.main()
        mock_create.assert_called()


if __name__ == "__main__":
    unittest.main()
