#!/usr/bin/env python3
"""
Detailed analysis of card ordering and table structure for issue #2133
"""

import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
}

def extract_card_placeholders(template_path):
    """Extract card ordering from template"""
    print(f"\nDetailed Card Analysis: {template_path.name}")
    print("=" * 80)
    
    with zipfile.ZipFile(template_path) as z:
        with z.open('content.xml') as f:
            content_tree = ET.parse(f)
            content_root = content_tree.getroot()
    
    body = content_root.find('.//office:body', NS)
    if not body:
        print("No body found!")
        return
    
    # Find all suits and their ordering
    suit_sections = []
    current_suit = None
    
    for para in body.findall('.//text:p', NS):
        style_name = para.get('{%s}style-name' % NS['text'])
        para_props = content_root.find(f'.//style:style[@style:name="{style_name}"]/style:paragraph-properties', NS)
        has_page_break = False
        if para_props is not None:
            break_before = para_props.get('{%s}break-before' % NS['fo'])
            has_page_break = (break_before == 'page')
        
        text = ''.join(para.itertext()).strip()
        
        # Look for suit indicators
        if '${' in text and '_suit}' in text:
            suit_id = text.split('${')[1].split('_suit}')[0] if '_suit}' in text else None
            if suit_id and suit_id in ['VE', 'AT', 'SM', 'AZ', 'CR', 'C', 'WC']:
                if current_suit != suit_id:
                    suit_sections.append({
                        'suit': suit_id,
                        'has_page_break': has_page_break,
                        'style': style_name,
                        'text_preview': text[:100]
                    })
                    current_suit = suit_id
    
    print("\n1. SUIT ORDERING AND PAGE BREAKS")
    print("-" * 40)
    for i, section in enumerate(suit_sections[:20]):  # Show first 20
        page_break_str = "✓ PAGE BREAK" if section['has_page_break'] else "✗ no break"
        print(f"{i+1}. Suit: {section['suit']:4s} | {page_break_str:15s} | Style: {section['style']}")
    
    # Analyze table structure for card layout
    print("\n2. CARD LAYOUT IN TABLES (Duplex Print Order)")
    print("-" * 40)
    
    tables = body.findall('.//table:table', NS)
    for i, table in enumerate(tables):
        table_name = table.get('{%s}name' % NS['table'])
        
        # Find tables with card data
        card_refs = []
        for cell in table.findall('.//table:table-cell', NS):
            cell_text = ''.join(cell.itertext()).strip()
            # Look for card value references
            if '_VE' in cell_text or '_AT' in cell_text or '_SM' in cell_text:
                for word in cell_text.split('$'):
                    if '_VE' in word or '_AT' in word or '_SM' in word:
                        card_refs.append(word[:30])
        
        if card_refs and len(card_refs) > 10:  # Focus on tables with many cards
            print(f"\nTable: {table_name} (Cards: {len(card_refs)})")
            print(f"  First 10 cards: {card_refs[:10]}")
            print(f"  Last 10 cards: {card_refs[-10:]}")
            
            # Check row structure
            rows = table.findall('.//table:table-row', NS)
            cols = table.findall('.//table:table-column', NS)
            print(f"  Grid: {len(rows)} rows x {len(cols)} columns")
    
    # Check for column break markers
    print("\n3. COLUMN CONFIGURATION")
    print("-" * 40)
    
    # Check automatic styles for multi-column sections
    auto_styles = content_root.find('.//office:automatic-styles', NS)
    if auto_styles:
        for style in auto_styles.findall('.//style:style', NS):
            section_props = style.find('.//style:section-properties', NS)
            if section_props is not None:
                columns = section_props.find('.//style:columns', NS)
                if columns is not None:
                    col_count = columns.get('{%s}column-count' % NS['style'])
                    style_name = style.get('{%s}name' % NS['style'])
                    print(f"Multi-column section found: {style_name}, columns: {col_count}")
    
    # Look for explicit sections
    sections = body.findall('.//text:section', NS)
    print(f"\nExplicit sections in document: {len(sections)}")
    for section in sections:
        section_name = section.get('{%s}name' % NS['text'])
        section_style = section.get('{%s}style-name' % NS['text'])
        print(f"  Section: {section_name}, style: {section_style}")


def main():
    base_path = Path(__file__).parent
    templates_path = base_path / 'resources' / 'templates'
    
    template_name = 'owasp_cornucopia_webapp_ver_guide_bridge_lang.odt'
    template_path = templates_path / template_name
    
    if template_path.exists():
        extract_card_placeholders(template_path)
    else:
        print(f"Template not found: {template_path}")


if __name__ == '__main__':
    main()
