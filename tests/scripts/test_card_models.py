"""Unit tests for card_models.py Pydantic validation.

This module tests the validation logic for YAML card and mapping structures
to ensure data integrity while maintaining backward compatibility.
"""

import pytest
from scripts.card_models import Card, Suit, Meta, CardYAML, MappingYAML, ValidationError


class TestCardValidation:
    """Test Card model validation"""
    
    def test_valid_minimal_card(self):
        """Valid card with only required fields"""
        data = {
            "id": "VE2",
            "value": "2",
            "desc": "Test description for card validation"
        }
        card = Card(**data)
        assert card.id == "VE2"
        assert card.value == "2"
        assert card.desc == "Test description for card validation"
    
    def test_valid_card_with_optional_fields(self):
        """Valid card with optional fields"""
        data = {
            "id": "VE2",
            "value": "2",
            "desc": "Test description",
            "url": "https://example.com",
            "misc": "Additional info"
        }
        card = Card(**data)
        assert card.url == "https://example.com"
        assert card.misc == "Additional info"
    
    def test_card_with_extra_fields_allowed(self):
        """Extra fields like capec, stride should be allowed"""
        data = {
            "id": "VE2",
            "value": "2",
            "desc": "Test description",
            "capec": [54, 113],
            "stride": ["I"],
            "owasp_asvs": ["2.4.1"]
        }
        card = Card(**data)
        # Should not raise error due to extra="allow"
        assert card.id == "VE2"
    
    def test_missing_required_id(self):
        """Missing required 'id' field"""
        data = {"value": "2", "desc": "Missing ID field"}
        with pytest.raises(ValidationError) as exc:
            Card(**data)
        assert "id" in str(exc.value).lower()
    
    def test_missing_required_value(self):
        """Missing required 'value' field"""
        data = {"id": "VE2", "desc": "Missing value field"}
        with pytest.raises(ValidationError) as exc:
            Card(**data)
        assert "value" in str(exc.value).lower()
    
    def test_missing_required_desc(self):
        """Missing required 'desc' field"""
        data = {"id": "VE2", "value": "2"}
        with pytest.raises(ValidationError) as exc:
            Card(**data)
        assert "desc" in str(exc.value).lower()
    
    def test_desc_too_short(self):
        """Description shorter than minimum length"""
        data = {"id": "VE2", "value": "2", "desc": "short"}
        with pytest.raises(ValidationError) as exc:
            Card(**data)
        assert "desc" in str(exc.value).lower()
    
    def test_invalid_type_id(self):
        """Invalid type for 'id' field"""
        data = {"id": 123, "value": "2", "desc": "Test description"}
        with pytest.raises(ValidationError):
            Card(**data)


class TestSuitValidation:
    """Test Suit model validation"""
    
    def test_valid_suit(self):
        """Valid suit with cards"""
        data = {
            "id": "VE",
            "name": "Data Validation",
            "cards": [
                {"id": "VE2", "value": "2", "desc": "Test card description"}
            ]
        }
        suit = Suit(**data)
        assert suit.id == "VE"
        assert len(suit.cards) == 1
    
    def test_suit_missing_cards(self):
        """Suit without cards should fail"""
        data = {"id": "VE", "name": "Data Validation", "cards": []}
        with pytest.raises(ValidationError):
            Suit(**data)
    
    def test_suit_with_invalid_card(self):
        """Suit with invalid card should fail"""
        data = {
            "id": "VE",
            "name": "Data Validation",
            "cards": [{"id": "VE2"}]  # Missing required fields
        }
        with pytest.raises(ValidationError):
            Suit(**data)


class TestMetaValidation:
    """Test Meta model validation"""
    
    def test_valid_meta(self):
        """Valid metadata"""
        data = {
            "edition": "webapp",
            "component": "cards",
            "language": "EN",
            "version": "3.0"
        }
        meta = Meta(**data)
        assert meta.edition == "webapp"
    
    def test_missing_edition(self):
        """Missing required 'edition' field"""
        data = {"component": "cards", "language": "EN", "version": "3.0"}
        with pytest.raises(ValidationError):
            Meta(**data)


class TestCardYAMLValidation:
    """Test full CardYAML structure"""
    
    def test_valid_card_yaml(self):
        """Complete valid card YAML"""
        data = {
            "meta": {
                "edition": "webapp",
                "component": "cards",
                "language": "EN",
                "version": "3.0"
            },
            "suits": [
                {
                    "id": "VE",
                    "name": "Data Validation",
                    "cards": [
                        {"id": "VE2", "value": "2", "desc": "Test description"}
                    ]
                }
            ]
        }
        card_yaml = CardYAML(**data)
        assert card_yaml.meta.edition == "webapp"
        assert len(card_yaml.suits) == 1
    
    def test_card_yaml_with_paragraphs(self):
        """CardYAML with extra 'paragraphs' field"""
        data = {
            "meta": {
                "edition": "webapp",
                "component": "cards",
                "language": "EN",
                "version": "3.0"
            },
            "suits": [
                {
                    "id": "VE",
                    "name": "Data Validation",
                    "cards": [
                        {"id": "VE2", "value": "2", "desc": "Test description"}
                    ]
                }
            ],
            "paragraphs": ["Some extra content"]
        }
        card_yaml = CardYAML(**data)
        # Should not fail due to extra="allow"
        assert card_yaml.meta.edition == "webapp"


class TestMappingYAMLValidation:
    """Test MappingYAML structure"""
    
    def test_valid_mapping_yaml(self):
        """Complete valid mapping YAML"""
        data = {
            "meta": {
                "edition": "webapp",
                "component": "mappings",
                "language": "ALL",
                "version": "3.0",
                "layouts": ["cards"],
                "templates": ["bridge"]
            },
            "suits": [
                {
                    "id": "VE",
                    "name": "Data Validation",
                    "cards": [
                        {
                            "id": "VE2",
                            "value": "2",
                            "desc": "Test description for mapping",
                            "capec": [54, 113],
                            "owasp_asvs": ["2.4.1"]
                        }
                    ]
                }
            ]
        }
        mapping_yaml = MappingYAML(**data)
        assert mapping_yaml.meta.component == "mappings"
