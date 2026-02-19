#!/usr/bin/env python3
"""
Fix ODT templates for Issue #2133
Applies page breaks and column layout corrections to guide templates
"""

import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import shutil

# Register namespaces to preserve prefixes
NS = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
    "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
    "style": "urn:oasis:names:tc:opendocument:xmlns:style:1.0",
    "fo": "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0",
    "svg": "urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0",
    "loext": "urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0",
}

# Register all namespaces
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


def apply_suit_page_breaks(content_root, styles_root):
    """
    Fix #1: Add page breaks before suit sections

    Strategy: Modify P24 style (suit heading style) to include break-before page
    """
    print("\n[Fix #1] Adding page breaks before suit sections...")

    # Find P24 style in automatic-styles (content.xml)
    auto_styles = content_root.find(".//office:automatic-styles", NS)
    if auto_styles is None:
        print("  ⚠ WARNING: No automatic-styles found in content.xml")
        return False

    # Find or create P24 style
    p24_style = auto_styles.find('.//style:style[@style:name="P24"]', NS)

    if p24_style is None:
        print("  ⚠ WARNING: Style P24 not found, searching for suit heading style...")
        # Try to find the actual suit heading style
        # Look for paragraphs containing ${VE_suit} and get their style
        body = content_root.find(".//office:body", NS)
        if body:
            for para in body.findall(".//text:p", NS):
                text = "".join(para.itertext())
                if "${VE_suit}" in text or "${AT_suit}" in text:
                    style_name = para.get(f'{{{NS["text"]}}}style-name')
                    p24_style = auto_styles.find(f'.//style:style[@style:name="{style_name}"]', NS)
                    print(f"  ✓ Found suit heading style: {style_name}")
                    break

    if p24_style is None:
        print("  ✗ FAILED: Could not find suit heading style")
        return False

    # Get or create paragraph-properties element
    para_props = p24_style.find(".//style:paragraph-properties", NS)
    if para_props is None:
        para_props = ET.SubElement(p24_style, f'{{{NS["style"]}}}paragraph-properties')

    # Add fo:break-before="page" attribute
    para_props.set(f'{{{NS["fo"]}}}break-before', "page")

    print("  ✓ Added fo:break-before='page' to suit heading style")
    return True


def apply_two_column_layout(content_root, styles_root):
    """
    Fix #2: Add proper two-column section layout

    Strategy: Create section style with 2 columns and wrap card tables in sections
    """
    print("\n[Fix #2] Implementing two-column section layout...")

    # Step 1: Create section style with 2 columns in automatic-styles
    auto_styles = content_root.find(".//office:automatic-styles", NS)
    if auto_styles is None:
        auto_styles = ET.SubElement(content_root, f'{{{NS["office"]}}}automatic-styles')

    # Check if section style already exists
    section_style_name = "Sect_TwoColumn"
    existing = auto_styles.find(f'.//style:style[@style:name="{section_style_name}"]', NS)

    if existing is None:
        # Create section style
        section_style = ET.SubElement(auto_styles, f'{{{NS["style"]}}}style')
        section_style.set(f'{{{NS["style"]}}}name', section_style_name)
        section_style.set(f'{{{NS["style"]}}}family', "section")

        # Add section properties with columns
        section_props = ET.SubElement(section_style, f'{{{NS["style"]}}}section-properties')
        columns_elem = ET.SubElement(section_props, f'{{{NS["style"]}}}columns')
        columns_elem.set(f'{{{NS["fo"]}}}column-count', "2")
        columns_elem.set(f'{{{NS["fo"]}}}column-gap', "0.5cm")

        # Define column widths
        for col_index in range(2):
            col = ET.SubElement(columns_elem, f'{{{NS["style"]}}}column')
            col.set(f'{{{NS["style"]}}}rel-width', "1*")
            if col_index == 0:
                col.set(f'{{{NS["fo"]}}}start-indent', "0cm")
                col.set(f'{{{NS["fo"]}}}end-indent', "0.25cm")
            else:
                col.set(f'{{{NS["fo"]}}}start-indent', "0.25cm")
                col.set(f'{{{NS["fo"]}}}end-indent', "0cm")

        print(f"  ✓ Created section style '{section_style_name}' with 2 columns")
    else:
        print(f"  ℹ Section style '{section_style_name}' already exists")

    # Step 2: Wrap card table groups in sections
    # For now, we'll document this as a manual step since automatic wrapping
    # is complex and risk of breaking existing structure

    print("  ℹ NOTE: Section wrapping should be applied manually in LibreOffice:")
    print("    1. Select card content for each suit")
    print("    2. Format → Sections → Insert Section")
    print("    3. Choose 'Columns' tab, set to 2 columns with 0.5cm gap")

    return True


