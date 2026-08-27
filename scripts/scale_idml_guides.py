"""Scale and validate layout details in IDML packages.

Usage:
    python scripts/scale_idml_guides.py SOURCE.idml TARGET.idml
    python scripts/scale_idml_guides.py SOURCE.idml TARGET.idml --check-printable-guides
    python scripts/scale_idml_guides.py SOURCE.idml TARGET.idml --check-artwork-scaling

Without a flag, guide locations are independently scaled to each matched target
page. Page matching uses the page name and whether the member is a spread or
master spread, while guides are matched by their order within a page.

``--check-printable-guides`` and ``--check-artwork-scaling`` do not modify the
target. All other flags update the target IDML in place, so make a copy before
using a fitting or card-text operation. Card-text flags target EoP bridge-card
templates and should not be applied to unrelated templates.

The utility intentionally edits IDML package XML as text. This preserves
InDesign-specific namespace declarations and member ordering while changing
only the targeted attributes.
"""

from __future__ import annotations

import argparse
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Match, Tuple

ATTRIBUTE_PATTERN = re.compile(r'([\w:]+)="([^"]*)"')
GUIDE_PATTERN = re.compile(r"<Guide\b[^>]*(?:/>|>.*?</Guide>)", re.DOTALL)
PAGE_PATTERN = re.compile(r'<Page\b[^>]*\bGeometricBounds="([^"]+)"[^>]*\bName="([^"]+)"[^>]*>')
TEXT_FRAME_PATTERN = re.compile(r"<TextFrame\b(?P<attributes>[^>]*)>(?P<content>.*?)</TextFrame>", re.DOTALL)
PATH_POINT_PATTERN = re.compile(r"<PathPointType\b[^>]*/>")
BODY_TEXT_X = 0.6024 * 72.0
BODY_TEXT_Y = 0.7392 * 72.0
BODY_TEXT_LEADING = 11.04 * 246.614 / 342.0
BODY_TEXT_WIDTH_INCREASE = 6.0
TITLE_HEIGHT_INCREASE = 4.0
TITLE_WIDTH_REDUCTION = 4.0
GUIDE_TOLERANCE = 0.00001


def get_attributes(match: Match[str]) -> Dict[str, str]:
    """Return XML attributes from a complete element match."""
    return dict(ATTRIBUTE_PATTERN.findall(match.group(0)))


def set_attribute(xml: str, name: str, value: str) -> str:
    """Set an existing XML attribute without reparsing InDesign XML."""
    pattern = re.compile(rf'\b{re.escape(name)}="[^"]*"')
    replacement = f'{name}="{value}"'
    if pattern.search(xml):
        return pattern.sub(replacement, xml, count=1)
    return xml.replace("/>", f" {replacement}/>", 1)


def format_number(value: float) -> str:
    """Format an IDML coordinate without insignificant trailing zeros."""
    return f"{value:.6f}".rstrip("0").rstrip(".")


def get_page_geometry(member_name: str, xml: str) -> Tuple[str, float, float]:
    """Return stable page name plus height and width for an IDML member."""
    match = PAGE_PATTERN.search(xml)
    if match is None:
        raise ValueError(f"The IDML member has no named page: {member_name}")
    bounds = [float(value) for value in match.group(1).split()]
    if len(bounds) != 4:
        raise ValueError(f"Invalid page bounds in: {member_name}")
    return match.group(2), bounds[2] - bounds[0], bounds[3] - bounds[1]


def get_page_key(member_name: str, xml: str) -> Tuple[str, str]:
    """Return a stable page identity independent of InDesign object IDs."""
    page_name, _, _ = get_page_geometry(member_name, xml)
    return member_name.split("/", 1)[0], page_name


def read_xml_members(path: Path, prefixes: Tuple[str, ...] = ("Spreads/", "MasterSpreads/")) -> Dict[str, str]:
    """Read package layout members as UTF-8 XML."""
    with zipfile.ZipFile(path) as archive:
        return {
            member.filename: archive.read(member).decode("utf-8")
            for member in archive.infolist()
            if member.filename.endswith(".xml") and member.filename.startswith(prefixes)
        }


