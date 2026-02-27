#!/usr/bin/env python3
import unittest
from unittest.mock import patch, mock_open
import argparse
import logging
from pathlib import Path

import scripts.convert_capec_map_to_asvs_map as capec_map

capec_map.convert_vars = capec_map.ConvertVars()


class ConvertVars:
    OUTPUT_DIR: str = str(Path(__file__).parent.parent.resolve() / "/test_files/output")
    OUTPUT_FILE: str = str(Path(__file__).parent.parent.resolve() / OUTPUT_DIR / "capec_to_asvs_map.yaml")


if "unittest.util" in __import__("sys").modules:
    # Show full diff in self.assertEqual.
    __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999


class TestExtractAsvsToCapecMappings(unittest.TestCase):
    """Test extract_asvs_to_capec_mappings function with various data structures"""

    def test_extract_simple_asvs_mapping(self):
        """Test extracting a simple ASVS to CAPEC mapping"""
        data = {"suits": [{"cards": [{"capec_map": {54: {"owasp_asvs": ["4.3.2", "13.2.2", "13.4.1"]}}}]}]}
        result = capec_map.extract_asvs_to_capec_mappings(data)

        self.assertIn("4.3.2", result)
        self.assertIn("13.2.2", result)
        self.assertIn("13.4.1", result)
        self.assertEqual(result["4.3.2"], {"54"})
        self.assertEqual(result["13.2.2"], {"54"})

    def test_extract_multiple_capec_same_asvs(self):
        """Test merging CAPEC codes from multiple cards with same ASVS requirement"""
        data = {
            "suits": [
                {
                    "cards": [
                        {"capec_map": {54: {"owasp_asvs": ["4.3.2", "13.2.2"]}}},
                        {"capec_map": {116: {"owasp_asvs": ["13.2.2", "15.2.3"]}}},
                    ]
                }
            ]
        }
        result = capec_map.extract_asvs_to_capec_mappings(data)

        self.assertIn("13.2.2", result)
        # Should merge CAPEC codes for same ASVS requirement
        self.assertEqual(result["13.2.2"], {"54", "116"})

    def test_extract_multiple_asvs_requirements(self):
        """Test extracting multiple ASVS requirements"""
        data = {
            "suits": [
                {"cards": [{"capec_map": {54: {"owasp_asvs": ["4.3.2"]}, 116: {"owasp_asvs": ["13.2.2", "15.2.3"]}}}]}
            ]
        }
        result = capec_map.extract_asvs_to_capec_mappings(data)

        self.assertGreaterEqual(len(result), 3)
        self.assertIn("4.3.2", result)
        self.assertIn("13.2.2", result)
        self.assertIn("15.2.3", result)

    def test_extract_asvs_no_suits(self):
        """Test with data that has no suits key"""
        data = {"other_key": "value"}

        with self.assertLogs(logging.getLogger(), logging.WARNING) as log:
            result = capec_map.extract_asvs_to_capec_mappings(data)

        self.assertEqual(result, {})
        self.assertIn("No 'suits' key found", log.output[0])

    def test_extract_asvs_empty_owasp_asvs(self):
        """Test with empty owasp_asvs list"""
        data = {"suits": [{"cards": [{"capec_map": {54: {"owasp_asvs": []}}}]}]}
        result = capec_map.extract_asvs_to_capec_mappings(data)

        self.assertEqual(result, {})


