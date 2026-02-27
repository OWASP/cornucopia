# tests/scripts/test_card_models.py
import pytest
from scripts.card_models import Card, Suit, Meta, CornucopiaData, ValidationError


class TestCard:
    """Test cases for Card model."""
    
    def test_valid_card(self):
        """Test creating a valid card."""
        data = {
            "id": "VE2",
            "value": "2",
            "url": "https://cornucopia.owasp.org/cards/VE2",
            "desc": "Test description for validation attacks"
        }
        card = Card(**data)
        assert card.id == "VE2"
        assert card.value == "2"
        assert card.url == "https://cornucopia.owasp.org/cards/VE2"
        assert card.desc == "Test description for validation attacks"
        assert card.misc is None
    
    def test_card_with_card_type(self):
        """Test creating a card with card type (e.g., Joker)."""
        data = {
            "id": "JOA",
            "value": "A",
            "url": "https://cornucopia.owasp.org/cards/JOA",
            "desc": "Alice can utilize the application to attack users' systems and data",
            "card": "Joker"
        }
        card = Card(**data)
        assert card.card == "Joker"
    
    def test_card_with_misc(self):
        """Test creating a card with miscellaneous information."""
        data = {
            "id": "VEA",
            "value": "A",
            "url": "https://cornucopia.owasp.org/cards/VEA",
            "desc": "Test description for ace card",
            "misc": "Additional information about this card"
        }
        card = Card(**data)
        assert card.misc == "Additional information about this card"
    
    def test_missing_id(self):
        """Test validation error when id is missing."""
        data = {
            "value": "2",
            "url": "https://cornucopia.owasp.org/cards/VE2",
            "desc": "Test description"
        }
        with pytest.raises(ValidationError) as exc:
            Card(**data)
        assert "id" in str(exc.value)
    
    def test_missing_value(self):
        """Test validation error when value is missing."""
        data = {
            "id": "VE2",
            "url": "https://cornucopia.owasp.org/cards/VE2",
            "desc": "Test description"
        }
        with pytest.raises(ValidationError) as exc:
            Card(**data)
        assert "value" in str(exc.value)
    
    def test_missing_url(self):
        """Test validation error when url is missing."""
        data = {
            "id": "VE2",
            "value": "2",
            "desc": "Test description"
        }
        with pytest.raises(ValidationError) as exc:
            Card(**data)
        assert "url" in str(exc.value)
    
    def test_missing_desc(self):
        """Test validation error when description is missing."""
        data = {
            "id": "VE2",
            "value": "2",
            "url": "https://cornucopia.owasp.org/cards/VE2"
        }
        with pytest.raises(ValidationError) as exc:
            Card(**data)
        assert "desc" in str(exc.value)
    
    def test_short_description(self):
        """Test validation error when description is too short."""
        data = {
            "id": "VE2",
            "value": "2",
            "url": "https://cornucopia.owasp.org/cards/VE2",
            "desc": "Short"
        }
        with pytest.raises(ValidationError) as exc:
            Card(**data)
        assert "desc" in str(exc.value)
    
    def test_invalid_type(self):
        """Test validation error when fields have wrong types."""
        data = {
            "id": 123,  # Should be string
            "value": "2",
            "url": "https://cornucopia.owasp.org/cards/VE2",
            "desc": "Test description for validation attacks"
        }
        with pytest.raises(ValidationError):
            Card(**data)
    
    def test_unknown_field(self):
        """Test validation error when unknown field is present."""
        data = {
            "id": "VE2",
            "value": "2",
            "url": "https://cornucopia.owasp.org/cards/VE2",
            "desc": "Test description for validation attacks",
            "unknown_field": "extra data"
        }
        with pytest.raises(ValidationError) as exc:
            Card(**data)
        assert "extra" in str(exc.value).lower()


class TestSuit:
    """Test cases for Suit model."""
    
    def test_valid_suit(self):
        """Test creating a valid suit."""
        cards = [
            {
                "id": "VE2",
                "value": "2",
                "url": "https://cornucopia.owasp.org/cards/VE2",
                "desc": "Test description for card 2"
            },
            {
                "id": "VE3",
                "value": "3",
                "url": "https://cornucopia.owasp.org/cards/VE3",
                "desc": "Test description for card 3"
            }
        ]
        data = {
            "id": "VE",
            "name": "DATA VALIDATION & ENCODING",
            "cards": cards
        }
        suit = Suit(**data)
        assert suit.id == "VE"
        assert suit.name == "DATA VALIDATION & ENCODING"
        assert len(suit.cards) == 2
        assert suit.cards[0].id == "VE2"
    
    def test_empty_cards(self):
        """Test creating a suit with no cards."""
        data = {
            "id": "VE",
            "name": "DATA VALIDATION & ENCODING",
            "cards": []
        }
        suit = Suit(**data)
        assert len(suit.cards) == 0
    
    def test_missing_id(self):
        """Test validation error when suit id is missing."""
        data = {
            "name": "DATA VALIDATION & ENCODING",
            "cards": []
        }
        with pytest.raises(ValidationError) as exc:
            Suit(**data)
        assert "id" in str(exc.value)


