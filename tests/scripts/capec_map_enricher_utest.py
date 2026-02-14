#!/usr/bin/env python3
import unittest
from unittest.mock import patch, mock_open
import argparse
import logging
from pathlib import Path

import scripts.capec_map_enricher as enricher

enricher.enricher_vars = enricher.EnricherVars()


class ConvertVars:
    OUTPUT_DIR: str = str(Path(__file__).parent.parent.resolve() / "test_files/output")
    OUTPUT_FILE: str = str(Path(__file__).parent.parent.resolve() / OUTPUT_DIR / "enriched_capec.yaml")


if "unittest.util" in __import__("sys").modules:
    # Show full diff in self.assertEqual.
    __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999


class TestExtractCapecNames(unittest.TestCase):
    """Test extract_capec_names function"""

    def test_extract_simple_capec_names(self):
        """Test extracting CAPEC names from simple JSON structure"""
        data = {
            "Attack_Pattern_Catalog": {
                "Attack_Patterns": {
                    "Attack_Pattern": [
                        {"_ID": "1", "_Name": "Test Attack 1"},
                        {"_ID": "5", "_Name": "Test Attack 5"},
                    ]
                }
            }
        }
        result = enricher.extract_capec_names(data)

        self.assertEqual(len(result), 2)
        self.assertIn(1, result)
        self.assertIn(5, result)
        self.assertEqual(result[1], "Test Attack 1")
        self.assertEqual(result[5], "Test Attack 5")

    def test_extract_capec_names_missing_catalog(self):
        """Test with missing Attack_Pattern_Catalog"""
        data = {"other_key": "value"}

        with self.assertLogs(logging.getLogger(), logging.WARNING) as log:
            result = enricher.extract_capec_names(data)

        self.assertEqual(result, {})
        self.assertIn("No 'Attack_Pattern_Catalog' key found", log.output[0])

    def test_extract_capec_names_missing_patterns(self):
        """Test with missing Attack_Patterns"""
        data = {"Attack_Pattern_Catalog": {"other_key": "value"}}

        with self.assertLogs(logging.getLogger(), logging.WARNING) as log:
            result = enricher.extract_capec_names(data)

        self.assertEqual(result, {})
        self.assertIn("No 'Attack_Patterns' key found", log.output[0])

    def test_extract_capec_names_missing_attack_pattern(self):
        """Test with missing Attack_Pattern"""
        data = {"Attack_Pattern_Catalog": {"Attack_Patterns": {"other_key": "value"}}}

        with self.assertLogs(logging.getLogger(), logging.WARNING) as log:
            result = enricher.extract_capec_names(data)

        self.assertEqual(result, {})
        self.assertIn("No 'Attack_Pattern' key found", log.output[0])

    def test_extract_capec_names_not_list(self):
        """Test with Attack_Pattern not being a list"""
        data = {"Attack_Pattern_Catalog": {"Attack_Patterns": {"Attack_Pattern": "not a list"}}}

        with self.assertLogs(logging.getLogger(), logging.WARNING) as log:
            result = enricher.extract_capec_names(data)

        self.assertEqual(result, {})
        self.assertIn("'Attack_Pattern' is not a list", log.output[0])

    def test_extract_capec_names_missing_fields(self):
        """Test with missing _ID or _Name fields"""
        data = {
            "Attack_Pattern_Catalog": {
                "Attack_Patterns": {
                    "Attack_Pattern": [
                        {"_ID": "1", "_Name": "Complete Entry"},
                        {"_ID": "2"},  # Missing _Name
                        {"_Name": "Missing ID"},  # Missing _ID
                    ]
                }
            }
        }
        result = enricher.extract_capec_names(data)

        # Should only extract the complete entry
        self.assertEqual(len(result), 1)
        self.assertIn(1, result)


