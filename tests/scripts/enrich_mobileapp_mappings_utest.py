import tempfile
import unittest
from pathlib import Path

import scripts.enrich_mobileapp_mappings as enricher


class TestMobileappMappingsEnrichment(unittest.TestCase):
    def test_enrich_mappings_merges_mastg_siblings_and_maswe_metadata(self) -> None:
        mappings = {
            "meta": {"edition": "mobileapp"},
            "suits": [
                {
                    "cards": [
                        {
                            "id": "PC8",
                            "owasp_mastg": ["0357"],
                            "owasp_mastg_best": [],
                            "owasp_mastg_know": ["0104"],
                            "owasp_maswe": [],
                        }
                    ]
                }
            ],
        }
        mastg = {"0357": {"owasp_maswe": ["0018"], "owasp_mastg_know": ["0020", "0117"], "owasp_mastg_best": ["0049"]}}
        maswe = {
            "0018": {
                "owasp_mas_threat": {"0018": "Attackers can access sensitive data and functionality exposed by app components."},
                "owasp_mas_attack": {
                    "0038": "Invoking exported or unprotected app components from another app installed on the device.",
                    "0039": "Connecting to open ports or local services exposed by the app.",
                },
            }
        }

        card = enricher.enrich_mappings(mappings, mastg, maswe)["suits"][0]["cards"][0]

        self.assertEqual(["0357"], card["owasp_mastg"])
        self.assertEqual(["0049"], card["owasp_mastg_best"])
        self.assertEqual(["0104", "0020", "0117"], card["owasp_mastg_know"])
        self.assertEqual(["0018"], card["owasp_maswe"])
        self.assertEqual(maswe["0018"]["owasp_mas_attack"], card["attack_vector"])
        self.assertEqual(maswe["0018"]["owasp_mas_threat"], card["threat"])

    def test_enrich_mappings_preserves_placeholder_mastg_value(self) -> None:
        mappings = {"suits": [{"cards": [{"id": "PCA", "owasp_mastg": ["-"]}]}]}

        card = enricher.enrich_mappings(mappings, {}, {})["suits"][0]["cards"][0]

        self.assertEqual(["-"], card["owasp_mastg"])
        self.assertEqual([], card["owasp_maswe"])

    def test_enrich_mappings_preserves_legacy_mastg_value(self) -> None:
        mappings = {"suits": [{"cards": [{"id": "CMJ", "owasp_mastg": ["0043"]}]}]}

        with self.assertLogs(level="WARNING"):
            card = enricher.enrich_mappings(mappings, {}, {})["suits"][0]["cards"][0]

        self.assertEqual(["0043"], card["owasp_mastg"])
        self.assertEqual([], card["owasp_maswe"])

    def test_save_yaml_file_keeps_scalar_lists_inline(self) -> None:
        data = {"suits": [{"cards": [{"id": "PC2", "owasp_mastg": ["0289", "0290"], "capec": [37, 155]}]}]}
        with tempfile.TemporaryDirectory() as directory:
            output_path = Path(directory) / "mapping.yaml"
            enricher.save_yaml_file(output_path, data)
            content = output_path.read_text(encoding="utf-8")

        self.assertIn("owasp_mastg: ['0289', '0290']", content)
        self.assertIn("capec: [37, 155]", content)
        self.assertIn("suits:\n- cards:", content)

    def test_load_yaml_file_rejects_duplicate_keys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "mapping.yaml"
            input_path.write_text("suits: []\nsuits: []\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Duplicate YAML key"):
                enricher.load_yaml_file(input_path)


if __name__ == "__main__":
    unittest.main()