class TestMeta:
    """Test cases for Meta model."""
    
    def test_valid_meta(self):
        """Test creating valid metadata."""
        data = {
            "edition": "webapp",
            "component": "cards",
            "language": "EN",
            "version": "3.0"
        }
        meta = Meta(**data)
        assert meta.edition == "webapp"
        assert meta.component == "cards"
        assert meta.language == "EN"
        assert meta.version == "3.0"
    
    def test_missing_edition(self):
        """Test validation error when edition is missing."""
        data = {
            "component": "cards",
            "language": "EN",
            "version": "3.0"
        }
        with pytest.raises(ValidationError) as exc:
            Meta(**data)
        assert "edition" in str(exc.value)
    
    def test_invalid_language_code(self):
        """Test validation error when language code is too short."""
        data = {
            "edition": "webapp",
            "component": "cards",
            "language": "E",  # Too short
            "version": "3.0"
        }
        with pytest.raises(ValidationError) as exc:
            Meta(**data)
        assert "language" in str(exc.value)


class TestCornucopiaData:
    """Test cases for CornucopiaData model."""
    
    def test_valid_complete_data(self):
        """Test creating valid complete Cornucopia data."""
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
                    "name": "DATA VALIDATION & ENCODING",
                    "cards": [
                        {
                            "id": "VE2",
                            "value": "2",
                            "url": "https://cornucopia.owasp.org/cards/VE2",
                            "desc": "Test description for validation attacks"
                        }
                    ]
                }
            ]
        }
        cornucopia = CornucopiaData(**data)
        assert cornucopia.meta.edition == "webapp"
        assert len(cornucopia.suits) == 1
        assert cornucopia.suits[0].id == "VE"
        assert len(cornucopia.suits[0].cards) == 1
    
    def test_empty_suits(self):
        """Test creating data with no suits."""
        data = {
            "meta": {
                "edition": "webapp",
                "component": "cards",
                "language": "EN",
                "version": "3.0"
            },
            "suits": []
        }
        cornucopia = CornucopiaData(**data)
        assert len(cornucopia.suits) == 0
    
    def test_missing_meta(self):
        """Test validation error when meta is missing."""
        data = {
            "suits": []
        }
        with pytest.raises(ValidationError) as exc:
            CornucopiaData(**data)
        assert "meta" in str(exc.value)
    
    def test_unknown_top_level_field(self):
        """Test that extra top-level fields are allowed."""
        data = {
            "meta": {
                "edition": "webapp",
                "component": "cards",
                "language": "EN",
                "version": "3.0"
            },
            "suits": [],
            "unknown_section": "extra data"
        }
        # This should now pass since we allow extra fields at top level
        cornucopia = CornucopiaData(**data)
        assert cornucopia.meta.edition == "webapp"
        assert len(cornucopia.suits) == 0


class TestRealWorldValidation:
    """Test cases based on real YAML structure."""
    
    def test_realistic_card_structure(self):
        """Test with realistic card data structure."""
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
                    "name": "DATA VALIDATION & ENCODING",
                    "cards": [
                        {
                            "id": "VE2",
                            "value": "2",
                            "url": "https://cornucopia.owasp.org/cards/VE2",
                            "desc": "Brian can gather information about the underlying configurations, schemas, logic, code, software, services and infrastructure due to the content of error messages, or poor configuration, or the presence of default installation files or old, test, backup or copies of resources, or exposure of source code"
                        },
                        {
                            "id": "VEA",
                            "value": "A",
                            "url": "https://cornucopia.owasp.org/cards/VEA",
                            "desc": "You have invented a new attack against Data Validation and Encoding",
                            "misc": "Read more about this topic in OWASP's free Cheat Sheets on Input Validation, XSS Prevention, DOM-based XSS Prevention, SQL Injection Prevention, and Query Parameterization"
                        }
                    ]
                },
                {
                    "id": "AT",
                    "name": "AUTHENTICATION",
                    "cards": [
                        {
                            "id": "AT2",
                            "value": "2",
                            "url": "https://cornucopia.owasp.org/cards/AT2",
                            "desc": "James can undertake authentication functions without the real user ever being aware this has occurred (e.g. attempt to log in, log in with stolen credentials, reset the password)"
                        }
                    ]
                }
            ]
        }
        
        # This should validate successfully
        cornucopia = CornucopiaData(**data)
        assert len(cornucopia.suits) == 2
        assert cornucopia.suits[0].id == "VE"
        assert len(cornucopia.suits[0].cards) == 2
        assert cornucopia.suits[1].id == "AT"
        assert len(cornucopia.suits[1].cards) == 1
        
        # Check the ace card has misc info
        vea_card = next(card for card in cornucopia.suits[0].cards if card.id == "VEA")
        assert vea_card.misc is not None
        assert "OWASP" in vea_card.misc
