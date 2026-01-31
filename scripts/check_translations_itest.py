"""
Integration tests for translation tag checking.

Tests that all translations in the actual source directory have the same T0xxx tags as the English version.
"""

import unittest
import yaml
import re
from pathlib import Path
import sys

# Add scripts directory to path
scripts_path = Path(__file__).parent.parent.parent / 'scripts'
sys.path.insert(0, str(scripts_path))

from check_translations import TranslationChecker


class TestTranslationTagsIntegration(unittest.TestCase):
    """Integration tests that check actual translation files."""

    def setUp(self):
        """Set up test fixtures."""
        # Navigate up from scripts to cornucopia root
        self.base_path = Path(__file__).parent.parent.parent
        self.source_dir = self.base_path / 'source'
        self.checker = TranslationChecker(self.source_dir)

    def test_source_directory_exists(self):
        """Test that the source directory exists."""
        self.assertTrue(
            self.source_dir.exists(),
            f"Source directory not found: {self.source_dir}"
        )

    def test_english_files_exist(self):
        """Test that English card files exist."""
        english_files = list(self.source_dir.glob('*-cards-*-en.yaml'))
        self.assertGreater(
            len(english_files), 0,
            "No English card files found in source directory"
        )

    def test_translations_completeness(self):
        """
        Test that all translations have the same T0xxx tags as English.
        
        This test will fail if:
        - Tags are missing in translations
        - Tags are untranslated (identical to English)
        - Tags are empty
        """
        results = self.checker.check_translations()
        
        if results:
            # Generate detailed report
            report = self.checker.generate_markdown_report()
            
            # Count total issues
            total_issues = 0
            for base_name, languages in results.items():
                for lang, issues in languages.items():
                    total_issues += len(issues.get('missing', []))
                    total_issues += len(issues.get('untranslated', []))
                    total_issues += len(issues.get('empty', []))
                    
            self.fail(
                f"\\n\\nTranslation issues found ({total_issues} total):\\n\\n{report}\\n"
            )

    def test_no_duplicate_tags_in_english(self):
        """Test that English files don't have duplicate T0xxx tags."""
        english_files = list(self.source_dir.glob('*-cards-*-en.yaml'))
        
        for eng_file in english_files:
            with open(eng_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            if data and 'paragraphs' in data:
                seen_ids = set()
                duplicates = []
                
                for paragraph in data['paragraphs']:
                    if 'sentences' in paragraph:
                        for sentence in paragraph['sentences']:
                            tag_id = sentence.get('id', '')
                            if tag_id.startswith('T0'):
                                if tag_id in seen_ids:
                                    duplicates.append(tag_id)
                                seen_ids.add(tag_id)
                        
                self.assertEqual(
                    len(duplicates), 0,
                    f"Duplicate tags found in {eng_file.name}: {duplicates}"
                )

    def test_tag_format(self):
        """Test that tags follow the T0xxxx format."""
        tag_pattern = re.compile(r'^T0\d{4,5}$')
        
        english_files = list(self.source_dir.glob('*-cards-*-en.yaml'))
        
        for eng_file in english_files:
            tags = self.checker.extract_tags(eng_file)
            
            for tag_id in tags.keys():
                self.assertIsNotNone(
                    tag_pattern.match(tag_id),
                    f"Tag {tag_id} in {eng_file.name} doesn't match format T0xxxx"
                )

    def test_generate_markdown_report(self):
        """Test that markdown report generation works."""
        report = self.checker.generate_markdown_report()
        
        self.assertIsInstance(report, str)
        self.assertIn("Translation Check Report", report)


if __name__ == '__main__':
    unittest.main()
