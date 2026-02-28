"""Integration tests for card_models.py with actual YAML files.

This module tests Pydantic validation against real project YAML files
to ensure compatibility with existing data structures.
"""

import pytest
import yaml
import os
from scripts.card_models import CardYAML, MappingYAML, ValidationError
from scripts import convert as c

# Initialize convert_vars for tests
c.convert_vars = c.ConvertVars()


class TestRealFileValidation:
    """Test validation against actual project YAML files"""
    
    def test_validate_real_card_file(self):
        """Validate an actual card YAML file"""
        card_file = os.path.join(
            c.convert_vars.BASE_PATH,
            "source",
            "webapp-cards-3.0-en.yaml"
        )
        
        with open(card_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        # Should not raise ValidationError
        validated = CardYAML(**data)
        assert validated.meta.edition == "webapp"
        assert validated.meta.version == "3.0"
        assert len(validated.suits) > 0
    
    def test_validate_real_mapping_file(self):
        """Validate an actual mapping YAML file"""
        mapping_file = os.path.join(
            c.convert_vars.BASE_PATH,
            "source",
            "webapp-mappings-3.0.yaml"
        )
        
        with open(mapping_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        # Should not raise ValidationError
        validated = MappingYAML(**data)
        assert validated.meta.component == "mappings"
        assert len(validated.suits) > 0
    
    def test_invalid_card_structure(self):
        """Test that invalid structures are caught"""
        invalid_data = {
            "meta": {
                "edition": "webapp",
                "component": "cards",
                "language": "EN",
                "version": "3.0"
            },
            "suits": [
                {
                    "id": "VE",
                    "name": "Test",
                    "cards": [
                        {"id": "VE2"}  # Missing required fields
                    ]
                }
            ]
        }
        
        with pytest.raises(ValidationError):
            CardYAML(**invalid_data)
    
    def test_validate_multiple_card_files(self):
        """Validate multiple card files from different editions and languages"""
        test_files = [
            "webapp-cards-2.2-en.yaml",
            "webapp-cards-3.0-en.yaml",
            "mobileapp-cards-1.1-en.yaml",
        ]
        
        for filename in test_files:
            card_file = os.path.join(
                c.convert_vars.BASE_PATH,
                "source",
                filename
            )
            
            if not os.path.exists(card_file):
                pytest.skip(f"Test file {filename} not found")
            
            with open(card_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            # Should validate without errors
            validated = CardYAML(**data)
            assert validated.meta is not None
            assert len(validated.suits) > 0
    
    def test_validate_all_cards_in_suit(self):
        """Ensure all cards in a real file have required fields"""
        card_file = os.path.join(
            c.convert_vars.BASE_PATH,
            "source",
            "webapp-cards-3.0-en.yaml"
        )
        
        with open(card_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        validated = CardYAML(**data)
        
        for suit in validated.suits:
            assert len(suit.cards) > 0
            for card in suit.cards:
                # All required fields must be present
                assert card.id is not None
                assert card.value is not None
                assert card.desc is not None
                assert len(card.desc) >= 10
