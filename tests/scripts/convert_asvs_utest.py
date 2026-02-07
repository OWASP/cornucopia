#!/usr/bin/env python3
import unittest
from unittest.mock import patch, mock_open
import argparse
import logging
from pathlib import Path

import scripts.convert_asvs as asvs

asvs.convert_vars = asvs.ConvertVars()


if "unittest.util" in __import__("sys").modules:
    # Show full diff in self.assertEqual.
    __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999


class TestCreateLevelSummary(unittest.TestCase):
    """Test create_level_summary function"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_output_path = Path("/fake/output")
        asvs.convert_vars.args = argparse.Namespace(output_path=self.mock_output_path)

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.mkdir")
    def test_create_level_summary_level_1(self, mock_mkdir, mock_file):
        """Test creating level 1 summary with multiple controls"""
        test_arr = [
            {
                "topic": "01-encoding-and-sanitization",
                "cat": "01-encoding-and-sanitization-architecture",
                "name": "V1.1.1",
                "link": "/taxonomy/asvs-4.0.3/01-encoding/01-architecture#V1.1.1",
                "description": "Verify that input is decoded or unescaped into a canonical form",
            },
            {
                "topic": "01-encoding-and-sanitization",
                "cat": "02-injection-prevention",
                "name": "V1.2.1",
                "link": "/taxonomy/asvs-4.0.3/01-encoding/02-injection#V1.2.1",
                "description": "Verify that output encoding for an HTTP response is relevant",
            },
        ]

        asvs.create_level_summary(1, test_arr)

        # Verify directory was created
        mock_mkdir.assert_called_once_with(self.mock_output_path / "level-1-controls")

        # Verify file was opened for writing
        mock_file.assert_called_once_with(self.mock_output_path / "level-1-controls/index.md", "w", encoding="utf-8")

        # Get the file handle
        handle = mock_file()

        # Verify content was written
        write_calls = [call_args[0][0] for call_args in handle.write.call_args_list]
        content = "".join(write_calls)

        self.assertIn("# Level 1 controls", content)
        self.assertIn("Level 1 contains 2 controls listed below:", content)
        self.assertIn("## 01-encoding-and-sanitization", content)
        self.assertIn("### 01-encoding-and-sanitization-architecture", content)
        self.assertIn("### 02-injection-prevention", content)
        self.assertIn("[V1.1.1]", content)
        self.assertIn("[V1.2.1]", content)

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.mkdir")
    def test_create_level_summary_empty_array(self, mock_mkdir, mock_file):
        """Test creating level summary with empty array"""
        asvs.create_level_summary(2, [])

        mock_mkdir.assert_called_once_with(self.mock_output_path / "level-2-controls")

        handle = mock_file()
        write_calls = [call_args[0][0] for call_args in handle.write.call_args_list]
        content = "".join(write_calls)

        self.assertIn("# Level 2 controls", content)
        self.assertIn("Level 2 contains 0 controls listed below:", content)


class TestHasNoCapecMapping(unittest.TestCase):
    """Test has_no_capec_mapping function"""

    def test_has_no_capec_mapping_with_valid_mapping(self):
        """Test when ASVS ID has valid CAPEC mapping"""
        asvs_map = {"1.1.1": {"capec_codes": ["120", "126", "152"]}}
        result = asvs.has_no_capec_mapping("1.1.1", asvs_map)
        self.assertFalse(result)

    def test_has_no_capec_mapping_with_empty_codes(self):
        """Test when ASVS ID has empty capec_codes"""
        asvs_map = {"1.1.1": {"capec_codes": []}}
        result = asvs.has_no_capec_mapping("1.1.1", asvs_map)
        self.assertTrue(result)

    def test_has_no_capec_mapping_with_missing_id(self):
        """Test when ASVS ID is not in map"""
        asvs_map = {"1.1.1": {"capec_codes": ["120"]}}
        result = asvs.has_no_capec_mapping("2.2.2", asvs_map)
        self.assertTrue(result)

    def test_has_no_capec_mapping_with_no_capec_codes_key(self):
        """Test when mapping exists but has no capec_codes key"""
        asvs_map = {"1.1.1": {"other_key": "value"}}  # type: ignore[dict-item]
        result = asvs.has_no_capec_mapping("1.1.1", asvs_map)
        self.assertTrue(result)

    def test_has_no_capec_mapping_with_none_value(self):
        """Test when capec_codes is None"""
        asvs_map = {"1.1.1": {"capec_codes": None}}  # type: ignore[dict-item]
        result = asvs.has_no_capec_mapping("1.1.1", asvs_map)
        self.assertTrue(result)


class TestCreateLinkList(unittest.TestCase):
    """Test create_link_list function"""

    def test_create_link_list_multiple_codes(self):
        """Test creating link list with multiple CAPEC codes"""
        requirements = {"capec_codes": ["120", "126", "152"]}
        result = asvs.create_link_list(requirements, "3.9")

        expected = (
            "[120](/taxonomy/capec-3.9/120/index.md), "
            "[126](/taxonomy/capec-3.9/126/index.md), "
            "[152](/taxonomy/capec-3.9/152/index.md)"
        )
        self.assertEqual(result, expected)

    def test_create_link_list_single_code(self):
        """Test creating link list with single CAPEC code"""
        requirements = {"capec_codes": ["120"]}
        result = asvs.create_link_list(requirements, "3.9")

        expected = "[120](/taxonomy/capec-3.9/120/index.md)"
        self.assertEqual(result, expected)

    def test_create_link_list_empty_codes(self):
        """Test creating link list with empty capec_codes"""
        requirements = {"capec_codes": []}
        result = asvs.create_link_list(requirements, "3.9")

        self.assertEqual(result, "")

    def test_create_link_list_no_capec_codes_key(self):
        """Test creating link list when capec_codes key is missing"""
        requirements = {"other_key": "value"}
        result = asvs.create_link_list(requirements, "3.9")

        self.assertEqual(result, "")

    def test_create_link_list_sorted(self):
        """Test that CAPEC codes are sorted"""
        requirements = {"capec_codes": ["152", "120", "126"]}
        result = asvs.create_link_list(requirements, "3.9")

        expected = (
            "[120](/taxonomy/capec-3.9/120/index.md), "
            "[126](/taxonomy/capec-3.9/126/index.md), [152](/taxonomy/capec-3.9/152/index.md)"
        )
        self.assertEqual(result, expected)


class TestParseArguments(unittest.TestCase):
    """Test parse_arguments function"""

    def test_parse_arguments_with_defaults(self):
        """Test parsing arguments with default values"""
        args = asvs.parse_arguments([])

        self.assertEqual(Path(args.output_path), asvs.ConvertVars.DEFAULT_OUTPUT_PATH)
        self.assertEqual(Path(args.input_path), asvs.ConvertVars.DEFAULT_INPUT_PATH)
        self.assertEqual(Path(args.asvs_to_capec), asvs.ConvertVars.DEFAULT_ASVS_TO_CAPEC_INPUT_PATH)
        self.assertEqual(args.capec_version, "3.9")
        self.assertFalse(args.debug)

    def test_parse_arguments_with_custom_values(self):
        """Test parsing arguments with custom values"""
        test_args = [
            "-o",
            "/custom/output",
            "-i",
            "/custom/input.json",
            "-ac",
            "/custom/mapping.yaml",
            "-cv",
            "4.0",
            "-d",
        ]

        args = asvs.parse_arguments(test_args)

        self.assertEqual(Path(args.output_path), Path("/custom/output"))
        self.assertEqual(Path(args.input_path), Path("/custom/input.json"))
        self.assertEqual(Path(args.asvs_to_capec), Path("/custom/mapping.yaml"))
        self.assertEqual(args.capec_version, "4.0")
        self.assertTrue(args.debug)

    def test_parse_arguments_long_form(self):
        """Test parsing arguments with long form flags"""
        test_args = [
            "--output-path",
            "/custom/output",
            "--input-path",
            "/custom/input.json",
            "--asvs-to-capec",
            "/custom/mapping.yaml",
            "--capec-version",
            "4.0",
            "--debug",
        ]

        args = asvs.parse_arguments(test_args)

        self.assertEqual(Path(args.output_path), Path("/custom/output"))
        self.assertEqual(Path(args.input_path), Path("/custom/input.json"))
        self.assertEqual(Path(args.asvs_to_capec), Path("/custom/mapping.yaml"))
        self.assertEqual(args.capec_version, "4.0")
        self.assertTrue(args.debug)


class TestGetValidVersion(unittest.TestCase):
    """Test get_valid_version function"""

    def test_get_valid_version_with_valid_version(self):
        """Test getting valid version when version is in choices"""
        result = asvs.get_valid_version("3.9")
        self.assertEqual(result, "3.9")

    def test_get_valid_version_with_invalid_version(self):
        """Test getting valid version when version is not in choices"""
        result = asvs.get_valid_version("invalid")
        # Should return the last choice
        self.assertEqual(result, asvs.ConvertVars.LATEST_ASVS_VERSION_CHOICES[-1])

    def test_get_valid_version_with_empty_string(self):
        """Test getting valid version with empty string"""
        result = asvs.get_valid_version("")
        self.assertEqual(result, asvs.ConvertVars.LATEST_ASVS_VERSION_CHOICES[-1])


class TestSetLogging(unittest.TestCase):
    """Test set_logging function"""

    def setUp(self):
        """Reset logging configuration"""
        # Store original level
        self.original_level = logging.getLogger().level

    def tearDown(self):
        """Restore logging configuration"""
        logging.getLogger().setLevel(self.original_level)

    def test_set_logging_debug_mode(self):
        """Test setting logging to DEBUG level"""
        asvs.convert_vars.args = argparse.Namespace(debug=True)
        asvs.set_logging()

        self.assertEqual(logging.getLogger().level, logging.DEBUG)

    def test_set_logging_info_mode(self):
        """Test setting logging to INFO level"""
        asvs.convert_vars.args = argparse.Namespace(debug=False)
        asvs.set_logging()

        self.assertEqual(logging.getLogger().level, logging.INFO)


class TestEmptyFolder(unittest.TestCase):
    """Test empty_folder function"""

    @patch("shutil.rmtree")
    def test_empty_folder_success(self, mock_rmtree):
        """Test successfully emptying a folder"""
        test_path = Path("/test/path")

        asvs.empty_folder(test_path)

        mock_rmtree.assert_called_once_with(test_path)

    @patch("shutil.rmtree", side_effect=Exception("Test error"))
    def test_empty_folder_with_error(self, mock_rmtree):
        """Test emptying folder when error occurs"""
        test_path = Path("/test/path")

        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            asvs.empty_folder(test_path)

        self.assertIn("Error while emptying folder", log.output[0])
        self.assertIn("Test error", log.output[0])


class TestCreateFolder(unittest.TestCase):
    """Test create_folder function"""

    @patch("os.makedirs")
    def test_create_folder_success(self, mock_makedirs):
        """Test successfully creating a folder"""
        test_path = Path("/test/path")

        asvs.create_folder(test_path)

        mock_makedirs.assert_called_once_with(test_path, exist_ok=True)

    @patch("os.makedirs", side_effect=Exception("Test error"))
    def test_create_folder_with_error(self, mock_makedirs):
        """Test creating folder when error occurs"""
        test_path = Path("/test/path")

        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            asvs.create_folder(test_path)

        self.assertIn("Error while creating folder", log.output[0])
        self.assertIn("Test error", log.output[0])


class TestLoadJsonFile(unittest.TestCase):
    """Test load_json_file function"""

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_load_json_file_success(self, mock_file):
        """Test successfully loading JSON file"""
        test_path = Path("/test/file.json")

        result = asvs.load_json_file(test_path)

        mock_file.assert_called_once_with(test_path, encoding="utf8")
        self.assertEqual(result, {"key": "value"})

    @patch("builtins.open", side_effect=Exception("File not found"))
    def test_load_json_file_with_error(self, mock_file):
        """Test loading JSON file when error occurs"""
        test_path = Path("/test/file.json")

        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            result = asvs.load_json_file(test_path)

        self.assertEqual(result, {})
        self.assertIn("Error while loading JSON file", log.output[0])

    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    def test_load_json_file_with_invalid_json(self, mock_file):
        """Test loading JSON file with invalid JSON content"""
        test_path = Path("/test/file.json")

        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            result = asvs.load_json_file(test_path)

        self.assertEqual(result, {})
        self.assertIn("Error while loading JSON file", log.output[0])


class TestLoadAsvsToCapecMapping(unittest.TestCase):
    """Test load_asvs_to_capec_mapping function"""

    @patch("builtins.open", new_callable=mock_open, read_data='1.1.1:\n  capec_codes:\n  - "120"\n  - "126"')
    @patch("yaml.safe_load")
    def test_load_asvs_to_capec_mapping_success(self, mock_yaml_load, mock_file):
        """Test successfully loading YAML mapping file"""
        test_path = Path("/test/mapping.yaml")
        test_data = {"1.1.1": {"capec_codes": ["120", "126"]}}
        mock_yaml_load.return_value = test_data

        with self.assertLogs(logging.getLogger(), logging.INFO) as log:
            result = asvs.load_asvs_to_capec_mapping(test_path)

        mock_file.assert_called_once_with(test_path, "r", encoding="utf-8")
        self.assertEqual(result, test_data)
        self.assertIn("Successfully loaded YAML file", log.output[0])

    @patch("builtins.open", side_effect=Exception("File not found"))
    def test_load_asvs_to_capec_mapping_with_error(self, mock_file):
        """Test loading YAML mapping file when error occurs"""
        test_path = Path("/test/mapping.yaml")

        with self.assertLogs(logging.getLogger(), logging.ERROR) as log:
            result = asvs.load_asvs_to_capec_mapping(test_path)

        self.assertEqual(result, {})
        self.assertIn("Error loading YAML file", log.output[0])


class TestFormatDirectoryName(unittest.TestCase):
    """Test _format_directory_name helper function"""

    def test_format_directory_name_single_digit(self):
        """Test formatting with single digit ordinal"""
        result = asvs._format_directory_name(1, "Encoding and Sanitization")
        self.assertEqual(result, "01-encoding-and-sanitization")

    def test_format_directory_name_double_digit(self):
        """Test formatting with double digit ordinal"""
        result = asvs._format_directory_name(10, "Validation and Business Logic")
        self.assertEqual(result, "10-validation-and-business-logic")

    def test_format_directory_name_with_commas(self):
        """Test formatting with commas in name"""
        result = asvs._format_directory_name(3, "Web Frontend Security, Testing")
        self.assertEqual(result, "03-web-frontend-security-testing")


class TestGetLevelRequirementText(unittest.TestCase):
    """Test _get_level_requirement_text helper function"""

    def test_get_level_requirement_text_level_1(self):
        """Test getting text for level 1"""
        result = asvs._get_level_requirement_text(1)
        self.assertEqual(result, "Required for Level 1, 2 and 3\n\n")

    def test_get_level_requirement_text_level_2(self):
        """Test getting text for level 2"""
        result = asvs._get_level_requirement_text(2)
        self.assertEqual(result, "Required for Level 2 and 3\n\n")

    def test_get_level_requirement_text_level_3(self):
        """Test getting text for level 3"""
        result = asvs._get_level_requirement_text(3)
        self.assertEqual(result, "Required for Level 3\n\n")

    def test_get_level_requirement_text_invalid_level(self):
        """Test getting text for invalid level"""
        result = asvs._get_level_requirement_text(99)
        self.assertEqual(result, "")


class TestWriteDisclaimer(unittest.TestCase):
    """Test _write_disclaimer helper function"""

    @patch("builtins.open", new_callable=mock_open)
    def test_write_disclaimer(self, mock_file):
        """Test writing disclaimer to file"""
        handle = mock_file()
        asvs._write_disclaimer(handle)

        write_calls = [call_args[0][0] for call_args in handle.write.call_args_list]
        content = "".join(write_calls)

        self.assertIn("## Disclaimer", content)
        self.assertIn("OWASP ASVS", content)
        self.assertIn("Creative Commons Attribution-Share Alike v4.0", content)


class TestCreateLevelObj(unittest.TestCase):
    """Test _create_level_obj helper function"""

    def test_create_level_obj(self):
        """Test creating level object"""
        subitem = {
            "Shortcode": "V1.1.1",
            "Description": "Verify that input is decoded",
            "L": "1",
        }

        result = asvs._create_level_obj(subitem, "01-encoding", "01-architecture")

        self.assertEqual(result["topic"], "01-encoding")
        self.assertEqual(result["cat"], "01-architecture")
        self.assertEqual(result["name"], "V1.1.1")
        self.assertEqual(result["link"], "/taxonomy/asvs-4.0.3/01-encoding/01-architecture#V1.1.1")
        self.assertEqual(result["description"], "Verify that input is decoded")


class TestCategorizeByLevel(unittest.TestCase):
    """Test _categorize_by_level helper function"""

    def test_categorize_by_level_1(self):
        """Test categorizing level 1 requirement"""
        L1, L2, L3 = [], [], []
        subitem = {"Shortcode": "V1.1.1", "Description": "Test", "L": "1"}

        asvs._categorize_by_level(subitem, "01-encoding", "01-arch", L1, L2, L3)

        self.assertEqual(len(L1), 1)
        self.assertEqual(len(L2), 0)
        self.assertEqual(len(L3), 0)

    def test_categorize_by_level_2(self):
        """Test categorizing level 2 requirement"""
        L1, L2, L3 = [], [], []
        subitem = {"Shortcode": "V1.1.2", "Description": "Test", "L": "2"}

        asvs._categorize_by_level(subitem, "01-encoding", "01-arch", L1, L2, L3)

        self.assertEqual(len(L1), 0)
        self.assertEqual(len(L2), 1)
        self.assertEqual(len(L3), 0)

    def test_categorize_by_level_3(self):
        """Test categorizing level 3 requirement"""
        L1, L2, L3 = [], [], []
        subitem = {"Shortcode": "V1.1.3", "Description": "Test", "L": "3"}

        asvs._categorize_by_level(subitem, "01-encoding", "01-arch", L1, L2, L3)

        self.assertEqual(len(L1), 0)
        self.assertEqual(len(L2), 0)
        self.assertEqual(len(L3), 1)


class TestWriteSubitemContent(unittest.TestCase):
    """Test _write_subitem_content helper function"""

    @patch("builtins.open", new_callable=mock_open)
    def test_write_subitem_content_with_capec(self, mock_file):
        """Test writing subitem with CAPEC mapping"""
        handle = mock_file()
        subitem = {
            "Shortcode": "V1.1.1",
            "Description": "Verify that input is decoded",
            "L": "1",
        }
        asvs_map = {"1.1.1": {"capec_codes": ["120", "126"]}}

        asvs._write_subitem_content(handle, subitem, asvs_map, "3.9")

        write_calls = [call_args[0][0] for call_args in handle.write.call_args_list]
        content = "".join(write_calls)

        self.assertIn("## V1.1.1", content)
        self.assertIn("Verify that input is decoded", content)
        self.assertIn("Required for Level 1, 2 and 3", content)
        self.assertIn("Related CAPEC™ Requirements", content)

    @patch("builtins.open", new_callable=mock_open)
    def test_write_subitem_content_without_capec(self, mock_file):
        """Test writing subitem without CAPEC mapping"""
        handle = mock_file()
        subitem = {
            "Shortcode": "V1.1.1",
            "Description": "Verify that input is decoded",
            "L": "2",
        }

        with self.assertLogs(logging.getLogger(), logging.INFO) as log:
            asvs._write_subitem_content(handle, subitem, {}, "3.9")

        write_calls = [call_args[0][0] for call_args in handle.write.call_args_list]
        content = "".join(write_calls)

        self.assertIn("## V1.1.1", content)
        self.assertIn("Required for Level 2 and 3", content)
        self.assertNotIn("Related CAPEC™ Requirements", content)
        self.assertIn("has no CAPEC mapping", log.output[0])


class TestProcessRequirementItem(unittest.TestCase):
    """Test _process_requirement_item helper function"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_output_path = Path("/fake/output")
        asvs.convert_vars.args = argparse.Namespace(output_path=self.mock_output_path)

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.mkdir")
    def test_process_requirement_item(self, mock_mkdir, mock_file):
        """Test processing a requirement item"""
        item = {
            "Ordinal": 1,
            "Name": "Architecture",
            "Items": [{"Shortcode": "V1.1.1", "Description": "Test requirement", "L": "1"}],
        }
        L1, L2, L3 = [], [], []

        asvs._process_requirement_item(item, "01-encoding", {}, "3.9", L1, L2, L3)

        # Verify directory was created
        mock_mkdir.assert_called_once()

        # Verify file operations
        mock_file.assert_called_once()

        # Verify categorization
        self.assertEqual(len(L1), 1)


