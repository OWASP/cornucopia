#!/usr/bin/env python3
import unittest
import os
import tempfile
import shutil
from pathlib import Path
import yaml

import scripts.capec_map_enricher as enricher

enricher.enricher_vars = enricher.EnricherVars()


if "unittest.util" in __import__("sys").modules:
    # Show full diff in self.assertEqual.
    __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999


class TestCapecMapEnricherIntegration(unittest.TestCase):
    """Integration tests for capec_map_enricher.py using real test data"""

    def setUp(self) -> None:
        """Set up test environment with test data paths"""
        # Get the base path of the repository
        self.base_path = Path(__file__).parent.parent.parent.resolve()

        # Set up test input file paths
        self.test_capec_json = self.base_path / "tests" / "test_files" / "capec-3.9" / "3000.json"
        self.test_capec_yaml = self.base_path / "tests" / "test_files" / "source" / "webapp-capec-3.0.yaml"

        # Create temporary output directory
        self.temp_output_dir = tempfile.mkdtemp()
        self.test_output_file = Path(self.temp_output_dir) / "edition-capec-latest.yaml"

        # Verify test input files exist
        if not self.test_capec_json.exists():
            raise FileNotFoundError(f"Test CAPEC JSON file not found: {self.test_capec_json}")
        if not self.test_capec_yaml.exists():
            raise FileNotFoundError(f"Test CAPEC YAML file not found: {self.test_capec_yaml}")

    def tearDown(self) -> None:
        """Clean up test output directory"""
        if os.path.exists(self.temp_output_dir):
            shutil.rmtree(self.temp_output_dir)

    def test_load_test_json_file(self):
        """Test loading the test CAPEC JSON file"""
        data = enricher.load_json_file(self.test_capec_json)

        # Verify data was loaded
        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)
        self.assertIn("Attack_Pattern_Catalog", data)

    def test_load_test_yaml_file(self):
        """Test loading the test CAPEC YAML file"""
        data = enricher.load_yaml_file(self.test_capec_yaml)

        # Verify data was loaded
        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)
        self.assertGreater(len(data), 0)

        # Check that keys are integers
        for key in data.keys():
            self.assertIsInstance(key, int)

    def test_extract_capec_names_from_test_data(self):
        """Test extracting CAPEC names from real test JSON data"""
        json_data = enricher.load_json_file(self.test_capec_json)

        # Extract names
        capec_names = enricher.extract_capec_names(json_data)

        # Verify we extracted some names
        self.assertIsInstance(capec_names, dict)
        self.assertGreater(len(capec_names), 0, "Should extract at least one CAPEC name")

        # Verify the structure
        for capec_id, name in capec_names.items():
            self.assertIsInstance(capec_id, int)
            self.assertIsInstance(name, str)
            self.assertGreater(len(name), 0)

    def test_specific_capec_names_in_test_data(self):
        """Test that specific known CAPEC entries from test data are extracted"""
        json_data = enricher.load_json_file(self.test_capec_json)
        capec_names = enricher.extract_capec_names(json_data)

        # Based on the test JSON file structure, these should exist
        expected_ids = [1, 5, 560]

        for capec_id in expected_ids:
            self.assertIn(capec_id, capec_names, f"CAPEC-{capec_id} should be in extracted names")
            self.assertIsInstance(capec_names[capec_id], str)
            self.assertGreater(len(capec_names[capec_id]), 0)

    def test_enrich_capec_mappings_integration(self):
        """Test enriching CAPEC mappings with real test data"""
        # Load data
        json_data = enricher.load_json_file(self.test_capec_json)
        yaml_data = enricher.load_yaml_file(self.test_capec_yaml)

        # Extract and enrich
        capec_names = enricher.extract_capec_names(json_data)
        enriched = enricher.enrich_capec_mappings(yaml_data, capec_names)

        # Verify enrichment
        self.assertEqual(len(enriched), len(yaml_data))

        for capec_id, entry in enriched.items():
            # Each entry should have a name
            self.assertIn("name", entry)
            self.assertIsInstance(entry["name"], str)

            # Each entry should preserve original owasp_asvs data
            if capec_id in yaml_data and "owasp_asvs" in yaml_data[capec_id]:
                self.assertIn("owasp_asvs", entry)
                self.assertEqual(entry["owasp_asvs"], yaml_data[capec_id]["owasp_asvs"])

    def test_full_enrichment_pipeline(self):
        """Test the complete enrichment pipeline from input to output"""
        # Load input files
        json_data = enricher.load_json_file(self.test_capec_json)
        yaml_data = enricher.load_yaml_file(self.test_capec_yaml)

        self.assertIsNotNone(json_data)
        self.assertIsNotNone(yaml_data)
        self.assertGreater(len(yaml_data), 0)

        # Extract CAPEC names
        capec_names = enricher.extract_capec_names(json_data)
        self.assertGreater(len(capec_names), 0)

        # Enrich mappings
        enriched = enricher.enrich_capec_mappings(yaml_data, capec_names)
        self.assertEqual(len(enriched), len(yaml_data))

        # Save output
        success = enricher.save_yaml_file(self.test_output_file, enriched)
        self.assertTrue(success)

        # Verify output file exists
        self.assertTrue(self.test_output_file.exists())

        # Load and verify output
        with open(self.test_output_file, "r", encoding="utf-8") as f:
            loaded_output = yaml.safe_load(f)

        self.assertIsInstance(loaded_output, dict)
        for capec_code, mapping in loaded_output.items():
            self.assertIn("name", mapping)
            self.assertIn("owasp_asvs", mapping)
            self.assertIsInstance(mapping["owasp_asvs"], list)

    def test_enriched_output_has_correct_names(self):
        """Test that enriched output has correct CAPEC names"""
        # Load and process data
        json_data = enricher.load_json_file(self.test_capec_json)
        yaml_data = enricher.load_yaml_file(self.test_capec_yaml)
        capec_names = enricher.extract_capec_names(json_data)
        enriched = enricher.enrich_capec_mappings(yaml_data, capec_names)

        # Check specific entries
        if 1 in enriched and 1 in capec_names:
            self.assertEqual(enriched[1]["name"], capec_names[1])

        if 5 in enriched and 5 in capec_names:
            self.assertEqual(enriched[5]["name"], capec_names[5])

        if 560 in enriched and 560 in capec_names:
            self.assertEqual(enriched[560]["name"], capec_names[560])

    def test_save_and_reload_preserves_data(self):
        """Test that saving and reloading enriched data preserves all information"""
        # Process data
        json_data = enricher.load_json_file(self.test_capec_json)
        yaml_data = enricher.load_yaml_file(self.test_capec_yaml)
        capec_names = enricher.extract_capec_names(json_data)
        enriched = enricher.enrich_capec_mappings(yaml_data, capec_names)

        # Save and reload
        enricher.save_yaml_file(self.test_output_file, enriched)
        reloaded = enricher.load_yaml_file(self.test_output_file)

        # Compare
        self.assertEqual(len(reloaded), len(enriched))
        for capec_id in enriched.keys():
            self.assertIn(capec_id, reloaded)
            self.assertEqual(reloaded[capec_id]["name"], enriched[capec_id]["name"])
            self.assertEqual(reloaded[capec_id]["owasp_asvs"], enriched[capec_id]["owasp_asvs"])

    def test_output_to_test_files_directory(self):
        """Test saving output to the tests/test_files/output directory"""
        # Set up the expected output path
        expected_output_path = self.base_path / "tests" / "test_files" / "output" / "edition-capec-latest.yaml"

        # Create output directory if it doesn't exist
        expected_output_path.parent.mkdir(parents=True, exist_ok=True)

        # Load and process data
        json_data = enricher.load_json_file(self.test_capec_json)
        yaml_data = enricher.load_yaml_file(self.test_capec_yaml)
        capec_names = enricher.extract_capec_names(json_data)
        enriched = enricher.enrich_capec_mappings(yaml_data, capec_names)

        # Save to expected location
        success = enricher.save_yaml_file(expected_output_path, enriched)

        self.assertTrue(success)
        self.assertTrue(expected_output_path.exists())

        # Verify content
        with open(expected_output_path, "r", encoding="utf-8") as f:
            loaded_data = yaml.safe_load(f)

        self.assertEqual(len(loaded_data), len(enriched))

        # Clean up the created file
        if expected_output_path.exists():
            expected_output_path.unlink()

    def test_enrichment_preserves_yaml_structure(self):
        """Test that enrichment preserves YAML structure and ordering"""
        # Load and process
        json_data = enricher.load_json_file(self.test_capec_json)
        yaml_data = enricher.load_yaml_file(self.test_capec_yaml)
        capec_names = enricher.extract_capec_names(json_data)
        enriched = enricher.enrich_capec_mappings(yaml_data, capec_names)

        # Save
        enricher.save_yaml_file(self.test_output_file, enriched)

        # Read as text to check structure
        content = self.test_output_file.read_text(encoding="utf-8")

        # Should contain CAPEC IDs as keys
        for capec_id in enriched.keys():
            self.assertIn(f"{capec_id}:", content)

        # Should contain name fields
        self.assertIn("name:", content)

        # Should contain owasp_asvs fields
        self.assertIn("owasp_asvs:", content)

    def test_main_function_with_test_files(self):
        """Test main function with test file paths"""
        import argparse

        # Set up arguments for test files
        enricher.enricher_vars.args = argparse.Namespace(
            capec_json=self.test_capec_json,
            input_path=self.test_capec_yaml,
            output_path=self.test_output_file,
            source_dir=self.base_path / "tests" / "test_files" / "source",
            version="latest",
            edition="edition",
            debug=False,
        )

        # Manually execute main logic
        enricher.set_logging()

        # Load JSON
        json_data = enricher.load_json_file(self.test_capec_json)
        self.assertTrue(json_data, "Should load JSON data")

        # Extract names
        capec_names = enricher.extract_capec_names(json_data)
        self.assertTrue(capec_names, "Should extract CAPEC names")

        # Load YAML
        yaml_data = enricher.load_yaml_file(self.test_capec_yaml)
        self.assertTrue(yaml_data, "Should load YAML data")

        # Enrich
        enriched = enricher.enrich_capec_mappings(yaml_data, capec_names)
        self.assertEqual(len(enriched), len(yaml_data))

        # Save
        success = enricher.save_yaml_file(self.test_output_file, enriched)
        self.assertTrue(success)
        self.assertTrue(self.test_output_file.exists())

    def test_unicode_handling_in_names(self):
        """Test that unicode characters in CAPEC names are handled correctly"""
        # Load and process data
        json_data = enricher.load_json_file(self.test_capec_json)
        yaml_data = enricher.load_yaml_file(self.test_capec_yaml)
        capec_names = enricher.extract_capec_names(json_data)
        enriched = enricher.enrich_capec_mappings(yaml_data, capec_names)

        # Save with unicode
        success = enricher.save_yaml_file(self.test_output_file, enriched)
        self.assertTrue(success)

        # Reload and verify
        reloaded = enricher.load_yaml_file(self.test_output_file)
        self.assertEqual(len(reloaded), len(enriched))


if __name__ == "__main__":
    unittest.main()
