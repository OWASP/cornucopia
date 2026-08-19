"""
OWASP Cornucopia — deck generation engine.

Reads pdf_config.yaml and the source card YAML, injects card data into the
Scribus master templates, and (when running inside Scribus) exports print-ready
PDFs.

The engine holds no knowledge of how many editions, languages or suits exist,
whether an edition has jokers, or how a given language should be typeset. All
of that comes from pdf_config.yaml via cornucopia_common.

Run inside Scribus:   Script > Execute Script > generate_deck.py
Run standalone:       python generate_deck.py --dry-run
                      (writes .sla files only; PDF export needs Scribus)
"""

import argparse
import json
import os
import sys
import traceback

# Used only to build new elements, which carries no parsing risk. Reading XML
# goes through parse_xml below.
import xml.etree.ElementTree as ET  # nosec B405

# Make sibling modules importable when Scribus executes this by absolute path.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

try:
    import cornucopia_common as cc  # noqa: E402  (needs the sys.path line above)
except ImportError as exc:
    # Scribus runs scripts in its own interpreter, which is usually not the
    # `python3` on your PATH. Packages installed with the wrong one are
    # invisible here, and the bare traceback does not make that obvious.
    sys.stderr.write(
        "\nERROR: a required package is missing: {0}\n\n"
        "This script is running in:\n"
        "  {1}\n"
        "  Python {2}\n"
        "  PYTHONPATH={3}\n\n"
        "Packages must be installed into THAT interpreter, or be on its\n"
        "PYTHONPATH. Installing them with a different python3 will not work.\n\n"
        "If you installed with 'pip install --target <dir>', check that\n"
        "PYTHONPATH is EXPORTED in this terminal:\n"
        "  export PYTHONPATH=<dir>\n"
        "  echo $PYTHONPATH        # must print the path\n\n"
        "Setting it without 'export' does not pass it to Scribus.\n\n"
        "To see what this interpreter can and cannot find, run\n"
        "check_environment.py the same way. See README.md.\n\n".format(
            exc, sys.prefix, sys.version.split()[0], os.environ.get("PYTHONPATH") or "(not set)"
        )
    )
    raise

try:
    # Hardened XML parser. The templates read here are this repository's own
    # .sla files rather than user-supplied data, but the safe parser is used
    # whenever it is available.
    from defusedxml.ElementTree import parse as parse_xml

    XML_HARDENED = True
except ImportError:
    # defusedxml is not installed. Fall back rather than refuse to run, so a
    # missing optional package cannot stop a build; install it where you can.
    from xml.etree.ElementTree import parse as parse_xml  # nosec B405

    XML_HARDENED = False

try:
    import qrcode

    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

try:
    import scribus

    SCRIBUS_AVAILABLE = True
except ImportError:
    SCRIBUS_AVAILABLE = False


# --------------------------------------------------------------------------
# Logging — absolute paths, because Scribus changes the working directory
# when it opens a document.
# --------------------------------------------------------------------------