class TestExtractCapecMappings(unittest.TestCase):
    """Test extract_capec_mappings function with various data structures"""

    def test_extract_simple_capec_mapping(self):
        """Test extracting a simple CAPEC mapping"""
        data = {"suits": [{"cards": [{"capec_map": {54: {"owasp_asvs": ["4.3.2", "13.2.2", "13.4.1"]}}}]}]}
        result = capec_map.extract_capec_mappings(data)

        self.assertIn(54, result)
        self.assertEqual(result[54], {"4.3.2", "13.2.2", "13.4.1"})

    def test_extract_multiple_cards_same_capec(self):
        """Test merging ASVS requirements from multiple cards with same CAPEC code"""
        data = {
            "suits": [
                {
                    "cards": [
                        {"capec_map": {54: {"owasp_asvs": ["4.3.2", "13.2.2"]}}},
                        {"capec_map": {54: {"owasp_asvs": ["13.2.2", "15.2.3"]}}},
                    ]
                }
            ]
        }
        result = capec_map.extract_capec_mappings(data)

        self.assertIn(54, result)
        # Should merge and deduplicate
        self.assertEqual(result[54], {"4.3.2", "13.2.2", "15.2.3"})

    def test_extract_multiple_capec_codes(self):
        """Test extracting multiple CAPEC codes"""
        data = {
            "suits": [
                {"cards": [{"capec_map": {54: {"owasp_asvs": ["4.3.2"]}, 116: {"owasp_asvs": ["13.2.2", "15.2.3"]}}}]}
            ]
        }
        result = capec_map.extract_capec_mappings(data)

        self.assertEqual(len(result), 2)
        self.assertIn(54, result)
        self.assertIn(116, result)
        self.assertEqual(result[54], {"4.3.2"})
        self.assertEqual(result[116], {"13.2.2", "15.2.3"})

    def test_extract_no_suits(self):
        """Test with data that has no suits key"""
        data = {"other_key": "value"}

        with self.assertLogs(logging.getLogger(), logging.WARNING) as log:
            result = capec_map.extract_capec_mappings(data)

        self.assertEqual(result, {})
        self.assertIn("No 'suits' key found", log.output[0])

    def test_extract_no_cards_in_suit(self):
        """Test with suit that has no cards"""
        data = {"suits": [{"other_key": "value"}]}
        result = capec_map.extract_capec_mappings(data)

        self.assertEqual(result, {})

    def test_extract_no_capec_map_in_card(self):
        """Test with card that has no capec_map"""
        data = {"suits": [{"cards": [{"other_key": "value"}]}]}
        result = capec_map.extract_capec_mappings(data)

        self.assertEqual(result, {})

    def test_extract_capec_map_not_dict(self):
        """Test with capec_map that is not a dictionary"""
        data = {"suits": [{"cards": [{"capec_map": "not a dict"}]}]}
        result = capec_map.extract_capec_mappings(data)

        self.assertEqual(result, {})

    def test_extract_empty_owasp_asvs(self):
        """Test with empty owasp_asvs list"""
        data = {"suits": [{"cards": [{"capec_map": {54: {"owasp_asvs": []}}}]}]}
        result = capec_map.extract_capec_mappings(data)

        self.assertIn(54, result)
        self.assertEqual(result[54], set())

    def test_extract_multiple_suits(self):
        """Test extracting from multiple suits"""
        data = {
            "suits": [
                {"cards": [{"capec_map": {54: {"owasp_asvs": ["4.3.2"]}}}]},
                {"cards": [{"capec_map": {116: {"owasp_asvs": ["13.2.2"]}}}]},
            ]
        }
        result = capec_map.extract_capec_mappings(data)

        self.assertEqual(len(result), 2)
        self.assertIn(54, result)
        self.assertIn(116, result)


class TestConvertToOutputFormat(unittest.TestCase):
    """Test convert_to_output_format function"""

    def test_convert_simple_mapping(self):
        """Test converting a simple mapping"""
        capec_mapping = {54: {"4.3.2", "13.2.2", "13.4.1"}}
        result = capec_map.convert_to_output_format(capec_mapping)

        self.assertIn(54, result)
        self.assertIn("owasp_asvs", result[54])
        # Should be sorted
        self.assertEqual(result[54]["owasp_asvs"], ["13.2.2", "13.4.1", "4.3.2"])

    def test_convert_multiple_mappings(self):
        """Test converting multiple mappings"""
        capec_mapping = {54: {"4.3.2", "13.2.2"}, 116: {"15.2.3", "16.2.5"}}
        result = capec_map.convert_to_output_format(capec_mapping)

        self.assertEqual(len(result), 2)
        self.assertIn(54, result)
        self.assertIn(116, result)
        self.assertEqual(result[54]["owasp_asvs"], ["13.2.2", "4.3.2"])
        self.assertEqual(result[116]["owasp_asvs"], ["15.2.3", "16.2.5"])

    def test_convert_empty_mapping(self):
        """Test converting empty mapping"""
        capec_mapping = {}
        result = capec_map.convert_to_output_format(capec_mapping)

        self.assertEqual(result, {})

    def test_convert_sorted_keys(self):
        """Test that keys are sorted in output"""
        capec_mapping = {116: {"15.2.3"}, 54: {"4.3.2"}, 28: {"1.2.2"}}
        result = capec_map.convert_to_output_format(capec_mapping)

        keys = list(result.keys())
        self.assertEqual(keys, [28, 54, 116])  # Sorted as integers

    def test_convert_with_capec_codes_parameter(self):
        """Test converting ASVS to CAPEC mapping with capec_codes parameter"""
        asvs_mapping = {"4.3.2": {54, 116}, "13.2.2": {54}}
        result = capec_map.convert_to_output_format(asvs_mapping, parameter="capec_codes")

        self.assertIn("4.3.2", result)
        self.assertIn("capec_codes", result["4.3.2"])
        self.assertEqual(sorted(result["4.3.2"]["capec_codes"]), [54, 116])


