#!/usr/bin/env python3
import unittest
import os
import logging
import tempfile
import shutil
import argparse
from pathlib import Path

import scripts.convert_capec as capec

capec.convert_vars = capec.ConvertVars()


if "unittest.util" in __import__("sys").modules:

    __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999


class TestConvertCAPECIntegration(unittest.TestCase):
    """Integration tests for convert_capec.py using real test data"""

    def setUp(self) -> None:
        """Set up test environment with test data paths"""

        self.base_path = Path(__file__).parent.parent.parent.resolve()

        self.test_input_file = self.base_path / "tests" / "test_files" / "capec-3.9" / "3000.json"
        self.test_asvs_mapping = (
            self.base_path
            / "tests"
            / "test_files"
            / "asvs-5.0"
            / "OWASP_Application_Security_Verification_Standard_5.0.0_en.json"
        )
        self.test_capec_to_asvs = self.base_path / "tests" / "test_files" / "source" / "webapp-capec-3.0.yaml"

        self.temp_output_dir = tempfile.mkdtemp()
        self.test_output_path = Path(self.temp_output_dir)

        if not self.test_input_file.exists():
            raise FileNotFoundError(f"Test input file not found: {self.test_input_file}")
        if not self.test_asvs_mapping.exists():
            raise FileNotFoundError(f"Test ASVS mapping file not found: {self.test_asvs_mapping}")
        if not self.test_capec_to_asvs.exists():
            raise FileNotFoundError(f"Test CAPEC to ASVS mapping file not found: {self.test_capec_to_asvs}")

    def tearDown(self) -> None:
        """Clean up test output directory"""
        if os.path.exists(self.temp_output_dir):
            shutil.rmtree(self.temp_output_dir)

    def test_load_test_json_file(self):
        """Test loading the test CAPEC JSON file"""
        data = capec.load_json_file(self.test_input_file)

        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)
        self.assertIn("Attack_Pattern_Catalog", data)

    def test_validate_test_json_data(self):
        """Test that the test JSON data has valid structure"""
        data = capec.load_json_file(self.test_input_file)

        is_valid = capec.validate_json_data(data)
        self.assertTrue(is_valid, "Test JSON data should have valid structure")

    def test_create_capec_pages_from_test_data(self):
        """Test creating CAPEC pages from test data"""

        data = capec.load_json_file(self.test_input_file)

        self.assertTrue(capec.validate_json_data(data))

        capec.convert_vars.args = argparse.Namespace(
            output_path=self.test_output_path,
            input_path=self.test_input_file,
            asvs_mapping=self.test_asvs_mapping,
            capec_to_asvs=self.test_capec_to_asvs,
            asvs_version="5.0",
            debug=False,
        )

        asvs_map = capec.load_json_file(self.test_asvs_mapping)
        capec_to_asvs_map = capec.load_capec_to_asvs_mapping(self.test_capec_to_asvs)
        capec.create_capec_pages(data, capec_to_asvs_map, asvs_map, "5.0")

        attack_patterns = data["Attack_Pattern_Catalog"]["Attack_Patterns"]["Attack_Pattern"]

        self.assertGreater(len(attack_patterns), 0, "Should have at least one attack pattern")

        first_pattern = attack_patterns[0]
        first_id = str(first_pattern["_ID"])
        first_name = first_pattern["_Name"]

        pattern_dir = self.test_output_path / first_id
        index_file = pattern_dir / "index.md"

        self.assertTrue(pattern_dir.exists(), f"Directory for CAPEC-{first_id} should exist")
        self.assertTrue(index_file.exists(), f"index.md for CAPEC-{first_id} should exist")

        content = index_file.read_text(encoding="utf-8")
        self.assertIn(f"CAPEC™ {first_id}", content)
        self.assertIn(first_name, content)
        self.assertIn("## Description", content)
        self.assertIn(f"Source: [CAPEC™ {first_id}]", content)

    def test_all_attack_patterns_created(self):
        """Test that all attack patterns in test data are converted"""

        data = capec.load_json_file(self.test_input_file)
        attack_patterns = data["Attack_Pattern_Catalog"]["Attack_Patterns"]["Attack_Pattern"]

        capec.convert_vars.args = argparse.Namespace(
            output_path=self.test_output_path,
            input_path=self.test_input_file,
            asvs_mapping=self.test_asvs_mapping,
            capec_to_asvs=self.test_capec_to_asvs,
            asvs_version="5.0",
            debug=False,
        )

        # Create pages
        asvs_map = capec.load_json_file(self.test_asvs_mapping)
        capec_to_asvs_map = capec.load_capec_to_asvs_mapping(self.test_capec_to_asvs)
        capec.create_capec_pages(data, capec_to_asvs_map, asvs_map, "5.0")

        for pattern in attack_patterns:
            pattern_id = str(pattern["_ID"])
            index_file = self.test_output_path / pattern_id / "index.md"

            self.assertTrue(index_file.exists(), f"index.md should exist for CAPEC-{pattern_id}")

    def test_created_file_content_structure(self):
        """Test that created markdown files have correct structure"""

        data = capec.load_json_file(self.test_input_file)

        capec.convert_vars.args = argparse.Namespace(
            output_path=self.test_output_path,
            input_path=self.test_input_file,
            asvs_mapping=self.test_asvs_mapping,
            capec_to_asvs=self.test_capec_to_asvs,
            asvs_version="5.0",
            debug=False,
        )

        # Create pages
        asvs_map = capec.load_json_file(self.test_asvs_mapping)
        capec_to_asvs_map = capec.load_capec_to_asvs_mapping(self.test_capec_to_asvs)
        capec.create_capec_pages(data, capec_to_asvs_map, asvs_map, "5.0")

        attack_patterns = data["Attack_Pattern_Catalog"]["Attack_Patterns"]["Attack_Pattern"]
        pattern = attack_patterns[0]
        pattern_id = str(pattern["_ID"])
        pattern_name = pattern["_Name"]

        index_file = self.test_output_path / pattern_id / "index.md"
        content = index_file.read_text(encoding="utf-8")

        lines = content.split("\n")

        self.assertTrue(lines[0].startswith("# CAPEC™ "), "First line should be title with CAPEC-")
        self.assertIn(pattern_name, lines[0])

        self.assertIn("## Description", content)

        self.assertIn("Source: [CAPEC™", content)
        self.assertIn("capec.mitre.org", content)

    def test_parse_arguments_with_test_paths(self):
        """Test argument parsing with test file paths"""
        args = capec.parse_arguments(
            [
                "-i",
                str(self.test_input_file),
                "-o",
                str(self.test_output_path),
                "-am",
                str(self.test_asvs_mapping),
                "-ca",
                str(self.test_capec_to_asvs),
            ]
        )

        self.assertEqual(args.input_path, str(self.test_input_file))
        self.assertEqual(args.output_path, str(self.test_output_path))
        self.assertEqual(args.asvs_mapping, str(self.test_asvs_mapping))
        self.assertEqual(args.capec_to_asvs, str(self.test_capec_to_asvs))

    def test_empty_and_recreate_folder(self):
        """Test emptying and recreating output folder"""

        test_dir = self.test_output_path / "test_folder"
        test_dir.mkdir()
        (test_dir / "test_file.txt").write_text("test content")

        capec.empty_folder(test_dir)

        self.assertFalse(test_dir.exists())

        capec.create_folder(test_dir)

        self.assertTrue(test_dir.exists())
        self.assertEqual(len(list(test_dir.iterdir())), 0)

    def test_full_conversion_workflow(self):
        """Test the full conversion workflow from input to output"""

        capec.convert_vars.args = capec.parse_arguments(
            [
                "-i",
                str(self.test_input_file),
                "-o",
                str(self.test_output_path),
                "-am",
                str(self.test_asvs_mapping),
                "-ca",
                str(self.test_capec_to_asvs),
                "-av",
                "5.0",
                "-d",
            ]  # Enable debug logging
        )

        capec.set_logging()

        capec.empty_folder(self.test_output_path)

        capec.create_folder(self.test_output_path)

        data = capec.load_json_file(self.test_input_file)
        asvs_map = capec.load_json_file(self.test_asvs_mapping)
        capec_to_asvs_map = capec.load_capec_to_asvs_mapping(self.test_capec_to_asvs)

        is_valid = capec.validate_json_data(data)
        self.assertTrue(is_valid)

        with self.assertLogs(logging.getLogger(), logging.INFO):
            capec.create_capec_pages(data, capec_to_asvs_map, asvs_map, "5.0")

        attack_patterns = data["Attack_Pattern_Catalog"]["Attack_Patterns"]["Attack_Pattern"]

        for pattern in attack_patterns:
            pattern_id = str(pattern["_ID"])
            index_file = self.test_output_path / pattern_id / "index.md"
            self.assertTrue(index_file.exists())

    def test_description_parsing_variations(self):
        """Test that different description formats in test data are parsed correctly"""

        data = capec.load_json_file(self.test_input_file)
        attack_patterns = data["Attack_Pattern_Catalog"]["Attack_Patterns"]["Attack_Pattern"]

        for pattern in attack_patterns:
            description = pattern.get("Description", "")
            parsed = capec.parse_description(description)

            self.assertIsInstance(parsed, str)
            self.assertGreater(len(parsed), 0, f"Description should not be empty for CAPEC-{pattern['_ID']}")

    def test_load_capec_to_asvs_mapping(self):
        """Test loading CAPEC to ASVS mapping YAML file"""
        capec_to_asvs_map = capec.load_capec_to_asvs_mapping(self.test_capec_to_asvs)

        self.assertIsNotNone(capec_to_asvs_map)
        self.assertIsInstance(capec_to_asvs_map, dict)
        # Check for known CAPEC IDs in test data
        self.assertIn(1, capec_to_asvs_map)
        self.assertIn(5, capec_to_asvs_map)
        self.assertIn(560, capec_to_asvs_map)

        # Verify structure
        self.assertIn("owasp_asvs", capec_to_asvs_map[1])
        self.assertIsInstance(capec_to_asvs_map[1]["owasp_asvs"], list)

    def test_create_link_list(self):
        """Test creating link list from ASVS requirements"""
        asvs_map = capec.load_json_file(self.test_asvs_mapping)
        capec_to_asvs_map = capec.load_capec_to_asvs_mapping(self.test_capec_to_asvs)

        # Test with CAPEC ID 1 which has mappings
        requirements = capec_to_asvs_map.get(1, {})
        link_list = capec.create_link_list(requirements, asvs_map, "5.0")

        self.assertIsInstance(link_list, str)
        self.assertGreater(len(link_list), 0)
        # Should contain markdown links
        self.assertIn("[", link_list)
        self.assertIn("]", link_list)
        self.assertIn("/taxonomy/asvs-5.0/", link_list)

    def test_create_link_list_empty(self):
        """Test creating link list with no requirements"""
        asvs_map = capec.load_json_file(self.test_asvs_mapping)

        link_list = capec.create_link_list({}, asvs_map, "5.0")

        self.assertEqual(link_list, "")

    def test_createlink(self):
        """Test creating individual ASVS link"""
        asvs_map = capec.load_json_file(self.test_asvs_mapping)

        # Test with a known shortcode from test data
        link = capec.createlink(asvs_map, "V8.1.1", "5.0")

        self.assertIsInstance(link, str)
        self.assertIn("V8.1.1", link)
        self.assertIn("/taxonomy/asvs-5.0/", link)

    def test_has_no_asvs_mapping(self):
        """Test checking for ASVS mapping"""
        capec_to_asvs_map = capec.load_capec_to_asvs_mapping(self.test_capec_to_asvs)

        # CAPEC ID 1 has mapping
        self.assertFalse(capec.has_no_asvs_mapping(1, capec_to_asvs_map))

        # Non-existent CAPEC ID should have no mapping
        self.assertTrue(capec.has_no_asvs_mapping(99999, capec_to_asvs_map))

    def test_get_valid_version(self):
        """Test ASVS version validation"""
        # Valid version
        self.assertEqual(capec.get_valid_version("5.0"), "5.0")

        # Invalid version should return latest
        latest = capec.ConvertVars.LATEST_ASVS_VERSION_CHOICES[-1]
        self.assertEqual(capec.get_valid_version("invalid"), latest)
        self.assertEqual(capec.get_valid_version("4.0"), latest)

    def test_asvs_mapping_in_output(self):
        """Test that ASVS mappings appear in output files"""
        data = capec.load_json_file(self.test_input_file)
        capec.convert_vars.args = argparse.Namespace(
            output_path=self.test_output_path,
            input_path=self.test_input_file,
            asvs_mapping=self.test_asvs_mapping,
            capec_to_asvs=self.test_capec_to_asvs,
            asvs_version="5.0",
            debug=False,
        )

        asvs_map = capec.load_json_file(self.test_asvs_mapping)
        capec_to_asvs_map = capec.load_capec_to_asvs_mapping(self.test_capec_to_asvs)
        capec.create_capec_pages(data, capec_to_asvs_map, asvs_map, "5.0")

        # Check CAPEC-1 which has ASVS mappings
        capec_1_file = self.test_output_path / "1" / "index.md"
        self.assertTrue(capec_1_file.exists())

        content = capec_1_file.read_text(encoding="utf-8")
        self.assertIn("## Related ASVS Requirements", content)
        self.assertIn("ASVS (5.0):", content)
        # Should contain at least one ASVS reference
        self.assertIn("V", content)  # ASVS codes start with V

    def test_no_asvs_mapping_output(self):
        """Test that CAPECs without mappings don't show ASVS section"""
        data = capec.load_json_file(self.test_input_file)
        capec.convert_vars.args = argparse.Namespace(
            output_path=self.test_output_path,
            input_path=self.test_input_file,
            asvs_mapping=self.test_asvs_mapping,
            capec_to_asvs=self.test_capec_to_asvs,
            asvs_version="5.0",
            debug=False,
        )

        # Create a modified map with no mapping for CAPEC-5
        asvs_map = capec.load_json_file(self.test_asvs_mapping)
        capec_to_asvs_map = {1: {"owasp_asvs": []}, 5: {}, 560: {"owasp_asvs": []}}
        capec.create_capec_pages(data, capec_to_asvs_map, asvs_map, "5.0")

        # Check CAPEC-5 which should have no ASVS section
        capec_5_file = self.test_output_path / "5" / "index.md"
        if capec_5_file.exists():
            content = capec_5_file.read_text(encoding="utf-8")
            # Should not have ASVS section if mapping is empty
            lines_with_asvs = [line for line in content.split("\n") if "## Related ASVS Requirements" in line]
            # Either no section, or empty section
            self.assertTrue(len(lines_with_asvs) == 0 or "ASVS (5.0):" not in content)


