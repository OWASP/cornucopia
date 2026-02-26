"""
Unit tests for translation tag checking.

Tests the TranslationChecker class with mock data.
"""

import unittest
import yaml
import re
import sys
from pathlib import Path

# Add scripts directory to path
scripts_path = Path(__file__).parent.parent.parent / "scripts"
sys.path.insert(0, str(scripts_path))

from check_translations import TranslationChecker  # type: ignore[import-not-found]  # noqa: E402


class TestTranslationCheckerUnit(unittest.TestCase):
    """Unit tests for TranslationChecker using mock files."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        # Use test_files directory for mock data
        # Navigate from cornucopia/scripts -> cornucopia -> tests/test_files/source
        script_dir = Path(__file__).parent
        cornucopia_dir = script_dir.parent
        self.test_source_dir = cornucopia_dir / "tests" / "test_files" / "source"
        self.checker = TranslationChecker(self.test_source_dir)

    def test_extract_tags_from_english(self) -> None:
        """Test extracting tags from an English YAML file."""
        english_file = self.test_source_dir / "test-cards-1.0-en.yaml"
        tags = self.checker.extract_tags(english_file)

        self.assertIn("T00001", tags)
        self.assertIn("T00002", tags)
        self.assertIn("T00003", tags)
        self.assertIn("T00004", tags)
        self.assertEqual(tags["T00001"], "This is the first test tag")

    def test_detect_missing_tags(self) -> None:
        """Test detection of missing tags in translation."""
        results = self.checker.check_translations()

        # Spanish file is missing T00004
        self.assertIn("test-cards-1.0", results)
        self.assertIn("es", results["test-cards-1.0"])
        self.assertIn("T00004", results["test-cards-1.0"]["es"]["missing"])

    def test_detect_untranslated_tags(self) -> None:
        """Test detection of untranslated tags (identical to English)."""
        results = self.checker.check_translations()

        # Spanish file has T00002 identical to English
        self.assertIn("test-cards-1.0", results)
        self.assertIn("es", results["test-cards-1.0"])
        self.assertIn("T00002", results["test-cards-1.0"]["es"]["untranslated"])

    def test_detect_empty_tags(self) -> None:
        """Test detection of empty tag values."""
        results = self.checker.check_translations()

        # Spanish file has T00003 empty
        self.assertIn("test-cards-1.0", results)
        self.assertIn("es", results["test-cards-1.0"])
        self.assertIn("T00003", results["test-cards-1.0"]["es"]["empty"])

    def test_generate_report_with_issues(self) -> None:
        """Test markdown report generation when issues exist."""
        self.checker.check_translations()
        report = self.checker.generate_markdown_report()

        self.assertIn("Translation Check Report", report)
        self.assertIn("Spanish", report)
        self.assertIn("Missing Tags", report)
        self.assertIn("Untranslated Tags", report)
        self.assertIn("Empty Tags", report)

    def test_tag_format_validation(self) -> None:
        """Test that tags follow the T0xxxx format."""
        tag_pattern = re.compile(r"^T0\d{4,5}$")

        english_file = self.test_source_dir / "test-cards-1.0-en.yaml"
        tags = self.checker.extract_tags(english_file)

        for tag_id in tags.keys():
            self.assertIsNotNone(tag_pattern.match(tag_id), f"Tag {tag_id} doesn't match format T0xxxx")

    def test_no_duplicate_tags(self) -> None:
        """Test that files don't have duplicate T0xxx tags."""
        english_file = self.test_source_dir / "test-cards-1.0-en.yaml"

        with open(english_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if data and "paragraphs" in data:
            seen_ids = set()
            duplicates = []

            for paragraph in data["paragraphs"]:
                if "sentences" in paragraph:
                    for sentence in paragraph["sentences"]:
                        tag_id = sentence.get("id", "")
                        if tag_id.startswith("T0"):
                            if tag_id in seen_ids:
                                duplicates.append(tag_id)
                            seen_ids.add(tag_id)

            self.assertEqual(len(duplicates), 0, f"Duplicate tags found: {duplicates}")

    def test_file_groups(self) -> None:
        """Test that files are correctly grouped by base name."""
        file_groups = self.checker.get_file_groups()

        self.assertIn("test-cards-1.0", file_groups)
        files = [f.name for f in file_groups["test-cards-1.0"]]
        self.assertIn("test-cards-1.0-en.yaml", files)
        self.assertIn("test-cards-1.0-es.yaml", files)


class TestWhitespaceHandling(unittest.TestCase):

    def setUp(self) -> None:
        self.checker = TranslationChecker(Path("."))

    def test_whitespace_only_detected_as_empty(self) -> None:
        english_tags = {"T00001": "Login", "T00002": "Password"}
        trans_tags = {"T00001": "Login", "T00002": "   "}  # Whitespace only

        result = self.checker._check_translation_tags(english_tags, trans_tags)

        self.assertIn("T00002", result["empty"], "Whitespace-only translation should be detected as empty")

    def test_tabs_and_newlines_detected_as_empty(self) -> None:
        english_tags = {"T00001": "Submit", "T00002": "Cancel"}
        trans_tags = {"T00001": "Submit", "T00002": "\t \n"}  # Tabs and newlines

        result = self.checker._check_translation_tags(english_tags, trans_tags)

        self.assertIn("T00002", result["empty"], "Tabs and newlines should be detected as empty")

    def test_extra_spaces_detected_as_untranslated(self) -> None:
        english_tags = {"T00001": "Login", "T00002": "Register"}
        trans_tags = {"T00001": "  Login  ", "T00002": "Registrar"}  # Extra spaces

        result = self.checker._check_translation_tags(english_tags, trans_tags)

        self.assertIn("T00001", result["untranslated"], "Extra spaces should be detected as untranslated")

    def test_properly_translated_no_issues(self) -> None:
        english_tags = {"T00001": "Login", "T00002": "Register"}
        trans_tags = {"T00001": "Iniciar Sesión", "T00002": "Registrar"}  # Proper translations

        result = self.checker._check_translation_tags(english_tags, trans_tags)

        self.assertEqual(len(result["missing"]), 0, "No missing tags expected")
        self.assertEqual(len(result["untranslated"]), 0, "No untranslated tags expected")
        self.assertEqual(len(result["empty"]), 0, "No empty tags expected")


if __name__ == "__main__":
    unittest.main()