class TestLoadYamlFile(unittest.TestCase):
    """Test load_yaml_file function"""

    @patch("builtins.open", new_callable=mock_open, read_data="key: value\n")
    @patch("yaml.safe_load")
    def test_load_valid_yaml(self, mock_yaml_load, mock_file):
        """Test loading a valid YAML file"""
        mock_yaml_load.return_value = {"key": "value"}

        result = capec_map.load_yaml_file(Path(ConvertVars.OUTPUT_DIR + "test.yaml"))

        self.assertEqual(result, {"key": "value"})
        mock_file.assert_called_once()
        mock_yaml_load.assert_called_once()

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_file_not_found(self, mock_file):
        """Test loading non-existent file"""
        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            result = capec_map.load_yaml_file(Path(ConvertVars.OUTPUT_DIR + "nonexistent.yaml"))

        self.assertEqual(result, {})
        self.assertIn("File not found", log.output[0])

    @patch("builtins.open", new_callable=mock_open, read_data="invalid: yaml: content:")
    @patch("yaml.safe_load", side_effect=Exception("YAML parse error"))
    def test_load_yaml_error(self, mock_yaml_load, mock_file):
        """Test loading file with YAML error"""
        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            result = capec_map.load_yaml_file(Path(ConvertVars.OUTPUT_DIR + "invalid.yaml"))

        self.assertEqual(result, {})
        self.assertIn("Error loading YAML file", log.output[0])

    @patch("builtins.open", new_callable=mock_open, read_data="")
    @patch("yaml.safe_load", return_value=None)
    def test_load_empty_yaml(self, mock_yaml_load, mock_file):
        """Test loading empty YAML file"""
        result = capec_map.load_yaml_file(Path(ConvertVars.OUTPUT_DIR + "empty.yaml"))

        self.assertEqual(result, {})


class TestSaveYamlFile(unittest.TestCase):
    """Test save_yaml_file function"""

    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.dump")
    def test_save_valid_yaml(self, mock_yaml_dump, mock_file):
        """Test saving a valid YAML file"""
        data = {"key": "value"}

        result = capec_map.save_yaml_file(Path(ConvertVars.OUTPUT_FILE), data)

        self.assertTrue(result)
        mock_file.assert_called_once()
        mock_yaml_dump.assert_called_once()

    @patch("builtins.open", side_effect=IOError("Write error"))
    def test_save_io_error(self, mock_file):
        """Test saving with IO error"""
        data = {"key": "value"}

        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            result = capec_map.save_yaml_file(Path(ConvertVars.OUTPUT_DIR + "error.yaml"), data)

        self.assertFalse(result)
        self.assertIn("Error saving YAML file", log.output[0])


