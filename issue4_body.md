## Describe the bug

In `scripts/convert_asvs.py`, the `create_level_summary()` function opens a file using `f = open(...)` without a `with` context manager. If any exception is raised inside the loop body (e.g., a missing dictionary key during iteration), the file handle `f` is never explicitly closed, leaking the OS file descriptor. On batch runs that generate many ASVS taxonomy pages, this can exhaust system file handle limits.

## Affected file

`scripts/convert_asvs.py` — `create_level_summary()` function (and similar patterns elsewhere in the file)

## Code snippet (problematic section)

```python
def create_level_summary(level: int, arr: List[dict[str, Any]]) -> None:
    topic = ""
    category = ""
    os.mkdir(Path(convert_vars.args.output_path, f"level-{level}-controls"))
    f = open(Path(convert_vars.args.output_path, f"level-{level}-controls/index.md"), "w", encoding="utf-8")
    # ^ File opened without 'with' — if any exception occurs below, f is never closed
    f.write(f"# Level {level} controls\n\n")
    f.write(f"Level {level} contains {len(arr)} controls listed below: \n\n")
    for link in arr:
        if link["topic"] != topic:          # KeyError here would leak file handle
            topic = link["topic"]
            f.write(f"## {topic}\n\n")
        ...
    f.close()  # only reached if no exception — not guaranteed
```

## Expected behavior

All file handles opened by the script should use `with open(...) as f:` context manager so that the file is guaranteed to be closed even if an exception is raised within the block.

## Proposed fix

```python
def create_level_summary(level: int, arr: List[dict[str, Any]]) -> None:
    topic = ""
    category = ""
    os.mkdir(Path(convert_vars.args.output_path, f"level-{level}-controls"))
    with open(Path(convert_vars.args.output_path, f"level-{level}-controls/index.md"), "w", encoding="utf-8") as f:
        f.write(f"# Level {level} controls\n\n")
        f.write(f"Level {level} contains {len(arr)} controls listed below: \n\n")
        for link in arr:
            if link["topic"] != topic:
                topic = link["topic"]
                f.write(f"## {topic}\n\n")
            ...
```

The same pattern should be applied to other `open()` calls in `scripts/convert_asvs.py` and `scripts/convert_capec.py` that do not use `with` statements.

## Additional context

Python's `with` statement is the standard and recommended way to handle file I/O. Using bare `open()`/`f.close()` pairs is error-prone; if any code path between `open()` and `close()` raises an exception, the file is never properly flushed and closed. This is a well-known resource leak anti-pattern (CWE-775: Missing Release of File Descriptor or Handle after Effective Lifetime).
