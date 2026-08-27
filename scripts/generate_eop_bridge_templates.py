"""Generate EoP Bridge IDML templates from their Tarot counterparts.

This script replicates the page-dimension rescaling applied when
eop_ver_cards_tarot_lang.idml was converted into
eop_ver_cards_bridge_lang.idml and applies it to the remaining 11 EoP
Tarot templates listed in GitHub issue #3409.

Usage:
    python scripts/generate_eop_bridge_templates.py

Outputs are written to resources/templates/ alongside the existing templates.
"""

from __future__ import annotations

import re
import shutil
import tempfile
import uuid
import zipfile
from pathlib import Path
from typing import Dict, Tuple

# ---------------------------------------------------------------------------
# Card-size constants (points)
# ---------------------------------------------------------------------------
TAROT_H = 342.0   # height (taller dimension)
TAROT_W = 198.0   # width
BRIDGE_H = 246.614
BRIDGE_W = 158.74
BLEED_TAROT = 9.0
BLEED_BRIDGE = 8.503937

SCALE_H = BRIDGE_H / TAROT_H  # ≈ 0.720508…
SCALE_W = BRIDGE_W / TAROT_W  # ≈ 0.801717…

TEMPLATES_DIR = Path("resources/templates")

# Source → Target pairs (tarot → bridge)
TEMPLATE_PAIRS: list[Tuple[str, str]] = [
    ("eop_ver_about_tarot_lang.idml",                      "eop_ver_about_bridge_lang.idml"),
    ("eop_ver_instructions1_tarot_lang.idml",              "eop_ver_instructions1_bridge_lang.idml"),
    ("eop_ver_instructions2_tarot_lang.idml",              "eop_ver_instructions2_bridge_lang.idml"),
    ("eop_ver_strategy-cards_tarot_lang.idml",             "eop_ver_strategy-cards_bridge_lang.idml"),
    ("eop_ver_threat-denialofsvc-cards_tarot_lang.idml",   "eop_ver_threat-denialofsvc-cards_bridge_lang.idml"),
    ("eop_ver_threat-elevofpriv-cards_tarot_lang.idml",    "eop_ver_threat-elevofpriv-cards_bridge_lang.idml"),
    ("eop_ver_threat-infodisclosure-cards_tarot_lang.idml","eop_ver_threat-infodisclosure-cards_bridge_lang.idml"),
    ("eop_ver_threat-repudation-cards_tarot_lang.idml",    "eop_ver_threat-repudation-cards_bridge_lang.idml"),
    ("eop_ver_threat-spoofing-cards_tarot_lang.idml",      "eop_ver_threat-spoofing-cards_bridge_lang.idml"),
    ("eop_ver_threat-tampering-cards_tarot_lang.idml",     "eop_ver_threat-tampering-cards_bridge_lang.idml"),
    ("eop_ver_deck_tarot_lang.idml",                       "eop_ver_deck_bridge_lang.idml"),
]

# ---------------------------------------------------------------------------
# Reference transformation derived from cards tarot → bridge diff
# ---------------------------------------------------------------------------

def _fmt(v: float) -> str:
    """Format a coordinate/size value, stripping insignificant trailing zeros."""
    s = f"{v:.6f}".rstrip("0").rstrip(".")
    return s


def _scale_number(text: str, factor: float) -> str:
    """Scale a single numeric string by factor."""
    try:
        return _fmt(float(text) * factor)
    except ValueError:
        return text


def _scale_pair(pair_str: str, sx: float, sy: float) -> str:
    """Scale a 'x y' coordinate pair."""
    parts = pair_str.split()
    if len(parts) != 2:
        return pair_str
    return f"{_scale_number(parts[0], sx)} {_scale_number(parts[1], sy)}"


def _scale_4tuple(bounds_str: str) -> str:
    """Scale a 'top left bottom right' bounds string (page bounds use H/W)."""
    parts = bounds_str.split()
    if len(parts) != 4:
        return bounds_str
    top    = _scale_number(parts[0], SCALE_H)
    left   = _scale_number(parts[1], SCALE_W)
    bottom = _scale_number(parts[2], SCALE_H)
    right  = _scale_number(parts[3], SCALE_W)
    return f"{top} {left} {bottom} {right}"


def _rewrite_attr(xml: str, attr: str, new_val: str) -> str:
    """Replace the value of a specific XML attribute (first occurrence only)."""
    pat = re.compile(rf'\b{re.escape(attr)}="([^"]*)"')
    return pat.sub(f'{attr}="{new_val}"', xml, count=1)