class TestParseArguments(unittest.TestCase):
    """Test parse_arguments function"""

    def test_parse_default_arguments(self):
        """Test parsing with no arguments (uses defaults)"""
        args = capec_map.parse_arguments([])

        self.assertIsNone(args.input_path)
        self.assertEqual(args.output_path, capec_map.ConvertVars.DEFAULT_OUTPUT_PATH)
        self.assertEqual(args.version, "latest")
        self.assertEqual(args.edition, "edition")
        self.assertFalse(args.debug)

    def test_parse_custom_input_path(self):
        """Test parsing with custom input path"""
        args = capec_map.parse_arguments(["-i", "custom/input.yaml"])

        self.assertEqual(args.input_path, "custom/input.yaml")

    def test_parse_custom_output_path(self):
        """Test parsing with custom output path"""
        args = capec_map.parse_arguments(["-o", ConvertVars.OUTPUT_FILE])

        self.assertEqual(args.output_path, ConvertVars.OUTPUT_FILE)

    def test_parse_debug_flag(self):
        """Test parsing with debug flag"""
        args = capec_map.parse_arguments(["-d"])

        self.assertTrue(args.debug)

    def test_parse_version_parameter(self):
        """Test parsing with version parameter"""
        args = capec_map.parse_arguments(["-v", "3.0"])
        self.assertEqual(args.version, "3.0")

    def test_parse_edition_parameter(self):
        """Test parsing with edition parameter"""
        args = capec_map.parse_arguments(["-e", "webapp"])
        self.assertEqual(args.edition, "webapp")

    def test_parse_asvs_json_argument(self):
        """Test parsing with asvs-json argument"""
        args = capec_map.parse_arguments(["--asvs-json", "asvs.json"])
        self.assertEqual(args.asvs_json, "asvs.json")

    def test_parse_all_arguments(self):
        """Test parsing with all arguments"""
        args = capec_map.parse_arguments(
            [
                "-i",
                "input.yaml",
                "-o",
                ConvertVars.OUTPUT_FILE,
                "-v",
                "3.0",
                "-e",
                "webapp",
                "-d",
                "--asvs-json",
                "asvs.json",
            ]
        )

        self.assertEqual(args.input_path, "input.yaml")
        self.assertEqual(args.output_path, ConvertVars.OUTPUT_FILE)
        self.assertEqual(args.version, "3.0")
        self.assertEqual(args.edition, "webapp")
        self.assertEqual(args.asvs_json, "asvs.json")
        self.assertTrue(args.debug)

    def test_parse_long_form_arguments(self):
        """Test parsing with long form arguments"""
        args = capec_map.parse_arguments(
            [
                "--input-path",
                "input.yaml",
                "--output-path",
                ConvertVars.OUTPUT_FILE,
                "--version",
                "3.0",
                "--edition",
                "webapp",
                "--asvs-json",
                "asvs.json",
                "--debug",
            ]
        )

        self.assertEqual(args.input_path, "input.yaml")
        self.assertEqual(args.output_path, ConvertVars.OUTPUT_FILE)
        self.assertEqual(args.version, "3.0")
        self.assertEqual(args.edition, "webapp")
        self.assertEqual(args.asvs_json, "asvs.json")
        self.assertTrue(args.debug)


class TestSetLogging(unittest.TestCase):
    """Test set_logging function"""

    def test_set_logging_info_level(self):
        """Test setting logging to INFO level"""
        capec_map.convert_vars.args = argparse.Namespace(debug=False)

        capec_map.set_logging()

        self.assertEqual(logging.getLogger().level, logging.INFO)

    def test_set_logging_debug_level(self):
        """Test setting logging to DEBUG level"""
        capec_map.convert_vars.args = argparse.Namespace(debug=True)

        capec_map.set_logging()

        self.assertEqual(logging.getLogger().level, logging.DEBUG)


