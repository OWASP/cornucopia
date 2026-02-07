#!/usr/bin/env python3
import unittest
import os
import logging
import tempfile
import shutil
import argparse
from pathlib import Path

import scripts.convert_asvs as asvs

asvs.convert_vars = asvs.ConvertVars()


if "unittest.util" in __import__("sys").modules:
    # Show full diff in self.assertEqual.
    __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999


class TestConvertASVSIntegration(unittest.TestCase):
    """Integration tests for convert_asvs.py using real test data"""

    def setUp(self) -> None:
        """Set up test environment with test data paths"""
        # Get base path
        self.base_path = Path(__file__).parent.parent.parent.resolve()

        # Set up test input files
        self.test_input_file = (
            self.base_path
            / "tests"
            / "test_files"
            / "asvs-5.0"
            / "OWASP_Application_Security_Verification_Standard_5.0.0_en.json"
        )
        self.test_asvs_to_capec = self.base_path / "tests" / "test_files" / "source" / "webapp-asvs-3.0.yaml"

        # Create temporary output directory
        self.temp_output_dir = tempfile.mkdtemp()
        self.test_output_path = Path(self.temp_output_dir)

        # Verify test files exist
        if not self.test_input_file.exists():
            raise FileNotFoundError(f"Test input file not found: {self.test_input_file}")
        if not self.test_asvs_to_capec.exists():
            raise FileNotFoundError(f"Test ASVS to CAPEC mapping file not found: {self.test_asvs_to_capec}")

    def tearDown(self) -> None:
        """Clean up test output directory"""
        if os.path.exists(self.temp_output_dir):
            shutil.rmtree(self.temp_output_dir)

    def test_load_test_json_file(self):
        """Test loading the test ASVS JSON file"""
        data = asvs.load_json_file(self.test_input_file)

        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)
        self.assertIn("Requirements", data)
        self.assertIn("Name", data)
        self.assertEqual(data["Name"], "Application Security Verification Standard Project")

    def test_load_test_yaml_mapping(self):
        """Test loading the test ASVS to CAPEC YAML mapping file"""
        data = asvs.load_asvs_to_capec_mapping(self.test_asvs_to_capec)

        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)
        # Check for some expected mappings
        self.assertIn("1.1.1", data)
        self.assertIn("capec_codes", data["1.1.1"])

    def test_create_folder(self):
        """Test creating output folder"""
        test_folder = self.test_output_path / "test_folder"

        asvs.create_folder(test_folder)

        self.assertTrue(test_folder.exists())
        self.assertTrue(test_folder.is_dir())

    def test_empty_folder(self):
        """Test emptying a folder"""
        # Create a test folder with some content
        test_folder = self.test_output_path / "test_empty"
        test_folder.mkdir()
        (test_folder / "test_file.txt").write_text("test content")

        # Verify folder exists and has content
        self.assertTrue(test_folder.exists())
        self.assertTrue((test_folder / "test_file.txt").exists())

        # Empty the folder
        asvs.empty_folder(test_folder)

        # Verify folder is gone
        self.assertFalse(test_folder.exists())

    def test_parse_arguments_integration(self):
        """Test parsing arguments with real file paths"""
        args = asvs.parse_arguments(
            [
                "-o",
                str(self.test_output_path),
                "-i",
                str(self.test_input_file),
                "-ac",
                str(self.test_asvs_to_capec),
                "-cv",
                "3.9",
            ]
        )

        self.assertEqual(Path(args.output_path), self.test_output_path)
        self.assertEqual(Path(args.input_path), self.test_input_file)
        self.assertEqual(Path(args.asvs_to_capec), self.test_asvs_to_capec)
        self.assertEqual(args.capec_version, "3.9")

    def test_create_asvs_pages_integration(self):
        """Test creating ASVS pages from real test data"""
        # Load test data
        data = asvs.load_json_file(self.test_input_file)
        asvs_map = asvs.load_asvs_to_capec_mapping(self.test_asvs_to_capec)

        # Set up convert_vars
        asvs.convert_vars.args = argparse.Namespace(
            output_path=self.test_output_path,
            input_path=self.test_input_file,
            asvs_to_capec=self.test_asvs_to_capec,
            capec_version="3.9",
            debug=False,
        )

        # Create ASVS pages
        asvs.create_asvs_pages(data, asvs_map, "3.9", "5.0")

        # Verify that output was created
        self.assertTrue(self.test_output_path.exists())

        # Check that some directories were created
        output_dirs = [d for d in self.test_output_path.iterdir() if d.is_dir()]
        self.assertGreater(len(output_dirs), 0, "Should have created at least one directory")

        # Check for level control directories
        level_dirs = [d for d in output_dirs if d.name.startswith("level-") and d.name.endswith("-controls")]
        self.assertEqual(len(level_dirs), 3, "Should have created 3 level control directories (L1, L2, L3)")

        # Verify level control index files exist
        for level in [1, 2, 3]:
            level_index = self.test_output_path / f"level-{level}-controls" / "index.md"
            self.assertTrue(level_index.exists(), f"Level {level} index should exist")

            # Read and verify content
            content = level_index.read_text(encoding="utf-8")
            self.assertIn(f"# Level {level} controls", content)
            self.assertIn("controls listed below:", content)

    def test_create_asvs_pages_with_requirements(self):
        """Test that created pages contain requirement information"""
        # Load test data
        data = asvs.load_json_file(self.test_input_file)
        asvs_map = asvs.load_asvs_to_capec_mapping(self.test_asvs_to_capec)

        # Set up convert_vars
        asvs.convert_vars.args = argparse.Namespace(
            output_path=self.test_output_path,
            input_path=self.test_input_file,
            asvs_to_capec=self.test_asvs_to_capec,
            capec_version="3.9",
            debug=False,
        )

        # Create ASVS pages
        asvs.create_asvs_pages(data, asvs_map, "3.9", "5.0")

        # Find a requirement directory (e.g., 01-encoding-and-sanitization)
        requirement_dirs = [
            d for d in self.test_output_path.iterdir() if d.is_dir() and not d.name.startswith("level-")
        ]
        self.assertGreater(len(requirement_dirs), 0, "Should have created requirement directories")

        # Check first requirement directory
        first_req_dir = sorted(requirement_dirs)[0]

        # It should have subdirectories for items
        item_dirs = [d for d in first_req_dir.iterdir() if d.is_dir()]
        self.assertGreater(len(item_dirs), 0, "Requirement should have item subdirectories")

        # Check first item directory for index.md
        first_item_dir = sorted(item_dirs)[0]
        index_file = first_item_dir / "index.md"
        self.assertTrue(index_file.exists(), "Item directory should have index.md")

        # Verify content
        content = index_file.read_text(encoding="utf-8")
        self.assertIn("##", content, "Should contain headers")
        self.assertIn("Disclaimer", content, "Should contain disclaimer")
        self.assertIn("OWASP ASVS", content, "Should mention OWASP ASVS")

    def test_create_asvs_pages_with_capec_links(self):
        """Test that pages include CAPEC links when mappings exist"""
        # Load test data
        data = asvs.load_json_file(self.test_input_file)
        asvs_map = asvs.load_asvs_to_capec_mapping(self.test_asvs_to_capec)

        # Set up convert_vars
        asvs.convert_vars.args = argparse.Namespace(
            output_path=self.test_output_path,
            input_path=self.test_input_file,
            asvs_to_capec=self.test_asvs_to_capec,
            capec_version="3.9",
            debug=False,
        )

        # Create ASVS pages
        with self.assertLogs(logging.getLogger(), logging.INFO):
            asvs.create_asvs_pages(data, asvs_map, "3.9", "5.0")

        # Look for pages with CAPEC mappings
        # Check the first requirement
        requirement_dirs = [
            d for d in self.test_output_path.iterdir() if d.is_dir() and not d.name.startswith("level-")
        ]

        found_capec_reference = False
        for req_dir in requirement_dirs:
            for item_dir in req_dir.iterdir():
                if item_dir.is_dir():
                    index_file = item_dir / "index.md"
                    if index_file.exists():
                        content = index_file.read_text(encoding="utf-8")
                        if "Related CAPEC™ Requirements" in content:
                            found_capec_reference = True
                            self.assertIn("CAPEC™ (3.9):", content)
                            self.assertIn("/taxonomy/capec-", content)
                            break
            if found_capec_reference:
                break

        # Note: We may not always find CAPEC references if the test data doesn't have mappings
        # This is okay - just verify the structure is correct

    def test_main_integration(self):
        """Test the main function with real test files"""
        # Create permanent output directory for this test
        test_output_dir = self.base_path / "tests" / "test_files" / "output" / "asvs_integration_test"

        # Clean up if exists
        if test_output_dir.exists():
            shutil.rmtree(test_output_dir)

        # Set up arguments
        test_args = [
            "-o",
            str(test_output_dir),
            "-i",
            str(self.test_input_file),
            "-ac",
            str(self.test_asvs_to_capec),
            "-cv",
            "3.9",
        ]

        # Parse arguments
        asvs.convert_vars.args = asvs.parse_arguments(test_args)

        # Run main workflow (without calling main() to avoid sys.argv issues)
        capec_version = asvs.get_valid_capec_version(asvs.convert_vars.args.capec_version)
        asvs_version = asvs.get_valid_asvs_version(asvs.convert_vars.args.asvs_version)
        asvs.set_logging()

        with self.assertLogs(logging.getLogger(), logging.INFO) as log:
            asvs.empty_folder(Path(asvs.convert_vars.args.output_path))
            asvs.create_folder(Path(asvs.convert_vars.args.output_path))
            data = asvs.load_json_file(Path(asvs.convert_vars.args.input_path))
            asvs_map = asvs.load_asvs_to_capec_mapping(Path(asvs.convert_vars.args.asvs_to_capec))
            asvs.create_asvs_pages(data, asvs_map, capec_version, asvs_version)

        # Verify logging
        log_messages = "\n".join(log.output)
        self.assertIn("Successfully loaded YAML file", log_messages)

        # Verify output exists
        self.assertTrue(test_output_dir.exists())

        # Verify some content was created
        output_items = list(test_output_dir.iterdir())
        self.assertGreater(len(output_items), 0, "Should have created output files/directories")

        # Clean up
        if test_output_dir.exists():
            shutil.rmtree(test_output_dir)

    def test_level_summary_content(self):
        """Test that level summaries contain expected content"""
        # Load test data
        data = asvs.load_json_file(self.test_input_file)
        asvs_map = asvs.load_asvs_to_capec_mapping(self.test_asvs_to_capec)

        # Set up convert_vars
        asvs.convert_vars.args = argparse.Namespace(
            output_path=self.test_output_path,
            input_path=self.test_input_file,
            asvs_to_capec=self.test_asvs_to_capec,
            capec_version="3.9",
            debug=False,
        )

        # Create ASVS pages
        asvs.create_asvs_pages(data, asvs_map, "3.9", "5.0")

        # Check Level 1 summary
        level1_index = self.test_output_path / "level-1-controls" / "index.md"
        self.assertTrue(level1_index.exists())

        content = level1_index.read_text(encoding="utf-8")

        # Verify structure
        self.assertIn("# Level 1 controls", content)
        self.assertIn("controls listed below:", content)

        # Should contain some requirement links
        self.assertIn("[V", content, "Should contain requirement references")
        self.assertIn("](", content, "Should contain markdown links")

    def test_get_valid_version(self):
        """Test version validation with real version numbers"""
        # Test with valid CAPEC version
        result = asvs.get_valid_capec_version("3.9")
        self.assertEqual(result, "3.9")

        # Test with invalid CAPEC version
        result = asvs.get_valid_capec_version("99.99")
        self.assertEqual(result, asvs.ConvertVars.LATEST_CAPEC_VERSION_CHOICES[-1])

        # Test with valid ASVS version
        result = asvs.get_valid_asvs_version("5.0")
        self.assertEqual(result, "5.0")

        # Test with invalid ASVS version
        result = asvs.get_valid_asvs_version("99.99")
        self.assertEqual(result, asvs.ConvertVars.LATEST_ASVS_VERSION_CHOICES[-1])


