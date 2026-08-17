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
import xml.etree.ElementTree as ET

# Make sibling modules importable when Scribus executes this by absolute path.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

try:
    import cornucopia_common as cc
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
            exc, sys.prefix, sys.version.split()[0],
            os.environ.get('PYTHONPATH') or '(not set)'))
    raise

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
        with open(self.path, 'w', encoding='utf-8') as handle:
            handle.write("=== OWASP Cornucopia build log ===\n")

    def write(self, message):
        with open(self.path, 'a', encoding='utf-8') as handle:
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
    for default_style in page_object.iter('DefaultStyle'):
        default_style.set('FCOLOR', color_name)
    for itext in page_object.iter('ITEXT'):
        itext.set('FCOLOR', color_name)


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
    document = root.find('DOCUMENT')
    if document is None:
        document = root

    existing = {color.get('NAME') for color in root.iter('COLOR')}
    definitions = dict(config.get('color_definitions', {}) or {})
    definitions.update(extra_definitions or {})
    added = []

    for name in list(needed_names) + sorted(extra_definitions or {}):
        if not name or name in existing:
            continue
        spec = definitions.get(name)
        if not spec:
            log.warn("Swatch '{0}' is referenced but has no entry in "
                     "color_definitions; Scribus will fall back.".format(name))
            continue
        element = ET.Element('COLOR')
        element.set('NAME', name)
        element.set('SPACE', 'CMYK')
        for axis in ('c', 'm', 'y', 'k'):
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
    qr_cfg = config.get('qr', {}) or {}
    qr = qrcode.QRCode(
        version=qr_cfg.get('version', 1),
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=qr_cfg.get('box_size', 10),
        border=qr_cfg.get('border', 0),
    )
    qr.add_data(url)
    qr.make(fit=True)

    try:
        from qrcode.image.pure import PyPNGImage
    except ImportError:
        raise ImportError(
            "Cannot render QR codes: 'pypng' is not installed in the "
            "interpreter running this script. See README.md.")

    qr.make_image(image_factory=PyPNGImage).save(output_path)


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
    for edition in (config.get('editions', {}) or {}):
        names.update((cc.edition_config(config, edition).get('suit_colors') or {}).values())
    fallback = (config.get('defaults', {}) or {}).get('suit_color')
    if fallback:
        names.add(fallback)
    return {n for n in names if n}