class TestMainFunction(unittest.TestCase):
    """Test main function with mocked dependencies"""

    @patch("scripts.convert_capec_map_to_asvs_map.save_yaml_file")
    @patch("scripts.convert_capec_map_to_asvs_map.load_yaml_file")
    @patch("scripts.convert_capec_map_to_asvs_map.parse_arguments")
    @patch("sys.exit")
    def test_main_successful_execution(self, mock_exit, mock_parse_args, mock_load, mock_save):
        """Test successful main execution"""
        # Setup mocks
        mock_parse_args.return_value = argparse.Namespace(
            input_path=Path("input.yaml"),
            output_path=Path(ConvertVars.OUTPUT_FILE),
            version="3.0",
            edition="webapp",
            asvs_json=None,
            debug=False,
        )
        mock_load.return_value = {"suits": [{"cards": [{"capec_map": {54: {"owasp_asvs": ["4.3.2"]}}}]}]}
        mock_save.return_value = True

        capec_map.main()

        mock_load.assert_called_once()
        # Should be called twice - once for capec file, once for asvs file
        self.assertEqual(mock_save.call_count, 2)
        mock_exit.assert_not_called()

    @patch("scripts.convert_capec_map_to_asvs_map.load_yaml_file")
    @patch("scripts.convert_capec_map_to_asvs_map.parse_arguments")
    @patch("sys.exit")
    def test_main_no_data_loaded(self, mock_exit, mock_parse_args, mock_load):
        """Test main with no data loaded"""
        mock_parse_args.return_value = argparse.Namespace(
            input_path=Path("input.yaml"),
            output_path=Path(ConvertVars.OUTPUT_DIR + "nonexistent2.yaml"),
            version="3.0",
            edition="webapp",
            asvs_json=None,
            debug=False,
        )
        mock_load.return_value = {}

        with self.assertLogs(logging.getLogger(), logging.ERROR):
            capec_map.main()

        # Check that exit was called at least once with argument 1
        self.assertTrue(mock_exit.called)
        # Get the last call
        last_call = mock_exit.call_args_list[-1]
        self.assertEqual(last_call[0][0], 1)

    @patch("scripts.convert_capec_map_to_asvs_map.save_yaml_file")
    @patch("scripts.convert_capec_map_to_asvs_map.load_yaml_file")
    @patch("scripts.convert_capec_map_to_asvs_map.parse_arguments")
    @patch("sys.exit")
    def test_main_save_fails(self, mock_exit2, mock_parse_args, mock_load, mock_save):
        """Test main when save fails"""
        mock_parse_args.return_value = argparse.Namespace(
            input_path=Path("input.yaml"),
            output_path=Path(ConvertVars.OUTPUT_DIR + "nonexistent3.yaml"),
            version="3.0",
            edition="webapp",
            asvs_json=None,
            debug=False,
        )
        mock_load.return_value = {"suits": [{"cards": [{"capec_map": {54: {"owasp_asvs": ["4.3.2"]}}}]}]}
        mock_save.return_value = False

        with self.assertLogs(logging.getLogger(), logging.ERROR):
            capec_map.main()

        # Check that exit was called at least once with argument 1
        self.assertTrue(mock_exit2.called)
        # Get the last call
        last_call = mock_exit2.call_args_list[-1]
        self.assertEqual(last_call[0][0], 1)

    @patch("scripts.convert_capec_map_to_asvs_map.save_yaml_file")
    @patch("scripts.convert_capec_map_to_asvs_map.load_json_file")
    @patch("scripts.convert_capec_map_to_asvs_map.load_yaml_file")
    @patch("scripts.convert_capec_map_to_asvs_map.parse_arguments")
    @patch("sys.exit")
    def test_main_with_asvs_json(self, mock_exit, mock_parse_args, mock_load_yaml, mock_load_json, mock_save):
        """Test main execution with asvs_json argument"""
        mock_parse_args.return_value = argparse.Namespace(
            input_path=Path("input.yaml"),
            output_path=Path(ConvertVars.OUTPUT_FILE),
            version="3.0",
            edition="webapp",
            asvs_json="asvs.json",
            debug=False,
        )
        mock_load_yaml.return_value = {
            "meta": {"edition": "webapp"},
            "suits": [
                {
                    "cards": [
                        {
                            "capec_map": {54: {"owasp_asvs": ["4.3.2"]}},
                            "asvs_map": {"4.3.2": {"capec_codes": [54]}},
                        }
                    ]
                }
            ],
        }
        mock_load_json.return_value = {
            "Requirements": [{"Shortcode": "V4.3.2", "Description": "Test description", "L": "L1"}]
        }
        mock_save.return_value = True

        capec_map.main()

        mock_load_json.assert_called_once()
        self.assertEqual(mock_save.call_count, 2)
        mock_exit.assert_not_called()

    @patch("scripts.convert_capec_map_to_asvs_map.save_yaml_file")
    @patch("scripts.convert_capec_map_to_asvs_map.load_json_file")
    @patch("scripts.convert_capec_map_to_asvs_map.load_yaml_file")
    @patch("scripts.convert_capec_map_to_asvs_map.parse_arguments")
    @patch("sys.exit")
    def test_main_with_asvs_json_load_fails(
        self, mock_exit, mock_parse_args, mock_load_yaml, mock_load_json, mock_save
    ):
        """Test main execution when asvs_json file fails to load"""
        mock_parse_args.return_value = argparse.Namespace(
            input_path=Path("input.yaml"),
            output_path=Path(ConvertVars.OUTPUT_FILE),
            version="3.0",
            edition="webapp",
            asvs_json="bad_asvs.json",
            debug=False,
        )
        mock_load_yaml.return_value = {"suits": [{"cards": [{"capec_map": {54: {"owasp_asvs": ["4.3.2"]}}}]}]}
        mock_load_json.return_value = {}
        mock_save.return_value = True

        capec_map.main()

        mock_load_json.assert_called_once()
        self.assertEqual(mock_save.call_count, 2)
        mock_exit.assert_not_called()

    @patch("scripts.convert_capec_map_to_asvs_map.save_yaml_file")
    @patch("scripts.convert_capec_map_to_asvs_map.load_yaml_file")
    @patch("scripts.convert_capec_map_to_asvs_map.parse_arguments")
    @patch("sys.exit")
    def test_main_no_input_path(self, mock_exit, mock_parse_args, mock_load, mock_save):
        """Test main when input_path is None (uses default path construction)"""
        mock_parse_args.return_value = argparse.Namespace(
            input_path=None,
            output_path=Path(ConvertVars.OUTPUT_FILE),
            version="3.0",
            edition="webapp",
            asvs_json=None,
            debug=False,
        )
        mock_load.return_value = {"suits": [{"cards": [{"capec_map": {54: {"owasp_asvs": ["4.3.2"]}}}]}]}
        mock_save.return_value = True

        capec_map.main()

        mock_load.assert_called_once()
        self.assertEqual(mock_save.call_count, 2)
        mock_exit.assert_not_called()

    @patch("scripts.convert_capec_map_to_asvs_map.save_yaml_file")
    @patch("scripts.convert_capec_map_to_asvs_map.load_yaml_file")
    @patch("scripts.convert_capec_map_to_asvs_map.parse_arguments")
    @patch("sys.exit")
    def test_main_asvs_save_fails(self, mock_exit, mock_parse_args, mock_load, mock_save):
        """Test main when the second save (ASVS output) fails"""
        mock_parse_args.return_value = argparse.Namespace(
            input_path=Path("input.yaml"),
            output_path=Path(ConvertVars.OUTPUT_FILE),
            version="3.0",
            edition="webapp",
            asvs_json=None,
            debug=False,
        )
        mock_load.return_value = {"suits": [{"cards": [{"capec_map": {54: {"owasp_asvs": ["4.3.2"]}}}]}]}
        # First save succeeds, second save fails
        mock_save.side_effect = [True, False]

        with self.assertLogs(logging.getLogger(), logging.ERROR):
            capec_map.main()

        self.assertTrue(mock_exit.called)
        last_call = mock_exit.call_args_list[-1]
        self.assertEqual(last_call[0][0], 1)


