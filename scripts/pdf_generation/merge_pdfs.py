"""
OWASP Cornucopia — deck merger and packager.

Stitches the per-card PDFs produced by generate_deck.py into full decks, in
factory order, with each card's back page ahead of its front page ready for
duplex printing. Optionally packages the finished decks into ZIP archives.

Runs in a normal system Python (needs PyMuPDF); it does not require Scribus.

  python merge_pdfs.py                          # merge everything discoverable
  python merge_pdfs.py --edition websiteapp     # one edition
  python merge_pdfs.py --language en --zip      # one language, and package it
  python merge_pdfs.py --bleed-mm 6             # pick a different export profile
"""

import argparse
import json
import os
import sys
import zipfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import cornucopia_common as cc  # noqa: E402  (needs the sys.path line above)

try:
    import pymupdf
except ImportError:
    try:
        import fitz as pymupdf  # older releases only expose the legacy name
    except ImportError:
        # Only merge_deck actually reads or writes PDFs. Everything else here
        # works on filenames, so the module stays importable without PyMuPDF
        # and --dry-run still reports what a merge would produce. Anything
        # that needs it says so plainly rather than failing on the import.
        pymupdf = None

PYMUPDF_HELP = (
    "ERROR: merging decks needs PyMuPDF, which is not installed in this "
    "interpreter.\n"
    "  {0}\n"
    "Install it with 'python3 -m pip install pymupdf', then run this again.\n"
    "Use --dry-run to see what would be merged without it."
)


def parse_args():
    parser = argparse.ArgumentParser(description="Merge generated card PDFs into full decks, and optionally zip them.")
    parser.add_argument("--config", default="pdf_config.yaml", help="Config file to drive the merge")
    parser.add_argument("--edition", action="append", help="Edition to merge (repeatable). Overrides config.")
    parser.add_argument("--language", action="append", help="Language to merge (repeatable). Overrides config.")
    parser.add_argument("--size", action="append", help="Size profile to merge (repeatable). Overrides config.")
    parser.add_argument("--profile", help="Export profile name from the config")
    parser.add_argument("--bleed-mm", type=float, help="Bleed value to merge, e.g. 0, 3 or 6")
    parser.add_argument(
        "--printers-marks",
        dest="printers_marks",
        action="store_true",
        default=None,
        help="Merge the printers-marks PDFs",
    )
    parser.add_argument(
        "--no-printers-marks", dest="printers_marks", action="store_false", help="Merge the no-printers-marks PDFs"
    )
    parser.add_argument("--output-dir", help="Override the configured output directory")
    parser.add_argument(
        "--zip", dest="do_zip", action="store_true", default=None, help="Package the merged decks into ZIP archives"
    )
    parser.add_argument(
        "--no-zip", dest="do_zip", action="store_false", help="Skip packaging even if the config enables it"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete the per-card PDFs, .sla files and QR codes once the "
        "decks have been written. Only the finished decks are kept.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Report what would be merged, then exit")
    return parser.parse_args()


def files_with_suffix(directory, suffix):
    """Every file directly in a directory with the given extension."""
    if not os.path.isdir(directory):
        return []
    return [os.path.join(directory, name) for name in os.listdir(directory) if name.lower().endswith(suffix)]


def clean_intermediates(consumed_pdfs, config, base_dir, out_dir):
    """
    Remove the working files left behind once the decks exist.

    A build produces one PDF and one .sla per card, plus a QR image per card
    ID. For a full run that is thousands of files and a couple of gigabytes,
    none of which is needed after merging. Only files this run actually
    consumed are removed, and the merged decks are never touched.

    Returns ``(files_removed, bytes_freed)``.
    """
    removed, freed = 0, 0

    def drop(path):
        nonlocal removed, freed
        if not path or not os.path.isfile(path):
            return
        try:
            size = os.path.getsize(path)
            os.remove(path)
            removed += 1
            freed += size
        except OSError as exc:
            print("    could not remove {0}: {1}".format(os.path.basename(path), exc))

    for pdf_path in sorted(set(consumed_pdfs)):
        drop(pdf_path)

    # The .sla files sit alongside the card PDFs and are named independently,
    # so they are matched by extension within the output directory.
    for path in files_with_suffix(out_dir, ".sla"):
        drop(path)

    qr_directory = cc.qr_dir(config, base_dir)
    for path in files_with_suffix(qr_directory, ".png"):
        drop(path)
    try:
        os.rmdir(qr_directory)
    except OSError:
        # Not empty, or not there. Either way, leaving it is harmless.
        pass

    return removed, freed


