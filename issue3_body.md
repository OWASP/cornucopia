## Describe the bug

In `scripts/convert.py`, the `get_docx_document()` function is supposed to open and return a `.docx` template file. When the file does not exist, it logs an error but **returns a blank `docx.Document()` instead of `None`**. Since a blank `docx.Document()` is always truthy in Python, the caller's `if doc:` check always passes — causing the script to silently replace text in and save an empty document to the output path, producing a corrupted zero-content output file with no further error.

## Affected file

`scripts/convert.py` — `get_docx_document()` and its call site in `create_edition_from_template()`

## Code snippet

```python
def get_docx_document(docx_file: str) -> Any:
    import docx
    if os.path.isfile(docx_file):
        return docx.Document(docx_file)
    else:
        logging.error("Could not find file at: %s", str(docx_file))
        return docx.Document()  # <-- blank Document, always truthy!

# Call site:
doc = get_docx_document(template_doc)
if doc:  # always True — even for a blank Document returned on error
    doc = replace_docx_inline_text(doc, language_dict)
    doc.save(output_file)  # saves an empty file with no content
```

## Expected behavior

When the template file does not exist:
- `get_docx_document()` should return `None`
- The caller should detect `None` and skip the output file creation, or raise a clear error

## Proposed fix

```python
def get_docx_document(docx_file: str) -> Any:
    import docx
    if os.path.isfile(docx_file):
        return docx.Document(docx_file)
    else:
        logging.error("Could not find file at: %s", str(docx_file))
        return None  # caller already checks `if doc:`
```

## Steps to reproduce

1. Specify a non-existent or missing template `.docx` file path
2. Run `python scripts/convert.py -lt cards -l en -v 2.2`
3. No error is raised; an empty `.docx` file is written to the output folder

## Additional context

The docstring does not indicate that a blank fallback document will be returned on failure, making this behavior surprising and hard to diagnose. Returning `None` is cleaner, consistent with the existing `if doc:` guard in the caller, and avoids silently writing corrupt output files.
