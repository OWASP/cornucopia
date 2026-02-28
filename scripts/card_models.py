"""Pydantic models for validating YAML card and mapping structures.

This module provides validation models for OWASP Cornucopia YAML files,
ensuring structural integrity while maintaining backward compatibility.
"""

from pydantic import BaseModel, Field, ValidationError, ConfigDict
from typing import Dict, List, Optional, Any


class Card(BaseModel):
    """Minimal validation for card YAML structure.
    
    Validates core required fields while allowing additional fields
    like capec, stride, owasp_asvs, etc. through extra="allow".
    """
    model_config = ConfigDict(extra="allow")
    
    id: str = Field(..., min_length=1, description="Required card ID (e.g. VE2, AT3)")
    value: str = Field(..., min_length=1, description="Required card value (e.g. 2, K, A)")
    desc: str = Field(..., min_length=10, description="Required card description")
    url: Optional[str] = None
    misc: Optional[str] = None


class MappingCard(BaseModel):
    """Minimal validation for mapping card structure.
    
    Mapping files don't have descriptions, only id, value, and mapping data.
    """
    model_config = ConfigDict(extra="allow")
    
    id: str = Field(..., min_length=1, description="Required card ID (e.g. VE2, AT3)")
    value: str = Field(..., min_length=1, description="Required card value (e.g. 2, K, A)")
    url: Optional[str] = None


class Suit(BaseModel):
    """Validation for suit structure.
    
    A suit contains an ID, name, and a collection of cards.
    """
    model_config = ConfigDict(extra="allow")
    
    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    cards: List[Card] = Field(..., min_length=1)


class MappingSuit(BaseModel):
    """Validation for mapping suit structure.
    
    A mapping suit contains an ID, name, and a collection of mapping cards.
    """
    model_config = ConfigDict(extra="allow")
    
    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    cards: List[MappingCard] = Field(..., min_length=1)


class Meta(BaseModel):
    """Validation for metadata section.
    
    Contains edition, component, language, and version information.
    Additional fields like layouts, templates, and languages are allowed.
    """
    model_config = ConfigDict(extra="allow")
    
    edition: str
    component: str
    language: str
    version: str


class CardYAML(BaseModel):
    """Top-level card YAML structure.
    
    Represents the complete structure of a card YAML file,
    including metadata, suits, and optional paragraphs.
    """
    model_config = ConfigDict(extra="allow")
    
    meta: Meta
    suits: List[Suit] = Field(..., min_length=1)


class MappingYAML(BaseModel):
    """Top-level mapping YAML structure.
    
    Represents the complete structure of a mapping YAML file,
    which includes additional mapping information like CAPEC, ASVS, etc.
    """
    model_config = ConfigDict(extra="allow")
    
    meta: Meta
    suits: List[MappingSuit] = Field(..., min_length=1)


# Export ValidationError for convenience
__all__ = ['Card', 'MappingCard', 'Suit', 'MappingSuit', 'Meta', 'CardYAML', 'MappingYAML', 'ValidationError']