def generate_card(card, edition, language, size_key, template_path, output_path,
                  config, assets_data, base_dir, log):
    """Inject one card's data into a copy of the master template."""
    profile = (config.get('size_profiles', {}) or {}).get(size_key, {}) or {}
    defaults = config.get('defaults', {}) or {}

    suit_color, number_color, inline_swatches = cc.card_colors(
        config, assets_data, edition, card, language)
    body_font = cc.get_font(config, language, 'body')
    heading_font = cc.get_font(config, language, 'heading')
    accent_font = cc.get_font(config, language, 'accent')

    joker = cc.is_joker(card, config, edition)
    special = cc.has_special_text(card)

    special_frame = 'special_text_joker' if joker else 'special_text'
    special_size = str(cc.get_font_size(config, size_key, special_frame, language))
    special_font = accent_font if joker else body_font
    attack_size = str(cc.get_font_size(config, size_key, 'attack_text', language))

    tree = ET.parse(template_path)
    root = tree.getroot()
    elements_to_delete = []

    inject_color_definitions(
        root, config, cc.suit_colors_for_edition(config, edition), log,
        extra_definitions=inline_swatches)

    qr_path = "{0}/{1}.png".format(
        cc.qr_dir(config, base_dir).replace('\\', '/'), card['card_id'])

    back_path, back_found = cc.resolve_card_back(config, base_dir, edition, size_key)
    border_path, border_found = cc.resolve_background(
        config, assets_data, base_dir, edition, card, size_key, language)

    if not back_found:
        log.warn("Card back missing for {0}/{1}: {2}".format(edition, size_key, back_path))
    if not border_found:
        log.warn("Artwork missing for card {0} ({1}/{2}): {3}".format(
            card['card_id'], edition, size_key, border_path))

    if card['url'] and QR_AVAILABLE:
        create_qr_image(card['url'], qr_path, config)

    placeholder_colors = recolorable_swatches(config)

    for parent in root.iter():
        for child in parent:
            if child.tag != 'PAGEOBJECT':
                continue

            frame_name = child.get('ANNAME', '').lower().strip()

            if child.get('PTYPE') == '6' and child.get('PCOLOR') in placeholder_colors:
                child.set('PCOLOR', suit_color)
                child.set('SHADE', '100')
                child.set('TransValue', '0')
                child.set('TransValueS', '0')
                child.attrib.pop('TransBlend', None)
                child.attrib.pop('TransBlendS', None)

            if frame_name == 'qr_code':
                child.set('PFILE', qr_path)
                child.set('ScaleType', '1')
                child.set('AspectRatio', '1')

            elif frame_name == 'card_border':
                child.set('PFILE', border_path)
                child.set('ScaleType', '1')
                child.set('AspectRatio', '0')

            elif frame_name == 'card_back':
                child.set('PFILE', back_path)
                child.set('ScaleType', '1')
                child.set('AspectRatio', '0')

            elif frame_name == 'special_text':
                # Rendered only when the card actually carries misc text. This
                # is data-driven, so jokerless editions need no special case.
                if not special:
                    elements_to_delete.append((parent, child))
                else:
                    move_sla_object_y(child, float(profile.get('special_text_y_offset', 0.0)))
                    for itext in child.iter('ITEXT'):
                        itext.set('CH', card['misc_text'])
                        itext.set('FCOLOR', defaults.get('special_text_color', 'Black'))
                        itext.set('FSHADE', str(defaults.get('special_text_shade', '70')))
                        itext.set('FONTSIZE', special_size)
                        itext.set('FONT', special_font)

                    for def_style in child.iter('DefaultStyle'):
                        def_style.set('FONT', body_font)
                        def_style.set('FONTSIZE', special_size)

                    for trail in child.iter('trail'):
                        trail.set('FONT', body_font)
                        trail.set('FONTSIZE', special_size)

                    for para in child.iter('para'):
                        para.set('FONTSIZE', special_size)
                        para.set('FONT', special_font)

            elif frame_name == 'attack_text':
                for itext in child.iter('ITEXT'):
                    itext.set('CH', card['attack_text'])
                    itext.set('FONTSIZE', attack_size)
                    itext.set('FONT', body_font)
                    itext.set('FCOLOR', defaults.get('body_text_color', 'Black'))
                    itext.set('FSHADE', str(defaults.get('body_text_shade', '100')))

                for def_style in child.iter('DefaultStyle'):
                    def_style.set('FONT', body_font)

                for trail in child.iter('trail'):
                    trail.set('FONT', body_font)

                for para in child.iter('para'):
                    para.set('FONT', body_font)
                    para.set('FONTSIZE', attack_size)

            elif frame_name == 'card_number':
                set_sla_text_color(child, number_color)
                for itext in child.iter('ITEXT'):
                    if joker:
                        display_text = (card.get('card_kind')
                                        or (config.get('card_semantics', {}) or {})
                                        .get('joker_label', 'Joker'))
                    else:
                        display_text = card['value']
                    itext.set('CH', display_text)

            elif frame_name == 'suit_name':
                set_sla_text_color(child, defaults.get('suit_name_color', 'Pure_White'))
                for itext in child.iter('ITEXT'):
                    itext.set('CH', card['suit_name'])
                    itext.set('FONT', heading_font)
                    if 'CSTYLE' in itext.attrib:
                        del itext.attrib['CSTYLE']
                    if 'PSTYLE' in itext.attrib:
                        del itext.attrib['PSTYLE']

                for def_style in child.iter('DefaultStyle'):
                    def_style.set('FONT', heading_font)
                    if 'PARENT' in def_style.attrib:
                        del def_style.attrib['PARENT']

                for trail in child.iter('trail'):
                    trail.set('FONT', heading_font)
                    if 'PARENT' in trail.attrib:
                        del trail.attrib['PARENT']

                for para in child.iter('para'):
                    para.set('FONT', heading_font)
                    if 'CSTYLE' in para.attrib:
                        del para.attrib['CSTYLE']
                    if 'PSTYLE' in para.attrib:
                        del para.attrib['PSTYLE']

            elif frame_name == 'url_text':
                for itext in child.iter('ITEXT'):
                    itext.set('CH', card['url'])

    for parent, child in elements_to_delete:
        parent.remove(child)

    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    return output_path


