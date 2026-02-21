#!/usr/bin/env python3
"""
Fix ODT templates for Issue #2133
Normalizes Table10 row heights to match other suit tables

Problem: Table10 (VE cards A-7) has inconsistent row heights:
  - Table10.2: 3.501cm (should be 4.001cm)
  - Table10.3: 4.501cm (should be 4.001cm)

All other suit tables use 4.001cm uniformly for these row types.
This asymmetry causes text overflow in translations with longer text.

Solution: Change both to 4.001cm to match Tables 17,24,31,38,45,52,59,66,73,80,87
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


def normalize_first_suit_table_row_heights(content_root, template_name):
    """
    Normalize the first suit table's inconsistent row heights

    Non-QR templates (Table10): VE cards A-7
      - Table10.2: 3.501cm -> 4.001cm
      - Table10.3: 4.501cm -> 4.001cm

    QR templates (Table11): VE cards A-7 (with QR code rows)
      - Table11.4: 3.501cm -> 4.001cm (appears twice: rows 3 and 6)

    All other suit tables in each variant use 4.001cm uniformly.
    """
    auto_styles = content_root.find(".//office:automatic-styles", NS)
    if auto_styles is None:
        print("  WARNING: No automatic-styles found in content.xml")
        return False

    # Determine template variant by checking for QR in filename
    is_qr = "qr" in template_name.lower()
    
    if is_qr:
        print("\n[Fix] Normalizing Table11 row heights (QR variant)...")
        # QR variant uses Table11 with a different structure
        fixes_applied = 0
        
        # Fix Table11.4: 3.501cm -> 4.001cm
        table11_4 = auto_styles.find('.//style:style[@style:name="Table11.4"]', NS)
        if table11_4 is not None:
            row_props = table11_4.find("style:table-row-properties", NS)
            if row_props is not None:
                current = row_props.get(f'{{{NS["style"]}}}row-height', '')
                if current == "3.501cm":
                    row_props.set(f'{{{NS["style"]}}}row-height', "4.001cm")
                    print(f"  ✓ Table11.4: row-height {current} → 4.001cm")
                    fixes_applied += 1
                else:
                    print(f"  • Table11.4: already {current}")
            else:
                print("  ⚠ Table11.4 has no row-properties")
        else:
            print("  ⚠ Style Table11.4 not found")
        
        if fixes_applied > 0:
            print(f"  ✓ Table11 row height normalized")
            return True
        else:
            print("  ℹ No changes needed or styles not found")
            return False
    else:
        print("\n[Fix] Normalizing Table10 row heights (standard variant)...")
        # Standard variant uses Table10
        fixes_applied = 0
        
        # Fix Table10.2: 3.501cm -> 4.001cm
        table10_2 = auto_styles.find('.//style:style[@style:name="Table10.2"]', NS)
        if table10_2 is not None:
            row_props = table10_2.find("style:table-row-properties", NS)
            if row_props is not None:
                current = row_props.get(f'{{{NS["style"]}}}row-height', '')
                if current == "3.501cm":
                    row_props.set(f'{{{NS["style"]}}}row-height', "4.001cm")
                    print(f"  ✓ Table10.2: row-height {current} → 4.001cm")
                    fixes_applied += 1
                else:
                    print(f"  • Table10.2: already {current}")
        
        # Fix Table10.3: 4.501cm -> 4.001cm
        table10_3 = auto_styles.find('.//style:style[@style:name="Table10.3"]', NS)
        if table10_3 is not None:
            row_props = table10_3.find("style:table-row-properties", NS)
            if row_props is not None:
                current = row_props.get(f'{{{NS["style"]}}}row-height', '')
                if current == "4.501cm":
                    row_props.set(f'{{{NS["style"]}}}row-height', "4.001cm")
                    print(f"  ✓ Table10.3: row-height {current} → 4.001cm")
                    fixes_applied += 1
                else:
                    print(f"  • Table10.3: already {current}")
        
        if fixes_applied == 2:
            print("  ✓ Both row heights normalized to 4.001cm")
            return True
        elif fixes_applied > 0:
            print(f"  ℹ Partial: {fixes_applied}/2 fixes applied")
            return True
        else:
            print("  ℹ No changes needed or styles not found")
            return False





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

    # Apply fix
    fix_ok = normalize_first_suit_table_row_heights(content_root, template_path.name)

    # Save modified XML (only content.xml needs changes)
    content_tree.write(content_xml, encoding="UTF-8", xml_declaration=True)

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

    if fix_ok:
        print("  ✓ Table10 row heights normalized to match other suit tables")
    else:
        print("  ⚠ FAILED: Could not normalize row heights")

    return fix_ok


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
    print("OWASP Cornucopia Issue #2133 - Table10 Row Height Fix")
    print("=" * 80)
    print("\nThis fixes the inconsistent row heights in Table10 (VE cards A-7)")
    print("Normalizes Table10.2 (3.501cm→4.001cm) and Table10.3 (4.501cm→4.001cm)")
    print("to match all other suit tables, preventing text overflow in translations.")
    print("\n" + "=" * 80)

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
    if success_count == len(templates_to_fix):
        print("\nNext steps:")
        print("1. Review fixed templates in output/fixed_templates/")
        print("2. Open in LibreOffice to verify row heights are consistent")
        print("3. Test with: python scripts/convert.py --pdf -lt guide -l en -v 2.2")
        print("4. If verified, replace original templates in resources/templates/")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
