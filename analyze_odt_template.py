#!/usr/bin/env python3
"""
Script to analyze the ODT template structure and identify formatting issues.
Issue #2133: Guide template formatting problems
"""

import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

# Define namespaces used in ODT files
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
}

def analyze_template(template_path):
    """Analyze ODT template for formatting issues"""
    print(f"\nAnalyzing: {template_path.name}")
    print("=" * 80)
    
    with zipfile.ZipFile(template_path) as z:
        # Read content.xml
        with z.open('content.xml') as f:
            content_tree = ET.parse(f)
            content_root = content_tree.getroot()
        
        # Read styles.xml
        with z.open('styles.xml') as f:
            styles_tree = ET.parse(f)
            styles_root = styles_tree.getroot()
    
    # Analyze content structure
    print("\n1. PAGE BREAKS AND SECTIONS")
    print("-" * 40)
    body = content_root.find('.//office:body', NS)
    if body:
        # Check for page breaks
        page_breaks = body.findall('.//text:soft-page-break', NS)
        print(f"Soft page breaks found: {len(page_breaks)}")
        
        # Check paragraph styles with page breaks
        paragraphs_with_breaks = []
        for para in body.findall('.//text:p', NS):
            style_name = para.get('{%s}style-name' % NS['text'])
            if style_name:
                para_text = ''.join(para.itertext()).strip()[:50]
                if para_text:
                    paragraphs_with_breaks.append((style_name, para_text))
        
        print(f"Total paragraphs: {len(paragraphs_with_breaks)}")
        print(f"First few paragraph styles: {paragraphs_with_breaks[:5]}")
    
    # Analyze column layout
    print("\n2. COLUMN LAYOUT")
    print("-" * 40)
    
    # Check master page layout
    master_pages = styles_root.findall('.//style:master-page', NS)
    for mp in master_pages:
        mp_name = mp.get('{%s}name' % NS['style'])
        page_layout = mp.get('{%s}page-layout-name' % NS['style'])
        print(f"Master page: {mp_name}, layout: {page_layout}")
        
    # Check page layouts for column settings
    page_layouts = styles_root.findall('.//style:page-layout', NS)
    for pl in page_layouts:
        pl_name = pl.get('{%s}name' % NS['style'])
        props = pl.find('.//style:page-layout-properties', NS)
        if props is not None:
            width = props.get('{%s}page-width' % NS['fo'])
            height = props.get('{%s}page-height' % NS['fo'])
            orientation = props.get('{%s}print-orientation' % NS['style'])
            print(f"\nPage layout: {pl_name}")
            print(f"  Size: {width} x {height}, Orientation: {orientation}")
            
            # Check for column configuration
            columns = props.find('.//style:columns', NS)
            if columns is not None:
                col_count = columns.get('{%s}column-count' % NS['style'])
                print(f"  Columns: {col_count}")
            else:
                print(f"  Columns: None (single column)")

    # Analyze tables (cards are in tables)
    print("\n3. TABLE STRUCTURE (CARD LAYOUT)")
    print("-" * 40)
    tables = body.findall('.//table:table', NS) if body else []
    print(f"Total tables: {len(tables)}")
    
    for i, table in enumerate(tables[:5]):  # Show first 5 tables
        table_name = table.get('{%s}name' % NS['table'])
        rows = table.findall('.//table:table-row', NS)
        cols = table.findall('.//table:table-column', NS)
        print(f"\nTable {i+1}: {table_name}")
        print(f"  Rows: {len(rows)}, Columns: {len(cols)}")
        
        # Check for suit placeholders
        cells_text = []
        for cell in table.findall('.//table:table-cell', NS):
            cell_text = ''.join(cell.itertext()).strip()
            if '$' in cell_text and 'suit' in cell_text.lower():
                cells_text.append(cell_text[:60])
        
        if cells_text:
            print(f"  Card placeholders found: {len(cells_text)}")
            print(f"  Examples: {cells_text[:2]}")
    
    # Check for section/suit ordering
    print("\n4. SUIT/SECTION ORDERING")
    print("-" * 40)
    suit_references = []
    if body:
        for elem in body.iter():
            text = ''.join(elem.itertext()).strip()
            if '${' in text and 'suit' in text.lower():
                suit_references.append(text[:80])
    
    print(f"Total suit references: {len(suit_references)}")
    if suit_references:
        print(f"First references: {suit_references[:5]}")
        print(f"Last references: {suit_references[-5:]}")
    
    # Check paragraph styles that might control page breaks
    print("\n5. PARAGRAPH STYLES (PAGE BREAK BEHAVIOR)")
    print("-" * 40)
    auto_styles = content_root.find('.//office:automatic-styles', NS)
    if auto_styles:
        for style in auto_styles.findall('.//style:style[@style:family="paragraph"]', NS):
            style_name = style.get('{%s}name' % NS['style'])
            para_props = style.find('.//style:paragraph-properties', NS)
            if para_props is not None:
                break_before = para_props.get('{%s}break-before' % NS['fo'])
                break_after = para_props.get('{%s}break-after' % NS['fo'])
                keep_together = para_props.get('{%s}keep-together' % NS['fo'])
                keep_with_next = para_props.get('{%s}keep-with-next' % NS['fo'])
                
                if any([break_before, break_after, keep_together, keep_with_next]):
                    print(f"\nStyle: {style_name}")
                    if break_before: print(f"  break-before: {break_before}")
                    if break_after: print(f"  break-after: {break_after}")
                    if keep_together: print(f"  keep-together: {keep_together}")
                    if keep_with_next: print(f"  keep-with-next: {keep_with_next}")


def main():
    """Main analysis function"""
    base_path = Path(__file__).parent
    templates_path = base_path / 'resources' / 'templates'
    
    # Analyze both guide templates
    templates_to_analyze = [
        'owasp_cornucopia_webapp_ver_guide_bridge_lang.odt',
        'owasp_cornucopia_webapp_ver_guide_bridge_qr_lang.odt',
    ]
    
    for template_name in templates_to_analyze:
        template_path = templates_path / template_name
        if template_path.exists():
            analyze_template(template_path)
        else:
            print(f"Template not found: {template_path}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    main()
