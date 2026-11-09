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
from unittest import mock

# The generator adds its own directory to sys.path at runtime and imports its
# modules flat. Doing the same here exercises the real import path.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_PDF_GENERATION = os.path.join(_REPO_ROOT, "scripts", "pdf_generation")
if _PDF_GENERATION not in sys.path:
    sys.path.insert(0, _PDF_GENERATION)

import cornucopia_common as cc  # noqa: E402  (needs the sys.path line above)
import check_environment  # noqa: E402
import merge_pdfs  # noqa: E402
import generate_deck  # noqa: E402
import runpy  # noqa: E402

# Repeated fixture values, named once so a change lands in one place.
_DATA_PATTERN = "source/%edition%.yaml"
_DEFAULT_ART = "aa-small-default.png"
_COURT_ART = "aa-small-court.png"
_CUSTOM_ART = "custom.png"
_CUSTOM_REL = "demo/" + _CUSTOM_ART
_SUIT_OVERRIDE_REL = "demo/suit-override.png"
_EMPTY_SUIT = "  - id: AA\n    cards: []\n"


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
        self.config = _base_config(_DATA_PATTERN)
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
        self.config = _base_config(_DATA_PATTERN)

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
        self.config = _base_config(_DATA_PATTERN)
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
        self.config = _base_config(_DATA_PATTERN)

    def test_uses_the_default_for_a_language_with_no_entry(self) -> None:
        self.assertEqual(cc.get_font(self.config, "fr", "body"), "Noto Sans Light")

    def test_uses_the_language_override_where_one_exists(self) -> None:
        self.assertEqual(cc.get_font(self.config, "hi", "body"), "Noto Sans Devanagari Light")

    def test_falls_back_to_the_default_for_a_role_not_overridden(self) -> None:
        self.assertEqual(cc.get_font(self.config, "hi", "heading"), "Noto Sans Medium")


class TestGetFontSize(unittest.TestCase):
    def setUp(self) -> None:
        self.config = _base_config(_DATA_PATTERN)

    def test_uses_the_base_size_for_the_card_format(self) -> None:
        self.assertEqual(cc.get_font_size(self.config, "bridge", "attack_text", "en"), 7.0)
        self.assertEqual(cc.get_font_size(self.config, "tarot", "attack_text", "en"), 9.0)

    def test_applies_the_offset_for_a_dense_language(self) -> None:
        self.assertEqual(cc.get_font_size(self.config, "bridge", "attack_text", "hi"), 6.0)

    def test_the_offset_applies_only_to_the_frame_it_names(self) -> None:
        self.assertEqual(cc.get_font_size(self.config, "bridge", "special_text", "hi"), 8.0)


class TestCardColors(unittest.TestCase):
    def setUp(self) -> None:
        self.config = _base_config(_DATA_PATTERN)

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
        self.config = _base_config(_DATA_PATTERN)
        art = os.path.join(self.tmp, "art", "card_artwork", "demo")
        for name in (_DEFAULT_ART, _COURT_ART, _CUSTOM_ART, "suit-override.png"):
            _write(os.path.join(art, name))

    def _resolve(self, card: dict, assets: dict) -> str:
        path, _found = cc.resolve_background(self.config, assets, self.tmp, "demo", card, "bridge")
        return os.path.basename(path)

    def test_a_pip_card_uses_the_default_artwork(self) -> None:
        self.assertEqual(self._resolve({"suit_id": "AA", "card_id": "AA2", "value": "2"}, {}), _DEFAULT_ART)

    def test_a_court_card_uses_the_court_artwork(self) -> None:
        self.assertEqual(self._resolve({"suit_id": "AA", "card_id": "AAK", "value": "K"}, {}), _COURT_ART)

    def test_a_per_card_entry_wins_over_everything(self) -> None:
        assets = {"demo": {"suits": [{"id": "AA", "cards": [{"id": "AAK", "small": _CUSTOM_REL}]}]}}
        self.assertEqual(self._resolve({"suit_id": "AA", "card_id": "AAK", "value": "K"}, assets), _CUSTOM_ART)

    def test_a_suits_court_entry_is_used_for_a_court_card(self) -> None:
        assets = {"demo": {"suits": [{"id": "AA", "court_backgrounds": {"small": _CUSTOM_REL}}]}}
        self.assertEqual(self._resolve({"suit_id": "AA", "card_id": "AAK", "value": "K"}, assets), _CUSTOM_ART)

    def test_a_suits_court_entry_is_ignored_for_a_pip_card(self) -> None:
        assets = {"demo": {"suits": [{"id": "AA", "court_backgrounds": {"small": _CUSTOM_REL}}]}}
        card = {"suit_id": "AA", "card_id": "AA2", "value": "2"}
        self.assertEqual(self._resolve(card, assets), _DEFAULT_ART)

    def test_a_per_card_entry_beats_the_suits_court_entry(self) -> None:
        assets = {
            "demo": {
                "suits": [
                    {
                        "id": "AA",
                        "court_backgrounds": {"small": _SUIT_OVERRIDE_REL},
                        "cards": [{"id": "AAK", "small": _CUSTOM_REL}],
                    }
                ]
            }
        }
        self.assertEqual(self._resolve({"suit_id": "AA", "card_id": "AAK", "value": "K"}, assets), _CUSTOM_ART)

    def test_a_suit_entry_does_not_override_court_artwork(self) -> None:
        assets = {"demo": {"suits": [{"id": "AA", "backgrounds": {"small": _SUIT_OVERRIDE_REL}}]}}
        self.assertEqual(self._resolve({"suit_id": "AA", "card_id": "AAK", "value": "K"}, assets), _COURT_ART)

    def test_a_suit_entry_applies_to_a_pip_card(self) -> None:
        assets = {"demo": {"suits": [{"id": "AA", "backgrounds": {"small": _SUIT_OVERRIDE_REL}}]}}
        self.assertEqual(self._resolve({"suit_id": "AA", "card_id": "AA2", "value": "2"}, assets), "suit-override.png")

    def test_missing_artwork_is_reported_rather_than_guessed(self) -> None:
        _path, found = cc.resolve_background(
            self.config, {}, self.tmp, "demo", {"suit_id": "ZZ", "card_id": "ZZ2", "value": "2"}, "bridge"
        )
        self.assertFalse(found)


class TestOutputNames(unittest.TestCase):
    def setUp(self) -> None:
        self.config = _base_config(_DATA_PATTERN)

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
            _write(os.path.join(tmp, "source", name), _card_yaml(_EMPTY_SUIT))
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
        _write(os.path.join(tmp, "source", "demo", "en", "cards_en.yaml"), _card_yaml(_EMPTY_SUIT))
        config = _base_config("source/%edition%/%language%/cards_%language%.yaml")
        config["editions"] = {"demo": {}}
        self.assertEqual(cc.discover_editions(config, tmp), ["demo"])
        self.assertEqual(cc.discover_languages(config, tmp, "demo"), ["en"])


