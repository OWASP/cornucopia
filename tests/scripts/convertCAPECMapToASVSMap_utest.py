#!/usr/bin/env python3
import unittest
from unittest.mock import patch, mock_open
import argparse
import logging
from pathlib import Path

import scripts.convertCAPECMapToASVSMap as capec_map

capec_map.convert_vars = capec_map.ConvertVars()

class ConvertVars:
    OUTPUT_DIR: str = str(Path(__file__).parent.parent.resolve() / "/test_files/output")
    OUTPUT_FILE: str = str(Path(__file__).parent.parent.resolve() / OUTPUT_DIR / "capec_to_asvs_map.yaml")


if "unittest.util" in __import__("sys").modules:
    # Show full diff in self.assertEqual.
    __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999


class TestExtractCapecMappings(unittest.TestCase):
    """Test extract_capec_mappings function with various data structures"""

    def test_extract_simple_capec_mapping(self):
        """Test extracting a simple CAPEC mapping"""
        data = {"suits": [{"cards": [{"capec_map": {"54": {"owasp_asvs": ["4.3.2", "13.2.2", "13.4.1"]}}}]}]}
        result = capec_map.extract_capec_mappings(data)

        self.assertIn("54", result)
        self.assertEqual(result["54"], {"4.3.2", "13.2.2", "13.4.1"})

    def test_extract_multiple_cards_same_capec(self):
        """Test merging ASVS requirements from multiple cards with same CAPEC code"""
        data = {
            "suits": [
                {
                    "cards": [
                        {"capec_map": {"54": {"owasp_asvs": ["4.3.2", "13.2.2"]}}},
                        {"capec_map": {"54": {"owasp_asvs": ["13.2.2", "15.2.3"]}}},
                    ]
                }
            ]
        }
        result = capec_map.extract_capec_mappings(data)

        self.assertIn("54", result)
        # Should merge and deduplicate
        self.assertEqual(result["54"], {"4.3.2", "13.2.2", "15.2.3"})

    def test_extract_multiple_capec_codes(self):
        """Test extracting multiple CAPEC codes"""
        data = {
            "suits": [
                {
                    "cards": [
                        {"capec_map": {"54": {"owasp_asvs": ["4.3.2"]}, "116": {"owasp_asvs": ["13.2.2", "15.2.3"]}}}
                    ]
                }
            ]
        }
        result = capec_map.extract_capec_mappings(data)

        self.assertEqual(len(result), 2)
        self.assertIn("54", result)
        self.assertIn("116", result)
        self.assertEqual(result["54"], {"4.3.2"})
        self.assertEqual(result["116"], {"13.2.2", "15.2.3"})

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
        data = {"suits": [{"cards": [{"capec_map": {"54": {"owasp_asvs": []}}}]}]}
        result = capec_map.extract_capec_mappings(data)

        self.assertIn("54", result)
        self.assertEqual(result["54"], set())

    def test_extract_multiple_suits(self):
        """Test extracting from multiple suits"""
        data = {
            "suits": [
                {"cards": [{"capec_map": {"54": {"owasp_asvs": ["4.3.2"]}}}]},
                {"cards": [{"capec_map": {"116": {"owasp_asvs": ["13.2.2"]}}}]},
            ]
        }
        result = capec_map.extract_capec_mappings(data)

        self.assertEqual(len(result), 2)
        self.assertIn("54", result)
        self.assertIn("116", result)


