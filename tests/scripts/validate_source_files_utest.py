"""
Unit tests for scripts/validate_source_files.py.
"""

from __future__ import annotations

import io
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

import yaml

from scripts.validate_source_files import SourceValidator, main, parse_arguments


class TestSourceValidator(unittest.TestCase):
    """Test suite for SourceValidator class."""

    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp())
        self.validator = SourceValidator()

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _write_yaml(self, filename: str, data: Any) -> Path:
        file_path = self.temp_dir / filename
        with open(file_path, "w", encoding="utf-8") as f:
            if isinstance(data, str):
                f.write(data)
            else:
                yaml.dump(data, f)
        return file_path

    def test_file_does_not_exist(self) -> None:
        res = self.validator.validate_file(self.temp_dir / "nonexistent.yaml")
        self.assertFalse(res)
        self.assertTrue(any("does not exist" in e for e in self.validator.errors))

    def test_malformed_yaml(self) -> None:
        file_path = self._write_yaml("bad.yaml", ": invalid: yaml: [")
        res = self.validator.validate_file(file_path)
        self.assertFalse(res)
        self.assertTrue(any("Failed to parse YAML" in e for e in self.validator.errors))

    def test_empty_yaml_file(self) -> None:
        file_path = self._write_yaml("empty.yaml", "")
        res = self.validator.validate_file(file_path)
        self.assertFalse(res)
        self.assertTrue(any("is empty" in e for e in self.validator.errors))

    def test_non_dict_root(self) -> None:
        file_path = self._write_yaml("scalar.yaml", ["item1", "item2"])
        res = self.validator.validate_file(file_path)
        self.assertFalse(res)
        self.assertTrue(any("must be a mapping" in e for e in self.validator.errors))

    def test_meta_validation_errors(self) -> None:
        file_path = self._write_yaml("test-mappings-1.0.yaml", {"suits": []})
        res = self.validator.validate_file(file_path)
        self.assertFalse(res)
        self.assertTrue(any("Missing or invalid 'meta'" in e for e in self.validator.errors))

        # Missing required key in meta
        file_path2 = self._write_yaml(
            "test2-mappings-1.0.yaml",
            {"meta": {"edition": "webapp", "component": ""}, "suits": []},
        )
        validator2 = SourceValidator()
        res2 = validator2.validate_file(file_path2)
        self.assertFalse(res2)
        self.assertTrue(any("missing required key" in e for e in validator2.errors))

    def test_valid_mappings_file(self) -> None:
        self._write_yaml(
            "webapp-asvs-3.0.yaml",
            {
                "meta": {"edition": "webapp", "component": "asvs", "version": "3.0"},
                "2.4.1": {},
                "13.3.1": {},
            },
        )
        data = {
            "meta": {"edition": "webapp", "component": "mappings", "version": "3.0"},
            "labels": {"owasp_asvs": "OWASP ASVS (v5.0)"},
            "suits": [
                {
                    "id": "VE",
                    "name": "Validation",
                    "cards": [
                        {
                            "id": "VE2",
                            "owasp_asvs": ["2.4.1", "13.3.1", "-"],
                            "capec": [54, "113", "-"],
                            "safecode": [4, "-", "12"],
                            "stride": ["I"],
                            "capec_map": {54: {"owasp_asvs": ["2.4.1"]}},
                            "owasp_cre": {"owasp_asvs": ["166-15"]},
                        }
                    ],
                }
            ],
        }
        file_path = self._write_yaml("test-mappings-3.0.yaml", data)
        res = self.validator.validate_file(file_path)
        self.assertTrue(res)
        self.assertEqual(len(self.validator.errors), 0)

    def test_mappings_invalid_suits_structure(self) -> None:
        data = {
            "meta": {"edition": "webapp", "component": "mappings", "version": "3.0"},
            "suits": "not a list",
        }
        file_path = self._write_yaml("bad-mappings-1.yaml", data)
        res = self.validator.validate_file(file_path)
        self.assertFalse(res)
        self.assertTrue(any("'suits' must be a list" in e for e in self.validator.errors))

        data2 = {
            "meta": {"edition": "webapp", "component": "mappings", "version": "3.0"},
            "suits": [
                "not a dict",
                {"name": "Test", "cards": "not a list"},
                {"name": "T2", "cards": ["not dict"]},
            ],
        }
        validator2 = SourceValidator()
        file_path2 = self._write_yaml("bad-mappings-2.yaml", data2)
        res2 = validator2.validate_file(file_path2)
        self.assertFalse(res2)
        self.assertEqual(len(validator2.errors), 5)
        self.assertTrue(any("Suit entry missing 'id'" in e for e in validator2.errors))

    def test_mappings_corrupted_asvs(self) -> None:
        data = {
            "meta": {"edition": "webapp", "component": "mappings", "version": "3.0"},
            "suits": [
                {
                    "name": "Auth",
                    "cards": [
                        {
                            "id": "A1",
                            "owasp_asvs": ["15.3.5 15.3.6"],  # space-separated typo
                        },
                        {
                            "id": "A2",
                            "owasp_asvs": ["invalid_asvs"],
                        },
                        {
                            "id": "A3",
                            "owasp_asvs": "not a list",
                        },
                    ],
                }
            ],
        }
        file_path = self._write_yaml("corrupted-mappings.yaml", data)
        res = self.validator.validate_file(file_path)
        self.assertFalse(res)
        self.assertTrue(any("space-separated" in e for e in self.validator.errors))
        self.assertTrue(any("must match dotted numeric pattern" in e for e in self.validator.errors))
        self.assertTrue(any("'owasp_asvs' must be a list" in e for e in self.validator.errors))

    def test_mappings_invalid_capec_and_safecode(self) -> None:
        data = {
            "meta": {"edition": "webapp", "component": "mappings", "version": "3.0"},
            "suits": [
                {
                    "name": "Test",
                    "cards": [
                        {
                            "id": "C1",
                            "capec": "not a list",
                            "safecode": "not a list",
                        },
                        {
                            "id": "C2",
                            "capec": ["bad_capec"],
                            "safecode": ["bad_code"],
                        },
                    ],
                }
            ],
        }
        file_path = self._write_yaml("invalid-capec-mappings.yaml", data)
        res = self.validator.validate_file(file_path)
        self.assertFalse(res)
        self.assertTrue(any("'capec' must be a list" in e for e in self.validator.errors))
        self.assertTrue(any("'safecode' must be a list" in e for e in self.validator.errors))
        self.assertTrue(any("Malformed CAPEC ID" in e for e in self.validator.errors))
        self.assertTrue(any("Malformed SAFECode ID" in e for e in self.validator.errors))

    def test_mappings_invalid_stride_and_cre(self) -> None:
        data = {
            "meta": {"edition": "webapp", "component": "mappings", "version": "3.0"},
            "suits": [
                {
                    "name": "Test",
                    "cards": [
                        {
                            "id": "S1",
                            "stride": "not a list",
                            "owasp_cre": "not a dict",
                        },
                        {
                            "id": "S2",
                            "stride": ["   "],  # empty token
                        },
                    ],
                }
            ],
        }
        file_path = self._write_yaml("stride-cre-mappings.yaml", data)
        res = self.validator.validate_file(file_path)
        self.assertFalse(res)
        self.assertTrue(any("'stride' must be a list" in e for e in self.validator.errors))
        self.assertTrue(any("Empty STRIDE token" in e for e in self.validator.errors))
        self.assertTrue(any("'owasp_cre' must be a dictionary" in e for e in self.validator.errors))

    def test_mappings_invalid_capec_map(self) -> None:
        data = {
            "meta": {"edition": "webapp", "component": "mappings", "version": "3.0"},
            "suits": [
                {
                    "name": "Test",
                    "cards": [
                        {
                            "id": "CM1",
                            "capec_map": "not a dict",
                        },
                        {
                            "id": "CM2",
                            "capec_map": {
                                "bad_key": "not a dict",
                                " 54 ": {},
                                "54": {"owasp_asvs": ["bad asvs"]},
                            },
                        },
                    ],
                }
            ],
        }
        file_path = self._write_yaml("capec-map-mappings.yaml", data)
        res = self.validator.validate_file(file_path)
        self.assertFalse(res)
        self.assertTrue(any("'capec_map' must be a dictionary" in e for e in self.validator.errors))
        self.assertTrue(any("CAPEC key 'bad_key' must be an integer" in e for e in self.validator.errors))
        self.assertTrue(any("CAPEC key '54' must be an integer" in e for e in self.validator.errors))

    def test_valid_cards_file(self) -> None:
        data = {
            "meta": {"edition": "webapp", "component": "cards", "version": "3.0"},
            "suits": [
                {
                    "id": "AT",
                    "name": "Auth",
                    "cards": [{"id": "AT2", "name": "Card 2"}],
                }
            ],
        }
        file_path = self._write_yaml("test-cards-3.0-en.yaml", data)
        res = self.validator.validate_file(file_path)
        self.assertTrue(res)

    def test_invalid_cards_file(self) -> None:
        data = {
            "meta": {"edition": "webapp", "component": "cards", "version": "3.0"},
            "suits": [
                "not a dict",
                {"name": "", "cards": "not a list"},
                {"id": "S1", "name": "Suit", "cards": ["not dict", {"id": ""}]},
                {"id": None, "name": None, "cards": [{"id": None}]},
                {"name": "MissingID", "cards": [{"id": "C1"}]},
            ],
        }
        file_path = self._write_yaml("bad-cards-1.0.yaml", data)
        res = self.validator.validate_file(file_path)
        self.assertFalse(res)
        self.assertTrue(any("missing 'name'" in e for e in self.validator.errors))
        self.assertTrue(any("missing 'id'" in e for e in self.validator.errors))
        self.assertTrue(any("Card missing 'id'" in e for e in self.validator.errors))

    def test_cards_file_suits_not_list(self) -> None:
        data = {
            "meta": {"edition": "webapp", "component": "cards", "version": "3.0"},
            "suits": "not list",
        }
        file_path = self._write_yaml("cards-no-list.yaml", data)
        res = self.validator.validate_file(file_path)
        self.assertFalse(res)
        self.assertTrue(any("'suits' must be a list" in e for e in self.validator.errors))

    def test_catalog_files(self) -> None:
        asvs_data = {
            "meta": {"edition": "webapp", "component": "asvs", "version": "3.0"},
            "1.1.1": {"capec_codes": ["120", 126]},
            "1.1.2": {},
        }
        asvs_path = self._write_yaml("webapp-asvs-3.0.yaml", asvs_data)
        self.assertTrue(self.validator.validate_file(asvs_path))

        capec_data = {
            "meta": {"edition": "webapp", "component": "capec", "version": "3.0"},
            54: {"owasp_asvs": ["1.1.1", "1.1.2"]},
            113: {},
        }
        capec_path = self._write_yaml("webapp-capec-3.0.yaml", capec_data)
        self.assertTrue(self.validator.validate_file(capec_path))

        mastg_data = {
            "meta": {"edition": "mobileapp", "component": "mastg", "version": "2.0"},
            "0200": {"owasp_maswe": ["0002"]},
        }
        mastg_path = self._write_yaml("mobileapp-mastg-2.0.yaml", mastg_data)
        self.assertTrue(self.validator.validate_file(mastg_path))

        maswe_data = {
            "meta": {"edition": "mobileapp", "component": "maswe", "version": "2.0"},
            "0001": {"owasp_mastg": ["0207"]},
        }
        maswe_path = self._write_yaml("mobileapp-maswe-2.0.yaml", maswe_data)
        self.assertTrue(self.validator.validate_file(maswe_path))

        bad_asvs_data = {
            "meta": {"edition": "webapp", "component": "asvs", "version": "3.0"},
            "15.3.5 15.3.6": {},
            " 1.1.1 ": {},
            "bad_id": {},
        }
        validator2 = SourceValidator()
        bad_asvs_path = self._write_yaml("bad-asvs-1.0.yaml", bad_asvs_data)
        self.assertFalse(validator2.validate_file(bad_asvs_path))
        self.assertTrue(any("contains whitespace" in e for e in validator2.errors))
        self.assertTrue(any("contains surrounding whitespace" in e for e in validator2.errors))
        self.assertTrue(any("does not match pattern" in e for e in validator2.errors))

        bad_capec_data = {
            "meta": {"edition": "webapp", "component": "capec", "version": "3.0"},
            113: {"owasp_asvs": ["15.3.5 15.3.6"]},
        }
        validator3 = SourceValidator()
        bad_capec_path = self._write_yaml("bad-capec-1.0.yaml", bad_capec_data)
        self.assertFalse(validator3.validate_file(bad_capec_path))
        self.assertTrue(any("space-separated" in e for e in validator3.errors))

    def test_catalog_non_dict_entry(self) -> None:
        data = {
            "meta": {"edition": "webapp", "component": "asvs", "version": "3.0"},
            "1.1.1": "not a dictionary",
            "1.1.2": ["list", "value"],
        }
        path = self._write_yaml("test-asvs-non-dict.yaml", data)
        res = self.validator.validate_file(path)
        self.assertFalse(res)
        self.assertTrue(any("must be a dictionary" in e for e in self.validator.errors))

    def test_asvs_compact_range_rejected(self) -> None:
        data = {
            "meta": {"edition": "webapp", "component": "mappings", "version": "3.0"},
            "suits": [
                {
                    "name": "Test",
                    "cards": [
                        {
                            "id": "T1",
                            "owasp_asvs": ["13.3.1-3"],
                        }
                    ],
                }
            ],
        }
        path = self._write_yaml("range-mappings.yaml", data)
        res = self.validator.validate_file(path)
        self.assertFalse(res)
        self.assertTrue(any("must match dotted numeric pattern" in e for e in self.validator.errors))

    def test_stride_invalid_enum_rejected(self) -> None:
        data = {
            "meta": {"edition": "webapp", "component": "mappings", "version": "3.0"},
            "suits": [
                {
                    "name": "Test",
                    "cards": [
                        {
                            "id": "T1",
                            "stride": ["InvalidStrideEnum"],
                        }
                    ],
                }
            ],
        }
        path = self._write_yaml("bad-stride-mappings.yaml", data)
        res = self.validator.validate_file(path)
        self.assertFalse(res)
        self.assertTrue(any("Invalid STRIDE token 'InvalidStrideEnum'" in e for e in self.validator.errors))

    def test_asvs_catalog_integrity_missing_id_rejected(self) -> None:
        asvs_data = {
            "meta": {"edition": "webapp", "component": "asvs", "version": "3.0"},
            "1.1.1": {},
            "1.1.2": {},
        }
        self._write_yaml("webapp-asvs-3.0.yaml", asvs_data)

        mappings_data = {
            "meta": {"edition": "webapp", "component": "mappings", "version": "3.0"},
            "suits": [
                {
                    "name": "Auth",
                    "cards": [
                        {
                            "id": "A1",
                            "owasp_asvs": ["1.1.1", "999.3.3"],
                        }
                    ],
                }
            ],
        }
        mappings_path = self._write_yaml("webapp-mappings-3.0.yaml", mappings_data)
        validator = SourceValidator(catalog_dir=self.temp_dir)
        res = validator.validate_file(mappings_path)
        self.assertFalse(res)
        self.assertTrue(any("does not exist in authoritative catalog" in e for e in validator.errors))

    def test_generic_yaml_file(self) -> None:
        path = self._write_yaml(
            "generic.yaml",
            {
                "meta": {"edition": "generic", "component": "misc", "version": "1.0"},
                "key": "value",
            },
        )
        self.assertTrue(self.validator.validate_file(path))

        empty_data_path = self._write_yaml("empty_dict.yaml", {})
        validator2 = SourceValidator()
        self.assertFalse(validator2.validate_file(empty_data_path))
        self.assertTrue(any("Missing or invalid 'meta'" in e for e in validator2.errors))

    def test_meta_null_values_rejected(self) -> None:
        for field in ["edition", "component", "version"]:
            meta = {"edition": "webapp", "component": "cards", "version": "3.0"}
            meta[field] = None
            path = self._write_yaml(f"null_{field}.yaml", {"meta": meta, "suits": []})
            validator = SourceValidator()
            self.assertFalse(validator.validate_file(path))
            self.assertTrue(any(f"missing required key '{field}'" in e for e in validator.errors))

    def test_cards_dispatch_by_component_metadata(self) -> None:
        bad_against_data = {
            "meta": {
                "edition": "against-appsec",
                "component": "cards",
                "version": "1.0",
            },
            "suits": [
                {
                    "name": "Cards Against AppSec",
                    "cards": [{"id": "CA1"}],
                }
            ],
        }
        bad_path = self._write_yaml("against-appsec-1.0-en.yaml", bad_against_data)
        validator = SourceValidator()
        self.assertFalse(validator.validate_file(bad_path))
        self.assertTrue(any("Suit entry missing 'id'" in e for e in validator.errors))

        valid_against_data = {
            "meta": {
                "edition": "against-appsec",
                "component": "cards",
                "version": "1.0",
            },
            "suits": [
                {
                    "id": "CAAB",
                    "name": "Cards Against AppSec",
                    "cards": [{"id": "CA1"}],
                }
            ],
        }
        valid_path = self._write_yaml("against-appsec-valid.yaml", valid_against_data)
        validator2 = SourceValidator()
        self.assertTrue(validator2.validate_file(valid_path))

    def test_asvs_catalog_resolution_via_labels(self) -> None:
        self._write_yaml(
            "webapp-asvs-3.0.yaml",
            {
                "meta": {"edition": "webapp", "component": "asvs", "version": "3.0"},
                "2.3.2": {},
            },
        )
        valid_companion_data = {
            "meta": {"edition": "companion", "component": "mappings", "version": "1.0"},
            "labels": {"owasp_asvs": "ASVS (5.0)"},
            "suits": [
                {
                    "id": "C",
                    "name": "Companion",
                    "cards": [{"id": "C1", "owasp_asvs": ["2.3.2"]}],
                }
            ],
        }
        valid_path = self._write_yaml("companion-mappings-1.0.yaml", valid_companion_data)
        validator = SourceValidator(catalog_dir=self.temp_dir)
        self.assertTrue(validator.validate_file(valid_path))

        bad_companion_data = {
            "meta": {"edition": "companion", "component": "mappings", "version": "1.0"},
            "labels": {"owasp_asvs": "ASVS (5.0)"},
            "suits": [
                {
                    "id": "C",
                    "name": "Companion",
                    "cards": [{"id": "C1", "owasp_asvs": ["999.3.3"]}],
                }
            ],
        }
        bad_path = self._write_yaml("companion-mappings-bad.yaml", bad_companion_data)
        validator2 = SourceValidator(catalog_dir=self.temp_dir)
        self.assertFalse(validator2.validate_file(bad_path))
        self.assertTrue(any("does not exist in authoritative catalog" in e for e in validator2.errors))

    def test_asvs_unresolved_catalog_rejected(self) -> None:
        isolated_dir = Path(tempfile.mkdtemp())
        try:
            mappings_data = {
                "meta": {
                    "edition": "unknown",
                    "component": "mappings",
                    "version": "9.9",
                },
                "suits": [
                    {
                        "id": "U",
                        "name": "Unknown",
                        "cards": [{"id": "U1", "owasp_asvs": ["1.1.1"]}],
                    }
                ],
            }
            unresolved_path = isolated_dir / "unknown-mappings-9.9.yaml"
            with open(unresolved_path, "w", encoding="utf-8") as f:
                yaml.dump(mappings_data, f)

            validator = SourceValidator()
            self.assertFalse(validator.validate_file(unresolved_path))
            self.assertTrue(any("Unable to resolve authoritative ASVS catalog" in e for e in validator.errors))
        finally:
            shutil.rmtree(isolated_dir, ignore_errors=True)

    def test_asvs_whitespace_padded_rejected(self) -> None:
        data = {
            "meta": {"edition": "webapp", "component": "mappings", "version": "3.0"},
            "suits": [
                {
                    "name": "Test",
                    "cards": [
                        {
                            "id": "T1",
                            "owasp_asvs": [" 1.1.1 "],
                        }
                    ],
                }
            ],
        }
        path = self._write_yaml("padded-mappings.yaml", data)
        res = self.validator.validate_file(path)
        self.assertFalse(res)
        self.assertTrue(any("contains surrounding whitespace" in e for e in self.validator.errors))

    def test_duplicate_yaml_keys_rejected(self) -> None:
        raw_yaml = """
meta:
  edition: webapp
  component: mappings
  version: "3.0"
suits:
  - id: T1
    name: Test 1
    cards: []
suits:
  - id: T2
    name: Test 2
    cards: []
"""
        path = self._write_yaml("duplicate_key.yaml", raw_yaml)
        res = self.validator.validate_file(path)
        self.assertFalse(res)
        self.assertTrue(any("Duplicate YAML key" in e for e in self.validator.errors))

    def test_explicit_asvs_version_does_not_fallback_to_unmatched_edition_catalog(
        self,
    ) -> None:
        isolated_dir = Path(tempfile.mkdtemp())
        try:
            asvs_5_catalog = {
                "meta": {"edition": "webapp", "component": "asvs", "version": "3.0"},
                "5.1.1": {"name": "Auth requirement"},
            }
            with open(isolated_dir / "webapp-asvs-3.0.yaml", "w", encoding="utf-8") as f:
                yaml.dump(asvs_5_catalog, f)

            mappings_data = {
                "meta": {
                    "edition": "webapp",
                    "component": "mappings",
                    "version": "3.0",
                },
                "labels": {"owasp_asvs": "OWASP ASVS (v4.0)"},
                "suits": [
                    {
                        "id": "T",
                        "name": "Test",
                        "cards": [{"id": "T1", "owasp_asvs": ["5.1.1"]}],
                    }
                ],
            }
            mapping_path = isolated_dir / "webapp-mappings-3.0.yaml"
            with open(mapping_path, "w", encoding="utf-8") as f:
                yaml.dump(mappings_data, f)

            validator = SourceValidator()
            self.assertFalse(validator.validate_file(mapping_path))
            self.assertTrue(any("Unable to resolve authoritative ASVS catalog" in e for e in validator.errors))
        finally:
            shutil.rmtree(isolated_dir, ignore_errors=True)

    def test_mastg_scalar_reference_rejected(self) -> None:
        mastg_data = {
            "meta": {"edition": "mobileapp", "component": "mastg", "version": "2.0"},
            "0200": {
                "title": "Testing Network Communication",
                "owasp_maswe": "0002",
            },
        }
        path = self._write_yaml("mobileapp-mastg-2.0.yaml", mastg_data)
        res = self.validator.validate_file(path)
        self.assertFalse(res)
        self.assertTrue(any("'owasp_maswe' must be a list of strings" in e for e in self.validator.errors))

    def test_mastg_valid_list_references_accepted(self) -> None:
        mastg_data = {
            "meta": {"edition": "mobileapp", "component": "mastg", "version": "2.0"},
            "0200": {
                "title": "Testing Network Communication",
                "owasp_maswe": ["0002"],
                "owasp_mastg": ["0100"],
            },
        }
        path = self._write_yaml("mobileapp-mastg-2.0.yaml", mastg_data)
        res = self.validator.validate_file(path)
        self.assertTrue(res)

    def test_mobile_card_mapping_scalar_reference_rejected(self) -> None:
        data = {
            "meta": {"edition": "mobileapp", "component": "mappings", "version": "2.0"},
            "suits": [
                {
                    "id": "PC",
                    "name": "Platform & Code",
                    "cards": [
                        {
                            "id": "PC2",
                            "owasp_mastg": "0289",
                        }
                    ],
                }
            ],
        }
        path = self._write_yaml("mobileapp-mappings-2.0.yaml", data)
        res = self.validator.validate_file(path)
        self.assertFalse(res)
        self.assertTrue(any("'owasp_mastg' must be a list of strings" in e for e in self.validator.errors))

    def test_mobile_catalog_non_string_key_rejected(self) -> None:
        maswe_data = {
            "meta": {"edition": "mobileapp", "component": "maswe", "version": "2.0"},
            1: {
                "title": "Insecure Data Storage",
                "owasp_masvs": ["MASVS-STORAGE-1"],
            },
        }
        path = self._write_yaml("mobileapp-maswe-2.0.yaml", maswe_data)
        res = self.validator.validate_file(path)
        self.assertFalse(res)
        self.assertTrue(any("MASWE catalog key 1 must be a string" in e for e in self.validator.errors))

    def test_maswe_scalar_masvs_reference_rejected(self) -> None:
        maswe_data = {
            "meta": {"edition": "mobileapp", "component": "maswe", "version": "2.0"},
            "0001": {
                "title": "Insecure Data Storage",
                "owasp_masvs": "MASVS-STORAGE-1",
            },
        }
        path = self._write_yaml("mobileapp-maswe-2.0.yaml", maswe_data)
        res = self.validator.validate_file(path)
        self.assertFalse(res)
        self.assertTrue(any("'owasp_masvs' must be a list of strings" in e for e in self.validator.errors))

    def test_legacy_asvs_4_catalog_resolution_and_validation(self) -> None:
        isolated_dir = Path(tempfile.mkdtemp())
        try:
            import json

            json_catalog = {
                "requirements": [
                    {"req_id": "V1.1.1", "req_description": "Requirement 1.1.1"},
                    {"req_id": "V1.2.1", "req_description": "Requirement 1.2.1"},
                ]
            }
            catalog_file = isolated_dir / "OWASP_Application_Security_Verification_Standard_4.0.3.flat.json"
            with open(catalog_file, "w", encoding="utf-8") as f:
                json.dump(json_catalog, f)

            valid_mapping = {
                "meta": {
                    "edition": "webapp",
                    "component": "mappings",
                    "version": "2.2",
                },
                "labels": {"owasp_asvs": "OWASP ASVS (v4.0)"},
                "suits": [
                    {
                        "id": "VE",
                        "name": "Encoding",
                        "cards": [{"id": "VE2", "owasp_asvs": ["1.1.1", "1.2.1"]}],
                    }
                ],
            }
            mapping_path = isolated_dir / "webapp-mappings-2.2.yaml"
            with open(mapping_path, "w", encoding="utf-8") as f:
                yaml.dump(valid_mapping, f)

            validator = SourceValidator(catalog_dir=isolated_dir)
            self.assertTrue(validator.validate_file(mapping_path))

            invalid_mapping = {
                "meta": {
                    "edition": "webapp",
                    "component": "mappings",
                    "version": "2.2",
                },
                "labels": {"owasp_asvs": "OWASP ASVS (v4.0)"},
                "suits": [
                    {
                        "id": "VE",
                        "name": "Encoding",
                        "cards": [{"id": "VE2", "owasp_asvs": ["99.99.99"]}],
                    }
                ],
            }
            invalid_path = isolated_dir / "webapp-mappings-2.2-bad.yaml"
            with open(invalid_path, "w", encoding="utf-8") as f:
                yaml.dump(invalid_mapping, f)

            validator2 = SourceValidator(catalog_dir=isolated_dir)
            self.assertFalse(validator2.validate_file(invalid_path))
            self.assertTrue(any("does not exist in authoritative catalog" in e for e in validator2.errors))
        finally:
            shutil.rmtree(isolated_dir, ignore_errors=True)

    def test_mappings_missing_suit_or_card_id_rejected(self) -> None:
        missing_suit_id = {
            "meta": {"edition": "webapp", "component": "mappings", "version": "3.0"},
            "suits": [
                {
                    "name": "Auth",
                    "cards": [{"id": "AT1"}],
                }
            ],
        }
        path1 = self._write_yaml("missing-suit-id-mappings.yaml", missing_suit_id)
        validator1 = SourceValidator()
        self.assertFalse(validator1.validate_file(path1))
        self.assertTrue(any("Suit entry missing 'id'" in e for e in validator1.errors))

        missing_card_id = {
            "meta": {"edition": "webapp", "component": "mappings", "version": "3.0"},
            "suits": [
                {
                    "id": "AT",
                    "name": "Auth",
                    "cards": [{"name": "Card without id"}],
                }
            ],
        }
        path2 = self._write_yaml("missing-card-id-mappings.yaml", missing_card_id)
        validator2 = SourceValidator()
        self.assertFalse(validator2.validate_file(path2))
        self.assertTrue(any("Card missing 'id' in suit 'Auth'" in e for e in validator2.errors))

    def test_cre_legacy_mappings_accepted_and_missing_value_rejected(self) -> None:
        valid_cre = {
            "meta": {"edition": "webapp", "component": "mappings", "version": "1.20"},
            "suits": [
                {
                    "name": "Data validation & encoding",
                    "cards": [
                        {"value": "2", "cre": ["308-515"]},
                        {"value": "3", "cre": ["010-308"]},
                    ],
                }
            ],
        }
        path_valid = self._write_yaml("cre-mappings.yaml", valid_cre)
        validator1 = SourceValidator()
        self.assertTrue(validator1.validate_file(path_valid))

        missing_value_cre = {
            "meta": {"edition": "webapp", "component": "mappings", "version": "1.20"},
            "suits": [
                {
                    "name": "Data validation & encoding",
                    "cards": [
                        {"cre": ["308-515"]},
                    ],
                }
            ],
        }
        path_invalid = self._write_yaml("cre-mappings-bad.yaml", missing_value_cre)
        validator2 = SourceValidator()
        self.assertFalse(validator2.validate_file(path_invalid))
        self.assertTrue(
            any("Card missing 'value' in suit 'Data validation & encoding'" in e for e in validator2.errors)
        )

    def test_capec_map_quoted_string_or_negative_key_rejected(self) -> None:
        data = {
            "meta": {"edition": "webapp", "component": "mappings", "version": "3.0"},
            "suits": [
                {
                    "id": "CM",
                    "name": "CapecMapTest",
                    "cards": [
                        {
                            "id": "CM1",
                            "capec_map": {
                                "116": {"owasp_asvs": ["1.1.1"]},
                                -5: {"owasp_asvs": ["1.1.1"]},
                            },
                        }
                    ],
                }
            ],
        }
        path = self._write_yaml("bad-capec-map-types.yaml", data)
        res = self.validator.validate_file(path)
        self.assertFalse(res)
        self.assertTrue(any("CAPEC key '116' must be an integer" in e for e in self.validator.errors))
        self.assertTrue(any("CAPEC key -5 must be an integer" in e for e in self.validator.errors))

    def test_capec_catalog_quoted_string_or_negative_key_rejected(self) -> None:
        bad_capec_catalog = {
            "meta": {"edition": "webapp", "component": "capec", "version": "3.0"},
            "54": {"owasp_asvs": ["1.1.1"]},
            -10: {},
        }
        path = self._write_yaml("webapp-capec-3.0.yaml", bad_capec_catalog)
        res = self.validator.validate_file(path)
        self.assertFalse(res)
        self.assertTrue(any("CAPEC catalog key '54' must be an integer" in e for e in self.validator.errors))
        self.assertTrue(any("CAPEC catalog key -10 must be an integer" in e for e in self.validator.errors))