def _rewrite_attr_all(xml: str, attr: str, transformer) -> str:
    """Replace every occurrence of an XML attribute using transformer(value)."""
    def replace(m: re.Match) -> str:
        return f'{attr}="{transformer(m.group(1))}"'
    return re.sub(rf'\b{re.escape(attr)}="([^"]*)"', replace, xml)


# ---------------------------------------------------------------------------
# Per-file transformation helpers
# ---------------------------------------------------------------------------

def _transform_preferences(xml: str) -> str:
    """Scale DocumentPreference page size and bleed in Resources/Preferences.xml."""
    xml = _rewrite_attr(xml, "PageHeight", _fmt(BRIDGE_H))
    xml = _rewrite_attr(xml, "PageWidth",  _fmt(BRIDGE_W))
    for bleed_attr in (
        "DocumentBleedTopOffset", "DocumentBleedBottomOffset",
        "DocumentBleedInsideOrLeftOffset", "DocumentBleedOutsideOrRightOffset",
    ):
        xml = _rewrite_attr(xml, bleed_attr, _fmt(BLEED_BRIDGE))
    return xml


def _scale_point_size(v: str) -> str:
    """Scale a PointSize value using the height ratio (tarot is portrait)."""
    try:
        return _fmt(float(v) * SCALE_H)
    except ValueError:
        return v


def _scale_stroke_weight(v: str) -> str:
    try:
        return _fmt(float(v) * SCALE_H)
    except ValueError:
        return v


def _transform_styles(xml: str) -> str:
    """Rescale point sizes, leading, stroke weights in Resources/Styles.xml."""
    # Regenerate StyleUniqueId so InDesign treats bridge as a distinct document
    def new_uuid(_: str) -> str:
        return str(uuid.uuid4())

    xml = _rewrite_attr_all(xml, "StyleUniqueId", new_uuid)

    # Scale numeric size attributes
    for attr in ("PointSize", "RuleAboveLineWeight", "RuleBelowLineWeight",
                 "StrokeWeight", "KerningValue"):
        def scale_val(v: str, _attr=attr) -> str:  # noqa: E731
            if v in ("1e+11",):   # special InDesign sentinel – leave alone
                return v
            try:
                return _fmt(float(v) * SCALE_H)
            except ValueError:
                return v
        xml = _rewrite_attr_all(xml, attr, scale_val)

    return xml


def _scale_item_transform(transform_str: str) -> str:
    """Scale the translation components (indices 4 & 5) of a 6-value matrix."""
    parts = transform_str.split()
    if len(parts) != 6:
        return transform_str
    try:
        # matrix: a b c d tx ty – scale tx by SCALE_W, ty by SCALE_H
        tx = float(parts[4]) * SCALE_W
        ty = float(parts[5]) * SCALE_H
        parts[4] = _fmt(tx)
        parts[5] = _fmt(ty)
    except ValueError:
        pass
    return " ".join(parts)


def _transform_spread(xml: str) -> str:
    """Rescale Spread and MasterSpread layout XML."""
    # Scale ItemTransform translations in Spread/MasterSpread elements
    xml = _rewrite_attr_all(xml, "ItemTransform", _scale_item_transform)

    # Scale GeometricBounds (top left bottom right)
    xml = _rewrite_attr_all(xml, "GeometricBounds", _scale_4tuple)

    # Scale Anchor / LeftDirection / RightDirection (x y pairs)
    for coord_attr in ("Anchor", "LeftDirection", "RightDirection"):
        xml = _rewrite_attr_all(xml, coord_attr,
                                lambda v: _scale_pair(v, SCALE_W, SCALE_H))

    # Scale StrokeWeight
    xml = _rewrite_attr_all(xml, "StrokeWeight",
                            lambda v: _scale_number(v, SCALE_H))

    # Scale MarginPreference columns / ColumnGutter (use SCALE_W)
    for margin_attr in ("Top", "Bottom", "Left", "Right", "ColumnGutter"):
        xml = _rewrite_attr_all(xml, margin_attr,
                                lambda v: _scale_number(v, SCALE_W))

    # Scale GridDataInformation PointSize
    xml = _rewrite_attr_all(xml, "PointSize", _scale_point_size)

    # Scale TextColumnFixedWidth / TextColumnGutter / MinimumFirstBaselineOffset
    for tf_attr in ("TextColumnFixedWidth", "TextColumnGutter"):
        xml = _rewrite_attr_all(xml, tf_attr,
                                lambda v: _scale_number(v, SCALE_W))

    # Scale ColumnsPositions (space-separated list)
    def scale_cols(v: str) -> str:
        return " ".join(_scale_number(x, SCALE_W) for x in v.split())
    xml = _rewrite_attr_all(xml, "ColumnsPositions", scale_cols)

    # Scale GradientFillStart / GradientFillLength / GradientStrokeStart
    for gattr in ("GradientFillStart", "GradientStrokeStart"):
        xml = _rewrite_attr_all(xml, gattr,
                                lambda v: _scale_pair(v, SCALE_W, SCALE_H))
    for gattr in ("GradientFillLength", "GradientStrokeLength",
                  "GradientFillHiliteLength", "GradientStrokeHiliteLength"):
        xml = _rewrite_attr_all(xml, gattr,
                                lambda v: _scale_number(v, SCALE_H))

    return xml


