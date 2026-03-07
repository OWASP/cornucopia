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




class TestCompoundLocales(unittest.TestCase):
    """Tests specifically for compound locale code handling (issue #2550)."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        script_dir = Path(__file__).parent
        cornucopia_dir = script_dir.parent
        self.test_source_dir = cornucopia_dir / "tests" / "test_files" / "source"
        self.checker = TranslationChecker(self.test_source_dir)

    def test_compound_locale_files_included_in_file_groups(self) -> None:
        """Test that compound locale files (no_nb, pt_br, pt_pt) are included by get_file_groups()."""
        file_groups = self.checker.get_file_groups()

        self.assertIn("test-cards-1.0", file_groups)
        files = [f.name for f in file_groups["test-cards-1.0"]]
        self.assertIn("test-cards-1.0-no_nb.yaml", files, "Norwegian (no_nb) file should be included")
        self.assertIn("test-cards-1.0-pt_br.yaml", files, "Portuguese Brazil (pt_br) file should be included")
        self.assertIn("test-cards-1.0-pt_pt.yaml", files, "Portuguese Portugal (pt_pt) file should be included")

    def test_compound_locale_not_excluded_by_old_len_filter(self) -> None:
        """Regression test: ensure 5-char locale codes are NOT filtered out."""
        file_groups = self.checker.get_file_groups()
        all_files = [f.name for files in file_groups.values() for f in files]

        self.assertTrue(
            any("no_nb" in name for name in all_files),
            "no_nb locale must not be excluded (regression: len('no_nb')==5, not 2)",
        )
        self.assertTrue(
            any("pt_br" in name for name in all_files),
            "pt_br locale must not be excluded (regression: len('pt_br')==5, not 2)",
        )
        self.assertTrue(
            any("pt_pt" in name for name in all_files),
            "pt_pt locale must not be excluded (regression: len('pt_pt')==5, not 2)",
        )

    def test_norwegian_translation_issues_detected(self) -> None:
        """Test that issues in Norwegian (no_nb) translation are detected."""
        results = self.checker.check_translations()

        self.assertIn("test-cards-1.0", results)
        self.assertIn("no_nb", results["test-cards-1.0"], "Norwegian (no_nb) results should be present")
        no_nb_issues = results["test-cards-1.0"]["no_nb"]
        self.assertIn("T00004", no_nb_issues["missing"], "T00004 should be missing in no_nb")
        self.assertIn("T00003", no_nb_issues["empty"], "T00003 should be empty in no_nb")

    def test_portuguese_brazil_untranslated_detected(self) -> None:
        """Test that untranslated tags in Portuguese Brazil (pt_br) are detected."""
        results = self.checker.check_translations()

        self.assertIn("test-cards-1.0", results)
        self.assertIn("pt_br", results["test-cards-1.0"], "Portuguese Brazil (pt_br) results should be present")
        pt_br_issues = results["test-cards-1.0"]["pt_br"]
        self.assertIn("T00002", pt_br_issues["untranslated"], "T00002 should be untranslated in pt_br")

    def test_portuguese_portugal_fully_translated_no_issues(self) -> None:
        """Test that a fully-translated Portuguese Portugal (pt_pt) file produces no issues."""
        results = self.checker.check_translations()

        pt_pt_issues = results.get("test-cards-1.0", {}).get("pt_pt", None)
        self.assertIsNone(pt_pt_issues, "pt_pt has no issues and should not appear in results")

    def test_lang_names_uses_underscore_keys(self) -> None:
        """Test that generate_markdown_report resolves compound locale display names correctly."""
        self.checker.results["test-cards-1.0"]["no_nb"] = {
            "missing": ["T00001"],
            "untranslated": [],
            "empty": [],
            "file": "test-cards-1.0-no_nb.yaml",
        }
        self.checker.results["test-cards-1.0"]["pt_br"] = {
            "missing": [],
            "untranslated": ["T00001"],
            "empty": [],
            "file": "test-cards-1.0-pt_br.yaml",
        }
        self.checker.results["test-cards-1.0"]["pt_pt"] = {
            "missing": [],
            "untranslated": [],
            "empty": ["T00001"],
            "file": "test-cards-1.0-pt_pt.yaml",
        }
        report = self.checker.generate_markdown_report()

        self.assertIn("Norwegian", report, "Norwegian display name should appear for no_nb")
        self.assertIn("Portuguese (Brazil)", report, "Portuguese (Brazil) display name should appear for pt_br")
        self.assertIn("Portuguese (Portugal)", report, "Portuguese (Portugal) display name should appear for pt_pt")


class TestCoverageBranches(unittest.TestCase):
    """Tests to ensure branch coverage for edge cases."""

    def setUp(self) -> None:
        self.checker = TranslationChecker(Path("."))

    def test_extract_tags_nonexistent_file(self) -> None:
        """Test that extract_tags handles non-existent files gracefully."""
        tags = self.checker.extract_tags(Path("/nonexistent/path/file.yaml"))
        self.assertEqual(tags, {}, "Should return empty dict for non-existent file")

    def test_generate_report_no_issues(self) -> None:
        """Test markdown report when there are no translation issues."""
        report = self.checker.generate_markdown_report()
        self.assertIn("All existing translations have been completed", report)

    def test_get_file_groups_skips_archive_files(self) -> None:
        """Test that files with 'archive' in their path/name are skipped."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            # Place a YAML file whose name contains "archive" directly in source dir
            (tmp_path / "webapp-archive-cards-1.0-en.yaml").write_text("---\nparagraphs: []")
            (tmp_path / "test-cards-1.0-en.yaml").write_text("---\nparagraphs: []")
            checker = TranslationChecker(tmp_path)
            file_groups = checker.get_file_groups()
            all_files = [f.name for files in file_groups.values() for f in files]
            self.assertNotIn("webapp-archive-cards-1.0-en.yaml", all_files, "Files with 'archive' in name should be skipped")

    def test_check_translations_no_english_file(self) -> None:
        """Test check_translations warns when no English file exists in a group."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            (tmp_path / "test-cards-1.0-es.yaml").write_text(
                "---\nparagraphs:\n- id: Common\n  sentences:\n  - id: T00001\n    text: 'Hola'"
            )
            checker = TranslationChecker(tmp_path)
            import io
            from contextlib import redirect_stderr
            with redirect_stderr(io.StringIO()) as captured:
                results = checker.check_translations()
            self.assertEqual(results, {}, "No results when there is no English file")
            self.assertIn("Warning", captured.getvalue())

    def test_check_translations_empty_english_tags(self) -> None:
        """Test check_translations skips groups when English file has no T0 tags."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            (tmp_path / "test-cards-1.0-en.yaml").write_text("---\nparagraphs: []")
            (tmp_path / "test-cards-1.0-es.yaml").write_text("---\nparagraphs: []")
            checker = TranslationChecker(tmp_path)
            results = checker.check_translations()
            self.assertEqual(results, {}, "Should produce no results when English has no tags")


    def test_main_exits_when_source_dir_missing(self) -> None:
        """Test that main() exits with code 1 when source directory does not exist."""
        import check_translations
        from unittest.mock import patch

        with patch.object(Path, "exists", return_value=False):
            with self.assertRaises(SystemExit) as cm:
                check_translations.main()
        self.assertEqual(cm.exception.code, 1)

    def test_main_runs_and_writes_report(self) -> None:
        """Test that main() runs end-to-end with a mocked TranslationChecker."""
        import check_translations
        from unittest.mock import patch, MagicMock, mock_open

        mock_checker = MagicMock()
        mock_checker.check_translations.return_value = {}
        mock_checker.generate_markdown_report.return_value = "# Report\n\u2705 Done"

        with patch.object(check_translations, "TranslationChecker", return_value=mock_checker), \
             patch("builtins.open", mock_open()), \
             patch("builtins.print"), \
             self.assertRaises(SystemExit) as cm:
            check_translations.main()
        self.assertEqual(cm.exception.code, 0)

if __name__ == "__main__":
    unittest.main()
