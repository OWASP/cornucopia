#!/usr/bin/env python3
import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch

import scripts.scaffold_cards as scaffold

if "unittest.util" in __import__("sys").modules:
    # Show full diff in self.assertEqual.
    __import__("sys").modules["unittest.util"]._MAX_LENGTH = 999999999


def _make_data(edition="eop", version="1.0", language="EN", suits=None):
    """Return a minimal cards data dict whose meta values pass safe_component validation."""
    if suits is None:
        suits = [
            {
                "id": "TS",
                "name": "Test Suit",
                "cards": [{"id": "TSA", "value": "A", "desc": "Card A"}, {"id": "TSB", "value": "B", "desc": "Card B"}],
            }
        ]
    return {"meta": {"edition": edition, "version": version, "language": language}, "suits": suits}


class TestExtractSuitFolderName(unittest.TestCase):
    def test_lowercases_name(self):
        self.assertEqual(scaffold.extract_suit_folder_name("Spoofing"), "spoofing")

    def test_replaces_spaces_with_hyphens(self):
        self.assertEqual(scaffold.extract_suit_folder_name("Denial Of Service"), "denial-of-service")

    def test_strips_leading_trailing_whitespace(self):
        self.assertEqual(scaffold.extract_suit_folder_name("  Tampering  "), "tampering")


