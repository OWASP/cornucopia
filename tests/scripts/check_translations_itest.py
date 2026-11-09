"""
Integration tests for translation tag checking.

Tests the translation checker against the mock files in tests/test_files/source.
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


class TestTranslationTagsIntegration(unittest.TestCase):
    """Integration tests that check translation files read from disk."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        # Navigate up from tests/scripts to cornucopia root
        self.base_path = Path(__file__).parent.parent.parent
        self.source_dir = self.base_path / "tests" / "test_files" / "source"
        self.checker = TranslationChecker(self.source_dir)

    def test_source_directory_exists(self) -> None:
        """Test that the source directory exists."""
        self.assertTrue(self.source_dir.exists(), f"Source directory not found: {self.source_dir}")

    def test_english_files_exist(self) -> None:
        """Test that English card files exist."""
        english_files = list(self.source_dir.glob("*-cards-*-en.yaml"))
        self.assertGreater(len(english_files), 0, "No English card files found in source directory")

    def test_reports_missing_untranslated_and_empty_tags(self) -> None:
        """Test that the checker reports the missing, untranslated and empty tags in the mock Spanish file."""
        results = self.checker.check_translations()

        spanish_issues = results["test-cards-1.0"]["es"]
        self.assertIn("T00004", spanish_issues["missing"])
        self.assertIn("T00002", spanish_issues["untranslated"])
        self.assertIn("T00003", spanish_issues["empty"])

    def test_no_duplicate_tags_in_english(self) -> None:
        """Test that English files don't have duplicate T0xxx tags."""
        english_files = list(self.source_dir.glob("*-cards-*-en.yaml"))

        for eng_file in english_files:
            with open(eng_file, "r", encoding="utf-8") as f:
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

                self.assertEqual(len(duplicates), 0, f"Duplicate tags found in {eng_file.name}: {duplicates}")

    def test_tag_format(self) -> None:
        """Test that tags follow the T0xxxx format."""
        tag_pattern = re.compile(r"^T0\d{4,5}$")

        english_files = list(self.source_dir.glob("*-cards-*-en.yaml"))

        for eng_file in english_files:
            tags = self.checker.extract_tags(eng_file)

            for tag_id in tags.keys():
                self.assertIsNotNone(
                    tag_pattern.match(tag_id), f"Tag {tag_id} in {eng_file.name} doesn't match format T0xxxx"
                )

    def test_generate_markdown_report(self) -> None:
        """Test that markdown report generation works."""
        report = self.checker.generate_markdown_report()

        self.assertIsInstance(report, str)
        self.assertIn("Translation Check Report", report)


if __name__ == "__main__":
    unittest.main()