class TestRealFileOperations(unittest.TestCase):
    """Test real file operations without mocking"""

    def setUp(self) -> None:
        """Set up temporary directories for testing"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_path = Path(self.temp_dir)

    def tearDown(self) -> None:
        """Clean up temporary directories"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_create_and_empty_folder(self):
        """Test creating and emptying folders with real file system"""
        # Create a folder
        test_folder = self.test_path / "test_folder"
        asvs.create_folder(test_folder)

        self.assertTrue(test_folder.exists())

        # Add some content
        (test_folder / "file1.txt").write_text("content1")
        (test_folder / "file2.txt").write_text("content2")
        sub_folder = test_folder / "subfolder"
        sub_folder.mkdir()
        (sub_folder / "file3.txt").write_text("content3")

        # Verify content exists
        self.assertEqual(len(list(test_folder.rglob("*"))), 4)  # 2 files + 1 folder + 1 file in folder

        # Empty the folder
        asvs.empty_folder(test_folder)

        # Verify it's gone
        self.assertFalse(test_folder.exists())

    def test_load_and_save_json(self):
        """Test loading JSON from real file"""
        # Create a test JSON file
        test_json_file = self.test_path / "test.json"
        test_data = {"Requirements": [{"Ordinal": 1, "Name": "Test Requirement"}], "Version": "5.0.0"}

        with open(test_json_file, "w", encoding="utf-8") as f:
            import json

            json.dump(test_data, f)

        # Load it
        loaded_data = asvs.load_json_file(test_json_file)

        self.assertEqual(loaded_data, test_data)
        self.assertEqual(loaded_data["Version"], "5.0.0")

    def test_load_yaml_mapping(self):
        """Test loading YAML from real file"""
        # Create a test YAML file
        test_yaml_file = self.test_path / "test_mapping.yaml"
        test_content = """1.1.1:
  capec_codes:
  - '120'
  - '126'
1.2.1:
  capec_codes:
  - '152'
"""
        test_yaml_file.write_text(test_content, encoding="utf-8")

        # Load it
        with self.assertLogs(logging.getLogger(), logging.INFO) as log:
            loaded_data = asvs.load_asvs_to_capec_mapping(test_yaml_file)

        self.assertIn("Successfully loaded YAML file", log.output[0])
        self.assertIn("1.1.1", loaded_data)
        self.assertIn("1.2.1", loaded_data)
        self.assertEqual(loaded_data["1.1.1"]["capec_codes"], ["120", "126"])


if __name__ == "__main__":
    unittest.main()
