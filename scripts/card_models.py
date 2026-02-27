# scripts/card_models.py
from pydantic import BaseModel, Field, ValidationError, ConfigDict
from typing import Dict, List, Optional, Any


class Card(BaseModel):
    """Individual card model matching Cornucopia YAML structure."""
    model_config = ConfigDict(extra='forbid')
    
    id: str = Field(..., min_length=1, description="Card identifier (e.g., 'VE2', 'ATJ')")
    value: str = Field(..., min_length=1, description="Card value (e.g., '2', '3', 'J', 'Q', 'K', 'A')")
    url: str = Field(..., min_length=1, description="Card URL")
    desc: str = Field(..., min_length=10, description="Card description")
    misc: Optional[str] = Field(None, description="Optional miscellaneous information")
    card: Optional[str] = Field(None, description="Optional card type (e.g., 'Joker')")


class Suit(BaseModel):
    """Suit model containing cards."""
    model_config = ConfigDict(extra='forbid')
    
    id: str = Field(..., min_length=1, description="Suit identifier (e.g., 'VE', 'AT')")
    name: str = Field(..., min_length=1, description="Suit name")
    cards: List[Card] = Field(default_factory=list, description="List of cards in this suit")


class Meta(BaseModel):
    """Metadata model for YAML files."""
    model_config = ConfigDict(extra='forbid')
    
    edition: str = Field(..., min_length=1, description="Edition (e.g., 'webapp', 'mobileapp')")
    component: str = Field(..., min_length=1, description="Component (e.g., 'cards')")
    language: str = Field(..., min_length=2, description="Language code (e.g., 'EN', 'es')")
    version: str = Field(..., min_length=1, description="Version (e.g., '3.0', '1.1')")


class CornucopiaData(BaseModel):
    """Main model for Cornucopia YAML card data."""
    model_config = ConfigDict(extra='allow')  # Allow extra fields at top level
    
    meta: Meta = Field(..., description="File metadata")
    suits: List[Suit] = Field(default_factory=list, description="List of suits containing cards")


# Usage example (for testing):
# validated = CornucopiaData(**yaml_data)
