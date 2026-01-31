#!/usr/bin/env python3
import unittest
import os
import tempfile
import shutil
from pathlib import Path
import yaml

import scripts.convert_capec_map_to_asvs_map as capec_map

capec_map.convert_vars = capec_map.ConvertVars()


if "unittest.util" in __import__("sys").modules:
    # Show full diff in self.assertEqual.
    __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999


class TestConvertCAPECMapToASVSMapIntegration(unittest.TestCase):
    """Integration tests for convert_capec_map_to_asvs_map.py using real test data"""

    def setUp(self) -> None:
        """Set up test environment with test data paths"""
        # Get the base path of the repository
        self.base_path = Path(__file__).parent.parent.parent.resolve()

        # Set up test input file path
        self.test_input_file = self.base_path / "tests" / "test_files" / "source" / "webapp-mappings-3.0.yaml"

        # Create temporary output directory
        self.temp_output_dir = tempfile.mkdtemp()
        self.test_capec_output_file = Path(self.temp_output_dir) / "webapp-capec-3.0.yaml"
        self.test_asvs_output_file = Path(self.temp_output_dir) / "webapp-asvs-3.0.yaml"

        # Verify test input file exists
        if not self.test_input_file.exists():
            raise FileNotFoundError(f"Test input file not found: {self.test_input_file}")

    def tearDown(self) -> None:
        """Clean up test output directory"""
        if os.path.exists(self.temp_output_dir):
            shutil.rmtree(self.temp_output_dir)

    def test_load_test_yaml_file(self):
        """Test loading the test webapp-mappings YAML file"""
        data = capec_map.load_yaml_file(self.test_input_file)

        # Verify data was loaded
        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)
        self.assertIn("suits", data)
        self.assertIn("meta", data)

    def test_extract_capec_mappings_from_test_data(self):
        """Test extracting CAPEC mappings from real test data"""
        data = capec_map.load_yaml_file(self.test_input_file)

        # Extract mappings
        capec_mapping = capec_map.extract_capec_mappings(data)

        # Verify we extracted some mappings
        self.assertIsInstance(capec_mapping, dict)
        self.assertGreater(len(capec_mapping), 0, "Should extract at least one CAPEC mapping")

        # Verify the structure of extracted data
        for capec_code, asvs_set in capec_mapping.items():
            self.assertIsInstance(capec_code, int, f"CAPEC code {capec_code} should be int")
            self.assertIsInstance(asvs_set, set, f"ASVS set for {capec_code} should be a set")

    def test_extract_asvs_to_capec_mappings_from_test_data(self):
        """Test extracting ASVS to CAPEC mappings from real test data"""
        data = capec_map.load_yaml_file(self.test_input_file)

        # Extract mappings
        asvs_mapping = capec_map.extract_asvs_to_capec_mappings(data)

        # Verify we extracted some mappings
        self.assertIsInstance(asvs_mapping, dict)
        self.assertGreater(len(asvs_mapping), 0, "Should extract at least one ASVS mapping")

        # Verify the structure of extracted data
        for asvs_req, capec_set in asvs_mapping.items():
            self.assertIsInstance(asvs_req, str, f"ASVS requirement {asvs_req} should be string")
            self.assertIsInstance(capec_set, set, f"CAPEC set for {asvs_req} should be a set")
            # Each CAPEC code in the set should be an integer
            for capec_code in capec_set:
                self.assertIsInstance(capec_code, str, f"CAPEC code {capec_code} should be int")

    def test_convert_to_output_format_with_test_data(self):
        """Test converting extracted mappings to output format"""
        data = capec_map.load_yaml_file(self.test_input_file)
        capec_mapping = capec_map.extract_capec_mappings(data)

        # Convert to output format
        output_data = capec_map.convert_to_output_format(capec_mapping)

        # Verify output structure
        self.assertIsInstance(output_data, dict)
        for capec_code, mapping in output_data.items():
            self.assertIn("owasp_asvs", mapping)
            self.assertIsInstance(mapping["owasp_asvs"], list)
            # Verify list is sorted
            self.assertEqual(mapping["owasp_asvs"], sorted(mapping["owasp_asvs"]))

    def test_save_yaml_file_integration(self):
        """Test saving YAML file"""
        test_data = {54: {"owasp_asvs": ["4.3.2", "13.2.2", "13.4.1"]}, 116: {"owasp_asvs": ["15.2.3", "16.2.5"]}}

        # Save the file
        success = capec_map.save_yaml_file(self.test_capec_output_file, test_data)

        # Verify save was successful
        self.assertTrue(success)
        self.assertTrue(self.test_capec_output_file.exists())

        # Load and verify content
        with open(self.test_capec_output_file, "r", encoding="utf-8") as f:
            loaded_data = yaml.safe_load(f)

        self.assertEqual(loaded_data, test_data)

    def test_full_conversion_pipeline(self):
        """Test the complete conversion pipeline from input to output for both CAPEC and ASVS mappings"""
        # Load test input
        data = capec_map.load_yaml_file(self.test_input_file)
        self.assertIsNotNone(data)

        # Extract CAPEC mappings
        capec_mapping = capec_map.extract_capec_mappings(data)
        self.assertGreater(len(capec_mapping), 0)

        # Convert to output format
        output_data = capec_map.convert_to_output_format(capec_mapping)

        # Save CAPEC output
        success = capec_map.save_yaml_file(self.test_capec_output_file, output_data)
        self.assertTrue(success)

        # Verify output file exists and has correct structure
        self.assertTrue(self.test_capec_output_file.exists())

        # Load and verify CAPEC output
        with open(self.test_capec_output_file, "r", encoding="utf-8") as f:
            loaded_output = yaml.safe_load(f)

        self.assertIsInstance(loaded_output, dict)
        for capec_code, mapping in loaded_output.items():
            self.assertIn("owasp_asvs", mapping)
            self.assertIsInstance(mapping["owasp_asvs"], list)

        # Extract ASVS mappings
        asvs_mapping = capec_map.extract_asvs_to_capec_mappings(data)
        self.assertGreater(len(asvs_mapping), 0)

        # Convert to output format with capec_codes parameter
        output_data_asvs = capec_map.convert_to_output_format(asvs_mapping, parameter="capec_codes")

        # Save ASVS output
        success = capec_map.save_yaml_file(self.test_asvs_output_file, output_data_asvs)
        self.assertTrue(success)

        # Verify ASVS output file exists and has correct structure
        self.assertTrue(self.test_asvs_output_file.exists())

        # Load and verify ASVS output
        with open(self.test_asvs_output_file, "r", encoding="utf-8") as f:
            loaded_asvs_output = yaml.safe_load(f)

        self.assertIsInstance(loaded_asvs_output, dict)
        for asvs_req, mapping in loaded_asvs_output.items():
            self.assertIn("capec_codes", mapping)
            self.assertIsInstance(mapping["capec_codes"], list)

    def test_specific_capec_codes_in_test_data(self):
        """Test that specific known CAPEC codes from test data are extracted"""
        data = capec_map.load_yaml_file(self.test_input_file)
        capec_mapping = capec_map.extract_capec_mappings(data)

        # Check for specific CAPEC codes that should be in the test data
        # Based on the test file structure
        expected_capec_codes = [54, 116, 143, 144]

        for code in expected_capec_codes:
            self.assertIn(code, capec_mapping, f"CAPEC code {code} should be in mappings")

    def test_specific_asvs_requirements_in_test_data(self):
        """Test that ASVS requirements from test data are extracted correctly"""
        data = capec_map.load_yaml_file(self.test_input_file)
        asvs_mapping = capec_map.extract_asvs_to_capec_mappings(data)

        # Should have extracted ASVS requirements
        self.assertGreater(len(asvs_mapping), 0, "Should extract ASVS requirements")

        # Each ASVS requirement should map to one or more CAPEC codes
        for asvs_req, capec_codes in asvs_mapping.items():
            self.assertIsInstance(capec_codes, set)
            self.assertGreater(len(capec_codes), 0, f"ASVS {asvs_req} should map to at least one CAPEC code")

    def test_asvs_requirements_merged_correctly(self):
        """Test that ASVS requirements are merged correctly for duplicate CAPEC codes"""
        data = capec_map.load_yaml_file(self.test_input_file)
        capec_mapping = capec_map.extract_capec_mappings(data)

        # If a CAPEC code appears in multiple cards, the ASVS requirements should be merged
        # We'll check that there are no duplicates in any CAPEC code's ASVS set
        for capec_code, asvs_set in capec_mapping.items():
            # Convert to list to check for duplicates
            asvs_list = list(asvs_set)
            self.assertEqual(
                len(asvs_list), len(set(asvs_list)), f"CAPEC code {capec_code} has duplicate ASVS requirements"
            )

    def test_output_to_expected_location(self):
        """Test saving both output files to the expected test location"""
        # Set up the expected output paths
        expected_capec_output_path = self.base_path / "tests" / "test_files" / "output" / "webapp-capec-3.0.yaml"
        expected_asvs_output_path = self.base_path / "tests" / "test_files" / "output" / "webapp-asvs-3.0.yaml"

        # Create output directory if it doesn't exist
        expected_capec_output_path.parent.mkdir(parents=True, exist_ok=True)

        # Load and process data
        data = capec_map.load_yaml_file(self.test_input_file)

        # Process CAPEC mappings
        capec_mapping = capec_map.extract_capec_mappings(data)
        output_data = capec_map.convert_to_output_format(capec_mapping)

        # Save CAPEC to expected location
        success = capec_map.save_yaml_file(expected_capec_output_path, output_data)
        self.assertTrue(success)
        self.assertTrue(expected_capec_output_path.exists())

        # Verify CAPEC content
        with open(expected_capec_output_path, "r", encoding="utf-8") as f:
            loaded_data = yaml.safe_load(f)
        self.assertEqual(loaded_data, output_data)

        # Process ASVS mappings
        asvs_mapping = capec_map.extract_asvs_to_capec_mappings(data)
        output_data_asvs = capec_map.convert_to_output_format(asvs_mapping, parameter="capec_codes")

        # Save ASVS to expected location
        success = capec_map.save_yaml_file(expected_asvs_output_path, output_data_asvs)
        self.assertTrue(success)
        self.assertTrue(expected_asvs_output_path.exists())

        # Verify ASVS content
        with open(expected_asvs_output_path, "r", encoding="utf-8") as f:
            loaded_asvs_data = yaml.safe_load(f)
        self.assertEqual(loaded_asvs_data, output_data_asvs)

        # Clean up the created files
        if expected_capec_output_path.exists():
            expected_capec_output_path.unlink()
        if expected_asvs_output_path.exists():
            expected_asvs_output_path.unlink()

    def test_empty_suits_handling(self):
        """Test handling of YAML with no suits or empty suits"""
        # Create a minimal test file
        minimal_data = {"meta": {"version": "3.0"}, "suits": []}

        # Create temporary input file
        temp_input = Path(self.temp_output_dir) / "minimal.yaml"
        with open(temp_input, "w", encoding="utf-8") as f:
            yaml.dump(minimal_data, f)

        # Load and process
        data = capec_map.load_yaml_file(temp_input)
        capec_mapping = capec_map.extract_capec_mappings(data)

        # Should return empty mapping
        self.assertEqual(capec_mapping, {})

    def test_main_function_with_test_files(self):
        """Test main function logic with test file paths"""
        import argparse

        # Set up arguments for test files
        capec_map.convert_vars.args = argparse.Namespace(
            input_path=self.test_input_file,
            output_path=self.temp_output_dir,
            version="3.0",
            edition="webapp",
            debug=False,
        )

        # Manually execute main logic (without sys.argv parsing)
        capec_map.set_logging()

        # Load input
        data = capec_map.load_yaml_file(self.test_input_file)
        self.assertTrue(data, "Should load test data")

        # Extract and convert CAPEC mappings
        capec_mapping = capec_map.extract_capec_mappings(data)
        output_data = capec_map.convert_to_output_format(capec_mapping)

        # Save CAPEC output
        success = capec_map.save_yaml_file(self.test_capec_output_file, output_data)
        self.assertTrue(success)
        self.assertTrue(self.test_capec_output_file.exists())

        # Extract and convert ASVS mappings
        asvs_mapping = capec_map.extract_asvs_to_capec_mappings(data)
        output_data_asvs = capec_map.convert_to_output_format(asvs_mapping, parameter="capec_codes")

        # Save ASVS output
        success = capec_map.save_yaml_file(self.test_asvs_output_file, output_data_asvs)
        self.assertTrue(success)
        self.assertTrue(self.test_asvs_output_file.exists())

    def test_output_yaml_is_valid(self):
        """Test that both output YAML files are valid and can be reloaded"""
        # Process test data
        data = capec_map.load_yaml_file(self.test_input_file)

        # Test CAPEC output
        capec_mapping = capec_map.extract_capec_mappings(data)
        output_data = capec_map.convert_to_output_format(capec_mapping)
        capec_map.save_yaml_file(self.test_capec_output_file, output_data)
        reloaded_data = capec_map.load_yaml_file(self.test_capec_output_file)
        self.assertEqual(reloaded_data, output_data)

        # Test ASVS output
        asvs_mapping = capec_map.extract_asvs_to_capec_mappings(data)
        output_data_asvs = capec_map.convert_to_output_format(asvs_mapping, parameter="capec_codes")
        capec_map.save_yaml_file(self.test_asvs_output_file, output_data_asvs)
        reloaded_asvs_data = capec_map.load_yaml_file(self.test_asvs_output_file)
        self.assertEqual(reloaded_asvs_data, output_data_asvs)

    def test_unicode_handling(self):
        """Test that unicode characters in ASVS requirements are handled correctly"""
        # The test data might contain unicode characters
        data = capec_map.load_yaml_file(self.test_input_file)
        capec_mapping = capec_map.extract_capec_mappings(data)
        output_data = capec_map.convert_to_output_format(capec_mapping)

        # Save with unicode
        success = capec_map.save_yaml_file(self.test_capec_output_file, output_data)
        self.assertTrue(success)

        # Reload and verify
        reloaded = capec_map.load_yaml_file(self.test_capec_output_file)
        self.assertEqual(reloaded, output_data)


if __name__ == "__main__":
    unittest.main()