class BuildLog(object):
    def __init__(self, path):
        self.path = path
        self.warnings = []
        parent = os.path.dirname(os.path.abspath(path))
        if parent and not os.path.isdir(parent):
            os.makedirs(parent, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as handle:
            handle.write("=== OWASP Cornucopia build log ===\n")

    def write(self, message):
        with open(self.path, "a", encoding="utf-8") as handle:
            handle.write("{0}\n".format(message))

    def warn(self, message):
        self.warnings.append(message)
        self.write("WARNING: {0}".format(message))
        print("  WARNING: {0}".format(message))

    def info(self, message):
        self.write(message)
        print(message)


# --------------------------------------------------------------------------
# Scribus XML helpers — unchanged behaviour, these drive line spacing and
# glyph rendering and are deliberately left exactly as they were.
# --------------------------------------------------------------------------


def set_sla_text_color(page_object, color_name):
    for default_style in page_object.iter("DefaultStyle"):
        default_style.set("FCOLOR", color_name)
    for itext in page_object.iter("ITEXT"):
        itext.set("FCOLOR", color_name)


def move_sla_object_y(page_object, offset):
    for attr in ("YPOS", "gYpos"):
        value = page_object.get(attr)
        if value is not None:
            page_object.set(attr, str(float(value) + offset))


def inject_color_definitions(root, config, needed_names, log, extra_definitions=None):
    """
    Add any referenced swatch that the master template does not already define.

    This is what lets a new edition ship its own palette from config or
    assets.yaml without anyone hand-editing the .sla files in the Scribus GUI.
    """
    document = root.find("DOCUMENT")
    if document is None:
        document = root

    existing = {color.get("NAME") for color in root.iter("COLOR")}
    definitions = dict(config.get("color_definitions", {}) or {})
    definitions.update(extra_definitions or {})
    added = []

    for name in list(needed_names) + sorted(extra_definitions or {}):
        if not name or name in existing:
            continue
        spec = definitions.get(name)
        if not spec:
            log.warn(
                "Swatch '{0}' is referenced but has no entry in "
                "color_definitions; Scribus will fall back.".format(name)
            )
            continue
        element = ET.Element("COLOR")
        element.set("NAME", name)
        element.set("SPACE", "CMYK")
        for axis in ("c", "m", "y", "k"):
            element.set(axis.upper(), str(int(spec.get(axis, 0))))
        document.insert(0, element)
        added.append(name)

    return added


def create_qr_image(url, output_path, config):
    """
    Draw one card's QR code.

    The pure-Python PNG writer from pypng is requested explicitly rather than
    letting qrcode choose. Two reasons: qrcode 7 falls back to it when Pillow
    is absent but qrcode 8 defaults to Pillow and fails instead, and naming it
    outright means every machine produces the same image whether or not Pillow
    happens to be installed.
    """
    qr_cfg = config.get("qr", {}) or {}
    qr = qrcode.QRCode(
        version=qr_cfg.get("version", 1),
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=qr_cfg.get("box_size", 10),
        border=qr_cfg.get("border", 0),
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Test for pypng itself: qrcode's PyPNGImage class imports fine without it
    # and only fails when the image is actually drawn.
    try:
        import png  # noqa: F401
        from qrcode.image.pure import PyPNGImage

        image = qr.make_image(image_factory=PyPNGImage)
    except ImportError:
        # Pillow is the only other renderer qrcode offers. It is not what the
        # published decks use -- Scribus has pypng -- but falling back keeps
        # .sla generation working in a plain Python that lacks pypng.
        try:
            import PIL  # noqa: F401
        except ImportError:
            raise ImportError(
                "Cannot render QR codes: install 'pypng' (preferred) or "
                "'pillow' into the interpreter running this script. "
                "See README.md."
            )
        image = qr.make_image(fill_color="black", back_color="transparent")

    image.save(output_path)


# --------------------------------------------------------------------------
# Card generation
# --------------------------------------------------------------------------


def recolorable_swatches(config):
    """
    Every swatch name that may appear as the placeholder fill on the suit band
    in a master template. Collected across all editions so one template can
    serve any of them.
    """
    names = set()
    for edition in config.get("editions", {}) or {}:
        names.update((cc.edition_config(config, edition).get("suit_colors") or {}).values())
    fallback = (config.get("defaults", {}) or {}).get("suit_color")
    if fallback:
        names.add(fallback)
    return {n for n in names if n}


def card_style(card, edition, language, size_key, config, assets_data):
    """
    Everything that has to be decided once per card before the template is
    touched: which fonts, which sizes, which colours, and whether this card is
    a joker or carries misc text.
    """
    joker = cc.is_joker(card, config, edition)
    suit_color, number_color, inline_swatches = cc.card_colors(config, assets_data, edition, card, language)
    body_font = cc.get_font(config, language, "body")
    special_frame = "special_text_joker" if joker else "special_text"

    return {
        "defaults": config.get("defaults", {}) or {},
        "profile": (config.get("size_profiles", {}) or {}).get(size_key, {}) or {},
        "joker": joker,
        "joker_label": (config.get("card_semantics", {}) or {}).get("joker_label", "Joker"),
        "special": cc.has_special_text(card),
        "suit_color": suit_color,
        "number_color": number_color,
        "inline_swatches": inline_swatches,
        "body_font": body_font,
        "heading_font": cc.get_font(config, language, "heading"),
        "special_font": cc.get_font(config, language, "accent") if joker else body_font,
        "special_size": str(cc.get_font_size(config, size_key, special_frame, language)),
        "attack_size": str(cc.get_font_size(config, size_key, "attack_text", language)),
    }


def card_artwork(card, edition, language, size_key, config, assets_data, base_dir, log):
    """
    Locate this card's images, reporting anything missing, and draw its QR
    code. Returns the three paths the template needs.
    """
    qr_path = "{0}/{1}.png".format(cc.qr_dir(config, base_dir).replace("\\", "/"), card["card_id"])

    back_path, back_found = cc.resolve_card_back(config, base_dir, edition, size_key)
    border_path, border_found = cc.resolve_background(config, assets_data, base_dir, edition, card, size_key, language)

    if not back_found:
        log.warn("Card back missing for {0}/{1}: {2}".format(edition, size_key, back_path))
    if not border_found:
        log.warn("Artwork missing for card {0} ({1}/{2}): {3}".format(card["card_id"], edition, size_key, border_path))

    if card["url"] and QR_AVAILABLE:
        create_qr_image(card["url"], qr_path, config)

    return border_path, back_path, qr_path


def fill_image_frame(frame, path, aspect_ratio):
    frame.set("PFILE", path)
    frame.set("ScaleType", "1")
    frame.set("AspectRatio", aspect_ratio)


def recolour_suit_band(frame, suit_color):
    """Tint the coloured band. It sits under opaque artwork, so this is cosmetic."""
    frame.set("PCOLOR", suit_color)
    frame.set("SHADE", "100")
    frame.set("TransValue", "0")
    frame.set("TransValueS", "0")
    frame.attrib.pop("TransBlend", None)
    frame.attrib.pop("TransBlendS", None)


def fill_special_text(frame, card, style):
    """The optional 'read more' frame, used by aces and jokers."""
    defaults, size = style["defaults"], style["special_size"]
    move_sla_object_y(frame, float(style["profile"].get("special_text_y_offset", 0.0)))

    for itext in frame.iter("ITEXT"):
        itext.set("CH", card["misc_text"])
        itext.set("FCOLOR", defaults.get("special_text_color", "Black"))
        itext.set("FSHADE", str(defaults.get("special_text_shade", "70")))
        itext.set("FONTSIZE", size)
        itext.set("FONT", style["special_font"])

    for def_style in frame.iter("DefaultStyle"):
        def_style.set("FONT", style["body_font"])
        def_style.set("FONTSIZE", size)

    for trail in frame.iter("trail"):
        trail.set("FONT", style["body_font"])
        trail.set("FONTSIZE", size)

    for para in frame.iter("para"):
        para.set("FONTSIZE", size)
        para.set("FONT", style["special_font"])


def fill_attack_text(frame, card, style):
    """The card's description, the largest block of text on the card."""
    defaults, size, font = style["defaults"], style["attack_size"], style["body_font"]

    for itext in frame.iter("ITEXT"):
        itext.set("CH", card["attack_text"])
        itext.set("FONTSIZE", size)
        itext.set("FONT", font)
        itext.set("FCOLOR", defaults.get("body_text_color", "Black"))
        itext.set("FSHADE", str(defaults.get("body_text_shade", "100")))

    for def_style in frame.iter("DefaultStyle"):
        def_style.set("FONT", font)

    for trail in frame.iter("trail"):
        trail.set("FONT", font)

    for para in frame.iter("para"):
        para.set("FONT", font)
        para.set("FONTSIZE", size)


def fill_card_number(frame, card, style):
    """The value in the corner: a number, a court letter, or the joker's label."""
    set_sla_text_color(frame, style["number_color"])
    if style["joker"]:
        display_text = card.get("card_kind") or style["joker_label"]
    else:
        display_text = card["value"]
    for itext in frame.iter("ITEXT"):
        itext.set("CH", display_text)


def fill_suit_name(frame, card, style):
    """
    The suit name across the top.

    The style attributes are removed as well as set, because the template's own
    paragraph styles would otherwise override the font chosen for the language.
    """
    font = style["heading_font"]
    set_sla_text_color(frame, style["defaults"].get("suit_name_color", "Pure_White"))

    for itext in frame.iter("ITEXT"):
        itext.set("CH", card["suit_name"])
        itext.set("FONT", font)
        itext.attrib.pop("CSTYLE", None)
        itext.attrib.pop("PSTYLE", None)

    for def_style in frame.iter("DefaultStyle"):
        def_style.set("FONT", font)
        def_style.attrib.pop("PARENT", None)

    for trail in frame.iter("trail"):
        trail.set("FONT", font)
        trail.attrib.pop("PARENT", None)

    for para in frame.iter("para"):
        para.set("FONT", font)
        para.attrib.pop("CSTYLE", None)
        para.attrib.pop("PSTYLE", None)


def fill_url_text(frame, card, _style):
    for itext in frame.iter("ITEXT"):
        itext.set("CH", card["url"])


# Frames carrying text, by their Scribus object name.
TEXT_FRAME_HANDLERS = {
    "special_text": fill_special_text,
    "attack_text": fill_attack_text,
    "card_number": fill_card_number,
    "suit_name": fill_suit_name,
    "url_text": fill_url_text,
}


def generate_card(card, edition, language, size_key, template_path, output_path, config, assets_data, base_dir, log):
    """Inject one card's data into a copy of the master template."""
    style = card_style(card, edition, language, size_key, config, assets_data)
    border_path, back_path, qr_path = card_artwork(
        card, edition, language, size_key, config, assets_data, base_dir, log
    )
    images = {"qr_code": (qr_path, "1"), "card_border": (border_path, "0"), "card_back": (back_path, "0")}

    # parse_xml is defusedxml's parser whenever that package is installed. The
    # file read here is one of this repository's own .sla templates, named by
    # the config rather than supplied by a caller, so it is not untrusted input.
    tree = parse_xml(template_path)  # nosec B314
    root = tree.getroot()

    inject_color_definitions(
        root, config, cc.suit_colors_for_edition(config, edition), log, extra_definitions=style["inline_swatches"]
    )

    placeholder_colors = recolorable_swatches(config)
    elements_to_delete = []

    for parent in root.iter():
        for child in parent:
            if child.tag != "PAGEOBJECT":
                continue

            name = child.get("ANNAME", "").lower().strip()

            if child.get("PTYPE") == "6" and child.get("PCOLOR") in placeholder_colors:
                recolour_suit_band(child, style["suit_color"])

            if name in images:
                fill_image_frame(child, *images[name])
            elif name == "special_text" and not style["special"]:
                # Only cards carrying misc text keep this frame. Being driven by
                # the data means a jokerless edition needs no special case.
                elements_to_delete.append((parent, child))
            elif name in TEXT_FRAME_HANDLERS:
                TEXT_FRAME_HANDLERS[name](child, card, style)

    for parent, child in elements_to_delete:
        parent.remove(child)

    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    return output_path


# --------------------------------------------------------------------------
# PDF export (Scribus only)
# --------------------------------------------------------------------------


def apply_scribus_colours(card, edition, language, config, assets_data, log):
    """
    Reassert the card's colours through the Scribus API.

    They are already written into the .sla, so this is belt and braces and a
    failure here is not fatal. Each call is guarded on its own: they were once
    nested in a single try block, and because the suit band is not named
    consistently across the two master templates, a failure on the first
    silently skipped the card number colour on every tarot card.
    """
    defaults = config.get("defaults", {}) or {}
    suit_color, number_color, _inline = cc.card_colors(config, assets_data, edition, card, language)

    def try_set(action, label, warn=False):
        """Apply one Scribus setting; report whether it succeeded."""
        try:
            action()
            return True
        except Exception as exc:
            if warn:
                log.warn("{0} failed for {1}: {2}".format(label, card["card_id"], exc))
            return False

    try_set(lambda: scribus.setTextColor(number_color, "card_number"), "Card number colour", warn=True)
    try_set(
        lambda: scribus.setTextColor(defaults.get("suit_name_color", "Pure_White"), "suit_name"), "Suit name colour"
    )
    try_set(lambda: scribus.setFillColor("None", "qr_code_frame"), "QR frame fill")

    # The suit band sits beneath the full-bleed artwork, which is opaque, so
    # this is cosmetic only, and its object name varies between the two master
    # templates. Whichever name exists is the one that gets filled.
    def fill_band(name):
        scribus.setFillColor(suit_color, name)
        scribus.setFillShade(100, name)
        scribus.setFillTransparency(0, name)

    for band in ("Polygon1", "Polygon2"):
        if try_set(lambda: fill_band(band), "Suit band fill"):
            break


def back_frame_name():
    """Move to the card back and name its frame."""
    scribus.gotoPage(2)
    return "card_back"


def place_artwork_frame(frame, width, height, offset):
    """
    Size an artwork frame to the full bleed area and pin it to the page.

    The frame is larger than the trimmed card and sits at a negative offset, so
    the artwork runs past every edge and nothing white shows after cutting.
    """
    scribus.sizeObject(width, height, frame)
    scribus.moveObjectAbs(offset, offset, frame)
    scribus.setScaleImageToFrame(True, False, frame)
    scribus.setFillColor("None", frame)
    scribus.setLineColor("None", frame)


def write_pdf(export_profile, card, edition, language, size_key, config, out_dir, log):
    """Export the open document once, for one bleed and printer's marks setting."""
    output_cfg = config.get("output", {}) or {}
    bleed = float(export_profile.get("bleed_mm", 0.0))
    marks = bool(export_profile.get("printers_marks", False))

    pdf = scribus.PDFfile()
    pdf.resolution = output_cfg.get("resolution_dpi", 300)
    pdf.version = output_cfg.get("pdf_version", 14)
    pdf.file = os.path.join(
        out_dir, cc.card_pdf_name(config, edition, card["card_id"], size_key, language, bleed, marks)
    )
    pdf.useDocBleeds = False

    # Output destination decides the colour space: 1 = printer (CMYK), 0 =
    # screen (RGB). CMYK preserves the values defined in assets.yaml instead of
    # converting them on export.
    mode = str(output_cfg.get("color_mode", "cmyk")).strip().lower()
    if mode not in ("cmyk", "rgb"):
        log.warn("Unknown color_mode '{0}'; using cmyk".format(mode))
        mode = "cmyk"
    pdf.outdst = 1 if mode == "cmyk" else 0

    icc = str(output_cfg.get("icc_profile", "") or "").strip()
    if icc:
        try:
            pdf.profiles = 1
            pdf.solidpr = icc
            pdf.imagepr = icc
            pdf.printprofc = icc
        except Exception as exc:
            log.warn("ICC profile '{0}' unavailable ({1}); exporting without it".format(icc, exc))
            pdf.profiles = 0

    pdf.bleedt = bleed
    pdf.bleedb = bleed
    pdf.bleedl = bleed
    pdf.bleedr = bleed
    pdf.cropMarks = marks
    pdf.bleedMarks = marks
    pdf.registrationMarks = marks
    pdf.colorMarks = marks
    pdf.save()

    return {"path": pdf.file, "bleed": cc.format_bleed(bleed), "marks": marks}


def export_pdfs(sla_filepath, card, edition, language, size_key, config, assets_data, base_dir, out_dir, profiles, log):
    if not SCRIBUS_AVAILABLE:
        return []

    profile = (config.get("size_profiles", {}) or {}).get(size_key, {}) or {}

    width = float(profile.get("width_mm", 68.0))
    height = float(profile.get("height_mm", 99.0))
    offset = float(profile.get("artwork_offset_mm", -6.0))

    try:
        scribus.openDoc(sla_filepath)
        scribus.gotoPage(1)

        border_frame = "card_border"
        bg_path, found = cc.resolve_background(config, assets_data, base_dir, edition, card, size_key, language)

        if found:
            try:
                scribus.loadImage(bg_path, border_frame)
            except Exception as exc:
                log.warn("loadImage failed for {0}: {1}".format(card["card_id"], exc))
        else:
            log.warn("Artwork not found for {0}: {1}".format(card["card_id"], bg_path))

        place_artwork_frame(border_frame, width, height, offset)

        apply_scribus_colours(card, edition, language, config, assets_data, log)

        place_artwork_frame(back_frame_name(), width, height, offset)

        exported = []
        for export_profile in profiles:
            exported.append(write_pdf(export_profile, card, edition, language, size_key, config, out_dir, log))

        scribus.closeDoc()
        return exported

    except Exception as exc:
        log.warn("Export crashed on {0}: {1}".format(card["card_id"], exc))
        try:
            scribus.closeDoc()
        except Exception as close_exc:
            # Already handling a failure; a document that will not close is
            # noted rather than allowed to mask the original error.
            log.warn("Could not close document after that failure: {0}".format(close_exc))
        return []


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------


def parse_args():
    parser = argparse.ArgumentParser(description="Generate OWASP Cornucopia card templates and PDFs.")
    parser.add_argument("--config", default="pdf_config.yaml", help="Config file to drive the build")
    parser.add_argument("--edition", action="append", help="Edition to build (repeatable). Overrides config.")
    parser.add_argument("--language", action="append", help="Language to build (repeatable). Overrides config.")
    parser.add_argument("--size", action="append", help="Size profile to build (repeatable). Overrides config.")
    parser.add_argument(
        "--cards",
        help="Only build these card IDs, comma separated "
        "(e.g. VEA,VEJ,JOA). Useful for spot checks "
        "and for regenerating a single card.",
    )
    parser.add_argument("--profile", help="Export profile name to use")
    parser.add_argument("--output-dir", help="Override the configured output directory")
    parser.add_argument("--dry-run", action="store_true", help="Report the build matrix and asset problems, then exit")
    parser.add_argument("--skip-existing", action="store_true", help="Skip cards whose PDFs are already on disk")
    # Scribus injects its own arguments, so ignore anything we do not recognise.
    args, _unknown = parser.parse_known_args()
    return args


def select_deck(target, args, config, base_dir, log):
    """
    Read and order one target's cards, narrowed by --cards if given.

    Returns None when there is nothing to build, having said why.
    """
    edition, language, size_key = target["edition"], target["language"], target["size"]
    profile = (config.get("size_profiles", {}) or {}).get(size_key, {}) or {}
    template_path = os.path.join(base_dir, profile.get("template", ""))

    if not os.path.exists(template_path):
        log.warn("Template missing for size '{0}': {1}".format(size_key, template_path))
        return None

    data_path = cc.card_data_path(config, base_dir, edition, language)
    cards, suit_order = cc.parse_cards(data_path)
    if not cards:
        log.warn("No cards found at {0}".format(data_path))
        return None

    deck = cc.sort_deck(cards, config, edition, suit_order, language)

    if args.cards:
        wanted = {c.strip().upper() for c in args.cards.split(",") if c.strip()}
        deck = [c for c in deck if str(c["card_id"]).upper() in wanted]
        if not deck:
            log.warn("None of the requested cards exist in {0}/{1}".format(edition, language))
            return None

    return deck, suit_order, template_path


def report_missing_artwork(deck, target, config, assets_data, base_dir, log):
    """Check every image a target needs, without building anything."""
    edition, language, size_key = target["edition"], target["language"], target["size"]

    missing = [
        card["card_id"]
        for card in deck
        if not cc.resolve_background(config, assets_data, base_dir, edition, card, size_key, language)[1]
    ]

    back_path, back_found = cc.resolve_card_back(config, base_dir, edition, size_key)
    if not back_found:
        log.warn("  card back missing: {0}".format(back_path))
    if missing:
        log.warn("  artwork missing for {0} card(s): {1}".format(len(missing), ", ".join(missing[:10])))
    else:
        log.info("  all artwork resolved")


def already_exported(card, target, config, out_dir, profiles):
    """True when every PDF this card would produce is already on disk."""
    edition, language, size_key = target["edition"], target["language"], target["size"]
    expected = [
        os.path.join(
            out_dir,
            cc.card_pdf_name(
                config,
                edition,
                card["card_id"],
                size_key,
                language,
                p.get("bleed_mm", 0.0),
                p.get("printers_marks", False),
            ),
        )
        for p in profiles
    ]
    return all(os.path.exists(path) for path in expected)


def build_target(target, args, config, assets_data, base_dir, out_dir, profiles, log):
    """
    Build one edition, language and card size.

    Returns a record of what was produced, or None if there was nothing to do.
    """
    edition, language, size_key = target["edition"], target["language"], target["size"]
    log.info("\n--- {0} | {1} | {2} ---".format(edition, language.upper(), size_key))

    selected = select_deck(target, args, config, base_dir, log)
    if not selected:
        return None
    deck, suit_order, template_path = selected

    jokers = sum(1 for c in deck if cc.is_joker(c, config, edition))
    log.info("  {0} cards, {1} suit(s), {2} joker(s)".format(len(deck), len(suit_order), jokers))

    unmapped = sorted({c["suit_id"] for c in deck if not cc.has_suit_color(config, assets_data, edition, c["suit_id"])})
    if unmapped:
        log.warn(
            "No suit colour mapped for {0} in '{1}'; using {2}".format(
                ", ".join(unmapped), edition, (config.get("defaults", {}) or {}).get("suit_color", "Data_Color")
            )
        )

    record = {
        "edition": edition,
        "language": language,
        "size": size_key,
        "cards": len(deck),
        "jokers": jokers,
        "pdfs": 0,
    }

    if args.dry_run:
        report_missing_artwork(deck, target, config, assets_data, base_dir, log)
        return record

    for card in deck:
        if args.skip_existing and SCRIBUS_AVAILABLE and already_exported(card, target, config, out_dir, profiles):
            continue

        sla_path = os.path.join(out_dir, cc.sla_name(config, edition, card["card_id"], size_key, language))
        generate_card(card, edition, language, size_key, template_path, sla_path, config, assets_data, base_dir, log)
        record["pdfs"] += len(
            export_pdfs(
                sla_path, card, edition, language, size_key, config, assets_data, base_dir, out_dir, profiles, log
            )
        )

    log.info("  generated {0} card file(s), {1} PDF(s)".format(len(deck), record["pdfs"]))
    return record


def main():
    args = parse_args()
    base_dir = SCRIPT_DIR

    config = cc.load_config(base_dir, args.config)
    if not config:
        print("ERROR: could not load {0}".format(args.config))
        return 1

    assets_data = cc.load_assets(config, base_dir)
    paths = config.get("paths", {}) or {}

    out_dir = args.output_dir or cc.output_dir(config, base_dir)
    log = BuildLog(os.path.join(base_dir, paths.get("log_file", "build_log.txt")))

    targets, warnings = cc.resolve_targets(config, base_dir, args.edition, args.language, args.size)
    for warning in warnings:
        log.warn(warning)

    if not targets:
        log.info("Nothing to build. Check generation_targets in your config.")
        return 1

    try:
        profiles = cc.get_export_profiles(config, profile_name=args.profile)
    except ValueError as exc:
        log.info("ERROR: {0}".format(exc))
        return 1

    editions = sorted({t["edition"] for t in targets})
    log.info("Building {0} target(s) across edition(s): {1}".format(len(targets), ", ".join(editions)))
    log.info(
        "Scribus {0} — PDF export {1}".format(
            "detected" if SCRIBUS_AVAILABLE else "not detected",
            "enabled" if SCRIBUS_AVAILABLE else "disabled (.sla only)",
        )
    )

    if not args.dry_run:
        os.makedirs(out_dir, exist_ok=True)
        os.makedirs(cc.qr_dir(config, base_dir), exist_ok=True)

    manifest = {"targets": [], "warnings": [], "total_cards": 0, "total_pdfs": 0}

    for target in targets:
        record = build_target(target, args, config, assets_data, base_dir, out_dir, profiles, log)
        if record:
            manifest["targets"].append(record)
            manifest["total_cards"] += record["cards"]
            manifest["total_pdfs"] += record["pdfs"]

    manifest["warnings"] = log.warnings
    manifest_path = os.path.join(base_dir, paths.get("manifest_file", "build_manifest.json"))
    with open(manifest_path, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    log.info(
        "\nDone. {0} card file(s), {1} PDF(s), {2} warning(s).".format(
            manifest["total_cards"], manifest["total_pdfs"], len(log.warnings)
        )
    )
    log.info("Manifest: {0}".format(manifest_path))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception:
        details = traceback.format_exc()
        print(details)
        with open(os.path.join(SCRIPT_DIR, "build_log.txt"), "a", encoding="utf-8") as handle:
            handle.write("\nFATAL:\n{0}\n".format(details))
        raise