class TestConvertToOutputFormat(unittest.TestCase):
    """Test convert_to_output_format function"""

    def test_convert_simple_mapping(self):
        """Test converting a simple mapping"""
        capec_mapping = {"54": {"4.3.2", "13.2.2", "13.4.1"}}
        result = capec_map.convert_to_output_format(capec_mapping)

        self.assertIn("54", result)
        self.assertIn("owasp_asvs", result["54"])
        # Should be sorted
        self.assertEqual(result["54"]["owasp_asvs"], ["13.2.2", "13.4.1", "4.3.2"])

    def test_convert_multiple_mappings(self):
        """Test converting multiple mappings"""
        capec_mapping = {"54": {"4.3.2", "13.2.2"}, "116": {"15.2.3", "16.2.5"}}
        result = capec_map.convert_to_output_format(capec_mapping)

        self.assertEqual(len(result), 2)
        self.assertIn("54", result)
        self.assertIn("116", result)
        self.assertEqual(result["54"]["owasp_asvs"], ["13.2.2", "4.3.2"])
        self.assertEqual(result["116"]["owasp_asvs"], ["15.2.3", "16.2.5"])

    def test_convert_empty_mapping(self):
        """Test converting empty mapping"""
        capec_mapping = {}
        result = capec_map.convert_to_output_format(capec_mapping)

        self.assertEqual(result, {})

    def test_convert_sorted_keys(self):
        """Test that keys are sorted in output"""
        capec_mapping = {"116": {"15.2.3"}, "54": {"4.3.2"}, "28": {"1.2.2"}}
        result = capec_map.convert_to_output_format(capec_mapping)

        keys = list(result.keys())
        self.assertEqual(keys, ["116", "28", "54"])  # Sorted as strings


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

        self.assertEqual(args.input_path, capec_map.ConvertVars.DEFAULT_INPUT_PATH)
        self.assertEqual(args.output_path, capec_map.ConvertVars.DEFAULT_OUTPUT_PATH)
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

    def test_parse_all_arguments(self):
        """Test parsing with all arguments"""
        args = capec_map.parse_arguments(["-i", "input.yaml", "-o", ConvertVars.OUTPUT_FILE, "-d"])

        self.assertEqual(args.input_path, "input.yaml")
        self.assertEqual(args.output_path, ConvertVars.OUTPUT_FILE)
        self.assertTrue(args.debug)

    def test_parse_long_form_arguments(self):
        """Test parsing with long form arguments"""
        args = capec_map.parse_arguments(["--input-path", "input.yaml", "--output-path", ConvertVars.OUTPUT_FILE, "--debug"])

        self.assertEqual(args.input_path, "input.yaml")
        self.assertEqual(args.output_path, ConvertVars.OUTPUT_FILE)
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

    @patch("scripts.convertCAPECMapToASVSMap.save_yaml_file")
    @patch("scripts.convertCAPECMapToASVSMap.load_yaml_file")
    @patch("scripts.convertCAPECMapToASVSMap.parse_arguments")
    @patch("sys.exit")
    def test_main_successful_execution(self, mock_exit, mock_parse_args, mock_load, mock_save):
        """Test successful main execution"""
        # Setup mocks
        mock_parse_args.return_value = argparse.Namespace(
            input_path=Path("input.yaml"), output_path=Path(ConvertVars.OUTPUT_FILE), debug=False
        )
        mock_load.return_value = {"suits": [{"cards": [{"capec_map": {"54": {"owasp_asvs": ["4.3.2"]}}}]}]}
        mock_save.return_value = True

        capec_map.main()

        mock_load.assert_called_once()
        mock_save.assert_called_once()
        mock_exit.assert_not_called()

    @patch("scripts.convertCAPECMapToASVSMap.load_yaml_file")
    @patch("scripts.convertCAPECMapToASVSMap.parse_arguments")
    @patch("sys.exit")
    def test_main_no_data_loaded(self, mock_exit, mock_parse_args, mock_load):
        """Test main with no data loaded"""
        mock_parse_args.return_value = argparse.Namespace(
            input_path=Path("input.yaml"), output_path=Path(ConvertVars.OUTPUT_DIR + "nonexistent2.yaml"), debug=False
        )
        mock_load.return_value = {}

        with self.assertLogs(logging.getLogger(), logging.ERROR):
            capec_map.main()

        # Check that exit was called at least once with argument 1
        self.assertTrue(mock_exit.called)
        # Get the last call
        last_call = mock_exit.call_args_list[-1]
        self.assertEqual(last_call[0][0], 1)

    @patch("scripts.convertCAPECMapToASVSMap.save_yaml_file")
    @patch("scripts.convertCAPECMapToASVSMap.load_yaml_file")
    @patch("scripts.convertCAPECMapToASVSMap.parse_arguments")
    @patch("sys.exit")
    def test_main_save_fails(self, mock_exit2, mock_parse_args, mock_load, mock_save):
        """Test main when save fails"""
        mock_parse_args.return_value = argparse.Namespace(
            input_path=Path("input.yaml"), output_path=Path(ConvertVars.OUTPUT_DIR + "nonexistent3.yaml"), debug=False
        )
        mock_load.return_value = {"suits": [{"cards": [{"capec_map": {"54": {"owasp_asvs": ["4.3.2"]}}}]}]}
        mock_save.return_value = False

        with self.assertLogs(logging.getLogger(), logging.ERROR):
            capec_map.main()
        
        # Check that exit was called at least once with argument 1
        self.assertTrue(mock_exit2.called)
        # Get the last call
        last_call = mock_exit2.call_args_list[-1]
        self.assertEqual(last_call[0][0], 1)


if __name__ == "__main__":
    unittest.main()