class TestLoadJsonFile(unittest.TestCase):
    """Test load_json_file function"""

    @patch("builtins.open", mock_open(read_data='{"key": "value"}'))
    def test_load_valid_json(self):
        """Test loading a valid JSON file"""
        result = capec_map.load_json_file(Path("test.json"))
        self.assertEqual(result, {"key": "value"})

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_file_not_found(self, mock_file):
        """Test loading non-existent file"""
        with self.assertLogs(logging.getLogger(), logging.ERROR):
            result = capec_map.load_json_file(Path("nonexistent.json"))
        self.assertEqual(result, {})

    @patch("builtins.open", mock_open(read_data="not valid json"))
    def test_load_json_error(self):
        """Test loading file with JSON parse error"""
        with self.assertLogs(logging.getLogger(), logging.ERROR):
            result = capec_map.load_json_file(Path("bad.json"))
        self.assertEqual(result, {})

    @patch("builtins.open", mock_open(read_data="null"))
    def test_load_empty_json(self):
        """Test loading JSON file that returns None"""
        result = capec_map.load_json_file(Path("empty.json"))
        self.assertEqual(result, {})

    @patch("builtins.open", side_effect=PermissionError("Access denied"))
    def test_load_json_generic_error(self, mock_file):
        """Test loading JSON file with a generic exception"""
        with self.assertLogs(logging.getLogger(), logging.ERROR):
            result = capec_map.load_json_file(Path("noperm.json"))
        self.assertEqual(result, {})


