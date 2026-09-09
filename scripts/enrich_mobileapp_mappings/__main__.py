"""Run the Mobile App mapping enrichment module."""

import sys
from pathlib import Path

if __package__ in {None, ""}:  # pragma: no cover
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.enrich_mobileapp_mappings import main  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    main()
