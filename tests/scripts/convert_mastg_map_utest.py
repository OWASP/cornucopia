import argparse
import logging
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

import scripts.convert_mastg_map as converter


TEST_DOCUMENT = """---
platform: android
id: MASTG-TEST-0330
weakness: MASWE-0020
knowledge: [MASTG-KNOW-0001, MASTG-KNOW-0043]
best-practices: [MASTG-BEST-0036]
---

## Overview
"""

MASWE_DOCUMENT = """---
id: MASWE-0005
threat: MAS-THREAT-0005
attacks: [MAS-ATTACK-0005, MAS-ATTACK-0006]
mappings:
    masvs-v2: [MASVS-STORAGE-2]
---
"""

THREATS = "MAS-THREAT-0005: Attackers can access sensitive data written to logs.\n"
ATTACKS = """MAS-ATTACK-0005: Accessing the device storage on a compromised device.
MAS-ATTACK-0006: Accessing the system logs on a compromised device.
"""


class TestMastgMapConversion(unittest.TestCase):
    def setUp(self) -> None:
        converter.convert_vars = converter.ConvertVars()

    def test_extract_test_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            test_file = Path(directory) / "MASTG-TEST-0330.md"
            test_file.write_text(TEST_DOCUMENT, encoding="utf-8")

            test_id, mapping = converter.extract_test_mapping(test_file)  # type: ignore[misc]

        self.assertEqual("0330", test_id)
        self.assertEqual(
            {
                "owasp_maswe": ["0020"],
                "owasp_mastg_know": ["0001", "0043"],
                "owasp_mastg_best": ["0036"],
            },
            mapping,
        )

    def test_extract_test_mapping_skips_missing_or_invalid_identifier(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            test_file = Path(directory) / "MASTG-TEST-0000.md"
            test_file.write_text("---\nid: invalid\n---\n", encoding="utf-8")
            self.assertIsNone(converter.extract_test_mapping(test_file))

    def test_extract_front_matter_returns_empty_mapping_when_absent_or_not_a_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing_front_matter = Path(directory) / "no-front-matter.md"
            missing_front_matter.write_text("# Test\n", encoding="utf-8")
            list_front_matter = Path(directory) / "list-front-matter.md"
            list_front_matter.write_text("---\n- a value\n---\n\n", encoding="utf-8")

            self.assertEqual({}, converter.extract_front_matter(missing_front_matter))
            self.assertEqual({}, converter.extract_front_matter(list_front_matter))

    def test_extract_front_matter_rejects_duplicate_keys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            test_file = Path(directory) / "duplicate-key.md"
            test_file.write_text("---\nid: MASTG-TEST-0001\nid: MASTG-TEST-0002\n---\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Duplicate YAML key"):
                converter.extract_front_matter(test_file)

    def test_normalize_references_rejects_invalid_data(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            test_file = Path(directory) / "test.md"
            with self.assertRaisesRegex(ValueError, "references must be a list"):
                converter.normalize_references("MASWE-0001", "MASWE-", test_file)
            with self.assertRaisesRegex(ValueError, "invalid MASWE"):
                converter.normalize_references(["MASTG-KNOW-0001"], "MASWE-", test_file)

    def test_extract_mastg_mappings_and_output_data(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            tests_path = repository / "tests-beta" / "android" / "MASVS-STORAGE"
            tests_path.mkdir(parents=True)
            (tests_path / "MASTG-TEST-0330.md").write_text(TEST_DOCUMENT, encoding="utf-8")
            (tests_path / "MASTG-TEST-0999.md").write_text("# No front matter\n", encoding="utf-8")

            mappings = converter.extract_mastg_mappings(repository)

        data = converter.output_data(mappings, "mobileapp", "2.0")
        self.assertEqual("mastg", data["meta"]["component"])
        self.assertEqual(["0020"], data["0330"]["owasp_maswe"])

    def test_extract_mastg_mappings_requires_beta_tests_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(FileNotFoundError, "beta tests directory"):
                converter.extract_mastg_mappings(Path(directory))

    def test_output_maswe_data_aggregates_mastg_siblings_and_maswe_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            weakness_path = repository / "weaknesses" / "MASVS-STORAGE"
            catalog_path = repository / ".github" / "instructions"
            weakness_path.mkdir(parents=True)
            catalog_path.mkdir(parents=True)
            (weakness_path / "MASWE-0005.md").write_text(MASWE_DOCUMENT, encoding="utf-8")
            (catalog_path / "threats.yaml").write_text(THREATS, encoding="utf-8")
            (catalog_path / "attacks.yaml").write_text(ATTACKS, encoding="utf-8")

            data = converter.output_maswe_data(
                {
                    "0203": {"owasp_maswe": ["0005"], "owasp_mastg_know": ["0049"], "owasp_mastg_best": ["0002"]},
                    "0231": {"owasp_maswe": ["0005"], "owasp_mastg_know": ["0049"]},
                },
                repository,
                "mobileapp",
                "2.0",
            )

        self.assertEqual("maswe", data["meta"]["component"])
        self.assertEqual(["0203", "0231"], data["0005"]["owasp_mastg"])
        self.assertEqual(["0049"], data["0005"]["owasp_mastg_know"])
        self.assertEqual(["0002"], data["0005"]["owasp_mastg_best"])
        self.assertEqual(["MASVS-STORAGE-2"], data["0005"]["owasp_masvs"])
        self.assertEqual({"0005": "Attackers can access sensitive data written to logs."}, data["0005"]["owasp_mas_threat"])
        self.assertEqual(
            {
                "0005": "Accessing the device storage on a compromised device.",
                "0006": "Accessing the system logs on a compromised device.",
            },
            data["0005"]["owasp_mas_attack"],
        )

    def test_save_yaml_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output_path = Path(directory) / "nested" / "mapping.yaml"
            converter.save_yaml_file(
                output_path,
                converter.output_data({"0208": {"owasp_maswe": ["0008"], "owasp_mastg_know": ["0049"]}}, "mobileapp", "2.0"),
            )
            content = output_path.read_text(encoding="utf-8")
            data = yaml.safe_load(content)
        self.assertEqual({"edition": "mobileapp", "component": "mastg", "language": "ALL", "version": "2.0"}, data["meta"])
        self.assertIn("'0208':", content)
        self.assertIn("- '0008'", content)
        self.assertIn("- '0049'", content)

    def test_extract_mastg_mappings_rejects_duplicate_test_identifiers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tests_path = Path(directory) / "tests-beta" / "android" / "MASVS-STORAGE"
            tests_path.mkdir(parents=True)
            for suffix in ("a", "b"):
                (tests_path / f"MASTG-TEST-0330-{suffix}.md").write_text(TEST_DOCUMENT, encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Duplicate MASTG test identifier"):
                converter.extract_mastg_mappings(Path(directory))

    @mock.patch("scripts.convert_mastg_map.subprocess.run")
    def test_clone_mastg(self, run: mock.Mock) -> None:
        destination = Path("mastg-checkout")
        converter.clone_mastg(destination)
        run.assert_has_calls(
            [
                mock.call(
                    ["git", "clone", "--no-checkout", "--depth", "1", converter.ConvertVars.MASTG_REPOSITORY_URL, str(destination)],
                    check=True,
                    capture_output=True,
                    text=True,
                ),
                mock.call(
                    ["git", "-C", str(destination), "fetch", "--depth", "1", "origin", converter.ConvertVars.MASTG_REPOSITORY_REVISION],
                    check=True,
                    capture_output=True,
                    text=True,
                ),
                mock.call(
                    ["git", "-C", str(destination), "checkout", "--detach", converter.ConvertVars.MASTG_REPOSITORY_REVISION],
                    check=True,
                    capture_output=True,
                    text=True,
                ),
            ]
        )

    @mock.patch("scripts.convert_mastg_map.subprocess.run")
    def test_clone_maswe(self, run: mock.Mock) -> None:
        destination = Path("maswe-checkout")
        converter.clone_maswe(destination)
        run.assert_has_calls(
            [
                mock.call(
                    ["git", "clone", "--no-checkout", "--depth", "1", converter.ConvertVars.MASWE_REPOSITORY_URL, str(destination)],
                    check=True,
                    capture_output=True,
                    text=True,
                ),
                mock.call(
                    ["git", "-C", str(destination), "fetch", "--depth", "1", "origin", converter.ConvertVars.MASWE_REPOSITORY_REVISION],
                    check=True,
                    capture_output=True,
                    text=True,
                ),
                mock.call(
                    ["git", "-C", str(destination), "checkout", "--detach", converter.ConvertVars.MASWE_REPOSITORY_REVISION],
                    check=True,
                    capture_output=True,
                    text=True,
                ),
            ]
        )

    def test_parse_arguments_defaults(self) -> None:
        args = converter.parse_arguments([])
        self.assertEqual("mobileapp", args.edition)
        self.assertEqual("2.0", args.version)

    def test_parse_arguments_accepts_all_converter_options(self) -> None:
        args = converter.parse_arguments(
            ["--input-path", "mastg", "--edition", "custom", "--version", "9.9", "--output-path", "output", "--debug"]
        )
        self.assertEqual("mastg", args.input_path)
        self.assertEqual("custom", args.edition)
        self.assertEqual("9.9", args.version)
        self.assertEqual("output", args.output_path)
        self.assertTrue(args.debug)

    def test_parse_arguments_rejects_path_traversal_in_generated_filename(self) -> None:
        with self.assertRaises(SystemExit):
            converter.parse_arguments(["--edition", "../outside"])

    def test_set_logging_uses_requested_level(self) -> None:
        converter.convert_vars.args = argparse.Namespace(debug=True)
        converter.set_logging()
        self.assertEqual(logging.DEBUG, logging.getLogger().level)

        converter.convert_vars.args = argparse.Namespace(debug=False)
        converter.set_logging()
        self.assertEqual(logging.INFO, logging.getLogger().level)

    @mock.patch("scripts.convert_mastg_map.output_maswe_data", return_value={})
    @mock.patch("scripts.convert_mastg_map.set_logging")
    @mock.patch("scripts.convert_mastg_map.save_yaml_file")
    @mock.patch("scripts.convert_mastg_map.extract_mastg_mappings", return_value={"0330": {"owasp_maswe": ["0020"]}})
    @mock.patch("scripts.convert_mastg_map.parse_arguments")
    def test_main_uses_existing_checkout(
        self, parse_arguments: mock.Mock, extract_mastg_mappings: mock.Mock, save_yaml_file: mock.Mock, _: mock.Mock, __: mock.Mock
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "mastg"
            output_path = Path(directory) / "output"
            parse_arguments.return_value = argparse.Namespace(
                input_path=str(input_path), maswe_input_path=str(input_path), output_path=str(output_path), edition="mobileapp", version="2.0", debug=False
            )

            converter.main()

        extract_mastg_mappings.assert_called_once_with(input_path.resolve())
        self.assertEqual(output_path.resolve() / "mobileapp-mastg-2.0.yaml", save_yaml_file.call_args_list[0].args[0])
        self.assertEqual(output_path.resolve() / "mobileapp-maswe-2.0.yaml", save_yaml_file.call_args_list[1].args[0])

    @mock.patch("scripts.convert_mastg_map.output_maswe_data", return_value={})
    @mock.patch("scripts.convert_mastg_map.set_logging")
    @mock.patch("scripts.convert_mastg_map.save_yaml_file")
    @mock.patch("scripts.convert_mastg_map.extract_mastg_mappings", return_value={})
    @mock.patch("scripts.convert_mastg_map.clone_mastg")
    @mock.patch("scripts.convert_mastg_map.parse_arguments")
    def test_main_clones_temporary_checkout(
        self,
        parse_arguments: mock.Mock,
        clone_mastg: mock.Mock,
        extract_mastg_mappings: mock.Mock,
        _: mock.Mock,
        __: mock.Mock,
        ___: mock.Mock,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output_path = Path(directory) / "output"
            parse_arguments.return_value = argparse.Namespace(
                input_path=None, maswe_input_path=str(output_path), output_path=str(output_path), edition="mobileapp", version="2.0", debug=False
            )

            converter.main()

        clone_destination = clone_mastg.call_args.args[0]
        self.assertEqual("mastg", clone_destination.name)
        extract_mastg_mappings.assert_called_once_with(clone_destination)

    @mock.patch("scripts.convert_mastg_map.output_maswe_data", return_value={})
    @mock.patch("scripts.convert_mastg_map.set_logging")
    @mock.patch("scripts.convert_mastg_map.save_yaml_file")
    @mock.patch("scripts.convert_mastg_map.extract_mastg_mappings", return_value={})
    @mock.patch("scripts.convert_mastg_map.clone_mastg")
    @mock.patch("scripts.convert_mastg_map.parse_arguments")
    @mock.patch("scripts.convert_mastg_map.tempfile.TemporaryDirectory")
    def test_main_cleans_up_temporary_checkout(
        self,
        temporary_directory: mock.Mock,
        parse_arguments: mock.Mock,
        _: mock.Mock,
        __: mock.Mock,
        ___: mock.Mock,
        ____: mock.Mock,
        _____: mock.Mock,
    ) -> None:
        temporary_directory.return_value.name = "temporary-checkout"
        parse_arguments.return_value = argparse.Namespace(
            input_path=None, maswe_input_path="maswe", output_path="output", edition="mobileapp", version="2.0", debug=False
        )

        converter.main()

        temporary_directory.return_value.cleanup.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()