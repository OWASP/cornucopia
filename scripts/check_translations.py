"""
Translation Tag Checker for OWASP Cornucopia

This script checks that translation files have the same T0xxx tags as the English version.
It detects:
- Missing tags in translations
- Untranslated tags (text identical to English)
- Empty tag values
"""

import re
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Any
from collections import defaultdict


class TranslationChecker:
    """Check translations for missing, untranslated, or empty tags."""

    def __init__(self, source_dir: Path):
        self.source_dir = source_dir
        self.results: Dict[str, Dict[str, Any]] = defaultdict(lambda: defaultdict(dict))

    def extract_tags(self, yaml_file: Path) -> Dict[str, str]:
        """Extract T0xxx tags and their text from a YAML file."""
        tags = {}
        try:
            with open(yaml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            # Extract tags from paragraphs.sentences
            if data and "paragraphs" in data:
                for paragraph in data["paragraphs"]:
                    if "sentences" in paragraph:
                        for sentence in paragraph["sentences"]:
                            tag_id = sentence.get("id", "")
                            if tag_id.startswith("T0"):
                                tags[tag_id] = sentence.get("text", "")

        except Exception as e:
            print(f"Error reading {yaml_file}: {e}", file=sys.stderr)

        return tags

    def get_file_groups(self) -> Dict[str, List[Path]]:
        """Group YAML files by their base name (e.g., webapp-cards-2.2)."""
        file_groups = defaultdict(list)

        for yaml_file in self.source_dir.glob("*-*.yaml"):
            # Skip archived files
            if "archive" in str(yaml_file):
                continue

            # Extract base name and language
            # Format: {edition}-{component}-{version}-{lang}.yaml
            parts = yaml_file.stem.split("-")
            if len(parts) >= 3:
                # Find language code (usually last part or second to last)
                lang = parts[-1]
                base_name = "-".join(parts[:-1])

                # Only process card files with language codes
                # Matches 2-letter codes (e.g. en, es) and regional codes (e.g. pt_pt, no_nb)
                lang_pattern = re.compile(r"^[a-z]{2}([_-][a-z]{2})?$")
                if "cards" in base_name and lang_pattern.match(lang):
                    file_groups[base_name].append(yaml_file)

        return file_groups

    def _separate_english_and_translations(self, files: List[Path]) -> Tuple[Path | None, List[Path]]:
        """Separate English reference file from translation files."""
        english_file = None
        translation_files = []

        for f in files:
            lang = f.stem.split("-")[-1]
            if lang == "en":
                english_file = f
            else:
                translation_files.append(f)

        return english_file, translation_files

    def _check_translation_tags(self, english_tags: Dict[str, str], trans_tags: Dict[str, str]) -> Dict[str, Any]:
        """Check translation tags against English reference."""
        missing = []
        untranslated = []
        empty = []

        for tag_id, eng_text in english_tags.items():
            if tag_id not in trans_tags:
                missing.append(tag_id)
            elif not trans_tags[tag_id] or not trans_tags[tag_id].strip():
                empty.append(tag_id)
            elif trans_tags[tag_id].strip() == eng_text.strip():
                untranslated.append(tag_id)

        return {
            "missing": sorted(missing),
            "untranslated": sorted(untranslated),
            "empty": sorted(empty),
        }

    def check_translations(self) -> Dict[str, Dict[str, Any]]:
        """
        Check all translation files against English versions.

        Returns:
            Dict with structure:
            {
                'base_name': {
                    'language': {
                        'missing': ['T00145', ...],
                        'untranslated': ['T00100', ...],
                        'empty': ['T00200', ...]
                    }
                }
            }
        """
        file_groups = self.get_file_groups()

        for base_name, files in file_groups.items():
            english_file, translation_files = self._separate_english_and_translations(files)

            if not english_file:
                print(f"Warning: No English file found for {base_name}", file=sys.stderr)
                continue

            english_tags = self.extract_tags(english_file)
            if not english_tags:
                continue

            for trans_file in translation_files:
                lang = trans_file.stem.split("-")[-1]
                trans_tags = self.extract_tags(trans_file)
                issues = self._check_translation_tags(english_tags, trans_tags)

                if any(issues.values()):
                    issues["file"] = str(trans_file.name)
                    self.results[base_name][lang] = issues

        return dict(self.results)

    def generate_markdown_report(self) -> str:
        """Generate a Markdown report of translation issues."""
        report_lines = []

        if not self.results:
            report_lines.append("# Translation Check Report\n")
            report_lines.append("✅ All existing translations have been completed.\n")
            return "\n".join(report_lines)

        report_lines.append("# Translation Check Report\n")
        report_lines.append("The following sentences/tags have issues in the translations:\n")

        # Language name mapping
        lang_names = {
            "es": "Spanish",
            "fr": "French",
            "hu": "Hungarian",
            "it": "Italian",
            "nl": "Dutch",
            "no-nb": "Norwegian",
            "pt-br": "Portuguese (Brazil)",
            "pt-pt": "Portuguese (Portugal)",
            "ru": "Russian",
        }

        for base_name in sorted(self.results.keys()):
            languages = self.results[base_name]

            for lang in sorted(languages.keys()):
                lang_name = lang_names.get(lang, lang)
                issues = languages[lang]
                filename = issues.get("file", "")

                report_lines.append(f"\n## {lang_name}\n")
                report_lines.append(f"**File:** `{filename}`\n")

                if issues["missing"]:
                    report_lines.append("### Missing Tags\n")
                    report_lines.append(
                        "The following tags are present in the English version but missing in this translation:\n"
                    )
                    tags_str = ", ".join(issues["missing"])
                    report_lines.append(f"{tags_str}\n")

                if issues["untranslated"]:
                    report_lines.append("### Untranslated Tags\n")
                    report_lines.append("The following tags have identical text to English (not translated):\n")
                    tags_str = ", ".join(issues["untranslated"])
                    report_lines.append(f"{tags_str}\n")

                if issues["empty"]:
                    report_lines.append("### Empty Tags\n")
                    report_lines.append("The following tags are empty:\n")
                    tags_str = ", ".join(issues["empty"])
                    report_lines.append(f"{tags_str}\n")

        return "\n".join(report_lines)


def main() -> None:
    """Main entry point for the translation checker."""
    # Determine source directory
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent
    source_dir = base_dir / "source"

    if not source_dir.exists():
        print(f"Error: Source directory not found: {source_dir}", file=sys.stderr)
        sys.exit(1)

    # Run checker
    checker = TranslationChecker(source_dir)
    results = checker.check_translations()

    # Generate report
    report = checker.generate_markdown_report()

    # Output report
    print(report)

    # Write to file
    output_file = base_dir / "translation_check_report.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n---\nReport written to: {output_file}", file=sys.stderr)

    # Exit with error code if issues found
    if results:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