class TestCLIAndMain(unittest.TestCase):
    """Test suite for argument parsing and CLI main() function."""

    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_parse_arguments(self) -> None:
        args = parse_arguments(["file1.yaml", "file2.yaml"])
        self.assertEqual(args.files, ["file1.yaml", "file2.yaml"])
        self.assertIsNone(args.source_dir)

        args2 = parse_arguments(["--source-dir", "source/"])
        self.assertEqual(args2.source_dir, "source/")

    def test_main_no_files_specified(self) -> None:
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            code = main([])
            self.assertEqual(code, 0)
            self.assertIn("No source files specified", fake_out.getvalue())

    def test_main_invalid_source_dir(self) -> None:
        with patch("sys.stderr", new=io.StringIO()) as fake_err:
            code = main(["--source-dir", str(self.temp_dir / "nonexistent")])
            self.assertEqual(code, 1)
            self.assertIn("does not exist", fake_err.getvalue())

    def test_main_valid_file_passes(self) -> None:
        file_path = self.temp_dir / "valid.yaml"
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(
                {
                    "meta": {"edition": "test", "component": "misc", "version": "1.0"},
                    "key": "value",
                },
                f,
            )

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            code = main([str(file_path)])
            self.assertEqual(code, 0)
            self.assertIn("[PASSED]", fake_out.getvalue())

    def test_main_invalid_file_fails(self) -> None:
        file_path = self.temp_dir / "bad.yaml"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(":")

        with patch("sys.stderr", new=io.StringIO()) as fake_err:
            code = main([str(file_path)])
            self.assertEqual(code, 1)
            self.assertIn("[FAILED]", fake_err.getvalue())

    def test_main_source_dir_glob(self) -> None:
        file1 = self.temp_dir / "a.yaml"
        with open(file1, "w", encoding="utf-8") as f:
            yaml.dump(
                {
                    "meta": {"edition": "test", "component": "misc", "version": "1.0"},
                    "key": "val1",
                },
                f,
            )

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            code = main(["--source-dir", str(self.temp_dir)])
            self.assertEqual(code, 0)
            self.assertIn("Validating 1 source file(s)", fake_out.getvalue())

    def test_main_default_argv(self) -> None:
        with patch("sys.argv", ["validate_source_files.py"]):
            code = main()
            self.assertEqual(code, 0)

    def test_main_source_dir_glob_supports_yaml_and_yml(self) -> None:
        file_yaml = self.temp_dir / "file1.yaml"
        file_yml = self.temp_dir / "file2.yml"
        for f in (file_yaml, file_yml):
            with open(f, "w", encoding="utf-8") as fh:
                yaml.dump(
                    {
                        "meta": {
                            "edition": "test",
                            "component": "misc",
                            "version": "1.0",
                        },
                        "key": "val",
                    },
                    fh,
                )

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            code = main(["--source-dir", str(self.temp_dir)])
            self.assertEqual(code, 0)
            self.assertIn("Validating 2 source file(s)", fake_out.getvalue())


if __name__ == "__main__":
    unittest.main()
