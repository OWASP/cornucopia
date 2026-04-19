## Describe the bug

In `scripts/check_translations.py`, the `get_file_groups()` method splits filenames by `-` and takes `parts[-1]` as the language code, then only includes files where `len(lang) == 2`. This logic breaks entirely for multi-component locale codes like `no-nb`, `pt-pt`, and `pt-br` — which are all listed as supported languages in `LANGUAGE_CHOICES` in `convert.py`.

## Affected file

`scripts/check_translations.py` — `get_file_groups()` method

## Code snippet (problematic section)

```python
def get_file_groups(self) -> Dict[str, List[Path]]:
    file_groups = defaultdict(list)
    for yaml_file in self.source_dir.glob("*-*.yaml"):
        parts = yaml_file.stem.split("-")
        if len(parts) >= 3:
            lang = parts[-1]          # <-- for 'webapp-cards-2.2-no-nb.yaml', lang = 'nb' (WRONG)
            base_name = "-".join(parts[:-1])  # base_name = 'webapp-cards-2.2-no' (WRONG)
            if "cards" in base_name and len(lang) == 2:  # 'nb' passes len check, but base_name is corrupt
                file_groups[base_name].append(yaml_file)
    return file_groups
```

## What happens for `webapp-cards-2.2-no-nb.yaml`

- `parts` = `['webapp', 'cards', '2.2', 'no', 'nb']`
- `lang` = `'nb'` (should be `'no-nb'`)
- `base_name` = `'webapp-cards-2.2-no'` (should be `'webapp-cards-2.2'`)
- This file gets placed into its own broken group `'webapp-cards-2.2-no'`, never compared against the English reference `'webapp-cards-2.2'`

The same problem affects `pt-pt` (lang=`'pt'`, base misidentified) and `pt-br` (lang=`'br'`).

## Expected behavior

Files with multi-component locale codes (`no-nb`, `pt-pt`, `pt-br`) should be correctly grouped with their English base counterpart. The language code should be extracted as the full locale string (e.g., `no-nb`), not just the last hyphen-separated segment.

## Proposed fix

Detect multi-component locale codes explicitly before splitting, for example by checking a known set of multi-part locales:

```python
MULTI_PART_LOCALES = {"no-nb", "pt-pt", "pt-br"}

def get_file_groups(self) -> Dict[str, List[Path]]:
    file_groups = defaultdict(list)
    for yaml_file in self.source_dir.glob("*-*.yaml"):
        if "archive" in str(yaml_file):
            continue
        stem = yaml_file.stem
        lang = None
        base_name = None
        for locale in MULTI_PART_LOCALES:
            if stem.endswith("-" + locale):
                lang = locale
                base_name = stem[: -(len(locale) + 1)]
                break
        if lang is None:
            parts = stem.split("-")
            if len(parts) >= 3:
                lang = parts[-1]
                base_name = "-".join(parts[:-1])
        if base_name and lang and "cards" in base_name and (len(lang) == 2 or lang in MULTI_PART_LOCALES):
            file_groups[base_name].append(yaml_file)
    return file_groups
```

## Additional context

`ConvertVars.LANGUAGE_CHOICES` in `convert.py` explicitly includes `"no-nb"`, `"pt-pt"`, and `"pt-br"`. The translation checker therefore silently skips validation for these locales even though they are officially supported.
