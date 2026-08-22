#!/usr/bin/env python3
"""Integration tests for Scribus template population.

These run the generator against the real .sla master templates, then parse the
files it produces and check what was injected: the card text, the fonts chosen
for a language, the colours, the artwork selected, and whether the optional
special-text frame was kept or removed.

Scribus itself is only needed to export a PDF. Writing and reading the .sla is
plain XML, so these tests run anywhere and cover the part of the pipeline that
decides what each card says and looks like.
"""

import os
import sys
import tempfile
import unittest

# Used only for type annotations; the .sla files are read with defusedxml's
# parser below, which is how scripts/convert.py handles the same job.
import xml.etree.ElementTree as ET  # nosec B405
from defusedxml.ElementTree import parse as parse_xml

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_PDF_GENERATION = os.path.join(_REPO_ROOT, "scripts", "pdf_generation")
if _PDF_GENERATION not in sys.path:
    sys.path.insert(0, _PDF_GENERATION)

import generate_deck  # noqa: E402  (needs the sys.path line above)

BRIDGE_TEMPLATE = os.path.join(_PDF_GENERATION, "small_master.sla")


class _CollectingLog:
    """Stands in for the build log, keeping messages so tests can inspect them."""

    def __init__(self) -> None:
        self.warnings: list = []

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def info(self, message: str) -> None:
        """Deliberately discarded. Only warnings are asserted on."""


def _touch(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "a", encoding="utf-8").close()


def _frame(root: ET.Element, name: str):
    """The PAGEOBJECT with the given Scribus object name, or None if removed."""
    for obj in root.iter("PAGEOBJECT"):
        if obj.get("ANNAME", "").strip().lower() == name:
            return obj
    return None


def _texts(frame) -> list:
    return [itext.get("CH") for itext in frame.iter("ITEXT")]


def _fonts(frame) -> set:
    return {itext.get("FONT") for itext in frame.iter("ITEXT") if itext.get("FONT")}


class TemplatePopulationTestCase(unittest.TestCase):
    """Shared fixture: a temporary workspace with artwork and a config."""

    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()
        self.log = _CollectingLog()

        art = os.path.join(self.tmp, "art", "card_artwork", "demo")
        for name in ("aa-small-default.png", "aa-small-court.png", "wc-small-default.png", "back_small.png"):
            _touch(os.path.join(art, name))
        os.makedirs(os.path.join(self.tmp, "qrcodes"), exist_ok=True)

        self.config = {
            "project": {"version": "9.9"},
            "paths": {"asset_root": "art", "qr_code_dir": "qrcodes"},
            "size_profiles": {
                "bridge": {
                    "asset_key": "small",
                    "special_text_y_offset": 6.0,
                    "base_font_sizes": {"attack_text": 7.0, "special_text": 8.0, "special_text_joker": 8.0},
                }
            },
            "font_handling": {
                "default": {
                    "body": "Noto Sans Light",
                    "heading": "Noto Sans Medium",
                    "accent": "Noto Sans Medium Italic",
                },
                "hi": {
                    "body": "Noto Sans Devanagari Light",
                    "heading": "Noto Sans Devanagari Medium",
                    "accent": "Noto Sans Devanagari Regular",
                },
            },
            "font_scaling": {"attack_text": {"default": 0.0, "hi": -1.0}},
            "assets": {
                "image_dir": "card_artwork",
                "background_pattern": "%edition%/%suit%-%size%-%variant%.png",
                "card_back_pattern": "%edition%/back_%size%.png",
            },
            "card_semantics": {"court_values": ["J", "Q", "K"], "value_order": {"A": 1, "2": 2, "K": 13}},
            "defaults": {
                "suit_color": "Fallback_Grey",
                "court_text_color": "Pure_White",
                "suit_name_color": "Pure_White",
                "body_text_color": "Black",
                "body_text_shade": "100",
                "special_text_color": "Black",
                "special_text_shade": "70",
            },
            "editions": {"demo": {"joker_suits": ["wc"]}},
            "color_definitions": {},
            "output": {},
        }
        self.assets = {"demo": {"suits": [{"id": "AA", "color": {"c": 10, "m": 20, "y": 30, "k": 40}}]}}

    def build(self, card: dict, language: str = "en") -> ET.Element:
        """Generate one card and return the root of the .sla it produced."""
        out = os.path.join(self.tmp, "{0}_{1}.sla".format(card["card_id"], language))
        generate_deck.generate_card(
            card, "demo", language, "bridge", BRIDGE_TEMPLATE, out, self.config, self.assets, self.tmp, self.log
        )
        self.assertTrue(os.path.exists(out), "no .sla was written")
        return parse_xml(out).getroot()

    @staticmethod
    def card(**overrides) -> dict:
        base = {
            "card_id": "AA2",
            "suit_id": "AA",
            "suit_name": "Alpha Suit",
            "value": "2",
            "attack_text": "An attacker does something undesirable.",
            "misc_text": "",
            "card_kind": "",
            "url": "",
        }
        base.update(overrides)
        return base