# --------------------------------------------------------------------------
# PDF export (Scribus only)
# --------------------------------------------------------------------------

def export_pdfs(sla_filepath, card, edition, language, size_key, config,
                assets_data, base_dir, out_dir, profiles, log):
    if not SCRIBUS_AVAILABLE:
        return []

    profile = (config.get('size_profiles', {}) or {}).get(size_key, {}) or {}
    output_cfg = config.get('output', {}) or {}
    defaults = config.get('defaults', {}) or {}

    width = float(profile.get('width_mm', 68.0))
    height = float(profile.get('height_mm', 99.0))
    offset = float(profile.get('artwork_offset_mm', -6.0))

    try:
        scribus.openDoc(sla_filepath)
        scribus.gotoPage(1)

        border_frame = "card_border"
        bg_path, found = cc.resolve_background(
            config, assets_data, base_dir, edition, card, size_key, language)

        if found:
            try:
                scribus.loadImage(bg_path, border_frame)
            except Exception as exc:
                log.warn("loadImage failed for {0}: {1}".format(card['card_id'], exc))
        else:
            log.warn("Artwork not found for {0}: {1}".format(card['card_id'], bg_path))

        scribus.sizeObject(width, height, border_frame)
        scribus.moveObjectAbs(offset, offset, border_frame)
        scribus.setScaleImageToFrame(True, False, border_frame)
        scribus.setFillColor("None", border_frame)
        scribus.setLineColor("None", border_frame)

        suit_color, number_color, _inline = cc.card_colors(
            config, assets_data, edition, card, language)
        # Each of these is guarded independently. They were previously nested in
        # one try block, so a failure on the first silently skipped the rest --
        # and the suit band is not named consistently across the two masters,
        # which meant the card number colour was never applied on tarot.
        # The colours are already written into the .sla, so these calls only
        # reassert them; a failure here is not fatal.
        def try_set(action, label, warn=False):
            try:
                action()
            except Exception as exc:
                if warn:
                    log.warn("{0} failed for {1}: {2}".format(label, card['card_id'], exc))

        try_set(lambda: scribus.setTextColor(number_color, "card_number"),
                "Card number colour", warn=True)
        try_set(lambda: scribus.setTextColor(
            defaults.get('suit_name_color', 'Pure_White'), "suit_name"), "Suit name colour")
        try_set(lambda: scribus.setFillColor("None", "qr_code_frame"), "QR frame fill")

        # The suit band sits beneath the full-bleed artwork, which is opaque, so
        # this is cosmetic only and its object name varies between masters.
        for band in ("Polygon1", "Polygon2"):
            try:
                scribus.setFillColor(suit_color, band)
                scribus.setFillShade(100, band)
                scribus.setFillTransparency(0, band)
                break
            except Exception:
                continue

        scribus.gotoPage(2)
        back_frame = "card_back"
        scribus.sizeObject(width, height, back_frame)
        scribus.moveObjectAbs(offset, offset, back_frame)
        scribus.setScaleImageToFrame(True, False, back_frame)
        scribus.setFillColor("None", back_frame)
        scribus.setLineColor("None", back_frame)

        exported = []
        for export_profile in profiles:
            bleed = float(export_profile.get('bleed_mm', 0.0))
            marks = bool(export_profile.get('printers_marks', False))

            pdf_filename = cc.card_pdf_name(
                config, edition, card['card_id'], size_key, language, bleed, marks)

            pdf = scribus.PDFfile()
            pdf.resolution = output_cfg.get('resolution_dpi', 300)
            pdf.version = output_cfg.get('pdf_version', 14)
            pdf.file = os.path.join(out_dir, pdf_filename)
            pdf.useDocBleeds = False

            # Output destination decides the colour space: 1 = printer (CMYK),
            # 0 = screen (RGB). CMYK preserves the values defined in
            # assets.yaml instead of converting them on export.
            mode = str(output_cfg.get('color_mode', 'cmyk')).strip().lower()
            if mode not in ('cmyk', 'rgb'):
                log.warn("Unknown color_mode '{0}'; using cmyk".format(mode))
                mode = 'cmyk'
            pdf.outdst = 1 if mode == 'cmyk' else 0

            icc = str(output_cfg.get('icc_profile', '') or '').strip()
            if icc:
                try:
                    pdf.profiles = 1
                    pdf.solidpr = icc
                    pdf.imagepr = icc
                    pdf.printprofc = icc
                except Exception as exc:
                    log.warn("ICC profile '{0}' unavailable ({1}); "
                             "exporting without it".format(icc, exc))
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

            exported.append({'path': pdf.file, 'bleed': cc.format_bleed(bleed), 'marks': marks})

        scribus.closeDoc()
        return exported

    except Exception as exc:
        log.warn("Export crashed on {0}: {1}".format(card['card_id'], exc))
        try:
            scribus.closeDoc()
        except Exception:
            pass
        return []


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate OWASP Cornucopia card templates and PDFs.")
    parser.add_argument("--config", default="pdf_config.yaml",
                        help="Config file to drive the build")
    parser.add_argument("--edition", action="append",
                        help="Edition to build (repeatable). Overrides config.")
    parser.add_argument("--language", action="append",
                        help="Language to build (repeatable). Overrides config.")
    parser.add_argument("--size", action="append",
                        help="Size profile to build (repeatable). Overrides config.")
    parser.add_argument("--cards", help="Only build these card IDs, comma separated "
                                        "(e.g. VEA,VEJ,JOA). Useful for spot checks "
                                        "and for regenerating a single card.")
    parser.add_argument("--profile", help="Export profile name to use")
    parser.add_argument("--output-dir", help="Override the configured output directory")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report the build matrix and asset problems, then exit")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Skip cards whose PDFs are already on disk")
    # Scribus injects its own arguments, so ignore anything we do not recognise.
    args, _unknown = parser.parse_known_args()
    return args


