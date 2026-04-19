## Describe the bug

In `scripts/capec_map_enricher.py`, the `extract_capec_names()` function correctly guards against missing top-level keys (`Attack_Pattern_Catalog`, `Attack_Patterns`, `Attack_Pattern`) but then directly accesses `catalog["Categories"]["Category"]` without any guard check. If the CAPEC JSON data has no `"Categories"` key, the script crashes immediately with an unhandled `KeyError`.

## Affected file

`scripts/capec_map_enricher.py` — `extract_capec_names()` function

## Code snippet (problematic section)

```python
# After all the earlier guards for Attack_Pattern...
# Lines ~62-67: NO guard for "Categories" key
categories = catalog["Categories"]["Category"]  # KeyError if "Categories" is absent
for category in categories:
    if "_ID" in category and "_Name" in category:
        capec_id = int(category["_ID"])
        capec_name = category["_Name"]
        capec_names[capec_id] = capec_name
```

## Expected behavior

The function should check for the existence of `"Categories"` and `"Category"` before accessing them, consistent with the defensive guards already applied to `Attack_Pattern_Catalog`, `Attack_Patterns`, and `Attack_Pattern` earlier in the same function. A warning should be logged if absent rather than raising an unhandled exception.

## Proposed fix

```python
if "Categories" not in catalog:
    logging.warning("No 'Categories' key found in catalog")
else:
    categories_section = catalog["Categories"]
    if "Category" not in categories_section:
        logging.warning("No 'Category' key found in categories section")
    elif not isinstance(categories_section["Category"], list):
        logging.warning("'Category' is not a list")
    else:
        for category in categories_section["Category"]:
            if "_ID" in category and "_Name" in category:
                capec_id = int(category["_ID"])
                capec_name = category["_Name"]
                capec_names[capec_id] = capec_name
```

## Steps to reproduce

1. Provide a `3000.json` where `Attack_Pattern_Catalog` has no `"Categories"` key
2. Run: `python scripts/capec_map_enricher.py`
3. Observe unhandled `KeyError: 'Categories'`

## Additional context

This is inconsistent with the existing defensive coding style used for all preceding key accesses in the same function. The fix should follow the same pattern already established.