class TestResolveTargets(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()
        for name in ("demo-cards-1.0-en.yaml", "demo-cards-1.0-fr.yaml"):
            _write(os.path.join(self.tmp, "source", name), _card_yaml(_EMPTY_SUIT))
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
        self.config = _base_config(_DATA_PATTERN)

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


class TestCheckEnvironment(unittest.TestCase):
    def test_check_required_marks_other_interpreter_modules_as_not_needed(self) -> None:
        original_import = __import__

        def fake_import(name, *args, **kwargs):
            if name in {"qrcode", "png", "pymupdf"}:
                raise ImportError("missing for test")
            return original_import(name, *args, **kwargs)

        with mock.patch("builtins.__import__", side_effect=fake_import):
            lines, missing = check_environment.check_required(False)

        self.assertTrue(any("not needed  qrcode" in line for line in lines))
        self.assertTrue(any("not needed  png" in line for line in lines))
        self.assertIn("pymupdf", missing)

    def test_check_optional_reports_missing_modules_without_failing(self) -> None:
        original_import = __import__

        def fake_import(name, *args, **kwargs):
            if name == "defusedxml":
                raise ImportError("missing for test")
            return original_import(name, *args, **kwargs)

        with mock.patch("builtins.__import__", side_effect=fake_import):
            lines = check_environment.check_optional()

        self.assertTrue(any("not found   defusedxml" in line for line in lines))

    def test_report_includes_interpreter_context_and_package_section(self) -> None:
        with mock.patch.object(check_environment, "check_required", return_value=(["  found       yaml"], [])):
            with mock.patch.object(check_environment, "check_optional", return_value=["  found       defusedxml"]):
                text = check_environment.report()

        self.assertIn("Running inside: plain Python (not Scribus)", text)
        self.assertIn("Python version :", text)
        self.assertIn("Where this interpreter looks for packages:", text)
        self.assertIn("Packages this interpreter needs:", text)
        self.assertIn("  found       yaml", text)
        self.assertIn("Optional:", text)
        self.assertIn("All packages this interpreter needs are present.", text)

    def test_report_explains_missing_packages(self) -> None:
        with mock.patch.object(
            check_environment, "check_required", return_value=(["  MISSING     yaml      install pyyaml"], ["yaml"])
        ):
            with mock.patch.object(check_environment, "check_optional", return_value=[]):
                text = check_environment.report()

        self.assertIn("Missing: yaml", text)
        self.assertIn("These must be installed into THIS interpreter", text)

    def test_check_optional_finds_modules(self) -> None:
        original_import = __import__

        def fake_import(name, *args, **kwargs):
            if name == "defusedxml":
                return mock.MagicMock()
            return original_import(name, *args, **kwargs)

        with mock.patch("builtins.__import__", side_effect=fake_import):
            lines = check_environment.check_optional()
        self.assertTrue(any("found       defusedxml" in line for line in lines))

    def test_report_inside_scribus(self) -> None:
        with mock.patch.dict("sys.modules", {"scribus": mock.MagicMock()}):
            text = check_environment.report()
            self.assertIn("Running inside: Scribus", text)

    def test_check_environment_main(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            with mock.patch("os.getcwd", return_value=tmpdir):
                runpy.run_path(os.path.join(_PDF_GENERATION, "check_environment.py"), run_name="__main__")
            out_txt = os.path.join(tmpdir, "check_environment.txt")
            self.assertTrue(os.path.exists(out_txt))

            with mock.patch("builtins.open", side_effect=OSError("Read only")):
                with mock.patch("os.getcwd", return_value=tmpdir):
                    runpy.run_path(os.path.join(_PDF_GENERATION, "check_environment.py"), run_name="__main__")


class TestLoadConfig(unittest.TestCase):
    def test_find_config_path_locates_root_config(self) -> None:
        path = cc.find_config_path()
        self.assertTrue(os.path.isabs(path))
        self.assertTrue(os.path.isfile(path))
        self.assertEqual(os.path.basename(path), "pdf_config.yaml")

    def test_find_config_path_absolute(self) -> None:
        abs_path = os.path.abspath(__file__)
        self.assertEqual(cc.find_config_path(config_name=abs_path), abs_path)

    def test_find_config_path_in_base_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            custom = _write(os.path.join(tmp, "custom_config.yaml"), "project: test\n")
            resolved = cc.find_config_path(base_dir=tmp, config_name="custom_config.yaml")
            self.assertEqual(resolved, custom)

    def test_find_config_path_explicit_base_dir_takes_precedence_over_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            custom = _write(os.path.join(tmp, "pdf_config.yaml"), "project: custom\n")
            resolved = cc.find_config_path(base_dir=tmp, config_name="pdf_config.yaml")
            self.assertEqual(resolved, custom)

    def test_find_config_path_missing_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            resolved = cc.find_config_path(base_dir=tmp, config_name="nonexistent.yaml")
            self.assertEqual(resolved, os.path.join(tmp, "nonexistent.yaml"))

    def test_load_config_loads_root_yaml(self) -> None:
        config = cc.load_config()
        self.assertIn("project", config)
        self.assertIn("paths", config)
        self.assertIn("generation_targets", config)
        self.assertEqual(config["paths"]["source_root"], "source")
        self.assertEqual(config["paths"]["asset_root"], "resources")

    def test_load_config_missing_file_returns_empty_dict(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = cc.load_config(base_dir=tmp, config_name="nonexistent.yaml")
            self.assertEqual(config, {})

    def test_load_assets_resolution(self) -> None:
        config = {"paths": {"assets_config_path": "scripts/pdf_generation/assets.yaml"}}
        assets = cc.load_assets(config)
        self.assertIsInstance(assets, dict)
        self.assertIn("webapp", assets)

    def test_infer_base_dir_default_and_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = os.path.join(tmp, "sub", "config.yaml")
            self.assertEqual(cc.infer_base_dir(cfg_path), os.path.join(tmp, "sub"))
            explicit = os.path.join(tmp, "custom_root")
            self.assertEqual(cc.infer_base_dir(cfg_path, explicit_base_dir=explicit), os.path.abspath(explicit))

    def test_legacy_config_discovery_and_path_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            script_dir = os.path.join(tmp, "scripts", "pdf_generation")
            os.makedirs(script_dir, exist_ok=True)
            legacy_cfg = _write(
                os.path.join(script_dir, "legacy_config.yaml"),
                "paths:\n  source_root: ../../source\n  output_dir: output\n",
            )
            resolved = cc.find_config_path(config_name=legacy_cfg)
            base = cc.infer_base_dir(resolved)
            self.assertEqual(base, os.path.abspath(script_dir))
            cfg = cc.load_yaml(resolved)
            self.assertEqual(cc.output_dir(cfg, base), os.path.join(script_dir, "output"))
            self.assertEqual(
                os.path.normpath(os.path.join(base, cfg["paths"]["source_root"])),
                os.path.normpath(os.path.join(tmp, "source")),
            )

    def test_find_config_path_empty_defaults_to_pdf_config_yaml(self) -> None:
        self.assertEqual(cc.find_config_path(config_name=None), cc.find_config_path(config_name="pdf_config.yaml"))

    def test_find_config_path_repo_and_script_dir(self) -> None:
        self.assertTrue(os.path.isfile(cc.find_config_path(config_name="pdf_config.yaml")))
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("cornucopia_common._SCRIPT_DIR", tmp):
                _write(os.path.join(tmp, "script_only.yaml"), "x: 1")
                self.assertEqual(
                    cc.find_config_path(config_name="script_only.yaml"), os.path.join(tmp, "script_only.yaml")
                )

    def test_infer_base_dir_none(self) -> None:
        self.assertEqual(cc.infer_base_dir(None, None), cc._REPO_ROOT)

    def test_load_assets_variants(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            abs_yaml = _write(os.path.join(tmp, "abs_assets.yaml"), "default: {}\n")
            self.assertEqual(cc.load_assets({"paths": {"assets_config_path": abs_yaml}}), {"default": {}})
            _write(os.path.join(tmp, "local_assets.yaml"), "default: {}\n")
            self.assertEqual(
                cc.load_assets({"paths": {"assets_config_path": "local_assets.yaml"}}, base_dir=tmp),
                {"default": {}},
            )
            with mock.patch("cornucopia_common._SCRIPT_DIR", tmp):
                _write(os.path.join(tmp, "script_assets.yaml"), "default: {}\n")
                self.assertEqual(
                    cc.load_assets({"paths": {"assets_config_path": "script_assets.yaml"}}),
                    {"default": {}},
                )
            self.assertEqual(cc.load_assets({"paths": {"assets_config_path": "missing_assets.yaml"}}, base_dir=tmp), {})


class TestCornucopiaCommonEdgeCases(unittest.TestCase):
    def test_resolve_asset_path_assets_prefix_and_abs_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = {"paths": {"asset_root": "resources"}}
            res = cc.resolve_asset_path(tmp, cfg, "assets/images/pic.png")
            self.assertEqual(res, os.path.join(tmp, "resources", "images", "pic.png").replace("\\", "/"))

            cfg_abs = {"paths": {"asset_root": "/var/assets"}}
            res_abs = cc.resolve_asset_path(tmp, cfg_abs, "pic.png")
            self.assertEqual(res_abs, "/var/assets/pic.png")

    def test_card_data_path_edition_version(self) -> None:
        cfg = {"paths": {"card_data_path": "source/%edition%-%edition_version%-%language%.yaml"}}
        p = cc.card_data_path(cfg, "/tmp", "webapp", "en", version="3.0")
        self.assertEqual(p, "/tmp/source/webapp-3.0-en.yaml")
        with mock.patch("cornucopia_common.edition_data_version", return_value="3.0"):
            p2 = cc.card_data_path(cfg, "/tmp", "webapp", "en")
            self.assertEqual(p2, "/tmp/source/webapp-3.0-en.yaml")

    def test_data_pattern_regex_unknown_token(self) -> None:
        cfg = {"paths": {"card_data_path": "source/%edition%-%custom_token%-%language%.yaml"}}
        regex = cc._data_pattern_regex(cfg)
        self.assertIsNotNone(regex)

    def test_scan_and_misnamed_non_directory(self) -> None:
        cfg = {"paths": {"source_root": "nonexistent_source"}}
        self.assertEqual(cc.scan_card_files(cfg, "/tmp"), [])
        self.assertEqual(cc.find_misnamed_files(cfg, "/tmp"), [])

    def test_discover_editions_unconfigured(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = _base_config("source/%edition%-cards-1.0-%language%.yaml")
            cfg["editions"] = {}
            _write(os.path.join(tmp, "source", "alpha-cards-1.0-en.yaml"), _card_yaml(_EMPTY_SUIT))
            eds = cc.discover_editions(cfg, tmp)
            self.assertEqual(eds, ["alpha"])

    def test_expand_selection_none(self) -> None:
        warnings = []
        sel = cc.expand_selection(None, ["a", "b"], "items", warnings)
        self.assertEqual(sel, ["a", "b"])

    def test_get_font_size_non_dict_scaling(self) -> None:
        cfg = {
            "size_profiles": {"bridge": {"base_font_sizes": {"frame": 10.0}}},
            "font_scaling": {"frame": 2.5},
        }
        self.assertEqual(cc.get_font_size(cfg, "bridge", "frame", "en"), 12.5)

    def test_suit_entry_and_colors_flat_suits(self) -> None:
        assets_data = {"suits": [{"id": "aa", "color": "Custom_AA", "court_color": "Custom_Court_AA"}]}
        cfg = _base_config(_DATA_PATTERN)
        cfg["editions"]["demo"]["suit_colors"] = {"aa": "Edition_AA"}
        card = {"suit_id": "aa", "card_id": "AA1"}
        suit_col, num_col, _defs = cc.card_colors(cfg, assets_data, "demo", card)
        self.assertEqual(suit_col, "Custom_AA")
        self.assertTrue(cc.has_suit_color(cfg, assets_data, "demo", "aa"))

        self.assertTrue(cc.has_suit_color(cfg, {}, "demo", "aa"))

    def test_assets_override_flat_suits(self) -> None:
        assets_data = {
            "suits": [
                {
                    "id": "aa",
                    "cards": [{"id": "aa1", "small": "custom_card.png"}],
                    "court_backgrounds": {"small": "court.png"},
                    "backgrounds": {"small": "bg.png"},
                }
            ]
        }
        card_level, court_level, suit_level = cc._assets_override(assets_data, "demo", "aa", "aa1", "small")
        self.assertEqual(card_level, "custom_card.png")
        self.assertEqual(court_level, "court.png")
        self.assertEqual(suit_level, "bg.png")

    def test_resolve_background_global_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bg_path = _write(os.path.join(tmp, "resources", "Backgrounds", "global_bg.png"), "image")
            assets_data = {"default": {"backgrounds": {"small": "global_bg.png"}}}
            cfg = _base_config(_DATA_PATTERN)
            cfg["paths"]["asset_root"] = "resources"
            cfg["assets"]["image_dir"] = "Backgrounds"
            card = {"card_id": "AA1", "suit_id": "aa"}
            full, found = cc.resolve_background(cfg, assets_data, tmp, "demo", card, "bridge")
            self.assertTrue(found)
            self.assertEqual(full, bg_path.replace("\\", "/"))

    def test_zip_name_and_sla_name(self) -> None:
        cfg = {
            "project": {"version": "2.0"},
            "packaging": {"zip_name": "Archive_%edition%_%version%.zip"},
            "output": {"sla_filename_format": "SLA_%edition%_%card_id%_%size%_%language%.sla"},
        }
        self.assertEqual(cc.zip_name(cfg, "demo"), "Archive_demo_2.0.zip")
        self.assertEqual(cc.sla_name(cfg, "demo", "AA1", "bridge", "en"), "SLA_demo_AA1_bridge_en.sla")


class TestMergePdfsCli(unittest.TestCase):
    def test_parse_args_defaults_and_options(self) -> None:
        test_argv = [
            "merge_pdfs.py",
            "--config",
            "custom_config.yaml",
            "--edition",
            "webapp",
            "--edition",
            "mobileapp",
            "--language",
            "en",
            "--size",
            "bridge",
            "--profile",
            "print",
            "--bleed-mm",
            "3.0",
            "--printers-marks",
            "--output-dir",
            "custom_out",
            "--zip",
            "--clean",
            "--dry-run",
            "--base-dir",
            "/tmp/base",
        ]
        with mock.patch("sys.argv", test_argv):
            args = merge_pdfs.parse_args()
            self.assertEqual(args.config, "custom_config.yaml")
            self.assertEqual(args.edition, ["webapp", "mobileapp"])
            self.assertEqual(args.language, ["en"])
            self.assertEqual(args.size, ["bridge"])
            self.assertEqual(args.profile, "print")
            self.assertEqual(args.bleed_mm, 3.0)
            self.assertTrue(args.printers_marks)
            self.assertEqual(args.output_dir, "custom_out")
            self.assertTrue(args.do_zip)
            self.assertTrue(args.clean)
            self.assertTrue(args.dry_run)
            self.assertEqual(args.base_dir, "/tmp/base")

    def test_parse_args_negated_flags(self) -> None:
        test_argv = [
            "merge_pdfs.py",
            "--no-printers-marks",
            "--no-zip",
        ]
        with mock.patch("sys.argv", test_argv):
            args = merge_pdfs.parse_args()
            self.assertFalse(args.printers_marks)
            self.assertFalse(args.do_zip)


class TestMergePdfsHelpers(unittest.TestCase):
    def test_files_with_suffix_non_directory(self) -> None:
        self.assertEqual(merge_pdfs.files_with_suffix("/nonexistent/dir", ".pdf"), [])

    def test_files_with_suffix_matches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _write(os.path.join(tmp, "a.PDF"))
            _write(os.path.join(tmp, "b.pdf"))
            _write(os.path.join(tmp, "c.txt"))
            matched = merge_pdfs.files_with_suffix(tmp, ".pdf")
            self.assertEqual(len(matched), 2)
            self.assertTrue(all(p.lower().endswith(".pdf") for p in matched))

    def test_clean_intermediates_handles_os_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "output")
            qr_dir = os.path.join(out, "qrcodes")
            pdf1 = _write(os.path.join(out, "card1.pdf"), "content")
            _write(os.path.join(out, "card1.sla"), "sla")
            _write(os.path.join(qr_dir, "qr1.png"), "qr")
            cfg = {"paths": {"qr_code_dir": "output/qrcodes"}}

            with mock.patch("os.remove", side_effect=OSError("Permission denied")):
                with mock.patch("os.rmdir", side_effect=OSError("Dir not empty")):
                    removed, freed = merge_pdfs.clean_intermediates([pdf1], cfg, tmp, out)
                    self.assertEqual(removed, 0)
                    self.assertEqual(freed, 0)

    def test_match_card_pdfs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = _base_config(_DATA_PATTERN)
            deck = [{"card_id": "AA1"}, {"card_id": "AA2"}]
            c1_name = cc.card_pdf_name(cfg, "demo", "AA1", "bridge", "en", 3.0, False)
            _write(os.path.join(tmp, c1_name), "pdf")

            found, missing = merge_pdfs.match_card_pdfs(deck, "demo", "en", "bridge", cfg, tmp, 3.0, False)
            self.assertEqual(len(found), 1)
            self.assertEqual(missing, ["AA2"])


class TestMergeDeck(unittest.TestCase):
    def test_merge_deck_raises_if_pymupdf_missing(self) -> None:
        with mock.patch.object(merge_pdfs, "pymupdf", None):
            with self.assertRaises(RuntimeError) as ctx:
                merge_pdfs.merge_deck(["dummy.pdf"], "out.pdf")
            self.assertIn("PyMuPDF", str(ctx.exception))

    def test_merge_deck_success_multi_page_and_single_page(self) -> None:
        mock_merged = mock.MagicMock()
        mock_merged.__len__.return_value = 4

        mock_card2 = mock.MagicMock()
        mock_card2.__len__.return_value = 2

        mock_card1 = mock.MagicMock()
        mock_card1.__len__.return_value = 1

        mock_pymupdf = mock.MagicMock()
        mock_pymupdf.open.side_effect = [mock_merged, mock_card2, mock_card1]

        with mock.patch.object(merge_pdfs, "pymupdf", mock_pymupdf):
            pages = merge_pdfs.merge_deck(["card2.pdf", "card1.pdf"], "deck.pdf")
            self.assertEqual(pages, 4)
            mock_merged.insert_pdf.assert_any_call(mock_card2, from_page=1, to_page=1)
            mock_merged.insert_pdf.assert_any_call(mock_card2, from_page=0, to_page=0)
            mock_merged.insert_pdf.assert_any_call(mock_card1, from_page=0, to_page=0)
            mock_merged.save.assert_called_once_with("deck.pdf", garbage=4, deflate=True)
            mock_merged.close.assert_called_once()


class TestPackageDecks(unittest.TestCase):
    def test_package_decks_per_edition(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = {
                "packaging": {"zip_scope": "per_edition", "zip_name": "OWASP_%edition%.zip"},
                "project": {"version": "1.0"},
            }
            deck1 = _write(os.path.join(tmp, "deck1.pdf"), "deck1")
            merge_pdfs.package_decks({"demo": [deck1]}, cfg["packaging"], cfg, tmp)
            archive = os.path.join(tmp, "OWASP_demo.zip")
            self.assertTrue(os.path.exists(archive))

    def test_package_decks_single_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = {
                "packaging": {"zip_scope": "single", "zip_name": "OWASP_%edition%.zip"},
                "project": {"version": "1.0"},
            }
            deck1 = _write(os.path.join(tmp, "deck1.pdf"), "deck1")
            deck2 = _write(os.path.join(tmp, "deck2.pdf"), "deck2")
            merge_pdfs.package_decks({"demo1": [deck1], "demo2": [deck2]}, cfg["packaging"], cfg, tmp)
            archive = os.path.join(tmp, "OWASP_demo1.zip")
            self.assertTrue(os.path.exists(archive))

    def test_maybe_package_skipped_when_empty_or_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            args = mock.Mock(do_zip=False)
            merge_pdfs.maybe_package(args, {}, {}, tmp)
            merge_pdfs.maybe_package(args, {}, {"demo": ["deck.pdf"]}, tmp)

    def test_maybe_package_enabled_by_args_or_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            deck = _write(os.path.join(tmp, "deck.pdf"), "deck")
            args = mock.Mock(do_zip=True)
            cfg = {
                "packaging": {"create_zip": False, "zip_name": "bundle_%edition%.zip"},
                "project": {"version": "1.0"},
            }
            merge_pdfs.maybe_package(args, cfg, {"demo": [deck]}, tmp)
            self.assertTrue(os.path.exists(os.path.join(tmp, "bundle_demo.zip")))

            args_none = mock.Mock(do_zip=None)
            cfg["packaging"]["create_zip"] = True
            cfg["packaging"]["zip_name"] = "bundle2_%edition%.zip"
            merge_pdfs.maybe_package(args_none, cfg, {"demo": [deck]}, tmp)
            self.assertTrue(os.path.exists(os.path.join(tmp, "bundle2_demo.zip")))


class TestMergePdfsReportingAndTidy(unittest.TestCase):
    def test_report_gaps(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            merge_pdfs.report_gaps([], tmp)
            self.assertFalse(os.path.exists(os.path.join(tmp, "merge_gaps.json")))

            merge_pdfs.report_gaps([{"target": "demo", "missing": ["AA1"]}], tmp)
            report_file = os.path.join(tmp, "merge_gaps.json")
            self.assertTrue(os.path.exists(report_file))

    def test_tidy_up_conditions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = {"paths": {"qr_code_dir": "output/qrcodes"}}
            out = os.path.join(tmp, "output")
            merge_pdfs.tidy_up([{"target": "demo"}], {"demo": ["deck.pdf"]}, ["card.pdf"], cfg, tmp, out)
            merge_pdfs.tidy_up([], {}, ["card.pdf"], cfg, tmp, out)
            card = _write(os.path.join(out, "card.pdf"), "card")
            merge_pdfs.tidy_up([], {"demo": ["deck.pdf"]}, [card], cfg, tmp, out)
            self.assertFalse(os.path.exists(card))


class TestMergeOneTarget(unittest.TestCase):
    def test_merge_one_target_no_cards(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = _base_config(_DATA_PATTERN)
            target = {"edition": "demo", "language": "en", "size": "bridge"}
            deck_path, used, gap = merge_pdfs.merge_one_target(target, cfg, tmp, tmp, 3.0, False, False)
            self.assertIsNone(deck_path)
            self.assertEqual(used, [])
            self.assertIsNone(gap)

    def test_merge_one_target_not_built(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = _base_config(_DATA_PATTERN)
            _write(os.path.join(tmp, "source", "demo.yaml"), _card_yaml("  - id: AA\n    cards:\n      - id: AA1\n"))
            target = {"edition": "demo", "language": "en", "size": "bridge"}
            deck_path, used, gap = merge_pdfs.merge_one_target(target, cfg, tmp, tmp, 3.0, False, False)
            self.assertIsNone(deck_path)
            self.assertEqual(used, [])
            self.assertIsNone(gap)

    def test_merge_one_target_dry_run_and_missing_gaps(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = _base_config(_DATA_PATTERN)
            cards_yaml = "  - id: AA\n    cards:\n" + "".join("      - id: AA{0}\n".format(i) for i in range(1, 13))
            _write(os.path.join(tmp, "source", "demo.yaml"), _card_yaml(cards_yaml))
            c1_name = cc.card_pdf_name(cfg, "demo", "AA1", "bridge", "en", 3.0, False)
            _write(os.path.join(tmp, c1_name), "pdf")

            target = {"edition": "demo", "language": "en", "size": "bridge"}
            deck_path, used, gap = merge_pdfs.merge_one_target(target, cfg, tmp, tmp, 3.0, False, dry_run=True)
            self.assertIsNone(deck_path)
            self.assertIsNotNone(gap)
            self.assertEqual(len(gap["missing"]), 11)

    def test_merge_one_target_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = _base_config(_DATA_PATTERN)
            _write(os.path.join(tmp, "source", "demo.yaml"), _card_yaml("  - id: AA\n    cards:\n      - id: AA1\n"))
            c1_name = cc.card_pdf_name(cfg, "demo", "AA1", "bridge", "en", 3.0, False)
            _write(os.path.join(tmp, c1_name), "pdf")
            target = {"edition": "demo", "language": "en", "size": "bridge"}

            with mock.patch("merge_pdfs.merge_deck", return_value=2):
                deck_path, used, gap = merge_pdfs.merge_one_target(target, cfg, tmp, tmp, 3.0, False, dry_run=False)
                self.assertIsNotNone(deck_path)
                self.assertEqual(len(used), 1)
                self.assertIsNone(gap)


class TestPrepareMerge(unittest.TestCase):
    def test_prepare_merge_config_none_or_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            args = mock.Mock(config="missing.yaml", output_dir=None)
            self.assertIsNone(merge_pdfs.prepare_merge(args, tmp, config={}))

    def test_prepare_merge_output_dir_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = _base_config(_DATA_PATTERN)
            args = mock.Mock(config="cfg.yaml", output_dir=os.path.join(tmp, "nonexistent"))
            self.assertIsNone(merge_pdfs.prepare_merge(args, tmp, config=cfg))

    def test_prepare_merge_invalid_profile(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = _base_config(_DATA_PATTERN)
            out = os.path.join(tmp, "out")
            os.makedirs(out, exist_ok=True)
            args = mock.Mock(
                config="cfg.yaml",
                output_dir=out,
                profile="unknown_profile",
                bleed_mm=None,
                printers_marks=None,
            )
            self.assertIsNone(merge_pdfs.prepare_merge(args, tmp, config=cfg))

    def test_prepare_merge_no_targets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = _base_config(_DATA_PATTERN)
            cfg["generation_targets"] = {"editions": [], "languages": [], "sizes": []}
            out = os.path.join(tmp, "out")
            os.makedirs(out, exist_ok=True)
            args = mock.Mock(
                config="cfg.yaml",
                output_dir=out,
                profile=None,
                bleed_mm=None,
                printers_marks=None,
                edition=None,
                language=None,
                size=None,
            )
            self.assertIsNone(merge_pdfs.prepare_merge(args, tmp, config=cfg))

    def test_prepare_merge_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = _base_config("source/%edition%-cards-%edition_version%-%language%.yaml")
            cfg["editions"] = {"demo": {}}
            _write(
                os.path.join(tmp, "source", "demo-cards-1.0-en.yaml"),
                _card_yaml("  - id: AA\n    cards:\n      - id: AA1\n"),
            )
            out = os.path.join(tmp, "out")
            os.makedirs(out, exist_ok=True)
            cfg_path = _write(os.path.join(tmp, "custom_cfg.yaml"), "paths:\n  output_dir: out\n")
            args = mock.Mock(
                config=cfg_path,
                output_dir=out,
                profile="main",
                bleed_mm=3.0,
                printers_marks=False,
                edition=["demo"],
                language=["en"],
                size=["bridge"],
            )
            # Test when config=None so line 294 executes
            with mock.patch("cornucopia_common.load_config", return_value=cfg):
                res = merge_pdfs.prepare_merge(args, tmp, config=None)
                self.assertIsNotNone(res)
                c, o, bleed, marks, targets = res
                self.assertEqual(bleed, 3.0)
                self.assertFalse(marks)
                self.assertEqual(len(targets), 1)

    def test_prepare_merge_logs_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = _base_config("source/%edition%-cards-%edition_version%-%language%.yaml")
            cfg["editions"] = {"demo": {}}
            _write(
                os.path.join(tmp, "source", "demo-cards-1.0-en.yaml"),
                _card_yaml("  - id: AA\n    cards:\n      - id: AA1\n"),
            )
            out = os.path.join(tmp, "out")
            os.makedirs(out, exist_ok=True)
            args = mock.Mock(
                config="cfg.yaml",
                output_dir=out,
                profile="main",
                bleed_mm=3.0,
                printers_marks=False,
                edition=["demo", "unknown_edition"],
                language=["en"],
                size=["bridge"],
            )
            res = merge_pdfs.prepare_merge(args, tmp, config=cfg)
            self.assertIsNotNone(res)


class TestMergePdfsMain(unittest.TestCase):
    def test_main_config_load_fail(self) -> None:
        with mock.patch("sys.argv", ["merge_pdfs.py", "--config", "nonexistent.yaml"]):
            with mock.patch("cornucopia_common.load_yaml", return_value=None):
                self.assertEqual(merge_pdfs.main(), 1)

    def test_main_base_dir_missing(self) -> None:
        with mock.patch("sys.argv", ["merge_pdfs.py", "--base-dir", "/nonexistent/base/dir"]):
            with mock.patch("cornucopia_common.load_yaml", return_value={"project": "test"}):
                self.assertEqual(merge_pdfs.main(), 1)

    def test_main_missing_pymupdf_without_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = _write(os.path.join(tmp, "pdf_config.yaml"), "project: test\n")
            with mock.patch.object(merge_pdfs, "pymupdf", None):
                with mock.patch("sys.argv", ["merge_pdfs.py", "--config", cfg_path, "--base-dir", tmp]):
                    self.assertEqual(merge_pdfs.main(), 1)

    def test_main_prepare_merge_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = _write(os.path.join(tmp, "pdf_config.yaml"), "project: test\n")
            with mock.patch.object(merge_pdfs, "pymupdf", mock.MagicMock()):
                with mock.patch("merge_pdfs.prepare_merge", return_value=None):
                    with mock.patch("sys.argv", ["merge_pdfs.py", "--config", cfg_path, "--base-dir", tmp]):
                        self.assertEqual(merge_pdfs.main(), 1)

    def test_main_dry_run_with_and_without_clean(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = _base_config("source/%edition%-cards-%edition_version%-%language%.yaml")
            cfg["editions"] = {"demo": {}}
            _write(
                os.path.join(tmp, "source", "demo-cards-1.0-en.yaml"),
                _card_yaml("  - id: AA\n    cards:\n      - id: AA1\n"),
            )
            out = os.path.join(tmp, "out")
            os.makedirs(out, exist_ok=True)
            cfg_path = _write(os.path.join(tmp, "pdf_config.yaml"), "project: test\n")

            with mock.patch("cornucopia_common.load_yaml", return_value=cfg):
                with mock.patch(
                    "sys.argv",
                    [
                        "merge_pdfs.py",
                        "--config",
                        cfg_path,
                        "--base-dir",
                        tmp,
                        "--output-dir",
                        out,
                        "--dry-run",
                        "--clean",
                    ],
                ):
                    self.assertEqual(merge_pdfs.main(), 0)

    def test_main_success_flow(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cfg = _base_config("source/%edition%-cards-%edition_version%-%language%.yaml")
            cfg["editions"] = {"demo": {}}
            _write(
                os.path.join(tmp, "source", "demo-cards-1.0-en.yaml"),
                _card_yaml("  - id: AA\n    cards:\n      - id: AA1\n"),
            )
            out = os.path.join(tmp, "out")
            os.makedirs(out, exist_ok=True)
            c1_name = cc.card_pdf_name(cfg, "demo", "AA1", "bridge", "en", 3.0, False)
            _write(os.path.join(out, c1_name), "pdf")
            cfg_path = _write(os.path.join(tmp, "pdf_config.yaml"), "project: test\n")

            with mock.patch.object(merge_pdfs, "pymupdf", mock.MagicMock()):
                with mock.patch("merge_pdfs.merge_deck", return_value=2):
                    with mock.patch("cornucopia_common.load_yaml", return_value=cfg):
                        with mock.patch(
                            "sys.argv",
                            [
                                "merge_pdfs.py",
                                "--config",
                                cfg_path,
                                "--base-dir",
                                tmp,
                                "--output-dir",
                                out,
                                "--clean",
                                "--zip",
                            ],
                        ):
                            self.assertEqual(merge_pdfs.main(), 0)

    def test_run_as_script(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch(
                "sys.argv",
                [
                    "merge_pdfs.py",
                    "--dry-run",
                    "--edition",
                    "webapp",
                    "--language",
                    "en",
                    "--size",
                    "bridge",
                    "--output-dir",
                    tmp,
                ],
            ):
                with self.assertRaises(SystemExit) as ctx:
                    runpy.run_path(os.path.join(_PDF_GENERATION, "merge_pdfs.py"), run_name="__main__")
                self.assertEqual(ctx.exception.code, 0)


_MINIMAL_SLA = """<?xml version="1.0" encoding="utf-8"?>
<SCRIBUSUTF8NEW Version="1.5.8">
  <DOCUMENT>
    <COLOR NAME="Data_Color" SPACE="CMYK" C="0" M="0" Y="0" K="50" />
    <PAGEOBJECT ANNAME="special_text" PTYPE="4">
      <ITEXT CH="text" />
      <DefaultStyle />
      <trail />
      <para />
    </PAGEOBJECT>
    <PAGEOBJECT ANNAME="attack_text" PTYPE="4">
      <ITEXT CH="text" />
      <DefaultStyle />
      <trail />
      <para />
    </PAGEOBJECT>
    <PAGEOBJECT ANNAME="card_number" PTYPE="4">
      <ITEXT CH="1" />
      <DefaultStyle />
      <trail />
      <para />
    </PAGEOBJECT>
    <PAGEOBJECT ANNAME="suit_name" PTYPE="4" CSTYLE="old" PSTYLE="old">
      <ITEXT CH="Suit" CSTYLE="old" PSTYLE="old" />
      <DefaultStyle PARENT="old" />
      <trail PARENT="old" />
      <para CSTYLE="old" PSTYLE="old" />
    </PAGEOBJECT>
    <PAGEOBJECT ANNAME="url_text" PTYPE="4">
      <ITEXT CH="https://example.com" />
    </PAGEOBJECT>
    <PAGEOBJECT ANNAME="Polygon1" PTYPE="6" PCOLOR="Fallback_Grey" TransBlend="1" TransBlendS="1" />
    <PAGEOBJECT ANNAME="card_border" PTYPE="2" />
    <PAGEOBJECT ANNAME="qr_code" PTYPE="2" />
    <PAGEOBJECT ANNAME="card_back" PTYPE="2" />
  </DOCUMENT>
</SCRIBUSUTF8NEW>
"""


class TestGenerateDeckBuildLog(unittest.TestCase):
    def test_build_log(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log_path = os.path.join(tmp, "subdir", "build.log")
            log = generate_deck.BuildLog(log_path)
            self.assertTrue(os.path.exists(log_path))
            log.info("info msg")
            log.warn("warn msg")
            self.assertIn("warn msg", log.warnings)
            with open(log_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("info msg", content)
                self.assertIn("WARNING: warn msg", content)


class TestGenerateDeckXmlAndColorHelpers(unittest.TestCase):
    def test_inject_color_definitions_document_fallback_and_missing_spec(self) -> None:
        import xml.etree.ElementTree as ET

        root = ET.Element("SCRIBUSUTF8NEW")
        # Add existing color
        color_elem = ET.SubElement(root, "COLOR")
        color_elem.set("NAME", "Existing")

        log = generate_deck.BuildLog(os.path.join(tempfile.mkdtemp(), "b.log"))
        config = {"color_definitions": {"ValidColor": {"c": 10, "m": 20, "y": 30, "k": 40}}}
        added = generate_deck.inject_color_definitions(
            root, config, ["", "Existing", "MissingColor", "ValidColor"], log
        )
        self.assertEqual(added, ["ValidColor"])
        self.assertTrue(any("MissingColor" in w for w in log.warnings))

    def test_move_sla_object_y_and_fill_card_number(self) -> None:
        import xml.etree.ElementTree as ET

        frame = ET.Element("PAGEOBJECT")
        frame.set("gYpos", "10.0")
        generate_deck.move_sla_object_y(frame, 5.0)
        self.assertEqual(frame.get("gYpos"), "15.0")

        # fill_card_number with joker
        frame_num = ET.fromstring("<PAGEOBJECT><ITEXT CH='1'/></PAGEOBJECT>")
        style = {"joker": True, "joker_label": "Joker", "number_color": "Red"}
        card = {"card_kind": "SpecialJoker"}
        generate_deck.fill_card_number(frame_num, card, style)
        self.assertEqual(frame_num.find("ITEXT").get("CH"), "SpecialJoker")

    def test_recolour_suit_band_cleans_trans_blend(self) -> None:
        import xml.etree.ElementTree as ET

        frame = ET.Element("PAGEOBJECT")
        frame.set("TransBlend", "1")
        frame.set("TransBlendS", "1")
        generate_deck.recolour_suit_band(frame, "CustomRed")
        self.assertEqual(frame.get("PCOLOR"), "CustomRed")
        self.assertNotIn("TransBlend", frame.attrib)
        self.assertNotIn("TransBlendS", frame.attrib)

    def test_text_frame_handlers_handle_para_elements(self) -> None:
        import xml.etree.ElementTree as ET

        style = {
            "defaults": {
                "special_text_color": "Black",
                "special_text_shade": 70,
                "body_text_color": "Black",
                "body_text_shade": 100,
            },
            "profile": {"special_text_y_offset": 5.0},
            "special_size": "8",
            "special_font": "Noto Sans Medium",
            "body_font": "Noto Sans Light",
            "heading_font": "Noto Sans Medium",
            "attack_size": "7",
            "number_color": "Black",
            "joker": False,
        }
        card = {
            "misc_text": "Read more",
            "attack_text": "Attack description",
            "value": "A",
            "suit_name": "Authentication",
            "url": "https://owasp.org",
        }

        # special_text with para
        frame_spec = ET.fromstring("<PAGEOBJECT><ITEXT /><DefaultStyle /><trail /><para /></PAGEOBJECT>")
        generate_deck.fill_special_text(frame_spec, card, style)
        self.assertEqual(frame_spec.find("para").get("FONT"), "Noto Sans Medium")

        # attack_text with para
        frame_att = ET.fromstring("<PAGEOBJECT><ITEXT /><DefaultStyle /><trail /><para /></PAGEOBJECT>")
        generate_deck.fill_attack_text(frame_att, card, style)
        self.assertEqual(frame_att.find("para").get("FONT"), "Noto Sans Light")

        # suit_name with para
        frame_suit = ET.fromstring("<PAGEOBJECT><ITEXT /><DefaultStyle /><trail /><para /></PAGEOBJECT>")
        generate_deck.fill_suit_name(frame_suit, card, style)
        self.assertEqual(frame_suit.find("para").get("FONT"), "Noto Sans Medium")

    def test_populate_frame_ptype_6(self) -> None:
        import xml.etree.ElementTree as ET

        frame = ET.fromstring('<PAGEOBJECT PTYPE="6" PCOLOR="Data_Color" />')
        style = {"suit_color": "Custom_Color"}
        res = generate_deck.populate_frame(frame, {}, style, {}, {"Data_Color"})
        self.assertFalse(res)
        self.assertEqual(frame.get("PCOLOR"), "Custom_Color")


class TestGenerateDeckQrAndArtwork(unittest.TestCase):
    def test_create_qr_image_pypng_and_pillow_fallbacks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            qr_file = os.path.join(tmp, "qr.png")
            # Normal create
            generate_deck.create_qr_image("https://owasp.org", qr_file, {})
            self.assertTrue(os.path.exists(qr_file))

            # Simulate png missing but Pillow present
            original_import = __import__

            def fake_import_pil_fallback(name, *args, **kwargs):
                if name == "png":
                    raise ImportError("No png module")
                if name == "PIL":
                    return mock.MagicMock()
                return original_import(name, *args, **kwargs)

            mock_img = mock.MagicMock()
            with mock.patch("builtins.__import__", side_effect=fake_import_pil_fallback):
                with mock.patch.object(
                    generate_deck.qrcode.QRCode, "make_image", return_value=mock_img
                ) as mock_make_image:
                    qr_file2 = os.path.join(tmp, "qr2.png")
                    generate_deck.create_qr_image("https://owasp.org", qr_file2, {})
                    mock_make_image.assert_called_once_with(fill_color="black", back_color="transparent")
                    mock_img.save.assert_called_once_with(qr_file2)

            # Simulate both png and PIL missing
            def fake_import_no_png_no_pil(name, *args, **kwargs):
                if name in ("png", "PIL"):
                    raise ImportError("Missing image library")
                return original_import(name, *args, **kwargs)

            with mock.patch("builtins.__import__", side_effect=fake_import_no_png_no_pil):
                with self.assertRaises(ImportError) as ctx:
                    generate_deck.create_qr_image("https://owasp.org", os.path.join(tmp, "qr3.png"), {})
                self.assertIn("Cannot render QR codes", str(ctx.exception))

    def test_card_artwork_missing_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log_path = os.path.join(tmp, "build.log")
            log = generate_deck.BuildLog(log_path)
            cfg = _base_config(_DATA_PATTERN)
            os.makedirs(cc.qr_dir(cfg, tmp), exist_ok=True)
            card = {"card_id": "AA1", "suit_id": "aa", "value": "A", "url": "https://owasp.org"}
            generate_deck.card_artwork(card, "demo", "en", "bridge", cfg, {}, tmp, log)
            self.assertTrue(any("Card back missing" in w for w in log.warnings))
            self.assertTrue(any("Artwork missing" in w for w in log.warnings))


class TestGenerateDeckScribusExport(unittest.TestCase):
    def test_apply_scribus_colours_and_failures(self) -> None:
        mock_scribus = mock.MagicMock()
        mock_log = mock.MagicMock()
        cfg = _base_config(_DATA_PATTERN)
        card = {"card_id": "AA1", "suit_id": "aa", "value": "A"}

        with mock.patch.object(generate_deck, "scribus", mock_scribus, create=True):
            # Success with Polygon1
            generate_deck.apply_scribus_colours(card, "demo", "en", cfg, {}, mock_log)
            mock_scribus.setTextColor.assert_any_call("Demo_AA", "card_number")
            mock_scribus.setFillColor.assert_any_call("Demo_AA", "Polygon1")

            # Failure on setTextColor warns
            mock_scribus.setTextColor.side_effect = Exception("Scribus error")
            generate_deck.apply_scribus_colours(card, "demo", "en", cfg, {}, mock_log)
            mock_log.warn.assert_called()

    def test_back_frame_name_and_place_artwork_frame(self) -> None:
        mock_scribus = mock.MagicMock()
        with mock.patch.object(generate_deck, "scribus", mock_scribus, create=True):
            name = generate_deck.back_frame_name()
            self.assertEqual(name, "card_back")
            mock_scribus.gotoPage.assert_called_with(2)

            generate_deck.place_artwork_frame("frame1", 68.0, 99.0, -6.0)
            mock_scribus.sizeObject.assert_called_with(68.0, 99.0, "frame1")
            mock_scribus.moveObjectAbs.assert_called_with(-6.0, -6.0, "frame1")

    def test_write_pdf_options_and_icc_handling(self) -> None:
        mock_scribus = mock.MagicMock()
        mock_pdf = mock.MagicMock()
        mock_scribus.PDFfile.return_value = mock_pdf
        mock_log = mock.MagicMock()

        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(generate_deck, "scribus", mock_scribus, create=True):
                cfg = _base_config(_DATA_PATTERN)
                card = {"card_id": "AA1"}

                # Successful ICC profile setting
                cfg["output"]["color_mode"] = "cmyk"
                cfg["output"]["icc_profile"] = "Coated_FOGRA39"
                generate_deck.write_pdf(
                    {"bleed_mm": 3.0, "printers_marks": False},
                    card,
                    "demo",
                    "en",
                    "bridge",
                    cfg,
                    tmp,
                    mock_log,
                )
                self.assertEqual(mock_pdf.profiles, 1)
                self.assertEqual(mock_pdf.solidpr, "Coated_FOGRA39")
                self.assertEqual(mock_pdf.imagepr, "Coated_FOGRA39")
                self.assertEqual(mock_pdf.printprofc, "Coated_FOGRA39")

                # Unknown color mode and failing ICC profile
                cfg["output"]["color_mode"] = "invalid_mode"
                cfg["output"]["icc_profile"] = "Coated_FOGRA39"
                type(mock_pdf).solidpr = mock.PropertyMock(side_effect=Exception("ICC error"))

                res = generate_deck.write_pdf(
                    {"bleed_mm": 3.0, "printers_marks": True},
                    card,
                    "demo",
                    "en",
                    "bridge",
                    cfg,
                    tmp,
                    mock_log,
                )
                self.assertEqual(res["bleed"], "3")
                self.assertTrue(res["marks"])
                self.assertEqual(mock_pdf.outdst, 1)  # CMYK fallback
                self.assertEqual(mock_pdf.profiles, 0)
                mock_log.warn.assert_any_call("Unknown color_mode 'invalid_mode'; using cmyk")
                mock_pdf.save.assert_called()

    def test_export_pdfs_flow_and_exception_handling(self) -> None:
        # Scribus unavailable
        with mock.patch.object(generate_deck, "SCRIBUS_AVAILABLE", False):
            self.assertEqual(
                generate_deck.export_pdfs("sla", {}, "demo", "en", "bridge", {}, {}, "", "", [], mock.MagicMock()),
                [],
            )

        # Scribus available - success
        mock_scribus = mock.MagicMock()
        mock_log = mock.MagicMock()
        cfg = _base_config(_DATA_PATTERN)
        card = {"card_id": "AA1", "suit_id": "aa", "value": "A"}

        with mock.patch.object(generate_deck, "SCRIBUS_AVAILABLE", True):
            with mock.patch.object(generate_deck, "scribus", mock_scribus, create=True):
                with mock.patch("generate_deck.write_pdf", return_value={"path": "out.pdf"}):
                    with mock.patch("cornucopia_common.resolve_background", return_value=("bg.png", True)):
                        res = generate_deck.export_pdfs(
                            "sla.sla", card, "demo", "en", "bridge", cfg, {}, "", "", [{"bleed_mm": 3.0}], mock_log
                        )
                        self.assertEqual(len(res), 1)
                        mock_scribus.openDoc.assert_called_once_with("sla.sla")
                        mock_scribus.closeDoc.assert_called_once()

                # loadImage failure
                mock_scribus.reset_mock()
                mock_scribus.loadImage.side_effect = Exception("Load image error")
                with mock.patch("generate_deck.write_pdf", return_value={"path": "out.pdf"}):
                    with mock.patch("cornucopia_common.resolve_background", return_value=("bg.png", True)):
                        res = generate_deck.export_pdfs(
                            "sla.sla", card, "demo", "en", "bridge", cfg, {}, "", "", [{"bleed_mm": 3.0}], mock_log
                        )
                        mock_log.warn.assert_any_call("loadImage failed for AA1: Load image error")

                # Background not found
                mock_scribus.reset_mock()
                with mock.patch("generate_deck.write_pdf", return_value={"path": "out.pdf"}):
                    with mock.patch("cornucopia_common.resolve_background", return_value=("bg.png", False)):
                        res = generate_deck.export_pdfs(
                            "sla.sla", card, "demo", "en", "bridge", cfg, {}, "", "", [{"bleed_mm": 3.0}], mock_log
                        )
                        mock_log.warn.assert_any_call("Artwork not found for AA1: bg.png")

                # Export crash and closeDoc fails
                mock_scribus.openDoc.side_effect = Exception("Fatal open error")
                mock_scribus.closeDoc.side_effect = Exception("Fatal close error")
                res = generate_deck.export_pdfs(
                    "sla.sla", card, "demo", "en", "bridge", cfg, {}, "", "", [{"bleed_mm": 3.0}], mock_log
                )
                self.assertEqual(res, [])
                mock_log.warn.assert_any_call("Export crashed on AA1: Fatal open error")
                mock_log.warn.assert_any_call("Could not close document after that failure: Fatal close error")


class TestGenerateDeckSelectionAndOrchestration(unittest.TestCase):
    def test_parse_args(self) -> None:
        argv = [
            "generate_deck.py",
            "--config",
            "custom.yaml",
            "--edition",
            "demo",
            "--language",
            "en",
            "--size",
            "bridge",
            "--cards",
            "AA1,AA2",
            "--profile",
            "print",
            "--output-dir",
            "out",
            "--dry-run",
            "--skip-existing",
            "--base-dir",
            "/tmp/base",
        ]
        with mock.patch("sys.argv", argv):
            args = generate_deck.parse_args()
            self.assertEqual(args.config, "custom.yaml")
            self.assertEqual(args.edition, ["demo"])
            self.assertEqual(args.cards, "AA1,AA2")
            self.assertTrue(args.dry_run)
            self.assertTrue(args.skip_existing)

    def test_select_deck_conditions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log_path = os.path.join(tmp, "b.log")
            log = generate_deck.BuildLog(log_path)
            cfg = _base_config("source/%edition%-cards-%edition_version%-%language%.yaml")
            cfg["size_profiles"]["bridge"]["template"] = "missing_template.sla"
            target = {"edition": "demo", "language": "en", "size": "bridge"}
            args = mock.Mock(cards=None)

            # Template missing
            self.assertIsNone(generate_deck.select_deck(target, args, cfg, tmp, log))

            # Template found in SCRIPT_DIR
            cfg["size_profiles"]["bridge"]["template"] = "small_master.sla"
            # No cards found at data path
            self.assertIsNone(generate_deck.select_deck(target, args, cfg, tmp, log))

            # Cards found and filtered by --cards
            _write(
                os.path.join(tmp, "source", "demo-cards-1.0-en.yaml"),
                _card_yaml("  - id: AA\n    name: AA\n    cards:\n      - id: AA1\n      - id: AA2\n"),
            )
            _write(os.path.join(tmp, "tmpl.sla"), _MINIMAL_SLA)
            cfg["size_profiles"]["bridge"]["template"] = "tmpl.sla"
            args_cards = mock.Mock(cards="AA1")
            res = generate_deck.select_deck(target, args_cards, cfg, tmp, log)
            self.assertIsNotNone(res)
            deck, suits, template = res
            self.assertEqual(len(deck), 1)
            self.assertEqual(deck[0]["card_id"], "AA1")

            # Cards filtered by --cards but none match
            args_nomatch = mock.Mock(cards="UNKNOWN")
            self.assertIsNone(generate_deck.select_deck(target, args_nomatch, cfg, tmp, log))

    def test_report_missing_artwork_and_already_exported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log_path = os.path.join(tmp, "b.log")
            log = generate_deck.BuildLog(log_path)
            cfg = _base_config(_DATA_PATTERN)
            target = {"edition": "demo", "language": "en", "size": "bridge"}
            deck = [{"card_id": "AA{0}".format(i), "suit_id": "aa"} for i in range(12)]

            # report_missing_artwork with missing back and cards
            generate_deck.report_missing_artwork(deck, target, cfg, {}, tmp, log)
            self.assertTrue(any("artwork missing for 12 card(s)" in w for w in log.warnings))

            # all artwork resolved
            with mock.patch("cornucopia_common.resolve_card_back", return_value=("back.png", True)):
                with mock.patch("cornucopia_common.resolve_background", return_value=("bg.png", True)):
                    generate_deck.report_missing_artwork(deck, target, cfg, {}, tmp, log)

            # already_exported
            profiles = [{"bleed_mm": 3.0, "printers_marks": False}]
            card = {"card_id": "AA1"}
            self.assertFalse(generate_deck.already_exported(card, target, cfg, tmp, profiles))
            c_name = cc.card_pdf_name(cfg, "demo", "AA1", "bridge", "en", 3.0, False)
            _write(os.path.join(tmp, c_name), "pdf")
            self.assertTrue(generate_deck.already_exported(card, target, cfg, tmp, profiles))

    def test_build_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log_path = os.path.join(tmp, "b.log")
            log = generate_deck.BuildLog(log_path)
            cfg = _base_config("source/%edition%-cards-%edition_version%-%language%.yaml")
            cfg["editions"] = {"demo": {}}
            _write(os.path.join(tmp, "tmpl.sla"), _MINIMAL_SLA)
            cfg["size_profiles"]["bridge"]["template"] = "tmpl.sla"
            _write(
                os.path.join(tmp, "source", "demo-cards-1.0-en.yaml"),
                _card_yaml("  - id: AA\n    cards:\n      - id: AA1\n"),
            )
            out = os.path.join(tmp, "out")
            os.makedirs(out, exist_ok=True)
            target = {"edition": "demo", "language": "en", "size": "bridge"}
            profiles = [{"name": "main", "bleed_mm": 3.0, "printers_marks": False}]
            args_dry = mock.Mock(cards=None, dry_run=True, skip_existing=False)

            # Select deck returns None
            with mock.patch("generate_deck.select_deck", return_value=None):
                self.assertIsNone(generate_deck.build_target(target, args_dry, cfg, {}, tmp, out, profiles, log))

            # Dry run
            rec_dry = generate_deck.build_target(target, args_dry, cfg, {}, tmp, out, profiles, log)
            self.assertIsNotNone(rec_dry)
            self.assertEqual(rec_dry["cards"], 1)

            # Normal build with skip_existing
            args_run = mock.Mock(cards=None, dry_run=False, skip_existing=True)
            with mock.patch.object(generate_deck, "SCRIBUS_AVAILABLE", True):
                with mock.patch("generate_deck.already_exported", return_value=True):
                    rec = generate_deck.build_target(target, args_run, cfg, {}, tmp, out, profiles, log)
                    self.assertEqual(rec["pdfs"], 0)

            # Normal build executing generate_card
            with mock.patch.object(generate_deck, "SCRIBUS_AVAILABLE", False):
                args_build = mock.Mock(cards=None, dry_run=False, skip_existing=False)
                rec = generate_deck.build_target(target, args_build, cfg, {}, tmp, out, profiles, log)
                self.assertEqual(rec["cards"], 1)


class TestGenerateDeckMain(unittest.TestCase):
    def test_main_failures(self) -> None:
        # Config missing
        with mock.patch("sys.argv", ["generate_deck.py", "--config", "nonexistent.yaml"]):
            with mock.patch("cornucopia_common.load_yaml", return_value=None):
                self.assertEqual(generate_deck.main(), 1)

        # Base dir missing
        with mock.patch("sys.argv", ["generate_deck.py", "--base-dir", "/nonexistent/base"]):
            with mock.patch("cornucopia_common.load_yaml", return_value={"project": "test"}):
                self.assertEqual(generate_deck.main(), 1)

        # No targets
        with tempfile.TemporaryDirectory() as tmp:
            cfg_path = _write(os.path.join(tmp, "pdf_config.yaml"), "project: test\n")
            with mock.patch("sys.argv", ["generate_deck.py", "--config", cfg_path, "--base-dir", tmp]):
                with mock.patch("cornucopia_common.resolve_targets", return_value=([], ["No targets"])):
                    self.assertEqual(generate_deck.main(), 1)

            # Invalid profile
            with mock.patch(
                "sys.argv", ["generate_deck.py", "--config", cfg_path, "--base-dir", tmp, "--profile", "bad"]
            ):
                with mock.patch("cornucopia_common.resolve_targets", return_value=([{"edition": "demo"}], [])):
                    with mock.patch(
                        "cornucopia_common.get_export_profiles", side_effect=ValueError("Profile not found")
                    ):
                        self.assertEqual(generate_deck.main(), 1)

    def test_main_success_dry_run_and_build(self) -> None:
        import yaml

        with tempfile.TemporaryDirectory() as tmp:
            cfg = _base_config("source/%edition%-cards-%edition_version%-%language%.yaml")
            cfg["editions"] = {"demo": {}}
            _write(os.path.join(tmp, "tmpl.sla"), _MINIMAL_SLA)
            cfg["size_profiles"]["bridge"]["template"] = "tmpl.sla"
            _write(
                os.path.join(tmp, "source", "demo-cards-1.0-en.yaml"),
                _card_yaml(
                    "  - id: AA\n"
                    "    name: AA\n"
                    "    cards:\n"
                    "      - id: AA1\n"
                    "        value: '1'\n"
                    "        desc: atk\n"
                    "        url: ''\n"
                ),
            )
            cfg_path = os.path.join(tmp, "pdf_config.yaml")
            with open(cfg_path, "w", encoding="utf-8") as f:
                yaml.dump(cfg, f)
            out = os.path.join(tmp, "out")

            # Dry run
            with mock.patch(
                "sys.argv",
                [
                    "generate_deck.py",
                    "--config",
                    cfg_path,
                    "--base-dir",
                    tmp,
                    "--output-dir",
                    out,
                    "--edition",
                    "demo",
                    "--language",
                    "en",
                    "--size",
                    "bridge",
                    "--dry-run",
                ],
            ):
                self.assertEqual(generate_deck.main(), 0)

            # Real build
            with mock.patch(
                "sys.argv",
                [
                    "generate_deck.py",
                    "--config",
                    cfg_path,
                    "--base-dir",
                    tmp,
                    "--output-dir",
                    out,
                    "--edition",
                    "demo",
                    "--language",
                    "en",
                    "--size",
                    "bridge",
                ],
            ):
                self.assertEqual(generate_deck.main(), 0)

    def test_module_import_fallbacks(self) -> None:
        original_import = __import__

        # cornucopia_common missing raises ImportError and writes to stderr
        def fake_import_no_cc(name, *args, **kwargs):
            if name == "cornucopia_common":
                raise ImportError("mock cc missing")
            return original_import(name, *args, **kwargs)

        with mock.patch("builtins.__import__", side_effect=fake_import_no_cc):
            with self.assertRaises(ImportError):
                runpy.run_path(os.path.join(_PDF_GENERATION, "generate_deck.py"))

        # defusedxml missing sets XML_HARDENED = False
        def fake_import_no_defusedxml(name, *args, **kwargs):
            if name == "defusedxml.ElementTree":
                raise ImportError("mock defusedxml missing")
            return original_import(name, *args, **kwargs)

        with mock.patch("builtins.__import__", side_effect=fake_import_no_defusedxml):
            runpy.run_path(os.path.join(_PDF_GENERATION, "generate_deck.py"))

        # qrcode missing sets QR_AVAILABLE = False
        def fake_import_no_qr(name, *args, **kwargs):
            if name == "qrcode":
                raise ImportError("mock qrcode missing")
            return original_import(name, *args, **kwargs)

        with mock.patch("builtins.__import__", side_effect=fake_import_no_qr):
            runpy.run_path(os.path.join(_PDF_GENERATION, "generate_deck.py"))

    def test_main_fatal_exception_and_system_exit(self) -> None:
        # SystemExit passes through
        with mock.patch("sys.argv", ["generate_deck.py", "--config", "nonexistent.yaml"]):
            with self.assertRaises(SystemExit) as ctx:
                runpy.run_path(os.path.join(_PDF_GENERATION, "generate_deck.py"), run_name="__main__")
            self.assertEqual(ctx.exception.code, 1)

        # Exception caught, logged to build_log.txt, and re-raised
        log_file = os.path.join(_PDF_GENERATION, "build_log.txt")
        had_log_before = os.path.exists(log_file)
        original_log_bytes = None
        if had_log_before:
            with open(log_file, "rb") as f:
                original_log_bytes = f.read()

        try:
            with mock.patch("sys.argv", ["generate_deck.py", "--config", "nonexistent.yaml"]):
                with mock.patch("cornucopia_common.find_config_path", side_effect=RuntimeError("Fatal deck crash")):
                    with self.assertRaises(RuntimeError):
                        runpy.run_path(os.path.join(_PDF_GENERATION, "generate_deck.py"), run_name="__main__")
        finally:
            if had_log_before:
                with open(log_file, "wb") as f:
                    f.write(original_log_bytes if original_log_bytes is not None else b"")
            elif os.path.exists(log_file):
                os.remove(log_file)


if __name__ == "__main__":
    unittest.main()
