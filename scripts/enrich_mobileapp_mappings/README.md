# Mobile App Mapping Enrichment

This module enriches Mobile App Edition card mappings with metadata generated
from the OWASP MASTG and MASWE data:

- MASTG test, knowledge, and best-practice mappings
- MASWE weakness mappings
- MASVS values associated with each referenced MASWE weakness
- MAS threat and attack-vector descriptions

## Usage

Run the module from the repository root:

```bash
python -m scripts.enrich_mobileapp_mappings --help
```

Enrich the default Mobile App Edition mapping in place:

```bash
python -m scripts.enrich_mobileapp_mappings
```

Use explicit input and output paths:

```bash
python -m scripts.enrich_mobileapp_mappings \
  --input-path source/mobileapp-mappings-2.0.yaml \
  --mastg-path source/mobileapp-mastg-2.0.yaml \
  --maswe-path source/mobileapp-maswe-2.0.yaml \
  --output-path source/mobileapp-mappings-2.0-enriched.yaml
```

The default paths are:

| File | Default |
|---|---|
| Card mappings | `source/mobileapp-mappings-2.0.yaml` |
| MASTG metadata | `source/mobileapp-mastg-2.0.yaml` |
| MASWE metadata | `source/mobileapp-maswe-2.0.yaml` |
| Output | The card mappings input file |

For each card, `owasp_maswe` values are matched against the root MASWE codes
in the MASWE metadata file. The card's `owasp_masvs` list is the
source-ordered, deduplicated union of the matching MASWE `owasp_masvs` lists.
It is recomputed on every run, so obsolete values from a previous generated
mapping are removed.
Missing legacy MASWE codes are reported as warnings and do not create
invented mappings.

## Module layout

| File | Responsibility |
|---|---|
| `__init__.py` | Public API and command orchestration |
| `__main__.py` | `python -m scripts.enrich_mobileapp_mappings` entry point |
| `arguments.py` | CLI argument parsing and filename validation |
| `card.py` | Enrichment of one card |
| `document.py` | Validation and enrichment of the card document |
| `mastg.py` | MASTG-derived mappings |
| `maswe.py` | MASWE threat and attack references |
| `masvs.py` | MASVS mappings derived from MASWE |
| `yaml_loader.py` | Safe YAML loading and duplicate-key detection |
| `yaml_output.py` | Stable YAML serialization |
| `utils.py` | Shared list validation and deduplication |

## Validation

From the repository root:

```bash
python -m unittest discover --start-directory tests/scripts \
  --pattern enrich_mobileapp_mappings_utest.py
python -m black --line-length=120 --check .
python -m flake8 --max-line-length=120 --max-complexity=10 \
  --ignore=E203,W503 scripts/enrich_mobileapp_mappings
python -m mypy --namespace-packages --strict scripts/enrich_mobileapp_mappings
python -m coverage run --branch -m unittest tests/scripts/enrich_mobileapp_mappings_utest.py
python -m coverage report --fail-under 95 scripts/enrich_mobileapp_mappings/*.py
```