class TestConvertCAPECWithOutputDirectory(unittest.TestCase):
    """Test using the specified tests/test_files/output directory structure"""

    def setUp(self) -> None:
        """Set up test environment"""
        self.base_path = Path(__file__).parent.parent.parent.resolve()
        self.test_input_file = self.base_path / "tests" / "test_files" / "capec-3.9" / "3000.json"
        self.test_asvs_mapping = (
            self.base_path
            / "tests"
            / "test_files"
            / "asvs-5.0"
            / "OWASP_Application_Security_Verification_Standard_5.0.0_en.json"
        )
        self.test_capec_to_asvs = self.base_path / "tests" / "test_files" / "source" / "webapp-capec-3.0.yaml"

        # Use the actual test output directory (create if doesn't exist)
        self.test_output_base = self.base_path / "tests" / "test_files" / "output"
        self.test_output_path = self.test_output_base / "capec_test_output"

        self.test_output_base.mkdir(exist_ok=True)

        if self.test_output_path.exists():
            shutil.rmtree(self.test_output_path)

        self.test_output_path.mkdir(exist_ok=True)

    def tearDown(self) -> None:
        """Clean up test output"""
        if self.test_output_path.exists():
            shutil.rmtree(self.test_output_path)

    def test_conversion_to_test_output_directory(self):
        """Test conversion using tests/test_files/output directory"""

        capec.convert_vars.args = argparse.Namespace(
            output_path=self.test_output_path,
            input_path=self.test_input_file,
            asvs_mapping=self.test_asvs_mapping,
            capec_to_asvs=self.test_capec_to_asvs,
            asvs_version="5.0",
            debug=False,
        )

        data = capec.load_json_file(self.test_input_file)
        asvs_map = capec.load_json_file(self.test_asvs_mapping)
        capec_to_asvs_map = capec.load_capec_to_asvs_mapping(self.test_capec_to_asvs)
        self.assertTrue(capec.validate_json_data(data))

        capec.create_capec_pages(data, capec_to_asvs_map, asvs_map, "5.0")

        attack_patterns = data["Attack_Pattern_Catalog"]["Attack_Patterns"]["Attack_Pattern"]
        first_pattern_id = str(attack_patterns[0]["_ID"])

        output_file = self.test_output_path / first_pattern_id / "index.md"
        self.assertTrue(output_file.exists())

        self.assertTrue(str(output_file).startswith(str(self.test_output_base)))


if __name__ == "__main__":
    unittest.main()