class TestCreateAsvsPages(unittest.TestCase):
    """Test create_asvs_pages function"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_output_path = Path("/fake/output")
        asvs.convert_vars.args = argparse.Namespace(output_path=self.mock_output_path)

        self.test_data = {
            "Requirements": [
                {
                    "Ordinal": 1,
                    "Name": "Encoding and Sanitization",
                    "Items": [
                        {
                            "Ordinal": 1,
                            "Name": "Encoding and Sanitization Architecture",
                            "Items": [
                                {
                                    "Shortcode": "V1.1.1",
                                    "Description": "Verify that input is decoded",
                                    "L": "1",
                                }
                            ],
                        }
                    ],
                }
            ]
        }

        self.test_asvs_map = {"1.1.1": {"capec_codes": ["120", "126"]}}

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.mkdir")
    def test_create_asvs_pages_basic(self, mock_mkdir, mock_file):
        """Test creating ASVS pages with basic data"""
        asvs.create_asvs_pages(self.test_data, self.test_asvs_map, "3.9")

        # Verify directories were created
        self.assertGreater(mock_mkdir.call_count, 0)

        # Verify files were created
        self.assertGreater(mock_file.call_count, 0)

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.mkdir")
    def test_create_asvs_pages_with_multiple_levels(self, mock_mkdir, mock_file):
        """Test creating ASVS pages with multiple levels"""
        multi_level_data = {
            "Requirements": [
                {
                    "Ordinal": 1,
                    "Name": "Encoding and Sanitization",
                    "Items": [
                        {
                            "Ordinal": 1,
                            "Name": "Encoding Architecture",
                            "Items": [
                                {
                                    "Shortcode": "V1.1.1",
                                    "Description": "Verify L1 requirement",
                                    "L": "1",
                                },
                                {
                                    "Shortcode": "V1.1.2",
                                    "Description": "Verify L2 requirement",
                                    "L": "2",
                                },
                                {
                                    "Shortcode": "V1.1.3",
                                    "Description": "Verify L3 requirement",
                                    "L": "3",
                                },
                            ],
                        }
                    ],
                }
            ]
        }

        asvs.create_asvs_pages(multi_level_data, {}, "3.9")

        # Verify that level summary files were created for all levels
        # Check that level-1-controls, level-2-controls, level-3-controls directories were created
        mkdir_calls = [str(call_args[0][0]) for call_args in mock_mkdir.call_args_list]

        # Should include level control directories
        level_dirs = [call for call in mkdir_calls if "level-" in str(call) and "-controls" in str(call)]
        self.assertEqual(len(level_dirs), 3)  # L1, L2, L3

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.mkdir")
    def test_create_asvs_pages_with_capec_mapping(self, mock_mkdir, mock_file):
        """Test creating ASVS pages with CAPEC mapping"""
        asvs.create_asvs_pages(self.test_data, self.test_asvs_map, "3.9")

        handle = mock_file()
        write_calls = [call_args[0][0] for call_args in handle.write.call_args_list]
        content = "".join(write_calls)

        # Verify CAPEC mapping is included
        self.assertIn("Related CAPEC™ Requirements", content)
        self.assertIn("CAPEC™ (3.9):", content)

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.mkdir")
    def test_create_asvs_pages_without_capec_mapping(self, mock_mkdir, mock_file):
        """Test creating ASVS pages without CAPEC mapping"""
        with self.assertLogs(logging.getLogger(), logging.INFO) as log:
            asvs.create_asvs_pages(self.test_data, {}, "3.9")

        # Verify log message about missing mapping
        log_messages = "\n".join(log.output)
        self.assertIn("has no CAPEC mapping", log_messages)


class TestMain(unittest.TestCase):
    """Test main function"""

    @patch("scripts.convert_asvs.create_asvs_pages")
    @patch("scripts.convert_asvs.load_asvs_to_capec_mapping")
    @patch("scripts.convert_asvs.load_json_file")
    @patch("scripts.convert_asvs.create_folder")
    @patch("scripts.convert_asvs.empty_folder")
    @patch("scripts.convert_asvs.set_logging")
    @patch("scripts.convert_asvs.parse_arguments")
    def test_main_success(
        self,
        mock_parse_args,
        mock_set_logging,
        mock_empty_folder,
        mock_create_folder,
        mock_load_json,
        mock_load_yaml,
        mock_create_pages,
    ):
        """Test main function execution"""
        # Set up mocks
        mock_args = argparse.Namespace(
            output_path=Path("/test/output"),
            input_path=Path("/test/input.json"),
            asvs_to_capec=Path("/test/mapping.yaml"),
            capec_version="3.9",
            debug=False,
        )
        mock_parse_args.return_value = mock_args

        mock_load_json.return_value = {"Requirements": []}
        mock_load_yaml.return_value = {}

        with self.assertLogs(logging.getLogger(), logging.INFO) as log:
            asvs.main()

        # Verify function calls
        mock_parse_args.assert_called_once()
        mock_set_logging.assert_called_once()
        mock_empty_folder.assert_called_once_with(Path("/test/output"))
        mock_create_folder.assert_called_once_with(Path("/test/output"))
        mock_load_json.assert_called_once_with(Path("/test/input.json"))
        mock_load_yaml.assert_called_once_with(Path("/test/mapping.yaml"))
        mock_create_pages.assert_called_once()

        # Verify logging
        log_messages = "\n".join(log.output)
        self.assertIn("Starting ASVS conversion process", log_messages)
        self.assertIn("ASVS conversion process completed", log_messages)


if __name__ == "__main__":
    unittest.main()
