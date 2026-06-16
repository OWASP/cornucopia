"""
Scaffold card files from the source/<edition-name>-cards-<version>-<language>.yaml file.

This script takes the yaml file of cards under source directory (e.g. source/eop-cards-5.0-en.yaml) as an argument
and creates the card folders and files including explanation.md and technical-note.md, inside data/cards/
(e.g. data/cards/eop-cards-5.0-en/

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


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: scaffold_cards.py <path-to-cards-yaml>")
        sys.exit(1)

    try:
        data = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
        meta = data["meta"]
        edition_dir = ROOT / f"{meta['edition']}-cards-{meta['version']}-{meta['language'].lower()}"

        for suit in data["suits"]:
            suit_dir = edition_dir / extract_suit_folder_name(suit["name"])
            for card in suit["cards"]:
                card_dir = suit_dir / card["id"]
                card_dir.mkdir(parents=True, exist_ok=True)
                for filename, content in [("explanation.md", EXPLANATION_TEMPLATE), ("technical-note.md", "")]:
                    f = card_dir / filename
                    if not f.exists():
                        f.write_text(content, encoding="utf-8")

        print("Done. The card folders have been created.")
    except FileNotFoundError:
        print(f"Error: file not found: {sys.argv[1]}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