class TestEnrichCapecMappings(unittest.TestCase):
    """Test enrich_capec_mappings function"""

    def test_enrich_simple_mappings(self):
        """Test enriching simple CAPEC mappings"""
        capec_mappings = {
            1: {"owasp_asvs": ["1.2.3", "4.5.6"]},
            5: {"owasp_asvs": ["7.8.9"]},
        }
        capec_names = {
            1: "Test Attack 1",
            5: "Test Attack 5",
        }

        result = enricher.enrich_capec_mappings(capec_mappings, capec_names)

        self.assertEqual(len(result), 2)
        self.assertIn(1, result)
        self.assertIn(5, result)
        self.assertEqual(result[1]["name"], "Test Attack 1")
        self.assertEqual(result[5]["name"], "Test Attack 5")
        self.assertEqual(result[1]["owasp_asvs"], ["1.2.3", "4.5.6"])
        self.assertEqual(result[5]["owasp_asvs"], ["7.8.9"])

    def test_enrich_mappings_missing_name(self):
        """Test enriching when name is not found"""
        capec_mappings = {
            1: {"owasp_asvs": ["1.2.3"]},
            999: {"owasp_asvs": ["4.5.6"]},  # No name in catalog
        }
        capec_names = {
            1: "Test Attack 1",
        }

        with self.assertLogs(logging.getLogger(), logging.WARNING) as log:
            result = enricher.enrich_capec_mappings(capec_mappings, capec_names)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[1]["name"], "Test Attack 1")
        self.assertEqual(result[999]["name"], "CAPEC-999")  # Fallback name
        self.assertIn("No name found for CAPEC-999", log.output[0])

    def test_enrich_mappings_preserves_data(self):
        """Test that enrichment preserves existing mapping data"""
        capec_mappings = {
            1: {"owasp_asvs": ["1.2.3", "4.5.6"], "other_field": "value"},
        }
        capec_names = {1: "Test Attack 1"}

        result = enricher.enrich_capec_mappings(capec_mappings, capec_names)

        self.assertEqual(result[1]["owasp_asvs"], ["1.2.3", "4.5.6"])
        self.assertEqual(result[1]["other_field"], "value")
        self.assertEqual(result[1]["name"], "Test Attack 1")


class TestLoadJsonFile(unittest.TestCase):
    """Test load_json_file function"""

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_valid_json(self, mock_file):
        """Test loading a valid JSON file"""
        result = enricher.load_json_file(Path(ConvertVars.OUTPUT_DIR + "/test.json"))

        self.assertEqual(result, {"key": "value"})
        mock_file.assert_called_once()

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_file_not_found(self, mock_file):
        """Test loading non-existent file"""
        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            result = enricher.load_json_file(Path(ConvertVars.OUTPUT_DIR + "/nonexistent.json"))

        self.assertEqual(result, {})
        self.assertIn("File not found", log.output[0])

    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    def test_load_invalid_json(self, mock_file):
        """Test loading file with invalid JSON"""
        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            result = enricher.load_json_file(Path(ConvertVars.OUTPUT_DIR + "/invalid.json"))

        self.assertEqual(result, {})
        self.assertIn("Error parsing JSON file", log.output[0])


class TestLoadYamlFile(unittest.TestCase):
    """Test load_yaml_file function"""

    @patch("builtins.open", new_callable=mock_open, read_data="1:\n  owasp_asvs:\n  - 1.2.3\n")
    @patch("yaml.safe_load")
    def test_load_valid_yaml(self, mock_yaml_load, mock_file):
        """Test loading a valid YAML file"""
        mock_yaml_load.return_value = {1: {"owasp_asvs": ["1.2.3"]}}

        result = enricher.load_yaml_file(Path(ConvertVars.OUTPUT_DIR + "/test.yaml"))

        # Should preserve integer keys
        self.assertIn(1, result)
        self.assertEqual(result[1]["owasp_asvs"], ["1.2.3"])
        mock_file.assert_called_once()
        mock_yaml_load.assert_called_once()

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_yaml_file_not_found(self, mock_file):
        """Test loading non-existent YAML file"""
        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            result = enricher.load_yaml_file(Path(ConvertVars.OUTPUT_DIR + "/nonexistent.yaml"))

        self.assertEqual(result, {})
        self.assertIn("File not found", log.output[0])


class TestSaveYamlFile(unittest.TestCase):
    """Test save_yaml_file function"""

    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.dump")
    def test_save_valid_yaml(self, mock_yaml_dump, mock_file):
        """Test saving a valid YAML file"""
        data = {1: {"name": "Test", "owasp_asvs": ["1.2.3"]}}

        result = enricher.save_yaml_file(Path(ConvertVars.OUTPUT_FILE), data)

        self.assertTrue(result)
        mock_file.assert_called_once()
        mock_yaml_dump.assert_called_once()

    @patch("builtins.open", side_effect=IOError("Write error"))
    def test_save_io_error(self, mock_file):
        """Test saving with IO error"""
        data = {1: {"name": "Test"}}

        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            result = enricher.save_yaml_file(Path(ConvertVars.OUTPUT_DIR + "/error.yaml"), data)

        self.assertFalse(result)
        self.assertIn("Error saving YAML file", log.output[0])