def read_stories(path: Path) -> Dict[str, str]:
    """Read stories keyed by InDesign story identifier."""
    with zipfile.ZipFile(path) as archive:
        return {
            Path(member.filename).stem.removeprefix("Story_"): archive.read(member).decode("utf-8")
            for member in archive.infolist()
            if member.filename.startswith("Stories/Story_") and member.filename.endswith(".xml")
        }


def rewrite_package(path: Path, replacements: Dict[str, str]) -> None:
    """Atomically replace selected IDML members, preserving all other entries."""
    if not replacements:
        return
    with tempfile.NamedTemporaryFile(delete=False, suffix=".idml", dir=path.parent) as temporary_file:
        temporary_path = Path(temporary_file.name)
    try:
        with zipfile.ZipFile(path) as source, zipfile.ZipFile(temporary_path, "w") as target:
            for member in source.infolist():
                content = replacements.get(member.filename)
                if content is None:
                    target.writestr(member, source.read(member))
                else:
                    target.writestr(member, content.encode("utf-8"))
        shutil.move(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def guide_location(attributes: Dict[str, str]) -> float:
    """Return an IDML guide's numeric location."""
    try:
        return float(attributes["Location"])
    except KeyError as error:
        raise ValueError("Guide is missing Location") from error


def guide_limit(attributes: Dict[str, str], height: float, width: float) -> float:
    """Return the page dimension applicable to a guide orientation."""
    orientation = attributes.get("Orientation", "Horizontal")
    return width if orientation == "Vertical" else height


def scale_guides(source: Path, target: Path) -> int:
    """Scale source guide locations into matched target pages by guide order."""
    source_members = read_xml_members(source)
    target_members = read_xml_members(target)
    source_pages = {get_page_key(member_name, xml): (member_name, xml) for member_name, xml in source_members.items()}
    replacements: Dict[str, str] = {}
    updated_guides = 0

    for member_name, target_xml in target_members.items():
        source_entry = source_pages.get(get_page_key(member_name, target_xml))
        if source_entry is None:
            raise ValueError(f"Missing source page for: {member_name}")
        source_member_name, source_xml = source_entry
        _, source_height, source_width = get_page_geometry(source_member_name, source_xml)
        _, target_height, target_width = get_page_geometry(member_name, target_xml)
        source_guides = [get_attributes(match) for match in GUIDE_PATTERN.finditer(source_xml)]
        target_guides = list(GUIDE_PATTERN.finditer(target_xml))
        if len(source_guides) != len(target_guides):
            raise ValueError(f"Guide count differs for page: {member_name}")
        guide_index = 0

        def replace_guide(match: Match[str]) -> str:
            nonlocal guide_index, updated_guides
            source_guide = source_guides[guide_index]
            guide_index += 1
            source_limit = guide_limit(source_guide, source_height, source_width)
            target_attributes = get_attributes(match)
            target_limit = guide_limit(target_attributes, target_height, target_width)
            scaled_location = guide_location(source_guide) * target_limit / source_limit
            updated_guides += 1
            return set_attribute(match.group(0), "Location", format_number(scaled_location))

        replacements[member_name] = GUIDE_PATTERN.sub(replace_guide, target_xml)

    rewrite_package(target, replacements)
    return updated_guides


def validate_guides(target: Path) -> Tuple[int, int]:
    """Validate that every guide lies within its corresponding page boundary."""
    checked = 0
    invalid = 0
    for member_name, xml in read_xml_members(target).items():
        _, height, width = get_page_geometry(member_name, xml)
        for match in GUIDE_PATTERN.finditer(xml):
            attributes = get_attributes(match)
            location = guide_location(attributes)
            limit = guide_limit(attributes, height, width)
            checked += 1
            if location < -GUIDE_TOLERANCE or location > limit + GUIDE_TOLERANCE:
                invalid += 1
    return checked, invalid


def fit_guides_to_trim(target: Path) -> int:
    """Clamp guides to the printable page boundary."""
    replacements: Dict[str, str] = {}
    changed = 0
    for member_name, xml in read_xml_members(target).items():
        _, height, width = get_page_geometry(member_name, xml)

        def replace_guide(match: Match[str]) -> str:
            nonlocal changed
            attributes = get_attributes(match)
            location = guide_location(attributes)
            fitted = min(max(location, 0.0), guide_limit(attributes, height, width))
            if abs(fitted - location) <= GUIDE_TOLERANCE:
                return match.group(0)
            changed += 1
            return set_attribute(match.group(0), "Location", format_number(fitted))

        replacements[member_name] = GUIDE_PATTERN.sub(replace_guide, xml)
    rewrite_package(target, replacements)
    return changed


def replace_path_points(content: str, transform: Callable[[Dict[str, str]], Dict[str, str]]) -> str:
    """Apply a coordinate transform to each path point in a text frame."""

    def replace_point(match: Match[str]) -> str:
        attributes = transform(get_attributes(match))
        point = match.group(0)
        for name, value in attributes.items():
            point = set_attribute(point, name, value)
        return point

    return PATH_POINT_PATTERN.sub(replace_point, content)


def update_text_frames(target: Path, eligible: Callable[[str], bool], transform: Callable[[str], str]) -> int:
    """Transform eligible spread text frames and return their count."""
    stories = read_stories(target)
    replacements: Dict[str, str] = {}
    updated = 0
    for member_name, xml in read_xml_members(target, ("Spreads/",)).items():

        def replace_frame(match: Match[str]) -> str:
            nonlocal updated
            attributes = get_attributes(match)
            if not eligible(stories.get(attributes.get("ParentStory", ""), "")):
                return match.group(0)
            updated += 1
            return match.group(0).replace(match.group("content"), transform(match.group("content")), 1)

        replacements[member_name] = TEXT_FRAME_PATTERN.sub(replace_frame, xml)
    rewrite_package(target, replacements)
    return updated


def straighten_card_text_frames(target: Path) -> int:
    """Square body and title frames by aligning Bezier handles with anchors."""

    def straighten(content: str) -> str:
        def transform(attributes: Dict[str, str]) -> Dict[str, str]:
            anchor = attributes.get("Anchor")
            if anchor:
                attributes["LeftDirection"] = anchor
                attributes["RightDirection"] = anchor
            return attributes

        return replace_path_points(content, transform)

    return update_text_frames(target, lambda story: "_desc}" in story or "_suit}" in story, straighten)


def widen_card_body_frames(target: Path) -> int:
    """Extend each body text frame's right edge without moving its left edge."""

    def widen(content: str) -> str:
        points = list(PATH_POINT_PATTERN.finditer(content))
        x_values = [float(get_attributes(point).get("Anchor", "0 0").split()[0]) for point in points]
        if not x_values:
            return content
        right_edge = max(x_values)

        def transform(attributes: Dict[str, str]) -> Dict[str, str]:
            anchor = attributes.get("Anchor", "").split()
            if len(anchor) == 2 and abs(float(anchor[0]) - right_edge) <= GUIDE_TOLERANCE:
                anchor[0] = format_number(right_edge + BODY_TEXT_WIDTH_INCREASE)
                attributes["Anchor"] = " ".join(anchor)
                attributes["LeftDirection"] = attributes["Anchor"]
                attributes["RightDirection"] = attributes["Anchor"]
            return attributes

        return replace_path_points(content, transform)

    return update_text_frames(target, lambda story: "_desc}" in story, widen)


def set_card_body_layout(target: Path) -> int:
    """Set bridge body frames to the requested position and scaled leading."""
    stories = read_stories(target)
    replacements: Dict[str, str] = {}
    for story_id, story in stories.items():
        if "_desc}" not in story:
            continue
        updated_story = re.sub(
            r'<Leading type="unit">[^<]+</Leading>',
            f'<Leading type="unit">{BODY_TEXT_LEADING:.6f}</Leading>',
            story,
        )
        if updated_story == story:
            updated_story = updated_story.replace(
                "</CharacterStyleRange>",
                f'<Properties><Leading type="unit">{BODY_TEXT_LEADING:.6f}</Leading></Properties></CharacterStyleRange>',
                1,
            )
        replacements[f"Stories/Story_{story_id}.xml"] = updated_story
    rewrite_package(target, replacements)

    def position(content: str) -> str:
        points = list(PATH_POINT_PATTERN.finditer(content))
        anchors = [get_attributes(point).get("Anchor", "0 0").split() for point in points]
        if not anchors or any(len(anchor) != 2 for anchor in anchors):
            return content
        left = min(float(anchor[0]) for anchor in anchors)
        top = min(float(anchor[1]) for anchor in anchors)

        def transform(attributes: Dict[str, str]) -> Dict[str, str]:
            anchor = attributes.get("Anchor", "").split()
            if len(anchor) == 2:
                x = float(anchor[0]) - left + BODY_TEXT_X
                y = float(anchor[1]) - top + BODY_TEXT_Y
                attributes["Anchor"] = f"{format_number(x)} {format_number(y)}"
                attributes["LeftDirection"] = attributes["Anchor"]
                attributes["RightDirection"] = attributes["Anchor"]
            return attributes

        return replace_path_points(content, transform)

    return update_text_frames(target, lambda story: "_desc}" in story, position)


def resize_card_title_boxes(target: Path, height_change: float = TITLE_HEIGHT_INCREASE) -> int:
    """Increase title-frame height by moving their bottom path points."""

    def resize(content: str) -> str:
        points = list(PATH_POINT_PATTERN.finditer(content))
        y_values = [float(get_attributes(point).get("Anchor", "0 0").split()[1]) for point in points]
        if not y_values:
            return content
        bottom = max(y_values)

        def transform(attributes: Dict[str, str]) -> Dict[str, str]:
            anchor = attributes.get("Anchor", "").split()
            if len(anchor) == 2 and abs(float(anchor[1]) - bottom) <= GUIDE_TOLERANCE:
                anchor[1] = format_number(bottom + height_change)
                attributes["Anchor"] = " ".join(anchor)
                attributes["LeftDirection"] = attributes["Anchor"]
                attributes["RightDirection"] = attributes["Anchor"]
            return attributes

        return replace_path_points(content, transform)

    return update_text_frames(target, lambda story: "_suit}" in story, resize)


def narrow_card_title_boxes(target: Path) -> int:
    """Reduce title-frame width by moving their right path points inward."""

    def narrow(content: str) -> str:
        points = list(PATH_POINT_PATTERN.finditer(content))
        x_values = [float(get_attributes(point).get("Anchor", "0 0").split()[0]) for point in points]
        if not x_values:
            return content
        right = max(x_values)

        def transform(attributes: Dict[str, str]) -> Dict[str, str]:
            anchor = attributes.get("Anchor", "").split()
            if len(anchor) == 2 and abs(float(anchor[0]) - right) <= GUIDE_TOLERANCE:
                anchor[0] = format_number(right - TITLE_WIDTH_REDUCTION)
                attributes["Anchor"] = " ".join(anchor)
                attributes["LeftDirection"] = attributes["Anchor"]
                attributes["RightDirection"] = attributes["Anchor"]
            return attributes

        return replace_path_points(content, transform)

    return update_text_frames(target, lambda story: "_suit}" in story, narrow)


def raise_card_titles(target: Path) -> int:
    """Move title-frame geometry up by the recorded four-point title adjustment."""

    def raise_frame(content: str) -> str:
        def transform(attributes: Dict[str, str]) -> Dict[str, str]:
            anchor = attributes.get("Anchor", "").split()
            if len(anchor) == 2:
                attributes["Anchor"] = f"{anchor[0]} {format_number(float(anchor[1]) - TITLE_HEIGHT_INCREASE)}"
                attributes["LeftDirection"] = attributes["Anchor"]
                attributes["RightDirection"] = attributes["Anchor"]
            return attributes

        return replace_path_points(content, transform)

    return update_text_frames(target, lambda story: "_suit}" in story, raise_frame)


def validate_artwork_scaling(source: Path, target: Path) -> Tuple[int, int]:
    """Check that matched page geometry has positive, finite scaling ratios."""
    source_pages = {get_page_key(name, xml): (name, xml) for name, xml in read_xml_members(source).items()}
    checked = 0
    invalid = 0
    for member_name, target_xml in read_xml_members(target).items():
        source_entry = source_pages.get(get_page_key(member_name, target_xml))
        if source_entry is None:
            invalid += 1
            continue
        _, source_xml = source_entry
        _, source_height, source_width = get_page_geometry(member_name, source_xml)
        _, target_height, target_width = get_page_geometry(member_name, target_xml)
        checked += 1
        if min(source_height, source_width, target_height, target_width) <= 0:
            invalid += 1
    return checked, invalid


def fit_master_dielines(target: Path) -> int:
    """Clamp master-spread guide/dieline positions to their page bounds."""
    return fit_guides_to_trim(target)


def build_parser() -> argparse.ArgumentParser:
    """Create the utility command-line parser."""
    parser = argparse.ArgumentParser(
        description="Scale and validate IDML guides and EoP card layout frames.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("source", type=Path, help="Source IDML package used as the scaling reference.")
    parser.add_argument("target", type=Path, help="Target IDML package to update or validate.")
    operation = parser.add_mutually_exclusive_group()
    operation.add_argument(
        "--check-printable-guides", action="store_true", help="Report target guides that lie outside their page."
    )
    operation.add_argument(
        "--check-artwork-scaling",
        action="store_true",
        help="Validate that matched source and target pages have valid geometry.",
    )
    operation.add_argument(
        "--fit-guides-to-trim", action="store_true", help="Clamp target spread and master-spread guides to page bounds."
    )
    operation.add_argument(
        "--fit-master-dielines", action="store_true", help="Clamp target master-spread guides to page bounds."
    )
    operation.add_argument(
        "--straighten-card-text", action="store_true", help="Square EoP body and title text-frame paths."
    )
    operation.add_argument(
        "--set-card-body-layout", action="store_true", help="Set EoP bridge-card body frame position and leading."
    )
    operation.add_argument(
        "--widen-card-body", action="store_true", help="Extend EoP bridge-card body-frame right edges by six points."
    )
    operation.add_argument(
        "--resize-card-title-boxes", action="store_true", help="Increase EoP title-frame height by four points."
    )
    operation.add_argument(
        "--narrow-card-title-boxes", action="store_true", help="Reduce EoP title-frame width by four points."
    )
    operation.add_argument(
        "--raise-card-titles", action="store_true", help="Move EoP title-frame paths up by four points."
    )
    operation.add_argument(
        "--adjust-card-text", action="store_true", help="Apply EoP bridge body layout and square its text frames."
    )
    return parser


def main() -> int:
    """Run the selected layout operation."""
    args = build_parser().parse_args()
    if not args.source.is_file() or not args.target.is_file():
        raise FileNotFoundError("Both source and target must be existing IDML files.")
    if args.check_printable_guides:
        checked, invalid = validate_guides(args.target)
        print(f"Guides checked: {checked}; out of bounds: {invalid}")
        return int(invalid > 0)
    if args.check_artwork_scaling:
        checked, invalid = validate_artwork_scaling(args.source, args.target)
        print(f"Page scaling checked: {checked}; invalid: {invalid}")
        return int(invalid > 0)
    if args.fit_guides_to_trim:
        print(f"Guides fitted: {fit_guides_to_trim(args.target)}")
    elif args.fit_master_dielines:
        print(f"Master guides fitted: {fit_master_dielines(args.target)}")
    elif args.straighten_card_text:
        print(f"Text frames straightened: {straighten_card_text_frames(args.target)}")
    elif args.set_card_body_layout:
        print(f"Body frames updated: {set_card_body_layout(args.target)}")
    elif args.widen_card_body:
        print(f"Body frames widened: {widen_card_body_frames(args.target)}")
    elif args.resize_card_title_boxes:
        print(f"Title boxes resized: {resize_card_title_boxes(args.target)}")
    elif args.narrow_card_title_boxes:
        print(f"Title boxes narrowed: {narrow_card_title_boxes(args.target)}")
    elif args.raise_card_titles:
        print(f"Title boxes raised: {raise_card_titles(args.target)}")
    elif args.adjust_card_text:
        set_card_body_layout(args.target)
        print(f"Text frames straightened: {straighten_card_text_frames(args.target)}")
    else:
        print(f"Guides scaled: {scale_guides(args.source, args.target)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