def match_card_pdfs(deck, edition, language, size_key, config, out_dir, bleed, marks):
    """
    Find the exported PDF for each card, in print order.

    The filename is rebuilt with the same helper the generator used, so the two
    cannot drift apart. Returns the paths found and the card IDs that were not.
    """
    found, missing = [], []
    for card in deck:
        path = os.path.join(
            out_dir, cc.card_pdf_name(config, edition, card["card_id"], size_key, language, bleed, marks)
        )
        if os.path.exists(path):
            found.append(path)
        else:
            missing.append(card["card_id"])
    return found, missing


def merge_deck(ordered_pdfs, output_path):
    """Interleave each card as back-then-front into a single deck PDF."""
    if pymupdf is None:
        raise RuntimeError(PYMUPDF_HELP.format(sys.prefix))
    merged = pymupdf.open()
    for pdf_path in ordered_pdfs:
        card = pymupdf.open(pdf_path)
        if len(card) >= 2:
            merged.insert_pdf(card, from_page=1, to_page=1)
            merged.insert_pdf(card, from_page=0, to_page=0)
        else:
            merged.insert_pdf(card, from_page=0, to_page=0)
        card.close()
    merged.save(output_path, garbage=4, deflate=True)
    page_count = len(merged)
    merged.close()
    return page_count


def package_decks(merged_by_edition, packaging, config, out_dir):
    """Zip the finished decks, either one archive per edition or one overall."""
    if packaging.get("zip_scope", "per_edition") == "single":
        everything = [path for paths in merged_by_edition.values() for path in paths]
        groups = {sorted(merged_by_edition)[0]: everything}
    else:
        groups = merged_by_edition

    for edition, paths in groups.items():
        archive = os.path.join(out_dir, cc.zip_name(config, edition))
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
            for path in paths:
                bundle.write(path, os.path.basename(path))
        size_mb = os.path.getsize(archive) / (1024.0 * 1024.0)
        print("Packaged {0} deck(s) into {1} ({2:.1f} MB)".format(len(paths), os.path.basename(archive), size_mb))


def maybe_package(args, config, merged_by_edition, out_dir):
    """Zip the decks if asked to, on the command line or in the config."""
    if not merged_by_edition:
        return
    packaging = config.get("packaging", {}) or {}
    should_zip = args.do_zip if args.do_zip is not None else packaging.get("create_zip", False)
    if should_zip:
        package_decks(merged_by_edition, packaging, config, out_dir)
    else:
        print("\nSkipped packaging (pass --zip or set packaging.create_zip to enable).")


def report_gaps(incomplete, out_dir):
    """Record any decks that came out short, so the gaps can be filled."""
    if not incomplete:
        return
    report = os.path.join(out_dir, "merge_gaps.json")
    with open(report, "w", encoding="utf-8") as handle:
        json.dump(incomplete, handle, indent=2)
    print("{0} target(s) were incomplete; details in {1}".format(len(incomplete), report))


def tidy_up(args, incomplete, merged_by_edition, consumed_pdfs, config, base_dir, out_dir):
    """Act on --clean, refusing when a deck came out short."""
    if incomplete:
        # Keeping the card files means the gaps can be filled and the merge
        # rerun, rather than everything rebuilt from nothing.
        print(
            "\nNot cleaning up: some decks were incomplete, so the card files are "
            "being kept. Rerun the generator for the cards listed above, merge "
            "again, then clean."
        )
    elif not merged_by_edition:
        print("\nNothing was merged, so there is nothing to clean up.")
    else:
        removed, freed = clean_intermediates(consumed_pdfs, config, base_dir, out_dir)
        print(
            "\nRemoved {0} working file(s), freeing {1:.1f} MB. "
            "The merged decks are kept.".format(removed, freed / (1024.0 * 1024.0))
        )