def _transform_story(xml: str) -> str:
    """Scale Leading values in Stories/*.xml."""
    def scale_leading(m: re.Match) -> str:
        tag_open = m.group(1)
        value    = m.group(2)
        tag_close = m.group(3)
        try:
            scaled = _fmt(float(value) * SCALE_H)
        except ValueError:
            scaled = value
        return f"{tag_open}{scaled}{tag_close}"

    return re.sub(
        r'(<Leading[^>]*>)([^<]+)(</Leading>)',
        scale_leading,
        xml,
    )


def _transform_metadata(xml: str) -> str:
    """Update document IDs and timestamps in META-INF/metadata.xml."""
    # New DocumentID
    new_id = f"xmp.did:{uuid.uuid4()}"
    xml = re.sub(
        r'(<xmpMM:DocumentID>)[^<]*(</xmpMM:DocumentID>)',
        rf'\g<1>{new_id}\g<2>',
        xml,
    )
    # Leave timestamps as-is (they reflect original InDesign save time)
    return xml


# ---------------------------------------------------------------------------
# Package rewriter
# ---------------------------------------------------------------------------

def _rewrite_package(src_path: Path, dst_path: Path) -> None:
    """Read src_path, apply transformations, write result to dst_path."""
    replacements: Dict[str, bytes] = {}

    with zipfile.ZipFile(src_path) as zin:
        members = zin.infolist()
        for info in members:
            raw = zin.read(info)
            name = info.filename

            if name == "Resources/Preferences.xml":
                text = raw.decode("utf-8")
                replacements[name] = _transform_preferences(text).encode("utf-8")

            elif name == "Resources/Styles.xml":
                text = raw.decode("utf-8")
                replacements[name] = _transform_styles(text).encode("utf-8")

            elif name == "META-INF/metadata.xml":
                text = raw.decode("utf-8")
                replacements[name] = _transform_metadata(text).encode("utf-8")

            elif name.startswith(("Spreads/", "MasterSpreads/")):
                text = raw.decode("utf-8")
                replacements[name] = _transform_spread(text).encode("utf-8")

            elif name.startswith("Stories/"):
                text = raw.decode("utf-8")
                replacements[name] = _transform_story(text).encode("utf-8")

        # Write output archive
        tmp = dst_path.parent / (dst_path.name + ".tmp")
        try:
            with zipfile.ZipFile(src_path) as zsrc, \
                 zipfile.ZipFile(tmp, "w") as zout:
                for info in zsrc.infolist():
                    data = replacements.get(info.filename)
                    if data is not None:
                        zout.writestr(info, data)
                    else:
                        zout.writestr(info, zsrc.read(info))
            shutil.move(tmp, dst_path)
        finally:
            if tmp.exists():
                tmp.unlink()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    for tarot_name, bridge_name in TEMPLATE_PAIRS:
        src = TEMPLATES_DIR / tarot_name
        dst = TEMPLATES_DIR / bridge_name

        if not src.exists():
            print(f"[SKIP] Source not found: {src}")
            continue

        print(f"[GEN ] {tarot_name} -> {bridge_name}", end=" ... ", flush=True)
        _rewrite_package(src, dst)
        print(f"OK ({dst.stat().st_size:,} bytes)")

    print("\nAll templates generated successfully.")


if __name__ == "__main__":
    main()