class TestCardTextIsInjected(TemplatePopulationTestCase):
    def test_the_description_reaches_the_attack_frame(self) -> None:
        root = self.build(self.card())
        self.assertIn("An attacker does something undesirable.", _texts(_frame(root, "attack_text")))

    def test_the_suit_name_reaches_its_frame(self) -> None:
        root = self.build(self.card())
        self.assertIn("Alpha Suit", _texts(_frame(root, "suit_name")))

    def test_the_card_value_reaches_the_number_frame(self) -> None:
        root = self.build(self.card(value="2"))
        self.assertIn("2", _texts(_frame(root, "card_number")))

    def test_the_url_reaches_its_frame(self) -> None:
        root = self.build(self.card(url="https://example.org/card"))
        self.assertIn("https://example.org/card", _texts(_frame(root, "url_text")))

    def test_the_output_is_well_formed_xml(self) -> None:
        root = self.build(self.card())
        self.assertEqual(root.tag, "SCRIBUSUTF8NEW")


class TestSpecialTextFrame(TemplatePopulationTestCase):
    def test_the_frame_is_removed_when_a_card_has_no_misc_text(self) -> None:
        root = self.build(self.card(misc_text=""))
        self.assertIsNone(_frame(root, "special_text"), "frame should be removed for a card with no misc text")

    def test_the_frame_is_kept_and_filled_when_misc_text_is_present(self) -> None:
        root = self.build(self.card(card_id="AAA", value="A", misc_text="Further reading."))
        frame = _frame(root, "special_text")
        self.assertIsNotNone(frame)
        self.assertIn("Further reading.", _texts(frame))

    def test_a_joker_uses_the_accent_font_for_its_misc_text(self) -> None:
        joker = self.card(card_id="JOA", suit_id="WC", value="A", misc_text="Wild.", card_kind="Joker")
        frame = _frame(self.build(joker), "special_text")
        self.assertIn("Noto Sans Medium Italic", _fonts(frame))


class TestFontSelection(TemplatePopulationTestCase):
    def test_english_uses_the_default_body_font(self) -> None:
        root = self.build(self.card(), language="en")
        self.assertIn("Noto Sans Light", _fonts(_frame(root, "attack_text")))

    def test_hindi_uses_the_devanagari_body_font(self) -> None:
        root = self.build(self.card(), language="hi")
        self.assertIn("Noto Sans Devanagari Light", _fonts(_frame(root, "attack_text")))

    def test_the_suit_name_uses_the_heading_font_not_the_body_font(self) -> None:
        root = self.build(self.card())
        self.assertIn("Noto Sans Medium", _fonts(_frame(root, "suit_name")))

    def test_a_dense_language_gets_the_reduced_size(self) -> None:
        root = self.build(self.card(), language="hi")
        sizes = {itext.get("FONTSIZE") for itext in _frame(root, "attack_text").iter("ITEXT")}
        self.assertIn("6.0", sizes)

    def test_the_base_size_is_used_where_no_offset_applies(self) -> None:
        root = self.build(self.card(), language="en")
        sizes = {itext.get("FONTSIZE") for itext in _frame(root, "attack_text").iter("ITEXT")}
        self.assertIn("7.0", sizes)