def merge_one_target(target, config, base_dir, out_dir, bleed, marks, dry_run):
    """
    Assemble the deck for one edition, language and card size.

    Returns ``(deck_path, consumed_pdfs, gap)``. ``deck_path`` is None when
    nothing was written, and ``gap`` records any cards that were missing.
    """
    edition, language, size_key = target["edition"], target["language"], target["size"]
    label = "{0} | {1} | {2}".format(edition, size_key, language.upper())

    data_path = cc.card_data_path(config, base_dir, edition, language)
    cards, suit_order = cc.parse_cards(data_path)
    if not cards:
        print("WARNING: no card data at {0}; skipping".format(data_path))
        return None, [], None

    deck = cc.sort_deck(cards, config, edition, suit_order, language)
    ordered_pdfs, missing = match_card_pdfs(deck, edition, language, size_key, config, out_dir, bleed, marks)

    if not ordered_pdfs:
        # None at all almost always means this size simply was not built, which
        # is a normal choice rather than a problem worth flagging.
        print("--- {0} --- not built, skipping".format(label))
        return None, [], None

    print("--- {0} --- matched {1}/{2}".format(label, len(ordered_pdfs), len(deck)))

    gap = None
    if missing:
        # Some but not all: this deck would be short, so say so loudly.
        gap = {"target": label, "missing": missing}
        print(
            "    WARNING: {0} card PDF(s) missing: {1}{2}".format(
                len(missing), ", ".join(missing[:10]), " ..." if len(missing) > 10 else ""
            )
        )

    deck_name = cc.deck_pdf_name(config, edition, size_key, language, bleed)
    if dry_run:
        print("    would write {0} ({1} pages)".format(deck_name, len(ordered_pdfs) * 2))
        return None, [], gap

    deck_path = os.path.join(out_dir, deck_name)
    pages = merge_deck(ordered_pdfs, deck_path)
    print("    wrote {0} ({1} pages)".format(deck_name, pages))
    return deck_path, ordered_pdfs, gap


def prepare_merge(args, base_dir):
    """
    Read the config and work out what to merge.

    Returns ``(config, out_dir, bleed, marks, targets)``, or None after
    explaining why there is nothing to do.
    """
    config = cc.load_config(base_dir, args.config)
    if not config:
        print("ERROR: could not load {0}".format(args.config))
        return None

    out_dir = args.output_dir or cc.output_dir(config, base_dir)
    if not os.path.isdir(out_dir):
        print("ERROR: output directory not found: {0}".format(out_dir))
        return None

    try:
        profiles = cc.get_export_profiles(
            config, profile_name=args.profile, bleed_mm=args.bleed_mm, printers_marks=args.printers_marks
        )
    except ValueError as exc:
        print("ERROR: {0}".format(exc))
        return None

    bleed = float(profiles[0].get("bleed_mm", 3.0))
    marks = bool(profiles[0].get("printers_marks", False))
    print("Merging profile: bleed {0}mm | {1}".format(cc.format_bleed(bleed), cc.marks_token(marks)))

    targets, warnings = cc.resolve_targets(config, base_dir, args.edition, args.language, args.size)
    for warning in warnings:
        print("WARNING: {0}".format(warning))

    if not targets:
        print("Nothing to merge. Check generation_targets in your config.")
        return None

    return config, out_dir, bleed, marks, targets


def main():
    args = parse_args()
    base_dir = SCRIPT_DIR

    if pymupdf is None and not args.dry_run:
        # Say so before any work is done, rather than partway through a run.
        print(PYMUPDF_HELP.format(sys.prefix))
        return 1

    prepared = prepare_merge(args, base_dir)
    if not prepared:
        return 1
    config, out_dir, bleed, marks, targets = prepared

    merged_by_edition = {}
    incomplete = []
    consumed_pdfs = []

    for target in targets:
        deck_path, used, gap = merge_one_target(target, config, base_dir, out_dir, bleed, marks, args.dry_run)
        if gap:
            incomplete.append(gap)
        if deck_path:
            merged_by_edition.setdefault(target["edition"], []).append(deck_path)
            consumed_pdfs.extend(used)

    if args.dry_run:
        if args.clean:
            print("\nWould then delete the per-card PDFs, .sla files and QR codes.")
        return 0

    maybe_package(args, config, merged_by_edition, out_dir)

    total = sum(len(paths) for paths in merged_by_edition.values())
    print("\nDone. {0} deck(s) merged.".format(total))

    report_gaps(incomplete, out_dir)

    if args.clean:
        tidy_up(args, incomplete, merged_by_edition, consumed_pdfs, config, base_dir, out_dir)

    return 0


if __name__ == "__main__":
    sys.exit(main())