class TestScaffoldCards(unittest.TestCase):
    """Tests for main(): directory layout, non-overwrite semantics, and path validation."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.patched_root = Path(self.temp_dir) / "data" / "cards"
        self.patched_root.mkdir(parents=True)
        self._root_patcher = patch.object(scaffold, "ROOT", self.patched_root)
        self._root_patcher.start()

        self.test_input_file = Path(__file__).parent.parent / "test_files" / "source" / "scaffold-cards-1.0-en.yaml"

    def tearDown(self) -> None:
        self._root_patcher.stop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _run(self, yaml_path: str) -> int:
        """Run main() and return the exit code (0 = success, 1 = error)."""
        with patch("sys.argv", ["scaffold_cards.py", yaml_path]):
            try:
                scaffold.main()
                return 0
            except SystemExit as exc:
                return int(exc.code) if exc.code is not None else 0

    def _write_yaml(self, data: dict) -> str:
        import yaml as _yaml

        path = Path(self.temp_dir) / "input.yaml"
        path.write_text(_yaml.dump(data), encoding="utf-8")
        return str(path)

    # --- Directory layout ---

    def test_creates_correct_directory_structure(self):
        """Creates edition/suit/card directory tree from the YAML file."""
        self._run(str(self.test_input_file))
        base = self.patched_root / "scaffold-cards-1.0-en" / "test-suit"
        self.assertTrue(base.is_dir())
        for card_id in ("TSA", "TSB"):
            self.assertTrue((base / card_id).is_dir())
            self.assertTrue((base / card_id / "explanation.md").exists())
            self.assertTrue((base / card_id / "technical-note.md").exists())

    def test_explanation_md_contains_template_and_technical_note_is_empty(self):
        """explanation.md is seeded with the template; technical-note.md starts empty."""
        self._run(str(self.test_input_file))
        card_dir = self.patched_root / "scaffold-cards-1.0-en" / "test-suit" / "TSA"
        content = (card_dir / "explanation.md").read_text(encoding="utf-8")
        self.assertIn("## Scenario:", content)
        self.assertIn("## Threat Modeling", content)
        self.assertEqual((card_dir / "technical-note.md").read_text(encoding="utf-8"), "")

    def test_does_not_overwrite_existing_files(self):
        """Running main() a second time leaves existing files untouched."""
        self._run(str(self.test_input_file))
        card_dir = self.patched_root / "scaffold-cards-1.0-en" / "test-suit" / "TSA"
        for filename, custom in [("explanation.md", "# explanation notes"), ("technical-note.md", "# tech notes")]:
            (card_dir / filename).write_text(custom, encoding="utf-8")

        self._run(str(self.test_input_file))
        self.assertEqual((card_dir / "explanation.md").read_text(encoding="utf-8"), "# explanation notes")
        self.assertEqual((card_dir / "technical-note.md").read_text(encoding="utf-8"), "# tech notes")

    # --- Path validation (safe_component) ---

    def test_rejects_edition_with_traversal(self):
        data = _make_data(edition="..")
        self.assertEqual(self._run(self._write_yaml(data)), 1)

    def test_rejects_edition_with_uppercase(self):
        data = _make_data(edition="EOP")
        self.assertEqual(self._run(self._write_yaml(data)), 1)

    def test_rejects_edition_with_slash(self):
        data = _make_data(edition="foo/bar")
        self.assertEqual(self._run(self._write_yaml(data)), 1)

    def test_rejects_version_with_traversal(self):
        data = _make_data(version="..")
        self.assertEqual(self._run(self._write_yaml(data)), 1)

    def test_rejects_version_with_letters(self):
        data = _make_data(version="1.0a")
        self.assertEqual(self._run(self._write_yaml(data)), 1)

    def test_rejects_language_with_traversal(self):
        data = _make_data(language="../../bad")
        self.assertEqual(self._run(self._write_yaml(data)), 1)

    def test_rejects_suit_name_with_traversal(self):
        data = _make_data(
            suits=[{"id": "TS", "name": "../../evil", "cards": [{"id": "TSA", "value": "A", "desc": "ok"}]}]
        )
        self.assertEqual(self._run(self._write_yaml(data)), 1)

    def test_rejects_card_id_with_traversal(self):
        data = _make_data(
            suits=[{"id": "TS", "name": "Test Suit", "cards": [{"id": "../../evil", "value": "A", "desc": "bad"}]}]
        )
        self.assertEqual(self._run(self._write_yaml(data)), 1)

    def test_accepts_valid_edition(self):
        data = _make_data(edition="eop")
        self.assertEqual(self._run(self._write_yaml(data)), 0)

    def test_accepts_valid_edition_with_hyphen(self):
        data = _make_data(edition="my-edition")
        self.assertEqual(self._run(self._write_yaml(data)), 0)

    def test_accepts_valid_version_with_dot(self):
        data = _make_data(version="5.0")
        self.assertEqual(self._run(self._write_yaml(data)), 0)

    def test_accepts_valid_version_single_digit(self):
        data = _make_data(version="3")
        self.assertEqual(self._run(self._write_yaml(data)), 0)

    def test_accepts_valid_language(self):
        data = _make_data(language="EN")
        self.assertEqual(self._run(self._write_yaml(data)), 0)

    def test_accepts_valid_language_with_underscore(self):
        data = _make_data(language="pt_BR")
        self.assertEqual(self._run(self._write_yaml(data)), 0)

    # --- Missing/Invalid YAML Keys and Structure ---

    def test_rejects_missing_meta(self):
        data = _make_data()
        del data["meta"]
        self.assertEqual(self._run(self._write_yaml(data)), 1)

    def test_rejects_missing_edition(self):
        data = _make_data()
        del data["meta"]["edition"]
        self.assertEqual(self._run(self._write_yaml(data)), 1)

    def test_rejects_missing_version(self):
        data = _make_data()
        del data["meta"]["version"]
        self.assertEqual(self._run(self._write_yaml(data)), 1)

    def test_rejects_missing_language(self):
        data = _make_data()
        del data["meta"]["language"]
        self.assertEqual(self._run(self._write_yaml(data)), 1)

    def test_rejects_missing_suits(self):
        data = _make_data()
        del data["suits"]
        self.assertEqual(self._run(self._write_yaml(data)), 1)

    def test_rejects_missing_suit_name(self):
        data = _make_data()
        del data["suits"][0]["name"]
        self.assertEqual(self._run(self._write_yaml(data)), 1)

    def test_rejects_missing_suit_cards(self):
        data = _make_data()
        del data["suits"][0]["cards"]
        self.assertEqual(self._run(self._write_yaml(data)), 1)

    def test_rejects_missing_card_id(self):
        data = _make_data()
        del data["suits"][0]["cards"][0]["id"]
        self.assertEqual(self._run(self._write_yaml(data)), 1)


if __name__ == "__main__":
    unittest.main()
