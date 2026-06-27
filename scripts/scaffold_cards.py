"""
Scaffold card files from the source/<edition-name>-cards-<version>-<language>.yaml file.

This script takes the yaml file of cards under source directory (e.g. source/eop-cards-5.0-en.yaml) as an argument
and creates the card folders and files including explanation.md and technical-note.md,
inside cornucopia.owasp.org/data/cards/ (e.g. cornucopia.owasp.org/data/cards/eop-cards-5.0-en/)

This is done by reading the cards.yaml and extracting the suit folder name from the meta section
and the card folder name from the id field of each card.

Also, the explanation.md file is populated with the template provided in this script (EXPLANATION_TEMPLATE)

Example:
    python scripts/scaffold_cards.py source/eop-cards-5.0-en.yaml
"""

import sys
import re
import yaml
from pathlib import Path
from typing import Any

EXPLANATION_TEMPLATE = """\
## Scenario: <name>'s ... scenario

### Example

## Threat Modeling

### STRIDE

### What can go wrong?

### What are we going to do about it?
"""

ROOT = Path(__file__).parent.parent / "cornucopia.owasp.org" / "data" / "cards"


def extract_suit_folder_name(name: str) -> str:
    return re.sub(r"\s+", "-", name.strip().lower())


def safe_component(value: str, field: str, pattern: str) -> str:
    if not isinstance(value, str) or re.fullmatch(pattern, value) is None:
        raise ValueError(f"Invalid {field}: {value!r}")
    return value


def _scaffold_card(card: dict[str, Any], suit_dir: Path) -> None:
    if "id" not in card:
        raise ValueError("Missing required field: 'card.id'")
    card_id = safe_component(card["id"], "card.id", r"[A-Z0-9]+")
    card_dir = suit_dir / card_id
    card_dir.mkdir(parents=True, exist_ok=True)
    for filename, content in [("explanation.md", EXPLANATION_TEMPLATE), ("technical-note.md", "")]:
        f = card_dir / filename
        if not f.exists():
            f.write_text(content, encoding="utf-8")


def scaffold_cards(data: dict[str, Any]) -> None:
    if "meta" not in data:
        raise ValueError("Missing required section: 'meta'")
    meta = data["meta"]
    for field in ("edition", "version", "language"):
        if field not in meta:
            raise ValueError(f"Missing required field: 'meta.{field}'")

    edition = safe_component(meta["edition"], "meta.edition", r"[a-z0-9][a-z0-9_-]*")
    version = safe_component(str(meta["version"]), "meta.version", r"[0-9]+(?:\.[0-9]+)*")
    language = safe_component(meta["language"].lower(), "meta.language", r"[a-z]{2}(?:_[a-z]{2})?")
    edition_dir = (ROOT / f"{edition}-cards-{version}-{language}").resolve()
    if not edition_dir.is_relative_to(ROOT.resolve()):
        raise ValueError("Resolved edition directory escapes output root")

    if "suits" not in data:
        raise ValueError("Missing required section: 'suits'")

    for suit in data["suits"]:
        if "name" not in suit:
            raise ValueError("Missing required field: 'suit.name'")
        if "cards" not in suit:
            raise ValueError("Missing required field: 'suit.cards'")

        suit_name = safe_component(extract_suit_folder_name(suit["name"]), "suit.name", r"[a-z0-9&_-]+")
        suit_dir = edition_dir / suit_name
        for card in suit["cards"]:
            _scaffold_card(card, suit_dir)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: scaffold_cards.py <path-to-cards-yaml>")
        sys.exit(1)

    try:
        cards_yaml_path = Path(sys.argv[1])
        data = yaml.safe_load(cards_yaml_path.read_text(encoding="utf-8"))
        scaffold_cards(data)
        print("Done. The card folders have been created.")
    except FileNotFoundError:
        print(f"Error: file not found: {sys.argv[1]}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