class TestArtworkSelection(TemplatePopulationTestCase):
    def test_a_pip_card_gets_the_default_artwork(self) -> None:
        root = self.build(self.card(value="2"))
        self.assertTrue(_frame(root, "card_border").get("PFILE").endswith("aa-small-default.png"))

    def test_a_court_card_gets_the_court_artwork(self) -> None:
        root = self.build(self.card(card_id="AAK", value="K"))
        self.assertTrue(_frame(root, "card_border").get("PFILE").endswith("aa-small-court.png"))

    def test_the_card_back_is_set(self) -> None:
        root = self.build(self.card())
        self.assertTrue(_frame(root, "card_back").get("PFILE").endswith("back_small.png"))

    def test_missing_artwork_is_reported_as_a_warning(self) -> None:
        self.build(self.card(suit_id="ZZ", card_id="ZZ2"))
        self.assertTrue(any("Artwork missing" in w for w in self.log.warnings))


class TestColourApplication(TemplatePopulationTestCase):
    def test_an_inline_cmyk_colour_is_added_to_the_document(self) -> None:
        root = self.build(self.card())
        names = {c.get("NAME") for c in root.iter("COLOR")}
        self.assertIn("Suit_Demo_AA", names)

    def test_the_injected_colour_carries_the_configured_values(self) -> None:
        root = self.build(self.card())
        swatch = [c for c in root.iter("COLOR") if c.get("NAME") == "Suit_Demo_AA"][0]
        self.assertEqual(swatch.get("SPACE"), "CMYK")
        self.assertEqual((swatch.get("C"), swatch.get("M"), swatch.get("Y"), swatch.get("K")), ("10", "20", "30", "40"))

    def test_a_pip_card_number_takes_the_suit_colour(self) -> None:
        root = self.build(self.card(value="2"))
        colours = {itext.get("FCOLOR") for itext in _frame(root, "card_number").iter("ITEXT")}
        self.assertIn("Suit_Demo_AA", colours)

    def test_a_court_card_number_is_white(self) -> None:
        root = self.build(self.card(card_id="AAK", value="K"))
        colours = {itext.get("FCOLOR") for itext in _frame(root, "card_number").iter("ITEXT")}
        self.assertIn("Pure_White", colours)


class TestJokerHandling(TemplatePopulationTestCase):
    def test_the_joker_label_comes_from_the_card_data(self) -> None:
        joker = self.card(card_id="JOA", suit_id="WC", value="A", card_kind="Jolly", misc_text="Wild.")
        self.assertIn("Jolly", _texts(_frame(self.build(joker), "card_number")))

    def test_an_ordinary_card_shows_its_value_instead(self) -> None:
        self.assertIn("2", _texts(_frame(self.build(self.card(value="2")), "card_number")))


class TestGeneratedFilesAreIndependent(TemplatePopulationTestCase):
    def test_generating_one_card_does_not_alter_the_master_template(self) -> None:
        with open(BRIDGE_TEMPLATE, "rb") as handle:
            before = handle.read()
        self.build(self.card())
        with open(BRIDGE_TEMPLATE, "rb") as handle:
            self.assertEqual(handle.read(), before, "the master template must never be modified")

    def test_two_languages_produce_different_files(self) -> None:
        english = self.build(self.card(), language="en")
        hindi = self.build(self.card(), language="hi")
        self.assertNotEqual(_fonts(_frame(english, "attack_text")), _fonts(_frame(hindi, "attack_text")))


if __name__ == "__main__":
    unittest.main()