def apply_card_ordering_fix(content_root):
    """
    Fix #3: Document card ordering requirements for duplex printing

    This fix is complex and should be done in a separate template variant
    """
    print("\n[Fix #3] Card ordering for duplex printing...")
    print("  ℹ NOTE: This requires creating a separate 'guide_print' template variant")
    print("  ℹ Manual restructuring needed to alternate front/back card pairs")
    print("  ℹ Skipping automatic fix (requires new template design)")
    return True


def fix_template(template_path, output_path):
    """Apply all fixes to a template file"""
    print(f"\n{'=' * 80}")
    print(f"Processing: {template_path.name}")
    print(f"{'=' * 80}")

    # Create backup
    backup_path = template_path.with_suffix(".odt.backup")
    if not backup_path.exists():
        shutil.copy2(template_path, backup_path)
        print(f"✓ Backup created: {backup_path.name}")

    # Extract template
    temp_dir = template_path.parent / "temp_fix"
    temp_dir.mkdir(exist_ok=True)

    with zipfile.ZipFile(template_path) as z:
        z.extractall(temp_dir)

    # Load XML files
    content_xml = temp_dir / "content.xml"
    styles_xml = temp_dir / "styles.xml"

    content_tree = ET.parse(content_xml)
    content_root = content_tree.getroot()

    styles_tree = ET.parse(styles_xml)
    styles_root = styles_tree.getroot()

    # Apply fixes
    fix1_ok = apply_suit_page_breaks(content_root, styles_root)
    fix2_ok = apply_two_column_layout(content_root, styles_root)
    fix3_ok = apply_card_ordering_fix(content_root)

    # Save modified XML
    content_tree.write(content_xml, encoding="UTF-8", xml_declaration=True)
    styles_tree.write(styles_xml, encoding="UTF-8", xml_declaration=True)

    # Repackage as ODT
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for file_path in temp_dir.rglob("*"):
            if file_path.is_file():
                arc_name = file_path.relative_to(temp_dir)
                # mimetype must be first and uncompressed
                if arc_name.name == "mimetype":
                    zout.write(file_path, arc_name, compress_type=zipfile.ZIP_STORED)
                else:
                    zout.write(file_path, arc_name)

    # Cleanup
    shutil.rmtree(temp_dir)

    print(f"\n{'=' * 80}")
    print(f"✓ Fixed template saved to: {output_path.name}")
    print(f"{'=' * 80}")

    if fix1_ok:
        print("  ✓ Fix #1: Page breaks applied")
    else:
        print("  ⚠ Fix #1: MANUAL FIX REQUIRED")

    if fix2_ok:
        print("  ✓ Fix #2: Column style created (manual section wrapping needed)")
    else:
        print("  ⚠ Fix #2: FAILED")

    if fix3_ok:
        print("  ℹ Fix #3: Documented (requires separate template)")

    return fix1_ok and fix2_ok


def main():
    """Main execution"""
    base_path = Path(__file__).parent
    templates_path = base_path / "resources" / "templates"
    output_path = base_path / "output" / "fixed_templates"
    output_path.mkdir(parents=True, exist_ok=True)

    templates_to_fix = [
        "owasp_cornucopia_webapp_ver_guide_bridge_lang.odt",
        "owasp_cornucopia_webapp_ver_guide_bridge_qr_lang.odt",
    ]

    print("\n" + "=" * 80)
    print("OWASP Cornucopia Issue #2133 Template Fixer")
    print("=" * 80)

    success_count = 0
    for template_name in templates_to_fix:
        template_path = templates_path / template_name
        if template_path.exists():
            output_file = output_path / f"fixed_{template_name}"
            if fix_template(template_path, output_file):
                success_count += 1
        else:
            print(f"\n⚠ Template not found: {template_name}")

    print("\n" + "=" * 80)
    print(f"COMPLETED: {success_count}/{len(templates_to_fix)} templates fixed")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Review fixed templates in output/fixed_templates/")
    print("2. Open in LibreOffice and manually wrap card sections in 2-column sections")
    print("3. Test PDF generation with: python -m pipenv run python .\\scripts\\convert.py ...")
    print("4. If successful, replace original templates")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