class TestExtractAsvsDetails(unittest.TestCase):
    """Test extract_asvs_details function"""

    def test_extract_simple_requirement(self):
        """Test extracting a single requirement"""
        data = {"Requirements": [{"Shortcode": "V1.1.1", "Description": "Test req", "L": "L1"}]}
        result = capec_map.extract_asvs_details(data)
        self.assertEqual(result, {"1.1.1": {"description": "Test req", "level": "L1"}})

    def test_extract_multiple_requirements(self):
        """Test extracting multiple requirements"""
        data = {
            "Requirements": [
                {"Shortcode": "V1.1.1", "Description": "First", "L": "L1"},
                {"Shortcode": "V2.2.2", "Description": "Second", "L": "L2"},
            ]
        }
        result = capec_map.extract_asvs_details(data)
        self.assertEqual(len(result), 2)
        self.assertEqual(result["1.1.1"]["description"], "First")
        self.assertEqual(result["2.2.2"]["description"], "Second")

    def test_extract_nested_structure(self):
        """Test extracting from nested structure"""
        data = {"chapter": {"sections": [{"items": [{"Shortcode": "V3.3.3", "Description": "Nested", "L": "L3"}]}]}}
        result = capec_map.extract_asvs_details(data)
        self.assertEqual(result, {"3.3.3": {"description": "Nested", "level": "L3"}})

    def test_extract_shortcode_without_v_prefix(self):
        """Test extracting requirement without V prefix"""
        data = {"Requirements": [{"Shortcode": "4.4.4", "Description": "No V", "L": "L1"}]}
        result = capec_map.extract_asvs_details(data)
        self.assertEqual(result, {"4.4.4": {"description": "No V", "level": "L1"}})

    def test_extract_empty_data(self):
        """Test extracting from empty dict"""
        result = capec_map.extract_asvs_details({})
        self.assertEqual(result, {})

    def test_extract_data_without_requirements(self):
        """Test extracting from data without requirement fields"""
        data = {"something": [{"other": "data"}]}
        result = capec_map.extract_asvs_details(data)
        self.assertEqual(result, {})

    def test_extract_ignores_partial_requirements(self):
        """Test that nodes missing required fields are skipped"""
        data = {
            "Requirements": [
                {"Shortcode": "V1.1.1", "Description": "Valid", "L": "L1"},
                {"Shortcode": "V2.2.2", "Description": "Missing L"},
                {"Shortcode": "V3.3.3", "L": "L1"},
            ]
        }
        result = capec_map.extract_asvs_details(data)
        self.assertEqual(len(result), 1)
        self.assertIn("1.1.1", result)


class TestConvertToOutputFormatWithEnrichment(unittest.TestCase):
    """Test convert_to_output_format function with enrichment_data"""

    def test_convert_with_enrichment_data(self):
        """Test converting with enrichment data"""
        capec_map_data = {"1.1.1": {"4.3.2"}}
        enrichment = {"1.1.1": {"description": "Test desc", "level": "L1"}}
        result = capec_map.convert_to_output_format(capec_map_data, parameter="capec_codes", enrichment_data=enrichment)
        self.assertIn("1.1.1", result)
        self.assertEqual(result["1.1.1"]["description"], "Test desc")
        self.assertEqual(result["1.1.1"]["level"], "L1")
        self.assertEqual(result["1.1.1"]["capec_codes"], ["4.3.2"])

    def test_convert_with_partial_enrichment(self):
        """Test converting when enrichment data is missing for some keys"""
        capec_map_data = {"1.1.1": {"4.3.2"}, "2.2.2": {"5.5.5"}}
        enrichment = {"1.1.1": {"description": "Only first", "level": "L1"}}
        result = capec_map.convert_to_output_format(capec_map_data, parameter="capec_codes", enrichment_data=enrichment)
        self.assertIn("description", result["1.1.1"])
        self.assertNotIn("description", result["2.2.2"])

    def test_convert_with_meta_and_enrichment(self):
        """Test converting with both meta and enrichment data"""
        capec_map_data = {"1.1.1": {"4.3.2"}}
        enrichment = {"1.1.1": {"description": "Desc", "level": "L2"}}
        meta = {"edition": "webapp"}
        result = capec_map.convert_to_output_format(
            capec_map_data, parameter="capec_codes", meta=meta, enrichment_data=enrichment
        )
        self.assertIn("meta", result)
        self.assertEqual(result["meta"]["edition"], "webapp")
        self.assertEqual(result["1.1.1"]["description"], "Desc")


if __name__ == "__main__":
    unittest.main()