class TestParseArguments(unittest.TestCase):
    """Test parse_arguments function"""

    def test_parse_default_arguments(self):
        """Test parsing with no arguments (uses defaults)"""
        args = enricher.parse_arguments([])

        self.assertEqual(args.capec_json, enricher.EnricherVars.DEFAULT_CAPEC_JSON_PATH)
        self.assertEqual(args.source_dir, enricher.EnricherVars.DEFAULT_SOURCE_DIR)
        self.assertIsNone(args.input_path)
        self.assertIsNone(args.output_path)
        self.assertEqual(args.version, "latest")
        self.assertEqual(args.edition, "edition")
        self.assertFalse(args.debug)

    def test_parse_custom_capec_json(self):
        """Test parsing with custom CAPEC JSON path"""
        args = enricher.parse_arguments(["-c", "custom/3000.json"])

        self.assertEqual(args.capec_json, "custom/3000.json")

    def test_parse_custom_input_path(self):
        """Test parsing with custom input path"""
        args = enricher.parse_arguments(["-i", "custom/input.yaml"])

        self.assertEqual(args.input_path, "custom/input.yaml")

    def test_parse_version_and_edition(self):
        """Test parsing with version and edition"""
        args = enricher.parse_arguments(["-v", "3.0", "-e", "mobileapp"])

        self.assertEqual(args.version, "3.0")
        self.assertEqual(args.edition, "mobileapp")

    def test_parse_all_arguments(self):
        """Test parsing with all arguments"""
        args = enricher.parse_arguments(
            [
                "-c",
                "capec.json",
                "-i",
                "input.yaml",
                "-v",
                "latest",
                "-e",
                "edition",
                "-s",
                "source_dir",
                "-o",
                "output.yaml",
                "-d",
            ]
        )

        self.assertEqual(args.capec_json, "capec.json")
        self.assertEqual(args.input_path, "input.yaml")
        self.assertEqual(args.version, "latest")
        self.assertEqual(args.edition, "edition")
        self.assertEqual(args.source_dir, "source_dir")
        self.assertEqual(args.output_path, "output.yaml")
        self.assertTrue(args.debug)


class TestSetLogging(unittest.TestCase):
    """Test set_logging function"""

    def test_set_logging_info_level(self):
        """Test setting logging to INFO level"""
        enricher.enricher_vars.args = argparse.Namespace(debug=False)

        enricher.set_logging()

        self.assertEqual(logging.getLogger().level, logging.INFO)

    def test_set_logging_debug_level(self):
        """Test setting logging to DEBUG level"""
        enricher.enricher_vars.args = argparse.Namespace(debug=True)

        enricher.set_logging()

        self.assertEqual(logging.getLogger().level, logging.DEBUG)


class TestMainFunction(unittest.TestCase):
    """Test main function with mocked dependencies"""

    @patch("scripts.capec_map_enricher.save_yaml_file")
    @patch("scripts.capec_map_enricher.enrich_capec_mappings")
    @patch("scripts.capec_map_enricher.extract_capec_names")
    @patch("scripts.capec_map_enricher.load_yaml_file")
    @patch("scripts.capec_map_enricher.load_json_file")
    @patch("scripts.capec_map_enricher.parse_arguments")
    @patch("sys.exit")
    def test_main_successful_execution(
        self, mock_exit, mock_parse_args, mock_load_json, mock_load_yaml, mock_extract_names, mock_enrich, mock_save
    ):
        """Test successful main execution"""
        # Setup mocks
        mock_parse_args.return_value = argparse.Namespace(
            capec_json=Path("capec.json"),
            input_path=Path("input.yaml"),
            output_path=Path("output.yaml"),
            source_dir=Path("."),
            version="3.0",
            edition="webapp",
            debug=False,
        )
        mock_load_json.return_value = {"Attack_Pattern_Catalog": {}}
        mock_load_yaml.return_value = {1: {"owasp_asvs": ["1.2.3"]}}
        mock_extract_names.return_value = {1: "Test Attack"}
        mock_enrich.return_value = {1: {"name": "Test Attack", "owasp_asvs": ["1.2.3"]}}
        mock_save.return_value = True

        enricher.main()

        mock_load_json.assert_called_once()
        mock_load_yaml.assert_called_once()
        mock_extract_names.assert_called_once()
        mock_enrich.assert_called_once()
        mock_save.assert_called_once()
        mock_exit.assert_not_called()

    @patch("scripts.capec_map_enricher.load_json_file")
    @patch("scripts.capec_map_enricher.parse_arguments")
    @patch("sys.exit")
    def test_main_no_json_data_loaded(self, mock_exit, mock_parse_args, mock_load_json):
        """Test main with no JSON data loaded"""
        mock_parse_args.return_value = argparse.Namespace(
            capec_json=Path("capec.json"),
            input_path=Path("input.yaml"),
            output_path=Path("output.yaml"),
            source_dir=Path("."),
            version="3.0",
            edition="webapp",
            debug=False,
        )
        mock_load_json.return_value = {}

        with self.assertLogs(logging.getLogger(), logging.ERROR):
            enricher.main()

        mock_exit.assert_called_with(1)


if __name__ == "__main__":
    unittest.main()