def main():
    args = parse_args()
    base_dir = SCRIPT_DIR

    config = cc.load_config(base_dir, args.config)
    if not config:
        print("ERROR: could not load {0}".format(args.config))
        return 1

    assets_data = cc.load_assets(config, base_dir)
    paths = config.get('paths', {}) or {}

    out_dir = args.output_dir or cc.output_dir(config, base_dir)
    log = BuildLog(os.path.join(base_dir, paths.get('log_file', 'build_log.txt')))

    targets, warnings = cc.resolve_targets(
        config, base_dir, args.edition, args.language, args.size)
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

    editions = sorted({t['edition'] for t in targets})
    log.info("Building {0} target(s) across edition(s): {1}".format(
        len(targets), ', '.join(editions)))
    log.info("Scribus {0} — PDF export {1}".format(
        "detected" if SCRIBUS_AVAILABLE else "not detected",
        "enabled" if SCRIBUS_AVAILABLE else "disabled (.sla only)"))

    if not args.dry_run:
        os.makedirs(out_dir, exist_ok=True)
        os.makedirs(cc.qr_dir(config, base_dir), exist_ok=True)

    manifest = {'targets': [], 'warnings': [], 'total_cards': 0, 'total_pdfs': 0}

    for target in targets:
        edition, language, size_key = target['edition'], target['language'], target['size']
        profile = (config.get('size_profiles', {}) or {}).get(size_key, {}) or {}
        template_path = os.path.join(base_dir, profile.get('template', ''))

        log.info("\n--- {0} | {1} | {2} ---".format(edition, language.upper(), size_key))

        if not os.path.exists(template_path):
            log.warn("Template missing for size '{0}': {1}".format(size_key, template_path))
            continue

        data_path = cc.card_data_path(config, base_dir, edition, language)
        cards, suit_order = cc.parse_cards(data_path)
        if not cards:
            log.warn("No cards found at {0}".format(data_path))
            continue

        deck = cc.sort_deck(cards, config, edition, suit_order, language)

        if args.cards:
            wanted = {c.strip().upper() for c in args.cards.split(',') if c.strip()}
            deck = [c for c in deck if str(c['card_id']).upper() in wanted]
            if not deck:
                log.warn("None of the requested cards exist in {0}/{1}".format(edition, language))
                continue

        jokers = sum(1 for c in deck if cc.is_joker(c, config, edition))
        log.info("  {0} cards, {1} suit(s), {2} joker(s)".format(
            len(deck), len(suit_order), jokers))

        unmapped = sorted({c['suit_id'] for c in deck
                           if not cc.has_suit_color(config, assets_data, edition, c['suit_id'])})
        if unmapped:
            log.warn("No suit colour mapped for {0} in '{1}'; using {2}".format(
                ', '.join(unmapped), edition,
                (config.get('defaults', {}) or {}).get('suit_color', 'Data_Color')))

        target_record = {'edition': edition, 'language': language, 'size': size_key,
                         'cards': len(deck), 'jokers': jokers, 'pdfs': 0}

        if args.dry_run:
            missing = []
            for card in deck:
                _path, found = cc.resolve_background(
                    config, assets_data, base_dir, edition, card, size_key, language)
                if not found:
                    missing.append(card['card_id'])
            back_path, back_found = cc.resolve_card_back(config, base_dir, edition, size_key)
            if not back_found:
                log.warn("  card back missing: {0}".format(back_path))
            if missing:
                log.warn("  artwork missing for {0} card(s): {1}".format(
                    len(missing), ', '.join(missing[:10])))
            else:
                log.info("  all artwork resolved")
            manifest['targets'].append(target_record)
            manifest['total_cards'] += len(deck)
            continue

        for card in deck:
            sla_filename = cc.sla_name(config, edition, card['card_id'], size_key, language)
            sla_path = os.path.join(out_dir, sla_filename)

            if args.skip_existing and SCRIBUS_AVAILABLE:
                expected = [os.path.join(out_dir, cc.card_pdf_name(
                    config, edition, card['card_id'], size_key, language,
                    p.get('bleed_mm', 0.0), p.get('printers_marks', False)))
                    for p in profiles]
                if all(os.path.exists(p) for p in expected):
                    continue

            generate_card(card, edition, language, size_key, template_path, sla_path,
                          config, assets_data, base_dir, log)

            exported = export_pdfs(sla_path, card, edition, language, size_key, config,
                                   assets_data, base_dir, out_dir, profiles, log)
            target_record['pdfs'] += len(exported)
            manifest['total_pdfs'] += len(exported)

        log.info("  generated {0} card file(s), {1} PDF(s)".format(
            len(deck), target_record['pdfs']))
        manifest['targets'].append(target_record)
        manifest['total_cards'] += len(deck)

    manifest['warnings'] = log.warnings
    manifest_path = os.path.join(base_dir, paths.get('manifest_file', 'build_manifest.json'))
    with open(manifest_path, 'w', encoding='utf-8') as handle:
        json.dump(manifest, handle, indent=2)

    log.info("\nDone. {0} card file(s), {1} PDF(s), {2} warning(s).".format(
        manifest['total_cards'], manifest['total_pdfs'], len(log.warnings)))
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
        with open(os.path.join(SCRIPT_DIR, 'build_log.txt'), 'a', encoding='utf-8') as handle:
            handle.write("\nFATAL:\n{0}\n".format(details))
        raise
