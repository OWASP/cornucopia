#!/usr/bin/env python3
"""Unit tests for the PDF generation lookup layer.

These cover cornucopia_common, which holds the decisions the generator makes:
which editions and languages exist, what order cards print in, which cards are
court cards or jokers, and which font, colour and artwork each card gets.

Everything here works on temporary fixtures rather than the repository's real
card data, so the tests do not change meaning when a translation is updated.
No Scribus is required.
"""

import os
import sys
import tempfile
import unittest

# The generator adds its own directory to sys.path at runtime and imports its
# modules flat. Doing the same here exercises the real import path.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_PDF_GENERATION = os.path.join(_REPO_ROOT, "scripts", "pdf_generation")
if _PDF_GENERATION not in sys.path:
    sys.path.insert(0, _PDF_GENERATION)

import cornucopia_common as cc  # noqa: E402  (needs the sys.path line above)
import merge_pdfs  # noqa: E402


def _write(path: str, text: str = "") -> str:
    """Create a file, and any directories leading to it."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    return path


def _card_yaml(suits: str) -> str:
    return "meta:\n  edition: demo\nsuits:\n" + suits


def _base_config(source_pattern: str) -> dict:
    """A config with the keys the lookup layer reads, and nothing more."""
    return {
        "project": {"version": "9.9"},
        "paths": {
            "source_root": "source",
            "asset_root": "art",
            "card_data_path": source_pattern,
        },
        "generation_targets": {"editions": "all", "languages": "all", "sizes": "all"},
        "size_profiles": {
            "bridge": {"asset_key": "small", "base_font_sizes": {"attack_text": 7.0, "special_text": 8.0}},
            "tarot": {"asset_key": "big", "base_font_sizes": {"attack_text": 9.0, "special_text": 9.8}},
        },
        "font_handling": {
            "default": {"body": "Noto Sans Light", "heading": "Noto Sans Medium", "accent": "Noto Sans Medium Italic"},
            "hi": {"body": "Noto Sans Devanagari Light"},
        },
        "font_scaling": {"attack_text": {"default": 0.0, "hi": -1.0}},
        "assets": {
            "image_dir": "card_artwork",
            "background_pattern": "%edition%/%suit%-%size%-%variant%.png",
            "card_back_pattern": "%edition%/back_%size%.png",
        },
        "card_semantics": {
            "court_values": ["J", "Q", "K"],
            "value_order": {"A": 1, "2": 2, "10": 10, "J": 11, "Q": 12, "K": 13},
            "language_overrides": {"ru": {"court_values": ["Д"], "value_order": {"Д": 12}}},
        },
        "defaults": {"suit_color": "Fallback_Grey", "court_text_color": "Pure_White"},
        "editions": {"demo": {"suit_colors": {"aa": "Demo_AA"}}},
        "output": {
            "filename_format": "card_%edition%_%card_id%_%size%_%version%_%language%_%bleed%_%printersmarks%.pdf",
            "deck_filename_format": "deck_%edition%_%size%_%language%_%bleed%.pdf",
        },
        "export_profiles": [{"name": "main", "bleed_mm": 3.0, "printers_marks": False}],
    }


class TestFormatBleed(unittest.TestCase):
    def test_whole_numbers_lose_the_decimal(self) -> None:
        self.assertEqual(cc.format_bleed(3.0), "3")

    def test_fractional_values_are_kept(self) -> None:
        self.assertEqual(cc.format_bleed(1.5), "1.5")

    def test_accepts_a_string(self) -> None:
        self.assertEqual(cc.format_bleed("6"), "6")


class TestMarksToken(unittest.TestCase):
    def test_marks_requested(self) -> None:
        self.assertEqual(cc.marks_token(True), "printersmarks")

    def test_marks_not_requested(self) -> None:
        self.assertEqual(cc.marks_token(False), "noprintersmarks")


class TestParseCards(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()
        self.path = _write(
            os.path.join(self.tmp, "cards.yaml"),
            _card_yaml(
                "  - id: AA\n"
                "    name: Alpha\n"
                "    cards:\n"
                "      - {id: AA2, value: '2', desc: Two, url: 'http://x/2'}\n"
                "      - {id: AAA, value: A, desc: Ace, misc: More reading}\n"
                "  - id: WC\n"
                "    name: Wild\n"
                "    cards:\n"
                "      - {id: JOA, value: A, desc: Joke, card: Joker}\n"
            ),
        )

    def test_reads_every_card(self) -> None:
        cards, _order = cc.parse_cards(self.path)
        self.assertEqual([c["card_id"] for c in cards], ["AA2", "AAA", "JOA"])

    def test_records_the_suit_order_from_the_file(self) -> None:
        _cards, order = cc.parse_cards(self.path)
        self.assertEqual(order, ["AA", "WC"])

    def test_carries_the_fields_the_generator_needs(self) -> None:
        cards, _order = cc.parse_cards(self.path)
        ace = [c for c in cards if c["card_id"] == "AAA"][0]
        self.assertEqual(ace["suit_name"], "Alpha")
        self.assertEqual(ace["attack_text"], "Ace")
        self.assertEqual(ace["misc_text"], "More reading")

    def test_missing_optional_fields_become_empty_not_none(self) -> None:
        cards, _order = cc.parse_cards(self.path)
        two = [c for c in cards if c["card_id"] == "AA2"][0]
        self.assertEqual(two["misc_text"], "")
        self.assertEqual(two["card_kind"], "")

    def test_a_missing_file_yields_no_cards(self) -> None:
        cards, order = cc.parse_cards(os.path.join(self.tmp, "absent.yaml"))
        self.assertEqual(cards, [])
        self.assertEqual(order, [])


class TestSortDeck(unittest.TestCase):
    def setUp(self) -> None:
        self.config = _base_config("source/%edition%.yaml")
        self.cards = [
            {"card_id": "AAK", "suit_id": "AA", "value": "K"},
            {"card_id": "AAA", "suit_id": "AA", "value": "A"},
            {"card_id": "BB2", "suit_id": "BB", "value": "2"},
            {"card_id": "AA2", "suit_id": "AA", "value": "2"},
        ]

    def test_orders_by_suit_then_value(self) -> None:
        ordered = cc.sort_deck(self.cards, self.config, "demo", ["AA", "BB"])
        self.assertEqual([c["card_id"] for c in ordered], ["AAA", "AA2", "AAK", "BB2"])

    def test_suit_order_follows_the_source_file(self) -> None:
        ordered = cc.sort_deck(self.cards, self.config, "demo", ["BB", "AA"])
        self.assertEqual([c["card_id"] for c in ordered][0], "BB2")

    def test_a_localised_value_still_sorts_as_its_court_card(self) -> None:
        cards = [
            {"card_id": "AAA", "suit_id": "AA", "value": "A"},
            {"card_id": "AAQ", "suit_id": "AA", "value": "Д"},
            {"card_id": "AA2", "suit_id": "AA", "value": "2"},
        ]
        ordered = cc.sort_deck(cards, self.config, "demo", ["AA"], "ru")
        self.assertEqual([c["card_id"] for c in ordered], ["AAA", "AA2", "AAQ"])


class TestIsCourt(unittest.TestCase):
    def setUp(self) -> None:
        self.config = _base_config("source/%edition%.yaml")

    def test_recognises_a_court_value(self) -> None:
        self.assertTrue(cc.is_court({"value": "Q"}, self.config))

    def test_a_pip_card_is_not_a_court_card(self) -> None:
        self.assertFalse(cc.is_court({"value": "7"}, self.config))

    def test_a_localised_court_value_is_missed_without_the_language(self) -> None:
        self.assertFalse(cc.is_court({"value": "Д"}, self.config))

    def test_a_localised_court_value_is_recognised_with_the_language(self) -> None:
        self.assertTrue(cc.is_court({"value": "Д"}, self.config, "ru"))

    def test_the_base_values_still_apply_for_that_language(self) -> None:
        self.assertTrue(cc.is_court({"value": "K"}, self.config, "ru"))


class TestIsJoker(unittest.TestCase):
    def setUp(self) -> None:
        self.config = _base_config("source/%edition%.yaml")
        self.config["editions"]["demo"]["joker_suits"] = ["wc"]

    def test_a_card_in_a_declared_joker_suit(self) -> None:
        self.assertTrue(cc.is_joker({"suit_id": "WC", "card_kind": ""}, self.config, "demo"))

    def test_a_card_the_data_marks_as_a_joker(self) -> None:
        self.assertTrue(cc.is_joker({"suit_id": "ZZ", "card_kind": "Joker"}, self.config, "demo"))

    def test_an_ordinary_card_is_not_a_joker(self) -> None:
        self.assertFalse(cc.is_joker({"suit_id": "AA", "card_kind": ""}, self.config, "demo"))

    def test_an_edition_with_no_joker_suits(self) -> None:
        self.config["editions"]["demo"]["joker_suits"] = []
        self.assertFalse(cc.is_joker({"suit_id": "WC", "card_kind": ""}, self.config, "demo"))


class TestHasSpecialText(unittest.TestCase):
    def test_a_card_carrying_misc_text(self) -> None:
        self.assertTrue(cc.has_special_text({"misc_text": "Read more"}))

    def test_a_card_without_misc_text(self) -> None:
        self.assertFalse(cc.has_special_text({"misc_text": ""}))

    def test_whitespace_alone_does_not_count(self) -> None:
        self.assertFalse(cc.has_special_text({"misc_text": "   "}))


class TestGetFont(unittest.TestCase):
    def setUp(self) -> None:
        self.config = _base_config("source/%edition%.yaml")

    def test_uses_the_default_for_a_language_with_no_entry(self) -> None:
        self.assertEqual(cc.get_font(self.config, "fr", "body"), "Noto Sans Light")

    def test_uses_the_language_override_where_one_exists(self) -> None:
        self.assertEqual(cc.get_font(self.config, "hi", "body"), "Noto Sans Devanagari Light")

    def test_falls_back_to_the_default_for_a_role_not_overridden(self) -> None:
        self.assertEqual(cc.get_font(self.config, "hi", "heading"), "Noto Sans Medium")


class TestGetFontSize(unittest.TestCase):
    def setUp(self) -> None:
        self.config = _base_config("source/%edition%.yaml")

    def test_uses_the_base_size_for_the_card_format(self) -> None:
        self.assertEqual(cc.get_font_size(self.config, "bridge", "attack_text", "en"), 7.0)
        self.assertEqual(cc.get_font_size(self.config, "tarot", "attack_text", "en"), 9.0)

    def test_applies_the_offset_for_a_dense_language(self) -> None:
        self.assertEqual(cc.get_font_size(self.config, "bridge", "attack_text", "hi"), 6.0)

    def test_the_offset_applies_only_to_the_frame_it_names(self) -> None:
        self.assertEqual(cc.get_font_size(self.config, "bridge", "special_text", "hi"), 8.0)


class TestCardColors(unittest.TestCase):
    def setUp(self) -> None:
        self.config = _base_config("source/%edition%.yaml")

    def test_a_named_swatch_is_used_as_given(self) -> None:
        assets = {"demo": {"suits": [{"id": "AA", "color": "Named_Colour"}]}}
        suit, number, defs = cc.card_colors(self.config, assets, "demo", {"suit_id": "AA", "value": "2"})
        self.assertEqual(suit, "Named_Colour")
        self.assertEqual(number, "Named_Colour")
        self.assertEqual(defs, {})

    def test_inline_cmyk_is_registered_for_injection(self) -> None:
        assets = {"demo": {"suits": [{"id": "AA", "color": {"c": 10, "m": 20, "y": 30, "k": 40}}]}}
        suit, _number, defs = cc.card_colors(self.config, assets, "demo", {"suit_id": "AA", "value": "2"})
        self.assertIn(suit, defs)
        self.assertEqual(defs[suit], {"c": 10, "m": 20, "y": 30, "k": 40})

    def test_a_court_card_takes_the_court_colour(self) -> None:
        assets = {"demo": {"suits": [{"id": "AA", "color": "Named_Colour", "court_color": "Court_Colour"}]}}
        _suit, number, _defs = cc.card_colors(self.config, assets, "demo", {"suit_id": "AA", "value": "K"})
        self.assertEqual(number, "Court_Colour")

    def test_a_court_card_defaults_to_white_when_no_court_colour_is_set(self) -> None:
        assets = {"demo": {"suits": [{"id": "AA", "color": "Named_Colour"}]}}
        _suit, number, _defs = cc.card_colors(self.config, assets, "demo", {"suit_id": "AA", "value": "K"})
        self.assertEqual(number, "Pure_White")

    def test_a_suit_with_no_entry_anywhere_falls_back(self) -> None:
        suit, _number, _defs = cc.card_colors(self.config, {}, "demo", {"suit_id": "ZZ", "value": "2"})
        self.assertEqual(suit, "Fallback_Grey")


class TestResolveBackground(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()
        self.config = _base_config("source/%edition%.yaml")
        art = os.path.join(self.tmp, "art", "card_artwork", "demo")
        for name in ("aa-small-default.png", "aa-small-court.png", "custom.png", "suit-override.png"):
            _write(os.path.join(art, name))

    def _resolve(self, card: dict, assets: dict) -> str:
        path, _found = cc.resolve_background(self.config, assets, self.tmp, "demo", card, "bridge")
        return os.path.basename(path)

    def test_a_pip_card_uses_the_default_artwork(self) -> None:
        self.assertEqual(self._resolve({"suit_id": "AA", "card_id": "AA2", "value": "2"}, {}), "aa-small-default.png")

    def test_a_court_card_uses_the_court_artwork(self) -> None:
        self.assertEqual(self._resolve({"suit_id": "AA", "card_id": "AAK", "value": "K"}, {}), "aa-small-court.png")

    def test_a_per_card_entry_wins_over_everything(self) -> None:
        assets = {"demo": {"suits": [{"id": "AA", "cards": [{"id": "AAK", "small": "demo/custom.png"}]}]}}
        self.assertEqual(self._resolve({"suit_id": "AA", "card_id": "AAK", "value": "K"}, assets), "custom.png")

    def test_a_suits_court_entry_is_used_for_a_court_card(self) -> None:
        assets = {"demo": {"suits": [{"id": "AA", "court_backgrounds": {"small": "demo/custom.png"}}]}}
        self.assertEqual(self._resolve({"suit_id": "AA", "card_id": "AAK", "value": "K"}, assets), "custom.png")

    def test_a_suits_court_entry_is_ignored_for_a_pip_card(self) -> None:
        assets = {"demo": {"suits": [{"id": "AA", "court_backgrounds": {"small": "demo/custom.png"}}]}}
        card = {"suit_id": "AA", "card_id": "AA2", "value": "2"}
        self.assertEqual(self._resolve(card, assets), "aa-small-default.png")

    def test_a_per_card_entry_beats_the_suits_court_entry(self) -> None:
        assets = {
            "demo": {
                "suits": [
                    {
                        "id": "AA",
                        "court_backgrounds": {"small": "demo/suit-override.png"},
                        "cards": [{"id": "AAK", "small": "demo/custom.png"}],
                    }
                ]
            }
        }
        self.assertEqual(self._resolve({"suit_id": "AA", "card_id": "AAK", "value": "K"}, assets), "custom.png")

    def test_a_suit_entry_does_not_override_court_artwork(self) -> None:
        assets = {"demo": {"suits": [{"id": "AA", "backgrounds": {"small": "demo/suit-override.png"}}]}}
        self.assertEqual(self._resolve({"suit_id": "AA", "card_id": "AAK", "value": "K"}, assets), "aa-small-court.png")

    def test_a_suit_entry_applies_to_a_pip_card(self) -> None:
        assets = {"demo": {"suits": [{"id": "AA", "backgrounds": {"small": "demo/suit-override.png"}}]}}
        self.assertEqual(self._resolve({"suit_id": "AA", "card_id": "AA2", "value": "2"}, assets), "suit-override.png")

    def test_missing_artwork_is_reported_rather_than_guessed(self) -> None:
        _path, found = cc.resolve_background(
            self.config, {}, self.tmp, "demo", {"suit_id": "ZZ", "card_id": "ZZ2", "value": "2"}, "bridge"
        )
        self.assertFalse(found)


class TestOutputNames(unittest.TestCase):
    def setUp(self) -> None:
        self.config = _base_config("source/%edition%.yaml")

    def test_a_card_filename_fills_every_token(self) -> None:
        name = cc.card_pdf_name(self.config, "demo", "AA2", "bridge", "en", 3.0, False)
        self.assertEqual(name, "card_demo_AA2_bridge_9.9_en_3_noprintersmarks.pdf")

    def test_a_deck_filename_fills_every_token(self) -> None:
        self.assertEqual(cc.deck_pdf_name(self.config, "demo", "bridge", "en", 3.0), "deck_demo_bridge_en_3.pdf")

    def test_printers_marks_change_the_card_filename(self) -> None:
        name = cc.card_pdf_name(self.config, "demo", "AA2", "bridge", "en", 3.0, True)
        self.assertTrue(name.endswith("_printersmarks.pdf"))


class TestExpandSelection(unittest.TestCase):
    def test_all_returns_everything_available(self) -> None:
        warnings: list = []
        self.assertEqual(cc.expand_selection("all", ["a", "b"], "edition", warnings), ["a", "b"])
        self.assertEqual(warnings, [])

    def test_an_explicit_list_is_kept_in_the_order_given(self) -> None:
        warnings: list = []
        self.assertEqual(cc.expand_selection(["b", "a"], ["a", "b"], "edition", warnings), ["b", "a"])

    def test_an_unknown_entry_is_reported(self) -> None:
        warnings: list = []
        self.assertEqual(cc.expand_selection(["a", "nope"], ["a"], "edition", warnings), ["a"])
        self.assertEqual(len(warnings), 1)
        self.assertIn("nope", warnings[0])

    def test_a_bare_string_is_treated_as_one_entry(self) -> None:
        warnings: list = []
        self.assertEqual(cc.expand_selection("a", ["a", "b"], "edition", warnings), ["a"])


class TestDiscovery(unittest.TestCase):
    """Discovery is driven by the configured filename pattern, not a fixed layout."""

    def _flat_repo(self) -> str:
        tmp = tempfile.mkdtemp()
        for name in (
            "demo-cards-1.0-en.yaml",
            "demo-cards-2.0-en.yaml",
            "demo-cards-2.0-fr.yaml",
            "other-cards-1.0-en.yaml",
            "demo-mappings-2.0.yaml",
        ):
            _write(os.path.join(tmp, "source", name), _card_yaml("  - id: AA\n    cards: []\n"))
        _write(os.path.join(tmp, "source", "archive", "demo-cards-0.9-en.yaml"), "")
        return tmp

    def setUp(self) -> None:
        self.tmp = self._flat_repo()
        self.config = _base_config("source/%edition%-cards-%edition_version%-%language%.yaml")
        self.config["editions"] = {"demo": {}, "other": {}}

    def test_finds_editions_from_the_filename_pattern(self) -> None:
        self.assertEqual(cc.discover_editions(self.config, self.tmp), ["demo", "other"])

    def test_ignores_files_that_are_not_card_data(self) -> None:
        found = {f["edition"] for f in cc.scan_card_files(self.config, self.tmp)}
        self.assertNotIn("demo-mappings", found)

    def test_ignores_archived_versions_in_a_subdirectory(self) -> None:
        versions = {f["version"] for f in cc.scan_card_files(self.config, self.tmp) if f["edition"] == "demo"}
        self.assertNotIn("0.9", versions)

    def test_uses_the_highest_version_when_none_is_pinned(self) -> None:
        self.assertEqual(cc.edition_data_version(self.config, self.tmp, "demo"), "2.0")

    def test_a_pinned_version_is_honoured(self) -> None:
        self.config["editions"]["demo"] = {"data_version": "1.0"}
        self.assertEqual(cc.edition_data_version(self.config, self.tmp, "demo"), "1.0")

    def test_languages_are_those_of_the_version_being_built(self) -> None:
        self.assertEqual(cc.discover_languages(self.config, self.tmp, "demo"), ["en", "fr"])

    def test_languages_follow_the_pinned_version(self) -> None:
        self.config["editions"]["demo"] = {"data_version": "1.0"}
        self.assertEqual(cc.discover_languages(self.config, self.tmp, "demo"), ["en"])

    def test_an_edition_with_data_but_no_config_entry_is_not_offered(self) -> None:
        self.config["editions"] = {"demo": {}}
        self.assertEqual(cc.discover_editions(self.config, self.tmp), ["demo"])

    def test_the_same_code_handles_a_nested_layout(self) -> None:
        tmp = tempfile.mkdtemp()
        _write(os.path.join(tmp, "source", "demo", "en", "cards_en.yaml"), _card_yaml("  - id: AA\n    cards: []\n"))
        config = _base_config("source/%edition%/%language%/cards_%language%.yaml")
        config["editions"] = {"demo": {}}
        self.assertEqual(cc.discover_editions(config, tmp), ["demo"])
        self.assertEqual(cc.discover_languages(config, tmp, "demo"), ["en"])


class TestResolveTargets(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()
        for name in ("demo-cards-1.0-en.yaml", "demo-cards-1.0-fr.yaml"):
            _write(os.path.join(self.tmp, "source", name), _card_yaml("  - id: AA\n    cards: []\n"))
        self.config = _base_config("source/%edition%-cards-%edition_version%-%language%.yaml")
        self.config["editions"] = {"demo": {}}

    def test_builds_every_combination_by_default(self) -> None:
        targets, _warnings = cc.resolve_targets(self.config, self.tmp)
        self.assertEqual(len(targets), 4)

    def test_command_line_selection_narrows_the_matrix(self) -> None:
        targets, _warnings = cc.resolve_targets(self.config, self.tmp, languages=["en"], sizes=["bridge"])
        self.assertEqual(len(targets), 1)
        self.assertEqual(targets[0], {"edition": "demo", "language": "en", "size": "bridge"})

    def test_an_unsupported_edition_is_refused(self) -> None:
        targets, warnings = cc.resolve_targets(self.config, self.tmp, editions=["nosuch"])
        self.assertEqual(targets, [])
        self.assertTrue(any("nosuch" in w for w in warnings))

    def test_a_misnamed_data_file_is_reported(self) -> None:
        _write(os.path.join(self.tmp, "source", "demo-cards-1.0-de,yaml"), "")
        _targets, warnings = cc.resolve_targets(self.config, self.tmp)
        self.assertTrue(any("de,yaml" in w for w in warnings))


class TestExportProfiles(unittest.TestCase):
    def setUp(self) -> None:
        self.config = _base_config("source/%edition%.yaml")

    def test_returns_the_configured_profiles(self) -> None:
        self.assertEqual(cc.get_export_profiles(self.config)[0]["name"], "main")

    def test_a_named_profile_can_be_selected(self) -> None:
        self.assertEqual(cc.get_export_profiles(self.config, profile_name="main")[0]["bleed_mm"], 3.0)

    def test_an_unknown_profile_name_is_an_error(self) -> None:
        with self.assertRaises(ValueError):
            cc.get_export_profiles(self.config, profile_name="nosuch")

    def test_command_line_values_override_the_profile(self) -> None:
        profile = cc.get_export_profiles(self.config, bleed_mm=6.0, printers_marks=True)[0]
        self.assertEqual(profile["bleed_mm"], 6.0)
        self.assertTrue(profile["printers_marks"])


class TestCleanIntermediates(unittest.TestCase):
    """The --clean tidy-up must remove working files and keep the finished decks."""

    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()
        self.out = os.path.join(self.tmp, "output")
        self.config = {"paths": {"qr_code_dir": "output/qrcodes"}}

        self.cards = [_write(os.path.join(self.out, "card_{0}.pdf".format(n)), "x" * 100) for n in range(3)]
        self.slas = [_write(os.path.join(self.out, "card_{0}.sla".format(n)), "y") for n in range(3)]
        self.qr = [_write(os.path.join(self.out, "qrcodes", "AA{0}.png".format(n)), "z") for n in range(3)]
        self.deck = _write(os.path.join(self.out, "deck_demo_bridge_en_3.pdf"), "keep me")

    def _clean(self) -> tuple:
        return merge_pdfs.clean_intermediates(self.cards, self.config, self.tmp, self.out)

    def test_removes_the_card_pdfs_it_consumed(self) -> None:
        self._clean()
        for path in self.cards:
            self.assertFalse(os.path.exists(path))

    def test_removes_the_sla_files(self) -> None:
        self._clean()
        for path in self.slas:
            self.assertFalse(os.path.exists(path))

    def test_removes_the_qr_images(self) -> None:
        self._clean()
        for path in self.qr:
            self.assertFalse(os.path.exists(path))

    def test_keeps_the_merged_deck(self) -> None:
        self._clean()
        self.assertTrue(os.path.exists(self.deck), "the merged deck must never be deleted")

    def test_reports_what_it_removed(self) -> None:
        removed, freed = self._clean()
        self.assertEqual(removed, 9)
        self.assertGreater(freed, 0)

    def test_a_file_already_gone_is_not_an_error(self) -> None:
        os.remove(self.cards[0])
        removed, _freed = self._clean()
        self.assertEqual(removed, 8)


if __name__ == "__main__":
    unittest.main()
